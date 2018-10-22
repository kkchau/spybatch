import yaml

from spybatch.job import Job
from spybatch.workflow import Workflow
from spybatch.job_definitions import read_rules, read_params, check_working_dir

def create_jobs(rules, params):
    """Create rules given definitions provided by rules and params dictionaries
    
    Return: List of Job instances
    """
    jobs = [
        Job(
            name = job, 
            depends_on = rules[job]["depends_on"],
            params = params[job],
            command = [rules["prepend"], rules[job]["command"]]
        ) for job in [
            _ for _ in rules.keys() if _ != "prepend"
        ]
    ]
    return(jobs)

def argument_parser():
    pass

def main():
    try:
        rules = read_rules      #TODO:  Parse args
    except ValueError as e:
        raise(e)

    params = read_params        # TODO: Parse args
    workflow = Workflow(create_jobs(rules, params))

    try:
        workflow.organize_workflow()
    except ValueError as e:
        raise(e)

    try:
        workflow.submit()
    except ValueError as e:
        exit(str(e))