import os
import re
import shutil
import json
import helpers

CONFIGPATH = './'
ORCACONFIG = 'orca_config.json'
GAUSSCONFIG = 'gaussian_config.json'

class Input:
    def __init__(self): 
        self.directory = ""
        self.basename = ""
        self.extension = ""
        self.keywords = []
        self.charge = 0
        self.multiplicity = 1
        self.xyzfile = "" 
        #self.xyzpath = "" #what is this, and why?
    
    def cleanup(self):
        raise NotImplementedError()

    def write_file(self):
        raise NotImplementedError()

    def load_file(self,filename,directory=None):
        raise NotImplementedError()


class ORCAInput(Input):
    def __init__(self):
        Input.__init__(self)
        self.strings = []
        self.blocks = {}
        self.extension = '.inp'

    def cleanup(self):
        self.keywords = [keyword for keyword in self.keywords if keyword]
        self.strings = [string for string in self.strings if string]
        self.blocks = {block : self.blocks[block] for block in self.blocks if block}
        return self
    
    def write_file(self):
        self.cleanup()
        full_path= os.path.join(self.directory,self.basename) + self.extension 
        with open (full_path,'w') as file:
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

    def load_file(self,filename,directory=None):
        self.basename = os.path.splitext(filename)[0]
        self.directory = directory
        if directory:
            filename = os.path.join(directory,filename)
        with open(filename,'r') as input_file:
            lines = input_file.readlines()
             
        self.keywords = []
        self.blocks = {}
        self.strings = []
        self.charge = 0
        self.multiplicity = 1
        self.xyzfile = ''

        in_block_flag = False
        temp_block = ['',[]]
        for line in lines:
            print(line)
            #TODO: MAKE THIS MORE FLEXIBLE TO MATCH WITH ALL ORCA SYNTAX
            if in_block_flag:
                if re.match(r'\s*end',line,re.I):
                    self.blocks[temp_block[0]] = temp_block[1]
                    in_block_flag = False
                    temp_block[0] = ''
                    temp_block[1] = []
                    print(f'ending block')
                else:
                    print('in temp block')
                    temp_block[1].append(line.strip())

            elif re.match(r'\s*%\s*maxcore\s+\d+',line,re.I):
                print('maxcore line found')
                self.strings.append(line.strip())

            elif re.match(r'\s*!',line):
                line = re.match(r'(?:\s*!)(.*)',line).group(1)
                keys = list(re.split(r'\s+',line))
                self.keywords.extend(keys)
                print(f'adding keywords: {keys}')
           
            elif re.match(r'\s*%',line):
                name = re.match(r'(?:\s*%)(\b.+\b)',line).group(1)
                temp_block[0] = name
                in_block_flag = True
                print(f'starting block with name: {name}')


            elif re.match(r'\s*\*\s*xyz',line,re.I):
                self.charge = int(re.search(r'(\d+)(?:\s+\d+)',line).group(1))
                self.multiplicity = int(re.search(r'(?:\d+\s+)(\d+)',line).group(1))
                if re.match(r'\s*\*\s*xyzfile',line,re.I):
                    self.xyzfile = re.search(r'(\S+\.xyz\b)',line).group(1)
                print(f'charge: {self.charge} multiplicity: {self.multiplicity} xyz fn: {self.xyzfile}')

class GaussianInput(Input):
    def __init__(self):
        Input.__init__(self)
        self.nprocs = 1
        self.mem_per_cpu_gb = 2
        self.title = "super secret special scripts shaped sthis submission sfile"
        self.extension = ".gjf"

    def cleanup(self):
        self.keywords = [keyword for keyword in self.keywords if keyword]
    
    def write_file(self):
        self.cleanup()
        full_path = os.path.join(self.directory,self.basename) + self.extension
        #NOTE: Gaussian input assumes an xyz file in the same directory as the .gjf file to be made 
        #full_xyz_path = os.path.join(self.directory,self.xyzfile)  
        with open(self.xyzfile,'r') as xyzfile:
            coordinates = xyzfile.readlines()[2:]
        with open(full_path,'w') as gjffile:
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
    
    def load_file(self):
        

