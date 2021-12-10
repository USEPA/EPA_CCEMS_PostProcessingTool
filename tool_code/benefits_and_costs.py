

def calc_social_impacts(settings, dict_of_values):
    """
    Note:
        The CCEMS calculates, internal to CCEMS, terms referred to as "Total Social Benefits," "Total Social Costs" and "Net Social Benefits." The tool characterizes some parameters differently than does
        the CCEMS and also introduces some new parameters not included in the CCEMS calculations. All of these parameters are calculated relative to a base-case scenario as set in the SetInputs class.
        The current setting is "2020hold" and, as such, the attributes calculated here are all calculated relative to that base scenario.

        The base scenario is used only for the purpose of calculating Benefit-Cost Analysis attributes relative to a common scenario. As such, the reporting of these parameters in this tool's output files should not
        be seen as absolute valuations. Instead, these attributes are relative to the base scenario (default="2020hold") which allows for calculation of incremental results relative to any scenario in the
        output files. For example, in the FRM analysis, the No Action scenario is comprised of CA framework OEMs meeting the framework while non-framework OEMs meet the SAFE FRM. The no action scenario
        contains the keyword "no-action" in the Scenario Name. The action scenario is comprised of framework OEMs meeting the framework and then meeting the final standards for 2023 and later while
        non-framework OEMs meet SAFE standards and then the final standards for 2023 and later. The scenario reflecting the final standards contains the keyword "final" in the Scenario Name.
        These two scenarios should be chosen carefully from the output files to calculate any incremental costs, benefits and net benefits of the final standards (or alternative) relative to the no action case.

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

        # calc social costs (these use action minus base)
        for arg in settings.social_cost_args:
            base_arg_value = dict_of_values[base_key][arg]
            delta_arg = dict_of_values[key][arg] - base_arg_value
            social_costs += delta_arg

        # include consumer surplus as costs (these use base minus action)
        for arg in settings.consumer_surplus_as_cost_args:
            base_arg_value = dict_of_values[base_key][arg]
            delta_arg = base_arg_value - dict_of_values[key][arg]
            social_costs += delta_arg

        # calc fatality/non-fatal crash costs and risk values net (the nets use action minus base)
        base_fatality_costs = dict_of_values[base_key][settings.fatality_costs]
        base_fatality_risk_value = dict_of_values[base_key][settings.fatality_risk_value]
        base_fatality_costs_net = base_fatality_costs - base_fatality_risk_value

        this_fatality_costs = dict_of_values[key][settings.fatality_costs]
        this_fatality_risk_value = dict_of_values[key][settings.fatality_risk_value]
        this_fatality_costs_net = this_fatality_costs - this_fatality_risk_value

        delta_fatality_costs_net = this_fatality_costs_net - base_fatality_costs_net

        base_nonfatal_crash_costs = dict_of_values[base_key][settings.non_fatal_crash_costs]
        base_nonfatal_crash_risk_value = dict_of_values[base_key][settings.non_fatal_crash_risk_value]
        base_nonfatal_crash_costs_net = base_nonfatal_crash_costs - base_nonfatal_crash_risk_value

        this_nonfatal_crash_costs = dict_of_values[key][settings.non_fatal_crash_costs]
        this_nonfatal_crash_risk_value = dict_of_values[key][settings.non_fatal_crash_risk_value]
        this_nonfatal_crash_costs_net = this_nonfatal_crash_costs - this_nonfatal_crash_risk_value

        delta_nonfatal_crash_costs_net = this_nonfatal_crash_costs_net - base_nonfatal_crash_costs_net

        social_costs = social_costs + delta_fatality_costs_net + delta_nonfatal_crash_costs_net

        delta_dict.update({'FatalityCosts_Net': this_fatality_costs_net,
                           'Non-FatalCrashCosts_Net': this_nonfatal_crash_costs_net,
                           'TotalCosts': social_costs})

        # calc non-emission social benefits (some are treated as costs or negative benefits)
        base_drive_value = dict_of_values[base_key][settings.drive_value]
        drive_value_benefit = dict_of_values[key][settings.drive_value] - base_drive_value

        base_refueling_time_cost = dict_of_values[base_key][settings.refueling_time_cost]
        refueling_time_savings = base_refueling_time_cost - dict_of_values[key][settings.refueling_time_cost]

        base_petrol_market_externalities = dict_of_values[base_key][settings.petrol_market_externalities]
        energy_security_benefits = base_petrol_market_externalities - dict_of_values[key][settings.petrol_market_externalities]

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
                delta_dict.update({f'TotalBenefits_{arg_criteria}_{arg_scc}': benefits})
                delta_dict.update({f'NetBenefits_{arg_criteria}_{arg_scc}': fuel_savings + benefits - social_costs})
        dict_of_values[key].update(delta_dict)

    return dict_of_values


if __name__ == '__main__':
    print('This module does not run as a script.')
