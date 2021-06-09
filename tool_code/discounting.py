from tool_code.dict_and_df_converters import create_costs_dict, convert_dict_to_df
from tool_code.benefits_and_costs import calc_social_impacts


def discount_values(settings, df, id_cols, discount_rates, *non_emission_cost_args):
    """
    Note:
        The discount function discounts non-emission args at the social discount rates entered in the SetInputs class and discounts
         emission args at their internal rate of return ONLY. Results are reported according ot the social discount rates, but emission
         args are always discounted at their internal rate of return. Values are discounted to a given year and assume costs start at the beginning
         or end of that year.\n
         The passed dictionary keys should consist of:\n
            (scenario_name, year, reg_class, discount_rate) or (scenario_name, model_year, age, calendar_year, reg_class, discount_rate)\n

        The costs_start entry of the SetInputs class should be set to 'start-year' or 'end-year', where start-year represents costs
        starting at time t=0 (i.e., first year costs are undiscounted), and end-year represents costs starting at time t=1 (i.e., first year
        costs are discounted).

    Parameters:
        settings: The SetInputs class.\n
        df: A DataFrame of values to be discounted.\n
        id_cols: The identifying columns to use as keys for the dictionary that is created in function.\n
        discount_rates: The social discount rates to use.\n
        non_emission_cost_args: Args to be discounted at both social discount rates.

    Return:
        The passed DataFrame with discounted values added; a DataFrame of present values (through the given calendar year); a DataFrame of annualized values (through the given calendar year).

    """
    if settings.costs_start == 'start-year': discount_offset = 0
    elif settings.costs_start == 'end-year': discount_offset = 1
    discount_to_year = settings.discount_year

    calc_dict = create_costs_dict(df, id_cols)
    for key in calc_dict.keys():
        args = [k for k in calc_dict[key].keys()]
    emission_costs_3 = [arg for arg in args if 'Cost' in arg and '3.0' in arg]
    emission_costs_7 = [arg for arg in args if 'Cost' in arg and '7.0' in arg]
    emission_costs_5 = [arg for arg in args if 'Cost' in arg and '5.0' in arg]
    emission_costs_25 = [arg for arg in args if 'Cost' in arg and '2.5' in arg]

    max_age = 0
    update_dict = dict()
    for key in calc_dict.keys():

        if len(id_cols) == 3:
            scenario_name, calendar_year, reg_class, discount_rate = key
        if len(id_cols) == 5:
            scenario_name, model_year, age, calendar_year, reg_class, discount_rate = key
            if age > max_age and calc_dict[key]['Retail Fuel Outlay'] > 0: max_age = age

        # first discount non-emission costs at each social discount rate while also discounting emission costs at their stream discount rate
        for social_discrate in discount_rates:
            rate_dict = dict()
            for arg in non_emission_cost_args:
                if calendar_year >= discount_to_year:
                    arg_value = calc_dict[key][arg] / ((1 + social_discrate) ** (calendar_year - discount_to_year + discount_offset))
                else: arg_value = calc_dict[key][arg]
                rate_dict.update({arg: arg_value})

            emission_discrate = 0.03
            for arg in emission_costs_3:
                if calendar_year >= discount_to_year:
                    arg_value = calc_dict[key][arg] / ((1 + emission_discrate) ** (calendar_year - discount_to_year + discount_offset))
                else: arg_value = calc_dict[key][arg]
                rate_dict.update({arg: arg_value})

            emission_discrate = 0.025
            for arg in emission_costs_25:
                if calendar_year >= discount_to_year:
                    arg_value = calc_dict[key][arg] / ((1 + emission_discrate) ** (calendar_year - discount_to_year + discount_offset))
                else: arg_value = calc_dict[key][arg]
                rate_dict.update({arg: arg_value})

            emission_discrate = 0.05
            for arg in emission_costs_5:
                if calendar_year >= discount_to_year:
                    arg_value = calc_dict[key][arg] / ((1 + emission_discrate) ** (calendar_year - discount_to_year + discount_offset))
                else: arg_value = calc_dict[key][arg]
                rate_dict.update({arg: arg_value})

            emission_discrate = 0.07
            for arg in emission_costs_7:
                if calendar_year >= discount_to_year:
                    arg_value = calc_dict[key][arg] / ((1 + emission_discrate) ** (calendar_year - discount_to_year + discount_offset))
                else: arg_value = calc_dict[key][arg]
                rate_dict.update({arg: arg_value})

            if len(id_cols) == 3:
                update_dict[scenario_name, calendar_year, reg_class, social_discrate] = rate_dict
            if len(id_cols) == 5:
                update_dict[scenario_name, model_year, age, calendar_year, reg_class, social_discrate] = rate_dict
    calc_dict.update(update_dict)

    calc_dict = calc_social_impacts(settings, calc_dict)

    return_df = convert_dict_to_df(calc_dict, *id_cols, 'Disc-Rate')

    if len(id_cols) == 3:
        present_values_dict = calc_present_values(settings, calc_dict, *non_emission_cost_args)
        annualized_dict = annualize_calendar_year_values(settings, present_values_dict, *non_emission_cost_args)

        present_values_dict = calc_social_impacts(settings, present_values_dict)
        annualized_dict = calc_social_impacts(settings, annualized_dict)

        present_values_df = convert_dict_to_df(present_values_dict, *id_cols, 'Disc-Rate')
        annualized_df = convert_dict_to_df(annualized_dict, *id_cols, 'Disc-Rate')

    if len(id_cols) == 5:
        present_values_dict = calc_present_values(settings, calc_dict, *non_emission_cost_args)
        annualized_dict = annualize_model_year_values(settings, present_values_dict, max_age, *non_emission_cost_args)

        present_values_dict = calc_social_impacts(settings, present_values_dict)
        annualized_dict = calc_social_impacts(settings, annualized_dict)

        present_values_df = convert_dict_to_df(present_values_dict, 'Scenario Name', 'Model Year', 'Reg-Class', 'Disc-Rate')
        annualized_df = convert_dict_to_df(annualized_dict, 'Scenario Name', 'Model Year', 'Reg-Class', 'Disc-Rate')

    return return_df, present_values_df, annualized_df


