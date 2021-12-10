Methodology
===========


General
^^^^^^^

The project folder for using this tool should contain an "inputs" folder containing necessary input files and a "tool_code" folder containing the Python modules.
Optionally, a virtual environment folder may be desirable. When running this tool, the user will be asked to provide a run ID. If a run ID is entered, that run ID will be
included in the run-results folder-ID for the given run. Hitting return will use the default run ID. The tool will create an "outputs" folder within the project folder
into which all run results will be saved. A timestamp is included in any run-results folder-ID so that new results never overwrite prior results.


Scenario names in output files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Scenarios included in the primary runs are shown in Table 1.

Table 1

==============================================  =====================================================
Scenario Name                                   Description
==============================================  =====================================================
2020hold                                        Full fleet meeting the 2020 standards

                                                for 2020+
Safe                                            Full fleet meeting the SAFE FRM standards

                                                through 2026 and thereafter
2012frm                                         Full fleet meeting the 2012 FRM standards
0_No-action                                     FW-OEMs meeting the FW; NonFW-OEMs meeting

                                                SAFE
Final                                           FW-OEMs meeting the FW thru 2022 then

                                                the Final standards for 2023+; NonFW-OEMs meeting

                                                SAFE thru 2022 then the Final standards for 2023+
Final_No-mult                                   FW-OEMs meeting the FW thru 2022 then

                                                the Final standards for 2023+; NonFW-OEMs meeting

                                                SAFE thru 2022 then the Final standards for 2023+

                                                but without advanced technology multipliers
Proposal                                        FW-OEMs meeting the FW thru 2022 then the Proposed

                                                standards for 2023+; NonFW-OEMs meeting SAFE thru 2022

                                                then the Proposed standards for 2023+
Alt2-10                                         FW-OEMs meeting the FW thru 2022 then the NPRM's

                                                Alternative 2 minus 10 for 2023+; NonFW-OEMs meeting

                                                SAFE thru 2022 then the NPRM's Alternative 2

                                                minus 10 for 2023+
==============================================  =====================================================


Calculations and Equations
^^^^^^^^^^^^^^^^^^^^^^^^^^

This is not meant to be an exhaustive list of all equations used in this tool, but rather a list of those that are considered to be of most interest. The associated Regulatory Impact Analysis (RIA)
also contains explanations of some of the calculations made.

Off-Cycle Credit Costs, Tech Costs and Reg-Costs
------------------------------------------------

CCEMS can calculate costs associated with off-cycle credits by entering in the scenarios input file a cost for each gram/mile of credit and by entering in the market file the number of grams/mile of
credit each manufacturer is projected to earn or use. However, the version of CCEMS used by EPA does not have the ability to consider off-cycle credit use versus application of other CO2 reducing
technologies. In other words, the credits are applied as stipulated in the market file and their costs are applied as stipulated in the scenarios file. Therefore, accounting for the costs of off-cycle
credits in the model inputs is not necessary and can be post-processed as done by this tool. Doing so requires re-calculation of tech costs and reg-costs that are direct outputs of CCEMS.

Compliance Report
.................

Average Off-Cycle Cost
**********************

.. math::
    :label: avg_oc_credit_cost

    AvgOffCycleCost = OffCycleCredits \times CostPerOffCycleCredit

where,

