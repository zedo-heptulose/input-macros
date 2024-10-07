import itertools

import orca_input
import os
import helpers

def product_of_options(*args,**kwargs):
    #each arg is a list of dicts
    #the output is a cartesian product of all of them
    product = []
    for arg in 
            
def build_orca_output_array(xyz_paths,options_list,write_directory='./',**kwargs):
    #this requires a list of xyz filenames including paths,
    #a list of config dicts,
    #and a path to write all of them to.
    #kwargs: sep
    sep = kwargs.get('sep','_')
    
    for path in xyz_paths:
        dir_path = os.path.dirname(path)
        basename = os.path.basename(path)
        mol_name = os.path.splitext(basename)
        for _options in options_list:
            options = _options.copy()
            options['write_directory'] = os.path.join(
                                            write_directory,
                                            options['write_directory']
                                            )
            options['xyz_directory'] = dir_path
            options['xyz_file'] = basename
            
            list_name_frags = []
            list_name_frags.append(mol_name)
            
            if type(options['name_fragments']) is list: 
                list_name_frags.extend(options['name_fragments'])
            elif type(options['name_fragments']) is str:
                list_name_frags.append(options['name_fragments'])

            options['job_name'] = sep.join(list_name_frags)

            job_builder = orca_input.ORCAInputBuilder()
            job_builder.change_params(options)
            job = job_builder.build()
            
            job.write_file()
                    
            