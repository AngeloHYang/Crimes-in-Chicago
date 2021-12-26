#!/usr/bin/env python
# coding: utf-8

# # Chicago Crime Theft Data Analysis

# > This is by us. Handling crime data of Chicago from 2001 to 2017
# 
# > Thanks to These projects:
# > - https://www.kaggle.com/fahd09/eda-of-crime-in-chicago-2005-2016
# > - 朱小波, 李昕, 叶信岳. 数据关联背景下芝加哥市一般盗窃案件的多维度分析[J]. 犯罪研究, 2018(4):10.

# ## Importing Data

# In[1]:


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import gc
import math
import random
import folium
from datetime import datetime
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import explained_variance_score
from sklearn.metrics import r2_score


# In[2]:


from fbprophet import Prophet
from fbprophet.diagnostics import cross_validation, performance_metrics
from fbprophet.plot import plot_cross_validation_metric, add_changepoints_to_plot, plot_plotly
import json
from fbprophet.serialize import model_to_json, model_from_json


# In[3]:


Crime_2001_to_2004 = pd.read_csv("../Data/Crimes in Chicago_An extensive dataset of crimes in Chicago (2001-2017), by City of Chicago/Chicago_Crimes_2001_to_2004.csv", error_bad_lines=False)
Crime_2005_to_2007 = pd.read_csv("../Data/Crimes in Chicago_An extensive dataset of crimes in Chicago (2001-2017), by City of Chicago/Chicago_Crimes_2005_to_2007.csv", error_bad_lines=False)
Crime_2008_to_2011 = pd.read_csv("../Data/Crimes in Chicago_An extensive dataset of crimes in Chicago (2001-2017), by City of Chicago/Chicago_Crimes_2008_to_2011.csv", error_bad_lines=False)
Crime_2012_to_2017 = pd.read_csv("../Data/Crimes in Chicago_An extensive dataset of crimes in Chicago (2001-2017), by City of Chicago/Chicago_Crimes_2012_to_2017.csv", error_bad_lines=False)


# In[4]:


print(Crime_2001_to_2004.columns)
Crime_2001_to_2004.head()


# ### ERROR
# 
# When trying to read data with
# 
# `Crime_2001_to_2004 = pd.read_csv("../Data/Crimes in Chicago_An extensive dataset of crimes in Chicago (2001-2017), by City of Chicago/Chicago_Crimes_2001_to_2004.csv")`
# 
# Got an Error that goes like:
# 
# > ParserError: Error tokenizing data. C error: Expected 23 fields in line 1513591, saw 24
# 
# The solution is:
# 
# `Crime_2001_to_2004 = pd.read_csv("../Data/Crimes in Chicago_An extensive dataset of crimes in Chicago (2001-2017), by City of Chicago/Chicago_Crimes_2001_to_2004.csv", error_bad_lines=False)`
# 
# So now it works:
# 
# > b'Skipping line 1513591: expected 23 fields, saw 24\n'
# /home/hanpeng/anaconda3/lib/python3.8/site-packages/IPython/core/interactiveshell.py:3165: DtypeWarning: Columns (17,20) have mixed types.Specify dtype option on import or set low_memory=False.
#   has_raised = await self.run_ast_nodes(code_ast.body, cell_name,
# 
# The reason being:
# 
# > 读取文件时遇到和列数不对应的行，此时会报错。若报错行可以忽略，则添加该参数
# > When the column number of one line doesn't met the header row's

# ### Data Combination
# 
# > To Combine the four files' data into one
# > 
# > gc.collect() to guarentee to save RAM

# In[5]:


Crime_data = pd.concat([Crime_2001_to_2004, Crime_2005_to_2007, Crime_2008_to_2011, Crime_2012_to_2017])
del Crime_2001_to_2004
del Crime_2005_to_2007
del Crime_2008_to_2011
del Crime_2012_to_2017
gc.collect()


# In[6]:


Crime_data.head()


# In[7]:


print('Crime_data loaded!')


# ### Basic Info

# In[8]:


Crime_data.info()


# In[9]:


print("Types of crime: \n", np.array(Crime_data['Primary Type'].drop_duplicates()))


# In[10]:


print("Location Type: \n", np.array(Crime_data['Location Description'].drop_duplicates().head()))


# ### Dropping Duplicated ones

# What makes two cases duplicated?

# - Could it be case number?

# In[11]:


