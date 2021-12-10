import pandas as pd

from tool_code.off_cycle_costs import calc_off_cycle_costs_in_compliance_report


class ComplianceReport:
    """
    Note:
        This class controls the summation, sales weighting, etc., of framework OEM and non-framework OEM results into a single fleet for the compliance report.
        The costs in the CCEMS compliance report are absolute for the CCEMS baseline scenario (settings.base_scenario_name) and then incremental to that for other
        scenarios. It is important that the baseline scenario be consistent for all runs processed by this tool since that scenario is scrubbed out of the
        post-processed file. For incremental costs between, for example, the No Action and any Action scenario in the tool, the results will only be valid
        if the CCEMS incremental Action scenario costs are relative to the same baseline scenario.

    """

    def __init__(self, report_df):
        self.report_df = report_df

    def new_report(self, settings):
        df = self.report_df.copy().fillna(0)
        id_args = ['Scenario Name', 'Model Year']
        merge_cols = ['Scenario Name', 'Model Year', 'Manufacturer', 'Reg-Class']

        # eliminate some total rows since those need re-calc (drop model year total row since unnecessary)
        df = pd.DataFrame(df.loc[df['Model Year'] != 'TOTAL', :])
        df = pd.DataFrame(df.loc[df['Model Year'] >= settings.summary_start_year, :])
        df = pd.DataFrame(df.loc[df['Manufacturer'] != 'TOTAL', :])
        df['Model Year'] = df['Model Year'].astype(int)

        # calc CO2_2cycle from CAFE 2-cycle
        df.insert(df.columns.get_loc('CO-2 Rating') + 1, 'CO-2 2cycle', 8887 / df['CAFE (2-cycle)'])
        df.insert(df.columns.get_loc('CO-2 Rating') + 2, 'CO-2 Credit Use',
                  df['CO-2 2cycle'] - df['CO-2 Rating'] - df['AC Efficiency'] - df['AC Leakage'] - df['Off-Cycle Credits'])

        # limit reg class to pass car and light truck and TOTAL (reg class TOTAL is specific to mfr so doesn't need recalc)
        df = pd.DataFrame(df.loc[(df['Reg-Class'] == 'Passenger Car') | (df['Reg-Class'] == 'Light Truck') | (df['Reg-Class'] == 'TOTAL'), :]).reset_index(drop=True)

        df_sum = pd.DataFrame(df, columns=id_args + ['Manufacturer', 'Reg-Class'] + settings.args_to_sum).reset_index(drop=True)
        df_sales_weight = pd.DataFrame(df, columns=id_args + ['Manufacturer', 'Reg-Class', 'Sales'] + settings.args_to_sales_weight).reset_index(drop=True)
        df_sales_vmt_weight = pd.DataFrame(df, columns=id_args + ['Manufacturer', 'Reg-Class', 'Sales'] + settings.args_to_sales_vmt_weight).reset_index(drop=True)

        # work on sums
        df_sum_regclass_totals = df_sum.groupby(by=id_args + ['Reg-Class'], as_index=False).sum()
        df_sum_regclass_totals.insert(df_sum_regclass_totals.columns.get_loc('Reg-Class'), 'Manufacturer', 'TOTAL')
        df_sum = pd.concat([df_sum, df_sum_regclass_totals], axis=0, ignore_index=True)
        df_sum = df_sum.reset_index(drop=True)

        # work on sales weighted averages
        for arg in settings.args_to_sales_weight:
            df_sales_weight.insert(len(df_sales_weight.columns), f'{arg}*Sales', df_sales_weight[arg] * df_sales_weight['Sales'])
        df_sales_weight_regclass_totals = df_sales_weight.groupby(by=id_args + ['Reg-Class'], as_index=False).sum()
        df_sales_weight_regclass_totals.insert(df_sales_weight_regclass_totals.columns.get_loc('Reg-Class'), 'Manufacturer', 'TOTAL')
        df_sales_weight = pd.concat([df_sales_weight, df_sales_weight_regclass_totals], axis=0, ignore_index=True)
        df_sales_weight = df_sales_weight.reset_index(drop=True)
        for arg in settings.args_to_sales_weight:
            df_sales_weight[arg] = df_sales_weight[f'{arg}*Sales'] / df_sales_weight['Sales']
            df_sales_weight.drop(columns=f'{arg}*Sales', inplace=True)
        df_sales_weight.drop(columns='Sales', inplace=True)

        # work on sales & vmt weighted averages
        df_sales_vmt_weight.insert(len(df_sales_vmt_weight.columns), 'Sales*VMT', 0)
        for arg in settings.args_to_sales_vmt_weight:
            df_sales_vmt_weight.insert(len(df_sales_vmt_weight.columns), f'{arg}*Sales*VMT', 0)
            df_sales_vmt_weight.loc[df_sales_vmt_weight['Reg-Class'] != 'Light Truck', f'{arg}*Sales*VMT'] \
                = df_sales_vmt_weight[arg] * df_sales_vmt_weight['Sales'] * settings.vmt_car
            df_sales_vmt_weight.loc[df_sales_vmt_weight['Reg-Class'] == 'Light Truck', f'{arg}*Sales*VMT'] \
                = df_sales_vmt_weight[arg] * df_sales_vmt_weight['Sales'] * settings.vmt_truck
            df_sales_vmt_weight.loc[df_sales_vmt_weight['Reg-Class'] != 'Light Truck', 'Sales*VMT'] \
                = df_sales_vmt_weight['Sales'] * settings.vmt_car
            df_sales_vmt_weight.loc[df_sales_vmt_weight['Reg-Class'] == 'Light Truck', 'Sales*VMT'] \
                = df_sales_vmt_weight['Sales'] * settings.vmt_truck
        df_sales_vmt_weight_regclass_totals = df_sales_vmt_weight.groupby(by=id_args + ['Reg-Class'], as_index=False).sum()
        df_sales_vmt_weight_regclass_totals.insert(df_sales_vmt_weight_regclass_totals.columns.get_loc('Reg-Class'), 'Manufacturer', 'TOTAL')
        df_sales_vmt_weight = pd.concat([df_sales_vmt_weight, df_sales_vmt_weight_regclass_totals], axis=0, ignore_index=True)
        df_sales_vmt_weight = df_sales_vmt_weight.reset_index(drop=True)
        for arg in settings.args_to_sales_vmt_weight:
            df_sales_vmt_weight[arg] = df_sales_vmt_weight[f'{arg}*Sales*VMT'] / df_sales_vmt_weight['Sales*VMT']
            df_sales_vmt_weight.drop(columns=f'{arg}*Sales*VMT', inplace=True)
        df_sales_vmt_weight.drop(columns='Sales*VMT', inplace=True)
        df_sales_vmt_weight.drop(columns='Sales', inplace=True)

        df = df_sum.merge(df_sales_weight, on=merge_cols, how='left').merge(df_sales_vmt_weight, on=merge_cols, how='left')

        # calc off-cycle credits and adjust impacted attributes
        df = calc_off_cycle_costs_in_compliance_report(settings, df)

        return df


