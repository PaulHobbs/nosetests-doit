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


  return "notify-send -i '{icon}' -t 10000 '{summary}' '{message}'".format(
    icon=icon,
    summary=summary,
    message=message)[:100]  # avoid "Argument list too long."

def notify_run(cmd):
  """
  Run a command and notify with result.
  """

  def go_():
    _, err_output, err = external(cmd)
    external(notify(err == 0, err_output))

  return go_
