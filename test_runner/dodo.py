from doit.tools import check_timestamp_unchanged
from test_runner.ph_test_reporter import nose, notify_run
import glob
import itertools
import os

TESTS = (("~/lnkd/lib/mint", 'linkedin/mint'),
         ("~/lnkd/apps/push-my-upgrade-server", 'pushmyupgradeserver'))

PATTERNS = ("*.py", "*.html")


def concat(seqs):
  return tuple(itertools.chain.from_iterable(seqs))


def make_test_tsk(root, module_name):
  root = os.path.expanduser(root)

  file_deps = concat(glob.glob(d + subdir + pattern)
                     for d in (root + '/test',
                               root + '/src/%s' % module)
                     for pattern in PATTERNS
                     for subdir in ['/', '/*/'])

  def task():
    return {
      'actions': [lambda: notify_run(nose(root + '/test'))],
      'file_dep': file_deps,
      'uptodate': map(check_timestamp_unchanged, file_deps),
    }

  task.__name__ = "task_run_tests_for_%s" % module
  return task


for root, module in TESTS:
  fn = make_test_tsk(root, module)
  globals()[fn.__name__] = fn
