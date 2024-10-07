import os
import shutil
import json
import helpers
import orca_input 

CONFIGPATH = './'
GAUSSCONFIG = 'gaussian_config.json'

class GaussianInput:
    def __init__(self):
        self.path = ""
        self.filename = ""
        self.nprocs = 1
        self.mem_per_cpu_gb = 2
        self.keywords = []
        self.title = "created with so and so tool"
        self.charge = 0
        self.multiplicity = 1
        self.xyzfile = "" 
        self.xyzpath = ""

    def cleanup(self):
        self.keywords = [keyword for keyword in self.keywords if keyword]
    
    def write_file(self):
        self.cleanup()
        full_path_basename = os.path.join(self.path,self.filename)
        with open(f'{self.xyzfile}','r') as xyzfile:
            coordinates = xyzfile.readlines()[2:]
        with open(f'{full_path_basename}.gjf','w') as gjffile:
            gjffile.write(f"%nprocshared={self.nprocs}\n")
            gjffile.write(f"%mem={self.nprocs*self.mem_per_cpu_gb}gb\n")
            gjffile.write(f"%chk={full_path_basename}.chk\n")
            gjffile.write(f"#{' '.join(self.keywords)}\n")
            gjffile.write(f"\n")
            gjffile.write(f"{self.title}\n")
            gjffile.write(f"\n")
            gjffile.write(f"{self.charge} {self.multiplicity}\n")
            gjffile.writelines(coordinates)
            gjffile.write(f"\n\n")

class GaussianInputBuilder:
    def __init__(self):
        self.config = helpers.load_config_from_file(f"{CONFIGPATH}{GAUSSCONFIG}")

    def change_params(self,diff_config):
        for key in diff_config:
            self.config[key] = diff_config[key]
        return self

    def build(self):
        newjob = orca_input.Job()
        newjob.inp = GaussianInput()
        #TODO: FIX THIS LATER
        newjob.path = os.path.join(self.config['write_directory'],self.config['job_name'])
        newjob.xyzpath = self.config['xyz_directory']
        newjob.xyz = self.config['xyz_file'] 
        #this will be a problem, since we're writing coords in the file here

        ###################### sh options ###########################
        newjob.sh.path = self.config['write_directory']
        newjob.sh.filename = self.config['job_name']
        newjob.sh.sbatch_statements = [
            f"--job-name={self.config['job_name']}",
            f"-n {self.config['num_cores']}",
            f"-N 1",
            f"-p genacc_q",
            f"-t {self.config['runtime']}",
            f"--mem-per-cpu={self.config['mem_per_cpu_GB']}GB",
        ]
        if self.config['pre_submit_lines'] is not None:
            for line in self.config['pre_submit_lines']:
                newjob.sh.commands.append(line)
        
        newjob.sh.commands.append(
            f"{self.config['path_to_program']} < {self.config['job_name']}.gjf > {self.config['job_name']}.log"
        )

        if self.config['post_submit_lines'] is not None:
            for line in self.config['post_submit_lines']:
                newjob.sh.commands.append(line)

        
        ################ inp options #####################

        newjob.inp.path = self.config['write_directory']
        newjob.inp.filename = self.config['job_name']
        
        newjob.inp.keywords = [
            f"{'u' if self.config['uks'] else ''}{self.config['functional']}/{self.config['basis']}",
            self.config['aux_basis'],
            self.config['density_fitting'],
            self.config['dispersion_correction'],
            self.config['bsse_correction'],
            'UNO' if self.config['natural_orbitals'] else None,
            self.config['integration_grid'],
            self.config['run_type'],
        ]
        newjob.inp.keywords.append(self.config['other_keywords'])

        newjob.nprocs = self.config['num_cores']
        newjob.mem_per_cpu_gb = self.config['mem_per_cpu_GB']
        newjob.inp.charge = self.config['charge']
        newjob.inp.multiplicity = self.config['spin_multiplicity']
        newjob.inp.xyzfile = os.path.join(self.config['xyz_directory'],self.config['xyz_file'])
        
        return newjob
