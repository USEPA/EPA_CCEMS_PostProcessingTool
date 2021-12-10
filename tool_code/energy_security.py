import pandas as pd
from tool_code.dict_and_df_converters import create_costs_dict, convert_dict_to_df


def get_energy_security_cost_factors(settings, year):
    """
    Note:
        This function reads a dictionary of energy security premia and returns those for the passed year.

    Parameter:
        settings: The SetInputs class.\n
        year: The calendar year for which energy security cost factors are needed.

    Return:
        1 value - the energy security cost factor (dollars/BBL).

    """
    max_year = max([yr for yr in settings.energy_security_cost_factors.keys()])
    if year > max_year: year = max_year
    energy_security_cost_factor = settings.energy_security_cost_factors[year]['2018 $ / barrel']

    return energy_security_cost_factor


def calc_energy_security_costs(settings, inv_df, costs_df, id_cols):
    """
    Parameters:
        settings: The SetInputs class.\n
        inv_df: A DataFrame of emission inventories.\n
        costs_df: A DataFrame based on one of the output cost reports.\n
        id_cols: A List of the identifying columns to use as keys for the inventory dictionary that is created in function.

    Return:
        A DataFrame of energy security costs (imported oil barrels times cost factor).

    """
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

        # get imported barrels of oil for this given key
        imported_bbl = inv_dict[inv_dict_key]['Barrels of Imported Oil']

        # get the cost factor for this key
        es_cost_factor = get_energy_security_cost_factors(settings, calendar_year)

        # multiply $/BBL by barrels and divide by 1000 to express in thousands as per the CAFE model convention
        key_dict = {'Petroleum Market Externalities': es_cost_factor * imported_bbl / 1000}

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

    # inv_dict_df = convert_dict_to_df(inv_dict, 'scenario_name', 'calendar_year', 'reg_class', 'fuel_type', 'discount_rate')
    # inv_dict_df.to_csv(settings.path_tool_runs_runid_outputs / 'inventory.csv', index=False)

    # keys_dict_df = convert_dict_to_df(keys_dict, 'scenario_name', 'calendar_year', 'reg_class', 'fuel_type', 'discount_rate')
    # keys_dict_df.to_csv(settings.path_tool_runs_runid_outputs / 'energy_security_costs.csv', index=False)

    return return_df
