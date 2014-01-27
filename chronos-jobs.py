#! /usr/bin/env python

import argparse
import datetime
import httplib
import json
import random
import sys

from lib.texttable import texttable

def main(args=None):
  parser = argparse.ArgumentParser(prog="chronos-jobs")
  parser.add_argument("--hostname", default="localhost:8080", metavar="<host:port>",
                      help="hostname and port of the Chronos instance (default: localhost:8080)")
  parser.add_argument("-v", action="store_true", default=False,
                      help="print verbose output")

  # Exactly one of the following arguments must be present. These are the
  # commands supported by chronos-jobs.
  group = parser.add_mutually_exclusive_group(required=True)
  group.add_argument("--create", const=1, metavar="<n>", nargs="?", type=int,
                      help="create <n> sleep jobs (default: 1)")
  group.add_argument("--createforest", const=1, metavar="<n>", nargs="?", type=int,
                      help="create <n> sleep jobs, with random dependencies (default: 1)")
  group.add_argument("--delete", metavar="<jobname>",
                      help="delete job with name <jobname>")
  group.add_argument("--deleteall", action="store_true",
                      help="delete all jobs (this is serious business)")
  group.add_argument("--list", action="store_true", help="list all jobs")
  group.add_argument("--run", metavar="<jobname>",
                      help="run job with name <jobname>")
  group.add_argument("--runall", action="store_true",
                      help="run all jobs (could be a lot of work)")

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

  elif args.createforest != None:
    p1 = 0.6
    p2 = 0.2
    available_parents = 0
    static_payload = {
      "async": False,
      "command": "sleep 50",
      "disabled": False,
      "executor": "",
      "epsilon": "PT15M",
      "owner": "rob@fake.com"
    }
    headers = {"Content-type": "application/json"}
    connection = httplib.HTTPConnection(args.hostname)
    payloads = []
    for i in range(args.createforest):
      now = datetime.datetime.utcnow()
      payload = dict(static_payload) # Create a copy
      payload["name"] = "DEPENDENTJOB%i" % ((now - datetime.datetime.utcfromtimestamp(0)).total_seconds() * 1000)
      if random.random() < p2 and available_parents > 2:
        # With probability p2, this node will have two parents selected at random from the list of completed payloads.
        payload["parents"] = [obj['name'] for obj in random.sample(payloads, 2)]
        available_parents += 1
        url = "/scheduler/dependency"
      elif random.random() < p1 and available_parents > 1:
        # With probability p1, this node will have a single parent selected at random from the list of completed payloads.
        payload["parents"] = [obj['name'] for obj in random.sample(payloads, 1)]
        available_parents += 1
        url = "/scheduler/dependency"
      else:
        # This job is a root job with no parents, so it must be scheduled.
        available_parents += 1
        payload["schedule"] = "R/%s/PT24H" % now.isoformat()
        url = "/scheduler/iso8601"

      payloads.append(payload)
      connection.request("POST", url, json.dumps(payload), headers)
      connection.getresponse().read()
    connection.close()
    print "Created %i dependent job(s) on local Chronos" % args.createforest

  elif args.delete != None:
    connection = httplib.HTTPConnection(args.hostname)
    connection.request("DELETE", "/scheduler/job/%s" % args.delete)
    response = connection.getresponse()
    connection.close()

    if 200 <= response.status < 300:
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
  elif args.list:
    connection = httplib.HTTPConnection(args.hostname)
    connection.request("GET", "/scheduler/jobs")
    response = connection.getresponse().read()
    connection.close()

    jobs = json.loads(response)

    table = texttable.Texttable(max_width=False)
    if args.v:
      headers = ["Name", "Owner", "Schedule", "Epsilon", "Retries", "Command"]
    else:
      headers = ["Name", "Owner", "Schedule"]

    rows = [headers]
    for job in jobs:
      if args.v:
        values = [job["name"], job["owner"], job["schedule"], job["epsilon"],
          job["retries"], job["command"]]
      else:
        values = [job["name"], job["owner"], job["schedule"]]

      rows.append(values)

    table.add_rows(rows)
    print table.draw()

    jobs_length = len(jobs)
    if jobs_length == 0:
      print "\nNo jobs"
    else:
      print "\nShowing all %i job(s)" % len(jobs)
  elif args.run != None:
    connection = httplib.HTTPConnection(args.hostname)
    connection.request("PUT", "/scheduler/job/%s" % args.run)
    response = connection.getresponse()
    connection.close()

    if 200 <= response.status < 300:
      print "Force ran job '%s'." % args.run
    else:
      print "Job named '%s' does not exist. No jobs were run." % args.run
  elif args.runall:
    sys.stdout.write("Are you sure you want to run ALL jobs? [yes/No] ")
    choice = raw_input()
    if choice == "yes":
      connection = httplib.HTTPConnection(args.hostname)
      connection.request("GET", "/scheduler/jobs")
      response = connection.getresponse().read()

      jobs = json.loads(response)
      for job in jobs:
        connection.request("PUT", "/scheduler/job/%s" % job["name"])
        connection.getresponse().read()

      connection.close()
      print "Ran ALL jobs. Watch out, that's a lot of work."
    else:
      print "Running all jobs must be confirmed with 'yes'. No jobs were run."

if __name__ == "__main__":
  main()
