import input_array_maker as ipam

mols = ipam.molecule_dict_from_directory('../mike/new_paper')

ipam.make_many_orca_rcc_inputs('mike_jul10_alkynes_job_singlets',ipam.high_mem,dict([ipam.uks_r2scan3c,ipam.uks_pbeh3c,ipam.uks_cam_b3lyp_631g_dp]),dict([ipam.normal_scfgeom,ipam.bs_normal_scfgeom]),dict([ipam.neu_singlet]),mols)


ipam.make_many_orca_rcc_inputs('mike_jul10_alkynes_job_triplets',ipam.high_mem,dict([ipam.uks_r2scan3c,ipam.uks_pbeh3c,ipam.uks_cam_b3lyp_631g_dp]),dict([ipam.normal_scfgeom]),dict([ipam.neu_triplet]),mols)



ipam.make_many_orca_rcc_inputs('mike_jul12',ipam.high_mem,dict([ipam.uks_r2scan3c]),dict([ipam.bs_normal_scfgeom]),dict([ipam.neu_singlet]),singlet_mols)


ipam.make_many_orca_rcc_inputs('mike_jul12',ipam.high_mem,dict([ipam.uks_r2scan3c]),dict([ipam.normal_scfgeom]),dict([ipam.neu_triplet]),triplet_mols)


import input_array_maker as ipam


mols = ipam.molecule_dict_from_directory('./dummy_strucs')


ipam.make_many_orca_rcc_inputs('queue_test',ipam.high_mem,dict([ipam.uks_r2scan3c]),dict([ipam.normal_scfgeom]),dict([ipam.neu_singlet]),mols)
