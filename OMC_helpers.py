import opensim as osim
import math
import pandas as pd
import numpy as np
from scipy.spatial.transform import Rotation as R



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
    print("Reading in data...")
    dataset = pd.read_csv(input_file_name, delimiter="\t")

    # Remove any values above the cutoff, to account for unstable/large values produced by MM interpolation
    largest_value_in_dataset = dataset.max(numeric_only=True).max()
    cutoff = 10
    if largest_value_in_dataset > cutoff:
        print("Large values encountered (above " + str(cutoff) + "m) from the following markers:")
    pd.set_option('display.max_rows', None)
    max_values = pd.DataFrame(dataset.max())
    for row in range(len(max_values)):
        if max_values.iloc[row, 0] > cutoff:
            print(max_values.head(len(max_values)).index.values[row])
    # # Replace values above/below cutoff with Nan
    # dataset.where(dataset <= cutoff, inplace=True)
    # dataset.where(dataset >= -cutoff, inplace=True)

    # # Fill NaN values with linear interpolation
    # print("\nInterpolating any Nan values...")
    # def interpolate_df(df):
    #     nan_count = df.isna().sum()
    #     pd.set_option('display.max_rows', None)
    #     print("Number of NaNs encountered:")
    #     print(nan_count)
    #     df = df.interpolate()
    #     # Deal with any nans at start
    #     df = df.interpolate(method='linear', limit=100, limit_direction='backward')
    #     return df
    # dataset = interpolate_df(dataset)

    print("Extracting data from MM file... ")

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

    print("Written data to .trc file")



def run_OMC_IK(IK_settings_template_file, trial_name, trim_bool, start_time, end_time,
               results_directory, marker_file_name, scaled_model_file_name):

    # Instantiate an InverseKinematicsTool from template
    IK_tool = osim.InverseKinematicsTool(IK_settings_template_file)

    IK_tool.setName(trial_name)
    IK_tool.set_model_file(scaled_model_file_name)
    IK_tool.set_marker_file(marker_file_name)
    IK_tool.set_results_directory(results_directory)
    IK_tool.setOutputMotionFileName(results_directory + r'\OMC_IK_results.mot')
    IK_tool.set_report_marker_locations(False)
    IK_tool.set_report_errors(True)
    if trim_bool == True:
        IK_tool.set_time_range(0, start_time)
        IK_tool.set_time_range(1, end_time)

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
    time_range.set(1, static_pose_time + 0.01)

    # Initiate the scale tool
    scale_tool = osim.ScaleTool(scale_settings_template_file)   # Template file to work from
    scale_tool.getGenericModelMaker().setModelFileName('das3.osim') # Name of input model

    # Define settings for the scaling step
    model_scaler = scale_tool.getModelScaler()
    model_scaler.setApply(True)
    model_scaler.setMarkerFileName(trc_file) # Marker file used for scaling
    model_scaler.setTimeRange(time_range) # Time range of the static pose
    model_scaler.setOutputModelFileName(results_path + r'\das3_scaled_only.osim')   # Name of the scaled model (before marker adjustment)
    model_scaler.setOutputScaleFileName(results_path + r'\Scaling_Factors_' + trial_name + '.xml') # Outputs scaling factor results

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


def create_states_file_from_coordinates_file(analyze_settings_template_file, model_file, coord_file,
                                             results_path, start_time, end_time):

    # Instantiate a Analyze Tool
    analyze_tool = osim.AnalyzeTool(analyze_settings_template_file)
    analyze_tool.setModelFilename(model_file)
    analyze_tool.setResultsDir(results_path)
    analyze_tool.setCoordinatesFileName(coord_file)
    analyze_tool.setInitialTime(start_time)
    analyze_tool.setFinalTime(end_time)
    analyze_tool.setName("OMC")
    analyze_tool.run()



def run_analyze_tool(analyze_settings_template_file, results_dir, model_file_path, mot_file_path, start_time, end_time):

    analyze_Tool = osim.AnalyzeTool(analyze_settings_template_file)
    analyze_Tool.updAnalysisSet().cloneAndAppend(osim.BodyKinematics())
    analyze_Tool.setModelFilename(model_file_path)
    analyze_Tool.setName("analyze")
    analyze_Tool.setCoordinatesFileName(mot_file_path)
    analyze_Tool.setStartTime(start_time)
    analyze_Tool.setFinalTime(end_time)
    analyze_Tool.setResultsDir(results_dir)
    print('Running Analyze Tool...')
    analyze_Tool.run()
    print('Analyze Tool run finished.')


# Define a function for extracting body orientations from the states table
def extract_body_quats(states_table, model_file, results_dir, tag):

    # Create the model and the bodies
    model = osim.Model(model_file)
    thorax = model.getBodySet().get('thorax')
    humerus = model.getBodySet().get('humerus_r')
    radius = model.getBodySet().get('radius_r')

    # Unlock any locked coordinates in model
    for coord in ['TH_x','TH_y','TH_z','TH_x_trans','TH_y_trans','TH_z_trans',
                  'SC_x','SC_y','SC_z','AC_x','AC_y','AC_z','GH_y','GH_z','GH_yy','EL_x','PS_y']:
        model.getCoordinateSet().get(coord).set_locked(False)

    print("Getting states info from states file...")

    # Get the states info from the states file (this is the step which is computationally slow)
    stateTrajectory = osim.StatesTrajectory.createFromStatesTable(model, states_table)
    n_rows = stateTrajectory.getSize()
    print('Created stateTrajectory from states file.')

    # Initiate the system so that the model can actively realise positions based on states
    model.initSystem()

    def get_body_quat(state, body):
        Rot = body.getTransformInGround(state).R()
        quat = Rot.convertRotationToQuaternion()
        output_quat = np.array([quat.get(0), quat.get(1), quat.get(2), quat.get(3)])
        return output_quat

    # Get the orientation of each body of interest
    thorax_quats = np.zeros((n_rows, 4))
    humerus_quats = np.zeros((n_rows, 4))
    radius_quats = np.zeros((n_rows, 4))
    for row in range(n_rows):
        state = stateTrajectory.get(row)
        model.realizePosition(state)
        thorax_quats[row] = get_body_quat(state, thorax)
        humerus_quats[row] = get_body_quat(state, humerus)
        radius_quats[row] = get_body_quat(state, radius)

    # Write all body quats to a csv file
    thorax_quats_df = pd.DataFrame({"Thorax_Q0": thorax_quats[:,0],"Thorax_Q1": thorax_quats[:,1], "Thorax_Q2": thorax_quats[:,2], "Thorax_Q3": thorax_quats[:,3]})
    humerus_quats_df = pd.DataFrame({"Humerus_Q0": humerus_quats[:,0],"Humerus_Q1": humerus_quats[:,1], "Humerus_Q2": humerus_quats[:,2],"Humerus_Q3": humerus_quats[:,3]})
    radius_quats_df = pd.DataFrame({"Radius_Q0": radius_quats[:,0],"Radius_Q1": radius_quats[:,1], "Radius_Q2": radius_quats[:,2],"Radius_Q3": radius_quats[:,3]})
    time_df = pd.DataFrame({"Time": np.asarray(states_table.getIndependentColumn())[:]})

    all_quats_df = pd.concat([time_df, thorax_quats_df, humerus_quats_df, radius_quats_df], axis=1)

    print("Writing " + tag + " orientations file to csv...")

    all_quats_df.to_csv(results_dir + "\\" + tag + "_quats.csv", mode='w', encoding='utf-8', na_rep='nan')




