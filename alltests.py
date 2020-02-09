import unittest

def run_all_tests():
  ''' 
  thanks to https://stackoverflow.com/a/40437679/307454
  '''

  loader = unittest.TestLoader()
  start_dir = 'graphtheory'
  suite = loader.discover(start_dir)

  runner = unittest.TextTestRunner()
  runner.run(suite)