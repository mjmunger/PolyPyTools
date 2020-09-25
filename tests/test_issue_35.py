import unittest
import os


class TestIssue35(unittest.TestCase):

    def issue_base(self):
        return os.path.join(os.path.dirname(__file__), "fixtures/issue_31")

if __name__ == '__main__':
    unittest.main()
