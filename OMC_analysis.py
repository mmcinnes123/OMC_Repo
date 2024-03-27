# This script extracts some more info from the IK results .mot file
# By creating a 'states' file, the calibrated OMC model is match to each state and the time-varying orientation of
# each body can be extracted
# Input is a .mot file
# Output is a states .sto file and a .csv file with body orientations (quaternions)

import os
from OMC_IK_functions import *

""" SETTINGS """

# Quick Settings
subject_code = 'P1'
trial_name_list = ['CP', 'JA_Slow', 'JA_Fast', 'ROM', 'ADL']
sample_rate = 100
trim_bool = False    # Option to use a smaller section by editing start and end time within the function (not tidy code)

# Define some file paths
parent_dir = os.path.join(r'C:\Users\r03mm22\Documents\Protocol_Testing\2024 Data Collection', subject_code)
OMC_dir = os.path.join(parent_dir, 'OMC')
model_file = os.path.join(OMC_dir, 'das3_scaled_and_placed.osim')  # Define a path to the scaled model

# ANALYZE SETTINGS
analyze_settings_template_file = 'Analysis_Settings.xml'
model_file_for_analysis = model_file


# Iterate through the collection of movement types
for trial_name in trial_name_list:

    # Specify where to get the IK results files and the newly create states file
    results_dir = os.path.join(OMC_dir, trial_name + '_IK_Results')
    coord_file_for_analysis = os.path.join(results_dir, 'OMC_IK_results.mot')
    states_file_path = os.path.join(results_dir, 'OMC_StatesReporter_states.sto')
    osim.Logger.addFileSink(results_dir + r'\analysis.log')

    # Set end time by checking length of data
    if trim_bool == True:
        start_time = 0
        end_time = 100
    else:
        if trial_name == 'ADL':
            start_time = 0
            end_time = 60
        else:
            coords_table = osim.TimeSeriesTable(coord_file_for_analysis)
            n_rows = coords_table.getNumRows()
            start_time = 0
            end_time = n_rows / sample_rate

    # Create a states file to be used in comparisons with IMU data
    print(f'\nCreating {trial_name} states file from IK results mot file')
    create_states_file_from_coordinates_file(analyze_settings_template_file, model_file_for_analysis,
                                             coord_file_for_analysis, results_dir, start_time, end_time)

    # Read in new states, match the model to the states, extract the orientation of each body, then save to csv
    print(f'\nCreating {trial_name} body orientations csv file from states file')
    states_table = osim.TimeSeriesTable(states_file_path)
    extract_body_quats(states_table, model_file, results_dir, tag=trial_name + '_OMC')