class CostsReport:
    """
    Note:
        This class controls the summation, sales weighting, etc., of framework OEM and non-framework OEM results into a single fleet for the cost report.

    """

    def __init__(self, report_df):
        self.report_df = report_df

    def new_report(self, settings):
        if self.report_df.columns.tolist().__contains__('Age'):
            df = self.report_df.copy().fillna(0)
            id_args = ['Scenario Name', 'Model Year', 'Age', 'Calendar Year', 'Disc-Rate']
        else:
            df = self.report_df.copy()
            id_args = ['Scenario Name', 'Calendar Year', 'Disc-Rate']

        # eliminate total rows since those need re-calc
        df = pd.DataFrame(df.loc[df['Reg-Class'] != 'TOTAL', :]).reset_index(drop=True)
        if id_args.__contains__('Calendar Year'):
            df = pd.DataFrame(df.loc[df['Calendar Year'] >= settings.summary_start_year, :])

        # limit full report to desired model years
        if id_args.__contains__('Model Year'):
            df = pd.DataFrame(df.loc[(df['Model Year'] >= settings.run_model_years[0]) &
                                     (df['Model Year'] <= settings.run_model_years[-1]), :])

        # eliminate damage data since those are calculated in this tool
        exclude_cols = list()
        for arg in settings.costs_metrics_to_exclude:
            # arg_list = [col for col in df.columns if arg in col]
            arg_list = [col for col in df.columns if arg in col and 'Property' not in col]
            exclude_cols = exclude_cols + arg_list
        df.drop(columns=exclude_cols, inplace=True)

        # eliminate discounted data since those are calculated in this tool
        df = pd.DataFrame(df.loc[df['Disc-Rate'] == 0, :])

        # eliminate total cost data since those are calculated in this tool
        df.drop(columns=['Total Social Costs', 'Total Social Benefits', 'Net Social Benefits'], inplace=True)

        # groupby id args along with args for which we want new totals (this combines into one fleet)
        df = df.groupby(by=id_args + ['Reg-Class'], as_index=False).sum()

        # groupby id args to get new calendar year (& age) totals
        total = df.groupby(by=id_args, as_index=False).sum()
        total.insert(df.columns.get_loc('Calendar Year'), 'Reg-Class', 'TOTAL')

        # bring everything together and return the new combined report
        df = pd.concat([df, total], axis=0, ignore_index=True)

        # determine the non-emission cost metrics
        non_emission_costs = [arg for arg in df.columns if arg not in id_args + ['Reg-Class']]

        return df, non_emission_costs


