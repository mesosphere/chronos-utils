chronos-utils
=============

Command line utilities for interacting with
[Airbnb Chronos](https://github.com/airbnb/chronos). Check out the [full reference](#full-reference) below for all available commands.

## First, a demonstration

This demonstrates creating jobs, deleting a single job, deleting all the jobs, and listing jobs from the command line.

    $ ./chronos.py jobs --create 3
    Created 3 job(s) on local Chronos

    $ ./chronos.py jobs --list
    +------------------+--------------+------------------------------------+
    |       Name       |    Owner     |              Schedule              |
    +==================+==============+====================================+
    | JOB1386714810695 | rob@fake.com | R/2013-12-10T22:33:30.695273/PT24H |
    +------------------+--------------+------------------------------------+
    | JOB1386714810719 | rob@fake.com | R/2013-12-10T22:33:30.719465/PT24H |
    +------------------+--------------+------------------------------------+
    | JOB1386714810737 | rob@fake.com | R/2013-12-10T22:33:30.737307/PT24H |
    +------------------+--------------+------------------------------------+

    Showing all 3 job(s)

    $ ./chronos.py jobs --delete JOB1386714810719
    Deleted job named 'JOB1386714810719'.

    $ ./chronos.py jobs --list
    +------------------+--------------+------------------------------------+
    |       Name       |    Owner     |              Schedule              |
    +==================+==============+====================================+
    | JOB1386714810695 | rob@fake.com | R/2013-12-10T22:33:30.695273/PT24H |
    +------------------+--------------+------------------------------------+
    | JOB1386714810737 | rob@fake.com | R/2013-12-10T22:33:30.737307/PT24H |
    +------------------+--------------+------------------------------------+

    Showing all 2 job(s)

    $ ./chronos.py jobs --deleteall
    Are you sure you want to delete ALL jobs? [yes/No] yes
    Deleted ALL jobs. The slate is all clean.

    $ ./chronos.py jobs --list
    +------+-------+----------+
    | Name | Owner | Schedule |
    +======+=======+==========+
    +------+-------+----------+

    No jobs

## Full Reference

### `chronos`

Forward commands to other files in the directory. New commands should be added
to the command description in this file.

```
./chronos.py -h
usage: chronos [-h] <command>

Supported chronos commands are:
  jobs      Create, destroy, and list jobs
  version   Print the chronos utils version

positional arguments:
  <command>   this is it, the command to execute

optional arguments:
  -h, --help  show this help message and exit
```

### `chronos-jobs`

Create, destroy, and list jobs

```
./chronos.py jobs -h
usage: chronos-jobs [-h] [--hostname <host:port>] [-v]
                    (--create [<n>] | --delete <jobname> | --deleteall | --list | --run <jobname> | --runall)

optional arguments:
  -h, --help            show this help message and exit
  --hostname <host:port>
                        hostname and port of the Chronos instance (default:
                        localhost:8080)
  -v                    print verbose output
  --create [<n>]        create <n> sleep jobs (default: 1)
  --delete <jobname>    delete job with name <jobname>
  --deleteall           delete all jobs (this is serious business)
  --list                list all jobs
  --run <jobname>       run job with name <jobname>
  --runall              run all jobs (could be a lot of work)
```
