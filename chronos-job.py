#! /usr/bin/env python

import argparse
import datetime
import httplib
import json

def main(args):
  parser = argparse.ArgumentParser(prog="chronos-job")
  parser.add_argument("-n", default=1, type=int,
                      help="number of Chronos jobs to create (default: 1)")
  args = parser.parse_args()

  payload = {
    "async": False,
    "command": "sleep 50",
    "disabled": False,
    "executor": "",
    "epsilon": "PT15M",
    "owner": "rob@fake.com"
  }
  headers = {"Content-type": "application/json"}

  for i in range(args.n):
    now = datetime.datetime.utcnow()
    payload["name"] = "JOB%i" % ((now - datetime.datetime.utcfromtimestamp(0)).total_seconds() * 1000)
    payload["schedule"] = "R/%s/PT24H" % now.isoformat()

    connection = httplib.HTTPConnection("localhost:8080")
    connection.request("POST", "/scheduler/iso8601", json.dumps(payload), headers)
    connection.close()

  print "Created %i job(s) on local Chronos" % args.n

if __name__ == "__main__":
  main()
