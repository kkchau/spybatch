import sys

from spybatch.job import Job
from spybatch.job_management import organize_jobs

class Workflow:
    """Organize a workflow for SLURM job submission

    Attributes:
        jobs (list): Jobs to be submitted
        ready_to_run (bool): Is the workflow ready to run?
    """

    def __init__(self, jobs, ready_to_run = False):
        self.jobs = jobs
        self.ready_to_run = ready_to_run

    def submit(self):
        pass

    def organize_workflow(self):
        try:
            organized_jobs = organize_jobs(self.jobs) 
        except ValueError as e:
            raise(e)
        self.jobs = organized_jobs
        self.ready_to_run = True
        return(self)
