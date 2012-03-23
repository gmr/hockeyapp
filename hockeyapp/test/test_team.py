
from hockeyapptest import HockeyAppTestCase

from .hockeyapp import team
from .. import api

class TestTeamAPI(HockeyAppTestCase):

	def test_list_failures(self):
		
		config = self.test_config

		user_list = team.AppUsers(config.api_key_read_only, None)
		self.assertIsNotNone(user_list)
		self.assertRaises(api.APIError, user_list.execute)

		try:
			user_list.execute()
		except api.APIError as e:
			self.assertRegexpMatches(str(e.value), "read only")

		user_list = team.AppUsers(config.api_key_read_write, None)
		self.assertIsNotNone(user_list)
		self.assertRaises(api.APIError, user_list.execute)

		try:
			user_list.execute()
		except api.APIError as e:
			self.assertRegexpMatches(str(e.value), "not found")

	def test_list(self):

		config = self.test_config

		user_list = team.AppUsers(config.api_key_read_write, config.app_id);
		users = user_list.execute();

		self.assertIsInstance(users, list)
