#from tests import *
from __future__ import absolute_import

from django.utils import unittest

from . import tests

def suite():
    return unittest.TestSuite((
        unittest.TestLoader().loadTestsFromTestCase(tests.BasicTest),
        #unittest.TestLoader().loadTestsFromTestCase(tests.UserTest),
    ))
