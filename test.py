import unittest
import bl

class TestBacklogCli(unittest.TestCase):
    def test_add_schema(self):
        self.assertEqual('https://nksm.backlog.com', bl.add_schema('nksm.backlog.com'))
        self.assertEqual('https://nksm.backlog.com', bl.add_schema('http://nksm.backlog.com'))
        self.assertNotEqual('https://nksm.backlog.com', bl.add_schema('hoge://nksm.backlog.com'))

if __name__ == '__main__':
    unittest.main()
