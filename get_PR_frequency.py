import pandas as pd
import datetime
from dateutil import relativedelta

cleanedProjectList = pd.read_csv('cleaned_project_w_pr.csv', sep = ',')

def round_school(x):
    i, f = divmod(x, 1)
    return int(i + ((f >= 0.5) if (x > 0) else (f > 0.5)))

for i in range(0, len(cleanedProjectList)):
    startDate = datetime.datetime.strptime(cleanedProjectList['Project Startdate'][i], '%m/%d/%y')
    endDate = datetime.datetime.strptime(cleanedProjectList['Project Enddate'][i], '%m/%d/%y')
    r = relativedelta.relativedelta(endDate, startDate)
    months = (r.years * 12) + r.months + 1
    PRFrequency = round_school(cleanedProjectList['PR Number'][i] / months) 
    cleanedProjectList['Merge Frequency'][i] = PRFrequency

cleanedProjectList.to_csv('Final_Project_List.csv', sep = ',', encoding = 'utf-8', index = True)
