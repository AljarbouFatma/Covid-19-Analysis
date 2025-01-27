#!/usr/bin/env python
# coding: utf-8

# In[8]:


#math opeations
import math
# produce random numbers
import random
# to load json files
import json
# datetime oprations
from datetime import timedelta
# to get web contents
from urllib.request import urlopen

# for numerical analyiss
import numpy as np
# to store and process data in dataframe
import pandas as pd


# In[9]:


# basic visualization package
import matplotlib.pyplot as plt
# advanced ploting
import seaborn as sns

# interactive visualization
import plotly.express as px
import plotly.graph_objs as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots


# In[10]:


# for offline ploting
from plotly.offline import plot, iplot, init_notebook_mode
init_notebook_mode(connected=True)


# In[11]:


# converter
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()   

# hide warnings
import warnings
warnings.filterwarnings('ignore')

# to USA states details
import us


# In[12]:


# color pallette
cnf, dth, rec, act = '#fff1c5', '#ff2e63', '#f96d00', '#fe9801' 

#seaborn plot style
sns.set_style('darkgrid')


# In[13]:


full_table = pd.read_csv('COVID-19 Dataset/covid_19_clean_complete.csv')
full_table.head()


# In[14]:


# Grouped by day, country
# =======================

full_grouped = pd.read_csv('COVID-19 Dataset/full_grouped.csv')
full_grouped['Date'] = pd.to_datetime(full_grouped['Date'])
full_grouped.head()


# In[15]:


# Day wise
# ========

day_wise = pd.read_csv('COVID-19 Dataset/day_wise.csv')
day_wise['Date'] = pd.to_datetime(day_wise['Date'])
day_wise.head()


# In[16]:


# Country wise
# ============

country_wise = pd.read_csv('COVID-19 Dataset/country_wise_latest.csv')
country_wise = country_wise.replace('', np.nan).fillna(0)
country_wise.head()


# In[17]:


# Worldometer data
# ================

worldometer_data = pd.read_csv('COVID-19 Dataset/worldometer_data.csv')
worldometer_data = worldometer_data.replace('', np.nan).fillna(0)
worldometer_data.head()


# In[18]:


temp = day_wise[['Date','Deaths', 'Recovered', 'Active']].tail(1)
temp = temp.melt(id_vars="Date", value_vars=['Active', 'Deaths', 'Recovered'])
fig = px.treemap(temp, path=["variable"], values="value", height=225, 
                 color_discrete_sequence=[act, rec, dth])
fig.data[0].textinfo = 'label+text+value'
fig.show()


# In[19]:


def plot_map(df, col, pal):
    df = df[df[col]>0]
    fig = px.choropleth(df, locations="Country/Region", locationmode='country names', 
                  color=col, hover_name="Country/Region", 
                  title=col, hover_data=[col], color_continuous_scale=pal)
#     fig.update_layout(coloraxis_showscale=False)
    fig.show()


# In[20]:


plot_map(country_wise, 'Confirmed', 'matter')


# In[21]:


plot_map(country_wise, 'Deaths', 'matter')


# In[22]:


plot_map(country_wise, 'Deaths / 100 Cases', 'matter')


# In[23]:


# Over the time

fig = px.choropleth(full_grouped, locations="Country/Region", 
                    color=np.log(full_grouped["Confirmed"]),
                    locationmode='country names', hover_name="Country/Region", 
                    animation_frame=full_grouped["Date"].dt.strftime('%Y-%m-%d'),
                    title='Cases over time', color_continuous_scale=px.colors.sequential.matter)
fig.update(layout_coloraxis_showscale=False)
fig.show()


# In[24]:


def plot_daywise(col, hue):
    fig = px.bar(day_wise, x="Date", y=col, width=700, color_discrete_sequence=[hue])
    fig.update_layout(title=col, xaxis_title="", yaxis_title="")
    fig.show()


# In[25]:


def plot_daywise_line(col, hue):
    fig = px.line(day_wise, x="Date", y=col, width=700, color_discrete_sequence=[hue])
    fig.update_layout(title=col, xaxis_title="", yaxis_title="")
    fig.show()


# In[26]:


temp = full_grouped.groupby('Date')['Recovered', 'Deaths', 'Active'].sum().reset_index()
temp = temp.melt(id_vars="Date", value_vars=['Recovered', 'Deaths', 'Active'],
                 var_name='Case', value_name='Count')
