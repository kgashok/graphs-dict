import unittest

def run_all_tests():
  loader = unittest.TestLoader()
  start_dir = 'graphtheory'
  suite = loader.discover(start_dir)

  runner = unittest.TextTestRunner()
  runner.run(suite)