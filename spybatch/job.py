import os

class Job: 
    """SLURM job class

    Attributes: 
        name (str): Name of the job
        depends_on (set): Set of immediate parent job dependencies
        params (dict): Keyword job parameters, matching those found in config file
        command (str): Command to be submitted
        slurm_id (int): Job submission id
        is_satisfied (bool): Is the job ready to be queued?
    """
    def __init__(
            self, 
            name, 
            depends_on, 
            params, 
            command,
            slurm_id = None): 
        self._name = name
        self._depends_on = depends_on
        self._params = params
        self._command = command

    @property
    def name(self):
        return(self._name)

    @property
    def depends_on(self):
        return(self._depends_on)

    def __eq__(self, other):
        if (isinstance(other, Job)):
            return(self.name == other.name)

    def __repr__(self):
        return(self._name)

    def check_dependencies(self, check_against):
        """Check if this job's dependencies are all found within the input list
        """
        if (self._depends_on.issubset(check_against)):
            self.is_ready = True
        else:
            self._is_satistfied = False
        return(self.is_ready)

    def build_submission(self, slurm_script, shell_prepend = None):
        """Build job submission script

        Function will write a SLURM submission script to the tmp_dir

        return: File handle to the submission script
        """
        prefix = "#SBATCH"
        script = ["#!/usr/bin/env bash"]
        script += [
            (" ".join((prefix, parameter, self._params[parameter]))) 
            for parameter in self._params.keys()
        ]
        script += [shell_prepend, self._command]
        slurm_script.write('\n'.join(script))
