# EPA_CCEMS_PostProcessingTool

This tool was developed by EPA to post-process runs of the CAFE Compliance and Effects Modeling System (CCEMS, or CAFE model). The post-processing was
needed for two reasons:

    - The fleet was split into two separate fleets each consisting of a subset of the full fleet. 
    The runs for the split fleets had to be brought back together into a full fleet and, 
    as appropriate, some values had to be were summed while some had to be sales-weighted.
    - The benefit-cost analysis results for the social cost of GHGs could be post-processed 
    simultaneously for four unique stream of SCGHG valuation streams rather than requiring
    four different runs of the CCEMS model.

Documentation
=============

https://usepaepa-ccems-postprocessingtool.readthedocs.io/
