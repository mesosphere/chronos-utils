chronos-utils
=============

Command line utilities for interacting with Chronos

```
./chronos.py -h
usage: chronos.py [-h]

Supported chronos commands are:
    job    Create dummy jobs

optional arguments:
  -h, --help  show this help message and exit
```

### chronos-job.py

Generate dummy sleep jobs on a local Chronos instance for testing purposes.

```
./chronos.py job -h
usage: chronos-job [-h] [-n N]

optional arguments:
  -h, --help  show this help message and exit
  -n N        number of Chronos jobs to create (default: 1)
```
