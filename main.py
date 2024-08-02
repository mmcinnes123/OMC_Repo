
from OMC_preprocess import run_preprocess
from OMC_scale_model import run_scale_model
from OMC_IK import run_OMC_IK


""" PREPROCESS """
preprocess = False
if preprocess:

    # Quick Settings
    subject_code_list = [f'P{str(i).zfill(3)}' for i in range(1, 21)]
    trial_name_list = ['CP', 'JA_Slow', 'JA_Fast', 'ROM', 'ADL']

    # Iterate through the collection of movement types
    for subject_code in subject_code_list:

        for trial_name in trial_name_list:

            run_preprocess(subject_code, trial_name, test=False)


""" SCALE MODEL """

scale_model = False
if scale_model:

    # Quick Settings
    subject_code_list = [f'P{str(i).zfill(3)}' for i in range(1, 21)]
    # A dict defining the time to use for OMC calibration (during CP trial at pose: Alt_asst)
    static_time_dict = {'P001': 30, 'P002': 29, 'P003': 23, 'P004': 21, 'P005': 36,
                        'P006': 38, 'P007': 44, 'P008': 38, 'P009': 41, 'P010': 28,
                        'P011': 38, 'P012': 40, 'P013': 20, 'P014': 34, 'P015': 32,
                        'P016': 40, 'P017': 25, 'P018': 32, 'P019': 21, 'P020': 26}
    # Alt option: use N_asst from CP trial
    # static_time_dict_N_pose = {'P1': 18, 'P2': 15, 'P3': 13, 'P4': 13, 'P5': 25,
    #                     'P6': 18, 'P7': 20, 'P8': 30, 'P9': 27}

    for subject_code in subject_code_list:

        run_scale_model(subject_code, static_time_dict, test=False)


""" RUN IK """

IK = False
if IK:

    # Quick Settings
    # subject_code_list = [f'P{str(i).zfill(3)}' for i in range(1, 21)]
    subject_code_list = ['P020']

    # Iterate through the collection of subjects and movement types
    for subject_code in subject_code_list:

        trial_name_list = ['CP', 'JA_Slow', 'JA_Fast', 'ROM', 'ADL']

        for trial_name in trial_name_list:

            run_OMC_IK(subject_code, trial_name, run_analysis=True, test=False)
