import yaml

from spybatch.job import Job
from spybatch.workflow import Workflow
from spybatch.job_definitions import read_rules, read_params

def create_jobs(rules, params):
    """Create rules given definitions provided by rules and params dictionaries
    
    Return: List of Job instances
    """
    prepend_command = rules["prepend"]
    jobs = []
    for job in [_ for _ in rules.keys() if _ != "prepend"]:
        new_job = Job(
            name = job,
            depends_on = rules[job]["depends_on"],
            params = params[job],
            command = [prepend_command, rules[job]["command"]]
        )
        jobs.append(new_job)
    return(jobs)

def argument_parser():
    pass

def main():
    try:
        rules = read_rules
    except ValueError as e:
        raise(e)
    params = read_params
    jobs_all = create_jobs(rules, params)
    workflow = Workflow(jobs_all)
    try:
        workflow.organize_workflow()
    except ValueError as e:
        raise(e)
    pass