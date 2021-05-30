Python scripts to fetch data from the GW100 database and create a script for Q-E.

**NOTE:** All the following require `pw.x` to be in ``$PATH``

# single_converter.py
Generate ``pw.x`` input file using the specified GW100 db configuration

``python single_converter.py ../../GW100/structures/xxx.upf``

# all_converter.py
Generate ``pw.x`` input file *for each* GW100 db file in given path.

``python all_converter.py ../../GW100/structures/``

The generated files are stored in ``./output/``

# all_runner.py
Compute ``pw.x`` for each input file in the given path 

``python all_converter.py ./output/``

Tip: run the program in a temporary directory, such as `tmp`

# all_plotter.py
``python all_plotter.py option <arguments> ``

Possible options:
- ``prepare <path>`` retrieve tot_en, wall time and cpu time from all the ``pw.x`` outputs in the given path.
- `` plot <names> ...`` plot given compounds (en tot vs cutoff). Run ``prepare`` first.
- `` plot_all <path>``  plot all compounds found in path (broken). Run ``prepare`` first.