pd.DataFrame(Crime_data).groupby(['Case Number']).count()


# It looks convincing, so be it! Let's drop duplicated ones by that:

# In[12]:


print("Before drop_duplicates: ", Crime_data.shape)
Crime_data.drop_duplicates(subset=['Case Number'], inplace=True)
print("After drop_duplicates: ", Crime_data.shape)


# In[13]:


Crime_data.head()


# ### Data Selection

# There are three types of crime that fits the defination of stealing: THEFT, MOTOR VEHICLE THEFT, BURGLARY.
# 
# So we should only keep data of them and forget about others.

# In[14]:


Crime_data.index = Crime_data['Case Number']


# In[15]:


print("Before the drop, it's ", Crime_data.shape)
Crime_data.drop(Crime_data[ 
                    (Crime_data['Primary Type'] != "THEFT") &
                    (Crime_data['Primary Type'] != "MOTOR VEHICLE THEFT") &
                    (Crime_data['Primary Type'] != 'BURGLARY')
                ].index, inplace=True, axis=0)
print("After the drop, it's ", Crime_data.shape)


# gc.collect() to make sure RAM stay low

# In[16]:


gc.collect()


# ### Handling NaN and Missing Value

# Turning it into df

# In[17]:


df = pd.DataFrame(Crime_data)


# There are missing values and null values:

# In[18]:


np.any(df.isnull())


# In[19]:


np.any(df['X Coordinate'] == 0)


# In[20]:


np.any(df['Y Coordinate'] == 0)


# So we need to deal with them

# In[21]:


#Crime_data[['X Coordinate', 'Y Coordinate']] = Crime_data[['X Coordinate', 'Y Coordinate']].replace(0, np.NaN)
Crime_data[['X Coordinate', 'Y Coordinate', 'Latitude', 'Longitude']] = Crime_data[['X Coordinate', 'Y Coordinate', 'Latitude', 'Longitude']].replace(0, np.NaN)
print("Before we drop NaN: ", Crime_data.shape)
Crime_data.dropna(inplace=True)
df = pd.DataFrame(Crime_data)
print("After we drop NaN: ", Crime_data.shape)


# ### Date Processing

# - Convert Date Format:

# In[22]:


Crime_data.Date = pd.to_datetime(Crime_data.Date, format="%m/%d/%Y %I:%M:%S %p")


# - Convert Latitude to float64

# In[23]:


Crime_data.info()


# In[24]:


Crime_data.Latitude = Crime_data.Latitude.astype(float)


# In[25]:


Crime_data.info()


# ### Deleting 2017

# There's something wrong with the result at the year of 2017:

# In[26]:


EachCountByYear = pd.crosstab(Crime_data['Year'], Crime_data['Primary Type'])
EachCountByYear


# In[27]:


plt.plot(EachCountByYear)
plt.show()


# The reason is the data only stops at 2017.1.18:

# In[28]:


theBeginningOf2017 = datetime(2017, 1, 1)
df[df['Date'] >= theBeginningOf2017].sort_values(['Date'], ascending=False).head()


# So for the sake of convenience, we should just delete data in 2017

# In[29]:


print("Before deleting data in 2017: ", Crime_data.shape)
Crime_data.drop(df[df['Date'] >= theBeginningOf2017].index, inplace=True, axis=0)
df = pd.DataFrame(Crime_data)
print("After deleting data in 2017: ", Crime_data.shape)


# ### Deleting 2004 and Before
# 
# There's something wrong with the data at the spring of 2004 and before the middle of 2002

# In[30]:


EachCountByDay = pd.crosstab(Crime_data['Date'].dt.floor('d'), Crime_data['Primary Type'])
sumOfEachDay = EachCountByDay.sum(axis=1)
percentagePerDay = EachCountByDay.div(sumOfEachDay, axis=0)
plt.figure(figsize=(20, 5))
plt.plot(EachCountByDay)
plt.plot(sumOfEachDay)
plt.ylabel('Crime Count')
plt.legend(['BURGLARY', 'MOTOR VEHICLE THEFT', 'THEFT', 'Sum'])
plt.show()


# So we decided to delete them

# In[31]:


theBeginningOf2005 = datetime(2005, 1, 1)
print("Before deleting data before 2005: ", Crime_data.shape)
Crime_data.drop(df[df['Date'] < theBeginningOf2005].index, inplace=True, axis=0)
df = pd.DataFrame(Crime_data)
print("After deleting data before 2005: ", Crime_data.shape)


