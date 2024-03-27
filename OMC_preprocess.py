# This script processes the raw marker data
# Input is a MM report .txt file
# Output is a .trc file

from OMC_IK_functions import *
import os

""" SETTINGS """

# Quick Settings
subject_code = 'P1'
trial_name_list = ['CP', 'JA_Slow', 'JA_Fast', 'ROM', 'ADL']
sample_rate = 100


""" MAIN """

# Create/specify some file directories
parent_dir = r'C:\Users\r03mm22\Documents\Protocol_Testing\2024 Data Collection' + '\\' + subject_code
OMC_dir = parent_dir + r'\OMC'
if os.path.exists(OMC_dir) == False:
    os.mkdir(OMC_dir)
output_dir = OMC_dir + r'\OMC_trcs'
if os.path.exists(output_dir) == False:
    os.mkdir(output_dir)

# Iterate through the collection of movement types
for trial_name in trial_name_list:

    print(f'\nWriting {trial_name}_marker_pos.trc...')

    input_file_name = parent_dir + r'\RawData' + r'\\' + subject_code + '_' + trial_name + r' - Report1 - Marker_Traj.txt'
    output_file_name = output_dir + r'\\' + trial_name + '_marker_pos.trc'

    # Convert MM .txt file to .trc and save .trc file
    MM_2_trc(input_file_name, sample_rate, output_file_name)

    print(f'\nWritten {trial_name}_marker_pos.trc')