def calc_present_values(settings, dict_of_values, *non_emission_cost_args):
    """
    Note:
        This function calculates present values based on the discounted values in the passed dictionary.

    Parameters:
        settings: The SetInputs class.\n
        dict_of_values: A Dictionary of values with keys of:\n
            (scenario_name, year, reg_class, discount_rate) or (scenario_name, model_year, age, calendar_year, reg_class, discount_rate)\n
        non_emission_cost_args: Args to be present valued (?) at both social discount rates.

    Return:
        A Dictionary of present values (for annual values: cumulative summations through the given calendar year; for model year lifetime
        values: present values of monetized values through the full lifetime) by key for any monetized arg in the passed dictionary.

    """
    discount_to_year = settings.discount_year

    for key in dict_of_values.keys():
        args = [k for k in dict_of_values[key].keys()]
    emission_costs = [arg for arg in args if 'Cost' in arg and 'SocialBenefits' not in arg]
    all_costs = [arg for arg in non_emission_cost_args] + emission_costs

    cumulative_dict = dict()
    for key in dict_of_values.keys():

        if len(key) == 4:
            scenario_name, calendar_year, reg_class, discount_rate = key
        if len(key) == 6:
            scenario_name, model_year, age, calendar_year, reg_class, discount_rate = key
        # scenario_name, calendar_year, reg_class, discount_rate = key

        # first calc present values as cumulative sums of all cost args
        key_dict = dict()
        if len(key) == 6:
            cumulative_dict_key = (scenario_name, model_year, reg_class, discount_rate)
            if model_year >= discount_to_year and age == 0:
                for arg in all_costs:
                    arg_value = dict_of_values[key][arg]
                    key_dict.update({arg: arg_value})
                cumulative_dict[cumulative_dict_key] = key_dict
            elif model_year >= discount_to_year and age > 0:
                for arg in all_costs:
                    arg_value = dict_of_values[key][arg]
                    last_year_cumulative_value = cumulative_dict[cumulative_dict_key][arg]
                    key_dict.update({arg: arg_value + last_year_cumulative_value})
                cumulative_dict[cumulative_dict_key] = key_dict
        else:
            if calendar_year == discount_to_year:
                for arg in all_costs:
                    arg_value = dict_of_values[key][arg]
                    key_dict.update({arg: arg_value})
                cumulative_dict[key] = key_dict
            if calendar_year > discount_to_year:
                for arg in all_costs:
                    arg_value = dict_of_values[key][arg]
                    last_year = calendar_year - 1
                    cumulative_arg_value = cumulative_dict[scenario_name, last_year, reg_class, discount_rate][arg]
                    key_dict.update({arg: cumulative_arg_value + arg_value})
                cumulative_dict[key] = key_dict

    return cumulative_dict


