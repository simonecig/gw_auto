Python scripts to fetch data from the GW100 database and create a script for Q-E.

*NOTE:*All the following require pw.x to be in ``$PATH``

# Single converter
Generate ``pw.x`` input file using the specified GW100 db configuration
``python single_converter.py ../../GW100/structures/xxx.upf``

# All converter
Generate ``pw.x`` input file *for each* GW100 db file in given path.
``python all_converter.py ../../GW100/structures/``
The generated files are stored in ``./output/``

# All runner
Compute ``pw.x`` for each input file in the given path 
``python all_converter.py ./output/``
Tip: run the program in a temporary directory 
