import unittest
import sys
from io import StringIO

from spybatch.job import Job
from spybatch.workflow import Workflow

class WorkflowTest(unittest.TestCase):
    """Test cases for Workflow class"""

    def setUp(self):
        self.workflow = Workflow(
            [
                Job(
                    "Job1", 
                    set(), 
                    {"--param1": "p1", "--param2": "p2"},
                    "Command 1"
                ),
                Job(
                    "Job2", 
                    set(["Job1"]), 
                    {"--param1": "p1", "--param2": "p2"},
                    "Command 1"
                ),
                Job(
                    "Job3", 
                    set(["Job1"]), 
                    {"--param1": "p1", "--param2": "p2"},
                    "Command 1"
                ),
                Job(
                    "Job4", 
                    set(["Job1", "Job3"]), 
                    {"--param1": "p1", "--param2": "p2"},
                    "Command 1"
                )
            ]
        )
        self.workflow_unsatisfiable = Workflow(
            [
                Job(
                    "Job1", 
                    set(), 
                    {"--param1": "p1", "--param2": "p2"},
                    "Command 1"
                ),
                Job(
                    "Job2", 
                    set(["Job1"]), 
                    {"--param1": "p1", "--param2": "p2"},
                    "Command 1"
                ),
                Job(
                    "Job3", 
                    set(["Job1"]), 
                    {"--param1": "p1", "--param2": "p2"},
                    "Command 1"
                ),
                Job(
                    "Job4", 
                    set(["Job1", "Job5"]), 
                    {"--param1": "p1", "--param2": "p2"},
                    "Command 1"
                )
            ]
        )

    def test_job_satisfiability(self):
        self.assertRaises(
            ValueError, 
            self.workflow_unsatisfiable.organize_workflow
        )

    def test_ordered_jobs(self):
        self.workflow.organize_workflow()
        self.assertEqual(
            ["Job1", "Job2", "Job3", "Job4"], 
            [job.name for job in self.workflow.jobs]
        )