# ### Remember to clean the RAM

# In[32]:


gc.collect()


# ### Info Once Again

# In[33]:


Crime_data.info()


# ## Data Analysis and Visualization

# ### Percentages

# - Percenrages of three crimes in total

# In[34]:


countTotal = df.groupby(['Primary Type']).count()['Case Number']
countSum = countTotal.sum()
percentageTotal = countTotal.div(countSum, axis=0)


# In[35]:


percentageTotal.plot(kind='pie')


# - Percentages of three types of crimes each year

# In[36]:


EachCountByYear = pd.crosstab(Crime_data['Year'], Crime_data['Primary Type'])
sumOfEachYear = EachCountByYear.sum(axis=1)
percentagePerYear = EachCountByYear.div(sumOfEachYear, axis=0)


# In[37]:


percentagePerYear.plot(kind='bar', stacked=True)


# - Percentages of three types of crimes each day
# 
# > It's too time and RAM consuming, so I'll leave out the plotting part.

# > `dt.floor('d')` means to convert the date to only day level

# In[38]:


EachCountByDay = pd.crosstab(Crime_data['Date'].dt.floor('d'), Crime_data['Primary Type'])
sumOfEachDay = EachCountByDay.sum(axis=1)
percentagePerDay = EachCountByDay.div(sumOfEachDay, axis=0)


# In[113]:


#percentagePerDay.plot(kind='bar', stacked=True, xticks=[])


# - Percentages of three types of crimes each hour

# In[40]:


EachCountByHour = pd.crosstab(Crime_data['Date'].dt.floor('h'), Crime_data['Primary Type'])
sumOfEachHour = EachCountByHour.sum(axis=1)
percentagePerHour = EachCountByHour.div(sumOfEachHour, axis=0)


# In[114]:


#percentagePerHour.plot(kind='bar', stacked=True, xticks=[])


# ### Trends

# - Crime Number by Year

# In[42]:


EachCountByYear


# In[43]:


plt.plot(EachCountByYear)
plt.plot(sumOfEachYear)
plt.ylabel('Crime Count')
plt.legend(['BURGLARY', 'MOTOR VEHICLE THEFT', 'THEFT', 'Sum'])
plt.show()


# - Crime Number by Day

# In[44]:


EachCountByDay


# In[45]:


plt.figure(figsize=(20, 5))
plt.plot(EachCountByDay)
plt.plot(sumOfEachDay)
plt.ylabel('Crime Count')
plt.legend(['BURGLARY', 'MOTOR VEHICLE THEFT', 'THEFT', 'Sum'])
plt.show()


# There seems to be an anual pattern.

# Also

# In[46]:


fig, axes = plt.subplots(nrows=12, ncols=1, figsize=(20, 100))

EachCountByDayDataFrame = pd.DataFrame(EachCountByDay)
EachCountByDayDataFrame = EachCountByDayDataFrame.reset_index(inplace=False)

for year in range(2005, 2017):
    i = year - 2005
    
    theBeginningOfTheYear = datetime(year, 1, 1)
    theEndOfTheYear = datetime(year + 1, 1, 1)

    EachCountByDayDataFrameTheYear = EachCountByDayDataFrame[
        (EachCountByDayDataFrame['Date'] >= theBeginningOfTheYear) & 
        (EachCountByDayDataFrame['Date'] < theEndOfTheYear)
    ].set_index(['Date'])
    sumOfEachCountByDayDataFrameTheYear = EachCountByDayDataFrameTheYear.sum(axis=1)
    
    axes[i].set_title("Data " + str(year) + " Each Day")
    axes[i].plot(EachCountByDayDataFrameTheYear)
    axes[i].plot(sumOfEachCountByDayDataFrameTheYear)
    axes[i].legend(['BURGLARY', 'MOTOR VEHICLE THEFT', 'THEFT', 'Sum'])

for ax in axes:
    ax.set_xticks([])
    
plt.show()


# There seems to be no monthly patterns

# Also

# In[47]:


fig, axes = plt.subplots(nrows=72, ncols=2, figsize=(20, 400))

