#                   name,alpha-2,alpha-3,country-code,iso_3166-2,region,sub-region,
#                   intermediate-region,region-code,sub-region-code,intermediate-region-code

import csv

from assets import *

countries = csv.reader(open("D:/countries.csv"), delimiter=',')

country_dict: dict[str, int] = {}

for index, data in enumerate(countries):
    if index == 0: continue
    print(data)
    # database.cursor.execute(f"insert into Country (name, alpha_2, alpha_3, code, region, sub_region)" ---------- DONE
    # "values (?, ?, ?, ?, ?, ?)", (data[0], data[1], data[2], data[3], data[5], data[6]))
