import sys
import yaml
from collections import OrderedDict

from spybatch.job import Job

def organize_jobs(job_list):
    """Organize the list of jobs so that all dependencies are satisfied
    
    Return: Ordered list of jobs
    """

    # Check if jobs are satisfiable
    jobs = [j.name for j in job_list]
    dependencies = [d for j in job_list for d in j.depends_on]
    if not (all([jn in jobs for jn in dependencies])):
        raise ValueError("Not all jobs have satisfiable dependencies")

    # Perform organization by dependencies
    ordered_jobs = OrderedDict()
    while (len(ordered_jobs.keys()) != len(job_list)):
        for job in job_list:
            if (job.name in ordered_jobs.keys()):
                 continue
            if (all([d in ordered_jobs.keys() for d in job.depends_on])):
                ordered_jobs[job.name] = job
                break
    return(list(ordered_jobs.values()))

def build_jobs(job_dict):
    """Build jobs according to passed dictionary of job definitions
    
    Return: List of jobs (unordered)
    """
    pass