import unittest
from code.bar import bar

class Foo(unittest.TestCase):
  def test_foo(self):
    bar("hello")
    self.fail()
