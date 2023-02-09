import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

caliHealthAreasFile = open("CaliHealthCounties.txt", mode='r')
caliHealthAreasList = caliHealthAreasFile.read().splitlines()[1:]
caliHealthAreas = pd.DataFrame({'serviceAreas': caliHealthAreasList})
caliHealthAreas.to_csv('caliHealthAreas.csv')

countiesList = pd.read_csv('CaliforniaZipCodeCounties.csv')
censusData = pd.read_csv('CaliforniaCensusDataByZip.csv')

df_caliHealthCoverage = pd.merge(caliHealthAreas, countiesList, how='inner', left_on='serviceAreas', right_on='county')
df_caliHealthCoverage = pd.merge(df_caliHealthCoverage, censusData, how='inner', left_on='zip', right_on='Geographic Area Name')

df_caliHealthCoverage.to_csv(r'Coverage of CaliHealth.csv', index=False)