for year in range(2005, 2006):
    for month in range(1, 13):
        i = int(((year - 2005) * 12 + month - 1) / 2)#aka row number
        j = int((year - 2005) * 12 + month + 1) % 2 #aka column number
        
        newMonth = (month + 1) if (month + 1) <= 12 else 1
        theBeginningOfTheMonth = datetime(year, month, 1)
        theEndOfTheMonth = datetime(year + int(month / 12), newMonth, 1)
        
        EachCountByDayDataFrameTheMonth = EachCountByDayDataFrame[
            (EachCountByDayDataFrame['Date'] >= theBeginningOfTheMonth) & 
            (EachCountByDayDataFrame['Date'] < theEndOfTheMonth)
        ].set_index(['Date'])
        sumOfEachCountByDayDataFrameTheMonth = EachCountByDayDataFrameTheMonth.sum(axis=1)
        
        axes[i][j].set_title("Data " + str(year) + "." + str(month))
        axes[i][j].plot(EachCountByDayDataFrameTheMonth)
        axes[i][j].plot(sumOfEachCountByDayDataFrameTheMonth)
        
        axes[i][j].legend(['BURGLARY', 'MOTOR VEHICLE THEFT', 'THEFT', 'Sum'])
        axes[i][j].grid()
    
plt.show()    


# - Crime Number by Hour

# In[48]:


EachCountByHour


# In[49]:


EachCountByHourDataFrame = pd.DataFrame(EachCountByHour)
EachCountByHourDataFrame = EachCountByHourDataFrame.reset_index(inplace=False)

fig, axes = plt.subplots(nrows=72, ncols=2, figsize=(20, 400))

for year in range(2005, 2017):
    for month in range(1, 13):
        i = int(((year - 2005) * 12 + month - 1) / 2)#aka row number
        j = int((year - 2005) * 12 + month + 1) % 2 #aka column number
        
        newMonth = (month + 1) if (month + 1) <= 12 else 1
        theBeginningOfTheMonth = datetime(year, month, 1)
        theEndOfTheMonth = datetime(year + int(month / 12), newMonth, 1)
        
        EachCountByHourDataFrameTheMonth = EachCountByHourDataFrame[
            (EachCountByHourDataFrame['Date'] >= theBeginningOfTheMonth) & 
            (EachCountByHourDataFrame['Date'] < theEndOfTheMonth)
        ].set_index(['Date'])
        sumOfEachCountByHourDataFrameTheMonth = EachCountByHourDataFrameTheMonth.sum(axis=1)
        
        axes[i][j].set_title("Data " + str(year) + "." + str(month))
        axes[i][j].plot(EachCountByHourDataFrameTheMonth)
        axes[i][j].plot(sumOfEachCountByHourDataFrameTheMonth)
        axes[i][j].legend(['BURGLARY', 'MOTOR VEHICLE THEFT', 'THEFT', 'Sum'])
        
plt.show()    


# ### Location Analysis

# - Here are location types:

# In[50]:


for i in np.array(Crime_data['Location Description'].drop_duplicates()):
    print(i)


# In[51]:


Location_Descripton_Count = df.groupby(['Location Description']).count()['Unnamed: 0']
Location_Descripton_Count = pd.DataFrame(Location_Descripton_Count)
Location_Descripton_Count = Location_Descripton_Count.sort_values(['Unnamed: 0'], ascending=False)


# In[52]:


Location_Descripton_Count


# What it looks like in bar graphs:

# In[53]:


Location_Descripton_Count.plot(kind='bar', figsize=(20, 8))


# - Also, when it comes to block names:

# In[54]:


for i in np.array(Crime_data['Block'].drop_duplicates()):
    print(i)


# In[55]:


Crime_data['Block'].shape


# In[56]:


Crime_data['Block'].drop_duplicates().shape


# So, in average, there are:

# In[57]:


Crime_data['Block'].shape[0] / Crime_data['Block'].drop_duplicates().shape[0]


# for each block

# - For street names

# In[58]:


streetNames = []
for i in Crime_data['Block'].drop_duplicates():
    streetName = i.split(' ', 2)
    streetName = streetName[2]
    streetNames.append(streetName)
streetNames = list(dict.fromkeys(streetNames))


# In[59]:


streetNames


# In[60]:


print("There are", len(streetNames), "streets")
print("In average,", Crime_data['Block'].shape[0] / len(streetNames), "crimes are in each street.")


# ### Paint the Map with Crime Data

# - With District

# In[61]:


plt.figure(figsize=(10, 10))
plt.scatter(x=Crime_data['X Coordinate'], y=Crime_data['Y Coordinate'], c=Crime_data['District'], s=1)
plt.show()


