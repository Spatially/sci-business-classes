#
# This script creates a lookup table that maps NAICS 2017 codes into the Spatially business classes.
#
# This script also does a lot of re-naming of the NAICS class labels. That's the main purpose of the
# big lookup table defined below.
#
# in:
# * n17_flat_tagged.csv: A amnually created file that marks up the NAICS 2017 codes with information on how
# we plan to map them into our business classes.
#
# out: lookup_n17_sbc.psv
#


import re
import csv


bc1Lookup = {
    'ret': '01: Retail',
    'eat': '02: Food and Drink',
    'pers': '03: Consumer Services',
    'ae': '04: Arts and Entertainment',
    'health': '05: Health Care',
    'edu': '06: Education',
    'prof': '07: Professional',
    'fin': '08: Finance and Insurance',
    'admin': '09: Administration',
    'govt': '10: Government',
    'soc': '11: Civic Organizations',
    'whol': '12: Wholesale',
    'indus': '13: Industry',
    'agri': '14: Agriculture and Mining',
    'oth': '15: Other',
}


renameLookup = {
    'Technical and Trade Schools': 'Vocational Schools',
    'RV Parks and Recreational Camps': 'Recreational Camps',
    'Snack and Nonalcoholic Beverage Bars': 'Coffee Shops and Snacks',
    'Other Electronic and Precision Equipment Repair and Maintenance': 'Other Electronic Equipment Repair',
    'Professional and Management Development Training': 'Professional Development Training',
    'Chemical and Allied Products Merchant Wholesalers': 'Chemical Products Merchant Wholesalers',
    'Miscellaneous Nondurable Goods Merchant Wholesalers': 'Miscellaneous Wholesalers',
    'Miscellaneous Durable Goods Merchant Wholesalers': 'Miscellaneous Wholesalers',
    'Hardware, and Plumbing and Heating Equipment and Supplies Merchant Wholesalers': 'Hardware Wholesalers',
    'American Indian and Alaska Native Tribal Governments': 'American Native Tribal Governments',
    'Securities and Commodity Exchanges': 'Securities and Commodities',
    'Other Depository Credit Intermediation': 'Other Banking and Savings',
    'Wired and Wireless Telecommunications Carriers': 'Telecommunications Carriers',
    'Data Processing, Hosting, and Related Services': 'Data Processing and Related Services',
    'Colleges, Universities, and Professional Schools': 'Colleges and Professional Schools',
    'Offices of Physical, Occupational and Speech Therapists, and Audiologists':
        'Offices of Other Health Practitioners',
    'Nature Parks and Other Similar Institutions': 'Nature Parks',
    'Other Electronic and Precision Equipment Repair': 'Other Electronic Equipment Repair',
    'Coin-Operated Laundries and Drycleaners': 'Coin-Operated Laundries',
    'Other Automotive Mechanical and Electrical Repair': 'Other Automotive Repair',
    'Motorcycle, ATV, and Other Motor Vehicle Dealers': 'Motorcycle and Other Motor Vehicle Dealers',
    'Cosmetics, Beauty Supplies, and Perfume Stores': 'Cosmetics and Beauty Supply Stores',
    "Children's and Infants' Clothing Stores": "Children's Clothing Stores",
    'Cafeterias, Grill Buffets, and Buffets': 'Cafeterias and Buffets',
    'Sewing, Needlework, and Piece Goods Stores': 'Sewing Supply Stores',
    'Office Supplies and Stationery Stores': 'Office Supply Stores',
    'Gift, Novelty, and Souvenir Stores': 'Gift Stores',
    'Lawn and Garden Equipment Stores': 'Lawn and Garden Stores',
    'Miscellaneous Store Retailers': 'Miscellaneous Retail',
    'Jewelry, Luggage, and Leather Goods Stores': 'Miscellaneous Retail',
    'Health and Personal Care Stores': 'Health and Wellness',
    'Other Direct Selling Establishments': 'Direct Sellers',
    'News Dealers and Newsstands': 'News Stands',
    'Automobile Dealers': 'Car Dealers',
    'Mining (except Oil and Gas)': 'Mining',
    'Beer, Wine, and Liquor Stores': 'Liquor Stores',
    'Agents and Managers for Artists, Athletes, Entertainers, and Other Public Figures': 'Arts Agents and Managers',
    'Promoters of Performing Arts, Sports, and Similar Events': 'Promoters',
    'Promoters of Performing Arts, Sports, and Similar Events with Facilities': 'Facility Event Promoters',
    'Promoters of Performing Arts, Sports, and Similar Events without Facilities': 'Non-facility Event Promoters',
    'Commercial and Industrial Machinery and Equipment (except Automotive and Electronic) Repair and Maintenance':
        'Industrial Machinery Repair and Maintenance',
    'Continuing Care Retirement Communities and Assisted Living Facilities for the Elderly': 'Elderly Care Facilities',
    'General Merchandise Stores, including Warehouse Clubs and Supercenters': 'General Merchandise Stores',
    'Business, Professional, Labor, Political, and Similar Organizations':
        'Professional and Political Organizations',
    'Automotive Parts, Accessories, and Tire Stores': 'Auto Parts',
    'Building Material and Supplies Dealers': 'Building Materials',
    'Direct Selling Establishments': 'Direct Sellers',
    'Electronic Shopping and Mail-Order Houses': 'Electronic and Mail-Order Shopping',
    'General Merchandise Stores': 'General Merchandise',
    'Other Miscellaneous Store Retailers': 'Miscellaneous Retail',
    'Sporting Goods, Hobby, and Musical Instrument Stores': 'Miscellaneous Retail',
    'Commercial and Industrial Machinery and Equipment Repair': 'Commercial Equipment Repair',
    'Drycleaning and Laundry Services': 'Drycleaning and Laundry',
    'Electronic and Precision Equipment Repair and Maintenance': 'Electronic Equipment Repair',
    'Personal and Household Goods Repair and Maintenance': 'Personal Goods Repair',
    "Rooming and Boarding Houses, Dormitories, and Workers' Camps": 'Boarding Houses and Dormitories',
    'Independent Artists, Writers, and Performers': 'Independent Artists',
    'Museums, Historical Sites, and Similar Institutions': 'Museums and Parks',
    'Other Amusement and Recreation Industries': 'Other Amusement and Recreation',
    'All Other Amusement and Recreation Industries': 'All Other Amusement and Recreation',
    'Bowling Centers': 'Bowling',
    'Fitness and Recreational Sports Centers': 'Fitness and Recreational Sports',
    'Ambulatory Health Care Services': 'General Health Care',
    'All Other Ambulatory Health Care Services': 'Other General Health Care',
    'Nursing and Residential Care Facilities': 'Residential Care Facilities',
    'Residential Intellectual and Developmental Disability Facilities': 'Developmental Disability Facilities',
    'Residential Mental Health and Substance Abuse Facilities': 'Mental Health and Substance Abuse Facilities',
    'Business Schools and Computer and Management Training': 'Vocational Schools',
    'Other Schools and Instruction': 'Instructional Schools',
    'Newspaper, Periodical, Book, and Directory Publishers': 'Publishers',
    'Lessors of Nonfinancial Intangible Assets (except Copyrighted Works)': 'Rental and Leasing',
    'Professional, Scientific, and Technical Services': 'Professional Services',
    'Other Professional, Scientific, and Technical Services': 'Other Professional Services',
    'Lessors of Real Estate': 'Real Estate Rental and Leasing',
    'Offices of Real Estate Agents and Brokers': 'Real Estate Agents and Brokers',
    'Rental and Leasing Services': 'Rental and Leasing',
    'Commercial and Industrial Machinery and Equipment Rental and Leasing': 'Commercial Equipment Rental and Leasing',
    'Activities Related to Credit Intermediation': 'Credit Services',
    'Financial Transactions Processing, Reserve, and Clearinghouse Activities': 'Financial Transactions',
    'Mortgage and Nonmortgage Loan Brokers': 'Loan Brokers',
    'Other Activities Related to Credit Intermediation': 'Other Credit Services',
    'Depository Credit Intermediation': 'Banking and Savings',
    'Direct Life, Health, and Medical Insurance Carriers': 'Life, Health, and Medical Insurance',
    'Monetary Authorities-Central Bank': 'Central Bank',
    'Nondepository Credit Services': 'Credit Services',
    'Other Nondepository Credit Intermediation': 'Other Credit Services',
    'Other Financial Investment Activities': 'Other Financial Activities',
    'All Other Financial Investment Activities': 'All Other Financial Activities',
    'Securities and Commodity Contracts Intermediation and Brokerage': 'Securities and Commodities',
    'Administration of Economic Programs': 'Economic Programs',
    'Administration of Environmental Quality Programs': 'Environmental Quality Programs',
    'Administration of Housing Programs, Urban Planning, and Community Development':
        'Urban Planning and Community Development',
    'Administration of Urban Planning and Community and Rural Development':
        'Administration of Urban Planning and Community Development',
    'Administration of Human Resource Programs': 'Human Resource Programs',
    'Executive, Legislative, and Other General Government Support': 'General Government',
    'Justice, Public Order, and Safety Activities': 'Justice and Public Order',
    'Other Justice, Public Order, and Safety Activities': 'Other Justice and Public Order Activities',
    'Grantmaking and Giving Services': 'Charitable Services',
    'Other Grantmaking and Giving Services': 'Other Charitable Services',
    'Social Advocacy Organizations': 'Social Advocacy',
    'Services for the Elderly and Persons with Disabilities': 'Services for the Elderly and Disabled',
    'Beer, Wine, and Distilled Alcoholic Beverage Merchant Wholesalers': 'Alcoholic Beverage Wholesalers',
    'Apparel, Piece Goods, and Notions Merchant Wholesalers': 'Apparel Wholesalers',
    'Household Appliances and Electrical and Electronic Goods Merchant Wholesalers': 'Household Appliance Wholesalers',
    'Electrical Apparatus and Equipment, Wiring Supplies, and Related Equipment Merchant Wholesalers':
        'Electrical Equipment Wholesalers',
    'Household Appliances, Electric Housewares, and Consumer Electronics Merchant Wholesalers':
        'Household Appliance Wholesalers',
    'Lumber and Other Construction Materials Merchant Wholesalers': 'Construction Materials Wholesalers',
    'Machinery, Equipment, and Supplies Merchant Wholesalers': 'Machinery Wholesalers',
    'Motor Vehicle and Motor Vehicle Parts and Supplies Merchant Wholesalers':
        'Motor Vehicles and Supplies Wholesalers',
    'Paper and Paper Product Merchant Wholesalers': 'Paper Products Wholesalers',
    'Petroleum and Petroleum Products Merchant Wholesalers': 'Petroleum Products Wholesalers',
    'Professional and Commercial Equipment and Supplies Merchant Wholesalers': 'Commercial Equipment Wholesalers',
    'Wholesale Electronic Markets and Agents and Brokers': 'Wholesale Agents and Brokers',
    'Electrical Equipment, Appliance, and Component Manufacturing': 'Electrical Equipment and Appliance Manufacturing',
    'Support Activities for Agriculture and Forestry': 'Support for Agriculture',
    'Waste Management and Remediation Services': 'Waste Management',
    'Animal Production and Aquaculture': 'Livestock and Aquaculture',
    'Administrative and Support Services': 'Administrative Support',
    'Management of Companies and Enterprises': 'Management of Companies',
    'Remediation and Other Waste Management Services': 'Other Waste Management Services',
    'Nursery, Garden Center, and Farm Supply Stores': 'Garden and Farm Supply Stores',
    'Restaurants and Other Eating Places': 'Eating Places',
    'Accounting, Tax Preparation, Bookkeeping, and Payroll Services': 'Accounting and Payroll Services',
    'Advertising, Public Relations, and Related Services': 'Advertising and Public Relations',
    'Management, Scientific, and Technical Consulting Services': 'Technical Consulting Services',
    'Agencies, Brokerages, and Other Insurance Related Activities': 'Agencies and Brokerages',
    'Nondepository Credit Intermediation': 'Credit Services',
    'Other Investment Pools and Funds': 'Other Investment Services',
    'Regulation and Administration of Communications, Electric, Gas, and Other Utilities':
        'Administration of Communications and Utilities',
    'Regulation and Administration of Transportation Programs': 'Administration of Transportation Programs',
    'Regulation, Licensing, and Inspection of Miscellaneous Commercial Sectors':
        'Regulation of Miscellaneous Commercial Sectors',
    'Administration of Air and Water Resource and Solid Waste Management Programs':
        'Administration of Waste Management Programs',
    'Labor Unions and Similar Labor Organizations': 'Labor Unions and Similar Organizations',
    'Office Supplies, Stationery, and Gift Stores': 'Office Supplies and Gift Stores',
    'Grocery and Related Product Merchant Wholesalers': 'Grocery Product Wholesalers',
    'Computer and Computer Peripheral Equipment and Software Merchant Wholesalers':
        'Computer and Software Merchant Wholesalers',
}


