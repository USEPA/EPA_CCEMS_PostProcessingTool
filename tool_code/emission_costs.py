import pandas as pd
from tool_code.dict_and_df_converters import create_costs_dict, convert_dict_to_df


def get_criteria_cost_factors(settings, year):
    """
    Note:
        This function reads a dictionary of emission cost factors and returns those for the passed year.

    Parameters:
        settings: The SetInputs class.\n
        year: The calendar year for which emission cost factors are needed.

    Return:
        12 values - the PM25, NOx and SO2 emission cost factors (dollars/ton) for each of two different sources (tailpipe & upstream) and each of two
        different discount rates.

    """
    pm_tailpipe_3, pm_upstream_3, pm_tailpipe_7, pm_upstream_7 = settings.criteria_cost_factors[year]['pm25_tailpipe_3.0_USD_per_uston'], \
                                                                 settings.criteria_cost_factors[year]['pm25_upstream_3.0_USD_per_uston'], \
                                                                 settings.criteria_cost_factors[year]['pm25_tailpipe_7.0_USD_per_uston'], \
                                                                 settings.criteria_cost_factors[year]['pm25_upstream_7.0_USD_per_uston']
    nox_tailpipe_3, nox_upstream_3, nox_tailpipe_7, nox_upstream_7 = settings.criteria_cost_factors[year]['nox_tailpipe_3.0_USD_per_uston'], \
                                                                     settings.criteria_cost_factors[year]['nox_upstream_3.0_USD_per_uston'], \
                                                                     settings.criteria_cost_factors[year]['nox_tailpipe_7.0_USD_per_uston'], \
                                                                     settings.criteria_cost_factors[year]['nox_upstream_7.0_USD_per_uston']
    so2_tailpipe_3, so2_upstream_3, so2_tailpipe_7, so2_upstream_7 = settings.criteria_cost_factors[year]['so2_tailpipe_3.0_USD_per_uston'], \
                                                                     settings.criteria_cost_factors[year]['so2_upstream_3.0_USD_per_uston'], \
                                                                     settings.criteria_cost_factors[year]['so2_tailpipe_7.0_USD_per_uston'], \
                                                                     settings.criteria_cost_factors[year]['so2_upstream_7.0_USD_per_uston']
    return pm_tailpipe_3, pm_upstream_3, pm_tailpipe_7, pm_upstream_7, \
           nox_tailpipe_3, nox_upstream_3, nox_tailpipe_7, nox_upstream_7, \
           so2_tailpipe_3, so2_upstream_3, so2_tailpipe_7, so2_upstream_7


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
    co2_5, co2_3, co2_25, co2_395 = settings.scc_cost_factors[year]['co2_global_5.0_USD_per_metricton'], \
                                    settings.scc_cost_factors[year]['co2_global_3.0_USD_per_metricton'], \
                                    settings.scc_cost_factors[year]['co2_global_2.5_USD_per_metricton'], \
                                    settings.scc_cost_factors[year]['co2_global_3.95_USD_per_metricton']
    ch4_5, ch4_3, ch4_25, ch4_395 = settings.scc_cost_factors[year]['ch4_global_5.0_USD_per_metricton'], \
                                    settings.scc_cost_factors[year]['ch4_global_3.0_USD_per_metricton'], \
                                    settings.scc_cost_factors[year]['ch4_global_2.5_USD_per_metricton'], \
                                    settings.scc_cost_factors[year]['ch4_global_3.95_USD_per_metricton']
    n2o_5, n2o_3, n2o_25, n2o_395 = settings.scc_cost_factors[year]['n2o_global_5.0_USD_per_metricton'], \
                                    settings.scc_cost_factors[year]['n2o_global_3.0_USD_per_metricton'], \
                                    settings.scc_cost_factors[year]['n2o_global_2.5_USD_per_metricton'], \
                                    settings.scc_cost_factors[year]['n2o_global_3.95_USD_per_metricton']
    return co2_5, co2_3, co2_25, co2_395, \
           ch4_5, ch4_3, ch4_25, ch4_395, \
           n2o_5, n2o_3, n2o_25, n2o_395


def calc_emission_costs(settings, df, id_cols):
    """
    Parameters:
        settings: The SetInputs class.\n
        df: A DataFrame of emission inventories.\n
        id_cols: The identifying columns to use as keys for the dictionary that is created in function.

    Return:
        The passed DataFrame with emission-related pollution (damage) costs (inventory times cost factor).

    """
    calc_dict = create_costs_dict(df, id_cols)

    for key in calc_dict.keys():
        if len(id_cols) == 3:
            scenario_name, calendar_year, reg_class, discount_rate = key
        if len(id_cols) == 5:
            scenario_name, model_year, age, calendar_year, reg_class, discount_rate = key
        # print(f'Calculating emission costs for {scenario_name}, {calendar_year}, {reg_class}')

        # get cost factors ($/ton)
        pm_tailpipe_3, pm_upstream_3, pm_tailpipe_7, pm_upstream_7, \
        nox_tailpipe_3, nox_upstream_3, nox_tailpipe_7, nox_upstream_7, \
        so2_tailpipe_3, so2_upstream_3, so2_tailpipe_7, so2_upstream_7 = get_criteria_cost_factors(settings, calendar_year)

        co2_5, co2_3, co2_25, co2_395, ch4_5, ch4_3, ch4_25, ch4_395, n2o_5, n2o_3, n2o_25, n2o_395 = get_scc_cost_factors(settings, calendar_year)

        # get tons
        pm_tailpipe_ustons = calc_dict[key]['PM Tailpipe (ustons)']
        pm_upstream_ustons = calc_dict[key]['PM Upstream (ustons)']
        nox_tailpipe_ustons = calc_dict[key]['NOx Tailpipe (ustons)']
        nox_upstream_ustons = calc_dict[key]['NOx Upstream (ustons)']
        so2_tailpipe_ustons = calc_dict[key]['SO2 Tailpipe (ustons)']
        so2_upstream_ustons = calc_dict[key]['SO2 Upstream (ustons)']

        co2_mmt = calc_dict[key]['CO2 Total (mmt)']
        ch4_tons = calc_dict[key]['CH4 Total (t)']
        n2o_tons = calc_dict[key]['N2O Total (t)']

        # multiply $/ton by tons and divide by 1000 to express in thousands as per the CAFE model convention; co2_mmt is multiplied by 10^6 to convert to tons
        update_dict = {'PM25_Costs_tailpipe_3.0': pm_tailpipe_3 * pm_tailpipe_ustons / 1000,
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

        calc_dict[key].update(update_dict)

    return_df = convert_dict_to_df(calc_dict, *id_cols, 'Disc-Rate')
    cost_cols = [col for col in return_df.columns if 'Cost' in col]
    cols = id_cols + ['Disc-Rate'] + cost_cols
    return_df = pd.DataFrame(return_df, columns=cols)

    return return_df


if __name__ == '__main__':
    print('This module does not run as a script.')