temp.head()

fig = px.area(temp, x="Date", y="Count", color='Case', height=600, width=700,
             title='Cases over time', color_discrete_sequence = [rec, dth, act])
fig.update_layout(xaxis_rangeslider_visible=True)
fig.show()


# In[27]:


plot_daywise('Confirmed', '#333333')


# In[28]:


plot_daywise('Active', '#333333')


# In[29]:


plot_daywise('New cases', '#333333')


# In[30]:


plot_daywise('Deaths', dth)


# In[31]:


plot_daywise('New deaths', dth)


# In[32]:


plot_daywise('Recovered', rec)


# In[33]:


plot_daywise('New recovered', rec)


# In[34]:


plot_daywise_line('Deaths / 100 Cases', dth)


# In[35]:


plot_daywise_line('Deaths / 100 Recovered', dth)


# In[36]:


plot_daywise_line('Recovered / 100 Cases', rec)


# In[37]:


plot_daywise('No. of countries', '#035aa6')


# In[38]:


temp = day_wise[['Date', 'Recovered', 'Active']]
temp = temp.melt(id_vars='Date', value_vars=['Recovered', 'Active'], 
                 var_name='Variable', value_name='Count')
px.line(temp, x='Date', y='Count', color='Variable')


# In[39]:


def plot_hbar(df, col, n, hover_data=[]):
    fig = px.bar(df.sort_values(col).tail(n), 
                 x=col, y="Country/Region", color='WHO Region',  
                 text=col, orientation='h', width=700, hover_data=hover_data,
                 color_discrete_sequence = px.colors.qualitative.Dark2)
    fig.update_layout(title=col, xaxis_title="", yaxis_title="", 
                      yaxis_categoryorder = 'total ascending',
                      uniformtext_minsize=8, uniformtext_mode='hide')
    fig.show()


# In[40]:


def plot_hbar_wm(col, n, min_pop=1000000, sort='descending'):
    df = worldometer_data[worldometer_data['Population']>min_pop]
    df = df.sort_values(col, ascending=True).tail(n)
    fig = px.bar(df,
                 x=col, y="Country/Region", color='WHO Region',  
                 text=col, orientation='h', width=700, 
                 color_discrete_sequence = px.colors.qualitative.Dark2)
    fig.update_layout(title=col+' (Only countries with > 1M Pop)', 
                      xaxis_title="", yaxis_title="", 
                      yaxis_categoryorder = 'total ascending',
                      uniformtext_minsize=8, uniformtext_mode='hide')
    fig.show()


# In[41]:


plot_hbar(country_wise, 'Confirmed', 15)


# In[42]:


plot_hbar(country_wise, 'Active', 15)


# In[43]:


plot_hbar(country_wise, 'New cases', 15)


# In[44]:


plot_hbar(country_wise, 'Deaths', 15)


# In[45]:


plot_hbar(country_wise, 'New deaths', 15)


# In[46]:


plot_hbar(country_wise, 'Deaths / 100 Cases', 15)


# In[47]:


plot_hbar(country_wise, 'Recovered', 15)


# In[48]:


plot_hbar(country_wise, 'New recovered', 15)


# In[49]:


plot_hbar(country_wise, 'Recovered / 100 Cases', 15)


# In[50]:


plot_hbar(country_wise, '1 week change', 15)


# In[51]:


plot_hbar(country_wise, '1 week % increase', 15)


# In[52]:


plot_hbar_wm('Tot Cases/1M pop', 15, 1000000)


# In[53]:


plot_hbar_wm('Deaths/1M pop', 15, 1000000)


# In[54]:


plot_hbar_wm('TotalTests', 15, 1000000)


# In[55]:


plot_hbar_wm('Tests/1M pop', 15)


# In[56]:


def plot_stacked(col):
    fig = px.bar(full_grouped, x="Date", y=col, color='Country/Region', 
                 height=600, title=col, 
                 color_discrete_sequence = px.colors.cyclical.mygbm)
    fig.update_layout(showlegend=True)
    fig.show()


# In[57]:


def plot_line(col):
    fig = px.line(full_grouped, x="Date", y=col, color='Country/Region', 
                  height=600, title=col, 
                  color_discrete_sequence = px.colors.cyclical.mygbm)
    fig.update_layout(showlegend=True)
    fig.show()


