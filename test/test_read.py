import unittest
import sys

from spybatch.job_definitions import read_params, check_rules, read_rules

class readTest(unittest.TestCase):

    def setUp(self):
        self.job_names = ["Job1", "Job2"]
        self.params_handle = open("test/test_params.yaml")
        self.rules_handle = open("test/test_rules.yaml")
        self.rules_fail = {
            "prepend": "", 
            "Job1": {
                "depends_on": "",
                "command": "command"
            }, 
            "Job2": {
                "dep_on": "",
                "command": "c"
            }
        }
        pass

    def test_read_params(self):
        job_params = read_params(self.params_handle, self.job_names)
        self.assertTrue(
            job_params,
            {
                "Job1": {
                    "--time": "00:05:00",
                    "--partition": "compute",
                    "--mem": "20G",
                    "--mail-type": "ALL",
                    "--mail-user": "test@test.edu"
                },
                "Job2": {
                    "--time": "00:05:00",
                    "--partition": "shared",
                    "--mem": "10G",
                    "--mail-type": "ALL",
                    "--mail-user": "test@test.edu"
                }
            }

        )
    
    def test_check_rules(self):
        self.assertRaises(ValueError, check_rules, self.rules_fail)

    def test_read_rules(self):
        self.assertEqual(
            read_rules(self.rules_handle),
            {
                "prepend": "Prepend this command",
                "Job1": {
                    "depends_on": "",
                    "command": "Rscript Job1.R"
                },
                "Job2": {
                    "depends_on": "Job1",
                    "command": "python3 Job2.R"
                }
            }
        )
