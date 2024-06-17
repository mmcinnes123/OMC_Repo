# This script processes the raw marker data
# Input is a MM report .txt file
# Output is a .trc file

from OMC_helpers import MM_2_trc
from constants import sample_rate

from os.path import join
from os import makedirs
from tkinter.filedialog import askdirectory, askopenfilename


def run_preprocess(subject_code, trial_name, test):

    # Input settings manually if running single test
    if test:
        input_file = str(askopenfilename(title=' Choose the TMM txt report file containing marker position data ... '))
        output_file_dir = str(askdirectory(title=' Choose the folder where the .trc file will be saved ... '))
        output_file_name = input("Name of output file: (include .trc)")
        output_file = join(output_file_dir, output_file_name)
    else:

        # Define some file directories
        parent_dir = join(r'C:\Users\r03mm22\Documents\Protocol_Testing\2024 Data Collection', subject_code)
        OMC_dir = join(parent_dir, 'OMC')
        OMC_trcs_dir = join(OMC_dir, 'OMC_trcs')
        raw_data_dir = join(parent_dir, 'RawData')
        input_file = join(raw_data_dir, subject_code + '_' + trial_name + r' - Report1 - Marker_Traj.txt')
        output_file = join(OMC_trcs_dir, trial_name + '_marker_pos.trc')

        # Create folders if they don't already exist
        makedirs(OMC_dir, exist_ok=True)
        makedirs(OMC_trcs_dir, exist_ok=True)

    # Convert MM .txt file to .trc file
    print(f'\nWriting {trial_name}_marker_pos.trc...')
    MM_2_trc(input_file, sample_rate, output_file)
    print(f'\nWritten {trial_name}_marker_pos.trc')


if __name__ == '__main__':
    run_preprocess(subject_code=None, trial_name=None, test=True)


