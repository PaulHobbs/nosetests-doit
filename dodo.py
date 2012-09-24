from doit.tools import check_timestamp_unchanged
from ph_test_reporter import nose, notify_run
import os

MINT_LIB = os.path.expanduser("~/lnkd/lib/mint/src/linkedin/mint")
MINT_INTEG = os.path.expanduser("~/lnkd/apps/mint/integTest")


def task_mint_unit_tests():
  """ Runs the unit tests for mint. """

  return {
    'actions': [notify_run(nose(MINT_LIB))],
    'uptodate': [check_timestamp_unchanged(MINT_LIB)],
    }


def task_mint_integration():
  """
  Runs the {fname} integration tests.
  """
  INTEG_ASSOCS = {
    'test_mint.py': MINT_LIB,
    'test_mint_build.py': MINT_LIB,
    'test_integration.py': MINT_LIB,
    'test_checkout_and_update.py': MINT_LIB + '/main.py'
    }

  for fname, dep in INTEG_ASSOCS.iteritems():
    try:
      if isinstance(dep, str):
        deps = [dep]
      else:
        deps = list(dep)
    except TypeError:
      deps = [dep]
    yield {
      'name': fname,
      'actions': [notify_run(nose(MINT_INTEG, fname))],
      'uptodate': map(check_timestamp_unchanged, deps),
      }
