import unittest
import inspect
import sys
import os

if 'WR_API_KEY' not in os.environ:
    raise Exception("Set the 'WR_API_KEY' environment variable before run the tests")

try:
    import PyWordReference
except Exception as e:
    module_path = os.path.join(
                      os.path.dirname(
                         os.path.abspath(inspect.getsourcefile(lambda:0))),
                                         "PyWordReference-submodule")
    sys.path.append(module_path)
    import PyWordReference

class PyWordReferenceTestCase(unittest.TestCase):
    def setUp(self):
        self.api_key = os.environ['WR_API_KEY']

    def tearDown(self):
        pass

    def test_01(self):
        """It verifies that the instance can be created"""
        w = PyWordReference.Translator(self.api_key)

    def test_02(self):
        """It verifies that the instance cannot be created without an API key"""
        self.assertRaises(Exception, PyWordReference.Translator)

    def test_03(self):
        """It runs the translation with a not supported language as source"""
        w = PyWordReference.Translator(self.api_key)
        self.assertRaises(Exception, w.search, "lol", "it", "ciao")

    def test_04(self):
        """It runs the translation with a not supported language as target"""
        w = PyWordReference.Translator(self.api_key)
        self.assertRaises(Exception, w.search, "it", "lol", "ciao")

    def test_05(self):
        """It runs the translation with a supported languages"""
        w = PyWordReference.Translator(self.api_key)
        res = w.search("it", "en", "ciao")
        self.assertIn("url", res)
        self.assertIn("translation", res)
        self.assertIn("compound", res)