class EffectsReport:
    """
    Note:
        This class controls the summation, sales weighting, etc., of framework OEM and non-framework OEM results into a single fleet for the effects report.
        Some data reported by CCEMS are excluded from the effects reports of this tool. The data to exclude are set in the SetInputs class and include metrics
        having keywords such as 'Admissions', 'Asthma', 'Attacks', 'Bronchitis', 'Premature', 'Respiratory', 'Restricted', 'Work Loss'.

    """

    def __init__(self, report_df):
        self.report_df = report_df

    def new_report(self, settings):
        if self.report_df.columns.tolist().__contains__('Average Age'):
            df = self.report_df.copy().fillna(0)
            # Fleet weight the Average Age arg
            df.insert(len(df.columns), 'Fleet*AverageAge', df[['Fleet', 'Average Age']].product(axis=1))
            id_args = ['Scenario Name', 'Calendar Year']
        else:
            df = self.report_df.copy()
            id_args = ['Scenario Name', 'Model Year', 'Age', 'Calendar Year']

        # eliminate total rows since those need re-calc
        df = pd.DataFrame(df.loc[df['Reg-Class'] != 'TOTAL', :]).reset_index(drop=True)
        df = pd.DataFrame(df.loc[df['Fuel Type'] != 'TOTAL', :]).reset_index(drop=True)
        if id_args.__contains__('Calendar Year'):
            df = pd.DataFrame(df.loc[df['Calendar Year'] >= settings.summary_start_year, :])

        # limit full report to desired model years
        if id_args.__contains__('Model Year'):
            df = pd.DataFrame(df.loc[(df['Model Year'] >= settings.run_model_years[0]) &
                                     (df['Model Year'] <= settings.run_model_years[-1]), :])

        # eliminate incidence data
        exclude_cols = list()
        for arg in settings.effects_metrics_to_exclude:
            arg_list = [col for col in df.columns if arg in col]
            exclude_cols = exclude_cols + arg_list
        df.drop(columns=exclude_cols, inplace=True)

        # groupby id args along with args for which we want new totals (this combines into one fleet)
        df = df.groupby(by=id_args + ['Reg-Class', 'Fuel Type'], as_index=False).sum()

        # groupby reg class to get new reg class totals
        regclass_totals = df.groupby(by=id_args + ['Reg-Class'], as_index=False).sum()
        regclass_totals.insert(regclass_totals.columns.get_loc('Reg-Class') + 1, 'Fuel Type', 'TOTAL')

        # groupby fuel type to get new fuel type totals, but only in the full report, not the summary report
        if df.columns.tolist().__contains__('Average Age'):
            pass
        else:
            fueltype_totals = df.groupby(by=id_args + ['Fuel Type'], as_index=False).sum()
            fueltype_totals.insert(fueltype_totals.columns.get_loc('Fuel Type'), 'Reg-Class', 'TOTAL')

        # groupby to get new calendar year (& age) totals
        total_total = df.groupby(by=id_args, as_index=False).sum()
        total_total.insert(df.columns.get_loc('Calendar Year'), 'Fuel Type', 'TOTAL')
        total_total.insert(df.columns.get_loc('Calendar Year'), 'Reg-Class', 'TOTAL')

        # bring everything together
        if self.report_df.columns.tolist().__contains__('Average Age'):
            df = pd.concat([df, regclass_totals, total_total], axis=0, ignore_index=True)
            # recalc the average age if appropriate
            df['Average Age'] = df['Fleet*AverageAge'] / df['Fleet']
            df.drop(columns='Fleet*AverageAge', inplace=True)
        else:
            # bring everything together
            df = pd.concat([df, fueltype_totals, regclass_totals, total_total], axis=0, ignore_index=True)

        return df


