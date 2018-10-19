import unittest
import sys

from spybatch import read_params

class readTest(unittest.TestCase):

    def setUp(self):
        self.job_names = ["Job1", "Job2"]
        pass

    def test_read_params(self):
        with open("test/test_params.yaml", "r") as test_params:
            job_params = read_params(test_params, self.job_names)
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
