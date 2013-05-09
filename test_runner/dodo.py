from doit.tools import check_timestamp_unchanged
from test_runner.ph_test_reporter import nose, notify_run
import glob
import itertools
import os

TESTS = (("~/lnkd/lib/mint", 'linkedin/mint'),
         ("~/lnkd/apps/push-my-upgrade-server", 'pushmyupgradeserver'))

PATTERNS = ("*.py", "*.html")

EXCLUDE = ("_flymake",)


def include(s):
  return not any(e in s for e in EXCLUDE)


def concat(seqs):
  return tuple(itertools.chain.from_iterable(seqs))


def make_test_tsk(root, module_name):
  root = os.path.expanduser(root)

  file_deps = concat(filter(include, glob.glob(d + subdir + pattern))
                     for d in (root + '/test',
                               root + '/src/%s' % module_name)
                     for pattern in PATTERNS
                     for subdir in ['/', '/*/'])

  deps_dict = {
    'file_dep': file_deps,
    'uptodate': map(check_timestamp_unchanged, file_deps),
  }

  # Make a task for each test_file.
  for test_file in glob.glob(root + '/test/*test*.py'):
    base_file_name = os.path.basename(test_file)[:-len(".py")]

    def tsk(test_file=test_file, base_file_name=base_file_name):
      return dict(deps_dict,
        actions=[lambda: notify_run(nose(root + '/test',
                                         test_file),
                                    func=base_file_name)])

    tsk.__name__ = "task_%s__%s" % (module_name, base_file_name)
    yield tsk

  # Make a task to run all of the module_name's tests.
  def tsk():
    return dict(deps_dict,
                actions=[lambda: notify_run(nose(root + '/test'),
                                            func=module_name)])

  tsk.__name__ = "task_%s" % module
  yield tsk


for root, module in TESTS:
  for fn in make_test_tsk(root, module):
    globals()[fn.__name__] = fn
