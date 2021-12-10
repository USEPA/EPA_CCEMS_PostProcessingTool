import pandas as pd
from tool_code.dict_and_df_converters import create_costs_dict, convert_dict_to_df


def get_criteria_cost_factors(settings, calendar_year, reg_class, fuel_type, discrate, cap_dict):
    """
    Note:
        This function reads a dictionary of emission cost factors and returns those for the max year <= the passed year.

    Parameters:
        settings: The SetInputs class.\n
        calendar_year: The year for which $/ton values are needed.
        reg_class: The reg class for which $/ton values are needed.
        fuel_type: The fuel type for which $/ton values are needed.
        discrate: The criteria air pollutant discount rate series to retrieve.

    Return:
        6 values - the PM25, NOx and SO2 emission cost factors (dollars/ton) for each of two different sources (tailpipe & upstream).

    """
    criteria_cost_factors_years = [k[0] for k in settings.criteria_cost_factors.keys() if k[0] <= calendar_year]
    yr = max(criteria_cost_factors_years)
    if fuel_type == 'E85': fuel_type = 'Gasoline'
    elif fuel_type == 'Hydrogen': fuel_type = 'Gasoline'
    criteria_cost_factors_key = (yr, (discrate, reg_class, fuel_type))
    dict_get = settings.criteria_cost_factors[criteria_cost_factors_key]
    pm_tailpipe, nox_tailpipe, so2_tailpipe \
        = dict_get['pm25_tailpipe_USD_per_uston'], dict_get['nox_tailpipe_USD_per_uston'], dict_get['so2_tailpipe_USD_per_uston']
    pm_upstream, nox_upstream, so2_upstream \
        = dict_get['pm25_upstream_USD_per_uston'], dict_get['nox_upstream_USD_per_uston'], dict_get['so2_upstream_USD_per_uston']
    cap_dict[criteria_cost_factors_key] = {'PM_tp': pm_tailpipe, 'NOx_tp': nox_tailpipe, 'SO2_tp': so2_tailpipe,
                                           'PM_up': pm_upstream, 'NOx_up': nox_upstream, 'SO2_up': so2_upstream}
    return pm_tailpipe, nox_tailpipe, so2_tailpipe, pm_upstream, nox_upstream, so2_upstream, cap_dict


def get_scc_cost_factors(settings, year):
    """
    Note:
        This function reads a dictionary of social cost of GHG cost factors and returns those for the passed year.

    Parameter:
        settings: The SetInputs class.\n
        year: The calendar year for which emission cost factors are needed.

    Return:
        12 values - the CO2, CH4 and N2O emission cost factors (dollars/ton) for each of 4 different discount rate/estimation streams.

    """
    co2_5, co2_3, co2_25, co2_395 = settings.scc_cost_factors[year]['co2_5.0_USD_per_metricton'], \
                                    settings.scc_cost_factors[year]['co2_3.0_USD_per_metricton'], \
                                    settings.scc_cost_factors[year]['co2_2.5_USD_per_metricton'], \
                                    settings.scc_cost_factors[year]['co2_3.95_USD_per_metricton']
    ch4_5, ch4_3, ch4_25, ch4_395 = settings.scc_cost_factors[year]['ch4_5.0_USD_per_metricton'], \
                                    settings.scc_cost_factors[year]['ch4_3.0_USD_per_metricton'], \
                                    settings.scc_cost_factors[year]['ch4_2.5_USD_per_metricton'], \
                                    settings.scc_cost_factors[year]['ch4_3.95_USD_per_metricton']
    n2o_5, n2o_3, n2o_25, n2o_395 = settings.scc_cost_factors[year]['n2o_5.0_USD_per_metricton'], \
                                    settings.scc_cost_factors[year]['n2o_3.0_USD_per_metricton'], \
                                    settings.scc_cost_factors[year]['n2o_2.5_USD_per_metricton'], \
                                    settings.scc_cost_factors[year]['n2o_3.95_USD_per_metricton']
    return co2_5, co2_3, co2_25, co2_395, \
           ch4_5, ch4_3, ch4_25, ch4_395, \
           n2o_5, n2o_3, n2o_25, n2o_395


