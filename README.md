# sci-business-classes

This repository contains scripts and data files used for defining the 
Spatially Business Classification (SBC) system and for relating it to SIC and
NAICS 2017 systems.

SIC = Standard Industrial Classification. Long-deprecated but still used byt many.

NAICS = North American Industry Classification System: The modern, accepted system for classifying businesses.

psv = pipe-separated value

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


## Group 2: SIC to NAICS 2017 mapping

This group of files / scripts establishes a mapping between SIC codes and NAICS 2017 codes. 
This involves concatenating several look-up table operations.

Input files:

* `lookup_1_sic_n07.psv`: Maps SIC codes to NAICS 2007 codes
* `lookup_2_n07_n12.psv`: Maps NAICS 2007 codes to NAICS 2012 codes
* `lookup_3_n12_n17.psv`: Maps NAICS 2012 codes to NAICS 2017 codes 
* `lookup_sic_n17_fixed.psv`: A manually created file that establishes some otherwise unknown mappings

Scripts:
* `z_combine_lookups.py`: Combines the lookup tables listed above.

Output files:
* `lookup_sic_n17.psv`: Mapping from SIC directly to NAICS 2017.






 