import unittest

from spybatch import create_jobs
from spybatch.job import Job
from spybatch.workflow import Workflow
from spybatch.job_definitions import read_rules, read_params

class submissionTest(unittest.TestCase):

    def setUp(self):
        with open("test/test_rules.yaml") as rules_handle:
            rules = read_rules(rules_handle)
        with open("test/test_params.yaml") as params_handle:
            params = read_params(params_handle, rules = rules)
        self.workflow = Workflow(create_jobs(rules, params)).organize_workflow()

    def test_submit_script(self):
        print("The following files should not exist anymore:")
        print(self.workflow.build_scripts())
        self.workflow.clean()