# In[58]:


plot_stacked('Confirmed')


# In[59]:


plot_stacked('Deaths')


# In[60]:


plot_stacked('New cases')


# In[61]:


plot_stacked('Active')


# In[62]:


temp = pd.merge(full_grouped[['Date', 'Country/Region', 'Confirmed', 'Deaths']], 
                day_wise[['Date', 'Confirmed', 'Deaths']], on='Date')
temp['% Confirmed'] = round(temp['Confirmed_x']/temp['Confirmed_y'], 3)*100
temp['% Deaths'] = round(temp['Deaths_x']/temp['Deaths_y'], 3)*100
temp.head()


# In[63]:


fig = px.bar(temp, x='Date', y='% Confirmed', color='Country/Region', 
             range_y=(0, 100), title='% of Cases from each country', 
             color_discrete_sequence=px.colors.qualitative.Prism)
fig.show()


# In[64]:


fig = px.bar(temp, x='Date', y='% Deaths', color='Country/Region', 
             range_y=(0, 100), title='% of Cases from each country', 
             color_discrete_sequence=px.colors.qualitative.Prism)
fig.show()


# In[65]:


def gt_n(n):
    countries = full_grouped[full_grouped['Confirmed']>n]['Country/Region'].unique()
    temp = full_table[full_table['Country/Region'].isin(countries)]
    temp = temp.groupby(['Country/Region', 'Date'])['Confirmed'].sum().reset_index()
    temp = temp[temp['Confirmed']>n]
    # print(temp.head())

    min_date = temp.groupby('Country/Region')['Date'].min().reset_index()
    min_date.columns = ['Country/Region', 'Min Date']
    # print(min_date.head())

    from_nth_case = pd.merge(temp, min_date, on='Country/Region')
    from_nth_case['Date'] = pd.to_datetime(from_nth_case['Date'])
    from_nth_case['Min Date'] = pd.to_datetime(from_nth_case['Min Date'])
    from_nth_case['N days'] = (from_nth_case['Date'] - from_nth_case['Min Date']).dt.days
    # print(from_nth_case.head())

    fig = px.line(from_nth_case, x='N days', y='Confirmed', color='Country/Region', 
                  title='N days from '+str(n)+' case', height=600)
    fig.show()


# In[72]:


gt_n(100000)


# In[73]:


fig = px.scatter(country_wise.sort_values('Deaths', ascending=False).iloc[:20, :], 
                 x='Confirmed', y='Deaths', color='Country/Region', size='Confirmed', 
                 height=700, text='Country/Region', log_x=True, log_y=True, 
                 title='Deaths vs Confirmed (Scale is in log10)')
fig.update_traces(textposition='top center')
fig.update_layout(showlegend=False)
fig.update_layout(xaxis_rangeslider_visible=True)
fig.show()


# In[74]:


def plot_treemap(col):
    fig = px.treemap(country_wise, path=["Country/Region"], values=col, height=700,
                 title=col, color_discrete_sequence = px.colors.qualitative.Dark2)
    fig.data[0].textinfo = 'label+text+value'
    fig.show()


# In[75]:


plot_treemap('Confirmed')


# In[76]:


plot_treemap('Deaths')


# In[77]:


def plot_bubble(col, pal):
    temp = full_grouped[full_grouped[col]>0].sort_values('Country/Region', ascending=False)
    fig = px.scatter(temp, x='Date', y='Country/Region', size=col, color=col, height=3000,
                    color_continuous_scale=pal)
    fig.update_layout(yaxis = dict(dtick = 1))
    fig.update(layout_coloraxis_showscale=False)
    fig.show()


# In[78]:


plot_bubble('New cases', 'Viridis')


# In[79]:


plot_bubble('Active', 'Viridis')


# In[81]:


temp = full_grouped[['Date', 'Country/Region', 'New cases']]
temp['New cases reported ?'] = temp['New cases']!=0
temp['New cases reported ?'] = temp['New cases reported ?'].astype(int)
temp.head()


# In[82]:


fig = go.Figure(data=go.Heatmap(
        z=temp['New cases reported ?'],
        x=temp['Date'],
        y=temp['Country/Region'],
        colorscale='Emrld',
        showlegend=False,
        text=temp['New cases reported ?']))

