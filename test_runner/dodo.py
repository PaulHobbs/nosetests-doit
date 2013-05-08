from doit.tools import check_timestamp_unchanged
from test_runner.ph_test_reporter import nose, notify_run
import os
from functools import partial

TESTS = (("~/lnkd/lib/mint", 'linkedin/mint'),
         ("~/lnkd/apps/push-my-upgrade-server", 'pushmyupgradeserver'))


def make_test_tsk(root, module_name):
  root = os.path.expanduser(root)

  def task():
    return {
    'actions': [lambda: notify_run(nose(root + '/test'))],
    'uptodate': [check_timestamp_unchanged(root + '/test'),
                 check_timestamp_unchanged(root + '/src/%s' % module)],
    }

  task.__name__ = "task_run_tests_for_%s" % module
  return task

for root, module in TESTS:

  fn = make_test_tsk(root, module)
  globals()[fn.__name__] = fn
