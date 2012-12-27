page-rank
=========

A very simple version/implementation of the page rank algorithm.

functions:

 - Page rank
 - Advanced version of page rank, topic sensitive
 - spam farms
 - spam mass
 - trust rank
 - Hiperlink induced topic search
 - Map reduce to efficiently calculates the page rank
 - Jaccard simiarity to be found in data analysis repo


implementation using list and matrix from the **numpy** library.


Calculation workflow : 

 1. Parse web pages for links
 2. Parse links
 3. Compute page rank  (iterate until convergence)
 4. Sort by page rank
 5. Create index
