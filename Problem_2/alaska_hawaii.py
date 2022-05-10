import numpy as np
import pandas as pd
from openpyxl import load_workbook
from matplotlib import pyplot as plt
import re

#takes one of the diseases and makes relevant plots
def plot_disease(disease):
	x_l = []
	y_l = []
	for county_state, info in counties.items():
		x = info.get('Pharmacy_density_sqmi', -1)
		y = info.get(disease, -1)
		if x <= 0  or y <= 0:
			continue
		x_l.append(x)
		y_l.append(y)
		plt.plot(x, y, color='red', linestyle='solid', linewidth = 3, marker='o')
	plt.xlabel("Pharmacies per sq.mi.")
	plt.ylabel(disease + " per 100k")
	plt.title("Pharmacy Density vs. " + disease + " - All States")
	if x_l and y_l:
		plt.plot(np.unique(x_l), np.poly1d(np.polyfit(x_l, y_l, 1))(np.unique(x_l)))
	plt.savefig(disease + '_all.png')
	plt.clf()

	x_l = []
	y_l = []
	for county_state, info in counties.items():
		x = info.get('Pharmacy_density_sqmi', -1)
		y = info.get(disease, -1)
		if x <= 0  or y <= 0 or not bool(re.search('hawaii', county_state)):
			continue
		x_l.append(x)
		y_l.append(y)
		plt.plot(x, y, color='green', linestyle='solid', linewidth = 3, marker='o')
	plt.xlabel("Pharmacies per sq.mi.")
	plt.ylabel(disease + " per 100k")
	plt.title("Pharmacy Density vs. " + disease + " - Hawaii")
	if x_l and y_l:
		plt.plot(np.unique(x_l), np.poly1d(np.polyfit(x_l, y_l, 1))(np.unique(x_l)))
	plt.savefig(disease + '_hawaii.png')
	plt.clf()

	x_l = []
	y_l = []
	for county_state, info in counties.items():
		x = info.get('Pharmacy_density_sqmi', -1)
		y = info.get(disease, -1)
		if x <= 0  or y <= 0 or not bool(re.search('alaska', county_state)):
			continue
		x_l.append(x)
		y_l.append(y)
		plt.plot(x, y, color='blue', linestyle='solid', linewidth = 3, marker='o')
	plt.xlabel("Pharmacies per sq.mi.")
	plt.ylabel(disease + " per 100k")
	plt.title("Pharmacy Density vs. " + disease + " - Alaska")
	if x_l and y_l:
		plt.plot(np.unique(x_l), np.poly1d(np.polyfit(x_l, y_l, 1))(np.unique(x_l)))
	plt.savefig(disease + '_alaska.png')
	plt.clf()


#stores all the info
#counties = {county_state : {Population : ___}, {Pop_density: ___}, etc.}
counties = dict()

#get population, population density, and square mileage of each county
pop_sheet = pd.read_excel('Demography_USA.xlsx', engine='openpyxl', sheet_name='Population')
for index, row in pop_sheet.iterrows():
	county_state = row['County Name'].lower() + '_' + row['STATE_NAME'].lower()
	row[8] = max(row[8], .04) #Density for huge(area) county in Alaska got rounded down to 0 in dataset. .04 is actual value
	counties[county_state] = dict()
	counties[county_state]['Population'] = row[7]
	counties[county_state]['Pop_density'] = row[8]
	counties[county_state]['Sq_mi'] = row[7]/row[8]

#get disease prevalence for each county
dis_sheet = pd.read_excel('Demography_USA.xlsx', engine='openpyxl', sheet_name='Diseases')
for index, row in dis_sheet.iterrows():
	county_state = row['County Name'].lower() + '_' + row['STATE_NAME'].lower()

	counties[county_state]['Obesity'] = row['Prevalence of obesity'] /\
		counties[county_state].get('Population') * 100000

	counties[county_state]['Hypertension'] = row['Hypertension'] /\
		counties[county_state].get('Population') * 100000

	counties[county_state]['Diabetes'] = row['Diabetes'] /\
		counties[county_state].get('Population') * 100000

	counties[county_state]['CVD'] = row['CVD'] /\
		counties[county_state].get('Population') * 100000

	counties[county_state]['HIV'] = row['HIV/AIDS'] /\
		counties[county_state].get('Population') * 100000

#get count of pharmacies for each county
pharmacy_sheets = pd.read_excel('Pharmacy-County.xlsx', engine='openpyxl', sheet_name=None)
for name, sheet in pharmacy_sheets.items():
	for index, row in sheet.iterrows():
		if pd.isna(row['county']):
			continue

		county_state = row['county'].lower() + '_' + row['State'].lower()

		county_state = county_state.replace(' County', '').replace(' county', '')

		counties[county_state]['Pharmacies'] =\
			counties[county_state].get('Pharmacies', 0) + 1

		counties[county_state]['Pharmacy_density_100pop'] = \
			counties[county_state].get('Pharmacies', 0) / \
			counties[county_state].get('Population') * 100000

		counties[county_state]['Pharmacy_density_sqmi'] = \
			counties[county_state].get('Pharmacies', 0) / \
			counties[county_state].get('Sq_mi')


