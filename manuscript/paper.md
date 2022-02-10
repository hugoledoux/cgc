---
title: 'CGC: a scalable Python package for co- and tri-clustering of geo-data cubes'
tags:
  - Python
  - clustering
  - co-clustering
  - tri-clustering
  - geospatial
authors:
  - name: Francesco Nattino
    orcid: 0000-0003-3286-0139
    affiliation: "1" # (Multiple affiliations must be quoted)
  - name: Ou Ku 
    orcid: 0000-0002-5373-5209
    affiliation: "1"
  - name: Meiert W. Grootes 
    orcid: 0000-0002-5733-4795
    affiliation: "1"
  - name: Emma Izquierdo-Verdiguier
    orcid: 0000-0003-2179-1262
    affiliation: "2"
  - name: Serkan Girgin
    orcid: 0000-0002-0156-185X
    affiliation: "3"
  - name: Raul Zurita-Milla
    orcid: 0000-0002-1769-6310
    affiliation: "3"
affiliations:
 - name: Netherlands eScience Center, Science Park 140, 1098 XG Amsterdam, The Netherlands
   index: 1
 - name: Institute of Geomatics, University of Natural Resources and Life Science (BOKU), 1190, Vienna, Austria
   index: 2
 - name: Faculty of Geo-Information Science and Earth Observation (ITC), University of Twente, PO Box 217, 7500 AE, Enschede, the Netherlands
   index: 3
date: 17 December 2021
bibliography: paper.bib
---
# Summary

Multidimensional data cubes are increasingly ubiquitous, in particular in the geosciences. Clustering techniques encompassing their full dimensionality are necessary to identify patterns "hidden" within these cubes. Clustering Geodata Cubes (CGC) is a Python package designed for partitional clustering, which identifies groups of similar data across two (e.g., spatial and temporal) or three (e.g., spatial, temporal, and thematic) dimensions. CGC provides efficient and scalable co- and tri-clustering functionality appropriate to analyze both small and large datasets as well as a cluster refinement functionality that supports users in their quest to make sense of complex datasets.   


# Introduction

Faced with the increasing ubiquity of large datasets, data mining techniques have become essential to extracting patterns and generating insights. In this regard, clustering techniques, which aim to identify groups or subgroups with similar properties within a larger data set, are becoming ever more popular.

Traditional clustering techniques focus on a single dimension and may therefore obfuscate relevant groups [@Hartigan:1972;@Cheng:2000]. Hence, clustering techniques capable of simultaneously grouping data along multiple dimensions are needed. These techniques - referred to as co- or bi-clustering and tri-clustering in the case of two and three dimensions, respectively - have seen significant development and adoption in fields ranging from bioinformatics [@Cheng:2000] to finance [@Shi:2018] and natural language processing [@Dhillon:2001].

The exponential growth of multidimensional data referring to geographical features (e.g., time series of satellite images) has resulted in a wide variety of geo-data cubes, which can benefit from co- and tri-clustering. Indeed, following the development of a general information-theoretical approach [@Dhillon:2003] to partitional co-clustering [@Banerjee:2007], Wu et al. presented an application of co-clustering to geo-data [@Wu:2015], as well as its extension to three dimensions [@Wu:2018]. 

In light of the eminent employability of co- and tri-clustering approaches to geospatial disciplines like geo-information science and Earth observation, and the transferability to other (geo)scientific domains, this paper presents the Clustering Geo-data Cubes (CGC) package. 

As outlined below, the package aims to meet the needs of geospatial data scientists. An example of its application is the ongoing work on the analysis of spring onset datasets at high spatial resolution and continental scale, a preview of which is presented in the CGC tutorial. Nevertheless, the algorithms implemented in the CGC package - performing partitional clustering of positive data matrices - remain widely applicable and can easily be applied in other domains.


# Statement of need 

The CGC package focuses on the needs of geospatial data scientists who require tools to make sense of multi-dimensional data cubes by providing the following features and functionalities:

- **Partitional co- and tri-clustering methods suitable for spatiotemporal (multi-dimensional) data.** 
  CGC includes clustering methods designed to simultaneously group elements into disjoint clusters along two or three dimensions. These methods are advantageous over one-dimensional clustering in that they provide a strategy to identify patterns that unfold across multiple dimensions (e.g. space and time). In addition, CGC provides functionality to refine the identified co- and tri-clusters. This post-processing step reduces the number of clusters to facilitate the identification and visualization of patterns.
 
- **Scalable clustering of small and big data sets.**
  CGC offers functionality to efficiently utilize available computational resources (ranging from single machines to computing clusters) and to tackle a wide range of data set sizes. For single machine execution the package offers optimized support of multi-core CPUs and/or system memory. For large data sets CGC supports the use of distributed data and computation on computing clusters

