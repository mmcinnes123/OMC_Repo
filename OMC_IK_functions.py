import opensim as osim
import math
import pandas as pd
import numpy as np
from scipy.signal import butter, filtfilt


# Function to write the data_out into a TRC file
def writeTRC(data, file):

    # Write header
    file.write("PathFileType\t4\t(X/Y/Z)\toutput.trc\n")
    file.write("DataRate\tCameraRate\tNumFrames\tNumMarkers\tUnits\tOrigDataRate\tOrigDataStartFrame\tOrigNumFrames\n")
    file.write("%d\t%d\t%d\t%d\t%s\t%d\t%d\t%d\n" % (data["DataRate"], data["CameraRate"], data["NumFrames"],
                                                     data["NumMarkers"], data["Units"], data["OrigDataRate"],
                                                     data["OrigDataStartFrame"], data["OrigNumFrames"]))

    # Write labels
    file.write("Frame#\tTime\t")
    for i, label in enumerate(data["Labels"]):
        if i != 0:
            file.write("\t")
        # file.write("\t\t%s" % (label))
        file.write("%s\t\t" % (label))
    file.write("\n")
    file.write("\t")
    for i in range(len(data["Labels"]*3)):
        file.write("\t%c%d" % (chr(ord('X')+(i%3)), math.ceil((i+1)/3)))
    file.write("\n")

    # Write data_out
    for i in range(len(data["Data"])):
        file.write("%d\t%f" % (i, data["Timestamps"][i]))
        for l in range(len(data["Data"][0])):
            file.write("\t%f" % data["Data"][i][l])

        file.write("\n")


def MM_2_trc(input_file_name, sample_rate, output_file_name):

    # Create new empty variables and dataframe
    marker_pos = []
    labelset = []
    data_out = {'DataRate': sample_rate,
            'CameraRate': sample_rate,
            'NumFrames': 1,
            'NumMarkers': 1,
            'Units': 'm',
            'OrigDataRate': sample_rate,
            'OrigDataStartFrame': 1,
            'OrigNumFrames': 1,
            'Labels': [],
            'Data': [],
            'Timestamps': []
                }

    # Read in MM .txt file
    print("\nReading in data...")
    dataset = pd.read_csv(input_file_name, delimiter="\t")

    # Remove any values above the cutoff, to account for unstable/large values produced by MM interpolation
    largest_value_in_dataset = dataset.max(numeric_only=True).max()
    cutoff = 10
    if largest_value_in_dataset > cutoff:
        print("\nLarge values encountered! Removing anything above " + str(cutoff) + "m from the following markers:")
    pd.set_option('display.max_rows', None)
    max_values = pd.DataFrame(dataset.max())
    for row in range(len(max_values)):
        if max_values.iloc[row, 0] > cutoff:
            print(max_values.head(len(max_values)).index.values[row])
    # Replace values above/below cutoff with Nan
    dataset.where(dataset <= cutoff, inplace=True)
    dataset.where(dataset >= -cutoff, inplace=True)

    # Fill NaN values with linear interpolation
    print("\nInterpolating any Nan values...")
    def interpolate_df(df):
        nan_count = df.isna().sum()
        pd.set_option('display.max_rows', None)
        print("Number of NaNs encountered:")
        print(nan_count)
        df = df.interpolate()
        # Deal with any nans at start
        df = df.interpolate(method='linear', limit=100, limit_direction='backward')
        return df
    dataset = interpolate_df(dataset)

    print("\nExtracting data from MM file... ")

    # Extract all the data and append to Data_out dataframe
    for index in range(dataset.shape[0]):
        test = []
        for counter in range(1,dataset.shape[1]-1):
            test.append(dataset.iloc[index][counter])
        marker_pos.append(test)

    for row in marker_pos:
        data_out['Data'].append(row)

    # Extract and edit marker label names
    for col in dataset.columns:
        labelset.append(str(col))
    # remove first and last item from list as they are not labels
    labelset = labelset[1:-1]
    # keep every third marker name (there are three for X, Y, Z)
    labelset = labelset[::3]
    # replace any spaces with underscores to be allowed in opensim
    converter = lambda x: x.replace(' ', '.')
    labelset = list(map(converter, labelset))
    # remove _X from every label
    converter_2 = lambda x: x.replace('_X', '')
    labelset = list(map(converter_2, labelset))

    # Create metadata for data_out dataframe
    num_markers = (len(data_out['Data'][0])) / 3
    num_frames = len(data_out['Data'])

    # Create new time column
    timestamps = list(np.arange(0, num_frames / sample_rate, 1 / sample_rate))

    # Add info into dataframe
    data_out['Timestamps'] = timestamps
    data_out['DataRate'] = sample_rate
    data_out['CameraRate'] = sample_rate
    data_out['OrigDataRate'] = sample_rate
    data_out['NumMarkers'] = num_markers
    data_out['NumFrames'] = num_frames
    data_out['OrigNumFrames'] = num_frames
    data_out['Labels'] = labelset

    # Check if the characters in strings are in ASCII, U+0-U+7F.
    def isascii(s):
        return len(s) == len(s.encode())

    # Write the data_out into new TRC file
    fullname = output_file_name
    outputfile = open(fullname, "w")
    writeTRC(data_out, outputfile)
    outputfile.close()

    print("\nWritten data to .trc file")



