# This script processes the raw marker data
# Input is a MM report .txt file
# Output is a .trc file

from OMC_IK_functions import *

""" SETTINGS """
raw_data_dir = r'C:\Users\r03mm22\Documents\Protocol_Testing\Tests\23_12_20\RawData'   # Path to the raw data files
input_file_name = raw_data_dir + r'\20thDec_Movements - Report1 - Marker_Traj.txt'
sample_rate = 100

# Convert MM .txt file to .trc and save .trc file
MM_2_trc(input_file_name, sample_rate, output_file_name=raw_data_dir.replace(r'\RawData', '') + r'\BL_marker_pos.trc')

# Preview marker data and check time for static pose
print("\nPreview data .trc file. \n Set static pose time in OMC_IK script.")
