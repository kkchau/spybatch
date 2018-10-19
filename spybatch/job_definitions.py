import sys
import yaml

def read_rules(rules_file):
    """Read rules defining each job from the provided fules file (handle)

    Return: Dictionary of job definitions
    """
    rules = yaml.safe_load(rules_file)
    try:
        check_rules(rules)
    except ValueError as e:
        raise(e)
    return rules

def check_rules(rules):
    """Check that each job definitionn has at least the correct attributes, i.e. dependencies and command
    
    Return: Success or failure (bool)
    """
    for job in [_ for _ in rules.keys() if _ != "prepend"]:
        if any(["depends_on", "command"] not in rules[job]):
            raise ValueError("Error in rule definition for job ", job)
    return(True)

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