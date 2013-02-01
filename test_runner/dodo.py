from doit.tools import check_timestamp_unchanged
from test_runner.ph_test_reporter import nose, notify_run
import os

MINT_LIB_TESTS = os.path.expanduser("~/lnkd/lib/mint/test")
MINT_LIB_SRC = os.path.expanduser("~/lnkd/lib/mint/src/linkedin/mint")
MINT_INTEG = os.path.expanduser("~/lnkd/apps/mint/integTest")


def task_mint_unit_tests():
  """ Runs the unit tests for mint. """

  return {
    'actions': [notify_run(nose(MINT_LIB_TESTS))],
    'uptodate': [check_timestamp_unchanged(MINT_LIB_SRC),
                 check_timestamp_unchanged(MINT_LIB_TESTS)],
    }
