# This script processes the raw marker data
# Input is a MM report .txt file
# Output is a .trc file

from OMC_IK_functions import *
import os

""" SETTINGS """
parent_dir = r'C:\Users\r03mm22\Documents\Protocol_Testing\2024 Data Collection\DataCollection2024\P2'   # Path to the parent directory
input_file_name = parent_dir + r'\RawData' + r'\P2_JA_Slow - Report1 - Marker_Traj.txt'
sample_rate = 100

# Create a new results directory
if os.path.exists(parent_dir + r'\OMC') == False:
    os.mkdir(parent_dir + r'\OMC')

# Convert MM .txt file to .trc and save .trc file
MM_2_trc(input_file_name, sample_rate, output_file_name=parent_dir + r'\OMC\BL_marker_pos.trc')

# Preview marker data and check time for static pose
print("\nPreview data .trc file. \n Set static pose time in OMC_IK script.")