# - With Streets

# In[62]:


streetNames[1]


# In[63]:


streetNameToIdDict = dict()
count = 0
for i in streetNames:
    streetNameToIdDict[i] = count
    count += 1

CrimeStreetsInNumbers = []
for i in list(Crime_data['Block']): 
    CrimeStreetsInNumbers.append(streetNameToIdDict[i.split(' ', 2)[2]])


# In[64]:


plt.figure(figsize=(10, 10))
plt.scatter(x=Crime_data['X Coordinate'], y=Crime_data['Y Coordinate'], c=CrimeStreetsInNumbers, s=0.001)
plt.show()


# - With Blocks and gradient colors
# 
# > Red means dangerous, green means safe

# In[65]:


blockAndCrimeCountAscending = pd.DataFrame(df.groupby(['Block']).count()['Unnamed: 0']).sort_values(['Unnamed: 0'], ascending=True).to_dict()['Unnamed: 0']

CrimeBlocksInNumbers = []
for i in list(Crime_data['Block']): 
    CrimeBlocksInNumbers.append(blockAndCrimeCountAscending[i])


# This is to make sure that bad blocks will be scattered later, since the later ones will cover the earlier ones

# In[66]:


a = df[['X Coordinate', 'Y Coordinate']].copy()
a['Crime Block In Numbers'] = CrimeBlocksInNumbers
a.sort_values(['Crime Block In Numbers'], inplace=True)


# In[67]:


CrimeBlocksInNumbers = list(a['Crime Block In Numbers'])


# In[68]:


CrimeBlocksInNumbers[1]


# > To calculate the best vmin and vmax with Interquartile Range related method

# In[69]:


plt.figure(figsize=(20, 20))

data_mean, data_std = np.mean(CrimeBlocksInNumbers), np.std(CrimeBlocksInNumbers)
print(data_mean, data_std)
cut_off = data_std * 3
lower, upper = max(CrimeBlocksInNumbers[0], data_mean - cut_off), min(CrimeBlocksInNumbers[-1], data_mean + cut_off)
print(lower, upper)

cm = plt.cm.get_cmap('RdYlGn_r')
sc = plt.scatter(x=a['X Coordinate'], y=a['Y Coordinate'], c=CrimeBlocksInNumbers, s=1, cmap=cm, vmax=upper, vmin=lower)
plt.colorbar(sc)
plt.show()


# In[70]:


del a


# ### Folium Limit to Chicago

# In[71]:


map = folium.Map(
    min_zoom=9,
    zoom_start = 10,
    location=[41.8781, -87.6298],
    zoom_control=True,
    control_scale=True,
    max_lat=43,
    max_lon=-86,
    min_lat=39,
    min_lon=-89,
    max_bounds=True,
    width='100%',
    height='100%',
)
gc.collect()


# In[72]:


map


# ### Block Crimes on Map with Radius and Colors

# In[73]:


blockNames = list(Crime_data['Block'].drop_duplicates())
blockNameToCoordinates = (df[['Block', 'Latitude', 'Longitude']].reset_index().groupby(['Block']).mean()).to_dict()
blockCrimeCount = (df.groupby(['Block']).count())['Unnamed: 0']


# In[74]:


pd.DataFrame(blockCrimeCount.sort_values(ascending=False))[:500].tail(1)


# Put block crimes onto the map with circles with radius
# 
# To get the best radius, extreme values needs to be handled
# 
# Radius 0 stands for no crime, then lower and upper should be converted to from 1(or other starting point) to 100(or other up limit)
# 
# So we need a function that fits: (x=lower, y=1) and (x=upper, y=100 or other target values)
# 
# the function will convert from crimeCount to radius value
# 
# We can get the a and b value of y = ax + b from basic math operations
# 
# > blockCrimeCount.max()
# >
# > blockCrimeCount.min()
# >
# > blockCrimeCount.mean()
# >
# > blockCrimeCount.std()

# In[75]:


cut_off = blockCrimeCount.std() * 3
lower, upper = max(blockCrimeCount.min(), blockCrimeCount.mean() - cut_off), min(blockCrimeCount.max(), blockCrimeCount.mean() + cut_off)
print("Values:", lower, upper)
startingPoint = 0.1
MaxRadius = 3

