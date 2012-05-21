from django.test.client import Client
from django.contrib.auth.models import User
from django.utils import unittest
from django.db import models
from piplmesh import test_runner

class BasicTest(unittest.TestCase):
	def setUp(self):
		self.client = Client()
		
	#Can NOT create user											
	def test_create_user(self):
		test_user = User.objects.create(
					username		= 	'test',
					first_name		= 	'test_firstname',
					last_name		= 	'test_lastname',
					email			= 	'test@test.si',
					gender			= 	'male',
					)
		test_user.set_password('testtest')
		test_user.save()
		
	def test__login(self):
		self.client.login(username='test', password='testtest')
		print 'Logged on.'

			                               
	def test_user_loged_on(self):
		response = self.client.get('/user/test/')
		self.assertEqual(response.status_code, 200)
		print response.status_code

	def test_logout(self):
		self.client.logout()
		print '\nLogged out.'
		
	def test_registration(self):
		response = self.client.get('/register/')
		self.assertEqual(response.status_code, 200)
		print response.status_code