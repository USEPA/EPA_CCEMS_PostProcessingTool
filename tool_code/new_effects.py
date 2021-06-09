from tool_code.dict_and_df_converters import create_effects_dict, convert_dict_to_df


def calc_new_fatality_metrics(df):
    """
    Note:
        This function calculates 'Fatality risk per billion VMT' and removes 'Fatalities from Rebound.'

    Parameters:
        df: A DataFrame containing 'Fatalities', 'Fatalities from Rebound' and 'kVMT.'

    Return:
        The passed DataFrame without 'Fatalities from Rebound' and with 'Fatality risk per billion VMT.'

    """

    # remove fatalities from rebound and calc fatalities per billion VMT
    df.drop(columns='Fatalities From Rebound', inplace=True)
    df.insert(df.columns.get_loc('Fatalities') + 1, 'Fatality risk per billion VMT', df['Fatalities'] / df['kVMT'] * 1e6)

    return df


def calc_new_effects(settings, df, id_cols):
    """
    Note:
        This function calculates new effects for the effects file.

    Parameters:
        settings: The SetInputs class.\n
        df: A DataFrame based on an effects report.\n
        id_cols: The identifying columns to use as keys for the dictionary that is created in function.

    Return:
        The passed DataFrame with new effects.

    """

    no_action = settings.base_social_name

    calc_dict = create_effects_dict(df, id_cols)

    base_key = ()
    # delta_dict = dict()
    for key in calc_dict.keys():

        if len(key) == 4:
            scenario_name, year, reg_class, fuel_type = key
            base_key = (no_action, year, reg_class, fuel_type)
        if len(key) == 6:
            scenario_name, model_year, age, calendar_year, reg_class, fuel_type = key
            base_key = (no_action, model_year, age, calendar_year, reg_class, fuel_type)

        # calc new fatality effects
        fatality_risk_no_action = calc_dict[base_key]['Fatality risk per billion VMT']
        fatality_risk_action = calc_dict[key]['Fatality risk per billion VMT']
        fatalities_action = calc_dict[key]['Fatalities']
        kvmt_action = calc_dict[key]['kVMT']
        fatalities_from_change_in_risk = (fatality_risk_action - fatality_risk_no_action) * kvmt_action / 1e6
        fatalities_from_change_in_vmt = fatalities_action - fatalities_from_change_in_risk

        calc_dict[key].update({'Fatalities from Change in Risk': fatalities_from_change_in_risk,
                               'Fatalities from Change in VMT': fatalities_from_change_in_vmt})

        # calc new fuel effects (ignoring diesel, E85, hydrogen since deltas are so small)
        if fuel_type == 'Gasoline':
            gasoline_bbl = calc_dict[key]['kGallons'] * 1000 / settings.gal_per_bbl
            percent_of_annual = gasoline_bbl / settings.bbl_us_annual
            calc_dict[key].update({'Barrels': gasoline_bbl, f'Percent of {settings.year_for_compares} US': percent_of_annual})
        if fuel_type == 'Electricity':
            kwh_electricity = calc_dict[key]['kGallons'] * 1000 / settings.kwh_per_gge
            percent_of_annual = kwh_electricity / settings.kwh_us_annual
            calc_dict[key].update({'kWh': kwh_electricity, f'Percent of {settings.year_for_compares} US': percent_of_annual})

    return_df = convert_dict_to_df(calc_dict, *id_cols)

    return return_df


if __name__ == '__main__':
    print('This module does not run as a script.')
