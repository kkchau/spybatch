import unittest
import sys
from io import StringIO

from spybatch.job import Job

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

if __name__ == "__main__":
    unittest.main()