- :math:`OffCycleCredits` are an output of CCEMS and reflect the inputs set in the market file
- :math:`CostPerOffCycleCredit` is set in the SetInputs class of the tool (EPA's value is $42/gram/mile)

Average Reg-Cost
****************

.. math::
    :label: avg_reg_cost

    & AvgRegCost

    & = \small Avg AC Efficiency Cost + Avg AC Leakage Cost + Avg OffCycle Cost + Avg Tech Cost

where,

- :math:`Avg AC Efficiency Cost` is the Average AC Efficiency Cost and is a direct output of CCEMS
- :math:`Avg AC Leakage Cost` is the Average AC Leakage Cost and is a direct output of CCEMS
- :math:`Avg Tech Cost` is the cost of technology added to achieve compliance and is a direct output of CCEMS
- :math:`Avg OffCycle Cost` is from Equation :eq:`avg_oc_credit_cost`

Off-Cycle Cost
**************

.. math::
    :label: oc_cost

    OffCycleCost = Avg OffCycle Cost \times Sales

where,

- :math:`Sales` is a direct output of CCEMS
- :math:`Avg OffCycle Cost` is from Equation :eq:`avg_oc_credit_cost`

Tech Cost
*********

.. math::
    :label: tech_cost

    Tech Cost = Avg Tech Cost \times Sales

where,

- :math:`Avg Tech Cost` is the average cost of technology added to achieve compliance and is a direct output of CCEMS
- :math:`Sales` is a direct output of CCEMS

Reg-Cost
********

.. math::
    :label: reg_cost

    RegCost = Avg RegCost \times Sales

where,

- :math:`Sales` is a direct output of CCEMS
- :math:`Avg RegCost` is from Equation :eq:`avg_reg_cost`

Annual Societal Costs Summary Report
....................................

The annual societal costs summary report uses the *RegCost* from Equation :eq:`reg_cost` and reported in the Compliance Report, but reports the result as *TechCost* in thousands in the
annual societal costs summary report.

.. math::
    :label: tech_cost_summary_report

    TechCost = \frac{RegCost} {1000}

where,

- :math:`RegCost` is from Equation :eq:`reg_cost`

Annual Societal Costs Report
............................

The annual societal costs report uses the *RegCost* from Equation :eq:`reg_cost` and reported in the Compliance Report, but reports the result as *TechCost* in thousands in the
annual societal cost report and reports that result for *Age* = 0 (i.e., the first year of the model year since costs are taken to be accrued at initial sale).

.. math::
    :label: tech_cost_report

    TechCost = \frac{RegCost} {1000}

where,

- :math:`RegCost` is from Equation :eq:`reg_cost`

Total social costs, social benefits and net social benefits
-----------------------------------------------------------

New or revised parameters calculated within each scenario
.........................................................

The following parameters are unique to this tool and represent a different accounting process compared to that followed internal to the CCEMS model. The above parameters calculate net results of fatality
costs with fatality risk values and non-fatal crash costs with non-fatal crash risk values. These net valuations are included as costs in this tool's accounting. These calculations are done for each
scenario and within each scenario. The equations shown below (Equation :eq:`fc_net` and Equation :eq:`nfc_net`) illustrate the calculations used in this tool.

- FatalityCosts_Net
- NonFatalCrashCosts_Net

The following criteria and GHG parameters are unique to this tool and are calculated consistent with CCEMS (tons * cost/ton) but include more granularity and all GHG valuations simultaneously.

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

This is a new parameter that is included in the cost and cost summary reports of this tool.

.. math::
    :label: fc_net

    FatalityCostsNet = FatalityCosts - FatalityRiskValue

where,

- :math:`FatalityCosts` and :math:`FatalityRiskValue` are direct outputs of CCEMS.

NonFatalCrashCosts_Net
**********************

This is a new parameter that is included in the cost and cost summary reports of this tool.

.. math::
    :label: nfc_net

    NonFatalCrashCostsNet = NonFatalCrashCosts - NonFatalCrashRiskValue

where,

- :math:`NonFatalCrashCosts` and :math:`NonFatalCrashRiskValue` are direct outputs of CCEMS.

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

The base scenario is used only for the purpose of calculating the above parameters relative to a common scenario. As such, the reporting of these parameters in this tool's output files should not
be seen as absolute valuations. Instead, these parameters are relative to the base scenario (default="2020hold") which allows for calculation of incremental results relative to any scenario in the
output files. For example, in the FRM analysis, the No Action scenario is comprised of CA framework OEMs meeting the framework while non-framework OEMs meet the SAFE FRM. The no action scenario
contains the keyword "no-action" in the Scenario Name. The action scenario is comprised of framework OEMs meeting the framework and then meeting the final standards for 2023 and later while
non-framework OEMs meet SAFE standards and then the final standards for 2023 and later. The scenario reflecting the final standards contains the keyword "final" in the Scneario Name.
These two scenarios should be chosen carefully from the output files to calculate any incremental costs, benefits and net benefits of the final standards (or alternative) relative to the no action case.


Total Costs
***********

This is a new parameter that is included in the cost and cost summary reports of this tool. The Total Costs are calculated as shown in Equation :eq:`costs`.

.. math::
    :label: costs

    & TotalCosts

    & =\small(ForegoneConsumerSalesSurplus_{NoAction} - ForegoneConsumerSalesSurplus_{Action})

    & + \small(TechCost_{Action} - TechCost_{NoAction})

    & + \small(Maint/RepairCost_{Action} - Maint/RepairCost_{NoAction})

    & + \small(CongestionCosts_{Action} - CongestionCosts_{NoAction})

    & + \small(NoiseCosts_{Action} - NoiseCosts_{NoAction})

    & + \small(FatalityCostsNet_{Action} - FatalityCostsNet_{NoAction})

    & + \small(NonFatalCrashCostsNet_{Action} - NonFatalCrashCostsNet_{NoAction})

where,

- :math:`FatalityCostsNet` is from Equation :eq:`fc_net`
- :math:`NonFatalCrashCostsNet` is from Equation :eq:`nfc_net`.
- :math:`TechCost` is from Equation :eq:`tech_cost_summary_report` or Equation :eq:`tech_cost_report`
- :math:`ForegoneConsumerSalesSurplus`, :math:`CongestionCost`, :math:`NoiseCost`, :math:`Maint/RepairCost` are direct CCEMS outputs.

Fuel Savings
************

This is a new parameter that is included in the cost and cost summary reports of this tool. The fuel savings are calculated as shown in Equation :eq:`fuel`.

.. math::
    :label: fuel

    & FuelSavings

    & = \small(RetailFuelOutlay_{NoAction} - RetailFuelOutlay_{Action})

    & - \small(FuelTaxRevenue_{NoAction} - FuelTaxRevenue_{Action})

where,

- :math:`RetailFuelOutlay` and :math:`FuelTaxRevenue` are direct outputs of CCEMS.

Refueling Time Savings
**********************

This is a parameter calculated internal to this tool only for inclusion in the NonEmissionBenefits. Note that the CCEMS calculates a Refueling Time Cost which is included in this tool's output files.

.. math::
    :label: refuel

    & RefuelingTimeSavings

    & = \small(RefuelingTimeCosts_{NoAction} - RefuelingTimeCosts_{Action})

where,

- :math:`RefuelingTimeCosts` are direct outputs of CCEMS.

Energy Security Benefits
************************

This is a parameter calculated internal to this tool for inclusion in the NonEmissionBenefits. Note that CCEMS calculates Petroleum Market Externalities using the $/gallon inputs set via the
Economic Inputs worksheet of the parameters input file. However, this tool calculates petroleum market externalities and the tool's output files report the tool's calculations for this attribute.
This tool uses the $/barrel inputs set via the "NT LDV FRM Oil Security Premia.xlsx" input file contained in the inputs folder (the default usage is the 2018 $/barrel column of data). Within
this tool, the following calculations are used to calculate the petroleum market externalities reported in this tool's output files (annual societal costs summary report and/or annual societal
costs report). The calculations below associated with energy security and petroleum market externalities do not treat electricity consumption as a gasoline equivalent fuel.

