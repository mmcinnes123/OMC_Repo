# This script runs the scale tool in OpenSim, which simultaneously scales the model bodies and moves the model markers
# Input is the template model file and a trc file with marker data at a static pose time
# Output is a scaled model (without markers moved), a scaled model with markers moved, and a static pose .mot showing
# results of the single IK step

from OMC_helpers import run_scale_model
from constants import scale_settings_template_file, template_model

import os
import opensim as osim
from tkinter.filedialog import askdirectory, askopenfilename


""" SETTINGS """

# Quick Settings
subject_code = 'P9'
static_time_dict = {'P1': 18, 'P2': 15, 'P3': 13, 'P4': 13, 'P5': 25, 'P6': 18, 'P7': 20, 'P8': 30, 'P9': 27}     # Input the time during CP trial at pose: N_asst
time_in_trc_for_scaling = static_time_dict[subject_code]
trc_for_scaling = r'CP_marker_pos.trc'  # The movement data used to scale the OMC model


""" MAIN """

# Define some file paths
parent_dir = os.path.join(r'C:\Users\r03mm22\Documents\Protocol_Testing\2024 Data Collection', subject_code)
OMC_dir = os.path.join(parent_dir, 'OMC')
trc_file_path = os.path.join(OMC_dir, 'OMC_trcs', trc_for_scaling)
osim.Logger.addFileSink(OMC_dir + r'\calibration.log')

# Scale the model
run_scale_model(scale_settings_template_file, template_model, time_in_trc_for_scaling, trc_file_path, OMC_dir)


""" TEST """

run_test = False
if run_test:

    template_model = 'das3_with_carry_angleDOF.osim'
    subject_code = 'P7'
    static_time_dict = {'P1': 18, 'P2': 15, 'P3': 13, 'P4': 13, 'P5': 25, 'P6': 18,
                        'P7': 48}  # Input the time during CP trial at pose: N_asst
    time_in_trc_for_scaling = static_time_dict[subject_code]

    OMC_dir = str(askdirectory(title=' Choose the folder where you want to save the calibrated model ... '))

    run_scale_model(scale_settings_template_file, template_model, time_in_trc_for_scaling, trc_file_path, OMC_dir)
