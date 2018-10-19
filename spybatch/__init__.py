import yaml

from spybatch.job import Job
from spybatch.workflow import Workflow

def read_rules(rules_file):
    """Read rules from the provided definitions file (handle)"""
    pass

def read_params(params_file, job_names):
    """Read cluster parameters from the provided parameters file (handle)
    
    Return: Processed dictionary of parameters
    """
    full_dict = yaml.safe_load(params_file)

    # Pre-initialize job parameters with defaults
    default_params = full_dict["__default__"]
    job_params = {j: default_params for j in job_names}

    # Overwrite default paramters with specifics per job
    for job in [_ for _ in full_dict if _ != "__default__"]:
        for parameter in full_dict[job]:
            job_params[job][parameter] = full_dict[job][parameter]

    return(job_params)

def argument_parser():
    pass

def main():
    pass