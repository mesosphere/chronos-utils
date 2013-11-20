chronos-utils
=============

Command line utilities for interacting with Chronos

### `chronos`

Forward commands to other files in the directory. New commands should be added
to the command description in this file.

```
./chronos.py -h
usage: chronos [-h] <command>

Supported chronos commands are:
  jobs   Create, destroy, and list jobs

positional arguments:
  <command>   this is it, the command to execute

optional arguments:
  -h, --help  show this help message and exit
```

### `chronos-jobs`

Create, destroy, and list jobs

```
./chronos.py jobs -h
usage: chronos-jobs [-h] [--hostname <host:port>]
                    (--create [<n>] | --delete <jobname> | --deleteall | --list)

optional arguments:
  -h, --help            show this help message and exit
  --hostname <host:port>
                        hostname of the Chronos instance
  --create [<n>]        create <n> sleep jobs (default: 1)
  --delete <jobname>    delete job with name <jobname>
  --deleteall           delete all jobs (this is serious business)
  --list                list all jobs
```
