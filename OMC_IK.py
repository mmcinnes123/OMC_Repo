# This script performs marker-based IK with OpenSim API
# Input is a .trc file
# Output is a scaled osim model and an .mot file

import os
from OMC_IK_functions import *

""" SETTINGS """

# Quick Settings
subject_code = 'P1'
# trial_name_list = ['CP', 'JA_Slow', 'JA_Fast', 'ROM', 'ADL']
trial_name_list = ['JA_Slow']
trim_bool = True   # Whether to use the start and end times defined below
IK_start_time = 0
IK_end_time = 104

# Define some file paths
parent_dir = os.path.join(r'C:\Users\r03mm22\Documents\Protocol_Testing\2024 Data Collection', subject_code)
OMC_dir = os.path.join(parent_dir, 'OMC')
OMC_trs_dir = os.path.join(OMC_dir, 'OMC_trcs')
path_to_scaled_model = os.path.join(OMC_dir, 'das3_scaled_and_placed.osim')  # Define a path to the scaled model


# IK SETTINGS
IK_settings_template_file = 'OMC_IK_Settings.xml'   # See run_OMC_IK() for more settings.


# Iterate through the collection of movement types
for trial_name in trial_name_list:

    """ MAIN """

    path_to_trc_file = os.path.join(OMC_trs_dir, trial_name + r'_marker_pos.trc')     # Define a path to the marker data

    # Create a new results directory
    results_directory = os.path.join(OMC_dir, trial_name + '_IK_Results')       # Define a name for the new IK results folder
    if os.path.exists(results_directory) == False:
        os.mkdir(results_directory)
    osim.Logger.addFileSink(results_directory + r'\IK.log')


    # Run the IK
    run_OMC_IK(IK_settings_template_file, trial_name, trim_bool, IK_start_time, IK_end_time,
               results_directory, path_to_trc_file, path_to_scaled_model)


    # Log the marker error
    find_marker_error(trial_name, results_directory)



