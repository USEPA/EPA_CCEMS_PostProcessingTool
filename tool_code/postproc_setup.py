from pathlib import Path
from datetime import datetime
from time import time
import attr
import pandas as pd

import tool_code.combinator


@attr.s
class SetInputs:
    """
    The SetInputs class does just that. It also controls what files to read and combine, etc.

    Note: The base_scenario_name must be in each file read and combined in any way. However, since it's in each file, it will be removed so that combining things doesn't
    double count that scenario. In this tool, the total social costs and benefits are calculated relative to the base_social_scenario entered here in the SetInputs class.
    This allows for any two scenarios to be compared since results for both are calculated relative to a common scenario.

    """
    # set time of run
    time_of_postproc_run = datetime.now().strftime('%Y%m%d-%H%M%S')
    start_time = time()

    # set what to run
    run_primary_runs = True # do this OR sensitivities, but not both at the same time
    run_sensitivity_runs = False # do this OR the primary, but not both at the same time
    run_copy_paster = True
    run_compliance_report = True
    run_costs_summary_report = True
    run_costs_report = True
    run_effects_summary_report = True
    run_effects_report = True
    run_tech_utilization_report = True
    run_full_fleet_runs = True # this now includes safe, 2012frm, full fleet FW
    run_model_years = [year for year in range(2020, 2030)] # only used for the model year lifetime reports
    summary_start_year = 2020

    base_scenario_name = '1 Mpg Standards'
    base_social_name = '2020hold'

    # Note: The base_scenario_name must be in each file read and combined in any way. However, only 1 version of the base_scenario is needed in the output file(s) of this tool
    # The social costs & benefits summation requires the base_scenario_name if running either of the cost reports, it's necessary to include the analagous effects report.

    # create lists of runs for primary runs, sensitivities, etc.

    # primary runs
    if run_primary_runs:
        model_runs = ['Run0_SAFE_2012FRM',
                      'FOS_FW-OEMs_P_oc15_mult',
                      'FOS_NFW-OEMs_P_oc15_mult',
                      'FOS_FW-OEMs_NA',
                      'FOS_NFW-OEMs_NA',
                      'FW-OEMs_P_oc15_mult_YearShift',
                      'NFW-OEMs_P_oc15_mult_YearShift',
                      'FW-OEMs_NA_YearShift',
                      'NFW-OEMs_NA_YearShift',
                      ]
        # model_runs = ['Run0_Combined',
        #               'Run50_FW-OEMs_SAFE_HH-Pop',
        #               'Run51_NonFW-OEMs_SAFE_HH-Pop',
        #               'Run60_FW-OEMs_SAFE_HH-HistVMT',
        #               'Run61_NonFW-OEMs_SAFE_HH-HistVMT',
        #               'Run70_FW-OEMs_SAFE_HH-HistFleet',
        #               'Run71_NonFW-OEMs_SAFE_HH-HistFleet',
        #               'Run80_FW-OEMs_SAFE_Pop-HistVMT',
        #               'Run81_NonFW-OEMs_SAFE_Pop-HistVMT',
        #               'Run90_FW-OEMs_SAFE_Pop-HistFleet',
        #               'Run91_NonFW-OEMs_SAFE_Pop-HistFleet',
        #               'Run100_FW-OEMs_SAFE_HistVMT-HistFleet',
        #               'Run101_NonFW-OEMs_SAFE_HistVMT-HistFleet',
        #               'Run110_FW-OEMs_SAFE_HH-Pop-HistVMT',
        #               'Run111_NonFW-OEMs_SAFE_HH-Pop-HistVMT',
        #               'Run120_FW-OEMs_SAFE_HH-Pop-HistFleet',
        #               'Run121_NonFW-OEMs_SAFE_HH-Pop-HistFleet',
        #               'Run130_FW-OEMs_SAFE_HH-HistVMT-HistFleet',
        #               'Run131_NonFW-OEMs_SAFE_HH-HistVMT-HistFleet',
        #               'Run140_FW-OEMs_SAFE_Pop-HistVMT-HistFleet',
        #               'Run141_NonFW-OEMs_SAFE_Pop-HistVMT-HistFleet',
        #               'Run150_FW-OEMs_SAFE_HH-Pop-HistVMT-HistFleet',
        #               'Run151_NonFW-OEMs_SAFE_HH-Pop-HistVMT-HistFleet',
        #               'Run160_FW-OEMs_SAFE_HH-PopV2-HistVMT-HistFleet',
        #               'Run161_NonFW-OEMs_SAFE_HH-PopV2-HistVMT-HistFleet',
        #               'Run170_FW-OEMs_SAFE_HH-PopV3-HistVMT-HistFleet',
        #               'Run171_NonFW-OEMs_SAFE_HH-PopV3-HistVMT-HistFleet',
        #               ]
        # model_runs = ['Run0_Combined',
        #               'Run3_FW-OEMs_FW-to-Proposal',
        #               'Run4_NonFW-OEMs_SAFE-to-Proposal',
        #               'Run9_FW-OEMs_FW',
        #               'Run10_NonFW-OEMs_SAFE',
        #               ]
        # model_runs = ['Run0_SAFE_2012FRM',
        #               'Run1_FW27',
        #               'Run2_SAFE-to-Alts',
        #               'Run3_FW-OEMs_FW-to-Proposal',
        #               'Run4_NonFW-OEMs_SAFE-to-Proposal',
        #               'Run5_FW-OEMs_FW-to-Alt1',
        #               'Run6_NonFW-OEMs_SAFE-to-Alt1',
        #               'Run7_FW-OEMs_FW-to-Alt2',
        #               'Run8_NonFW-OEMs_SAFE-to-Alt2',
        #               'Run9_FW-OEMs_FW',
        #               'Run10_NonFW-OEMs_SAFE',
        #               ]
        model_runs_to_combine = None
        model_runs_of_full_fleet = [model_runs[0]]
        # the 3rd entry in each of the dict values is for year_shift, if needed
        model_runs_with_scenarios_to_combine = {'proposal': [model_runs[1], model_runs[2], None],
                                                'no-action': [model_runs[3], model_runs[4], None],
                                                'proposal_year-shift': [model_runs[5], model_runs[6], 3],
                                                'no-action_year-shift': [model_runs[7], model_runs[8], 3],
                                                }
        # model_runs_with_scenarios_to_combine = {'hh-pop': [model_runs[1], model_runs[2]],
        #                                         'hh-vmt': [model_runs[3], model_runs[4]],
        #                                         'hh-fleet': [model_runs[5], model_runs[6]],
        #                                         'pop-vmt': [model_runs[7], model_runs[8]],
        #                                         'pop-fleet': [model_runs[9], model_runs[10]],
        #                                         'vmt-fleet': [model_runs[11], model_runs[12]],
        #                                         'hh-pop-vmt': [model_runs[13], model_runs[14]],
        #                                         'hh-pop-fleet': [model_runs[15], model_runs[16]],
        #                                         'hh-vmt-fleet': [model_runs[17], model_runs[18]],
        #                                         'pop-vmt-fleet': [model_runs[19], model_runs[20]],
        #                                         'hh-pop-vmt-fleet': [model_runs[21], model_runs[22]],
        #                                         'hh-popV2-vmt-fleet': [model_runs[23], model_runs[24]],
        #                                         'hh-popV3-vmt-fleet': [model_runs[25], model_runs[26]],
        #                                         }

    # runs for sensitivities
    else:
        model_runs = ['Run0_2020hold',
                      'Run3_FW-OEMs_FW-to-Proposal_PriceElas0p4',
                      'Run4_NonFW-OEMs_SAFE-to-Proposal_PriceElas0p4',
                      'Run3_FW-OEMs_FW-to-Proposal_aeoH',
                      'Run4_NonFW-OEMs_SAFE-to-Proposal_aeoH',
                      'Run3_FW-OEMs_FW-to-Proposal_aeoL',
                      'Run4_NonFW-OEMs_SAFE-to-Proposal_aeoL',
                      'Run3_FW-OEMs_FW-to-Proposal_MassSafety5thPctile',
                      'Run4_NonFW-OEMs_SAFE-to-Proposal_MassSafety5thPctile',
                      'Run3_FW-OEMs_FW-to-Proposal_MassSafety95thPctile',
                      'Run4_NonFW-OEMs_SAFE-to-Proposal_MassSafety95thPctile',
                      'Run3_FW-OEMs_FW-to-Proposal_NoHCR2',
                      'Run4_NonFW-OEMs_SAFE-to-Proposal_NoHCR2',
                      'Run3_FW-OEMs_FW-to-Proposal_PerfectTrading',
                      'Run4_NonFW-OEMs_SAFE-to-Proposal_PerfectTrading',
                      'Run3_FW-OEMs_FW-to-Proposal_Rebound-05',
                      'Run4_NonFW-OEMs_SAFE-to-Proposal_Rebound-05',
                      'Run3_FW-OEMs_FW-to-Proposal_Rebound-15',
                      'Run4_NonFW-OEMs_SAFE-to-Proposal_Rebound-15',
                      'Run9_FW-OEMs_FW_PriceElas0p4',
                      'Run10_NonFW-OEMs_SAFE_PriceElas0p4',
                      'Run9_FW-OEMs_FW_aeoH',
                      'Run10_NonFW-OEMs_SAFE_aeoH',
                      'Run9_FW-OEMs_FW_aeoL',
                      'Run10_NonFW-OEMs_SAFE_aeoL',
                      'Run9_FW-OEMs_FW_MassSafety5thPctile',
                      'Run10_NonFW-OEMs_SAFE_MassSafety5thPctile',
                      'Run9_FW-OEMs_FW_MassSafety95thPctile',
                      'Run10_NonFW-OEMs_SAFE_MassSafety95thPctile',
                      'Run9_FW-OEMs_FW_NoHCR2',
                      'Run10_NonFW-OEMs_SAFE_NoHCR2',
                      'Run9_FW-OEMs_FW_PerfectTrading',
                      'Run10_NonFW-OEMs_SAFE_PerfectTrading',
                      'Run9_FW-OEMs_FW_Rebound-05',
                      'Run10_NonFW-OEMs_SAFE_Rebound-05',
                      'Run9_FW-OEMs_FW_Rebound-15',
                      'Run10_NonFW-OEMs_SAFE_Rebound-15',
                      ]
        model_runs_to_combine = {}
        model_runs_with_scenarios_to_combine = {'FWandSAFE-to-Proposal_PriceElas0p4': [model_runs[1], model_runs[2]],
                                                'FWandSAFE-to-Proposal_aeoH': [model_runs[3], model_runs[4]],
                                                'FWandSAFE-to-Proposal_aeoL': [model_runs[5], model_runs[6]],
                                                'FWandSAFE-to-Proposal_MassSafety5thPctile': [model_runs[7], model_runs[8]],
                                                'FWandSAFE-to-Proposal_MassSafety95thPctile': [model_runs[9], model_runs[10]],
                                                'FWandSAFE-to-Proposal_NoHCR2': [model_runs[11], model_runs[12]],
                                                'FWandSAFE-to-Proposal_PerfectTrading': [model_runs[13], model_runs[14]],
                                                'FWandSAFE-to-Proposal_Rebound-05': [model_runs[15], model_runs[16]],
                                                'FWandSAFE-to-Proposal_Rebound-15': [model_runs[17], model_runs[18]],
                                                'FWandSAFE_PriceElas0p4': [model_runs[19], model_runs[20]],
                                                'FWandSAFE_aeoH': [model_runs[21], model_runs[22]],
                                                'FWandSAFE_aeoL': [model_runs[23], model_runs[24]],
                                                'FWandSAFE_MassSafety5thPctile': [model_runs[25], model_runs[26]],
                                                'FWandSAFE_MassSafety95thPctile': [model_runs[27], model_runs[28]],
                                                'FWandSAFE_NoHCR2': [model_runs[29], model_runs[30]],
                                                'FWandSAFE_PerfectTrading': [model_runs[31], model_runs[32]],
                                                'FWandSAFE_Rebound-05': [model_runs[33], model_runs[34]],
                                                'FWandSAFE_Rebound-15': [model_runs[35], model_runs[36]],
                                                }
        model_runs_of_full_fleet = [model_runs[0]]

    run_id = input('Provide a run identifier for the output folder name (press return to use the default name)\n')
    run_folder_identifier = f'{time_of_postproc_run}_{run_id}' if run_id != '' else f'{time_of_postproc_run}'
    filename_id = f'{run_id}' if run_id != '' else f'{time_of_postproc_run}'

    run_details = input('Provide some summary details for the given run if desired. Press <ENTER> if not.\n')

    # set paths
    path_code = Path(__file__).parent
    path_postproc = path_code.parent
    path_project = path_postproc.parent
    path_postproc_runs = path_postproc / 'runs'
    path_postproc_runs.mkdir(exist_ok=True)
    path_postproc_runs_runid = path_postproc / 'runs' / f'{run_folder_identifier}'
    path_postproc_runs_runid.mkdir(exist_ok=False)
    path_postproc_runs_runid_outputs = path_postproc_runs_runid / 'postproc_outputs'
    path_postproc_runs_runid_outputs.mkdir(exist_ok=False)
    path_postproc_runs_runid_code = path_postproc_runs_runid / 'code'
    path_postproc_runs_runid_code.mkdir(exist_ok=False)
    path_inputs = path_postproc / 'inputs'

    # create generator of files in path_code
    files_in_path_code = (entry for entry in path_code.iterdir() if entry.is_file())

    if model_runs_of_full_fleet:
        path_no_combine = dict()
        for item, run in enumerate(model_runs_of_full_fleet):
            if run_primary_runs:
                # path_no_combine[item] = path_project / f'CAFE_model_runs_v2021/output/{model_runs_of_full_fleet[item]}/reports-csv'
                path_no_combine[item] = path_project / f'CAFE_model_runs/output/{model_runs_of_full_fleet[item]}/reports-csv'
            else:
                path_no_combine[item] = path_project / f'CAFE_model_runs/sensitivities/output/{model_runs_of_full_fleet[item]}/reports-csv'

    if model_runs_to_combine:
        model_runs_to_combine_path_dict = dict()
        for k, v in model_runs_to_combine.items():
            if run_primary_runs:
                model_runs_to_combine_path_dict[k] = [Path(path_project / f'CAFE_model_runs/output/{v[0]}/reports-csv'),
                                                      Path(path_project / f'CAFE_model_runs/output/{v[1]}/reports-csv')]
            else:
                model_runs_to_combine_path_dict[k] = [Path(path_project / f'CAFE_model_runs/sensitivities/output/{v[0]}/reports-csv'),
                                                      Path(path_project / f'CAFE_model_runs/sensitivities/output/{v[1]}/reports-csv')]

    if model_runs_with_scenarios_to_combine:
        model_runs_with_scenarios_to_combine_path_dict = dict()
        for k, v in model_runs_with_scenarios_to_combine.items():
            if run_primary_runs:
                model_runs_with_scenarios_to_combine_path_dict[k] = [Path(path_project / f'CAFE_model_runs/output/{v[0]}/reports-csv'),
                                                                     Path(path_project / f'CAFE_model_runs/output/{v[1]}/reports-csv'),
                                                                     v[2]]
            else:
                model_runs_with_scenarios_to_combine_path_dict[k] = [Path(path_project / f'CAFE_model_runs/sensitivities/output/{v[0]}/reports-csv'),
                                                                     Path(path_project / f'CAFE_model_runs/sensitivities/output/{v[1]}/reports-csv')]

    # set report names to read and combine
    compliance_report_name = 'compliance_report'
    costs_summary_report_name = 'annual_societal_costs_summary_report'
    costs_report_name = 'annual_societal_costs_report'
    effects_summary_report_name = 'annual_societal_effects_summary_report'
    effects_report_name = 'annual_societal_effects_report'
    tech_pens_report_name = 'technology_utilization_report'

    # lists for calcs in the compliance report
    args_to_sum = ['Sales', 'Jobs',
                   'AC Efficiency Cost', 'AC Leakage Cost', 'Off-Cycle Cost', 'Tech Cost', 'Reg-Cost',
                   'HEV Cost', 'Tax Credit', 'Consumer WTP', 'Tech Burden',
                   'Credits Earned', 'Credits Out', 'Credits In', 'CO-2 Credits Earned', 'CO-2 Credits Out', 'CO-2 Credits In',
                   ]
    args_to_sales_weight = ['Average CW', 'Average FP',
                            'Avg AC Efficiency Cost', 'Avg AC Leakage Cost', 'Avg Off-Cycle Cost', 'Avg Tech Cost', 'Avg Fines', 'Avg Reg-Cost',
                            'Avg HEV Cost', 'Avg Tax Credit', 'Avg Consumer WTP', 'Avg Tech Burden',
                            ]
    args_to_sales_vmt_weight = ['CO-2 Standard', 'CO-2 Rating', 'AC Efficiency', 'AC Leakage', 'Off-Cycle Credits']

    # lists of metrics to exclude
    effects_metrics_to_exclude = ['Admissions', 'Asthma', 'Attacks', 'Bronchitis',
                                  'Premature', 'Respiratory', 'Restricted', 'Work Loss',
                                  ]
    costs_metrics_to_exclude = ['Damage']

    # lists of social costs and benefits
    retail_fuel_expenditures = 'Retail Fuel Outlay'
    fuel_tax_revenues = 'Fuel Tax Revenue'
    social_cost_args = ['Tech Cost',
                        'Maint/Repair Cost',
                        'Congestion Costs',
                        'Noise Costs'
                        ]
    consumer_surplus_as_cost_args = ['Foregone Consumer Sales Surplus']

    fatality_costs = 'Fatality Costs'
    non_fatal_injury_costs = 'Non-Fatal Injury Costs'
    # property_damage_crash_costs = 'Property Damage Crash Costs'
    non_fatal_crash_costs = 'Non-Fatal Crash Costs'

    drive_value = 'Drive Value'
    refueling_time_cost = 'Refueling Time Cost'
    fatality_risk_value = 'Fatality Risk Value'
    non_fatal_crash_risk_value = 'Non-Fatal Crash Risk Value'
    # non_fatal_crash_risk_value = 'Non-Fatal Risk Value'
    petrol_market_externalities = 'Petroleum Market Externalities'
    social_criteria_benefit_args = ['Criteria_Costs_3.0', 'Criteria_Costs_7.0']
    social_scc_benefit_args = ['GHG_Costs_5.0', 'GHG_Costs_3.0', 'GHG_Costs_2.5', 'GHG_Costs_3.0_95']


    # read criteria and scc cost factors
    criteria_cost_factors = pd.read_csv(path_inputs / 'cost_factors-criteria.csv', index_col=0)
    criteria_cost_factors = criteria_cost_factors.to_dict('index')
    scc_cost_factors = pd.read_csv(path_inputs / 'cost_factors-scc.csv', index_col=0)
    scc_cost_factors = scc_cost_factors.to_dict('index')

    # for discounting
    costs_start = 'end-year' # end-year will discount the first year of values; start-year will not discount that first year
    discount_year = 2021 # 2021 will discount 2021 values if costs_start is set to end-year
    social_discount_rates = [0.03, 0.07]
    criteria_discount_rates = [0.03, 0.07]
    scc_discount_rates = [0.025, 0.03, 0.05]

    # set constants
    vmt_car = 195264
    vmt_truck = 225865
    kwh_per_gge = 0.031 # kWh per gallon gasoline equivalent
    gal_per_bbl = 42 # gallons per barrel of oil
    kwh_us_annual = 3_802_000_000_000 # 3802 terrawatt hours electricity consumption in US in 2020
    bbl_us_annual = 2_940_000_000 # 2.94 billion BBL oil consumption in US in 2020
    year_for_compares = 2020
    grams_per_uston = 907185
    grams_per_metricton = 1_000_000
    metricton_per_uston = grams_per_uston / grams_per_metricton
    uston_per_metricton = 1 / metricton_per_uston
    

if __name__ == '__main__':
    settings = SetInputs()
    tool_code.combinator.main(settings)
