from dataclasses import dataclass

import input_maker as ipm
import os
import shutil

#the idea here:
# 1. make a class that holds all the information for a job
# 2. make a class that formats the job into a directory
# 


# dicts are a pain to work with.
# the main QOL change I want is a config file 
# and that it would let me re-use settings.
# abstract that it uses dicts away from the user most of the time.

@dataclass
class JobMatrix:
    directory: str #string
    
    cpu_cores: int #integer number
    memory: int #integer number
    nodes: int #integer number
    
    molecule_xyz_files: dict #string
    
    charges: dict#integer number
    spin_multiplicities: dict #integer number
    
    functionals: dict#b3lyp, etc.
    basis_sets: dict #cc-pvdz, etc.
    corrections: dict #d3bj, etc.
    
    operations: dict #opt, freq, sp, etc.
    
    scf_settings: dict #broken symmetry, etc.
    geometry_settings: dict # convergence criteria, etc.
    
    
@dataclass
class JobInfo:
    directory: str #string
    filename: str #string
    
    cpu_cores: int #integer number
    memory: int
    nodes: int
    
    molecule_xyz_file: str #string
    
    charge: int#integer number
    spin_multiplicity: int
    
    functional: str#b3lyp, etc.
    basis_set: str
    corrections: str
    
    operation: str #opt, freq, sp, etc.
    
    scf_setting: str #broken symmetry, etc.
    geometry_setting: str # convergence criteria, etc.
    

class DefaultOptions:
    def __init__(self):
        pass
    
# this is the class that reads jobmatrix files.
# start with basic functionality that already exists.
# it will even be a little simpler, since there will be a kind
# of shell around it. It doesn't need to be as flexible.

# right now, make it just for orca. That's all I need at the moment.
# i can think about making it more flexible when I want to share it.

class JobFormatter:
    def __init__(self, config_filename):
        pass
        
    def make_orca_rcc_input(self, job: JobInfo):
        os.makedirs(job.filename, exist_ok=True)
        ipm.make_orca_input(job.filename, job.instruct, job.mem_sett[0],
                            job.scf_geom_sett[0],job.scf_geom_sett[1],
                            job.charge_mult, job.molecule_xyz_file)
        ipm.make_orca_shell_script(job.filename, job.filename, job.filename, job.filename, 
                                    job.mem_sett[0], job.mem_sett[1], job.mem_sett[2])
        os.rename(job.filename + ".inp", os.path.join(job.filename, job.filename + ".inp"))
        os.rename(job.filename + ".sh", os.path.join(job.filename, job.filename + ".sh"))
