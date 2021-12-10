from pathlib import Path
import shutil


def copy_paster(settings, set_paths, path_tool_runs_runid):
    """
    Note:
        This functions does a direct copy/paste of model input and output files into the post-proc run results folder.

    Parameters:
        settings: The SetInputs class.
        set_paths: The SetPaths class.
        path_tool_runs_runid: The run_id.

    Return:
        Nothing is returned but files are copied and pasted.

    """
    print('Doing a copy/paste of model run inputs and outputs for this run ID.')
    # make a model runs folder within the postproc runs runid folder
    path_paste_model_runs = path_tool_runs_runid / 'CAFE_model_runs'
    path_paste_model_runs.mkdir(exist_ok=False)

    for k, v in settings.model_runs.items():
        for item in [0, 1]:
            if settings.run_folder_filename.__contains__('primary'):
                path_copy_input = set_paths.path_project / f'CAFE_model_runs/input/{settings.model_runs[k][item]}'
                path_copy_output = set_paths.path_project / f'CAFE_model_runs/output/{settings.model_runs[k][item]}/reports-csv'
            else:
                path_copy_input = set_paths.path_project / f'CAFE_model_runs/sensitivities/input/{settings.model_runs[k][item]}'
                path_copy_output = set_paths.path_project / f'CAFE_model_runs/sensitivities/output/{settings.model_runs[k][item]}/reports-csv'

            # create the subfolder paths we want
            path_paste_model_runs_folder = dict()
            for folder in ['input', 'output']:
                path_paste_model_runs_folder[folder] = path_paste_model_runs / folder
                path_paste_model_runs_folder[folder].mkdir(exist_ok=True)
                path_paste_model_runs_folder[folder] = path_paste_model_runs_folder[folder] / f'{settings.model_runs[k][item]}'
                path_paste_model_runs_folder[folder].mkdir(exist_ok=True)

            # create generator of files in copy paths
            files_in_path_copy_input = (entry for entry in path_copy_input.iterdir() if entry.is_file())
            files_in_path_copy_output = (entry for entry in path_copy_output.iterdir() if entry.is_file())

            # copy/paste input files
            for file in files_in_path_copy_input:
                shutil.copy2(file, path_paste_model_runs_folder['input'] / file.name)

            # copy/paste output files
            for file in files_in_path_copy_output:
                shutil.copy2(file, path_paste_model_runs_folder['output'] / file.name)

    return


if __name__ == '__main__':
    from postproc_setup import SetInputs as settings
    copy_paster(settings)
    print('Copy/Paste complete')
