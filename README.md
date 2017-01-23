# sci-business-classes

This repository contains scripts and data files used for defining the 
Spatially Business Classification (SBC) system and for relating it to SIC and
NAICS 2017 systems.

There are two distinct groups of files / scripts in this directory. 

## Group 1: NAICS 2017 to SBC mapping

Input files:
* `n17_original.csv`: The original file defining the NAICS 2017 codes
* `n17_flat.csv`: A flattened version of `n17_original.csv`
* `n17_flat_tagged.csv`: A manually marked-up version of `n17_flat.csv`. The extra information that has been added to this
file is understood by the script `z_map_n17_to_sbc.py`.

Scripts:
* `z_map_n17_to_sbc.py`: The script that creates the actual look-up table.

Output files:
* `lookup_n17_sbc.psv`: A mapping between NAICS2017 codes and SBC classes
* `sbc_list.psv`: A full list of the SBC classes

