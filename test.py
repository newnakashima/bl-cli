import unittest
from argparse import Namespace
import bl
import os
import json

class TestBacklogCli(unittest.TestCase):
    TEST_CONFIG = 'test'
    def setUp(self):
        bl.config.read('test_config.ini')

    def test_add_schema(self):
        self.assertEqual('https://nksm.backlog.com', bl.add_schema('nksm.backlog.com'))
        self.assertEqual('https://nksm.backlog.com', bl.add_schema('http://nksm.backlog.com'))
        self.assertNotEqual('https://nksm.backlog.com', bl.add_schema('hoge://nksm.backlog.com'))

    def test_command_wiki_list(self):
        args = Namespace()
        args.name = TestBacklogCli.TEST_CONFIG
        args.project = 'sandbox'
        BACKLOG_URL = os.environ.get('BACKLOG_URL')
        BACKLOG_API_KEY = os.environ.get('BACKLOG_API_KEY')
        bl.config[TestBacklogCli.TEST_CONFIG]['base_url'] = BACKLOG_URL
        bl.config[TestBacklogCli.TEST_CONFIG]['access_key'] = BACKLOG_API_KEY
        res = bl.get_wiki_list(args)
        try:
            res_json = json.loads(res)
        except Exception:
            self.fail('JSONの読み込みに失敗しました')
        for j in res_json:
            self.assertTrue('id' in j)
            self.assertTrue('projectId' in j)
            self.assertTrue('name' in j)

if __name__ == '__main__':
    unittest.main()
