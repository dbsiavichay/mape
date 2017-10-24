# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

class ContextTest(unittest.TestCase):
    def test_against_dictionary(self):
        c1 = Context()
        c1['update'] = 'value'
        self.assertEqual(c1.flatten(), {
            'True': True,
            'None': None,
            'False': False,
            'update': 'value',
        })
# Create your tests here.
