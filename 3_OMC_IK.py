# This script performs marker-based IK with OpenSim API
# Input is a .trc file and a scaled osim model
# Output is an .mot file

from OMC_helpers import run_OMC_IK, find_marker_error
from constants import IK_settings_template_file

import os
import opensim as osim
from tkinter.filedialog import askopenfilename, askdirectory


""" SETTINGS """

# Quick Settings
subject_code_list = ['P5']
trial_name_list = ['CP', 'JA_Slow', 'JA_Fast', 'ROM', 'ADL']
trim_bool = False   # Whether to use the start and end times defined below (as a rule, set to False)
IK_start_time = 0
IK_end_time = 104


""" MAIN """

# Iterate through the collection of subjects and movement types

for subject_code in subject_code_list:

    # Define some file paths
    parent_dir = os.path.join(r'C:\Users\r03mm22\Documents\Protocol_Testing\2024 Data Collection', subject_code)
    OMC_dir = os.path.join(parent_dir, 'OMC')
    OMC_trs_dir = os.path.join(OMC_dir, 'OMC_trcs')
    path_to_scaled_model = os.path.join(OMC_dir, 'das3_scaled_and_placed.osim')  # Define a path to the scaled model

    for trial_name in trial_name_list:

        # Define some file paths
        path_to_trc_file = os.path.join(OMC_trs_dir, trial_name + r'_marker_pos.trc')     # Define a path to the marker data
        results_directory = os.path.join(OMC_dir, trial_name + '_IK_Results')       # Define a name for new IK results folder
        # Make the IK results directory if it doesn't already exist
        os.makedirs(results_directory, exist_ok=True)
        # Add a new opensim.log
        osim.Logger.addFileSink(results_directory + r'\IK.log')

        """ MAIN """

        # Run the IK
        run_OMC_IK(IK_settings_template_file, trim_bool, IK_start_time, IK_end_time,
                   results_directory, path_to_trc_file, path_to_scaled_model)

        # Log the marker error
        find_marker_error(results_directory)


""" TEST """

run_test = False
if run_test == True:

    # Settings
    trim_bool = True  # Whether to use the start and end times defined below (as a rule, set to False)
    IK_start_time = 0
    IK_end_time = 5
    path_to_trc_file = str(askopenfilename(title=' Choose the trc marker file used to drive the IK ... '))
    path_to_scaled_model = str(askopenfilename(title=' Choose the scaled model used for the IK ... '))
    results_directory = str(askdirectory(title=' Choose the folder where you want to save the IK results ... '))

    # Run the IK
    run_OMC_IK(IK_settings_template_file, trim_bool, IK_start_time, IK_end_time,
               results_directory, path_to_trc_file, path_to_scaled_model)

    # Log the marker error
    find_marker_error(results_directory)
