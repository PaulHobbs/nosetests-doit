from linkedin.command import external
import sys

def nose(directory, *args):
  args = args or [""]
  print directory, args
  return 'nosetests -w {0} {1}'.format(directory, *args)

def notify(success, message):
  """
  Notify whether tests succeeded, and give the test output.
  """

  summary = "Tests pass!" if success else "Tests failed."
  icon = '/usr/share/pixmaps/apple-%s.png' % ('green' if success else 'red')

  print >>sys.stderr, 'message:', message

  message = message[:400]  # avoid "Argument list too long."

  return "notify-send -i '{icon}' -t 20000 '{summary}' '{message}'".format(
    icon=icon,
    summary=summary,
    message=message)

def notify_run(cmd):
  """
  Run a command and notify with result.
  """

  def go_():
    _, err_output, err = external(cmd)
    notify_cmd = notify(err == 0, err_output)
    if DEBUG:
      print notify_cmd
    external(notify_cmd)

  return go_
