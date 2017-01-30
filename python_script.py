import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
from pandas.tools.plotting import scatter_matrix
import pprint as pp

pathName = 'C:/Users/Runtong/Documents/BIKE_RENT/Question Data Set'
fileName = 'day.csv'
filePath = os.path.join(pathName, fileName)
raw_day = pd.read_csv(filePath)

pathName2 = 'C:/Users/Runtong/Documents/BIKE_RENT/Question Data Set'
fileName2 = 'hour.csv'
filePath2 = os.path.join(pathName2, fileName2)
raw_hour = pd.read_csv(filePath2)

# 1. scatter plot
plot_cols = ["weathersit",
             "temp",
             "atemp",
             "hum",
             "windspeed",
             "casual",
             "registered",
             "cnt",
             "season",
             "mnth",
             "holiday",
             "weekday",
             "workingday"]
# scatter matrix
fig = plt.figure(1, figsize=(18, 18))
fig.clf()
ax = fig.gca()
scatter_matrix(raw_day[plot_cols], alpha=0.3, ax=ax)
fig.savefig('scatter plot.png')
# plt.show()

#--------------------------------------------
# 2. line plot: average count w.r.t. hour, legend by weekday
count_avg = pd.DataFrame()
count_avg = raw_hour.loc[:, lambda df: ['hr', 'weekday','cnt']].groupby(['hr','weekday']).mean() \
                        .reset_index().sort_values('weekday', ascending=False).reset_index(drop=True)
pp.pprint(count_avg)
fig = plt.figure(2)
for num in range(0,7):
    if num == 0:
        legend = 'Sunday'
    if num == 1:
        legend = 'Monday'
    if num == 2:
        legend = 'Tuesday'
    if num == 3:
        legend = 'Wednesday'
    if num == 4:
        legend = 'Thursday'
    if num == 5:
        legend = 'Friday'
    if num == 6:
        legend = 'Saturday'
    weekday_count = count_avg.loc[count_avg['weekday'] == num].sort_values('hr', ascending=True).reset_index(drop=True)
    # pp.pprint(weekday_count[['hr', 'cnt']])
    plt.plot(weekday_count['hr'], weekday_count['cnt'],'o-', label=legend, lw=3, alpha=0.8)
plt.legend()
plt.grid(True)
plt.xlabel('Hour in a Day')
plt.ylabel('Average count')
plt.title('average count vs. Hour')
plt.show()

#-----------------------------------------------
# 3. line plot: average count w.r.t. hour, legend by workday, weekend, and non-working holidays
count_avg = pd.DataFrame()
count_avg = raw_hour.loc[:, lambda df: ['hr', 'holiday', 'workingday', 'cnt']].groupby(['hr', 'holiday', 'workingday']).mean() \
                        .reset_index().sort_values('holiday', ascending=False).reset_index(drop=True)
pp.pprint(count_avg)
fig = plt.figure(3)
for num in range(0,3):
    if num == 0:
        legend = 'Weekday Holiday'
        workingday_count = count_avg.loc[count_avg['workingday'] == 0].loc[count_avg['holiday'] == 1]\
                            .sort_values('hr', ascending=True).reset_index(drop=True)
    if num == 1:
        legend = 'Workingday'
        workingday_count = count_avg.loc[count_avg['workingday'] == 1].sort_values('hr', ascending=True)\
                            .reset_index(drop=True)
    if num == 2:
        legend = 'Weekend'
        workingday_count = count_avg.loc[count_avg['workingday'] == 0].loc[count_avg['holiday'] == 0]\
                            .sort_values('hr', ascending=True).reset_index(drop=True)

    # pp.pprint(weekday_count[['hr', 'cnt']])
    plt.plot(workingday_count['hr'], workingday_count['cnt'],'o-', label=legend, lw=3, alpha=0.8)
plt.legend()
plt.grid(True)
plt.xlabel('Hour in a Day')
plt.ylabel('Average count')
plt.title('average count vs. Hour')
plt.show()

#---------------------------------------
# 4. line plot: average count w.r.t months

count_avg = pd.DataFrame()
count_avg = raw_hour.loc[:, lambda df: ['hr', 'mnth', 'cnt']].groupby(['hr', 'mnth']).mean() \
                        .reset_index().sort_values('mnth', ascending=False).reset_index(drop=True)

fig = plt.figure(4)
# color map
color = iter(cm.rainbow(np.linspace(0,1,12)))
for num in range(0,12):
    if num == 0:
        legend = 'January'
    if num == 1:
        legend = 'February'
    if num == 2:
        legend = 'March'
    if num == 3:
        legend = 'April'
    if num == 4:
        legend = 'May'
    if num == 5:
        legend = 'June'
    if num == 6:
        legend = 'July'
    if num == 7:
        legend = 'August'
    if num == 8:
        legend = 'September'
    if num == 9:
        legend = 'October'
    if num == 10:
        legend = 'November'
    if num == 11:
        legend = 'December'

    weekday_count = count_avg.loc[count_avg['mnth'] == num+1].sort_values('hr', ascending=True).reset_index(drop=True)
    c = next(color)
    plt.plot(weekday_count['hr'], weekday_count['cnt'], 'o-', label=legend, lw=3, alpha=0.8, c=c)
