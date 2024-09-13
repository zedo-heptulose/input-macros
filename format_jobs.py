from dataclasses import dataclass

import os
import shutil
import re
import itertools

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
    
    charges: dict #integer number
    spin_multiplicities: dict #integer number
    
    functionals: dict #b3lyp, etc.
    basis_sets: dict #cc-pvdz, etc.
    corrections: dict #d3bj, etc.
    
    operations: dict #opt, freq, sp, etc.
    
    scf_settings: dict #list of strings... broken symmetry, etc.
    geometry_settings: dict #list of strings... convergence criteria, etc.
    
    
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
        self.config_filename = config_filename
        self.orca_template_filename = 'orca_template.dat'
        self.shell_template_filename = 'rcc_template.sh'
        self.master_script_filename = 'run_all.sh'
    
    def make_full_job(self, jm: JobMatrix):
        '''
        accepts memory settings, along with various dictionary lists of parameters.
        the keys of the lists of parameters are used to construct a filename.
        Iterates through all combinations of parameters.
        and a shell script to run it.
        '''
        os.makedirs(jm.directory, exist_ok=True)
        instructs = [jm.functionals, jm.basis_sets, jm.corrections, jm.operations]
        scf_geom_setts = [jm.scf_settings, jm.geometry_settings]
        charge_mults = [jm.charges, jm.spin_multiplicities]
        molecules = jm.molecule_xyz_files
        mem_setts = [jm.memory, jm.cpu_cores, jm.nodes]
        
        job_space = itertools.product(jm.functionals,
                          jm.basis_sets,
                          jm.corrections,
                          jm.operations,
                          jm.scf_settings,
                          jm.geometry_settings,
                          jm.charges,
                          jm.spin_multiplicities,
                          jm.molecule_xyz_files,
                        )
        jm.memory,
        jm.cpu_cores,
        jm.nodes
        
        for funk, bask, cork, oprk, scfk, geok, chrk, mltk , molk, in job_space:
            name = molk + '_' + chrk + '_' + funk + '_' + bask + '_' + cork + '_' + oprk + '_' + scfk + '_' + geok
            new_job = JobInfo(name, 
                              name, 
                              jm.cpu_cores, 
                              jm.memory, 
                              jm.nodes, 
                              molk, 
                              chrk, 
                              mltk, 
                              funk, 
                              bask, 
                              cork, 
                              oprk, 
                              scfk, 
                              geok)
        
        self.make_orca_rcc_directory(new_job)
        self.get_master_shell_script(jm.directory)
    
    def get_master_shell_script(folder):
        source_file = os.path.join(self.master_script_filename, 'run_all.sh')
        shutil.copy(source_file, os.path.join(folder, 'run_all.sh'))
    
    def make_orca_rcc_directory(self, job: JobInfo):
        os.makedirs(job.directory, exist_ok=True)
        self.make_orca_input(job)
        self.make_orca_shell_script(job)
        os.rename(job.filename + ".inp", os.path.join(job.directory, job.filename + ".inp"))
        os.rename(job.filename + ".sh", os.path.join(job.directory, job.filename + ".sh"))
        
    def make_orca_shell_script(self, _job: JobInfo):
        job_name_string = '#SBATCH --job-name='
        num_cores_string = '#SBATCH -n '
        time_string = '#SBATCH -t '
        mem_string = '#SBATCH --mem='
        path_to_orca = '/gpfs/research/software/orca/orca_5_0_1_linux_x86-64_openmpi411/orca'
        
        if not rcc_filename.endswith('.sh'):
            rcc_filename += '.sh'
        if not orca_infilename.endswith('.inp'):
            orca_infilename += '.inp'
        if not orca_outfilename.endswith('.out'):
            orca_outfilename += '.out'
        
        job_name = _job.filename.split('.')[0]    
    
        format_0 = job_name_string + job_name
        format_1 = num_cores_string + str(_job.cpu_cores)
        format_2 = time_string + _job.max_runtime
        format_3 = mem_string + _job.memory + 'GB'
        format_4 = path_to_orca + ' ' + f'{job_name}.inp' + ' > ' + f'{job_name}.out'
        
        list_of_fields = [format_0, format_1, format_2, format_3, format_4]
        
        self.format_input_file(self.shell_template_filename, rcc_filename, list_of_fields)
        
        
    def make_orca_input(self, _job: JobInfo):
        job = _job.copy()
        
        if not job.filename.endswith('.inp'):
            job.filename += '.inp'
        
        if not job.cpu_cores:
            raise ValueError('nprocs must be set')
        
        instructions = f'!{job.functional} {job.basis_set} {job.corrections} {job.operation}\n'
        
        maxcore_line = f'%maxcore {job.memory // job.cpu_cores * 1000}\n'
        
        nprocs_lines = "\n".join(r'%pal',f' nprocs {job.cpu_cores}','end\n')
            
        scf_lines = job.scf_setts if job.scf_setting else None
        
        geom_lines = job.geom_setts if job.geom_setting else None
        
        xyz_lines = self.read_xyz(job.molecule_xyz_file)
        
        charge_mult_line = f'* XYZ {job.charge} {job.spin_multiplicity}\n'
        
        coord_lines = [charge_mult_line] + xyz_lines + ['*']
        
        format_list = [instructions, maxcore_line, nprocs_lines, scf_lines, geom_lines, coord_lines]
        
        self.format_input_file(self.orca_template_filename, job.filename, format_list)
            
            
    def read_xyz(self, xyz_fn: str):
        with open(xyz_fn, 'r') as xyz:
            xyz_lines = xyz.readlines()
            return xyz_lines[2:]
            
            
    def format_input_file(rules_fn: str, output_fn: str, list_of_fields: list):

        with open(rules_fn, 'r') as template:
            lines = template.readlines()
        
        arg_pattern = re.compile(r'(?:{)(\d+)(?:})')
        with open(output_fn, 'w') as output:
            for line in lines:
                match = re.search(arg_pattern, line)
            
                if match:
                    index = int(match.group(1))
                    if index >= len(list_of_fields):
                        pass
                    else:
                        field = list_of_fields[index]
                        if isinstance(field, str):
                            output.write(list_of_fields[index].rstrip() + '\n')
                        
                        elif isinstance(field, list):
                            for element in field:
                                if isinstance(element, str):
                                    output.write(element.rstrip() + '\n')
                                else:
                                    type(element)
                                    print ('error for element: ' + str(element) + " of type " + str(type(element)))
                                    raise ValueError('data type other than string, list(string), or None in list_of_fields\n')
                                
                        elif field is None:
                            pass
                        
                        else:
                            type(element)
                            print ('error for element: ' + str(element) + " of type " + str(type(element)))
                            raise ValueError('data type other than string, list(string), or None in list_of_fields\n')
                        
                else:
                    output.write(line.rstrip() + '\n')
