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

Total social costs, benefits and net benefits
---------------------------------------------

Benefits and costs are calculated relative to a base-case scenario as set in the SetInputs class. The current setting is "2020hold" and, as such, all "Total Social Benefits" and "Total Social Costs"
along with "Net Social Benefits" are calculated relative that scenario. This scenario is used only for that purpose so those total social costs and benefits as output via this tool should not be seen
as absolute valuations. Instead, total costs and total benefits and net benefits should be calculated as increments from an appropriate "No Action" case within the output files. For example, in the
NPRM analysis, the no action case is comprised of CA framework OEMs meeting the framework while non-framework OEMs meet the SAFE FRM ("Framework_Safe"). The action case is comprised of framework OEMs
meeting the framework and then meeting the proposal for 2023 and later while non-framework OEMs meet SAFE standards and then the proposal for 2023 and later ("Fw-To-Proposal_Safe-To-Proposal"). These
two scenarios should be chosen carefully from the output files to calculate any incremental costs, benefits and net benefits of the proposal relative to the no action case.

The tool also adds some calculations that are not part of the CCEMS. Those are FatalityCost_Net, NonFatalCrashCosts_Net.

FatalityCosts_Net
.................

.. math::
    :label: fc_net

    & FatalityCostsNet

    & =\small(FatalityCosts_{Action} - FatalityCosts_{NoAction})

    & - \small(FatalityRiskValue_{Action} - FatalityRiskValue_{NoAction})

NonFatalCrashCosts_Net
......................

.. math::
    :label: nfc_net

    & NonFatalCrashCostsNet

    & =\small(NonFatalCrashCosts_{Action} - NonFatalCrashCosts_{NoAction})

    & - \small(NonFatalCrashRiskValue_{Action} - NonFatalCrashRiskValue_{NoAction})


Total Social Costs
..................

The total social costs are calculated as shown in equation :math:numref:`costs`

.. math::
    :label: costs

    & TotalSocialCosts

    & =\small(ForegoneConsumerSalesSurplus_{Action} - ForegoneConsumerSalesSurplus_{NoAction})

    & + \small(TechCost_{Action} - TechCost_{NoAction})

    & + \small(Maint/RepairCost_{Action} - Maint/RepairCost_{NoAction})

    & + \small(CongestionCosts_{Action} - CongestionCosts_{NoAction})

    & + \small(NoiseCosts_{Action} - NoiseCosts_{NoAction})

    & + \small(FatalityCostsNet_{Action} - FatalityCostsNet_{NoAction})

    & + \small(NonFatalCrashCostsNet_{Action} - NonFatalCrashCostsNet_{NoAction})


Fuel Savings
............

The fuel savings are calculated as shown in equation :math:numref:`fuel`

.. math::
    :label: fuel

    & FuelSavings

    & = \small(RetailFuelOutlay_{NoAction} - RetailFuelOutlay_{Action})

    & - \small(FuelTaxRevenue_{NoAction} - FuelTaxRevenue_{Action})


Refueling Time Savings
......................

Note that the CCEMS calculates a Refueling Time Cost which the tool tracks as a Savings rather than a cost.

.. math::
    :label: refuel

    & RefuelingTimeSavings

    & = \small(RefuelingTimeCosts_{NoAction} - RefuelingTimeCosts_{Action})

Energy Security Benefits
........................

Note that the CCEMs calculates Petroleum Market Externalities which the tool tracks as a Benefit.

.. math::
    :label: energy_sec

    & EnergySecurityBenefits

    & = \small(PetroleumMarketExternalities_{NoAction} - PetroleumMarketExternalities_{Action})

Non-Emission Benefits
......................

The non-emission-related benefits are calculated as shown in equation :math:numref:`non_emission_benefits`

.. math::
    :label: non_emission_benefits

    & NonEmissionBenefits

    & = \small(DriveValue_{Action} - DriveValue_{NoAction})

    & + RefuelingTimeSavings + EnergySecurityBenefits


Total Social Benefits
.....................

The total benefits are calculated as shown in equation :math:numref:`total_benefits`

.. math::
    :label: total_benefits

    TotalSocialBenefits = NonEmissionSocialBenefits

                          + CriteriaEmissionBenefits

                          + SCGHGEmissionBenefits


Net Social Benefits
...................

The net benefits are calculated as shown in equation :math:numref:`net_benefits`

.. math::
    :label: net_benefits

    NetSocialBenefits = FuelSavings + TotalSocialBenefits - TotalSocialCosts


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

    PV=\frac{AnnualValue_{0}} {(1+rate)^{(0+offset)}}+\frac{AnnualValue_{1}} {(1+rate)^{(1+offset)}} +⋯+\frac{AnnualValue_{n}} {(1+rate)^{(n+offset)}}

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
