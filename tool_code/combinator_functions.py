import pandas as pd
from itertools import product


def check_scenario_name(df, scen_name):
    """
    Note:
        This function checks to ensure that all passed DataFrames have a consistent scenario 0.

    Parameters:
        df: A DataFrame which must have a column named "Scenario Name'.\n
        scen_name: The scenario name that should be included in the passed DataFrame as scenario 0.

    Return:
        The passed DataFrame if scen_name is present as scenario 0, an error if not.

    """
    if df['Scenario Name'][0] == scen_name:
        return
    else:
        return print(f'Error:  Scenario 0 Scenario Name should be "{scen_name}"')


def scrub_data(settings, df):
    """
    Note:
        This function scrubs some records from the passed DataFrame.

    Parameters:
        settings: The SetInputs class.\n
        df: The passed DataFrame.

    Return:
        The passed DataFrame after scrubbing base_scenario_name and some model_year "TOTAL" records.

    """
    df = pd.DataFrame(df.loc[df['Scenario Name'] != settings.base_scenario_name])
    df.drop(columns=['Scenario'], inplace=True)
    if df.columns.tolist().__contains__('Model Year'):
        df = pd.DataFrame(df.loc[df['Model Year'] != 'TOTAL', :])
        df['Model Year'] = df['Model Year'].astype(int)
    return df


def do_year_shift(input_df, years_to_shift):
    """

    Parameters:
        df: A DataFrame of the data contained in the report-csv file being read and combined.
        years_to_shift: An integer representing the number of years by which to shift the model output file's data for use in this tool.

    Returns:
        The passed DataFrame with year data shifted by years_to_shift years.

    """
    df = input_df.copy()
    try:
        df['Model Year'] = df['Model Year'] + years_to_shift
        try:
            df['Calendar Year'] = df['Calendar Year'] + years_to_shift
        except:
            pass

    except:
        try:
            df['Calendar Year'] = df['Calendar Year'] + years_to_shift
        except:
            pass
    return df


def convert_to_ustons(settings, df):
    """
    Note:
        CCEMS reports criteria pollutants in metric tons and converts to US tons when multiplying by $/ton. EPA prefers to report US tons.

    Parameters:
        settings: The SetInputs class.\n
        df: A DataFrame containing inventory values in metric tons for conversion to US tons.

    Returns:
        A DataFrame with criteria pollutant inventories expressed in US tons.

    """
    args = [arg for arg in df.columns if '(t)' in arg and 'CO2' not in arg and 'CH4' not in arg and 'N2O' not in arg]
    for arg in args:
        df[arg] = df[arg] * settings.uston_per_metricton
        df = df.rename(columns={arg: arg.split(' ')[0] + ' ' + arg.split(' ')[1] + ' (ustons)'})
    return df


def read_files_and_combine_scenarios(settings, report_name):
    """
    Parameters:
        settings: The SetInputs class.\n
        report_name: The name of the report(s) to read.

    Return:
        A DataFrame that combines the Framework and NonFramework OEM scenario results for all runs in the model_runs_path_dict.

    """
    return_df = pd.DataFrame()
    for model_runs, files_to_combine in settings.model_runs_path_dict.items():
        framework_oem_run = files_to_combine[0]
        nonframework_oem_run = files_to_combine[1]
        years_to_shift = files_to_combine[2]

        framework_oem_report = pd.read_csv(framework_oem_run / f'{report_name}.csv')
        check_scenario_name(framework_oem_report, settings.base_scenario_name)
        framework_oem_report = scrub_data(settings, framework_oem_report)
        framework_oem_scenario_names = [name for name in framework_oem_report['Scenario Name'].unique()]

        nonframework_oem_report = pd.read_csv(nonframework_oem_run / f'{report_name}.csv')
        check_scenario_name(nonframework_oem_report, settings.base_scenario_name)
        nonframework_oem_report = scrub_data(settings, nonframework_oem_report)
        nonframework_oem_scenario_names = [name for name in nonframework_oem_report['Scenario Name'].unique()]

        for framework_oem_scenario_name, nonframework_oem_scenario_name in product(framework_oem_scenario_names, nonframework_oem_scenario_names):
            framework = pd.DataFrame(framework_oem_report.loc[framework_oem_report['Scenario Name'] == framework_oem_scenario_name, :])
            nonframework = pd.DataFrame(nonframework_oem_report.loc[nonframework_oem_report['Scenario Name'] == nonframework_oem_scenario_name, :])
            scenario_df = pd.concat([framework, nonframework], axis=0, ignore_index=True)
            if framework_oem_scenario_name == nonframework_oem_scenario_name:
                scenario_name = framework_oem_scenario_name
            else:
                scenario_name = f'{framework_oem_scenario_name}_{nonframework_oem_scenario_name}'
            scenario_df['Scenario Name'] = scenario_name
            # apply year shift if applicable
            if years_to_shift:
                scenario_df = do_year_shift(scenario_df, years_to_shift)
            return_df = pd.concat([return_df, scenario_df], axis=0, ignore_index=True)

    return_df = return_df.reset_index(drop=True)

    return return_df


if __name__ == '__main__':
    print('This module does not run as a script.')
