from __future__ import annotations

import unittest


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromName("tests.test_sports")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    raise SystemExit(0 if result.wasSuccessful() else 1)