import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

caliHealthAreasFile = open("CaliHealthCounties.txt", mode='r')
caliHealthAreasList = caliHealthAreasFile.read().splitlines()[1:]
caliHealthAreas = pd.DataFrame({'serviceAreas': caliHealthAreasList})

countiesList = pd.read_csv('CaliforniaZipCodeCounties.csv')
countiesList.to_csv('caliHealthAreas.csv')













