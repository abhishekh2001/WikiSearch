# IRE - Mini Project

## Directory structure
The code is structured as follows -
```
├── config.py
├── file_handling
│   └── combine.py
├── indexer
│   ├── indexer.py
│   └── wikipedia_handler.py
├── index.sh
├── ind.py
├── parser.py
├── readme.MD
├── requirements.txt
├── searcher
│   ├── compute_doclist.py
│   └── search.py
├── srch.py
```

* `searcher/` implements the search features.
* `indexer/` implements the indexing
* `combine.py` merges the intermediary index files into the final product
* `ind.py` controls the indexing procedure
* `srch.py` controls the search operations

To generate the index, 

```./index.sh <dataset> <target folder> stats.txt```

To perform the queries,

```python srch.py queries.txt```

## Optimizations used

* Search can easily be multi-threaded.
* While creating the index, processing can be parallelized by reading chunks of the document at a time and generating the index. 
* Used higher compression to save on disk space.
* Merging intermediary files has been performed with the help of k-way merge.

## Format of the index

Each dictionary file has some constant number of tokens (keys) and their respective values.
The format is `token:d<d>t<t>i<i>b<b>c<c>r<r>` where `<x>` is the number of times the token appears for that field.


