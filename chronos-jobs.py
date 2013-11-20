#! /usr/bin/env python

import argparse
import datetime
import httplib
import json

from lib.texttable import texttable

def main(args=None):
  parser = argparse.ArgumentParser(prog="chronos-job")
  parser.add_argument("--create", metavar="<n>", type=int,
                      help="create <n> sleep jobs (default: 1)")
  parser.add_argument("--delete", metavar="<jobname>",
                      help="delete job with name <jobname>")
  parser.add_argument("--list", action="store_true", help="list all jobs")

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

    for i in range(args.create):
      now = datetime.datetime.utcnow()
      payload["name"] = "JOB%i" % ((now - datetime.datetime.utcfromtimestamp(0)).total_seconds() * 1000)
      payload["schedule"] = "R/%s/PT24H" % now.isoformat()

      connection = httplib.HTTPConnection("localhost:8080")
      connection.request("POST", "/scheduler/iso8601", json.dumps(payload), headers)
      connection.close()

    print "Created %i job(s) on local Chronos" % args.create
  elif args.delete != None:
    connection = httplib.HTTPConnection("localhost:8080")
    connection.request("DELETE", "/scheduler/job/%s" % args.delete)
    response = connection.getresponse()
    connection.close()

    if response.status >= 200 and response.status < 300:
      print "Deleted job named '%s'." % args.delete
    else:
      print "Job named '%s' does not exist. No jobs were deleted." % args.delete
  elif args.list != None:
    connection = httplib.HTTPConnection("localhost:8080")
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
    print "\nShowing all %i jobs" % len(rows)
  else:
    print "Nothing happened. Call one of the actions. Try 'chronos job -h'."

if __name__ == "__main__":
  main()