def getRadius(blockCrimeNumber):
    if lower == upper:
        radius = (startingPoint + MaxRadius) / 2
    else:
        a = (MaxRadius - startingPoint) / (upper - lower)
        b = startingPoint - a * lower
        radius = a * blockCrimeNumber + b
    return radius

for blockName in blockNames:
    if blockCrimeCount[blockName] <= 200:
        continue
    lat = blockNameToCoordinates['Latitude'][blockName]
    lon = blockNameToCoordinates['Longitude'][blockName]
    radius = getRadius(blockCrimeCount[blockName])
    
    color = '#FF4500'
    
    popup_text = """Block Name: {}<br>
                Latitude : {}<br>
                Longitude : {}<br>
                Criminal Incidents : {}<br>"""
    popup_text = popup_text.format(
        blockName,
        lat,
        lon,
        blockCrimeCount[blockName])
    folium.CircleMarker(location=[lat, lon], 
                        popup=popup_text, 
                        radius=radius, 
                        color=color, 
                        fill=True).add_to(map)


# In[76]:


map


# - Map with block in squares with crime data as borders

# In[77]:


oneUserMap = folium.Map(
    min_zoom=9,
    zoom_start = 10,
    location=[41.710843655, -87.621197595],
    zoom_control=True,
    control_scale=True,
    max_lat=43,
    max_lon=-86,
    min_lat=39,
    min_lon=-89,
    max_bounds=True,
    width='100%',
    height='100%',
)
gc.collect()


# In[78]:


point1_Latitude = (df[['Block', 'Latitude', 'Longitude']].reset_index().groupby(['Block']).max()).iloc[3]['Latitude']
point1_Longitude = (df[['Block', 'Latitude', 'Longitude']].reset_index().groupby(['Block']).max()).iloc[3]['Longitude']
point2_Latitude = (df[['Block', 'Latitude', 'Longitude']].reset_index().groupby(['Block']).max()).iloc[3]['Latitude']
point2_Longitude = (df[['Block', 'Latitude', 'Longitude']].reset_index().groupby(['Block']).min()).iloc[3]['Longitude']
point3_Latitude = (df[['Block', 'Latitude', 'Longitude']].reset_index().groupby(['Block']).min()).iloc[3]['Latitude']
point3_Longitude = (df[['Block', 'Latitude', 'Longitude']].reset_index().groupby(['Block']).min()).iloc[3]['Longitude']
point4_Latitude = (df[['Block', 'Latitude', 'Longitude']].reset_index().groupby(['Block']).min()).iloc[3]['Latitude']
point4_Longitude = (df[['Block', 'Latitude', 'Longitude']].reset_index().groupby(['Block']).max()).iloc[3]['Longitude']


# In[79]:


print(point1_Latitude, point1_Longitude)


# In[80]:


# #     folium.RegularPolygonMarker(
#         [e[0],e[1]],
#         popup=str(i)+":"+e[0]+e[1],
#         fill_color='#769d96',
#         number_of_sides=8,
#         radius=10
#     ).add_to(oneUserMap)
#     i+=1
#     line_to_hanoi = folium.PolyLine(
#         location
#         color = black
#     ).add_to(oneUserMap)

folium.Rectangle(
    bounds = [
        [
            point1_Latitude, point1_Longitude
        ],
        [
            point2_Latitude, point2_Longitude
        ],
        [
            point3_Latitude, point3_Longitude
        ],
        [
            point4_Latitude, point4_Longitude
        ]
    ],
    fill_color = '#769d96',
    radius = 10
).add_to(oneUserMap)

oneUserMap


# ### Test

# In[81]:


#cm = plt.cm.get_cmap('RdYlBu')
x = [i/1000 for i in range(0, 20 * 1000)]

cm = plt.cm.get_cmap('RdYlGn_r')
sc = plt.scatter(x, x, c=x, vmin=10, vmax=15, s=35, cmap=cm)
plt.colorbar(sc)
plt.show()


# ## Prediction

# Here's an intro for Prophet:
# 
# 模型预测 - Prophet
# Facebook 所提供的 prophet 算法不仅可以处理时间序列存在一些异常值的情况，也可以处理部分缺失值的情形，还能够几乎全自动地预测时间序列未来的走势。prophet 所做的事情就是：
# 
# 输入已知的时间序列的时间戳和相应的值；
# 
# 输入需要预测的时间序列的长度；
# 
# 输出未来的时间序列走势。
# 
# 输出结果可以提供必要的统计指标，包括拟合曲线，上界和下界等。

