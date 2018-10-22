import unittest
import sys
from io import StringIO

from spybatch.job import Job
from spybatch.job_definitions import read_rules, read_params
from spybatch import create_jobs

class JobTest(unittest.TestCase):
    """Tests for the Job class (job.py)"""

    def setUp(self):
        self.job = Job(
            "test", 
            set(["dep1", "dep3"]), 
            {"--param1": "p1", "--param2": "p2"},
            ["PREPEND", "COMMAND"]
        )

    def test_check_dependencies(self):
        self.assertTrue(
            self.job.check_dependencies(set(["dep1", "dep2", "dep3"]))
        )
        self.assertTrue(self.job.is_ready)

    def test_build_submission(self):
        output = StringIO()
        self.job.build_submission(output)
        output.seek(0)
        test_content = [_.strip('\n') for _ in output.readlines()]
        self.assertEqual(
            test_content, 
            [
                "#!/usr/bin/env bash", 
                "#SBATCH --param1 p1", 
                "#SBATCH --param2 p2", 
                "PREPEND",
                "COMMAND"
            ]
        )

    def test_job_creation(self):
        with open("test/test_rules.yaml", 'r') as r_handle:
            rules = read_rules(r_handle)
        with open("test/test_params.yaml", 'r') as p_handle:
            params = read_params(p_handle, rules)
        jobs = create_jobs(rules, params)
        jobs_test = [
            Job(
                "Job1",
                [""],
                {
                    "--time": "00:05:00",
                    "--partition": "compute",
                    "--mem": "20G",
                    "--mail-type": "ALL",
                    "--mail-user": "test@test.edu",
                    "--workdir": "some/path"
                },
                ["Prepend this command", "Rscript some/path/Job1.R"]
            ),
            Job(
                "Job2",
                ["Job1"],
                {
                    "--time": "00:05:00",
                    "--partition": "shared",
                    "--mem": "10G",
                    "--mail-type": "ALL",
                    "--mail-user": "test@test.edu",
                    "--workdir": "."
                },
                ["Prepend this command", "Rscript Job2.R"]
            )
        ]
        self.assertEqual(
            jobs, 
            jobs_test
        )

if __name__ == "__main__":
    unittest.main()
