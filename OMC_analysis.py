# This script runs the OpenSim Analyse tool to extracts a .sto file with time-series body orientation data
# from the .mot IK results file
# Input is a .mot file and the model which was used for the IK
# Output is an .sto file called 'analyze_BodyKinematics_pos_global.sto' which contains the model bodies orientations in
# XYZ euler angles

from OMC_helpers import run_analyze_tool
from constants import analyze_settings_template_file, sample_rate

import opensim as osim
import os
from tkinter.filedialog import askopenfilename, askdirectory


""" SETTINGS """

# Quick Settings
subject_code_list = ['P4']
trial_name_list = ['CP', 'JA_Slow', 'JA_Fast', 'ROM', 'ADL']
trim_bool = False    # Option to use a smaller section by editing start and end time within the function (not tidy code)
start_time = 0
end_time = 100


""" MAIN """

# Iterate through the subjects and collection of movement types

for subject_code in subject_code_list:

    # Define some file paths
    parent_dir = os.path.join(r'C:\Users\r03mm22\Documents\Protocol_Testing\2024 Data Collection', subject_code)
    OMC_dir = os.path.join(parent_dir, 'OMC')
    model_file = os.path.join(OMC_dir, 'das3_scaled_and_placed.osim')  # Define a path to the scaled model
    model_file_for_analysis = model_file

    for trial_name in trial_name_list:

        # Specify where to get the IK results files and the newly create states file
        results_dir = os.path.join(OMC_dir, trial_name + '_IK_Results')
        coord_file_for_analysis = os.path.join(results_dir, 'OMC_IK_results.mot')
        states_file_path = os.path.join(results_dir, 'OMC_StatesReporter_states.sto')
        osim.Logger.addFileSink(results_dir + r'\analysis.log')

        # Set end time by checking length of data
        if trim_bool == False:
            if trial_name == 'ADL':     # Only run for the first 60s of the ADL trial
                start_time = 0
                end_time = 60
            else:
                coords_table = osim.TimeSeriesTable(coord_file_for_analysis)
                n_rows = coords_table.getNumRows()
                start_time = 0
                end_time = n_rows / sample_rate

        # Run the analyze tool to output the BodyKinematics.sto
        run_analyze_tool(analyze_settings_template_file, results_dir, model_file_for_analysis,
                         coord_file_for_analysis, start_time, end_time)


""" TEST """

run_test = False
if run_test == True:

    # Settings
    trim_bool = False
    start_time = 0
    end_time = 100
    model_file_for_analysis = str(askopenfilename(title=' Choose the OMC calibrated model file used in the anlaysis ... '))
    coord_file_for_analysis = str(askopenfilename(title=' Choose the .mot coords file used in the anlaysis ... '))
    results_dir = str(askdirectory(title=' Choose the folder where you want to save the analysis results ... '))

    # Set end time by checking length of data
    if trim_bool == False:
        coords_table = osim.TimeSeriesTable(coord_file_for_analysis)
        n_rows = coords_table.getNumRows()
        start_time = 0
        end_time = n_rows / sample_rate

    # Run the analyze tool to output the BodyKinematics.sto
    run_analyze_tool(analyze_settings_template_file, results_dir, model_file_for_analysis,
                     coord_file_for_analysis, start_time, end_time)