def annualize_calendar_year_values(settings, dict_of_values, *non_emission_cost_args):
    """
    Note:
        This function makes use of a cumulative sum of annual discounted values. As such, the cumulative sums represent a present value
        through the given calendar year. The Offset is included to reflect costs beginning at the start of the year (Offset=1)
        or the end of the year (Offset=0).\n
        The equation used here is shown below.

        AC = PV * DR * (1+DR)^(period) / [(1+DR)^(period+Offset) - 1]

        where,\n
        AC = Annualized Cost\n
        PV = Present Value (here, the cumulative summary of discounted annual values)\n
        DR = Discount Rate\n
        CY = Calendar Year (yearID)\n
        period = the current CY minus the year to which to discount values + a discount_offset value where discount_offset equals the costs_start input value\n
        Offset = 1 for costs at the start of the year, 0 for cost at the end of the year

    Parameters:
        settings: The SetInputs class.\n
        dict_of_values: A dictionary of present values containing optionID, yearID, DiscountRate and Cost arguments.\n
        non_emission_cost_args: Args to be annualized at both social discount rates.\n

    Return:
        A Dictionary of annualized values through the given calendar year and by key for any monetized arg in the passed dictionary.

    """
    global discount_offset, annualized_offset
    if settings.costs_start == 'start-year':
        discount_offset = 0
        annualized_offset = 1
    if settings.costs_start == 'end-year':
        discount_offset = 1
        annualized_offset = 0
    discount_to_year = settings.discount_year

    for key in dict_of_values.keys():
        args = [k for k in dict_of_values[key].keys()]
    emission_costs_3 = [arg for arg in args if 'Cost' in arg and '3.0' in arg]
    emission_costs_7 = [arg for arg in args if 'Cost' in arg and '7.0' in arg]
    emission_costs_5 = [arg for arg in args if 'Cost' in arg and '5.0' in arg]
    emission_costs_25 = [arg for arg in args if 'Cost' in arg and '2.5' in arg]

    # now annualize those present values, but skip for keys having discount_rate == 0
    annualized_dict = dict()
    for key in dict_of_values.keys():
        scenario_name, calendar_year, reg_class, discount_rate = key

        key_dict = dict()
        if discount_rate != 0:
            periods = calendar_year - discount_to_year + discount_offset
            key_dict.update({'Annualization_Periods': periods})
            for arg in non_emission_cost_args:
                present_value = dict_of_values[key][arg]
                annualized_arg = present_value * discount_rate * (1 + discount_rate) ** periods \
                                 / ((1 + discount_rate) ** (periods + annualized_offset) - 1)
                key_dict.update({arg: annualized_arg})

            emission_discrate = 0.03
            for arg in emission_costs_3:
                present_value = dict_of_values[key][arg]
                annualized_arg = present_value * emission_discrate * (1 + emission_discrate) ** periods \
                                 / ((1 + emission_discrate) ** (periods + annualized_offset) - 1)
                key_dict.update({arg: annualized_arg})

            emission_discrate = 0.025
            for arg in emission_costs_25:
                present_value = dict_of_values[key][arg]
                annualized_arg = present_value * emission_discrate * (1 + emission_discrate) ** periods \
                                 / ((1 + emission_discrate) ** (periods + annualized_offset) - 1)
                key_dict.update({arg: annualized_arg})

            emission_discrate = 0.05
            for arg in emission_costs_5:
                present_value = dict_of_values[key][arg]
                annualized_arg = present_value * emission_discrate * (1 + emission_discrate) ** periods \
                                 / ((1 + emission_discrate) ** (periods + annualized_offset) - 1)
                key_dict.update({arg: annualized_arg})

            emission_discrate = 0.07
            for arg in emission_costs_7:
                present_value = dict_of_values[key][arg]
                annualized_arg = present_value * emission_discrate * (1 + emission_discrate) ** periods \
                                 / ((1 + emission_discrate) ** (periods + annualized_offset) - 1)
                key_dict.update({arg: annualized_arg})
            annualized_dict[key] = key_dict

    return annualized_dict