plt.legend()
plt.grid(True)
plt.xlabel('Hour in a Day')
plt.ylabel('Average count')
plt.title('average count vs. Hour')
plt.show()

#-----------------------
# 5. box plot: average count w.r.t months
count_avg = pd.DataFrame()
count_avg = raw_hour.loc[:, lambda df: ['mnth', 'cnt']].groupby(['mnth']).mean() \
                        .reset_index().sort_values('mnth', ascending=False).reset_index(drop=True)

fig = plt.figure(5)
month = pd.DataFrame()
month = ['January', 'February', 'March', 'April','May', 'June','July','August','September','October','November','December']
for num in range(0,12):
    weekday_count = count_avg.loc[count_avg['mnth'] == num+1]
    plt.bar(weekday_count['mnth'], weekday_count['cnt'], alpha=0.5)
plt.legend()
plt.grid(False)
plt.xlabel('Month')
index = np.arange(12)
bar_width = 0.35
plt.xticks(1+index + bar_width, month)
plt.ylabel('Average count')
plt.title('average count vs. Month')
plt.show()


#---------------------
# 6. Box plot: weathersit vs count
count = pd.DataFrame()
count = raw_hour.loc[:, lambda df: ['weathersit', 'cnt']].reset_index().sort_values('weathersit', ascending=False).reset_index(drop=True)

fig = plt.figure(6)
temp1 = np.array(count.loc[count['weathersit'] == 1]['cnt'].reset_index(drop=True))
temp2 = np.array(count.loc[count['weathersit'] == 2]['cnt'].reset_index(drop=True))
temp3 = np.array(count.loc[count['weathersit'] == 3]['cnt'].reset_index(drop=True))
temp4 = np.array(count.loc[count['weathersit'] == 4]['cnt'].reset_index(drop=True))
temp = [temp1, temp2, temp3,temp4]
# print(temp4)
plt.boxplot(temp)
plt.legend()
plt.grid(False)
plt.xlabel('Weathersit')
plt.ylabel('Average count')
plt.title('average count vs. Weathersit')
plt.show()


#-----------------------------
# 7. Scatter Plot, atemp vs count
count = pd.DataFrame()
count = raw_hour.loc[:, lambda df: ['atemp', 'cnt']].reset_index().sort_values('atemp', ascending=False).reset_index(drop=True)
fig = plt.figure(7)
count_max = count.groupby(['atemp']).max().reset_index().reset_index(drop=True)
count_mean = count.groupby(['atemp']).mean().reset_index().reset_index(drop=True)
cm = plt.cm.get_cmap('rainbow')
plt.scatter(count['atemp'],count['cnt'],alpha=0.5,c=count['atemp'],cmap=cm, label='data points')
plt.plot(count_max['atemp'],count_max['cnt'], 'b', lw=3, alpha=0.8, label='max count')
plt.plot(count_mean['atemp'],count_mean['cnt'], 'r', lw=3, alpha=0.8, label='mean count')
plt.legend()
plt.xlabel('atemp')
plt.ylabel('Count')
plt.title('Count vs. atemp')
plt.show()

#------------------------------------
# 8. Scatter Plot, windspeed vs count
count = pd.DataFrame()
count = raw_hour.loc[:, lambda df: ['windspeed', 'cnt']].reset_index().sort_values('windspeed', ascending=False).reset_index(drop=True)
fig = plt.figure(8)
count_max = count.groupby(['windspeed']).max().reset_index().reset_index(drop=True)
count_mean = count.groupby(['windspeed']).mean().reset_index().reset_index(drop=True)
cm = plt.cm.get_cmap('rainbow')
plt.scatter(count['windspeed'],count['cnt'],alpha=0.5,c=count['windspeed'],cmap=cm, label='data points')
plt.plot(count_max['windspeed'],count_max['cnt'], 'b', lw=3, alpha=0.8, label='max count')
plt.plot(count_mean['windspeed'],count_mean['cnt'], 'r', lw=3, alpha=0.8, label='mean count')
plt.legend()
plt.xlabel('windspeed')
plt.ylabel('Count')
plt.title('Count vs. Windspeed')
plt.show()

#-------------------------------------
# 9. Scatter Plot, humidity vs count
count = pd.DataFrame()
count = raw_hour.loc[:, lambda df: ['hum', 'cnt']].reset_index().sort_values('hum', ascending=False).reset_index(drop=True)
fig = plt.figure(8)
count_max = count.groupby(['hum']).max().reset_index().reset_index(drop=True)
count_mean = count.groupby(['hum']).mean().reset_index().reset_index(drop=True)
cm = plt.cm.get_cmap('rainbow')
plt.scatter(count['hum'],count['cnt'],alpha=0.5,c=count['hum'],cmap=cm, label='data points')
plt.plot(count_max['hum'],count_max['cnt'], 'b', lw=3, alpha=0.8, label='max count')
plt.plot(count_mean['hum'],count_mean['cnt'], 'r', lw=3, alpha=0.8, label='mean count')
plt.legend()
plt.xlabel('humidity')
plt.ylabel('Count')
plt.title('Count vs. Humidity')
plt.show()