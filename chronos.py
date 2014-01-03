#! /usr/bin/env python

import argparse

def main():
  parser = argparse.ArgumentParser(
    description='''
Supported chronos commands are:
  jobs      Create, destroy, and list jobs
  version   Print the chronos utils version
''',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    prog="chronos")
  parser.add_argument("<command>", help="this is it, the command to execute")
  parser.add_argument("args", help=argparse.SUPPRESS, nargs=argparse.REMAINDER)
  args = parser.parse_args()

  command_name = getattr(args, "<command>")

  try:
    command_namespace = __import__("chronos-%s" % command_name)
  except ImportError:
    print "'%s' is not a chronos command. Try 'chronos -h'." % command_name
    exit(1)

  command = getattr(command_namespace, "main")
  command(getattr(args, "args"))

if __name__ == "__main__":
  main()