.. math::
    :label: e0_share

    ShareOfGasolineInRetailFuel = 0.9

where,

- :math:`0.9` reflects the share of pure gasoline in retail gasoline which is 10 percent ethanol
- Note that CCEMS treats all liquid fuel as retail gasoline equivalent. Therefore, kGallon (or, thousand gallons) fuel consumption data reported by CCEMS, whether noted as Gasoline, E85 or Diesel, is understood to be a retail gasoline equivalent fuel.

.. math::
    :label: energy_density_ratio

    EnergyDensityRatio = \small\frac{(BTU/gallon)_{Retail Gasoline}} {(BTU/gallon)_{Oil}} = \frac{114,200} {129,670} = 0.88

where,

- :math:`BTU/gallon` values are from GREET 2017.

The above equations along with the CCEMS reported kGallons of retail gasoline equivalents, allow the calculation of the number of barrels of oil consumed in the given scenario, as follows:

.. math::
    :label: oil_barrels

    & BarrelsOfOil

    & = \small\frac{kGallons \times 1000 \times ShareOfGasolineInRetailFuel \times EnergyDensityRatio} {42}

where,

- :math:`kGallons` = thousand gallons of retail gasoline equivalents and is a direct output of CCEMS
- :math:`1000` converts kGallons to gallons
- :math:`ShareOfGasolineInRetailFuel` is from Equation :eq:`e0_share`
- :math:`EnergyDensityRatio` is from Equation :eq:`energy_density_ratio`
- :math:`42` is the number of gallons of oil in a barrel of oil

