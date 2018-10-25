import sys
import os
from subprocess import check_output, CalledProcessError
from tempfile import mkstemp

from spybatch.job import Job
from spybatch.job_management import organize_jobs

class Workflow:
    """Organize a workflow for SLURM job submission

    Attributes:
        jobs (list): Jobs to be submitted
        ready_to_run (bool): Is the workflow ready to run?
        job_script_paths (dict): Paths to job scripts
        job_dependencies (dict): SLURM job ids for dependency resolution
    """

    def __init__(self, jobs, ready_to_run = False):
        self.jobs = jobs
        self.ready_to_run = ready_to_run
        self._job_script_paths = dict()
        self._job_dependencies = dict()

    def organize_workflow(self):
        try:
            organized_jobs = organize_jobs(self.jobs) 
        except ValueError as e:
            raise(e)
        self.jobs = organized_jobs
        self.ready_to_run = True
        return(self)

    def build_scripts(self, script_dir = "."):
        if not self.ready_to_run:
            raise(ValueError("Workflow is not ready to run"))
        for job in self.jobs:
            temp_file = mkstemp(dir = script_dir)
            job.build_submission(temp_file[0])
            self._job_script_paths[job.name] = temp_file
            print(job.name, temp_file[1], file = sys.stderr)

    def submit(self):
        """Submit jobs to SLURM as defined in _job_script_paths, ordered by self.jobs
        """
        if (self.ready_to_run == False):
            raise(ValueError("Workflow is not ready to run"))
        for job in self.jobs:

            ### THIS SHOULD BE IN JOB.PY (Job.build_sbatch_call)
            sbatch_call = ["sbatch"]
            if not job.depends_on:
                dep_flag = "--dependency=" + ",".join(["afterok:" + self._job_dependencies[dependency] for dependency in job.depends_on])
                sbatch_call.append(dep_flag)
            sbatch_call.append(self._job_script_paths[job.name][1])
            ###
            
            try:
                slurm_id_full = check_output(sbatch_call)
                slurm_id = slurm_id_full.strip().split()[-1]
                self._job_dependencies[job.name] = slurm_id
            except CalledProcessError as e:
                return_code = e.returncode
                print("Error in submitting job", job.name, file = sys.stderr)
                print(e, file = sys.stderr)
                print(return_code, file = sys.stderr)
        return(0)

    def clean(self):
        """Clean up temporary SBATCH scripts
        """
        for job in self.jobs:
            os.close(self._job_script_paths[job.name][0])
            os.remove(self._job_script_paths[job.name][1])