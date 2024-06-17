#first-
#just make something that can
#make matrices of the different
#settings that I want to use.
#worry about sorting into proper directories afterwards.

#function that combines lists of settings
#every setting is in a dictionary.
#so it constructs the filenames from the dictionary keys
#that were used to make the files.



import input_maker as ipm 
import os
import shutil

# past jobs
r2scan3c_opt_freq = ('r2scan_3c_of', '!R2SCAN-3C OPT FREQ')
b97_3c_opt_freq = ('b97_3c_of', '!B97-3C OPT FREQ')
pbeh3c_opt_freq = ('pbeh_3c_of', '!PBEh-3C OPT FREQ')

b3lyp_631g_dp_optfreq = ('b3lyp_631gdp_of', '!B3LYP 6-31G(d,p) OPT FREQ')
b3lyp_631_p_g_ss_optfreq = ('b3lyp_631pgss_of', '!B3LYP 6-31+G** OPT FREQ')
b3ylp_631_p_g_ss_d3bj_optfreq = ('b3lyp_631pgss_d3bj_of', '!B3LYP 6-31+G** D3BJ OPT FREQ')

b3lyp_6311_p_g2dp_optfreq = ('b3lyp_6311pg2dp_of', '!B3LYP 6-311+G(2d,p) OPT FREQ')
b3lyp_aug_cc_pvtz_d3bj_optfreq = ('b3lyp_aug_cc_pvtz_d3bj_of', '!B3LYP aug-cc-pVTZ D3BJ OPT FREQ')
b3lyp_def2_tzvp_d3bj_optfreq = ('b3lyp_def2_tzvp_d3bj_of', '!B3LYP def2-TZVP D3BJ OPT FREQ')

hf_3c_optfreq = ('hf_3c_of','!HF-3C OPT NUMFREQ')

#memory settings
v_high_mem = ('16','2-00:00:00', '64GB')
high_mem = ('8','2-00:00:00', '32GB')
med_mem = ('4','2-00:00:00', '16GB')
low_mem = ('2','2-00:00:00', '8GB')
lowest_mem = ('1','2-00:00:00', '4GB')

#SCF settings
hard_bs_scf = 'templates/orca_hardscf_bs.dat'
bs_scf = 'templates/orca_bsscf.dat'
hard_scf = 'templates/orca_hardscf.dat'
normal_scf = None

#geometry settings
hard_geom = 'templates/orca_hardgeom.dat'
normal_geom = None

#combined settings
normal_scfgeom = ('', (normal_scf, normal_geom))
bs_normal_scfgeom = ('bs', (bs_scf, normal_geom))
bs_strict_scfgeom = ('bs_strict', (hard_bs_scf, hard_geom))
hard_scfgeom = ('hard_scfgeom', (hard_scf, hard_geom))

#charge and multiplicity settings
neu_singlet = ('singlet', '0  1')
neu_doubet =  ('doublet', '0  2')
neu_triplet = ('triplet', '0  3')



def make_name_from_keys(key_list):
    name = key_list[0]
    for key in key_list[1:]:
        name += '_' + key

def make_orca_rcc_input(name, mem_sett, instruct, scf_geom_sett, charge_mult, molecule_xyz_file):
    os.makedirs(name, exist_ok=True)
    ipm.make_orca_input(name, instruct, mem_sett[0],
                        scf_geom_sett[0],scf_geom_sett[1],
                        charge_mult,molecule_xyz_file)
    ipm.make_orca_shell_script(name, name, name, name, 
                                mem_sett[0], mem_sett[1], mem_sett[2])
    os.rename(name + ".inp", os.path.join(name, name + ".inp"))
    os.rename(name + ".sh", os.path.join(name, name + ".sh"))

def get_master_shell_script(folder):
    source_file = os.path.join(ipm.template_path, 'run_all.sh')
    shutil.copy(source_file, os.path.join(folder, 'run_all.sh'))

def make_many_orca_rcc_inputs(folder, mem_setts, instructs, scf_geom_setts, charge_mults, molecules):
    '''
    accepts memory settings, along with various dictionary lists of parameters.
    the keys of the lists of parameters are used to construct a filename.
    Iterates through all combinations of parameters.
    and a shell script to run it.
    '''
    if type(instructs) is tuple:
        instructs = dict([instructs])
    if type(scf_geom_setts) is not dict:
        scf_geom_setts = {'' : scf_geom_setts}
    if type(charge_mults) is not dict:
        charge_mults = {'' : charge_mults}
        
    os.makedirs(folder, exist_ok=True)
    for i_key in instructs:
        for sg_key in scf_geom_setts:
            for c_key in charge_mults:
                for m_key in molecules:
                    name =  m_key + '_' + c_key + '_' + i_key + '_' + sg_key
                    make_orca_rcc_input(name, mem_setts, instructs[i_key],
                                        scf_geom_setts[sg_key], charge_mults[c_key],
                                        molecules[m_key])
                    os.rename(name, os.path.join(folder, name))
    get_master_shell_script(folder)
    
def molecule_dict_from_directory(directory):
    '''
    get all template molecules in the directory
    as a dict. 
    if present, reads keys.txt to get sites of the molecules; 
    these are appended as a dict.
    '''
    molecules = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.xyz'):
                basename = os.path.splitext(file)[0]
                molecule = os.path.join(root, file)
                molecules[basename] = (molecule)
    return molecules
            
    