#Plot Population density vs Pharmacy density (area and pop) for All, Alaska, and Hawaii
x_l = []
y_l = []
for county_state, info in counties.items():
	x = info.get('Pop_density', -1)
	y = info.get('Pharmacy_density_100pop', -1)
	if x < 0  or y < 0:
		continue
	x_l.append(x)
	y_l.append(y)
	plt.plot(x, y, color='green', linestyle='solid', linewidth = 3, marker='o')
plt.xlabel("Population Density")
plt.ylabel("Pharmacies per 100k people")
plt.title("Pop Density vs. Pharmacies/100k Pop - All States")
plt.plot(np.unique(x_l), np.poly1d(np.polyfit(x_l, y_l, 1))(np.unique(x_l)))
plt.savefig('pharm_pop_density_all.png')
plt.clf()

x_l = []
y_l = []
for county_state, info in counties.items():
	x = info.get('Pop_density', -1)
	y = info.get('Pharmacy_density_sqmi', -1)
	if x < 0  or y < 0:
		continue
	x_l.append(x)
	y_l.append(y)
	plt.plot(x, y, color='green', linestyle='solid', linewidth = 3, marker='o')
plt.xlabel("Population Density")
plt.ylabel("Pharmacies per sq.mi.")
plt.title("Pop Density vs. Pharmacies/sq.mi. - All States")
plt.plot(np.unique(x_l), np.poly1d(np.polyfit(x_l, y_l, 1))(np.unique(x_l)))
plt.savefig('pharm_area_density_all.png')
plt.clf()


x_l = []
y_l = []
for county_state, info in counties.items():
	x = info.get('Pop_density', -1)
	y = info.get('Pharmacy_density_sqmi', -1)
	if x < 0  or y < 0 or not bool(re.search('alaska', county_state)):
		continue
	x_l.append(x)
	y_l.append(y)
	plt.plot(x, y, color='green', linestyle='solid', linewidth = 3, marker='o')
plt.xlabel("Population Density")
plt.ylabel("Pharmacies per sq.mi.")
plt.title("Pop Density vs. Pharmacies/sq.mi. - Alaska")
plt.plot(np.unique(x_l), np.poly1d(np.polyfit(x_l, y_l, 1))(np.unique(x_l)))
plt.savefig('pharm_area_density_alaska.png')
plt.clf()

x_l = []
y_l = []
for county_state, info in counties.items():
	x = info.get('Pop_density', -1)
	y = info.get('Pharmacy_density_100pop', -1)
	if x < 0  or y < 0 or not bool(re.search('alaska', county_state)):
		continue
	x_l.append(x)
	y_l.append(y)
	plt.plot(x, y, color='green', linestyle='solid', linewidth = 3, marker='o')
plt.xlabel("Population Density")
plt.ylabel("Pharmacies per 100k people")
plt.title("Pop Density vs. Pharmacies/100k Pop - Alaska")
plt.plot(np.unique(x_l), np.poly1d(np.polyfit(x_l, y_l, 1))(np.unique(x_l)))
plt.savefig('pharm_pop_density_alaska.png')
plt.clf()

x_l = []
y_l = []
for county_state, info in counties.items():
	x = info.get('Pop_density', -1)
	y = info.get('Pharmacy_density_100pop', -1)
	if x < 0  or y < 0 or not bool(re.search('hawaii', county_state)):
		continue
	x_l.append(x)
	y_l.append(y)
	plt.plot(x, y, color='green', linestyle='solid', linewidth = 3, marker='o')
plt.xlabel("Population Density")
plt.ylabel("Pharmacies per 100k people")
plt.title("Pop Density vs. Pharmacies/100k Pop - Hawaii")
plt.plot(np.unique(x_l), np.poly1d(np.polyfit(x_l, y_l, 1))(np.unique(x_l)))
plt.savefig('pharm_pop_density_hawaii.png')
plt.clf()

x_l = []
y_l = []
for county_state, info in counties.items():
	x = info.get('Pop_density', -1)
	y = info.get('Pharmacy_density_sqmi', -1)
	if x < 0  or y < 0 or not bool(re.search('hawaii', county_state)):
		continue
	x_l.append(x)
	y_l.append(y)
	plt.plot(x, y, color='green', linestyle='solid', linewidth = 3, marker='o')
plt.xlabel("Population Density")
plt.ylabel("Pharmacies per sq.mi.")
plt.title("Pop Density vs. Pharmacies/sq.mi. - Hawaii")
plt.plot(np.unique(x_l), np.poly1d(np.polyfit(x_l, y_l, 1))(np.unique(x_l)))
plt.savefig('pharm_area_density_hawaii.png')
plt.clf()

#Generate disease plots
plot_disease('Obesity')
plot_disease('Hypertension')
plot_disease('Diabetes')
plot_disease('CVD')
plot_disease('HIV')