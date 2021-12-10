import pandas as pd


def calc_off_cycle_costs_in_compliance_report(settings, input_df):
    """
    Note:
        Note that the CCEMS compliance report includes in the 'Reg-Cost' and 'Avg Reg-Cost' fines paid by the manufacturer. EPA does not have a fine
        program. The calculation of 'Avg Reg-Cost' and, subsequently, the 'Reg-Cost' in this function eliminates those fines while also including off-cycle credit costs.

    Parameters:
        settings: The SetInputs class.
        input_df: A DataFrame reflecting the combined compliance report.

    Return:
         The combined compliance report DataFrame with Off-Cycle and Avg Off-Cycle costs added, Tech Cost, Avg Tech Cost, Reg-Cost and
         Avg Reg-Cost recalculated to include off-cycle costs.

    """
    calc_df = input_df.copy()

    calc_df['Avg Off-Cycle Cost'] = settings.off_cycle_cost_per_credit * calc_df['Off-Cycle Credits']

    calc_df['Avg Reg-Cost'] = calc_df['Avg AC Efficiency Cost'] \
                              + calc_df['Avg AC Leakage Cost'] \
                              + calc_df['Avg Off-Cycle Cost'] \
                              + calc_df['Avg Tech Cost']

    calc_df['Off-Cycle Cost'] = calc_df['Avg Off-Cycle Cost'] * calc_df['Sales']

    # recalc 'Tech Cost' since it is off in model output file (Avg Tech Cost * Sales does not equal Tech Cost)
    # We take 'Avg Tech Cost' as more accurate so use it as correct.
    calc_df['Tech Cost'] = calc_df['Avg Tech Cost'] * calc_df['Sales']

    calc_df['Reg-Cost'] = calc_df['Avg Reg-Cost'] * calc_df['Sales']

    return calc_df


def calc_new_tech_costs_in_cost_summary_report(input_df, compliance_report):
    """
    Note:
        This function adds off-cycle costs to the cost summary report results since off-cycle costs are not part of EPA's CCEMS runs.
        The Reg-Cost of the combined compliance report should already have been recalculated relative to the CCEMS value by removing any fines and including off-cycle costs.

    Parameters:
        input_df: A DataFrame reflecting the combined cost summary reports for the given tool run.
        compliance_report: A DataFrame reflecting the combined compliance reports for the given tool run.

    Return:
        The cost summary report with recalculated Tech Costs inclusive of off-cycle costs.

    """
    calc_df = input_df.copy()
    new_tech_costs = compliance_report.loc[compliance_report['Manufacturer'] == 'TOTAL',
                                           ['Scenario Name', 'Model Year', 'Reg-Class', 'Reg-Cost']]
    # convert to thousands for cost summary report
    new_tech_costs['Reg-Cost'] = new_tech_costs['Reg-Cost'] / 1000
    new_tech_costs.rename(columns={'Model Year': 'Calendar Year'}, inplace=True)

    calc_df.drop(columns='Tech Cost', inplace=True)
    calc_df = calc_df.merge(new_tech_costs, on=['Scenario Name', 'Calendar Year', 'Reg-Class'], how='left')
    calc_df.rename(columns={'Reg-Cost': 'Tech Cost'}, inplace=True)

    return calc_df


def calc_new_tech_costs_in_cost_report(input_df, compliance_report):
    """
    Note:
        This function adds off-cycle costs to the cost report results since off-cycle costs are not part of EPA's CCEMS runs.
        The Reg-Cost of the combined compliance report should already been been recalculated relative to the CCEMS value by removing any fines and including off-cycle costs.

    Parameters:
        input_df: A DataFrame reflecting the combined cost reports for the given tool run.
        compliance_report: A DataFrame reflecting the combined compliance reports for the given tool run.

    Return:
        The cost report with recalculated Tech Costs inclusive of off-cycle costs.

    """
    calc_df = input_df.copy()
    new_tech_costs = compliance_report.loc[compliance_report['Manufacturer'] == 'TOTAL',
                                           ['Scenario Name', 'Model Year', 'Reg-Class', 'Reg-Cost']]
    # convert to thousands for cost summary report
    new_tech_costs['Reg-Cost'] = new_tech_costs['Reg-Cost'] / 1000

    # add an Age column for merging (all compliance report costs are Age=0)
    new_tech_costs.insert(0, 'Age', 0)

    calc_df.drop(columns='Tech Cost', inplace=True)
    calc_df = calc_df.merge(new_tech_costs, on=['Scenario Name', 'Model Year', 'Age', 'Reg-Class'], how='left')
    calc_df.rename(columns={'Reg-Cost': 'Tech Cost'}, inplace=True)

    # now fill NaN with 0 since the merge above leaves NaN entries for Tech Cost where Age is > 0
    calc_df = calc_df.fillna(0)

    return calc_df