def fixup(s):

    if s in renameLookup:
        s = renameLookup[s]

    s = re.sub(' \(.*\)', '', s)
    s = re.sub('All Other', 'Other', s)
    s = re.sub('Merchant Wholesalers', 'Wholesalers', s)
    s = re.sub('Electrical and Electronic', 'Electrical', s)
    s = re.sub('Equipment and Supplies', 'Equipment', s)
    s = re.sub('Material and Supplies', 'Material', s)
    s = re.sub('Repair and Maintenance', 'Repair', s)
    return s



set0 = set()
set1 = set()
set2 = set()
codeList = []

# Go through the file that specifies the re-mapping of NAICS codes to Spatially categories.
with open('n17_flat_tagged.csv') as infile:
    reader = csv.DictReader(infile, delimiter=',', quotechar='"')
    for rec in reader:
        code = rec['code']
        bc1 = fixup(bc1Lookup[rec['a']])
        bc2 = fixup(rec['name%s' % rec['b']])
        bc3 = fixup(rec['name%s' % rec['c']])
        codeList.append({'naics2017': code, 'bcid': '00-000-000', 'bc1': bc1, 'bc2': bc2, 'bc3': bc3})
        set0.add(bc1)
        set1.add(bc2)
        set2.add(bc3)

# Make some lookup tables that will map the spatially category names into numeric codes.
code0 = {}
idn = 10
for bc1 in sorted(set0):
    code0[bc1] = '%02d' % idn
    idn += 1