fig.update_layout(yaxis = dict(dtick = 1))
fig.update_layout(height=3000)
fig.show()


# In[84]:


# HTML('''<div class="flourish-embed flourish-bar-chart-race" data-src="visualisation/1571387"><script src="https://public.flourish.studio/resources/embed.js"></script></div>''')


# In[86]:


temp = full_table.groupby(['Country/Region', 'Date', ])['Confirmed', 'Deaths']
temp = temp.sum().diff().reset_index()

mask = temp['Country/Region'] != temp['Country/Region'].shift(1)

temp.loc[mask, 'Confirmed'] = np.nan
temp.loc[mask, 'Deaths'] = np.nan

countries = full_table[full_table['Confirmed']>100000]['Country/Region'].unique()

temp = temp[temp['Country/Region'].isin(countries)]


n_cols = 3
n_rows = math.ceil(len(countries)/n_cols)

fig = make_subplots(rows=n_rows, cols=n_cols, shared_xaxes=False, subplot_titles=countries)

for ind, country in enumerate(countries):
    row = int((ind/n_cols)+1)
    col = int((ind%n_cols)+1)
    fig.add_trace(go.Bar(x=temp['Date'], y=temp.loc[temp['Country/Region']==country, 'Confirmed'], name=country), row=row, col=col)
    
fig.update_layout(height=4000, title_text="No. of new cases in each Country")
fig.update_layout(showlegend=False)
fig.show()


# In[88]:


usa_df = pd.read_csv('COVID-19 Dataset/usa_county_wise.csv')
usa_latest = usa_df[usa_df['Date'] == max(usa_df['Date'])]
usa_grouped = usa_latest.groupby('Province_State')['Confirmed', 'Deaths'].sum().reset_index()


# In[89]:


us_code = {'Alabama': 'AL', 'Alaska': 'AK', 'American Samoa': 'AS', 'Arizona': 'AZ', 'Arkansas': 'AR', 
    'California': 'CA','Colorado': 'CO','Connecticut': 'CT','Delaware': 'DE', 'District of Columbia': 'DC', 
    'Florida': 'FL', 'Georgia': 'GA', 'Guam': 'GU', 'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL',
    'Indiana': 'IN','Iowa': 'IA','Kansas': 'KS','Kentucky': 'KY','Louisiana': 'LA','Maine': 'ME',
    'Maryland': 'MD','Massachusetts': 'MA','Michigan': 'MI','Minnesota': 'MN','Mississippi': 'MS',
    'Missouri': 'MO','Montana': 'MT','Nebraska': 'NE','Nevada': 'NV','New Hampshire': 'NH', 'New Jersey': 'NJ',
    'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Northern Mariana Islands':'MP',
    'Ohio': 'OH', 'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA', 'Puerto Rico': 'PR',
    'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX',
    'Utah': 'UT', 'Vermont': 'VT', 'Virgin Islands': 'VI', 'Virginia': 'VA', 'Washington': 'WA',
    'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'}

usa_grouped['Code'] = usa_grouped['Province_State'].map(us_code)


# In[90]:


fig = px.choropleth(usa_grouped, color='Confirmed', locations='Code', locationmode="USA-states", 
                    scope="usa", color_continuous_scale="RdGy", title='No. of cases in USA')
fig


# In[93]:


with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

fig = px.choropleth(usa_latest, geojson=counties, locations='FIPS', color='Confirmed',
                            color_continuous_scale="Peach",
                            scope="usa",
                            labels={'Confirmed':'Confirmed'})
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()


# In[94]:


who = country_wise.groupby('WHO Region')['Confirmed', 'Deaths', 'Recovered', 'Active',
                                         'New cases', 'Confirmed last week'].sum().reset_index()
who['Fatality Rate'] = round((who['Deaths'] / who['Confirmed']) * 100, 2)
who['Recovery Rate'] = (who['Recovered'] / who['Confirmed']) * 100

who_g = full_grouped.groupby(['WHO Region', 'Date'])['Confirmed', 'Deaths', 'Recovered', 
                                                     'Active','New cases', 'New deaths'].sum().reset_index()


# In[95]:


