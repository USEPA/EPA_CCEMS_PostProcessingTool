import pandas as pd
from tool_code.combinator_functions import scrub_data
from tool_code.report_classes import TechReport


def data_to_use(settings, df, report_name):
    """
    Note:
        This function selects from the passed report only that data that was desired by EPA staff.

    Parameter:
        settings: The SetInputs class.\n
        df: A DataFrame consisting of the model output file to be revised.\n
        report_name: The name of that model output file.

    Return:
        The passed DataFrame with certain records removed depending on the report_name on which the DataFrame is based.

    """
    if df.columns.tolist().__contains__('Model Year'):
        if report_name != settings.compliance_report_name and report_name != settings.tech_pens_report_name:
            df = pd.DataFrame(df.loc[(df['Model Year'] >= settings.run_model_years[0]) &
                                     (df['Model Year'] <= settings.run_model_years[-1]), :])
            df = pd.DataFrame(df.loc[df['Model Year'] != 'TOTAL', :])
        if report_name == settings.compliance_report_name:
            df = pd.DataFrame(df.loc[(df['Reg-Class'] == 'Passenger Car')
                                     | (df['Reg-Class'] == 'Light Truck')
                                     | (df['Reg-Class'] == 'TOTAL'), :]).reset_index(drop=True)
            df = pd.DataFrame(df.loc[df['Model Year'] != 'TOTAL', :])
        if report_name == settings.tech_pens_report_name:
            df = pd.DataFrame(df.loc[(df['Reg-Class'] == 'Passenger Car')
                                     | (df['Reg-Class'] == 'Light Truck')
                                     | (df['Reg-Class'] == 'TOTAL'), :]).reset_index(drop=True)
    if report_name == settings.costs_summary_report_name or report_name == settings.costs_report_name:
        # eliminate discounted data since those are calculated in this tool
        df = pd.DataFrame(df.loc[df['Disc-Rate'] == 0, :])
        if df.columns.tolist().__contains__('Calendar Year'):
            df = df.loc[df['Calendar Year'] >= settings.summary_start_year, :]

    return df


def post_combinator_main(settings, report_df, report_name):
    """
    Note:
        This function is called to pull full fleet runs (those that do not require any sort of combining or re-sales weighting) into the DataFrame consisting
        of combined results.

    Parameters:
        settings: The SetInputs class.\n
        report_df: A DataFrame based on the model output "report_name" file.\n
        report_name: The name of that model output file.

    Return:
        A DataFrame with full fleet runs concatenated.

    """
    if settings.run_full_fleet_runs:
        result = pd.DataFrame()
        for item, path_to_report in settings.path_no_combine.items():
            report_at_path = pd.read_csv(path_to_report / f'{report_name}.csv')
            report_at_path = scrub_data(settings, report_at_path)
            report_at_path = data_to_use(settings, report_at_path, report_name)
            if report_name == settings.tech_pens_report_name:
                report_at_path = TechReport(report_at_path).sum_cols(report_at_path, 'BEV', 'PHEV')
            if report_df.empty:
                pass
            else:
                report_at_path = pd.DataFrame(report_at_path, columns=report_df.columns)
            result = pd.concat([result, report_at_path], axis=0, ignore_index=True)

        result = pd.concat([report_df, result], axis=0, ignore_index=True)

    if not settings.run_full_fleet_runs:
        result = report_df.copy()

    return result


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


if __name__ == '__main__':
    from postproc_setup import SetInputs as settings
    post_combinator_main(settings)
