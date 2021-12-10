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
        This function calculates new effects for the effects file, including:\n
        - fatalities from the change in risk\n
        - fatalities from the change in VMT\n
        - and several fuel-related parameters such a barrels of oil, imported oil and share of US fuel consumption

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
            # filename_keyword = 'summary'
        if len(key) == 6:
            scenario_name, model_year, age, calendar_year, reg_class, fuel_type = key
            base_key = (no_action, model_year, age, calendar_year, reg_class, fuel_type)
            # filename_keyword = 'lifetime'

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
        gallons, oil_bbl, share_of_annual, imported_oil_bbl, imported_oil_bbl_per_day, kwh_electricity = 0, 0, 0, 0, 0, 0
        # if fuel_type != 'TOTAL':
        if fuel_type != 'Electricity':
            if fuel_type == 'Gasoline':
                share = settings.e0_in_retail_gasoline
                ratio = settings.energy_density_ratio_e0
            elif fuel_type == 'E85': # CCEMS expresses kGallons in gallons of gasoline equivalents, so treat as retail
                share = settings.e0_in_retail_gasoline
                ratio = settings.energy_density_ratio_e0
                # share = settings.e0_in_e85
                # ratio = settings.energy_density_ratio_e0
            elif fuel_type == 'Hydrogen':
                share = 0
                ratio = 0
            else: # CCEMS expresses kGallons in gallons of gasoline equivalents, so treat as retail
                share = settings.e0_in_retail_gasoline
                ratio = settings.energy_density_ratio_e0
                # share = 1
                # ratio = settings.energy_density_ratio_diesel
            gallons = calc_dict[key]['kGallons'] * 1000
            oil_bbl = gallons * share * ratio / settings.gal_per_bbl
            imported_oil_bbl = oil_bbl * settings.imported_oil_share
            imported_oil_bbl_per_day = imported_oil_bbl / 365
            share_of_annual_gasoline = gallons / settings.gallons_of_gasoline_us_annual
            share_of_annual = oil_bbl / settings.bbl_oil_us_annual
        elif fuel_type == 'Electricity':
            kwh_electricity = calc_dict[key]['kGallons'] * 1000 * settings.kwh_per_gge
            share_of_annual = kwh_electricity / settings.kwh_us_annual

        calc_dict[key].update({f'Share of {settings.year_for_compares} US gasoline': share_of_annual_gasoline,
                               'Barrels of Oil': oil_bbl,
                               f'Share of {settings.year_for_compares} US oil/elec': share_of_annual,
                               'Barrels of Imported Oil': imported_oil_bbl,
                               'Barrels of Imported Oil per Day': imported_oil_bbl_per_day,
                               'kWh': kwh_electricity,
                               }
                              )

    # now sum the new petroleum and electricity args by reg-class (i.e., where fuel_type = 'TOTAL')
    for key in calc_dict.keys():

        try:
            scenario_name, year, reg_class, fuel_type = key
        except:
            scenario_name, model_year, age, calendar_year, reg_class, fuel_type = key

        fuel_types = ['Gasoline', 'Electricity', 'Diesel', 'E85', 'Hydrogen']
        reg_classes = ['Passenger Car', 'Light Truck']
        args_for_totals = [f'Share of {settings.year_for_compares} US gasoline',
                           'Barrels of Oil',
                           f'Share of {settings.year_for_compares} US oil/elec',
                           'Barrels of Imported Oil',
                           'Barrels of Imported Oil per Day',
                           'kWh',
                           ]

        if fuel_type == 'TOTAL':
            for arg in args_for_totals:
                for reg_class in reg_classes:
                    arg_value = 0
                    for fuel_type in fuel_types:
                        try:
                            arg_value += calc_dict[scenario_name, year, reg_class, fuel_type][arg]
                            calc_dict[scenario_name, year, reg_class, 'TOTAL'][arg] = arg_value
                        except:
                            arg_value += calc_dict[scenario_name, model_year, age, calendar_year, reg_class, fuel_type][arg]
                            calc_dict[scenario_name, model_year, age, calendar_year, reg_class, 'TOTAL'][arg] = arg_value

    for key in calc_dict.keys():

        try:
            scenario_name, year, reg_class, fuel_type = key
        except:
            scenario_name, model_year, age, calendar_year, reg_class, fuel_type = key

        if reg_class == 'TOTAL':
            for arg in args_for_totals:
                arg_value = 0
                for reg_class in reg_classes:
                    try:
                        arg_value += calc_dict[scenario_name, year, reg_class, 'TOTAL'][arg]
                        calc_dict[scenario_name, year, 'TOTAL', 'TOTAL'][arg] = arg_value
                    except:
                        arg_value += calc_dict[scenario_name, model_year, age, calendar_year, reg_class, 'TOTAL'][arg]
                        calc_dict[scenario_name, model_year, age, calendar_year, 'TOTAL', 'TOTAL'][arg] = arg_value

    return_df = convert_dict_to_df(calc_dict, *id_cols)

    # make use of below for QA/QC
    # return_df.to_csv(settings.path_tool_runs_runid_outputs / f'calcs_df_{filename_keyword}.csv', index=False)

    return return_df


if __name__ == '__main__':
    print('This module does not run as a script.')
