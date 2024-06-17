# This script runs the scale tool in OpenSim, which simultaneously scales the model bodies and moves the model markers
# Input is the template model file and a trc file with marker data at a static pose time
# Output is a scaled model (without markers moved), a scaled model with markers moved, and a static pose .mot showing
# results of the single IK step

from OMC_helpers import run_osim_scale_tool
from constants import scale_settings_template_file, OMC_template_model

# import os
from os.path import join
import opensim as osim
from tkinter.filedialog import askdirectory, askopenfilename


""" SETTINGS """


def run_scale_model(subject_code, static_time_dict, test):

    # Input settings manually if running single test
    if test:
        template_model = str(askopenfilename(title=' Choose the .osim model file which is the template for scaling ... '))
        trc_file_path = str(askopenfilename(title=' Choose the .trc file used for the scale IK step (usually CP)... '))
        OMC_dir = str(askdirectory(title=' Choose the folder where the scaled model file will be saved ... '))
        time_in_trc_for_scaling = input('Enter the pose time from the trc file used for the IK step (s):')
    else:

        # Define some file paths
        parent_dir = join(r'C:\Users\r03mm22\Documents\Protocol_Testing\2024 Data Collection', subject_code)
        OMC_dir = join(parent_dir, 'OMC')
        trc_for_scaling = r'CP_marker_pos.trc'  # The movement data used to scale the OMC model
        trc_file_path = join(OMC_dir, 'OMC_trcs', trc_for_scaling)
        template_model = OMC_template_model

        if subject_code in static_time_dict.keys():
            time_in_trc_for_scaling = static_time_dict[subject_code]
        else:
            time_in_trc_for_scaling = None
            print('QUIT MESSAGE: You need to add the pose time to the static_time_dict for subject ', subject_code)
            quit()

    # Create a log file
    osim.Logger.addFileSink(OMC_dir + r'\calibration.log')

    # Scale the model
    run_osim_scale_tool(scale_settings_template_file, template_model, time_in_trc_for_scaling, trc_file_path, OMC_dir)


""" TEST """

if __name__ == '__main__':
    run_scale_model(subject_code=None, static_time_dict=None, test=True)
