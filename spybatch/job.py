import os

class Job: 
    """SLURM job class

    Attributes: 
        name (str): Name of the job
        depends_on (set): Set of immediate parent job dependencies
        params (dict): Keyword job parameters, matching those found in config file
        command (str): Command to be submitted
    """
    def __init__(
            self, 
            name, 
            depends_on, 
            params, 
            command): 
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
        return('\n'.join(
            [
                "Job Name: " + self._name,
                "Depends on " + ", ".join(self._depends_on),
                "With parameters " + ", ".join([
                    " : ".join([a, self._params[a]]) for a in self._params
                ]),
                "Execution: " + self._command
            ]
        ))

    def check_dependencies(self, check_against):
        """Check if this job's dependencies are all found within the input list
        """
        if (self._depends_on.issubset(check_against)):
            self.is_ready = True
        else:
            self._is_satistfied = False
        return(self.is_ready)

    def build_submission(self, slurm_script):
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
        script += self._command
        slurm_script.write('\n'.join(script))
