import pandas as pd
import attr


@attr.s
class ComplianceReport:
    """
    Note:
        This class controls the summation, sales weighting, etc., of framework OEM and non-framework OEM results into a single fleet for the compliance report.

    """
    report_df = attr.ib()

    def new_report(self, settings):
        df = self.report_df.copy().fillna(0)
        id_args = ['Scenario Name', 'Model Year']
        merge_cols = ['Scenario Name', 'Model Year', 'Manufacturer', 'Reg-Class']

        # eliminate some total rows since those need re-calc (drop model year total row because .... what is it anyway?)
        df = pd.DataFrame(df.loc[df['Model Year'] != 'TOTAL', :])
        df = pd.DataFrame(df.loc[df['Model Year'] >= settings.summary_start_year, :])
        df = pd.DataFrame(df.loc[df['Manufacturer'] != 'TOTAL', :])
        df['Model Year'] = df['Model Year'].astype(int)

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
        # df = df_sum.merge(df_sales_weight, on=merge_cols, how='left')

        return df


@attr.s
class CostsReport:
    """
    Note:
        This class controls the summation, sales weighting, etc., of framework OEM and non-framework OEM results into a single fleet for the cost report.

    """
    report_df = attr.ib()

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


@attr.s
class EffectsReport:
    """
    Note:
        This class controls the summation, sales weighting, etc., of framework OEM and non-framework OEM results into a single fleet for the effects report.

    """
    report_df = attr.ib()

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


@attr.s
class TechReport:
    """
    Note:
        This class controls the summation, sales weighting, etc., of framework OEM and non-framework OEM results into a single fleet for the technology
        utilization report.

    """
    report_df = attr.ib()

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

        return df

    def sum_cols(self, df, *identifiers):
        for identifier in identifiers:
            df.insert(len(df.columns), identifier, df.loc[:, [x for x in df.columns if x.__contains__(identifier)]].sum(axis=1))
        return df


if __name__ == '__main__':
    print('This module does not run as a script.')
