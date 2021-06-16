Methodology
===========


General
^^^^^^^

The project folder for using the tool should contain an "inputs" folder containing necessary input files and a "tool_code" folder containing the Python modules.
Optionally, a virtual environment folder may be desirable. When running the tool, the user will be asked to provide a run ID. If a run ID is entered, that run ID will be
included in the run-results folder-ID for the given run. Hitting return will use the default run ID. The tool will create an "outputs" folder within the project folder
into which all run results will be saved. A timestamp is included in any run-results folder-ID so that new results never overwrite prior results.


Scenario names in output files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Because many of the model runs done in support of the NPRM involved split fleets (CA framework vs. non-framework OEMs), some scenario names attempt to indicate both the fleet involved and the
standards being met. Scenarios included in the primary runs are shown in Table 1.

Table 1

==============================================  =====================================================
Scenario Name                                   Description
==============================================  =====================================================
2020hold                                        Full fleet meeting the 2020 standards

                                                for 2020+
Safe                                            Full fleet meeting the SAFE FRM standards

                                                through 2026 and thereafter
2012frm                                         Full fleet meeting the 2012 FRM standards
Fw27                                            Full fleet meeting the CA FW 2.7%

                                                year-over-year standards
Framework_Safe                                  FW-OEMs meeting the FW; NonFW-OEMs meeting

                                                SAFE
Fw-To-Proposal_Safe-To-Proposal                 FW-OEMs meeting the FW thru 2022 then

                                                the Proposalfor 2023+; NonFW-OEMs meeting

                                                SAFE thru 2022 then the Proposal for 2023+
Fw-To-Proposal_Safe-To-Proposal-No-Mult         FW-OEMs meeting the FW thru 2022 then

                                                the Proposal for 2023+; NonFW-OEMs

                                                meeting SAFE thru 2022 then the Proposal

                                                for 2023+ (no multipliers in these runs)
Framework-To-Alternative1_Safe-To-Alternative1  FW-OEMs meeting the FW thru 2022 then

                                                Alternative 1 for 2023+; NonFW-OEMs meeting

                                                SAFE thru 2022 then Alternative 1 for 2023+
Framework-To-Alternative2_Safe-To-Alternative2  FW-OEMs meeting the FW thru 2022 then

                                                Alternative 1 for 2023+; NonFW-OEMs meeting

                                                SAFE thru 2022 then Alternative 1 for 2023+
Safe-To-Proposal                                Full fleet meeting SAFE thru 2022 then

                                                the Proposal for 2023+
Safe-To-Alternative1                            Full fleet meeting SAFE thru 2022 then

                                                Alternative 1 for 2023+
Safe-To-Alternative2                            Full fleet meeting SAFE thru 2022 then

                                                Alternative 2 for 2023+
Safe-To-Proposal-No-Mult                        Full fleet meeting SAFE thru 2022 then

                                                the Proposal for 2023+ (no multipliers)
==============================================  =====================================================


Calculations and Equations
^^^^^^^^^^^^^^^^^^^^^^^^^^

This is not meant to be an exhaustive list of all equations used in the tool, but rather a list of those that are considered to be of most interest. The associated draft Regulatory Impact Analysis (RIA)
also contains explanations of calculations made.

Total social costs, social benefits and net social benefits
-----------------------------------------------------------

New parameters calculated within each scenario
..............................................

The following parameters are unique to the tool and represent a different accounting process compared to that followed internal to the CCEMS model. The above parameters calculate net results of fatality
costs with fatality risk values and non-fatal crash costs with non-fatal crash risk values. These net valuations are included as costs in the tool's accounting. These calculations are done for each
scenario and within each scenario. The equations shown below (equations :math:numref:`fc_net` and :math:numref:`nfc_net`) illustrate the calculations used in the tool.

- FatalityCosts_Net
- NonFatalCrashCosts_Net

The following criteria and GHG parameters are unique to the tool and are calculated consistent with CCEMS (tons * cost/ton) but include more granularity and all GHG valuations simultaneously.

- PM25_Costs_tailpipe_3.0
- PM25_Costs_upstream_3.0
- NOx_Costs_tailpipe_3.0
- NOx_Costs_upstream_3.0
- SO2_Costs_tailpipe_3.0
- SO2_Costs_upstream_3.0
- PM25_Costs_tailpipe_7.0
- PM25_Costs_upstream_7.0
- NOx_Costs_tailpipe_7.0
- NOx_Costs_upstream_7.0
- SO2_Costs_tailpipe_7.0
- SO2_Costs_upstream_7.0
- Criteria_Costs_tailpipe_3.0
- Criteria_Costs_upstream_3.0
- Criteria_Costs_tailpipe_7.0
- Criteria_Costs_upstream_7.0
- Criteria_Costs_3.0
- Criteria_Costs_7.0
- CO2_Costs_5.0
- CO2_Costs_3.0
- CO2_Costs_2.5
- CO2_Costs_3.0_95
- CH4_Costs_5.0
- CH4_Costs_3.0
- CH4_Costs_2.5
- CH4_Costs_3.0_95
- N2O_Costs_5.0
- N2O_Costs_3.0
- N2O_Costs_2.5
- N2O_Costs_3.0_95
- GHG_Costs_5.0
- GHG_Costs_3.0
- GHG_Costs_2.5
- GHG_Costs_3.0_95

