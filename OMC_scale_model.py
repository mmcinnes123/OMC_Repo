# This script performs marker-based IK with OpenSim API
# Input is a .trc file
# Output is a scaled osim model and an .mot file

import os
from OMC_IK_functions import *

""" SETTINGS """

# Quick Settings
subject_code = 'P1'
trc_for_scaling = r'CP_marker_pos.trc'  # The movement data used to scale the OMC model
time_in_trc_for_scaling = 18     # Preview the trc to check for good static time with neutral pose (use N_asst from CP)

# Define some file paths
parent_dir = r'C:\Users\r03mm22\Documents\Protocol_Testing\2024 Data Collection' + '\\' + subject_code
OMC_dir = parent_dir + r'\OMC'
path_to_trc_file = OMC_dir + r'\OMC_trcs' + '\\' + trc_for_scaling
trial_name = 'OMC'
osim.Logger.addFileSink(OMC_dir + r'\calibration.log')

# SCALE SETTINGS
scale_settings_template_file = 'OMC_Scale_Settings.xml'     # See run_scale_model() for more settings


""" MAIN """

# Check you've updated the static pose time in this script
print("\nSet the static pose time in this script.")
scaling_confirmation = input("\nHappy to go ahead with Scaling?: ")
if scaling_confirmation == "No":
    quit()

# Scale the model
run_scale_model(scale_settings_template_file, time_in_trc_for_scaling, trial_name, OMC_dir, path_to_trc_file)

