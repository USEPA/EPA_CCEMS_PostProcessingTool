import pandas as pd
from datetime import datetime
from time import time
import shutil
import tool_code
from tool_code.postproc_setup import SetPaths, RuntimeSettings, SetInputs
from tool_code.copy_paster import copy_paster
from tool_code.combinator_functions import read_files_and_combine_scenarios, convert_to_ustons
from tool_code.report_classes import ComplianceReport, CostsReport, EffectsReport, TechReport, VehiclesReport
from tool_code.emission_costs import calc_emission_costs
from tool_code.energy_security import calc_energy_security_costs
from tool_code.discounting import discount_values
from tool_code.new_effects import calc_new_fatality_metrics, calc_new_effects
from tool_code.off_cycle_costs import calc_new_tech_costs_in_cost_summary_report, calc_new_tech_costs_in_cost_report


def main():
    """
    Note:
        This is the main module for the tool. What reports are run is controlled via the runtime_settings.csv input file.

    Return:
        The reports as requested in the runtime_settings.csv input file.

    """
    runtime_settings = RuntimeSettings()
    set_paths = SetPaths()
    settings = SetInputs()

    time_of_postproc_run = datetime.now().strftime('%Y%m%d-%H%M%S')
    start_time = time()

    run_id, run_folder_identifier, filename_id, run_details = set_paths.get_run_identifiers(time_of_postproc_run)
    path_tool_runs_runid, path_tool_runs_runid_inputs, path_tool_runs_runid_outputs, path_tool_runs_runid_code = set_paths.set_results_folders(run_folder_identifier)

    if runtime_settings.run_compliance_report:
        print('Working on compliance reports')
        combined_compliance_report = read_files_and_combine_scenarios(settings, settings.compliance_report_name)
        combined_compliance_report = combined_compliance_report.reset_index(drop=True)
        combined_compliance_report = ComplianceReport(combined_compliance_report).new_report(settings)
        combined_compliance_report.to_csv(path_tool_runs_runid_outputs / f'{settings.compliance_report_name}_{filename_id}.csv', index=False)

    if runtime_settings.run_effects_summary_report:
        print('Working on effects summary reports')
        combined_effects_summary_report = read_files_and_combine_scenarios(settings, settings.effects_summary_report_name)
        combined_effects_summary_report = combined_effects_summary_report.reset_index(drop=True)
        combined_effects_summary_report = EffectsReport(combined_effects_summary_report).new_report(settings)
        combined_effects_summary_report = convert_to_ustons(settings, combined_effects_summary_report)
        # create df of CAP and GHG inventories for recalc of damages
        inventory_summary_id_cols = ['Scenario Name', 'Calendar Year', 'Reg-Class', 'Fuel Type']
        cols = inventory_summary_id_cols + [col for col in combined_effects_summary_report.columns if '(t)' in col or '(mmt)' in col or '(ustons)' in col]
        inventory_summary = pd.DataFrame(combined_effects_summary_report
                                         .loc[(combined_effects_summary_report['Fuel Type'] != 'TOTAL')
                                              & (combined_effects_summary_report['Reg-Class'] != 'TOTAL'), :],
                                         columns=cols).reset_index(drop=True)
        # calc new fatality metrics
        combined_effects_summary_report = calc_new_fatality_metrics(combined_effects_summary_report)
        combined_effects_summary_report = calc_new_effects(settings, combined_effects_summary_report, inventory_summary_id_cols)
        combined_effects_summary_report.to_csv(path_tool_runs_runid_outputs / f'{settings.effects_summary_report_name}_{filename_id}.csv', index=False)

    if runtime_settings.run_effects_report:
        print('Working on effects reports')
        combined_effects_report = read_files_and_combine_scenarios(settings, settings.effects_report_name)
        combined_effects_report = combined_effects_report.reset_index(drop=True)
        combined_effects_report = EffectsReport(combined_effects_report).new_report(settings)
        combined_effects_report = convert_to_ustons(settings, combined_effects_report)
        # create df of CAP and GHG inventories for recalc of damages
        inventory_id_cols = ['Scenario Name', 'Model Year', 'Age', 'Calendar Year', 'Reg-Class', 'Fuel Type']
        cols = inventory_id_cols + [col for col in combined_effects_report.columns if '(t)' in col or '(mmt)' in col or '(ustons)' in col]
        inventory = pd.DataFrame(combined_effects_report
                                 .loc[(combined_effects_report['Fuel Type'] != 'TOTAL')
                                      & (combined_effects_report['Reg-Class'] != 'TOTAL'), :],
                                 columns=cols).reset_index(drop=True)
        # calc new fatality metrics
        combined_effects_report = calc_new_fatality_metrics(combined_effects_report)
        combined_effects_report = calc_new_effects(settings, combined_effects_report, inventory_id_cols)
        combined_effects_report.to_csv(path_tool_runs_runid_outputs / f'{settings.effects_report_name}_{filename_id}.csv', index=False)

    if runtime_settings.run_costs_summary_report:
        print('Working on costs summary reports')
        combined_costs_summary_report = read_files_and_combine_scenarios(settings, settings.costs_summary_report_name)
        combined_costs_summary_report = combined_costs_summary_report.reset_index(drop=True)
        combined_costs_summary_report, non_emission_costs_summary = CostsReport(combined_costs_summary_report).new_report(settings)
        new_emission_costs = calc_emission_costs(settings, inventory_summary, combined_costs_summary_report, inventory_summary_id_cols)
        inventory_summary_id_cols_no_fuel = [arg for arg in inventory_summary_id_cols if 'Fuel' not in arg]  # cost reports do not have fuel type, but it was used to calc damages
        combined_costs_summary_report = new_emission_costs.merge(combined_costs_summary_report, on=inventory_summary_id_cols_no_fuel + ['Disc-Rate'], how='left')
        combined_costs_summary_report = calc_new_tech_costs_in_cost_summary_report(combined_costs_summary_report, combined_compliance_report)
        energy_security_costs = calc_energy_security_costs(settings, combined_effects_summary_report, combined_costs_summary_report, inventory_summary_id_cols)
        combined_costs_summary_report = combined_costs_summary_report.drop(columns='Petroleum Market Externalities') \
            .merge(energy_security_costs, on=inventory_summary_id_cols_no_fuel + ['Disc-Rate'], how='left')
        combined_costs_summary_report, present_values, annualized_report = discount_values(settings, combined_costs_summary_report, inventory_summary_id_cols_no_fuel,
                                                                                           [0.03, 0.07], *non_emission_costs_summary)
        combined_costs_summary_report.to_csv(path_tool_runs_runid_outputs / f'{settings.costs_summary_report_name}_{filename_id}.csv', index=False)
        present_values.to_csv(path_tool_runs_runid_outputs / f'{settings.costs_summary_report_name}_present-values_{filename_id}.csv', index=False)
        annualized_report.to_csv(path_tool_runs_runid_outputs / f'{settings.costs_summary_report_name}_annualized-values_{filename_id}.csv', index=False)

    if runtime_settings.run_costs_report:
        print('Working on costs reports')
        combined_costs_report = read_files_and_combine_scenarios(settings, settings.costs_report_name)
        combined_costs_report = combined_costs_report.reset_index(drop=True)
        combined_costs_report, non_emission_costs = CostsReport(combined_costs_report).new_report(settings)
        new_emission_costs = calc_emission_costs(settings, inventory, combined_costs_report, inventory_id_cols)
        inventory_id_cols_no_fuel = [arg for arg in inventory_id_cols if 'Fuel' not in arg]  # cost reports do not have fuel type, but it was used to calc damages
        combined_costs_report = new_emission_costs.merge(combined_costs_report, on=inventory_id_cols_no_fuel + ['Disc-Rate'], how='left')
        combined_costs_report = calc_new_tech_costs_in_cost_report(combined_costs_report, combined_compliance_report)
        energy_security_costs = calc_energy_security_costs(settings, combined_effects_report, combined_costs_report, inventory_id_cols)
        combined_costs_report = combined_costs_report.drop(columns='Petroleum Market Externalities') \
            .merge(energy_security_costs, on=inventory_id_cols_no_fuel + ['Disc-Rate'], how='left')
        combined_costs_report, present_values, annualized_report = discount_values(settings, combined_costs_report, inventory_id_cols_no_fuel,
                                                                                   [0.03, 0.07], *non_emission_costs)
        combined_costs_report.to_csv(path_tool_runs_runid_outputs / f'{settings.costs_report_name}_{filename_id}.csv', index=False)
        present_values.to_csv(path_tool_runs_runid_outputs / f'{settings.costs_report_name}_present-values_{filename_id}.csv', index=False)
        annualized_report.to_csv(path_tool_runs_runid_outputs / f'{settings.costs_report_name}_annualized-values_{filename_id}.csv', index=False)

    if runtime_settings.run_tech_utilization_report:
        print('Working on tech utilization reports')
        tech_pens_report = read_files_and_combine_scenarios(settings, settings.tech_pens_report_name)
        tech_pens_report = tech_pens_report.reset_index(drop=True)

        # need sales from compliance report if running the tech pens report
        if runtime_settings.run_compliance_report:
            pass
        else:
            combined_compliance_report = read_files_and_combine_scenarios(settings, settings.compliance_report_name)
            combined_compliance_report = combined_compliance_report.reset_index(drop=True)
            combined_compliance_report = pd.DataFrame(combined_compliance_report.loc[combined_compliance_report['Model Year'] != 'TOTAL', :])
            combined_compliance_report = pd.DataFrame(combined_compliance_report.loc[combined_compliance_report['Manufacturer'] != 'TOTAL', :])
            combined_compliance_report['Model Year'] = combined_compliance_report['Model Year'].astype(int)
        cols = ['Scenario Name', 'Model Year', 'Manufacturer', 'Reg-Class', 'Sales']
        sales = combined_compliance_report[cols]

        tech_pens_report = TechReport(tech_pens_report).new_report(settings, sales)
        tech_pens_report.to_csv(path_tool_runs_runid_outputs / f'{settings.tech_pens_report_name}_{filename_id}.csv', index=False)

    if runtime_settings.run_vehicles_report:
        print('Working on vehicles reports')
        combined_vehicles_report = read_files_and_combine_scenarios(settings, settings.vehicles_report_name)
        combined_vehicles_report = combined_vehicles_report.reset_index(drop=True)
        combined_vehicles_report = VehiclesReport(combined_vehicles_report).new_report(settings)
        combined_vehicles_report.to_csv(path_tool_runs_runid_outputs / f'{settings.vehicles_report_name}_{filename_id}.csv', index=False)

    # copy/paste the model run inputs/outputs so that everything is bundled together
    if runtime_settings.run_copy_paster:
        copy_paster(settings, set_paths, path_tool_runs_runid)

    # copy/paste code to run folder in a folder named code
    for file in set_paths.files_in_path_code:
        shutil.copy2(file, path_tool_runs_runid_code / file.name)

    # copy/paste tool inputs to run folder in a folder named inputs
    for file in set_paths.files_in_tool_inputs:
        shutil.copy2(file, path_tool_runs_runid_inputs / file.name)

    end_time = time()
    elapsed_time = end_time - start_time

    summary_log = pd.DataFrame(data={
        'Item': ['Version', 'Run folder', 'Start of run', 'Elapsed time', 'Run info'],
        'Results': [tool_code.__version__, path_tool_runs_runid, time_of_postproc_run, elapsed_time, run_details],
        'Units': ['', '', 'YYYYmmdd-HHMMSS', 'seconds', '']})
    summary_log.to_csv(path_tool_runs_runid / 'summary_log.csv', index=False)

    # add run to run_log
    df = summary_log[['Item', 'Results']].set_index('Item').transpose()
    try:
        run_log = pd.read_csv(set_paths.path_tool_runs / 'run_log.csv')
        run_log = pd.concat([run_log, df], axis=0, ignore_index=True)
    except:
        run_log = df.copy()
    run_log.to_csv(set_paths.path_tool_runs / 'run_log.csv', index=False)
    print(f'Results have been saved to {path_tool_runs_runid}')


if __name__ == '__main__':
    main()