code1 = {}
idn = 100
for bc2 in sorted(set1):
    code1[bc2] = '%02d' % idn
    idn += 1

code2 = {}
idn = 100
for bc3 in sorted(set2):
    code2[bc3] = '%02d' % idn
    idn += 1


# Write the file that maps the NAICS 2017 codes into the Spatially Business Categories.
sbc_list = {}
with open('lookup_n17_sbc.psv', 'w') as outfile:
    fieldnames = ['naics2017', 'bcid', 'bc1', 'bc2', 'bc3']
    writer = csv.DictWriter(outfile, delimiter='|', fieldnames=fieldnames)
    writer.writeheader()

    for rec in codeList:
        rec['bcid'] = '%s-%s-%s' % (code0[rec['bc1']], code1[rec['bc2']], code2[rec['bc3']], )
        rec['bc1'] = re.sub('^.*: ', '', rec['bc1'])
        writer.writerow(rec)

        sbc_list[rec['bcid']] = {'bcid': rec['bcid'], 'bc1': rec['bc1'], 'bc2': rec['bc2'], 'bc3': rec['bc3']}


# Write a file that just lists all of the spatially business categories.
with open('sbc_list.psv', 'w') as outfile:
    fieldnames = ['bcid', 'bc1', 'bc2', 'bc3']
    writer = csv.DictWriter(outfile, delimiter='|', fieldnames=fieldnames)
    writer.writeheader()

    for bcid in sorted(sbc_list.keys()):
        writer.writerow(sbc_list[bcid])
