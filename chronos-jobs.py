#! /usr/bin/env python

import argparse
import datetime
import httplib
import json
import sys

from lib.texttable import texttable

def main(args=None):
  parser = argparse.ArgumentParser(prog="chronos-job")
  parser.add_argument("--hostname", default="localhost:8080", metavar="<host:port>",
                      help="hostname of the Chronos instance")

  # Exactly one of the following arguments must be present. These are the
  # commands supported by chronos-jobs.
  group = parser.add_mutually_exclusive_group(required=True)
  group.add_argument("--create", const=1, metavar="<n>", nargs="?", type=int,
                      help="create <n> sleep jobs (default: 1)")
  group.add_argument("--delete", metavar="<jobname>",
                      help="delete job with name <jobname>")
  group.add_argument("--deleteall", action="store_true",
                      help="delete all jobs (this is serious business)")
  group.add_argument("--list", action="store_true", help="list all jobs")

  # If called as a standalone file, `args` will be None. If called from the
  # chronos.py dispatcher, `args` will be the remainder options passed to
  # the top-level chronos.py call
  args = parser.parse_args(args)

  if args.create != None:
    payload = {
      "async": False,
      "command": "sleep 50",
      "disabled": False,
      "executor": "",
      "epsilon": "PT15M",
      "owner": "rob@fake.com"
    }
    headers = {"Content-type": "application/json"}

    connection = httplib.HTTPConnection(args.hostname)
    for i in range(args.create):
      now = datetime.datetime.utcnow()
      payload["name"] = "JOB%i" % ((now - datetime.datetime.utcfromtimestamp(0)).total_seconds() * 1000)
      payload["schedule"] = "R/%s/PT24H" % now.isoformat()

      connection.request("POST", "/scheduler/iso8601", json.dumps(payload), headers)
      connection.getresponse().read()

    connection.close()
    print "Created %i job(s) on local Chronos" % args.create
  elif args.delete != None:
    connection = httplib.HTTPConnection(args.hostname)
    connection.request("DELETE", "/scheduler/job/%s" % args.delete)
    response = connection.getresponse()
    connection.close()

    if response.status >= 200 and response.status < 300:
      print "Deleted job named '%s'." % args.delete
    else:
      print "Job named '%s' does not exist. No jobs were deleted." % args.delete
  elif args.deleteall:
    sys.stdout.write("Are you sure you want to delete ALL jobs? [yes/No] ")
    choice = raw_input()
    if choice == "yes":
      connection = httplib.HTTPConnection(args.hostname)
      connection.request("GET", "/scheduler/jobs")
      response = connection.getresponse().read()

      jobs = json.loads(response)
      for job in jobs:
        connection.request("DELETE", "/scheduler/job/%s" % job["name"])
        connection.getresponse().read()

      connection.close()
      print "Deleted ALL jobs. The slate is all clean."
    else:
      print "Deletion must be confirmed with 'yes'. No jobs were deleted."
  elif args.list != None:
    connection = httplib.HTTPConnection(args.hostname)
    connection.request("GET", "/scheduler/jobs")
    response = connection.getresponse().read()
    connection.close()

    jobs = json.loads(response)

    table = texttable.Texttable()
    rows = [["Name", "Owner", "Schedule"]]
    for job in jobs:
      rows.append([job["name"], job["owner"], job["schedule"]])

    table.add_rows(rows)
    print table.draw()

    jobs_length = len(jobs)
    if jobs_length == 0:
      print "\nNo jobs"
    else:
      print "\nShowing all %i job(s)" % len(jobs)
  else:
    print "Nothing happened. Call one of the actions. Try 'chronos job -h'."

if __name__ == "__main__":
  main()
