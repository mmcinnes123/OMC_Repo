
from OMC_preprocess import run_preprocess
from OMC_scale_model import run_scale_model
from OMC_IK import run_OMC_IK


""" PREPROCESS """
preprocess = False
if preprocess:

    # Quick Settings
    subject_code_list = ['P9']
    trial_name_list = ['CP', 'JA_Slow', 'JA_Fast', 'ROM', 'ADL']

    # Iterate through the collection of movement types
    for subject_code in subject_code_list:

        # ADL data missing for P6 and P7
        if subject_code in ['P6', 'P7']:
            if 'ADL' in trial_name_list:
                trial_name_list.remove('ADL')

        for trial_name in trial_name_list:
            run_preprocess(subject_code, trial_name)


""" SCALE MODEL """

scale_model = False
if scale_model:

    # Quick Settings
    subject_code_list = ['P1', 'P2', 'P3', 'P4', 'P5', 'P6']
    static_time_dict_Altpose = {'P1': 25, 'P2': 22, 'P3': 23, 'P4': 21, 'P5': 36, 'P6': 36}     # Input the time during CP trial at pose: Alt_asst
    # static_time_dict_N_pose = {'P1': 18, 'P2': 15, 'P3': 13, 'P4': 13, 'P5': 25,
    #                     'P6': 18, 'P7': 20, 'P8': 30, 'P9': 27}     # Input the time during CP trial at pose: N_asst

    for subject_code in subject_code_list:
        run_scale_model(subject_code, static_time_dict_Altpose, test=False)


""" RUN IK """

IK = False
if IK:

    # Quick Settings
    subject_code_list = ['P1', 'P2', 'P3', 'P4', 'P5', 'P6']
    trial_name_list = ['CP', 'JA_Slow', 'JA_Fast', 'ROM', 'ADL']

    # Iterate through the collection of subjects and movement types
    for subject_code in subject_code_list:

        # ADL data missing for P6 and P7
        if subject_code in ['P6', 'P7']:
            if 'ADL' in trial_name_list:
                trial_name_list.remove('ADL')

        for trial_name in trial_name_list:
            run_OMC_IK(subject_code, trial_name, run_analysis=True, test=False)