class TechReport:
    """
    Note:
        This class controls the summation, sales weighting, etc., of framework OEM and non-framework OEM results into a single fleet for the technology
        utilization report.

    """

    def __init__(self, report_df):
        self.report_df = report_df

    def new_report(self, settings, sales_df):
        df = self.report_df.copy()
        id_args = ['Scenario Name', 'Model Year']
        param_type_loc = df.columns.get_loc('Param Type')
        args = [arg for arg in df.columns[param_type_loc + 1:].tolist()]

        # eliminate total rows that need re-calc and eliminate domestic/import rows since not needed
        df = pd.DataFrame(df.loc[df['Manufacturer'] != 'TOTAL', :]).reset_index(drop=True)
        df = pd.DataFrame(df.loc[(df['Reg-Class'] == 'Passenger Car') | (df['Reg-Class'] == 'Light Truck') | (df['Reg-Class'] == 'TOTAL'), :]).reset_index(drop=True)
        df = pd.DataFrame(df.loc[df['Model Year'] >= settings.summary_start_year, :])

        # get sales from compliance report
        df = df.merge(sales_df, on=id_args + ['Manufacturer', 'Reg-Class'], how='left')
        for arg in args:
            df.insert(len(df.columns), f'{arg}*Sales', df[arg] * df['Sales'])

        # work on sums
        df_regclass_totals = df.groupby(by=id_args + ['Reg-Class', 'Param Type'], as_index=False).sum()
        df_regclass_totals.insert(df_regclass_totals.columns.get_loc('Reg-Class'), 'Manufacturer', 'TOTAL')
        df = pd.concat([df, df_regclass_totals], axis=0, ignore_index=True)
        df = df.reset_index(drop=True)

        for arg in args:
            df[arg] = df[f'{arg}*Sales'] / df['Sales']
            df.drop(columns=[f'{arg}*Sales'], inplace=True)

        # sum some columns
        df = self.sum_cols(df, 'BEV', 'PHEV', 'HCR')
        df.insert(len(df.columns), 'BEV+PHEV', df[['BEV', 'PHEV']].sum(axis=1))

        return df

    @staticmethod
    def sum_cols(df, *identifiers):
        for identifier in identifiers:
            df.insert(len(df.columns), identifier, df.loc[:, [x for x in df.columns if x.__contains__(identifier)]].sum(axis=1))
        return df


