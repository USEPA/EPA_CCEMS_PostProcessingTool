.. image:: https://www.epa.gov/sites/production/files/2013-06/epa_seal_verysmall.gif


Introduction
============


EPA CCEMS Post-Processing Tool
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

What is the CCEMS post-processing tool?
---------------------------------------

This tool was developed by EPA to post-process runs of the CAFE Compliance and Effects Modeling System (CCEMS, or CAFE model). The post-processing was
needed for two reasons:

    - The fleet was split into two separate fleets each consisting of a subset of the full fleet. The runs for the split fleets had to be brought back together into a full fleet and, as appropriate, some values had to be summed while some had to be sales-weighted.
    - The benefit-cost analysis results for the social cost of GHGs could be post-processed simultaneously for four unique SC-GHG valuation streams rather than requiring four different runs of the CCEMS model.

Note that the splitting of fleets into separate files is not a function of the tool. That was done manually prior to any CCEMS model runs.

What are the input files for the tool?
--------------------------------------

The following files must be located in an inputs folder located within the project directory. These files specify what CCEMS reports to post-process and various values used in-code.

    - general_inputs.csv which provides filenames of what input files to use to establish cost factors and folder names where files used for CCEMS model runs can be found.
    - runtime_settings.csv which specifies what CCEMS output report files to post-process (e.g., compliance_report, technology_utilization report).
    - run_folders_primary (or run_folders_sensitivities) that specify the folder names of CCEMS model runs to process.

There are three cost factor input files that must be located in an inputs folder located within the project directory.

    - a file specifying the criteria emission cost factors ($/US ton); the file to use is set via the general_inputs.csv input file
    - a file specifying the GHG emission cost factors ($/metric ton); the file to use is set via the general_inputs.csv input file
    - a file specifying the energy security cost factors ($/barrel of oil); the file to use is set via the general_inputs.csv input file

There are, of course, any number of CCEMS output files that serve as inputs to the postproc tool. The tool has to be able to locate those output files. Those files should exist in a CAFE_model_runs
folder a level above the tool's project folder.

What are the output files of the tool?
--------------------------------------

The tool saves all output files to a folder unique to the given run of the tool. The user is prompted for a run ID that will be used in the folder name.

The tool creates output files analogous to the following CCEMS output files.

    - societal effects report
    - societal effects summary report
    - societal costs report
    - societal costs summary report
    - compliance report
    - technology utilization report
    - vehicles report

The other CCEMS output files are not included as part of the tool. Note that the vehicles report output file of this tool differs from that of CCEMS. This tool makes use of the CCEMS vehicles report to calculate
year-by-year sales-weighted technology costs for each of the tracked powertrains within the CCEMS vehicles report. This report provides the share of vehicles with each tracked powertrain, the sales-weighted cost
of new tech added to vehicles within that powertrain, and the sales-weighted contribution to the resultant cost per vehicle. In other words, if the added technology cost of all vehicles in a given model year
averages $1000, then 50% of that might consist of conventional powertrains adding $300 per vehicle (or a $150 contribution to the $1000 average) and 50% might consist of start-stop powertrains adding $1700 per vehicle (or a
$850 contribution to the $1000 average). This tool's vehicles report offers a look at such data.

The tool also copies actual CCEMS input and output files into the run folder.

The tool also copies the tool's code into the run folder.


A note about the market files used for the FRM analysis
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For the final analysis, EPA updated the baseline fleet from a MY2017 fleet to a MY2020 based fleet. EPA did this by using the market file developed by NHTSA in their 2021 CAFE NPRM analysis. However,
EPA was using a prior version of CCEMS, that used in the SAFE FRM and EPA's August 2021 NPRM. Some vehicles in the MY2020 baseline fleet would not load properly in the version of CCEMS used by EPA. Specially,
the Mazda vehicles equipped with HCR2 technology would not load. For that reason, EPA coded the engines in those vehicles as having HCR0 technology and then specified in the market file that those engines
could not add HCR1 technology. Since HCR2 technology was not allowed in EPA's primary CCEMS model runs, those Mazda engines were unable to progress from HCR0 to a "better" HCR technology.

Also, some Engine Technology Classes on the vehicles workbook of the market file had to be re-coded since the version of CCEMS used by EPA did not contain code to properly handle the newer engine technology
classifications used by NHTSA in their 2021 NPRM version of the model.

EPA also removed data entered by NHTSA in the ZEV candidate column of data on the vehicles worksheet of the market file since EPA was not using that feature of CCEMS.
