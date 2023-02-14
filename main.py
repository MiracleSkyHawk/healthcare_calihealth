import warnings
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

warnings.filterwarnings("ignore")

caliHealthAreasFile = open("CaliHealthCounties.txt", mode='r')
caliHealthAreasList = caliHealthAreasFile.read().splitlines()[1:]
caliHealthAreas = pd.DataFrame({'serviceAreas': caliHealthAreasList})
caliHealthAreas.to_csv('caliHealthAreas.csv')

countiesList = pd.read_csv('CaliforniaZipCodeCounties.csv')
censusData = pd.read_csv('CaliforniaCensusDataByZip.csv')

df_caliHealthCoverage = pd.merge(caliHealthAreas, countiesList, how='inner', left_on='serviceAreas', right_on='county')
df_caliHealthCoverage = pd.merge(df_caliHealthCoverage, censusData, how='inner', left_on='zip',
                                 right_on='Geographic Area Name')

df_caliHealthCoverage.to_csv('CalihealthServiceAreas.csv', index=False)

# The minimum number of vaccine needed
vaccinationSurveyData = pd.read_csv('VaccinationSurveyData.csv')
populationIntention = vaccinationSurveyData['I intend to get vaccinated for COVID-19 when the vaccine becomes '
                                            'available to me. (1-7 scale with 7 being Likely and 1 being '
                                            'Unlikely)'].value_counts().reset_index()
populationIntention.columns = ['likelihood', 'population']
populationIntention['percentagePopulation'] = populationIntention['population'] / populationIntention[
    'population'].sum()
conversionChart = pd.read_excel('Likelihood to Receive Vaccine Conversion Chart.xlsx')
populationIntention = pd.merge(populationIntention,
                               conversionChart,
                               left_on='likelihood',
                               right_on='Self-Reporting Likelihood to Receive a Vaccine (1-7 scale)',
                               how='inner')
vaccinationPercentage = (populationIntention['percentagePopulation'] * populationIntention['Percent Likelihood to '
                                                                                           'Request a Vaccine '
                                                                                           'Appointment'])
vaccinationPercentage = vaccinationPercentage.sum()
totalPopulation = df_caliHealthCoverage['SEX AND AGE!!Total population'].sum()
vaccineNeeded = totalPopulation * vaccinationPercentage
print('The minimum number of vaccine needed is: ' + str(vaccineNeeded))

# Calihealth Facility within service area
calihealthFacility = pd.read_csv('CaliHealthFacilities.csv')
FacilityInServiceArea = pd.merge(caliHealthAreas, calihealthFacility,
                                 how='inner', left_on='serviceAreas', right_on='facility county')
FacilityInServiceArea.to_csv('FacilityInServiceArea.csv', index=False)

FacilityInServiceArea = pd.merge(FacilityInServiceArea, countiesList,
                                 how='inner', left_on='facility zip', right_on='zip')

# Clinic details
ClinicCapacity = pd.read_excel('ClinicCostandCapacity.xlsx')
FacilityInServiceArea = pd.merge(FacilityInServiceArea, ClinicCapacity,
                                 how='inner', left_on='facility type', right_on='Facility Type')

# Vaccine delivery capability
FacilityInServiceArea['Daily Capacity'] = FacilityInServiceArea['Square Meteres Available'] \
                                          * FacilityInServiceArea['Vaccines delivered per square meter, per day']
FacilityInServiceArea['100days Capacity'] = FacilityInServiceArea['Square Meteres Available']\
                                            * FacilityInServiceArea['Vaccines delivered per square meter, per day'] * 100

FacilityInServiceArea.to_csv('FacilityInServiceArea.csv', index=False)
totalCapacity = FacilityInServiceArea['100days Capacity'].sum()
print('The Maximum Vaccine Delivery Capacity of all CaliHealth facility: ' + str(totalCapacity))

countyCapacity = (FacilityInServiceArea.groupby(['facility county']).sum()['100days Capacity'])
#print(countyCapacity)

# Pop up clinics locations
Pop_up_Clinics = pd.read_csv('Pop_up_Clinics.csv')
Pop_up_Clinics_Detail = pd.merge(Pop_up_Clinics, countiesList,
                                 how='inner', left_on='City', right_on='city')
Pop_up_Clinics_Detail.to_csv('Pop_up_Clinics_Detail.csv', index=False)