class VehiclesReport:
    """
    Note:
        This class controls the summation, sales weighting, etc., of framework OEM and non-framework OEM results into a single fleet for the vehicles
        report.

    """

    def __init__(self, report_df):
        self.report_df = report_df

    def new_report(self, settings):
        """

        Note:
            This method returns a DataFrame of sales-weighted costs for the different powertrain techs for each scenario and model year (those
            specified in settings.run_model_years). It does not return the CCEMS vehicles report.

        Parameters:
            settings: The SetInputs class.

        Return:
            A DataFrame of Sales, Sales Share, Sales-Weighted Avg Cost Add and Contribution to the cost/vehicle in each model year for each scenario.

        """
        cols = ['Scenario Name', 'Model Year', 'Manufacturer', 'Powertrain', 'Tech Class', 'Sales', 'Tech Cost', 'TechKey']
        df = pd.DataFrame(self.report_df, columns=cols)
        scenario_names = pd.Series(df['Scenario Name']).unique()
        manufacturers = pd.Series(df['Manufacturer']).unique()
        powertrains = pd.Series(df['Powertrain']).unique()
        tech_classes = pd.Series(df['Tech Class']).unique()
        id_args = ['Scenario Name', 'Model Year', 'Powertrain']

        return_df = pd.DataFrame(columns=['Scenario Name', 'Model Year', 'Powertrain', 'Sales', 'Share', 'SalesWtdAvg_Cost_Add', 'Contribution to $/veh'])
        for scenario_name in scenario_names:
            for model_year in settings.run_model_years:
                my_data = df.loc[(df['Scenario Name'] == scenario_name) & (df['Model Year'] == model_year), :]
                my_sales = my_data['Sales'].sum(axis=0)
                for powertrain in powertrains:
                    if powertrain != 'MHEV':
                        tech_data = my_data.loc[my_data['Powertrain'] == powertrain, :]
                        tech_sales, wtd_avg_cost = self.calc_results(tech_data)
                        share = tech_sales / my_sales
                        contribution = wtd_avg_cost * share
                        new_data = pd.DataFrame({'Scenario Name': [scenario_name],
                                                 'Model Year': [model_year],
                                                 'Powertrain': [powertrain],
                                                 'Sales': [tech_sales],
                                                 'Share': [share],
                                                 'SalesWtdAvg_Cost_Add': [wtd_avg_cost],
                                                 'Contribution to $/veh': [contribution],
                                                 })
                        return_df = pd.concat([return_df, new_data], ignore_index=True, axis=0)
                    else:
                        for MHEV_tech in ['SS12V', 'BISG']:
                            tech_data = my_data.loc[my_data['TechKey'].str.contains(MHEV_tech)]
                            tech_sales, wtd_avg_cost = self.calc_results(tech_data)
                            share = tech_sales / my_sales
                            contribution = wtd_avg_cost * share
                            new_data = pd.DataFrame({'Scenario Name': [scenario_name],
                                                     'Model Year': [model_year],
                                                     'Powertrain': [MHEV_tech],
                                                     'Sales': [tech_sales],
                                                     'Share': [share],
                                                     'SalesWtdAvg_Cost_Add': [wtd_avg_cost],
                                                     'Contribution to $/veh': [contribution],
                                                     })
                            return_df = pd.concat([return_df, new_data], ignore_index=True, axis=0)

        return return_df

    @staticmethod
    def calc_results(tech_data):
        """

        Parameters:
            tech_data: A DataFrame of powertrain specific data for a given scenario and model year.

        Return:
            The sales of vehicles with the given powertrain tech and the sales-weighted average cost of that powertrain tech.

        """
        weighted_cost = tech_data[['Sales', 'Tech Cost']].product(axis=1).sum(axis=0)
        tech_sales = tech_data['Sales'].sum(axis=0)
        wtd_avg_cost = weighted_cost / tech_sales

        return tech_sales, wtd_avg_cost


if __name__ == '__main__':
    print('This module does not run as a script.')
