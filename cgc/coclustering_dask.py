import numpy as np

import dask.array as da
from dask.distributed import get_client, rejoin, secede


def _distance(Z, X, Y, epsilon):
    """ Distance function """
    Y = Y + epsilon
    d = da.dot(X, Y) - da.dot(Z, da.log(Y))
    return d


def _initialize_clusters(n_el, n_clusters):
    """ Initialize cluster array """
    cluster_idx = da.mod(da.arange(n_el), n_clusters)
    return da.random.permutation(cluster_idx)


def _setup_cluster_matrix(n_clusters, cluster_idx):
    """ Set cluster occupation matrix """
    # TODO: check if Z shape is larger than max int32?
    return da.eye(n_clusters, dtype=np.int32)[cluster_idx]


def coclustering(Z, nclusters_row, nclusters_col, errobj, niters, epsilon,
                 col_clusters_init=None, row_clusters_init=None,
                 run_on_worker=False):
    """
    Run the co-clustering, Dask implementation

    :param Z: m x n data matrix
    :param nclusters_row: num row clusters
    :param nclusters_col: number of column clusters
    :param errobj: convergence threshold for the objective function
    :param niters: maximum number of iterations
    :param epsilon: numerical parameter, avoids zero arguments in log
    :param row_clusters_init: initial row cluster assignment
    :param col_clusters_init: initial column cluster assignment
    :param run_on_worker: whether the function is submitted to a Dask worker
    :return: has converged, number of iterations performed. final row and
    column clustering, error value
    """
    client = get_client()

    [m, n] = Z.shape

    row_clusters = row_clusters_init if row_clusters_init is not None \
        else _initialize_clusters(m, nclusters_row)
    col_clusters = col_clusters_init if col_clusters_init is not None \
        else _initialize_clusters(n, nclusters_col)
    R = _setup_cluster_matrix(nclusters_row, row_clusters)
    C = _setup_cluster_matrix(nclusters_col, col_clusters)

    e, old_e = 2 * errobj, 0
    s = 0
    converged = False

    Gavg = Z.mean()

    while (not converged) & (s < niters):
        # Calculate cluster based averages
        CoCavg = (da.dot(da.dot(R.T, Z), C) + Gavg * epsilon) / (
            da.dot(da.dot(R.T, da.ones((m, n))), C) + epsilon)

        # Calculate distance based on row approximation
        d_row = _distance(Z, da.ones((m, n)), da.dot(C, CoCavg.T), epsilon)
        # Assign to best row cluster
        row_clusters = da.argmin(d_row, axis=1)
        R = _setup_cluster_matrix(nclusters_row, row_clusters)

        # Calculate distance based on column approximation
        d_col = _distance(Z.T, da.ones((n, m)), da.dot(R, CoCavg), epsilon)
        # Assign to best column cluster
        col_clusters = da.argmin(d_col, axis=1)
        C = _setup_cluster_matrix(nclusters_col, col_clusters)

        # Error value (actually just the column components really)
        old_e = e
        minvals = da.min(d_col, axis=1)
        # power 1 divergence, power 2 euclidean
        e = da.sum(da.power(minvals, 1))
        row_clusters, col_clusters, e = client.persist([row_clusters,
                                                        col_clusters,
                                                        e])
        if run_on_worker:
            # this is workaround for e.compute() for a function that runs
            # on a worker with multiple threads
            # https://github.com/dask/distributed/issues/3827
            e = client.compute(e)
            secede()
            e = e.result()
            rejoin()
        else:
            e.compute()

        converged = abs(e - old_e) < errobj
        s = s + 1

    return converged, s, row_clusters, col_clusters, e