def plot_hbar(col, hover_data=[]):
    fig = px.bar(who.sort_values(col), 
                 x=col, y="WHO Region", color='WHO Region',  
                 text=col, orientation='h', width=700, hover_data=hover_data,
                 color_discrete_sequence = px.colors.qualitative.Dark2)
    fig.update_layout(title=col, xaxis_title="", yaxis_title="", 
                      yaxis_categoryorder = 'total ascending',
                      uniformtext_minsize=8, uniformtext_mode='hide')
    fig.show()


# In[96]:


plot_hbar('Confirmed')


# In[97]:


plot_hbar('Deaths')


# In[98]:


plot_hbar('Fatality Rate')


# In[99]:


temp = worldometer_data[worldometer_data['WHO Region']!=0]


# In[103]:


fig = px.scatter(temp, x='TotalCases', y='TotalDeaths', color='WHO Region', 
                 height=700, hover_name='Country/Region', log_x=True, log_y=True, 
                 title='Confirmed vs Deaths',
                 color_discrete_sequence=px.colors.qualitative.Vivid)
fig.update_traces(textposition='top center')
fig.update_layout(showlegend=False)
fig.update_layout(xaxis_rangeslider_visible=True)
fig.show()


# In[104]:


fig = px.scatter(temp, x='Population', y='TotalCases', color='WHO Region', 
                 height=700, hover_name='Country/Region', log_x=True, log_y=True, 
                 title='Population vs Confirmed',
                 color_discrete_sequence=px.colors.qualitative.Vivid)
fig.update_traces(textposition='top center')
fig.update_layout(showlegend=False)
fig.update_layout(xaxis_rangeslider_visible=True)
fig.show()


# In[105]:


px.bar(who_g, x="Date", y="Confirmed", color='WHO Region', 
       height=600, title='Confirmed', 
       color_discrete_sequence=px.colors.qualitative.Vivid)


# In[106]:


px.bar(who_g, x="Date", y="New cases", color='WHO Region', 
       height=600, title='New cases', 
       color_discrete_sequence=px.colors.qualitative.Vivid)


# In[67]:


px.box(worldometer_data, x='WHO Region', y='TotalCases', color='WHO Region',
       title='Distribution of country wise no. of cases in different WHO Region')


# In[108]:


full_grouped['Week No.'] = full_grouped['Date'].dt.strftime('%U')
week_wise = full_grouped.groupby('Week No.')['Confirmed', 'Deaths', 'Recovered', 'Active', 'New cases', 'New deaths', 'New recovered'].sum().reset_index()


# In[109]:


def plot_weekwise(col, hue):
    fig = px.bar(week_wise, x="Week No.", y=col, width=700, color_discrete_sequence=[hue])
    fig.update_layout(title=col, xaxis_title="", yaxis_title="")
    fig.show()


# In[110]:


plot_weekwise('Confirmed', '#000000')


# In[111]:


plot_weekwise('Deaths', dth)


# In[112]:


plot_weekwise('New cases', '#cd6684')


# In[113]:


full_grouped['Month'] = pd.DatetimeIndex(full_grouped['Date']).month
month_wise = full_grouped.groupby('Month')['Confirmed', 'Deaths', 'Recovered', 'Active', 'New cases', 'New deaths', 'New recovered'].sum().reset_index()


# In[114]:


def plot_monthwise(col, hue):
    fig = px.bar(month_wise, x="Month", y=col, width=700, color_discrete_sequence=[hue])
    fig.update_layout(title=col, xaxis_title="", yaxis_title="")
    fig.show()


# In[115]:


plot_monthwise('Confirmed', '#000000')


# In[116]:


plot_monthwise('Deaths', dth)


# In[117]:


plot_monthwise('New cases', '#cd6684')


# In[118]:


temp = country_wise[country_wise['Active']==0]
temp = temp.sort_values('Confirmed', ascending=False)
temp.reset_index(drop=True)


# In[119]:


happiness_report = pd.read_csv('World Happiness Report/2019.csv')
happiness_report = happiness_report[['Country or region', 'Healthy life expectancy']]

temp = country_wise.merge(happiness_report, left_on='Country/Region', right_on='Country or region')
px.scatter(temp, y='Deaths / 100 Cases', x='Healthy life expectancy', color='WHO Region', hover_data=['Country/Region'])


# In[ ]:





# In[ ]:





# In[ ]:




