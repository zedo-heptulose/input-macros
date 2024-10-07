import orca_input as inp_lib
import helpers

CONFIGPATH = './'
XTBCONFIG = 'xtb_config.json'

class xTBInputBuilder:
    def __init__(self):
        self.config = helpers.load_config_from_file(f'{CONFIGPATH}{XTBCONFIG}')

    def change_params(self,diff_config):
        for key in diff_config:
            self.config[key] = diff_config[key]
        return self

    def build(self):
        newjob = inp_lib.Job()

        newjob.path = self.config['write_directory']
        newjob.xyzpath = self.config['xyz_directory']
        newjob.xyz = self.config['xyz_file']

        
        newjob.sh.filename = self.config['job_name']
        newjob.sh.path = self.config['write_directory']
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
        
        if self.config['post_submit_lines'] is not None:
            for line in self.config['post_submit_lines']:
                newjob.sh.commands.append(line)
        #########ONLY THIS PART IS UNIQUE, FOR FUTURE REFACTORING
        newjob.sh.commands.extend([
            f"export OMP_STACKSIZE={self.config['mem_per_cpu_GB']}G",
            f"export OMP_NUM_THREADS={self.config['num_cores']},1"
            ])
                        
        newjob.sh.commands.append(
            f"{self.config['path_to_program']} {self.config['xyz_file']} > {self.config['job_name']}.out -P {self.config['num_cores']} --{self.config['functional'].lower()} --{self.config['run_type'].lower()}" 
            #functional MUST be gfn1,gfn2,gfn0, or gfnff
        )
        
        return newjob

        