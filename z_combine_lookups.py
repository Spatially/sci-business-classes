#
# This script mashes together several lookup tables, yielding one that maps
# Neustar 8-digit SIC codes directly into 2017 NAICS codes.
#
# In:
#   lookup_1_sic_n17.psv
#   lookup_2_n07_n12.psv
#   lookup_3_n12_n17.psv
#
# Out:
#   lookup_sic_n17.psv


import csv


# This one is the original lookup table provided by Neustar for mapping their SIC codes
# to an older version of NAICS. Some of the SIC codes have no matching NAICS code; for those cases
# the NAICS code is given as "NULL". We'll just skip those and deal with them later, possibly manually.
# Also note that some of the NAICS codes in this file have fewer than the standard 6 characters.
# I'll pad these with zeros and hope for the best.
sic_to_n07 = {}
sic_name_lookup = {}
sic_values = set()
n07_values = set()
with open('lookup_1_sic_n07.psv') as infile:
    reader = csv.reader(infile, delimiter='|')
    for rec in reader:
        sic = rec[0]
        name = rec[1]
        n07 = rec[5]
        if n07 != 'NULL':
            if len(n07) == 2:
                n07 = '%s0000' % n07
            elif len(n07) == 3:
                n07 = '%s000' % n07
            elif len(n07) == 4:
                n07 = '%s00' % n07
            elif len(n07) == 5:
                n07 = '%s0' % n07
            sic_to_n07[sic] = n07
            sic_values.add(sic)
            n07_values.add(n07)
        sic_name_lookup[sic] = name


# The next two lookup tables are created by the NAICS organization for mapping the codes between different revisions.
# These file use 6-digit NAICS codes exclusively.
n07_to_n12 = {}
n12_values = set()
with open('lookup_2_n07_n12.psv') as infile:
    reader = csv.reader(infile, delimiter='|')
    header = reader.next()
    for rec in reader:
        n12 = rec[0]
        n07 = rec[2]
        if n07 in n07_values:
            n07_to_n12[n07] = n12
            n12_values.add(n12)
        else:
            print('!!! NAICS 2007 code "%s" not previously read' % n07)


n12_to_n17 = {}
n17_values = set()
with open('lookup_3_n12_n17.psv') as infile:
    reader = csv.reader(infile, delimiter='|')
    header = reader.next()
    for rec in reader:
        n17 = rec[0]
        n12 = rec[2]
        if n12 in n12_values:
            n12_to_n17[n12] = n17
            n17_values.add(n17)
        else:
            print('!!! NAICS 2012 code "%s" not previously read' % n12)


# Read a manually created lookup table that maps SICs directly to NAICS 2017 codes. This one was created for
# all SIC codes for which the mapping is unknown for whatever reason.
alt_sic_to_n17 = {}
with open('lookup_sic_n17_fixed.psv') as infile:
    reader = csv.reader(infile, delimiter='|')
    for rec in reader:
        sic = rec[0]
        n17 = rec[3]
        alt_sic_to_n17[sic] = n17


# # Combine all lookup tables.
sic_to_n17 = {}
nbad = 0
nrec = 0
bad07 = set()
for sic in sic_to_n07:

    nrec += 1
    bad = False
    sic4 = '%s0000' % sic[0:4]
    sic6 = '%s00' % sic[0:6]

    if sic in sic_to_n07:
        n07 = sic_to_n07[sic]
    elif sic6 in sic_to_n07:
        n07 = sic_to_n07[sic6]
    elif sic4 in sic_to_n07:
        n07 = sic_to_n07[sic4]
    else:
        n07 = '0'
        bad = True

    if n07 in n07_to_n12:
        n12 = n07_to_n12[n07]
    else:
        n12 = '0'
        bad = True

    if n12 in n12_to_n17:
        n17 = n12_to_n17[n12]
    else:
        n17 = '0'
        bad = True

    if n17 == '0':
        sic_to_n17[sic] = alt_sic_to_n17[sic]
    else:
        sic_to_n17[sic] = n17


# Write the result.
with open('lookup_sic_n17.psv', 'w') as outfile:
    fieldnames = ['sic', 'sic_name', 'naics2017']
    writer = csv.DictWriter(outfile, delimiter='|', fieldnames=fieldnames)
    writer.writeheader()
    for sic in sic_to_n17:
        n17 = sic_to_n17[sic]
        writer.writerow({'sic': sic, 'sic_name': sic_name_lookup[sic], 'naics2017': n17})

