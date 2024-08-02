# This script performs marker-based IK with OpenSim API
# Input is a .trc file and a scaled OpenSim model
# Output is an .mot file

from OMC_helpers import run_osim_OMC_IK_tool, find_marker_error, run_analyze_tool
from constants import IK_settings_template_file, sample_rate, analyze_settings_template_file

from os import makedirs
from os.path import join
import opensim as osim
from tkinter.filedialog import askopenfilename, askdirectory


def run_OMC_IK(subject_code, trial_name, run_analysis, test):

    """ SETTINGS """

    # Input settings/files manually if running single test
    if test:
        results_directory = str(askdirectory(title=' Choose the folder where the IK results will be saved ... '))
        scaled_model = str(askopenfilename(title=' Choose the scaled .osim model to run the IK ... '))
        trc_file_path = str(askopenfilename(title=' Choose the .trc file to run the IK ... '))
        trim_bool_str = input('IK trim bool (True or False):')
        if trim_bool_str == 'True':
            trim_bool = True
            IK_start_time = input('Start time (s): ')
            IK_end_time = input('End time (s): ')
        else:
            trim_bool = False
            IK_start_time = None
            IK_end_time = None
    else:

        # Define some file paths
        parent_dir = join(r'C:\Users\r03mm22\Documents\Protocol_Testing\2024 Data Collection', subject_code)
        OMC_dir = join(parent_dir, 'OMC')
        OMC_trs_dir = join(OMC_dir, 'OMC_trcs')
        scaled_model = join(OMC_dir, 'das3_scaled_and_placed.osim')  # Define a path to the scaled model
        trc_file_path = join(OMC_trs_dir, trial_name + r'_marker_pos.trc')  # Define a path to the marker data
        results_directory = join(OMC_dir, trial_name + '_IK_Results')  # Define a name for new IK results folder

        # Make the IK results directory if it doesn't already exist
        makedirs(results_directory, exist_ok=True)
        # Add a new opensim.log
        osim.Logger.addFileSink(results_directory + r'\IK.log')

        # Don't trim the data if we're iterating through subjects
        trim_bool = False
        IK_start_time = None
        IK_end_time = None

    """ MAIN """

    # Run the IK
    run_osim_OMC_IK_tool(IK_settings_template_file, trim_bool, IK_start_time, IK_end_time, results_directory,
                         trc_file_path, scaled_model)

    # Log the marker error
    find_marker_error(results_directory)

    """ ANALYSIS """

    if run_analysis:

        # Specify where to get the IK results file
        coord_file_for_analysis = join(results_directory, 'OMC_IK_results.mot')
        osim.Logger.addFileSink(results_directory + r'\analysis.log')

        # Set end time by checking length of data
        if trim_bool == False:
            if trial_name == 'ADL':     # Only run for the first 60s of the ADL trial
                analysis_start_time = 0
                analysis_end_time = 60
            else:
                coords_table = osim.TimeSeriesTable(coord_file_for_analysis)
                n_rows = coords_table.getNumRows()
                analysis_start_time = 0
                analysis_end_time = n_rows / sample_rate
        else:
            analysis_start_time = IK_start_time
            analysis_end_time = IK_end_time

        # Run the analyze tool to output the BodyKinematics.sto
        run_analyze_tool(analyze_settings_template_file, results_directory, scaled_model,
                         coord_file_for_analysis, analysis_start_time, analysis_end_time)


""" TEST """

if __name__ == '__main__':
    run_OMC_IK(subject_code=None, trial_name=None, run_analysis=True, test=True)
