import os
import shutil
import json
import helpers

CONFIGPATH = './'
ORCACONFIG = 'orca_config.json'

class OrcaInput:
    def __init__(self):
        self.path = ""
        self.filename = ""
        self.keywords = []
        self.strings = []
        self.blocks = {}
        
        self.charge = 0
        self.multiplicity = 1
        self.xyzfile = ""

    def cleanup(self):
        self.keywords = [keyword for keyword in self.keywords if keyword]
        self.strings = [string for string in self.strings if string]
        self.blocks = {block : self.blocks[block] for block in self.blocks if block}
        return self
    
    def write_file(self):
        self.cleanup()
        if not self.path.endswith('/'):
            self.path = f'{self.path.strip()}/'
        with open (f'{self.path}{self.filename}.inp','w') as file:
            for keyword in self.keywords:
                file.write(f'! {keyword.strip()}\n')
            file.write('\n')
            for string in self.strings:
                file.write(f'{string.strip()}\n')
            file.write('\n')
            for block in self.blocks:
                file.write(f'%{block.strip()}\n')
                for line in self.blocks[block]:
                    file.write(f' {line.strip()}\n')
                file.write('end\n\n')
            file.write('\n')
            file.write(f"* xyzfile {self.charge} {self.multiplicity} {self.xyzfile} \n\n")

    
class SbatchScript:
    def __init__(self):
        self.path = ""
        self.filename = ""
        self.sbatch_statements = []
        self.commands = []

    def write_file(self):
        if not self.path.endswith('/'):
            self.path = f'{self.path}/'
        with open (f'{self.path.strip()}{self.filename.strip()}.sh','w') as file:
            file.write('#!/bin/bash\n\n')
            for statement in self.sbatch_statements:
                file.write(f'#SBATCH {statement.strip()}\n')
            file.write('\n')
            for command in self.commands:
                file.write(f'{command.strip()}\n')


class Job:
    def __init__(self):
        self.path = "./"
        self.inp = OrcaInput() #or None, or other type
        self.sh = SbatchScript()
        self.xyzpath = "./"
        self.xyz = "test.xyz"
        
    def create_directory(self):
        if not self.xyzpath.endswith('/'):
            self.xyzpath = f'{self.xyzpath}/'
        if not self.path.endswith('/'):
            self.path = f'{self.path}/'
        
        os.makedirs(self.path,exist_ok=True)

        #print(f'path: {self.path}')
        self.inp.path = self.path
        self.inp.write_file()

        #print(f'sh path: {self.path}')
        self.sh.path = self.path
        self.sh.write_file()

        source_file = f'{self.xyzpath}{self.xyz}'
        dest_file = f'{self.path}{self.xyz}'
        try:
            shutil.copyfile(source_file, dest_file)
        except Exception as e:
            print(f"Error copying file: {e}")




class InputBuilder:
    def __init__(self):
            #defaults set here. In the future, uncouple from code
            self.config = helpers.load_config_from_file(f'{CONFIGPATH}{ORCACONFIG}')

    def change_params(self,diff_config):
        #change everything in self.config with diff_config.
        #diff_config files should be sparse to reflect this
        for key in diff_config:
            self.config[key] = diff_config[key]
        return self
    def build_input(self):
        pass

    def build_submit_script(self):
        sh = SbatchScript()
        sh.path = self.config['write_directory']
        sh.filename = self.config['job_name']
        sh.sbatch_statements = [
            f"--job-name={self.config['job_name']}",
            f"-n {self.config['num_cores']}",
            f"-N 1",
            f"-p genacc_q",
            f"-t {self.config['runtime']}",
            f"--mem-per-cpu={self.config['mem_per_cpu_GB']}GB",
        ]
        if self.config['pre_submit_lines'] is not None:
            for line in self.config['pre_submit_lines']:
                sh.commands.append(line)
        
        sh.commands.append(
            f"{self.config['path_to_program']} {self.config['job_name']}.inp > {self.config['job_name']}.out"
        )

        if self.config['post_submit_lines'] is not None:
            for line in self.config['post_submit_lines']:
                sh.commands.append(line)
        return sh


    def build(self):
        newjob = Job()
        
        newjob.path = self.config['write_directory']
        newjob.xyzpath = self.config['xyz_directory'] 
        newjob.xyz = self.config['xyz_file']

        newjob.sh = build_submit_script() 
        newjob.inp = build_input()
        
        return newjob
        
class ORCAInputBuilder(InputBuilder):
    def build_input()
        ################ inp options #####################
        inp = ORCAInput() 
        inp.path = self.config['write_directory']
        inp.filename = self.config['job_name']
        
        inp.keywords = [
            'UKS' if self.config['uks'] else None,
            self.config['functional'],
            self.config['basis'],
            self.config['aux_basis'],
            self.config['density_fitting'],
            self.config['dispersion_correction'],
            self.config['bsse_correction'],
            'UNO' if self.config['natural_orbitals'] else None,
            self.config['integration_grid'],
            self.config['run_type'],
        ]
        inp.keywords.append(self.config['other_keywords'])

        
        maxcore = int(self.config['mem_per_cpu_GB']) * 1000 * (3 / 4)
        inp.strings.append(f"%maxcore {int(maxcore)}")
        if not self.config['blocks'].get('pal',None):
            inp.blocks['pal'] = [f"nprocs {self.config['num_cores']}",]
            
        for name in self.config['blocks']:
            inp.blocks['name'] = self.config['blocks'][name]
        
        if self.config['broken_symmetry']:
            if not inp.blocks.get('scf',None):
                inp.blocks['scf'] = ['brokensym 1,1']
            else:
                condition = False
                for line in inp.blocks['scf']:
                    if 'brokensym' in line.lower():
                        condition = True
                if not condition:
                    inp.blocks['scf'].append('brokensym 1,1')
        
        inp.charge = self.config['charge']
        inp.multiplicity = self.config['spin_multiplicity']
        inp.xyzfile = self.config['xyz_file']
        return inp