def calc_emission_costs(settings, inv_df, costs_df, id_cols):
    """
    Parameters:
        settings: The SetInputs class.\n
        inv_df: A DataFrame of emission inventories.\n
        costs_df: A DataFrame based on one of the output cost reports.\n
        id_cols: A List of the identifying columns to use as keys for the inventory dictionary that is created in function.

    Return:
        A DataFrame of emission-related pollution (damage) costs (inventory times cost factor).

    """
    cap_dict = dict()
    inv_dict = create_costs_dict(inv_df, id_cols) # this adds discount_rate to the dict keys
    # determine what cost report we're working with, annual or model year lifetime
    new_df = costs_df.copy()
    if 'Model Year' in costs_df.columns:
        costs_keys = pd.Series(zip(new_df['Scenario Name'], new_df['Model Year'], new_df['Age'],
                                   new_df['Calendar Year'], new_df['Reg-Class'], new_df['Disc-Rate']))
    else:
        costs_keys = pd.Series(zip(new_df['Scenario Name'],
                                   new_df['Calendar Year'], new_df['Reg-Class'], new_df['Disc-Rate']))

    costs_dict = dict()

    keys_dict = dict()
    for inv_dict_key in inv_dict.keys():
        try:
            scenario_name, calendar_year, reg_class, fuel_type, discount_rate = inv_dict_key
        except:
            scenario_name, model_year, age, calendar_year, reg_class, fuel_type, discount_rate = inv_dict_key

        # get tons for this given key
        pm_tailpipe_ustons = inv_dict[inv_dict_key]['PM Tailpipe (ustons)']
        pm_upstream_ustons = inv_dict[inv_dict_key]['PM Upstream (ustons)']
        nox_tailpipe_ustons = inv_dict[inv_dict_key]['NOx Tailpipe (ustons)']
        nox_upstream_ustons = inv_dict[inv_dict_key]['NOx Upstream (ustons)']
        so2_tailpipe_ustons = inv_dict[inv_dict_key]['SO2 Tailpipe (ustons)']
        so2_upstream_ustons = inv_dict[inv_dict_key]['SO2 Upstream (ustons)']

        co2_mmt = inv_dict[inv_dict_key]['CO2 Total (mmt)']
        ch4_tons = inv_dict[inv_dict_key]['CH4 Total (t)']
        n2o_tons = inv_dict[inv_dict_key]['N2O Total (t)']

        pm_tailpipe_3, nox_tailpipe_3, so2_tailpipe_3, pm_upstream_3, nox_upstream_3, so2_upstream_3, cap_dict \
            = get_criteria_cost_factors(settings, calendar_year, reg_class, fuel_type, 0.03, cap_dict)
        pm_tailpipe_7, nox_tailpipe_7, so2_tailpipe_7, pm_upstream_7, nox_upstream_7, so2_upstream_7, cap_dict \
            = get_criteria_cost_factors(settings, calendar_year, reg_class, fuel_type, 0.07, cap_dict)

        co2_5, co2_3, co2_25, co2_395, ch4_5, ch4_3, ch4_25, ch4_395, n2o_5, n2o_3, n2o_25, n2o_395 \
            = get_scc_cost_factors(settings, calendar_year)

        # multiply $/ton by tons and divide by 1000 to express in thousands as per the CAFE model convention; co2_mmt is multiplied by 10^6 to convert to tons
        key_dict = {'PM25_Costs_tailpipe_3.0': pm_tailpipe_3 * pm_tailpipe_ustons / 1000,
                    'PM25_Costs_upstream_3.0': pm_upstream_3 * pm_upstream_ustons / 1000,
                    'NOx_Costs_tailpipe_3.0': nox_tailpipe_3 * nox_tailpipe_ustons / 1000,
                    'NOx_Costs_upstream_3.0': nox_upstream_3 * nox_upstream_ustons / 1000,
                    'SO2_Costs_tailpipe_3.0': so2_tailpipe_3 * so2_tailpipe_ustons / 1000,
                    'SO2_Costs_upstream_3.0': so2_upstream_3 * so2_upstream_ustons / 1000,
                    'PM25_Costs_tailpipe_7.0': pm_tailpipe_7 * pm_tailpipe_ustons / 1000,
                    'PM25_Costs_upstream_7.0': pm_upstream_7 * pm_upstream_ustons / 1000,
                    'NOx_Costs_tailpipe_7.0': nox_tailpipe_7 * nox_tailpipe_ustons / 1000,
                    'NOx_Costs_upstream_7.0': nox_upstream_7 * nox_upstream_ustons / 1000,
                    'SO2_Costs_tailpipe_7.0': so2_tailpipe_7 * so2_tailpipe_ustons / 1000,
                    'SO2_Costs_upstream_7.0': so2_upstream_7 * so2_upstream_ustons / 1000,
                    'Criteria_Costs_tailpipe_3.0': pm_tailpipe_3 * pm_tailpipe_ustons / 1000
                                                   + nox_tailpipe_3 * nox_tailpipe_ustons / 1000
                                                   + so2_tailpipe_3 * so2_tailpipe_ustons / 1000,
                    'Criteria_Costs_upstream_3.0': pm_upstream_3 * pm_upstream_ustons / 1000
                                                   + nox_upstream_3 * nox_upstream_ustons / 1000
                                                   + so2_upstream_3 * so2_upstream_ustons / 1000,
                    'Criteria_Costs_tailpipe_7.0': pm_tailpipe_7 * pm_tailpipe_ustons / 1000
                                                   + nox_tailpipe_7 * nox_tailpipe_ustons / 1000
                                                   + so2_tailpipe_7 * so2_tailpipe_ustons / 1000,
                    'Criteria_Costs_upstream_7.0': pm_upstream_7 * pm_upstream_ustons / 1000
                                                   + nox_upstream_7 * nox_upstream_ustons / 1000
                                                   + so2_upstream_7 * so2_upstream_ustons / 1000,
                    'Criteria_Costs_3.0': pm_tailpipe_3 * pm_tailpipe_ustons / 1000
                                          + nox_tailpipe_3 * nox_tailpipe_ustons / 1000
                                          + so2_tailpipe_3 * so2_tailpipe_ustons / 1000
                                          + pm_upstream_3 * pm_upstream_ustons / 1000
                                          + nox_upstream_3 * nox_upstream_ustons / 1000
                                          + so2_upstream_3 * so2_upstream_ustons / 1000,
                    'Criteria_Costs_7.0': pm_tailpipe_7 * pm_tailpipe_ustons / 1000
                                          + nox_tailpipe_7 * nox_tailpipe_ustons / 1000
                                          + so2_tailpipe_7 * so2_tailpipe_ustons / 1000
                                          + pm_upstream_7 * pm_upstream_ustons / 1000
                                          + nox_upstream_7 * nox_upstream_ustons / 1000
                                          + so2_upstream_7 * so2_upstream_ustons / 1000,
                    'CO2_Costs_5.0': co2_5 * co2_mmt * 1000000 / 1000,
                    'CO2_Costs_3.0': co2_3 * co2_mmt * 1000000 / 1000,
                    'CO2_Costs_2.5': co2_25 * co2_mmt * 1000000 / 1000,
                    'CO2_Costs_3.0_95': co2_395 * co2_mmt * 1000000 / 1000,
                    'CH4_Costs_5.0': ch4_5 * ch4_tons / 1000,
                    'CH4_Costs_3.0': ch4_3 * ch4_tons / 1000,
                    'CH4_Costs_2.5': ch4_25 * ch4_tons / 1000,
                    'CH4_Costs_3.0_95': ch4_395 * ch4_tons / 1000,
                    'N2O_Costs_5.0': n2o_5 * n2o_tons / 1000,
                    'N2O_Costs_3.0': n2o_3 * n2o_tons / 1000,
                    'N2O_Costs_2.5': n2o_25 * n2o_tons / 1000,
                    'N2O_Costs_3.0_95': n2o_395 * n2o_tons / 1000,
                    'GHG_Costs_5.0': co2_5 * co2_mmt * 1000000 / 1000 + ch4_5 * ch4_tons / 1000 + n2o_5 * n2o_tons / 1000,
                    'GHG_Costs_3.0': co2_3 * co2_mmt * 1000000 / 1000 + ch4_3 * ch4_tons / 1000 + n2o_3 * n2o_tons / 1000,
                    'GHG_Costs_2.5': co2_25 * co2_mmt * 1000000 / 1000 + ch4_25 * ch4_tons / 1000 + n2o_25 * n2o_tons / 1000,
                    'GHG_Costs_3.0_95': co2_395 * co2_mmt * 1000000 / 1000 + ch4_395 * ch4_tons / 1000 + n2o_395 * n2o_tons / 1000,
                    }

        keys_dict.update({inv_dict_key: key_dict})

    args_for_totals = [arg for arg, value in keys_dict[inv_dict_key].items()]
    fuel_types = ['Gasoline', 'Electricity', 'Diesel', 'E85', 'Hydrogen']
    reg_classes = ['Passenger Car', 'Light Truck']

    for costs_key in costs_keys:

        try:
            scenario_name, calendar_year, reg_class, discount_rate = costs_key
        except:
            scenario_name, model_year, age, calendar_year, reg_class, discount_rate = costs_key

        if reg_class != 'TOTAL':
            costs_dict[costs_key] = dict()
            for arg in args_for_totals:
                arg_value = 0
                for fuel_type in fuel_types:
                    try:
                        arg_value += keys_dict[scenario_name, calendar_year, reg_class, fuel_type, discount_rate][arg]
                    except:
                        arg_value += keys_dict[scenario_name, model_year, age, calendar_year, reg_class, fuel_type, discount_rate][arg]
                costs_dict[costs_key].update({arg: arg_value})

    for costs_key in costs_keys:

        try:
            scenario_name, calendar_year, reg_class, discount_rate = costs_key
        except:
            scenario_name, model_year, age, calendar_year, reg_class, discount_rate = costs_key

        if reg_class == 'TOTAL':
            costs_dict[costs_key] = dict()
            for arg in args_for_totals:
                arg_value = 0
                for reg_class in reg_classes:
                    try:
                        arg_value += costs_dict[scenario_name, calendar_year, reg_class, discount_rate][arg]
                    except:
                        arg_value += costs_dict[scenario_name, model_year, age, calendar_year, reg_class, discount_rate][arg]
                costs_dict[costs_key].update({arg: arg_value})

    if len(costs_key) == 4:
        costs_id_cols = ['Scenario Name', 'Calendar Year', 'Reg-Class', 'Disc-Rate']
    else:
        costs_id_cols = ['Scenario Name', 'Model Year', 'Age', 'Calendar Year', 'Reg-Class', 'Disc-Rate']
    return_df = convert_dict_to_df(costs_dict, *costs_id_cols)

    # re-activate the following for QA/QC of BPT values and results to ensure proper valuations
    # cap_df = convert_dict_to_df(cap_dict, 'year', 'discrate, reg_class, fuel_type')
    # cap_df.to_csv(settings.path_tool_runs_runid_outputs / 'cap_BPT.csv', index=False)

    # inv_dict_df = convert_dict_to_df(inv_dict, 'scenario_name', 'calendar_year', 'reg_class', 'fuel_type', 'discount_rate')
    # inv_dict_df.to_csv(settings.path_tool_runs_runid_outputs / 'inventory.csv', index=False)

    # keys_dict_df = convert_dict_to_df(keys_dict, 'scenario_name', 'calendar_year', 'reg_class', 'fuel_type', 'discount_rate')
    # keys_dict_df.to_csv(settings.path_tool_runs_runid_outputs / 'cap_costs.csv', index=False)

    return return_df


if __name__ == '__main__':
    print('This module does not run as a script.')
