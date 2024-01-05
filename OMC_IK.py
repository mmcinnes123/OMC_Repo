# This script performs marker-based IK with OpenSim API
# Input is a .trc file
# Output is a scaled osim model and an .mot file

import os
from OMC_IK_functions import *

""" SETTINGS """

# Quick Settings
trial_name = '20thDec'
parent_directory = r'C:\Users\r03mm22\Documents\Protocol_Testing\Tests\23_12_20\OMC'  # Path to working folder
static_pose_time = 5

# SCALE SETTINGS
scale_settings_template_file = 'OMC_Scale_Settings.xml' # See run_scale_model() for more settings

# IK SETTINGS
IK_settings_template_file = 'OMC_IK_Settings.xml'   # See run_OMC_IK() for more settings.


""" MAIN """

# Define some file paths
results_directory = os.path.join(parent_directory, trial_name + 'IK_Results')
path_to_trc_file = parent_directory.replace(r'\OMC', r'\BL_marker_pos.trc') # Define a path to the marker data
path_to_scaled_model = parent_directory + r'\das3_scaled_and_placed.osim'   # Define a path to the scaled model

# Create a new results directory
if os.path.exists(results_directory) == False:
    os.mkdir(results_directory)
osim.Logger.addFileSink(results_directory + r'\opensim.log')


# Scale the model
print("\nSet the static pose time in this script.")
scaling_confirmation = input("\nHappy to go ahead with Scaling?: ")
if scaling_confirmation == "No":
    quit()
run_scale_model(scale_settings_template_file, static_pose_time, trial_name, parent_directory, path_to_trc_file)


# Check we're happy to go ahead with IK
IK_confirmation = input("\nHappy to go ahead with IK?: ")
if IK_confirmation == "No":
    quit()


# Run the IK
IK_start_time = int(input("\nEnter IK start time:"))
IK_end_time = int(input("\nEnter IK end time:"))
run_OMC_IK(IK_settings_template_file, trial_name, IK_start_time, IK_end_time,
           results_directory, path_to_trc_file, path_to_scaled_model)



# Log the marker error
find_marker_error(trial_name, results_directory)

