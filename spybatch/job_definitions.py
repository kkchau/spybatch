import sys
import yaml
import re

SCRIPT_EXT = [".py", ".R", ".sh"]
SCRIPT_CAPTURES = [re.compile("^|\W(.+" + _ + ")") for _ in SCRIPT_EXT]

def read_rules(rules_file):
    """Read rules defining each job from the provided fules file (handle)

    Return: Dictionary of job definitions
    """
    rules = yaml.safe_load(rules_file)
    try:
        check_rules(rules)
        for r in rules:
            rules[r]["--workdir"] = check_working_dir(r)
        return(rules)
    except ValueError as e:
        raise(e)

def check_working_dir(rule):
        """Check if a working directory is defined for the rule, else use directory of the script
        """
        if ("--workdir" in rule.keys()):
            return(rule["--workdir"])
        else:
            # Parse command for path to script directory
            script = [re.findall(script_pattern, rule["command"])[1] for script_pattern in SCRIPT_CAPTURES if len(re.findall(script_pattern, rule["command"])) > 1]
            if not script:
                raise ValueError("No valid scripts detected")
            script_path = "/".join(script[0].strip().split("/")[:-1])
            if not script_path:
                return(".")
        return(script_path)

def check_rules(rules):
    """Check that each job definition has at least the correct attributes, i.e. dependencies and command
    
    Return: Success or failure (bool)
    """
    for job in [_ for _ in rules.keys() if _ != "prepend"]:
        if any([_ not in rules[job] for _ in ["depends_on", "command"]]):
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