From the barrels of oil consumed, this tool calculates the barrels of oil from imports (excluding that from domestic sources), as follows:

.. math::
    :label: imported_oil_barrels

    BarrelsOfImportedOil = BarrelsOfOil \times 0.91

where,

- :math:`0.91` reflects the estimated oil import reduction as percent of total oil demand reduction.
- :math:`BarrelsOfOil` is from Equation :eq:`oil_barrels`

.. math::
    :label: imported_oil_barrels_per_day

    BarrelsOfImportedOilPerDay = \frac{BarrelsOfImportedOil} {365}

where,

- :math:`BarrelsOfImportedOil` is from :eq:`imported_oil_barrels`
- :math:`365` is the number of days in a year

This tool then calculates new petroleum market externalities, as follows:

.. math::
    :label: petrol_market_externalities

    PetroleumMarketExternalities = BarrelsOfImportedOil \times \frac{$} {barrel}

where,

- :math:`BarrelsOfImportedOil` is from Equation :eq:`imported_oil_barrels`
- :math:`$/barrel` is from the Oil Security Premia input file

The energy security benefits can then be calculated as:

.. math::
    :label: energy_sec

    & EnergySecurityBenefits

    & = \small(PetroleumMarketExternalities_{NoAction} - PetroleumMarketExternalities_{Action})

where,

- :math:`PetroleumMarketExternalities` are from Equation :eq:`petrol_market_externalities`

Non-Emission Benefits
*********************

The non-emission-related benefits are calculated as shown in Equation :eq:`non_emission_benefits`.

.. math::
    :label: non_emission_benefits

    & NonEmissionBenefits

    & = \small(DriveValue_{Action} - DriveValue_{NoAction})

    & + \small(RefuelingTimeSavings + EnergySecurityBenefits)

where,

- :math:`RefuelingTimeSavings` is from Equation :eq:`refuel`
- :math:`EnergySecurityBenefits` is from Equation :eq:`energy_sec`
- :math:`DriveValue` is a direct output of CCEMS.

Emission Benefits
*****************

Costs for each pollutant are calculated using the inventory for each pollutant multiplied by the appropriate benefit per ton values (for criteria pollutants) or social cost of GHG values (for GHGs).
The Criteria_Costs and GHG_Costs shown in the above list of parameters are summations within the appropriate discount rate stream (that is, 2.5% valuations sum only with 2.5% values, etc.)
Criteria pollutants from tailpipe, refinery and electricity generating units are monetized separately but are summed within this tool and not reported separately. The summed costs are included in this tool's output files.
The benefits for each pollutant are not included in the output files and are calculated internal to this tool for inclusion in the Total Benefits and Net Benefits calculations. The benefits for each pollutant, and applicable discount rate,
are calculated as shown in Equation :eq:`emission_benefits`. Note that this tool converts criteria air pollutant metric tons (CCEMS default) to US tons and presents US tons in the output files.

.. math::
    :label: emission_benefits

    & EmissionBenefit_{Source;Pollutant;ApplicableDiscountRate}

    & = \small\frac{$} {ton} \times \small(tons_{Source;Pollutant;ApplicableDiscountRate;Action} - tons_{Source;Pollutant;ApplicableDiscountRate;NoAction})

where,

- :math:`$/ton` is from the tool's inputs files and is unique to *Source* and *Pollutant* and *DiscountRate*
- :math:`Source` refers to Refinery, Electric Generating Unit (EGU) or Tailpipe
- Note that the emission benefits are calculated unique to each *Source* but are summed into "tailpipe" and "upstream" categories in the societal cost-related output files of this tool.

Total Benefits
**************

The total benefits are calculated as shown in Equation :eq:`total_benefits`.

.. math::
    :label: total_benefits

    & TotalBenefits

    & = \small(NonEmissionBenefits + CriteriaEmissionBenefits + SCGHGEmissionBenefits)

where,

