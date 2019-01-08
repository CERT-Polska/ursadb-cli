UrsaDB Client
=============

A command line client for `ursadb`. Usage:

```
usage: ursaclient.py [-h] [--cmd [CMD]] [db_url]

Communicate with UrsaDB.

positional arguments:
  db_url

optional arguments:
  -h, --help   show this help message and exit
  --cmd [CMD]  execute provided command, print results and terminate
```


Full package installation
-------------------------

This repository is only for UrsaDB project (n-gram database). In order to see instructions on how to set up
the whole mquery system, see [CERT-Polska/mquery](https://github.com/CERT-Polska/mquery).


Querying database
-----------------

Query language is described in [CERT-Polska/ursadb](https://github.com/CERT-Polska/ursadb) repository.


Exemplary applications
----------------------

### Indexing Cuckoo's dumps
```
URSADB_URL=tcp://localhost:9281
CUCKOO_ANALYSES=storage/analyses
find $(readlink -f "$CUCKOO_ANALYSES") -maxdepth 2 -type d -name dumps > /tmp/ursadb-list.txt
python3 ursaclient.py --cmd 'index from list "/tmp/ursadb-list.txt";' $URSADB_URL
```