FatalityCosts_Net
*****************

This is a new parameter that is included in the cost and cost summary reports of the tool.

.. math::
    :label: fc_net

    & FatalityCostsNet

    & =\small(FatalityCosts - FatalityRiskValue)

NonFatalCrashCosts_Net
**********************

This is a new parameter that is included in the cost and cost summary reports of the tool.

.. math::
    :label: nfc_net

    & NonFatalCrashCostsNet

    & =\small(NonFatalCrashCosts - NonFatalCrashRiskValue)


New or revised parameters calculated relative to a base scenario
................................................................

The CCEMS calculates, internal to CCEMS, terms referred to as "Total Social Benefits," "Total Social Costs" and "Net Social Benefits." The tool characterizes some parameters differently than does
the CCEMS and also introduces some new parameters not included in the CCEMS calculations. All of these parameters are calculated relative to a base-case scenario as set in the SetInputs class.
The current setting is "2020hold" and, as such, the following parameters are all calculated relative to that base scenario.

- TotalCosts
- FuelSavings
- NonEmissionBenefits
- TotalBenefits_Criteria_Costs_3.0_GHG_Costs_5.0
- NetBenefits_Criteria_Costs_3.0_GHG_Costs_5.0
- TotalBenefits_Criteria_Costs_3.0_GHG_Costs_3.0
- NetBenefits_Criteria_Costs_3.0_GHG_Costs_3.0
- TotalBenefits_Criteria_Costs_3.0_GHG_Costs_2.5
- NetBenefits_Criteria_Costs_3.0_GHG_Costs_2.5
- TotalBenefits_Criteria_Costs_3.0_GHG_Costs_3.0_95
- NetBenefits_Criteria_Costs_3.0_GHG_Costs_3.0_95
- TotalBenefits_Criteria_Costs_7.0_GHG_Costs_5.0
- NetBenefits_Criteria_Costs_7.0_GHG_Costs_5.0
- TotalBenefits_Criteria_Costs_7.0_GHG_Costs_3.0
- NetBenefits_Criteria_Costs_7.0_GHG_Costs_3.0
- TotalBenefits_Criteria_Costs_7.0_GHG_Costs_2.5
- NetBenefits_Criteria_Costs_7.0_GHG_Costs_2.5
- TotalBenefits_Criteria_Costs_7.0_GHG_Costs_3.0_95
- NetBenefits_Criteria_Costs_7.0_GHG_Costs_3.0_95

The base scenario is used only for the purpose of calculating the above parameters relative to a common scenario. As such, the reporting of these parameters in the tool's output files should not
be seen as absolute valuations. Instead, these parameters are relative to the base scenario (default="202hold") which allows for calculation of incremental results relative to any scenario in the
output files. For example, in the NPRM analysis, the no action case is comprised of CA framework OEMs meeting the framework while non-framework OEMs meet the SAFE FRM ("Framework_Safe"). The action
case is comprised of framework OEMs meeting the framework and then meeting the proposal for 2023 and later while non-framework OEMs meet SAFE standards and then the proposal for 2023 and later
("Fw-To-Proposal_Safe-To-Proposal"). These two scenarios should be chosen carefully from the output files to calculate any incremental costs, benefits and net benefits of the proposal relative to
the no action case.


Total Costs
***********

This is a new parameter that is included in the cost and cost summary reports of the tool. The Total Costs are calculated as shown in equation :math:numref:`costs`.

.. math::
    :label: costs

    & TotalCosts

    & =\small(ForegoneConsumerSalesSurplus_{Action} - ForegoneConsumerSalesSurplus_{NoAction})

    & + \small(TechCost_{Action} - TechCost_{NoAction})

    & + \small(Maint/RepairCost_{Action} - Maint/RepairCost_{NoAction})

    & + \small(CongestionCosts_{Action} - CongestionCosts_{NoAction})

    & + \small(NoiseCosts_{Action} - NoiseCosts_{NoAction})

    & + \small(FatalityCostsNet_{Action} - FatalityCostsNet_{NoAction})

    & + \small(NonFatalCrashCostsNet_{Action} - NonFatalCrashCostsNet_{NoAction})

where FatalityCostsNet if from equation :math:numref:`fc_net` and NonFatalCrashCostsNet is from equation :math:numref:`nfc_net`.

Fuel Savings
************

This is a new parameter that is included in the cost and cost summary reports of the tool. The fuel savings are calculated as shown in equation :math:numref:`fuel`.

.. math::
    :label: fuel

    & FuelSavings

    & = \small(RetailFuelOutlay_{NoAction} - RetailFuelOutlay_{Action})

    & - \small(FuelTaxRevenue_{NoAction} - FuelTaxRevenue_{Action})


Refueling Time Savings
**********************

This is a parameter calculated internal to the tool only for inclusion in the NonEmissionBenefits. Note that the CCEMS calculates a Refueling Time Cost which is included in the tool's output files.

