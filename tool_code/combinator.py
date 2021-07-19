import pandas as pd
from time import time
import shutil
import tool_code
from tool_code.post_combinator import post_combinator_main, convert_to_ustons
from tool_code.copy_paster import copy_paster
from tool_code.combinator_functions import read_and_combine_files, read_files_and_combine_scenarios
from tool_code.report_classes import ComplianceReport, CostsReport, EffectsReport, TechReport
from tool_code.emission_costs import calc_emission_costs
from tool_code.discounting import discount_values
from tool_code.new_effects import calc_new_fatality_metrics, calc_new_effects


def main(settings):
    """
    Note:
        This is the main module for the tool. What is run is controlled via the SetInputs class.

    Parameter:
        settings: The SetInputs class.

    Return:
        The reports as selected in the SetInputs class.

    """
    if settings.run_compliance_report:
        print('Working on compliance reports')
        combined_compliance_report = read_and_combine_files(settings, settings.compliance_report_name)
        combined_scenarios_report = read_files_and_combine_scenarios(settings, settings.compliance_report_name)
        combined_compliance_report = pd.concat([combined_compliance_report, combined_scenarios_report], axis=0, ignore_index=True)
        combined_compliance_report = combined_compliance_report.reset_index(drop=True)
        combined_compliance_report = ComplianceReport(combined_compliance_report).new_report(settings)
        combined_compliance_report = post_combinator_main(settings, combined_compliance_report, settings.compliance_report_name)
        combined_compliance_report.to_csv(settings.path_postproc_runs_runid_outputs / f'{settings.compliance_report_name}_{settings.filename_id}.csv', index=False)

    if settings.run_effects_summary_report:
        print('Working on effects summary reports')
        combined_effects_summary_report = read_and_combine_files(settings, settings.effects_summary_report_name)
        combined_scenarios_report = read_files_and_combine_scenarios(settings, settings.effects_summary_report_name)
        combined_effects_summary_report = pd.concat([combined_effects_summary_report, combined_scenarios_report], axis=0, ignore_index=True)
        combined_effects_summary_report = combined_effects_summary_report.reset_index(drop=True)
        combined_effects_summary_report = EffectsReport(combined_effects_summary_report).new_report(settings)
        combined_effects_summary_report = post_combinator_main(settings, combined_effects_summary_report, settings.effects_summary_report_name)
        combined_effects_summary_report = convert_to_ustons(settings, combined_effects_summary_report)
        # create df of CAP and GHG inventories for recalc of damages
        inventory_summary_id_cols = ['Scenario Name', 'Calendar Year', 'Reg-Class']
        cols = inventory_summary_id_cols + [col for col in combined_effects_summary_report.columns if '(t)' in col or '(mmt)' in col or '(ustons)' in col]
        inventory_summary = pd.DataFrame(combined_effects_summary_report.loc[combined_effects_summary_report['Fuel Type'] == 'TOTAL', :],
                                         columns=cols).reset_index(drop=True)
        # calc new fatality metrics
        combined_effects_summary_report = calc_new_fatality_metrics(combined_effects_summary_report)
        combined_effects_summary_report = calc_new_effects(settings, combined_effects_summary_report, inventory_summary_id_cols + ['Fuel Type'])
        combined_effects_summary_report.to_csv(settings.path_postproc_runs_runid_outputs / f'{settings.effects_summary_report_name}_{settings.filename_id}.csv', index=False)

    if settings.run_effects_report:
        print('Working on effects reports')
        combined_effects_report = read_and_combine_files(settings, settings.effects_report_name)
        combined_scenarios_report = read_files_and_combine_scenarios(settings, settings.effects_report_name)
        combined_effects_report = pd.concat([combined_effects_report, combined_scenarios_report], axis=0, ignore_index=True)
        combined_effects_report = combined_effects_report.reset_index(drop=True)
        combined_effects_report = EffectsReport(combined_effects_report).new_report(settings)
        combined_effects_report = post_combinator_main(settings, combined_effects_report, settings.effects_report_name)
        combined_effects_report = convert_to_ustons(settings, combined_effects_report)
        # create df of CAP and GHG inventories for recalc of damages
        inventory_id_cols = ['Scenario Name', 'Model Year', 'Age', 'Calendar Year', 'Reg-Class']
        cols = inventory_id_cols + [col for col in combined_effects_report.columns if '(t)' in col or '(mmt)' in col or '(ustons)' in col]
        inventory = pd.DataFrame(combined_effects_report.loc[combined_effects_report['Fuel Type'] == 'TOTAL', :], columns=cols).reset_index(drop=True)
        # calc new fatality metrics
        combined_effects_report = calc_new_fatality_metrics(combined_effects_report)
        combined_effects_report.to_csv(settings.path_postproc_runs_runid_outputs / f'{settings.effects_report_name}_{settings.filename_id}.csv', index=False)

    if settings.run_costs_summary_report:
        print('Working on costs summary reports')
        combined_costs_summary_report = read_and_combine_files(settings, settings.costs_summary_report_name)
        combined_scenarios_report = read_files_and_combine_scenarios(settings, settings.costs_summary_report_name)
        combined_costs_summary_report = pd.concat([combined_costs_summary_report, combined_scenarios_report], axis=0, ignore_index=True)
        combined_costs_summary_report = combined_costs_summary_report.reset_index(drop=True)
        combined_costs_summary_report, non_emission_costs_summary = CostsReport(combined_costs_summary_report).new_report(settings)
        combined_costs_summary_report = post_combinator_main(settings, combined_costs_summary_report, settings.costs_summary_report_name)
        # calc emission costs since they were removed in the CostsReport class
        new_emission_costs = calc_emission_costs(settings, inventory_summary, inventory_summary_id_cols)
        combined_costs_summary_report = new_emission_costs.merge(combined_costs_summary_report, on=inventory_summary_id_cols + ['Disc-Rate'], how='left')
        combined_costs_summary_report, present_values, annualized_report = discount_values(settings, combined_costs_summary_report, inventory_summary_id_cols, [0.03, 0.07], *non_emission_costs_summary)
        combined_costs_summary_report.to_csv(settings.path_postproc_runs_runid_outputs / f'{settings.costs_summary_report_name}_{settings.filename_id}.csv', index=False)
        present_values.to_csv(settings.path_postproc_runs_runid_outputs / f'{settings.costs_summary_report_name}_present-values_{settings.filename_id}.csv', index=False)
        annualized_report.to_csv(settings.path_postproc_runs_runid_outputs / f'{settings.costs_summary_report_name}_annualized-values_{settings.filename_id}.csv', index=False)

    if settings.run_costs_report:
        print('Working on costs reports')
        combined_costs_report = read_and_combine_files(settings, settings.costs_report_name)
        combined_scenarios_report = read_files_and_combine_scenarios(settings, settings.costs_report_name)
        combined_costs_report = pd.concat([combined_costs_report, combined_scenarios_report], axis=0, ignore_index=True)
        combined_costs_report = combined_costs_report.reset_index(drop=True)
        combined_costs_report, non_emission_costs = CostsReport(combined_costs_report).new_report(settings)
        combined_costs_report = post_combinator_main(settings, combined_costs_report, settings.costs_report_name)
        # calc emission costs since they were removed in the CostsReport class
        new_emission_costs = calc_emission_costs(settings, inventory, inventory_id_cols)
        combined_costs_report = new_emission_costs.merge(combined_costs_report, on=inventory_id_cols + ['Disc-Rate'], how='left')
        combined_costs_report, present_values, annualized_report = discount_values(settings, combined_costs_report, inventory_id_cols, [0.03, 0.07], *non_emission_costs)
        combined_costs_report.to_csv(settings.path_postproc_runs_runid_outputs / f'{settings.costs_report_name}_{settings.filename_id}.csv', index=False)
        present_values.to_csv(settings.path_postproc_runs_runid_outputs / f'{settings.costs_report_name}_present-values_{settings.filename_id}.csv', index=False)
        annualized_report.to_csv(settings.path_postproc_runs_runid_outputs / f'{settings.costs_report_name}_annualized-values_{settings.filename_id}.csv', index=False)

    if settings.run_tech_utilization_report:
        print('Working on tech utilization reports')
        tech_pens_report = read_and_combine_files(settings, settings.tech_pens_report_name)
        combined_scenarios_report = read_files_and_combine_scenarios(settings, settings.tech_pens_report_name)
        tech_pens_report = pd.concat([tech_pens_report, combined_scenarios_report], axis=0, ignore_index=True)
        tech_pens_report = tech_pens_report.reset_index(drop=True)

        # need sales from compliance report if running the tech pens report
        if settings.run_compliance_report:
            pass
        else:
            combined_compliance_report = read_and_combine_files(settings, settings.compliance_report_name)
            combined_scenarios_report = read_files_and_combine_scenarios(settings, settings.compliance_report_name)
            combined_compliance_report = pd.concat([combined_compliance_report, combined_scenarios_report], axis=0, ignore_index=True)
            combined_compliance_report = combined_compliance_report.reset_index(drop=True)
            combined_compliance_report = pd.DataFrame(combined_compliance_report.loc[combined_compliance_report['Model Year'] != 'TOTAL', :])
            combined_compliance_report = pd.DataFrame(combined_compliance_report.loc[combined_compliance_report['Manufacturer'] != 'TOTAL', :])
            combined_compliance_report['Model Year'] = combined_compliance_report['Model Year'].astype(int)
        cols = ['Scenario Name', 'Model Year', 'Manufacturer', 'Reg-Class', 'Sales']
        sales = combined_compliance_report[cols]

        tech_pens_report = TechReport(tech_pens_report).new_report(sales)
        tech_pens_report = post_combinator_main(settings, tech_pens_report, settings.tech_pens_report_name)
        tech_pens_report.to_csv(settings.path_postproc_runs_runid_outputs / f'{settings.tech_pens_report_name}_{settings.filename_id}.csv', index=False)

    # copy/paste the model run inputs/outputs so that everything is bundled togeter
    if settings.run_copy_paster:
        copy_paster(settings)

    # copy/paste code to run folder in a folder named code
    for file in settings.files_in_path_code:
        shutil.copy2(file, settings.path_postproc_runs_runid_code / file.name)

    end_time = time()
    elapsed_time = end_time - settings.start_time

    summary_log = pd.DataFrame(data={
        'Item': ['Version', 'Run folder', 'Start of run', 'Elapsed time', 'Run info'],
        'Results': [tool_code.__version__, settings.path_postproc_runs_runid, settings.time_of_postproc_run, elapsed_time, settings.run_details],
        'Units': ['', '', 'YYYYmmdd-HHMMSS', 'seconds', '']})
    summary_log.to_csv(settings.path_postproc_runs_runid / 'summary_log.csv', index=False)
    print(f'Results have been saved to {settings.path_postproc_runs_runid}')


if __name__ == '__main__':
    from tool_code.postproc_setup import SetInputs as settings
    main(settings)
