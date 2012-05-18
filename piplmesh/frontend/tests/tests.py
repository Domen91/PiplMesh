import os
os.environ['DJANGO_SETTINGS_MODULE'] = "piplmesh.settings"

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.utils import unittest

class Testing(TestCase):
	def setUp(self):
        self.client = Client()
                        
    def test__login(self):
		c = Client()
		c.login(username='test', password='testtest')
		self.assertEqual(response.status_code, 200)
	
	def test_logout(self):
		c = Client()
		c.logout()
		
	def user_loged_on(self):
		response = self.client.get('/user/test/')
		self.assertEqual(response.status_code, 200)
		
 
  