.. math::
    :label: refuel

    & RefuelingTimeSavings

    & = \small(RefuelingTimeCosts_{NoAction} - RefuelingTimeCosts_{Action})


Energy Security Benefits
************************

This is a parameter calculated internal to the tool only for inclusion in the NonEmissionBenefits. Note that the CCEMs calculates Petroleum Market Externalities which is included in the tool's output files.

.. math::
    :label: energy_sec

    & EnergySecurityBenefits

    & = \small(PetroleumMarketExternalities_{NoAction} - PetroleumMarketExternalities_{Action})


Non-Emission Benefits
*********************

The non-emission-related benefits are calculated as shown in equation :math:numref:`non_emission_benefits`.

.. math::
    :label: non_emission_benefits

    & NonEmissionBenefits

    & = \small(DriveValue_{Action} - DriveValue_{NoAction})

    & + \small(RefuelingTimeSavings + EnergySecurityBenefits)

where RefuelingTimeSavings is from equation :math:numref:`refuel` and EnergySecurityBenefits is from equation :math:numref:`energy_sec`. The DriveValue is calculated internal to CCEMS.

Emission Benefits
*****************

Costs for each pollutant are calculated using the inventory for each pollutant multiplied by the appropriate benefit per ton values (for criteria pollutants) or social cost of GHG values (for GHGs).
The Criteria_Costs and GHG_Costs shown in the above list of parameters are summations within the appropriate internal rate of return stream (that is, 2.5% valuations sum only with 2.5% values, etc.)
While criteria pollutants upstream and tailpipe are monetized separately, the GHG pollutants are not. These costs are included in the tool's output files. The benefits for each pollutant are not
included in the output files and are calculated internal to the tool for inclusion in the Total Benefits and Net Benefits calculations. The benefits for each pollutant and internal discount rate,
are calculated as shown in equation :math:numref:`emission_benefits`.

.. math::
    :label: emission_benefits

    & EmissionBenefit_{Pollutant;InternalDiscountRate}

    & = cost/ton * \small(tons_{Pollutant;InternalDiscountRate;Action} - tons_{Pollutant;InternalDiscountRate;NoAction})

Total Benefits
**************

The total benefits are calculated as shown in equation :math:numref:`total_benefits`.

.. math::
    :label: total_benefits

    & TotalBenefits

    & = \small(NonEmissionBenefits + CriteriaEmissionBenefits + SCGHGEmissionBenefits)

where NonEmissionBenefits is from equation :math:numref:`non_emission_benefits` and EmissionBenefits are from equation :math:numref:`emission_benefits`.

Net Benefits
************

The net benefits are calculated as shown in equation :math:numref:`net_benefits`.

.. math::
    :label: net_benefits

    & NetBenefits

    & = \small(FuelSavings + TotalBenefits - TotalCosts)

where FuelSavings is from equation :math:numref:`fuel`, TotalBenefits is from equation :math:numref:`total_benefits` and TotalCosts is from equation :math:numref:`costs`.

Discounting
-----------

Monetized values are discounted at the social discount rates entered in the SetInputs class. The default values are 3% and 7%. Values are discounted to the year entered
in the SetInputs class. The default value is 2021. Monetized values are discounted assuming costs occur at the beginning of the year or the end of the year as entered in
the SetInputs class. The default value is "end-year", meaning that any monetized values in 2021 are discounted.

Importantly, all emission-related monetized values are discounted at their internal rates of return, regardless of the social discount rate. The internal rate of return
is indicated in the cost-factor input files (cost_factors-criteria.csv and cost_factors-scc.csv) in the heading (e.g., values using the "co2_global_5.0_USD_per_metricton"
cost factor will always be discounted at 5%, regardless of the social discount rate).


Present value
.............

.. math::
    :label: pv

    PV=\frac{AnnualValue_{0}} {(1+rate)^{(0+offset)}}+\frac{AnnualValue_{1}} {(1+rate)^{(1+offset)}} + ⋯ +\frac{AnnualValue_{n}} {(1+rate)^{(n+offset)}}

where,

- *PV* = present value
- *AnnualValue* = annual costs or annual benefits or annual net of costs and benefits
- *rate* = discount rate
- *0, 1, …, n* = the period or years of discounting
- *offset* = controller to set the discounting approach (0 means first costs occur at time=0; 1 means costs occur at time=1)

Note that the output files of present values are cumulative sums. Therefore, the results represent present values through the indicated year.


Annualized value
................

When the present value offset in equation :math:numref:`pv` equals 0:

.. math::
    :label:

    AV=PV\times\frac{rate\times(1+rate)^{n}} {(1+rate)^{(n+1)}-1}

When the present value offset in equation :math:numref:`pv` equals 1:

.. math::
    :label:

    AV=PV\times\frac{rate\times(1+rate)^{n}} {(1+rate)^{n}-1}

where,

- *AV* = annualized value of costs or benefits or net of costs and benefits
- *PV* = present value of costs or benefits or net of costs and benefits
- *rate* = discount rate
- *n* = the number of periods over which to annualize the present value

Note that the output files of annualized values represent values annualized through the given year.
