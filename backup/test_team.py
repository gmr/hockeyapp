
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

    def test_add_delete(self):
        config = self.test_config

        user_list = team.AppUsers(config.api_key_read_write, config.app_id)
        users = user_list.execute()

        for user in users:
            if user['email'] == config.user['email']:
                delete_user = team.AppDeleteUser(config.api_key_read_write, config.app_id, user['id'])
                delete_user.execute()
                break

        add_user = team.AppAddUser(config.api_key_read_write, config.app_id, config.user['email'])
        add_user.role = config.user['role']
        add_user.first_name = config.user['first']
        add_user.last_name = config.user['last']

        new_user = add_user.execute()
        
        self.assertIsNotNone(new_user)
        self.assertEqual(new_user['role'], config.user['role'])
        self.assertEqual(new_user['full_name'], ' '.join([config.user['first'], config.user['last']]))
        self.assertEqual(new_user['email'], config.user['email'])

        users = user_list.execute()
        user_id = None

        for user in users:
            if user['email'] == config.user['email']:
                user_id = user['id']
                break

        self.assertIsNotNone(user_id)

        delete_user = team.AppDeleteUser(config.api_key_read_write, config.app_id, user_id)
        delete_user.execute()

        users = user_list.execute()
        user_id = None

        for user in users:
            if user['email'] == config.user['email']:
                user_id = user['id']
                break

        self.assertIsNone(user_id)







