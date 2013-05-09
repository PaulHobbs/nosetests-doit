from linkedin.command import external
import sys
import re

DEBUG = True

IGNORE_REGEX = re.compile(r'(.*[wW]arning.*)|(.*import.*)')

def nose(directory, *args):
  args = args or ["-x"]
  print directory, args
  return 'nosetests -w {0} {1}'.format(directory, *args)


def notify(success, message, duration=10000, func=None):
  """
  Notify whether tests succeeded, and give the test output.
  """

  summary = "%s tests" % func if func else "Tests"
  summary += " passed." if success else " failed!"
  icon = '/usr/share/pixmaps/apple-%s.png' % ('green' if success else 'red')

  print >>sys.stderr, 'message:', message

  # filter out warnings and other noisy lines.
  lines = message.splitlines()
  keep = lambda line: not re.match(IGNORE_REGEX, line)
  message = "\n".join(filter(keep, lines))

  # Failures are usually too big:
  if not success:
    keywords = ['fail', 'error', '----']
    lines = [line for line in lines
             if any(k in line.lower() for k in keywords)]


  return "notify-send -i '{icon}' -t 10000 '{summary}' '{message}'".format(
    icon=icon,
    summary=summary,
    message=message)


def notify_run(cmd, *args, **kwargs):
  """
  Run a command and notify with result.
  """

  _, err_output, err = external(cmd)
  notify_cmd = notify(err == 0, err_output, *args, **kwargs)
  if DEBUG:
    print notify_cmd
  _, _, err = external(notify_cmd)
  if DEBUG:
    print "Notify command returned: ", err