- :math:`NonEmissionBenefits` are from Equation :eq:`non_emission_benefits`
- :math:`CriteriaEmissionBenefits` and :math:`SCGHGEmissionBenefits` are from Equation :eq:`emission_benefits`.

Net Benefits
************

The net benefits are calculated as shown in Equation :eq:`net_benefits`.

.. math::
    :label: net_benefits

    & NetBenefits

    & = \small(FuelSavings + TotalBenefits - TotalCosts)

where,

- :math:`FuelSavings` are from Equation :eq:`fuel`
- :math:`TotalBenefits` are from Equation :eq:`total_benefits`
- :math:`TotalCosts` are from Equation :eq:`costs`.

Discounting
-----------

Monetized values are discounted at the social discount rates entered in the SetInputs class. The default values are 3% and 7%. Values are discounted to the year entered
in the SetInputs class. The default value is 2021. Monetized values are discounted assuming costs occur at the beginning of the year or the end of the year as entered in
the SetInputs class. The default value is "end-year", meaning that any monetized values in 2021 are discounted.

Importantly, all emission-related monetized values are discounted at their applicable discount rates, regardless of the social discount rate. The applicable discount rate
is indicated in the cost-factor input files (cost_factors-criteria.csv and cost_factors-scc.csv) in the heading (e.g., values using the "co2_global_5.0_USD_per_metricton"
cost factor will always be discounted at 5%, regardless of the social discount rate).


Present value
.............

.. math::
    :label: pv

    PV=\frac{AnnualValue_{0}} {(1+rate)^{(0+offset)}}+\frac{AnnualValue_{1}} {(1+rate)^{(1+offset)}}+\cdots+\frac{AnnualValue_{n}} {(1+rate)^{(n+offset)}}

where,

- :math:`PV` is the present value
- :math:`AnnualValue` is the annual costs or annual benefit or annual net of costs and benefits
- :math:`rate` is the discount rate
- :math:`0, 1, …, n` is the period or years of discounting
- :math:`offset` is the controller to set the discounting approach (0 means first costs occur at time=0; 1 means costs occur at time=1)

Note that the output files of present values are cumulative sums. Therefore, the results represent present values through the indicated year.

Annualized value
................

When the present value offset in Equation :eq:`pv` equals 0:

.. math::
    :label: av_when_pv0

    AV=PV\times\frac{rate\times(1+rate)^{n}} {(1+rate)^{(n+1)}-1}

When the present value offset in Equation :eq:`pv` equals 1:

.. math::
    :label: av_when_pv1

    AV=PV\times\frac{rate\times(1+rate)^{n}} {(1+rate)^{n}-1}

where,

- :math:`AV` is the annualized value of costs or benefits or net of costs and benefits
- :math:`PV` is the present value of costs or benefits or net of costs and benefits
- :math:`rate` is the discount rate
- :math:`n` is the number of periods over which to annualize the present value

Note that the output files of annualized values represent values annualized through the given year.

Vehicles Report Calculations
----------------------------

This tool makes use of the CCEMS vehicles_report.csv direct output file, and makes the calculations described here. This tool then reports the results in the vehicles_report output file
included in the postproc_outputs directory in place of the vehicles_report.csv file reported by CCEMS. The CCEMS vehicles_report.csv reports technology and associated costs added to each vehicle model
in each model year. It also provides information regarding the powertrain of the vehicle after adding new technology. In other words, a "conventional" powertrain vehicle, meaning a liquid-fueled
internal combustion engine (ICE) vehicle with no start-stop and no electrification technologies might add hybridization technology during the course of modeling. That vehicle would be categorized as
having a "conventional" powertrain at the start of modeling and, when converted to hybrid technology, would be categorized as being "SHEV" to indicate that it was now a strong hybrid electric vehicle.
CCEMS includes the following powertrain categories:

- Conventional, i.e., liquid-fueled and lacking any of the following powertrain technologies
- SS12V, i.e., liquid-fueled and including 12 Volt start-stop technology
- BISG, i.e., liquid-fueled and including mild hybrid technology
- SHEV, i.e., liquid-fueled and including strong hybrid technology
- PHEV, i.e., dual-fueled (liquid and electric) plug-in electric vehicle
- BEV, i.e., electricity-fueled battery electric vehicle
- FCV, i.e., fuel-cell vehicle

