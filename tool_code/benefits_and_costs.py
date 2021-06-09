

def calc_social_impacts(settings, dict_of_values):
    """
    Note:
        The dictionary key = (scenario_name, year, reg_class, discount_rate) or (scenario_name, model_year, age, calendar_year, reg_class, discount_rate)

    Parameters:
        settings: The SetInputs class.\n
        dict_of_values: A dictionary consisting of a 4 or 6 element key.

    Return:
        The passed dictionary updated with new costs, benefits and net benefits calculations relative to the base_social_name.

    """
    no_action = settings.base_social_name
    base_key = ()
    delta_dict = dict()
    for key in dict_of_values.keys():

        if len(key) == 4:
            scenario_name, year, reg_class, discount_rate = key
            base_key = (no_action, year, reg_class, discount_rate)
        if len(key) == 6:
            scenario_name, model_year, age, calendar_year, reg_class, discount_rate = key
            base_key = (no_action, model_year, age, calendar_year, reg_class, discount_rate)

        social_costs = 0

        # calc fuel savings (calc as base minus action)
        base_fuel_expenditures = dict_of_values[base_key][settings.retail_fuel_expenditures]
        base_tax_revenues = dict_of_values[base_key][settings.fuel_tax_revenues]
        action_fuel_expenditures = dict_of_values[key][settings.retail_fuel_expenditures]
        action_tax_revenues = dict_of_values[key][settings.fuel_tax_revenues]
        fuel_savings = (base_fuel_expenditures - base_tax_revenues) - (action_fuel_expenditures - action_tax_revenues)
        delta_dict.update({'TotalFuelSavings': fuel_savings})

        # calc social costs
        for arg in settings.social_cost_args:
            base_arg_value = dict_of_values[base_key][arg]
            delta_arg = dict_of_values[key][arg] - base_arg_value
            social_costs += delta_arg

        # calc fatality and non-fatal crash costs and risk values
        base_fatality_costs = dict_of_values[base_key][settings.fatality_costs]
        delta_fatality_costs = dict_of_values[key][settings.fatality_costs] - base_fatality_costs

        base_fatality_risk_value = dict_of_values[base_key][settings.fatality_risk_value]
        delta_fatality_risk_value = dict_of_values[key][settings.fatality_risk_value] - base_fatality_risk_value

        base_nonfatal_crash_costs = dict_of_values[base_key][settings.non_fatal_crash_costs]
        delta_nonfatal_crash_costs = dict_of_values[key][settings.non_fatal_crash_costs] - base_nonfatal_crash_costs

        base_nonfatal_crash_risk_value = dict_of_values[base_key][settings.non_fatal_crash_risk_value]
        delta_nonfatal_crash_risk_value = dict_of_values[key][settings.non_fatal_crash_risk_value] - base_nonfatal_crash_risk_value

        fatality_cost_net = delta_fatality_costs - delta_fatality_risk_value
        nonfatal_cost_net = delta_nonfatal_crash_costs - delta_nonfatal_crash_risk_value

        social_costs = social_costs + fatality_cost_net + nonfatal_cost_net
        delta_dict.update({'FatalityCosts_Net': fatality_cost_net,
                           'Non-FatalCrashCosts_Net': nonfatal_cost_net,
                           'TotalSocialCosts': social_costs})

        # delta_dict.update({'TotalSocialCosts': social_costs})

        # calc non-emission social benefits (some are treated as costs or negative benefits)
        base_drive_value = dict_of_values[base_key][settings.drive_value]
        # delta_drive_value = dict_of_values[key][settings.drive_value] - base_drive_value
        drive_value_benefit = dict_of_values[key][settings.drive_value] - base_drive_value

        base_refueling_time_cost = dict_of_values[base_key][settings.refueling_time_cost]
        # delta_refueling_time_cost = dict_of_values[key][settings.refueling_time_cost] - base_refueling_time_cost
        refueling_time_savings = base_refueling_time_cost - dict_of_values[key][settings.refueling_time_cost]

        # base_fatality_risk_value = dict_of_values[base_key][settings.fatality_risk_value]
        # delta_fatality_risk_value = dict_of_values[key][settings.fatality_risk_value] - base_fatality_risk_value
        #
        # base_non_fatal_crash_risk_value = dict_of_values[base_key][settings.non_fatal_crash_risk_value]
        # delta_non_fatal_crash_risk_value = dict_of_values[key][settings.non_fatal_crash_risk_value] - base_non_fatal_crash_risk_value

        base_petrol_market_externalities = dict_of_values[base_key][settings.petrol_market_externalities]
        # delta_petrol_market_externalities = dict_of_values[key][settings.petrol_market_externalities] - base_petrol_market_externalities
        energy_security_benefits = base_petrol_market_externalities - dict_of_values[key][settings.petrol_market_externalities]

        # non_emission_social_benefits = delta_drive_value - delta_refueling_time_cost + delta_fatality_risk_value \
        #                                + delta_non_fatal_crash_risk_value - delta_petrol_market_externalities
        non_emission_social_benefits = drive_value_benefit + refueling_time_savings + energy_security_benefits
        delta_dict.update({'NonEmissionBenefits': non_emission_social_benefits})

        # calc benefits from reduced pollution and add the non-emission social benefits then calc net benefits
        for arg_criteria in settings.social_criteria_benefit_args:
            base_arg_value = dict_of_values[base_key][arg_criteria]
            delta_arg_criteria = dict_of_values[key][arg_criteria] - base_arg_value

            for arg_scc in settings.social_scc_benefit_args:
                base_arg_value = dict_of_values[base_key][arg_scc]
                delta_arg_scc = dict_of_values[key][arg_scc] - base_arg_value
                benefits = non_emission_social_benefits - delta_arg_criteria - delta_arg_scc
                delta_dict.update({f'TotalSocialBenefits_{arg_criteria}_{arg_scc}': benefits})
                delta_dict.update({f'NetSocialBenefits_{arg_criteria}_{arg_scc}': fuel_savings + benefits - social_costs})
        dict_of_values[key].update(delta_dict)

    return dict_of_values


if __name__ == '__main__':
    print('This module does not run as a script.')