def run_OMC_IK(IK_settings_template_file, trial_name, start_time, end_time,
               results_directory, marker_file_name, scaled_model_file_name):

    # Instantiate an InverseKinematicsTool from template
    IK_tool = osim.InverseKinematicsTool(IK_settings_template_file)

    IK_tool.setName(trial_name)
    IK_tool.set_model_file(scaled_model_file_name)
    IK_tool.set_marker_file(marker_file_name)
    IK_tool.set_time_range(0, start_time)
    IK_tool.set_time_range(1, end_time)
    IK_tool.set_results_directory(results_directory)
    IK_tool.setOutputMotionFileName(results_directory + r'\OMC_IK_results.mot')
    IK_tool.set_report_marker_locations(False)
    IK_tool.set_report_errors(True)

    # Update the settings in a setup file
    IK_tool.printToXML(results_directory + r'\IK_Settings_' + trial_name + '.xml')

    # Run IK
    IK_tool.run()


def find_marker_error(trial_name, results_dir):

    marker_error_file = results_dir + "\\" + trial_name + "_ik_marker_errors.sto"
    error_table = osim.TimeSeriesTable(marker_error_file)
    RMSE_column = error_table.getDependentColumn("marker_error_RMS").to_numpy()
    average_RMSE = np.round(np.mean(RMSE_column), 4)

    # Save value to file
    message = "Average RMSE is: " + str(average_RMSE) + " m"
    f = open(results_dir + r"\Marker_RMSE.txt", "w")
    f.write(message)
    f.close()



def visualize(model_file_name):

    # Visualise the IK results
    model = osim.Model(model_file_name)
    table = osim.TimeSeriesTable('OMC_IK_results.mot')
    osim.VisualizerUtilities_showMotion(model, table)

    # viz = osim.VisualizerUtilities()
    # viz.showModel(model)


def run_scale_model(scale_settings_template_file, static_pose_time, trial_name, results_path, trc_file):

    # Set time range of the moment the subject performed the static pose
    time_range = osim.ArrayDouble()
    time_range.set(0, static_pose_time)
    time_range.set(1, static_pose_time + 0.1)

    # Initiate the scale tool
    scale_tool = osim.ScaleTool(scale_settings_template_file)   # Template file to work off
    scale_tool.getGenericModelMaker().setModelFileName('das3.osim') # Name of input model

    # Define settings for the scaling step
    model_scaler = scale_tool.getModelScaler()
    model_scaler.setApply(True)
    model_scaler.setMarkerFileName(trc_file) # Marker file used for scaling
    model_scaler.setTimeRange(time_range) # Time range of the static pose
    model_scaler.setOutputModelFileName(results_path + r'\das3_scaled_only.osim')   # Name of the scaled model (before marker adjustment)
    model_scaler.setOutputScaleFileName(results_path + r'\Scaling_Factors_' + trial_name + '.xml') #Outputs scaling factor results

    # Define settings for the marker adjustment step
    marker_placer = scale_tool.getMarkerPlacer()
    marker_placer.setApply(True)
    marker_placer.setTimeRange(time_range) # Time range of the static pose
    marker_placer.setMarkerFileName(trc_file) # Marker file used for scaling
    marker_placer.setOutputMotionFileName(results_path + r'\Static.mot')    # Saves the coordinates of the estimated static pose
    marker_placer.setOutputModelFileName(results_path + r'\das3_scaled_and_placed.osim')    # Name of the final scaled model
    # marker_placer.setMaxMarkerMovement(-1)    # Maximum amount of movement allowed in marker data when averaging

    # Save adjusted scale settings
    scale_tool.printToXML(results_path + r'\Scale_Settings_' + trial_name + '.xml')

    # Run the scale tool
    scale_tool.run()

def adjust_scale_settings(static_pose_time, scale_settings_file):

    static_pose_end_time = static_pose_time + 0.1

    range_time = osim.ArrayDouble()
    range_time.set(0, static_pose_time)
    range_time.set(1, static_pose_end_time)

    # Instantiate an ScalingTool from template
    scale_settings = osim.ScaleTool(scale_settings_file)

    model_scaler = scale_settings.getModelScaler()

    # set time range
    model_scaler.setTimeRange(range_time)

    # Don't know how to update Scale tool with new 'Model Scaler'
    scale_settings

    scale_settings.printToXML(scale_settings_file)



