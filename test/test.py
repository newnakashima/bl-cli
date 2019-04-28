import unittest
from argparse import Namespace
import os
import sys
import bl
import json

class TestBacklogCli(unittest.TestCase):
    TEST_CONFIG = 'test'
    def setUp(self):
        bl.config.read('test/test_config.ini')
        BACKLOG_URL = os.environ.get('BACKLOG_URL')
        BACKLOG_API_KEY = os.environ.get('BACKLOG_API_KEY')
        bl.config[TestBacklogCli.TEST_CONFIG]['base_url'] = BACKLOG_URL
        bl.config[TestBacklogCli.TEST_CONFIG]['access_key'] = BACKLOG_API_KEY

    def test_add_schema_and_path(self):
        self.assertEqual('https://nksm.backlog.com/api/v2', bl.add_schema_and_path('nksm.backlog.com'))
        self.assertEqual('https://nksm.backlog.com/api/v2', bl.add_schema_and_path('http://nksm.backlog.com'))
        self.assertNotEqual('https://nksm.backlog.com/api/v2', bl.add_schema_and_path('hoge://nksm.backlog.com'))

    def test_command_wiki_list(self):
        args = Namespace()
        args.name = TestBacklogCli.TEST_CONFIG
        args.project = 'sandbox'
        res = bl.get_wiki_list(args)
        try:
            res_json = json.loads(res)
        except Exception:
            self.fail('JSONの読み込みに失敗しました')
        for j in res_json:
            self.assertTrue('id' in j)
            self.assertTrue('projectId' in j)
            self.assertTrue('name' in j)

    def test_command_wiki_show(self):
        args = Namespace()
        args.name = TestBacklogCli.TEST_CONFIG
        args.id = '33516'
        res = bl.get_wiki_show(args)
        try:
            res_json = json.loads(res)
        except Exception:
            self.fail('JSONの読み込みに失敗しました')
        self.assertTrue('id' in res_json)
        self.assertTrue('projectId' in res_json)
        self.assertTrue('name' in res_json)

    def test_command_projects_list(self):
        args = Namespace()
        args.name = TestBacklogCli.TEST_CONFIG
        params = [
            {
                'archived': True,
                'all': True,
            },
            {
                'archived': True,
                'all': False,
            },
            {
                'archived': False,
                'all': True,
            },
            {
                'archived': False,
                'all': False,
            }
        ]
        for p in params:
            args.archived = p['archived']
            args.all = p['all']
            res = bl.get_projects_list(args)
            try:
                res_json = json.loads(res)
            except Exception:
                self.fail('JSONの読み込みに失敗しました')
            if not args.archived:
                for r in res_json:
                    self.assertTrue('id' in r)
                    self.assertTrue('projectKey' in r)
                    self.assertTrue('name' in r)
            else:
                self.assertEqual(0, len(res_json))

    def test_command_projects_show(self):
        args = Namespace()
        args.name = TestBacklogCli.TEST_CONFIG
        args.project = 'sandbox'
        res = bl.get_projects_show(args)
        try:
            res_json = json.loads(res)
        except Exception:
            self.fail('JSONの読み込みに失敗しました')
        self.assertTrue('id' in res_json)
        self.assertTrue('projectKey' in res_json)
        self.assertTrue('name' in res_json)

    def test_command_projects_update(self):
        args = Namespace()
        args.name = TestBacklogCli.TEST_CONFIG
        args.project = 'sandbox'
        res = bl.get_projects_update(args)
        try:
            res_json = json.loads(res)
        except Exception:
            self.fail('JSONの読み込みに失敗しました')
        self.assertTrue('id' in res_json)
        self.assertTrue('projectKey' in res_json)
        self.assertTrue('name' in res_json)

if __name__ == '__main__':
    unittest.main()
