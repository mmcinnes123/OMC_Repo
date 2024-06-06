# This script processes the raw marker data
# Input is a MM report .txt file
# Output is a .trc file

from OMC_helpers import MM_2_trc
from constants import sample_rate

import os

""" SETTINGS """

# Quick Settings
subject_code_list = ['P9']
trial_name_list = ['CP', 'JA_Slow', 'JA_Fast', 'ROM', 'ADL']
# trial_name_list = ['CP', 'JA_Slow', 'JA_Fast', 'ROM'] # Use for P6 and P7 where ADL data is missing


""" MAIN """

# Iterate through the collection of movement types
for subject_code in subject_code_list:
    for trial_name in trial_name_list:

        # Define some file directories
        parent_dir = os.path.join(r'C:\Users\r03mm22\Documents\Protocol_Testing\2024 Data Collection', subject_code)
        OMC_dir = os.path.join(parent_dir, 'OMC')
        OMC_trcs_dir = OMC_dir + r'\OMC_trcs'
        input_file_name = parent_dir + r'\RawData' + r'\\' + subject_code + '_' + trial_name + r' - Report1 - Marker_Traj.txt'
        output_file_name = OMC_trcs_dir + r'\\' + trial_name + '_marker_pos.trc'
        # Create folders if they don't already exist
        os.makedirs(OMC_dir, exist_ok=True)
        os.makedirs(OMC_trcs_dir, exist_ok=True)

        # Convert MM .txt file to .trc file
        print(f'\nWriting {trial_name}_marker_pos.trc...')
        MM_2_trc(input_file_name, sample_rate, output_file_name)
        print(f'\nWritten {trial_name}_marker_pos.trc')