def annualize_model_year_values(settings, dict_of_values, max_age, *non_emission_cost_args):
    """
    Note:
        This function makes use of a cumulative sum of annual discounted values. As such, the cumulative sums represent a present value
        through the given calendar year. The Offset is included to reflect costs beginning at the start of the year (Offset=1)
        or the end of the year (Offset=0).\n
        The equation used here is shown below.

        AC = PV * DR * (1+DR)^(period) / [(1+DR)^(period+Offset) - 1]

        where,\n
        AC = Annualized Cost\n
        PV = Present Value (here, the cumulative summary of discounted annual values)\n
        DR = Discount Rate\n
        CY = Calendar Year (yearID)\n
        period = the current CY minus the year to which to discount values + a discount_offset value where discount_offset equals the costs_start input value\n
        Offset = 1 for costs at the start of the year, 0 for cost at the end of the year

    Parameters:
        settings: The SetInputs class.\n
        dict_of_values: A dictionary of present values.\n
        non_emission_cost_args: Args to be annualized at both social discount rates.\n

    Return:
        A Dictionary of annualized values for the given model year lifetime for any monetized arg in the passed dictionary.

    """
    global discount_offset, annualized_offset
    if settings.costs_start == 'start-year':
        discount_offset = 0
        annualized_offset = 1
    if settings.costs_start == 'end-year':
        discount_offset = 1
        annualized_offset = 0
    # discount_to_year = settings.discount_year

    for key in dict_of_values.keys():
        args = [k for k in dict_of_values[key].keys()]
    emission_costs_3 = [arg for arg in args if 'Cost' in arg and '3.0' in arg]
    emission_costs_7 = [arg for arg in args if 'Cost' in arg and '7.0' in arg]
    emission_costs_5 = [arg for arg in args if 'Cost' in arg and '5.0' in arg]
    emission_costs_25 = [arg for arg in args if 'Cost' in arg and '2.5' in arg]

    # now annualize those present values, but skip for keys having discount_rate == 0
    annualized_dict = dict()
    for key in dict_of_values.keys():
        scenario_name, model_year, reg_class, discount_rate = key

        key_dict = dict()
        if discount_rate != 0:
            periods = max_age + discount_offset
            key_dict.update({'Annualization_Periods': periods})
            for arg in non_emission_cost_args:
                present_value = dict_of_values[key][arg]
                annualized_arg = present_value * discount_rate * (1 + discount_rate) ** periods \
                                 / ((1 + discount_rate) ** (periods + annualized_offset) - 1)
                key_dict.update({arg: annualized_arg})

            emission_discrate = 0.03
            for arg in emission_costs_3:
                present_value = dict_of_values[key][arg]
                annualized_arg = present_value * emission_discrate * (1 + emission_discrate) ** periods \
                                 / ((1 + emission_discrate) ** (periods + annualized_offset) - 1)
                key_dict.update({arg: annualized_arg})

            emission_discrate = 0.025
            for arg in emission_costs_25:
                present_value = dict_of_values[key][arg]
                annualized_arg = present_value * emission_discrate * (1 + emission_discrate) ** periods \
                                 / ((1 + emission_discrate) ** (periods + annualized_offset) - 1)
                key_dict.update({arg: annualized_arg})

            emission_discrate = 0.05
            for arg in emission_costs_5:
                present_value = dict_of_values[key][arg]
                annualized_arg = present_value * emission_discrate * (1 + emission_discrate) ** periods \
                                 / ((1 + emission_discrate) ** (periods + annualized_offset) - 1)
                key_dict.update({arg: annualized_arg})

            emission_discrate = 0.07
            for arg in emission_costs_7:
                present_value = dict_of_values[key][arg]
                annualized_arg = present_value * emission_discrate * (1 + emission_discrate) ** periods \
                                 / ((1 + emission_discrate) ** (periods + annualized_offset) - 1)
                key_dict.update({arg: annualized_arg})
            annualized_dict[key] = key_dict

    return annualized_dict


if __name__ == '__main__':
    print('This module does not run as a script.')
