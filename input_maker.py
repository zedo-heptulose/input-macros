import re

template_path = '/home/zedo_heptulose/programming/Chemistry/RCC/input_macros/templates/'

def read_xyz(xyz_filename):
    with open(xyz_filename, 'r') as xyz:
        lines = xyz.readlines()
        return lines[2:]
    
    
    
def format_input_file(rules_filename, write_filename, list_of_fields):
    '''
    formats files using list of fields
    list of fields can contain strings, lists of strings, or None
    '''
    
    with open(rules_filename, 'r') as template:
        lines = template.readlines()
    
    arg_pattern = re.compile(r'(?:{)(\d+)(?:})')
    with open(write_filename, 'w') as output:
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



def make_gaussian_input(gaussian_filename, instructions, title, check_path = None, charge_multiplicity = None, xyz_filename = None, other_data=None):
    xyz_lines = read_xyz(xyz_filename)
    list_of_fields = [instructions, title, check_path, charge_multiplicity, xyz_lines, other_data] 
    gauss_tempname = template_path + 'gaussian_template.dat'
    format_input_file(gauss_tempname, gaussian_filename, list_of_fields)
    
    
    
def make_orca_input(orca_fn, instructions, nprocs, scf_fn, geom_fn, charge_mult, xyz_fn):
    '''
    function that uses file formatter to make orca input
    takes as parameters:
    orca filename (filename of .inp file, .inp extension optional)
    instructions: the job to be run; ex !R2SCAN3C OPT FREQ
    nprocs: integer number of CPU cores to use.
    scf_filename: file to read scf settings from.
    charge_mult: string of the form '<int>  <int>'
    xyz_filename: file to read xyz coordinates from.
    '''
    if not orca_fn.endswith('.inp'):
        orca_fn += '.inp'
    
    if nprocs:
        nprocs_lines = []
        nprocs_lines.append(r'%pal')
        nprocs_lines.append(' nprocs ' + str(nprocs))
        nprocs_lines.append('end')
    else:
        nprocs = None
    
    if scf_fn:
        with open(scf_fn, 'r') as scf:
            scf_lines = scf.readlines()
    else:
        scf_lines = None
    
    if geom_fn:
        with open(geom_fn, 'r') as geom:
            geom_lines = geom.readlines()
    else:
        geom_lines = None
            
    #XYZ BLOCK
    xyz_lines = read_xyz(xyz_fn)
    cm_line = '* XYZ ' + charge_mult
    coord_lines = []
    coord_lines.append(cm_line)
    coord_lines += xyz_lines
    coord_lines.append('*')
    
    list_of_fields = [instructions, nprocs_lines, scf_lines, geom_lines, coord_lines]
    
    orca_template_fn = template_path + 'orca_template.dat'
    format_input_file(orca_template_fn, orca_fn, list_of_fields)
    
    
    
def make_orca_shell_script(rcc_filename, orca_infilename, orca_outfilename, job_name, num_cores, max_runtime, memory):
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
        
    format_0 = job_name_string + job_name
    format_1 = num_cores_string + str(num_cores)
    format_2 = time_string + max_runtime
    format_3 = mem_string + memory
    format_4 = path_to_orca + ' ' + orca_infilename + ' > ' + orca_outfilename
    
    list_of_fields = [format_0, format_1, format_2, format_3, format_4]
    
    shell_template_filename = template_path + 'rcc_shell_template.dat'
    format_input_file(shell_template_filename, rcc_filename, list_of_fields)


def make_crest_rcc_shell_script(rcc_filename, orca_infilename, orca_outfilename, job_name, num_cores, max_runtime, memory):
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
        
    format_0 = job_name_string + job_name
    format_1 = num_cores_string + str(num_cores)
    format_2 = time_string + max_runtime
    format_3 = mem_string + memory
    format_4 = path_to_orca + ' ' + orca_infilename + ' > ' + orca_outfilename
    
    list_of_fields = [format_0, format_1, format_2, format_3, format_4]
    
    shell_template_filename = template_path + 'rcc_shell_template.dat'
    format_input_file(shell_template_filename, rcc_filename, list_of_fields)

