.. image:: https://www.epa.gov/sites/production/files/2013-06/epa_seal_verysmall.gif


Introduction
============


EPA CCEMS postproc_model_runs tool
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

What is the postproc_model_runs tool?
-------------------------------------

This tool was developed by EPA to post-process runs of the CAFE Compliance and Effects Modeling System (CCEMS, or CAFE model). The post-processing was
needed for two reasons:

    - The fleet was split into two separate fleets each consisting of a subset of the full fleet. The runs for the split fleets had to be brought back together into a full fleet and, as appropriate, some values had to be summed while some had to be sales-weighted.
    - The benefit-cost analysis results for the social cost of GHGs could be post-processed simultaneously for four unique stream of SCGHG valuation streams rather than requiring four different runs of the CCEMS model.

Note that the splitting of fleets into separate files is not a function of the tool. That was done manually prior to any CCEMS model runs.

What are the input files for the tool?
______________________________________

There are two cost factor input files that must be located in an inputs folder located within the project directory.

    - cost_factors_criteria.csv which provides $/ton values associated with criteria air pollutant emissions
    - cost_factors_scc.csv which provides $/ton values associated with greenhouse gas emissions

There are, of course, any number of CCEMS output files that serve as inputs to the postproc tool. The tool has to be able to locate those output files.
The location of those files and how those files are meant to be combined has to be controlled, in code, via the SetInputs class in the postproc_setup module.

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

The other CCEMS output files are not included as part of the tool.

The tool also copies actual CCEMS input and output files into the run folder.

The tool also copies the tool's code into the run folder.