- **Easy integration into geospatial analysis workflows.** 
  CGC is written in Python, which is widely used for geospatial scripting and applications, and employs Numpy and Dask [@Dask:2016] arrays as input and output data types, guaranteeing seamless integration to the Python ecosystem and interoperability with the Dask library prevalent in the field of big geo-data. This furthermore ensures the interoperability of CGC with the Xarray package [@Hoyer:2017], so that this versatile 
  and popular tool can be used for data loading and manipulation before and after analyses with CGC.

- **Ease of use and reproducibility.**
  To facilitate community use and adoption, documentation and tutorials illustrating domain-science examples, applications, and use cases are available via the [publicly accessible repository](https://github.com/phenology/cgc), where development takes place, and which provides a platform for issue tracking. CGC is distributed via the 
  Python Package Index (PyPI), and code-release snapshots archived on Zenodo facilitate reproducible analysis.


# Algorithms

## Co-clustering

CGC implements the Bregman block average co-clustering (BBAC) algorithm from @Banerjee:2007 as inspired by the MATLAB code of [@Merugu:2004].
Briefly, the BBAC algorithm iteratively optimizes the clustering of rows and columns of a data matrix starting from a random initial assignment until convergence. The information loss from the original matrix to the clustered one, which is constructed as the matrix of the co-cluster means, is minimized using a loss function that is based on the I-divergence. CGC also supports a user defined convergence threshold. To limit the influence of the initial conditions on the final clustering and to avoid local minima several runs are carried out, with the cluster assignments from the lowest loss function value ultimately being selected.

Note that in the CGC implementation of the algorithm, the update in the row- and column-cluster assignments is computed only from the previous iteration’s row and column. Contrarily to the original MATLAB implementation [@Merugu:2004], this makes the algorithm independent of the order in which the dimensions are considered, while still leading to an optimal clustering solution. 


## Tri-clustering

For tri-clustering CGC implements the so-called Bregman cube average tri-clustering (BCAT) algorithm, which is the natural generalization of the BBAC algorithm to three dimensions [@Wu:2018]. The algorithmic implementation with respect to the loss function and the update schema are analogous to that described above for the co-clustering. Importantly, the tri-clustering outcome is independent of the order in which the three dimensions of the input array are provided.


## Cluster refinement

The CGC package implements an optional, secondary cluster refinement step based on the k-means method [@Wu:2016] and optimized using the Silhouette metric [@Rousseeuw:1987] as implemented in the scikit-learn package [@Pedregosa:2011]. This secondary grouping is based on statistical properties of the co- or tri-clusters (see the [package documentation](https://cgc.readthedocs.io)) and helps to better capture patterns in the data by combining clusters and going beyond strict checkerboard structures.  


# Related Software

A number of co-/bi-clustering implementations based on a range of algorithms exist. While some of the available packages
focus on specific applications, like gene expression data [@Barkow:2006;@Eren:2012], generic co-clustering tools include biclust 
(R) and CoClust (Python) [@Role:2019], as well as two implementations from the scikit-learn Python library [@Pedregosa:2011]. 
However, most of the available algorithms target tabular data with a hidden blocked-diagonal structure, 
where each row and column of the input matrix is assigned to only one co-cluster. In contrast, in spatio-temporal data a
set of spatial elements often exhibits the same behaviour within multiple time windows and vice versa. This type of data 
requires algorithms where a subset taken along one dimension can be associated to multiple subsets taken along the other
dimension. Partitioning algorithms of this type, such as the BBAC and BCAT algorithms implemented in CGC, can discover 
checkerboard-like patterns in the input data matrix, although the CGC package additionally enables the user to recover 
more of the intrinsic structure of the data in a second step, going beyond the limits on structure imposed 

Within the Python ecosystem, prominent implementations targeting checkerboard-like structures akin to CGC's intial step are the 
scikit-learn SpectralBiclustering algorithm, which implements the method from [@Kluger:2003], and the CoclustInfo 
algorithm from CoClust, also based on information-theoretic co-clustering [@Dhillon:2003;@Govaert:2018]. However, both 
approaches differ from CGC in the field of applicability. Spectral methods like the former are fast, but their accuracy 
has been shown to be limited [@Ailem:2015;@Role:2019]. The latter focuses on datasets representing joint-probability 
distributions, preserving statistics other than the co-cluster average (the row and column averages) in the search for 
the optimal clustering solution [@Banerjee:2007]. This requirement does not generally apply to the geospatial datasets
which CGC is targeting. Neither, however, offers the ability to "break out" of the algorithmically-imposed checkerboard 
pattern.

Finally, to the best of our knowledge, CGC is unique in being designed from the outset for use with 'big data' (e.g. by 
including an implementation that supports distributed data) and in being able to analyze more complex data cubes via 
tri-clustering.

# Software package overview 

The CGC software is structured in the following main modules, details of which are described in the 
[online package documentation](https://cgc.readthedocs.io):

- [`coclustering`](https://cgc.readthedocs.io/en/latest/coclustering.html#), containing the following implementations of the co-clustering algorithm:

    - The [Numpy-based, vectorized single machine implementation with threading support for optimal usage of multi-core CPUs.](https://cgc.readthedocs.io/en/latest/coclustering.html#local-numpy-based)

    - The [Numpy-based single machine implementation with a reduced memory footprint](https://cgc.readthedocs.io/en/latest/coclustering.html#local-numpy-based-low-memory-footprint). This implementation trades performance for low memory usage, but uses Numba's
       just-in-time compilation to mitigate performance loss.

    - The [Dask-library-based implementation](https://cgc.readthedocs.io/en/latest/coclustering.html#distributed-dask-based). This 
      implementation provides support for clustering large, out-of-core data sets by distributing the computation across multiple nodes using Dask arrays. 

      
- [`triclustering`](https://cgc.readthedocs.io/en/latest/triclustering.html), containing the following tri-clustering 
  implementations:

    - A [Numpy-based implementation](https://cgc.readthedocs.io/en/latest/triclustering.html#local-numpy-based) 
      analogous to the co-clustering one described above (note that the low-memory version is currently not available).
    - A [Dask-based implementation](https://cgc.readthedocs.io/en/latest/triclustering.html#distributed-dask-based), 
      also analogous to the corresponding co-clustering version described above. 

- [`kmeans`](https://cgc.readthedocs.io/en/latest/kmeans.html), which implements the k-means cluster refinement step for 
  both co- and tri-clustering.

- [`utils`](https://https://cgc.readthedocs.io/en/latest/utils.html), which includes a collection of utility functions e.g., memory consumption estimation and cluster averaging. 
 
Performance comparisons between the various [co-clustering](https://cgc.readthedocs.io/en/latest/coclustering.html#performance-comparison) 
and [tri-clustering](https://cgc.readthedocs.io/en/latest/triclustering.html#performance-comparison) implementations are 
also briefly discussed in the package documentation. 

# Tutorial 
	
The software package is complemented by an [online tutorial](https://cgc-tutorial.readthedocs.io) (in the form of Jupyter notebooks [@Kluyver:2016]) that illustrates how to perform cluster analysis of geospatial datasets using CGC. Notebooks are made directly available via a 
[dedicated GitHub repository](https://github.com/esciencecenter-digital-skills/tutorial-cgc), and are also 
published as [static web pages](https://cgc-tutorial.readthedocs.io) for reference and linked to the 
[CGC documentation](https://cgc.readthedocs.io) via a 'Tutorials' tab. The tutorials are designed to run on systems with 
limited CPU/memory capacity, which, together with environment requirement specifications in a standardized format 
(`conda` YAML file) and binder badges, give users the possibility to easily run the notebooks live on 
`mybinder.org` [@Jupyter:2018].

Tutorials cover the following topics:

- Co- and tri-cluster analysis. 
- K-means-based cluster refinement.
- Choice of the suitable implementation for a given problem size/infrastructure available.
- Loading of geospatial data, common data-manipulation tasks in a workflow involving CGC, visualization of the output. 

Note they while the tutorial is aimed at geospatial uses cases, it illustrates some real-case applications that are 
likely to make it easier for users to carry out cluster analysis using CGC in other fields as well. 
 

# Acknowledgements

The authors would like to thank Dr. Yifat Dzigan for the helpful discussions and support and Dr. Romulo Goncalves for the 
preliminary work that led to the development of the software package presented here. We also would like to thank SURF for providing computational resources to test the first versions of the CGC package via the e-infra190130 grant.  
 

# Author contributions 

All co-authors contributed to the conceptualization of the work, which was led by R.Z.M. and E.I.V.. F.N., M.W.G., and O.K. prepared the first draft of the tutorials, and wrote the initial draft of this manuscript. F.N. suggested changes to the co- and tri-clustering algorithms. R.Z.M., E.I.V., and S.G. led the design of experiments to test and improve the CGC package. R.Z.M. and E.I.V. helped to improve the tutorials. S.G. provided the required computational resources to run the experiments and tutorials and made suggestions for code optimizations. All co-authors reviewed and edited the final document.  

# References