According to the CCEMS documentation (see DOT HS 812 934, March 2020), "The Vehicles Report contains disaggregate vehicle-level summary of compliance model results, providing a detailed view of the
final state of each vehicle examined by the model, for each model year and scenario analyzed. The report includes basic vehicle characteristics (such as vehicle code, manufacturer, engine and
transmission used, curb weight, footprint, and sales volumes), fuel economy information (before and after the analysis), initial and final technology utilization (via the reported “tech-keys”), and
cost metrics associated with application of additional technology." The documentation also notes that "Tech Costs" as reported in the vehicles_report.csv file represent "Unit costs accumulated by the
vehicle model from technology application in a specific model year."

This tool's vehicles_report provides the following newly calculated data by "Scenario Name", "Model Year" and "Powertrain".

.. math::
    :label: wtd_avg_cost

    SalesWtdAvgCostAdd_{Scenario;ModelYear;Powertrain} = \small\frac{(TechCost \times Sales)_{Scenario;ModelYear;Powertrain}} {Sales_{Scenario;ModelYear;Powertrain}}

where,

- :math:`SalesWtdAvgCostAdd_{Scenario;ModelYear;Powertrain}` is the sales weighted average cost of technology added to vehicles in the given scenario and model year having the given powertrain
- :math:`TechCost_{Scenario;ModelYear;Powertrain}` represents the costs accumulated by any vehicle model adding the given powertrain in the given scenario and model year and is a direct output of CCEMS
- :math:`Sales_{Scenario;ModelYear;Powertrain}` are the final sales of vehicles adding the powertrain technology in the given scenario and model year
- :math:`Sales_{Scenario;ModelYear}` are the final sales of vehicles in the given scenario and model year

.. math::
    :label: powertrain_share

    Share_{Scenario;ModelYear;Powertrain} = \frac{Sales_{Scenario;ModelYear;Powertrain}} {Sales_{Scenario;ModelYear}}

where,

- :math:`Share_{Scenario;ModelYear;Powertrain}` is the share of vehicles within the given scenario and model year having the given powertrain
- :math:`Sales_{Scenario;ModelYear;Powertrain}` are the final sales of vehicles adding the powertrain technology in the given scenario and model year
- :math:`Sales_{Scenario;ModelYear}` are the final sales of vehicles in the given scenario and model year

.. math::
    :label: contribution_to_per_veh_cost

    & ContributionToCostPerVehicle_{Scenario;ModelYear;Powertrain} \\
    & = \small SalesWtdAvgCostAdd_{Scenario;ModelYear;Powertrain} \times Share_{Scenario;ModelYear;Powertrain}

where,

- :math:`ContributionToCostPerVehicle_{Scenario;ModelYear;Powertrain}` represents the contribution of vehicles with the given powertrain to the average cost/vehicle for the given scenario and model year
- :math:`SalesWtdAvgCostAdd_{Scenario;ModelYear;Powertrain}` is from Equation :eq:`wtd_avg_cost`
- :math:`Share_{Scenario;ModelYear;Powertrain}` is from Equation :eq:`powertrain_share`

Compliance Report Calculations
------------------------------

This tool makes use of the CCEMS compliance_report.csv direct output file, and makes the calculations described here.

A 2-cycle CO2 value, in grams per mile CO2, is calculated as:

.. math::
    :label: 2cycle_co2

    CO2_{2cycle} = \frac{8887} {CAFE_{2cycle}}

where,

- :math:`8887` is the CO2 content of gasoline test fuel
- :math:`CAFE_{2cycle}` is a direct output of CCEMS

And a CO2 credit use, or the banked credits used toward compliance, is calculated as:

.. math::
    :label: co2_credit_use

    CO2_{CreditUse} = \small CO2_{2cycle} - CO2_{Rating} - AC_{Efficiency} - AC_{Leakage} - OffCycleCredits

where,

- :math:`CO2_{2cycle}` is from Equation :eq:`2cycle_co2`
- :math:`CO2_{Rating}` is a direct output of CCEMS and represents the achieved, or compliance CO2 value
- :math:`AC_{Efficiency}` and :math:`AC_{Leakage}` are credits associated with air conditioning
- :math:`OffCycleCredits` are the credits earned as part of the off-cycle credit program and are a direct output of CCEMS