class SbatchScript:
    def __init__(self):
        self.directory = ""
        self.basename= ""
        self.sbatch_statements = []
        self.commands = []

    def write_file(self):
        full_path = os.path.join(self.directory,self.basename) + '.sh'
        with open (full_path,'w') as file:
            file.write('#!/bin/bash\n\n')
            for statement in self.sbatch_statements:
                file.write(f'#SBATCH {statement.strip()}\n')
            file.write('\n')
            for command in self.commands:
                file.write(f'{command.strip()}\n')


class Job:
    def __init__(self):
        self.directory = "./"
        self.inp = Input() #or None, or other type #this throws an exception if not replaced
        self.sh = SbatchScript()
        self.xyzpath = "./"
        self.xyz = "test.xyz"
        
    def create_directory(self):
        if not self.xyzpath.endswith('/'):
            self.xyzpath = f'{self.xyzpath}/'
        if not self.directory.endswith('/'):
            self.directory = f'{self.directory}/'
        
        os.makedirs(self.directory,exist_ok=True)

        #print(f'path: {self.directory}')
        self.inp.path = self.directory
        self.inp.write_file()

        #print(f'sh path: {self.directory}')
        self.sh.path = self.directory
        self.sh.write_file()

        source_file = f'{self.xyzpath}{self.xyz}'
        dest_file = f'{self.directory}{self.xyz}'
        try:
            shutil.copyfile(source_file, dest_file)
        except Exception as e:
            print(f"Error copying file: {e}")




class InputBuilder:
    def __init__(self):
        raise NotImplementedError('InputBuilder is an abstract class')
        self.config = helpers.load_config_from_file('/path/to/config')

    def change_params(self,diff_config):
        for key in diff_config:
            self.config[key] = diff_config[key]
        return self

    def build_input(self):
        raise NotImplementedError()

    def submit_line(self):
        raise NotImplementedError()

    def build_submit_script(self):
        sh = SbatchScript()
        sh.path = self.config['write_directory']
        sh.basename = self.config['job_name']
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
        
        sh.commands.append(self.submit_line())

        if self.config['post_submit_lines'] is not None:
            for line in self.config['post_submit_lines']:
                sh.commands.append(line)
        return sh


    def build(self):
        newjob = Job()
        
        newjob.path = self.config['write_directory']
        newjob.xyzpath = self.config['xyz_directory'] 
        newjob.xyz = self.config['xyz_file']

        newjob.sh = self.build_submit_script() 
        newjob.inp = self.build_input()
        
        return newjob
       
    
class ORCAInputBuilder(InputBuilder):
    def __init__(self):
        self.config = helpers.load_config_from_file(f'{CONFIGPATH}{ORCACONFIG}') 
    
    def submit_line(self):
        return f"{self.config['path_to_program']} {self.config['job_name']}.inp > {self.config['job_name']}.out"
    
    def build_input(self):
        ################ inp options #####################
        inp = ORCAInput() 
        inp.directory = self.config['write_directory']
        inp.basename = self.config['job_name']
        
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



class GaussianInputBuilder(InputBuilder):
    def __init__(self):
        self.config = helpers.load_config_from_file(f"{CONFIGPATH}{GAUSSCONFIG}")

    def submit_line(self):
        return f"{self.config['path_to_program']} < {self.config['job_name']}.gjf > {self.config['job_name']}.log"

    def build_input(self):
        inp = GaussianInput()
        #TODO: FIX THIS LATER

        inp.directory = self.config['write_directory']
        inp.basename = self.config['job_name']
        
        inp.keywords = [
            self.config['run_type'],
            f"{'u' if self.config['uks'] else ''}{self.config['functional']}/{self.config['basis']}",
            self.config['aux_basis'],
            self.config['density_fitting'],
            self.config['dispersion_correction'],
            self.config['bsse_correction'],
            self.config['integration_grid'],
        ]
        inp.keywords.append(self.config['other_keywords'])

        nprocs = self.config['num_cores']
        mem_per_cpu_gb = self.config['mem_per_cpu_GB']
        inp.charge = self.config['charge']
        inp.multiplicity = self.config['spin_multiplicity']
        inp.xyzfile = os.path.join(self.config['xyz_directory'],self.config['xyz_file']) 
        return inp
