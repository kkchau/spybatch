import unittest
import sys

from spybatch.job_definitions import read_params, check_rules, read_rules

class readTest(unittest.TestCase):

    def setUp(self):
        self.job_names = ["Job1", "Job2"]
        self.params_file = "test/test_params.yaml"
        self.rules_file = "test/test_rules.yaml"
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
        with open(self.params_file, 'r') as params_handle:
            with open(self.rules_file, 'r') as rules_handle:
                job_params = read_params(params_handle, read_rules(rules_handle))
                self.assertTrue(
                    job_params,
                    {
                        "Job1": {
                            "--time": "00:05:00",
                            "--partition": "compute",
                            "--mem": "20G",
                            "--mail-type": "ALL",
                            "--mail-user": "test@test.edu",
                            "--workdir": "some/path"
                        },
                        "Job2": {
                            "--time": "00:05:00",
                            "--partition": "shared",
                            "--mem": "10G",
                            "--mail-type": "ALL",
                            "--mail-user": "test@test.edu",
                            "--workdir": "."
                        }
                    }
                )
    
    def test_check_rules(self):
        self.assertRaises(ValueError, check_rules, self.rules_fail)

    def test_read_rules(self):
        with open(self.rules_file, 'r') as rules_handle:
            self.assertEqual(
                read_rules(rules_handle),
                {
                    "prepend": "Prepend this command",
                    "Job1": {
                        "depends_on": "",
                        "command": "Rscript some/path/Job1.R"
                    },
                    "Job2": {
                        "depends_on": ["Job1"],
                        "command": "python3 Job2.py"
                    }
                }
            )