# ### Learning to Use the Model

# In[82]:


Theft_each_hour_dataset = pd.DataFrame(EachCountByHour['THEFT'])
Theft_each_hour_dataset = Theft_each_hour_dataset.reset_index(inplace=False)
Theft_each_hour_dataset.rename(columns={"Date": "ds", "THEFT": "y"}, inplace=True)


# In[83]:


prophet = Prophet(
    growth='linear',
    yearly_seasonality= True,
    weekly_seasonality = True,
    daily_seasonality = True,
    seasonality_mode = 'additive')
prophet.add_seasonality(name='monthly', period=30.5, fourier_order=5)


# In[84]:


get_ipython().run_line_magic('time', 'prophet.fit(Theft_each_hour_dataset)')


# In[85]:


get_ipython().run_line_magic('time', 'future = prophet.make_future_dataframe(periods=365)')


# If you want to add a new time period

# In[86]:


get_ipython().run_line_magic('time', 'confirmed_forecast = prophet.predict(future)')


# In[87]:


get_ipython().run_line_magic('time', 'prophet.plot(confirmed_forecast)')


# In[88]:


confirmed_forecast.head()


# In[89]:


confirmed_forecast.columns


# ### User Predict

# If you want to add a new time to predict

# In[90]:


future = pd.DataFrame(columns=['ds'])
future = future.append({'ds': datetime(2035, 1, 1)}, ignore_index=True)


# In[91]:


future


# In[92]:


get_ipython().run_line_magic('time', 'user_forecast = prophet.predict(future)')


# In[93]:


user_forecast.tail()


# In[94]:


get_ipython().run_line_magic('time', 'prophet.plot(user_forecast)')


# ### Manually Evaluate Test

# In[95]:


Theft_each_hour_dataset[Theft_each_hour_dataset['ds'] == datetime(2016, 1, 1)]


# In[96]:


train = Theft_each_hour_dataset[:95995]
test = Theft_each_hour_dataset[95995:]


# In[97]:


train.tail()


# In[98]:


test.head()


# In[99]:


prophet = Prophet(
    growth='linear',
    yearly_seasonality=True,
    weekly_seasonality=True,
    daily_seasonality=True,
    seasonality_mode='additive'
)
prophet.add_seasonality(name='monthly', period=30.5, fourier_order=5)
get_ipython().run_line_magic('time', 'prophet.fit(train)')


# In[100]:


future = pd.DataFrame(test['ds'])
future


# In[101]:


get_ipython().run_line_magic('time', 'forecast = prophet.predict(future)')


# In[102]:


prophet.plot(forecast)


# In[103]:


forecast.head()


# In[104]:


plt.figure(figsize=(20, 8))
plt.plot(test['ds'][200:300], test['y'][200:300], label='Actual')
plt.plot(forecast['ds'][200:300], forecast['yhat'][200:300], label='Predicted')
plt.legend()
plt.show()


# - MAE
# 
# > Mean Absolute Error, l1

# In[105]:


y_true = test['y'].values
y_predicted = forecast['yhat'].values
print('MAE: %.3f' % mean_absolute_error(y_true, y_predicted))


# - MSE
# 
# > Mean Squared Error, l2

# In[106]:


print('MSE: %.3f' % mean_squared_error(y_true, y_predicted))


# - RMSE

# In[107]:


print('RMSE: %.3f' % math.sqrt(mean_squared_error(y_true, y_predicted)))


# - Explained variance

# In[108]:


print('Explained variance: %.3f' % explained_variance_score(y_true, y_predicted))


# - Coefficient of determination
# 
# > R2

# In[109]:


print('Coefficient of determination: %.3f' % r2_score(y_true, y_predicted))


# ### Saving and Opening the Model
# 
# > According to https://facebook.github.io/prophet/docs/additional_topics.html#updating-fitted-models

# In[110]:


m = prophet

with open('serialized_model.json', 'w') as fout:
    json.dump(model_to_json(m), fout)  # Save model
    
del m
    
with open('serialized_model.json', 'r') as fin:
    mm = model_from_json(json.load(fin))  # Load model


# In[111]:


get_ipython().run_line_magic('time', 'forecast = mm.predict(future)')


# In[112]:


get_ipython().run_line_magic('time', 'mm.plot(forecast)')


# In[ ]:




