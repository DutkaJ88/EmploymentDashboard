# Import needed libraries
import pandas as pd
import requests
from bs4 import BeautifulSoup
import streamlit as st
import plotly.express as px
import folium
import geopandas
from streamlit_folium import st_folium

st.set_page_config(layout="wide")

@st.cache_data
def make_list():
    # Use beautifulsoup to get all links from the data download pages that are xlsx files and put them in a list
    url = "https://labourmarketinsights.gov.au/regions/data-downloads/all-regions-abs-sa4-downloads/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    links = soup.find_all("a")
    xlsxfiles = [link.get("href") for link in links if link.get("href") is not None and link.get("href").endswith(".xlsx")]
    # print(xlsxfiles)
    # Add the correct prefix to list xlsxfiles
    prefix = "https://labourmarketinsights.gov.au"
    fullxlsx = []
    for link in xlsxfiles:
        fullxlsx.append(prefix + link)
    return fullxlsx
    # print(fullxlsx)

@st.cache_data
def make_date(anylink):
    dateString = anylink.partition('_')[2]
    dateString = dateString.partition('.')[0]
    dateString = dateString.capitalize()
    return dateString

@st.cache_data
def make_qldsnapshotdf(link):
    df = pd.read_excel(link, sheet_name=2)
    df.drop(df[df['Region'] != "Queensland"].index, inplace = True)
    df.reset_index(drop=True, inplace=True)
    return df

@st.cache_data
def make_regionsnapshotdf(link):
    df = pd.read_excel(link, sheet_name=1)
    return df

@st.cache_data
def make_Msnap(dataFrame):
    df = dataFrame.loc[dataFrame['Region'] == "Darling Downs - Maranoa"]
    df = df.drop('State/Territory', axis=1)
    df.reset_index(drop=True, inplace=True)
    return df

@st.cache_data
def make_Tsnap(dataFrame):
    df = dataFrame.loc[dataFrame['Region'] == "Toowoomba"]
    df = df.drop('State/Territory', axis=1)
    df.reset_index(drop=True, inplace=True)
    return df

@st.cache_data
def make_qtimedf(link):
    df = pd.read_excel(link, sheet_name=2)
    df = df.sort_values(by=['Date'])
    df.drop(df[df['State/Territory'] != "QLD"].index, inplace = True)
    df = df.tail(60)
    df.reset_index(drop=True, inplace=True)
    return df

@st.cache_data
def make_regiontdf(link):
    df = pd.read_excel(timelink, sheet_name=1)
    return df

@st.cache_data
def make_mtimedf(dataFrame):
    df = dataFrame.loc[dataFrame['Region'] == "Darling Downs - Maranoa"]
    df = df.sort_values(by=['Date'])
    df = df.drop('State/Territory', axis=1)
    df = df.tail(60)
    df.reset_index(drop=True, inplace=True)
    return df

@st.cache_data
def make_ttimedf(dataFrame):
    df = dataFrame.loc[dataFrame['Region'] == "Toowoomba"]
    df = df.sort_values(by=['Date'])
    df = df.drop('State/Territory', axis=1)
    df = df.tail(60)
    df.reset_index(drop=True, inplace=True)
    return df

@st.cache_data
def make_qldlfdf():
    df = pd.read_excel(labourforcelink, sheet_name=2)
    df.drop(df[df['Region Name'] != "Queensland"].index, inplace = True)
    df.reset_index(drop=True, inplace=True)
    return df

@st.cache_data
def make_regionlfdf():
    df = pd.read_excel(labourforcelink, sheet_name=1)
    return df

@st.cache_data
def make_mlfdf(dataFrame):
    df = dataFrame.loc[dataFrame['Region Name'] == "Darling Downs - Maranoa"]
    df = df.drop('State/Territory', axis=1)
    df.reset_index(drop=True, inplace=True)
    return df

@st.cache_data
def make_tlfdf(dataFrame):
    df = dataFrame.loc[dataFrame['Region Name'] == "Toowoomba"]
    df = df.drop('State/Territory', axis=1)
    df.reset_index(drop=True, inplace=True)
    return df

@st.cache_data
def make_qldagedf():
    df = pd.read_excel(agelink, sheet_name=2)
    df.drop(df[df['Region Name'] != "Queensland"].index, inplace = True)
    df = df.sort_values(by='Age Group', ascending=False)
    df.reset_index(drop=True, inplace=True)
    return df

@st.cache_data
def make_regionagedf():
    df = pd.read_excel(agelink, sheet_name=1)
    return df

@st.cache_data
def make_magedf(dataFrame):
    df = dataFrame.loc[dataFrame['Region Name'] == "Darling Downs - Maranoa"]
    df = df.drop('State/Territory', axis=1)
    df = df.sort_values(by='Age Group', ascending=False)
    df.reset_index(drop=True, inplace=True)
    return df

@st.cache_data
def make_tagedf(dataFrame):
    df = dataFrame.loc[dataFrame['Region Name'] == "Toowoomba"]
    df = df.drop('State/Territory', axis=1)
    df = df.sort_values(by='Age Group', ascending=False)
    df.reset_index(drop=True, inplace=True)
    return df

@st.cache_data
def make_qeidf():
    df = pd.read_excel(employmentindustrylink, sheet_name=2)
    df.drop(df[df['Region Name'] != "Queensland"].index, inplace = True)
    df.reset_index(drop=True, inplace=True)
    return df

@st.cache_data
def make_regioneidf():
    df = pd.read_excel(employmentindustrylink, sheet_name=1)
    return df

@st.cache_data
def make_meidf(dataFrame):
    df = dataFrame.loc[dataFrame['Region Name'] == "Darling Downs - Maranoa"]
    df = df.drop('State/Territory', axis=1)
    df.reset_index(drop=True, inplace=True)
    return df

@st.cache_data
def make_teidf(dataFrame):
    df = dataFrame.loc[dataFrame['Region Name'] == "Toowoomba"]
    df = df.drop('State/Territory', axis=1)
    df.reset_index(drop=True, inplace=True)
    return df

@st.cache_data
def make_mtipdf():
    df = pd.read_excel(employmentprojectionlink, sheet_name=1, skiprows=[0,1], header=0, names=['Region Name','Proxy Region (Greater City / Rest of State)','State/Territory','Industry','Projected Growth (\'000)','Projected Growth (%)'])
    df2 = df.loc[df['Region Name'] == "Darling Downs - Maranoa"]
    df2 = df2.drop('State/Territory', axis=1)
    df2 = df2.drop('Proxy Region (Greater City / Rest of State)', axis=1) 
    df2.reset_index(drop=True, inplace=True)
    return df2

@st.cache_data
def make_qodf():
    df = pd.read_excel(occupationlink, sheet_name=2)
    df.drop(df[df['Region Name'] != "Queensland"].index, inplace = True)
    df.reset_index(drop=True, inplace=True)
    return df

@st.cache_data
def make_regionodf():
    df = pd.read_excel(occupationlink, sheet_name=1)
    return df

@st.cache_data
def make_todf(dataFrame):
    df = dataFrame.loc[dataFrame['Region Name'] == "Toowoomba"]
    df = df.drop('State/Territory', axis=1)
    df.reset_index(drop=True, inplace=True)
    return df

@st.cache_data
def make_modf(dataFrame):
    df = dataFrame.loc[dataFrame['Region Name'] == "Darling Downs - Maranoa"]
    df = df.drop('State/Territory', axis=1)
    df.reset_index(drop=True, inplace=True)
    return df

@st.cache_data
def make_qoedf():
    df = pd.read_excel(occupationemploymentlink, sheet_name=2)
    df.drop(df[df['Region Name'] != "Queensland"].index, inplace = True)
    df.reset_index(drop=True, inplace=True)
    return df

@st.cache_data
def make_regionoedf():
    df = pd.read_excel(occupationemploymentlink, sheet_name=1)
    return df

@st.cache_data
def make_toedf(dataFrame):
    df = dataFrame.loc[dataFrame['Region Name'] == "Toowoomba"]
    df = df.drop('State/Territory', axis=1)
    df.reset_index(drop=True, inplace=True)
    return df

@st.cache_data
def make_moedf(dataFrame):
    df = dataFrame.loc[dataFrame['Region Name'] == "Darling Downs - Maranoa"]
    df = df.drop('State/Territory', axis=1)
    df.reset_index(drop=True, inplace=True)
    return df

@st.cache_data
def make_sa4Areas():
    sa4Areas = geopandas.read_file('https://www.abs.gov.au/statistics/standards/australian-statistical-geography-standard-asgs-edition-3/jul2021-jun2026/access-and-downloads/digital-boundary-files/SA4_2021_AUST_SHP_GDA2020.zip')
    #'https://www.abs.gov.au/statistics/standards/australian-statistical-geography-standard-asgs-edition-3/jul2021-jun2026/access-and-downloads/digital-boundary-files/SA4_2021_AUST_SHP_GDA2020.zip'
    return sa4Areas

# Initialise variable of every list item, alternatively you could manually place links here for each xlsx file
snapshotlink = make_list()[0]
timelink = make_list()[1]
labourforcelink = make_list()[2]
agelink = make_list()[3]
employmentindustrylink = make_list()[4]
employmentprojectionlink = make_list()[5]
occupationlink = make_list()[6]
occupationemploymentlink = make_list()[7]

#Create a string that contains the date of the data
dateString = make_date(snapshotlink)
dateStringProjections = make_date(employmentprojectionlink)
dateStringLF = make_date(labourforcelink)
dateStringAge = make_date(agelink)
dateStringEI = make_date(employmentindustrylink)
dateStringLO = make_date(occupationlink)
dateStringOE = make_date(occupationemploymentlink)
# print(dateString)

# Create dataframe for Queensland snapshot data
qldsnapshotdf = make_qldsnapshotdf(snapshotlink)
# print(qldsnapshotdf)

# Create dataframe for all regions of snapshot data
regionsnapshotdf = make_regionsnapshotdf(snapshotlink)

# Create dataframe for snapshot of Maranoa
maranoasnapshotdf = make_Msnap(regionsnapshotdf)
# print(maranoasnapshotdf)

# Create dataframe for snapshot of Toowoomba
toowoombasnapshotdf = make_Tsnap(regionsnapshotdf)
# print(toowoombasnapshotdf)

# Create dataframe for time series of Queensland
qldtimedf = make_qtimedf(timelink)

qtUEmaxdf = qldtimedf[qldtimedf.iloc[:,3] == qldtimedf.iloc[:,3].max()]
qtUEmindf = qldtimedf[qldtimedf.iloc[:,3] == qldtimedf.iloc[:,3].min()]
qtEmaxdf = qldtimedf[qldtimedf.iloc[:,2] == qldtimedf.iloc[:,2].max()]
qtEmindf = qldtimedf[qldtimedf.iloc[:,2] == qldtimedf.iloc[:,2].min()]
qtPmaxdf = qldtimedf[qldtimedf.iloc[:,4] == qldtimedf.iloc[:,4].max()]
qtPmindf = qldtimedf[qldtimedf.iloc[:,4] == qldtimedf.iloc[:,4].min()]
# print(qldtimedf)

# Create dataframe for time series of region
regiontimedf = make_regiontdf(timelink)

# Create dataframe for time series of Maranoa
maranoatimedf = make_mtimedf(regiontimedf)
# print(maranoatimedf)

mtUEmaxdf = maranoatimedf[maranoatimedf.iloc[:,3] == maranoatimedf.iloc[:,3].max()]
mtUEmindf = maranoatimedf[maranoatimedf.iloc[:,3] == maranoatimedf.iloc[:,3].min()]
mtEmaxdf = maranoatimedf[maranoatimedf.iloc[:,2] == maranoatimedf.iloc[:,2].max()]
mtEmindf = maranoatimedf[maranoatimedf.iloc[:,2] == maranoatimedf.iloc[:,2].min()]
mtPmaxdf = maranoatimedf[maranoatimedf.iloc[:,4] == maranoatimedf.iloc[:,4].max()]
mtPmindf = maranoatimedf[maranoatimedf.iloc[:,4] == maranoatimedf.iloc[:,4].min()]

# Create dataframe for time series of Toowoomba
toowoombatimedf = make_ttimedf(regiontimedf)
# print(toowoombatimedf)

ttUEmaxdf = toowoombatimedf[toowoombatimedf.iloc[:,3] == toowoombatimedf.iloc[:,3].max()]
ttUEmindf = toowoombatimedf[toowoombatimedf.iloc[:,3] == toowoombatimedf.iloc[:,3].min()]
ttEmaxdf = toowoombatimedf[toowoombatimedf.iloc[:,2] == toowoombatimedf.iloc[:,2].max()]
ttEmindf = toowoombatimedf[toowoombatimedf.iloc[:,2] == toowoombatimedf.iloc[:,2].min()]
ttPmaxdf = toowoombatimedf[toowoombatimedf.iloc[:,4] == toowoombatimedf.iloc[:,4].max()]
ttPmindf = toowoombatimedf[toowoombatimedf.iloc[:,4] == toowoombatimedf.iloc[:,4].min()]

qldlfdf = make_qldlfdf()
regionlfdf = make_regionlfdf()
mlfdf = make_mlfdf(regionlfdf)
tlfdf = make_tlfdf(regionlfdf)

qagedf = make_qldagedf()
regionagedf = make_regionagedf()
magedf = make_magedf(regionagedf)
tagedf = make_tagedf(regionagedf)

qeidf = make_qeidf()
regioneidf = make_regioneidf()
meidf = make_meidf(regioneidf)
teidf = make_teidf(regioneidf)

mtepdf = make_mtipdf()

qodf = make_qodf()
regionodf = make_regionodf()
modf = make_modf(regionodf)
todf = make_todf(regionodf)

qoedf = make_qoedf()
regionoedf = make_regionoedf()
moedf = make_moedf(regionoedf)
toedf = make_toedf(regionoedf)

strPercent = '%'
st.title('Employment Dashboard')


def map_func():
    st.markdown('# Map Information')
    with st.container():
        col1,col2 = st.columns(2)
        with col1:
            st.write('## Toowoomba SA4')
            sa4AreasT = make_sa4Areas()
            sa4AreasT = sa4AreasT.iloc[[65]]
            mapt = folium.Map(location=[-27.566668, 151.949997], zoom_start=9)
            folium.GeoJson(data=sa4AreasT["geometry"]).add_to(mapt)
            st_data = st_folium(mapt, returned_objects=[])
            with st.expander("More Information"):
                st.write('More information on this object :)')
        
        with col2:
            st.write('## Darling Downs - Maranoa SA4')
            sa4AreasM = make_sa4Areas()
            sa4AreasM = sa4AreasM.iloc[[55]]
            mapm = folium.Map(location=[-27.529991, 150.582068], zoom_start=6)
            folium.GeoJson(data=sa4AreasM["geometry"]).add_to(mapm)
            st_data = st_folium(mapm, returned_objects=[])
            with st.expander("More Information"):
                st.write('More information on this object :)')

@st.cache_data
def snapshot_func():
    st.markdown('# Snapshot Data')
    st.markdown('## Unemployment Rate')
    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write('### Toowoomba SA4')
            st.write('Data from: ', dateString)
            st.metric(label='Unemployment Rate', value=str(toowoombasnapshotdf.iloc[0][5])+strPercent)
            st.write('Last 5 years')
            st.metric(label='Minimum Unemployment Rate:', value=str(ttUEmindf.iloc[-1][3])+strPercent)
            st.write('On ',ttUEmindf.iloc[-1,1].strftime('%B-%Y'))
            st.metric(label='Maximum Unemployment Rate:', value=str(ttUEmaxdf.iloc[-1][3])+strPercent)
            st.write('On ',ttUEmaxdf.iloc[-1,1].strftime('%B-%Y'))

        with col2:
            st.write('### Darling Downs - Maranoa SA4')
            st.write('Data from: ', dateString)
            st.metric(label='Unemployment Rate', value=str(maranoasnapshotdf.iloc[0][5])+strPercent)
            st.write('Last 5 years')
            st.metric(label='Minimum Unemployment Rate:', value=str(mtUEmindf.iloc[-1][3])+strPercent)
            st.write('On ',mtUEmindf.iloc[-1,1].strftime('%B-%Y'))
            st.metric(label='Maximum Unemployment Rate:', value=str(mtUEmaxdf.iloc[-1][3])+strPercent)
            st.write('On ',mtUEmaxdf.iloc[-1,1].strftime('%B-%Y'))

        with col3:
            st.write('### Queensland SA4')
            st.write('Data from: ', dateString)
            st.metric(label='Unemployment Rate', value=str(qldsnapshotdf.iloc[0][5])+strPercent)
            st.write('Last 5 years')
            st.metric(label='Minimum Unemployment Rate:', value=str(qtUEmindf.iloc[-1][3])+strPercent)
            st.write('On ',qtUEmindf.iloc[-1,1].strftime('%B-%Y'))
            st.metric(label='Maximum Unemployment Rate:', value=str(qtUEmaxdf.iloc[-1][3])+strPercent)
            st.write('On ',qtUEmaxdf.iloc[-1,1].strftime('%B-%Y'))
            
        with st.expander("More Information"):
            st.write('More information on this object :)')

    st.markdown('## Employment Rate')
    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write('### Toowoomba SA4')
            st.write('Data from: ', dateString)
            st.metric(label='Employment Rate', value=str(toowoombasnapshotdf.iloc[0][3])+strPercent)
            st.write('Last 5 years')
            st.metric(label='Minimum Employment Rate:', value=str(ttEmindf.iloc[-1][2])+strPercent)
            st.write('On ',ttEmindf.iloc[-1,1].strftime('%B-%Y'))
            st.metric(label='Maximum Employment Rate:', value=str(ttEmaxdf.iloc[-1][2])+strPercent)
            st.write('On ',ttEmaxdf.iloc[-1,1].strftime('%B-%Y'))

        with col2:
            st.write('### Darling Downs - Maranoa SA4')
            st.write('Data from: ', dateString)
            st.metric(label='Employment Rate', value=str(maranoasnapshotdf.iloc[0][3])+strPercent)
            st.write('Last 5 years')
            st.metric(label='Minimum Employment Rate:', value=str(mtEmindf.iloc[-1][2])+strPercent)
            st.write('On ',mtEmindf.iloc[-1,1].strftime('%B-%Y'))
            st.metric(label='Maximum Employment Rate:', value=str(mtEmaxdf.iloc[-1][2])+strPercent)
            st.write('On ',mtEmaxdf.iloc[-1,1].strftime('%B-%Y'))


        with col3:
            st.write('### Queensland SA4')
            st.write('Data from: ', dateString)
            st.metric(label='Employment Rate', value=str(qldsnapshotdf.iloc[0][3])+strPercent)
            st.write('Last 5 years')
            st.metric(label='Minimum Employment Rate:', value=str(qtEmindf.iloc[-1][2])+strPercent)
            st.write('On ',qtEmindf.iloc[-1,1].strftime('%B-%Y'))
            st.metric(label='Maximum Employment Rate:', value=str(qtEmaxdf.iloc[-1][2])+strPercent)
            st.write('On ',qtEmaxdf.iloc[-1,1].strftime('%B-%Y'))
            
        with st.expander("More Information"):
            st.write('More information on this object :)')

    st.markdown('## Participation Rate')
    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write('### Toowoomba SA4')
            st.write('Data from: ', dateString)
            st.metric(label='Participation Rate', value=str(toowoombasnapshotdf.iloc[0][4])+strPercent)
            st.write('Last 5 years')
            st.metric(label='Minimum Participation Rate:', value=str(ttPmindf.iloc[-1][4])+strPercent)
            st.write('On ',ttPmindf.iloc[-1,1].strftime('%B-%Y'))
            st.metric(label='Maximum Participation Rate:', value=str(ttPmaxdf.iloc[-1][4])+strPercent)
            st.write('On ',ttPmaxdf.iloc[-1,1].strftime('%B-%Y'))

        with col2:
            st.write('### Darling Downs - Maranoa SA4')
            st.write('Data from: ', dateString)
            st.metric(label='Participation Rate', value=str(maranoasnapshotdf.iloc[0][4])+strPercent)
            st.write('Last 5 years')
            st.metric(label='Minimum Participation Rate:', value=str(mtPmindf.iloc[-1][4])+strPercent)
            st.write('On ',mtPmindf.iloc[-1,1].strftime('%B-%Y'))
            st.metric(label='Maximum Participation Rate:', value=str(mtPmaxdf.iloc[-1][4])+strPercent)
            st.write('On ',mtPmaxdf.iloc[-1,1].strftime('%B-%Y'))

        with col3:
            st.write('### Queensland SA4')
            st.write('Data from: ', dateString)
            st.metric(label='Participation Rate', value=str(qldsnapshotdf.iloc[0][4])+strPercent)
            st.write('Last 5 years')
            st.metric(label='Minimum Participation Rate:', value=str(qtEmindf.iloc[-1][4])+strPercent)
            st.write('On ',qtEmindf.iloc[-1,1].strftime('%B-%Y'))
            st.metric(label='Maximum Participation Rate:', value=str(qtEmaxdf.iloc[-1][4])+strPercent)
            st.write('On ',qtEmaxdf.iloc[-1,1].strftime('%B-%Y'))
            
        with st.expander("More Information"):
            st.write('More information on this object :)')

    st.markdown('### Other Key Figures')
    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write('### Toowoomba SA4')
            st.write('Data from: ', dateString)
            st.metric(label='Youth Unemployment (15-24yrs):', value=str(toowoombasnapshotdf.iloc[0][6])+strPercent)
            st.metric(label='Working Age Population (15-64yrs): ', value=str(toowoombasnapshotdf.iloc[0][1]))
            st.metric(label='Employed Population (15+ yrs): ', value=str(toowoombasnapshotdf.iloc[0][2]))

        with col2:
            st.write('### Darling Downs - Maranoa SA4')
            st.write('Data from: ', dateString)
            st.metric(label='Youth Unemployment (15-24yrs):', value=str(maranoasnapshotdf.iloc[0][6])+strPercent)
            st.metric(label='Working Age Population (15-64yrs): ', value=str(maranoasnapshotdf.iloc[0][1]))
            st.metric(label='Employed Population (15+ yrs): ', value=str(maranoasnapshotdf.iloc[0][2]))

        with col3:
            st.write('### Queensland SA4')
            st.write('Data from: ', dateString)
            st.metric(label='Youth Unemployment (15-24yrs):', value=str(qldsnapshotdf.iloc[0][6])+strPercent)
            st.metric(label='Working Age Population (15-64yrs): ', value=str(qldsnapshotdf.iloc[0][1]))
            st.metric(label='Employed Population (15+ yrs): ', value=str(qldsnapshotdf.iloc[0][2]))
            
        with st.expander("More Information"):
            st.write('More information on this object :)')

def timeseries_func():
    st.markdown('# Time Series Data')
    percent_label = "(%)"
    with st.container():
        st.write('### Toowoomba SA4')
        st.write('Data from: ', dateString, ', displaying the last 5 years')
        y_axis_valuet = st.selectbox('Select Toowoomba Time Series Data', options=toowoombatimedf.columns[-3:])
        y_axis_valuet_title = y_axis_valuet + percent_label
        figtt = px.line(toowoombatimedf, x='Date', y=y_axis_valuet).update_layout(yaxis_title=y_axis_valuet_title)
        st.plotly_chart(figtt)
        with st.expander("More Information"):
            st.write('More information on this object :)')
    
    with st.container():
        st.write('### Darling Downs - Maranoa SA4')
        st.write('Data from: ', dateString, ', displaying the last 5 years')
        y_axis_valuem = st.selectbox('Select Darling Downs - Maranoa Time Series Data', options=maranoatimedf.columns[-3:])
        y_axis_valuem_title = y_axis_valuem + percent_label
        figtm = px.line(maranoatimedf, x='Date', y=y_axis_valuem).update_layout(yaxis_title=y_axis_valuem_title)
        st.plotly_chart(figtm)
        with st.expander("More Information"):
            st.write('More information on this object :)')
    
    with st.container():
        st.write('### Queensland')
        st.write('Data from: ', dateString, ', displaying the last 5 years')
        y_axis_valueq = st.selectbox('Select Queensland Time Series Data', options=qldtimedf.columns[-3:])
        y_axis_valueq_title = y_axis_valueq + percent_label
        figtq = px.line(qldtimedf, x='Date', y=y_axis_valueq).update_layout(yaxis_title=y_axis_valueq_title)
        st.plotly_chart(figtq)
        with st.expander("More Information"):
            st.write('More information on this object :)')

@st.cache_data
def labourforce_func():
    st.markdown('# Labour Force Data')
    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write('### Toowoomba SA4')
            st.write('Data from: ', dateStringLF)
            tlftotal = tlfdf.iloc[0][2] + tlfdf.iloc[1][2] + tlfdf.iloc[2][2] + tlfdf.iloc[3][2]
            st.metric(label='Employed Full-time Persons', value=str(tlfdf.iloc[0][2])+', '+str(round((tlfdf.iloc[0][2]/tlftotal*100), 1))+strPercent)
            st.metric(label='Employed Part-time Persons', value=str(tlfdf.iloc[1][2])+', '+str(round((tlfdf.iloc[1][2]/tlftotal*100), 1))+strPercent)
            st.metric(label='Unemployed Total', value=str(tlfdf.iloc[2][2])+', '+str(round((tlfdf.iloc[2][2]/tlftotal*100), 1))+strPercent)
            st.metric(label='Not in the Labour Force', value=str(tlfdf.iloc[3][2])+', '+str(round((tlfdf.iloc[3][2]/tlftotal*100), 1))+strPercent)

        with col2:
            st.write('### Darling Downs - Maranoa SA4')
            st.write('Data from: ', dateStringLF)
            mlftotal = mlfdf.iloc[0][2] + mlfdf.iloc[1][2] + mlfdf.iloc[2][2] + mlfdf.iloc[3][2]
            st.metric(label='Employed Full-time Persons', value=str(mlfdf.iloc[0][2])+', '+str(round((mlfdf.iloc[0][2]/mlftotal*100), 1))+strPercent)
            st.metric(label='Employed Part-time Persons', value=str(mlfdf.iloc[1][2])+', '+str(round((mlfdf.iloc[1][2]/mlftotal*100), 1))+strPercent)
            st.metric(label='Unemployed Total', value=str(mlfdf.iloc[2][2])+', '+str(round((mlfdf.iloc[2][2]/mlftotal*100), 1))+strPercent)
            st.metric(label='Not in the Labour Force', value=str(mlfdf.iloc[3][2])+', '+str(round((mlfdf.iloc[3][2]/mlftotal*100), 1))+strPercent)

        with col3:
            st.write('### Queensland SA4')
            st.write('Data from: ', dateStringLF)
            qlftotal = qldlfdf.iloc[0][2] + qldlfdf.iloc[1][2] + qldlfdf.iloc[2][2] + qldlfdf.iloc[3][2]
            st.metric(label='Employed Full-time Persons', value=str(qldlfdf.iloc[0][2])+', '+str(round((qldlfdf.iloc[0][2]/qlftotal*100), 1))+strPercent)
            st.metric(label='Employed Part-time Persons', value=str(qldlfdf.iloc[1][2])+', '+str(round((qldlfdf.iloc[1][2]/qlftotal*100), 1))+strPercent)
            st.metric(label='Unemployed Total', value=str(qldlfdf.iloc[2][2])+', '+str(round((qldlfdf.iloc[2][2]/qlftotal*100), 1))+strPercent)
            st.metric(label='Not in the Labour Force', value=str(qldlfdf.iloc[3][2])+', '+str(round((qldlfdf.iloc[3][2]/qlftotal*100), 1))+strPercent)
            
        with st.expander("More Information"):
            st.write('More information on this object :)')

    st.markdown('# Labour Force Age Data')
    with st.container():
            st.write('### Toowoomba SA4')
            st.write('Data from: ', dateStringAge)
            figat = px.bar(tagedf, x=tagedf.columns[2], y=tagedf.columns[1], text=tagedf.columns[3])
            st.plotly_chart(figat)
            st.write('Combined Age Group total of (55 to 64) and (over 65) years old: ', tagedf.iloc[0][2]+tagedf.iloc[1][2], ', ', tagedf.iloc[0][3]+tagedf.iloc[1][3], '%')
            with st.expander("More Information"):
                st.write('More information on this object :)')
    with st.container():
            st.write('### Darling downs - Maranoa SA4')
            st.write('Data from: ', dateStringAge)
            figam = px.bar(magedf, x=magedf.columns[2], y=magedf.columns[1], text=magedf.columns[3])
            st.plotly_chart(figam)
            st.write('Combined Age Group total of (55 to 64) and (over 65) years old: ', magedf.iloc[0][2]+magedf.iloc[1][2], ', ', magedf.iloc[0][3]+magedf.iloc[1][3], '%')
            with st.expander("More Information"):
                st.write('More information on this object :)')
    with st.container():
            st.write('### Queensland')
            st.write('Data from: ', dateStringAge)
            figaq = px.bar(qagedf, x=qagedf.columns[2], y=qagedf.columns[1], text=qagedf.columns[3])
            st.plotly_chart(figaq)
            st.write('Combined Age Group total of (55 to 64) and (over 65) years old: ', qagedf.iloc[0][2]+qagedf.iloc[1][2], ', ', qagedf.iloc[1][3]+qagedf.iloc[1][3], '%')
            with st.expander("More Information"):
                st.write('More information on this object :)')

def employmentindustry_func():
    st.markdown('# Employment by Industry')
    with st.container():
        st.write('### Toowoomba SA4')
        st.write('Data from: ', dateStringEI)
        x_axis_value = st.selectbox('Select Toowoomba Industry Employment Figure', options=teidf.columns[2:7])
        figeit = px.bar(teidf, x=x_axis_value, y=teidf.columns[1])
        st.plotly_chart(figeit)
        figeipiet = px.pie(teidf, values=teidf.columns[7], names=teidf.columns[1], title=teidf.columns[7]).update_layout(legend_itemclick=False)
        st.plotly_chart(figeipiet)
        with st.expander("More Information"):
            st.write('More information on this object :)')
    
    with st.container():
        st.write('### Darling downs - Maranoa SA4')
        st.write('Data from: ', dateStringEI)
        x_axis_value = st.selectbox('Select Darling Down - Maranoa Industry Employment Figure', options=meidf.columns[2:7])
        figeim = px.bar(meidf, x=x_axis_value, y=meidf.columns[1])
        st.plotly_chart(figeim)
        figeipiem = px.pie(meidf, values=meidf.columns[7], names=meidf.columns[1], title=meidf.columns[7]).update_layout(legend_itemclick=False)
        st.plotly_chart(figeipiem)
        with st.expander("More Information"):
            st.write('More information on this object :)')

    with st.container():
        st.write('### Queensland')
        st.write('Data from: ', dateStringEI)
        x_axis_value = st.selectbox('Select Queensland Industry Employment Figure', options=qeidf.columns[2:7])
        figeiq = px.bar(qeidf, x=x_axis_value, y=qeidf.columns[1])
        st.plotly_chart(figeiq)
        figeipieq = px.pie(qeidf, values=qeidf.columns[7], names=qeidf.columns[1], title=qeidf.columns[7]).update_layout(legend_itemclick=False)
        st.plotly_chart(figeipieq)
        with st.expander("More Information"):
            st.write('More information on this object :)')

@st.cache_data
def employmentprojections_func():
    st.markdown('# Employment Projections for Next 5 Years')
    st.markdown('### Toowoomba and Darling Downs - Maranoa')
    st.write('Data from: ', dateStringProjections)
    mask = mtepdf[mtepdf['Industry'] != 'Total (industry)']
    figep = px.bar(mask, x=mask.columns[2], y=mask.columns[1])
    st.plotly_chart(figep)
    st.write('Expected total job industry growth is: ', int(mtepdf.iloc[19][2]*1000))
    figep2 = px.bar(mtepdf, x=mtepdf.columns[3], y=mtepdf.columns[1])
    st.plotly_chart(figep2)
    with st.expander("More Information"):
            st.write('More information on this object :)')

@st.cache_data
def largestoccupations_func():
    st.markdown('# Largest Employing Occupations')

    with st.container():
        st.markdown('### Toowoomba SA4')
        st.write('Data from: ', dateStringLO)
        figot = px.bar(todf, x=todf.columns[2], y=todf.columns[1])
        st.plotly_chart(figot)
        with st.expander("More Information"):
            st.write('More information on this object :)')

    with st.container():
        st.markdown('### Darling Downs - Maranoa SA4')
        st.write('Data from: ', dateStringLO)
        figom = px.bar(modf, x=modf.columns[2], y=modf.columns[1])
        st.plotly_chart(figom)
        with st.expander("More Information"):
            st.write('More information on this object :)')

    with st.container():
        st.markdown('### Queensland')
        st.write('Data from: ', dateStringLO)
        figoq = px.bar(qodf, x=qodf.columns[2], y=qodf.columns[1])
        st.plotly_chart(figoq)
        with st.expander("More Information"):
            st.write('More information on this object :)')

def employingoccupations_func():
    st.markdown('# Current Employing Occupations')
    with st.container():
        st.write('### Toowoomba SA4')
        st.write('Data from: ', dateStringOE)
        x_axis_value = st.selectbox('Select Toowoomba Occupation Employment Figure', options=toedf.columns[2:7])
        figoet = px.bar(toedf, x=x_axis_value, y=toedf.columns[1])
        st.plotly_chart(figoet)
        figoepiet = px.pie(toedf, values=toedf.columns[7], names=toedf.columns[1], title=toedf.columns[7]).update_layout(legend_itemclick=False)
        st.plotly_chart(figoepiet)
        with st.expander("More Information"):
            st.write('More information on this object :)')
    
    with st.container():
        st.write('### Darling downs - Maranoa SA4')
        st.write('Data from: ', dateStringOE)
        x_axis_value = st.selectbox('Select Darling Down - Maranoa Occupation Employment Figure', options=moedf.columns[2:7])
        figoem = px.bar(moedf, x=x_axis_value, y=moedf.columns[1])
        st.plotly_chart(figoem)
        figoepiem = px.pie(moedf, values=moedf.columns[7], names=moedf.columns[1], title=moedf.columns[7]).update_layout(legend_itemclick=False)
        st.plotly_chart(figoepiem)
        with st.expander("More Information"):
            st.write('More information on this object :)')

    with st.container():
        st.write('### Queensland')
        st.write('Data from: ', dateStringOE)
        x_axis_value = st.selectbox('Select Queensland Occupation Employment Figure', options=qoedf.columns[2:7])
        figoeq = px.bar(qoedf, x=x_axis_value, y=qoedf.columns[1])
        st.plotly_chart(figoeq)
        figoepieq = px.pie(qoedf, values=qoedf.columns[7], names=qoedf.columns[1], title=qoedf.columns[7]).update_layout(legend_itemclick=False)
        st.plotly_chart(figoepieq)
        with st.expander("More Information"):
            st.write('More information on this object :)')

st.sidebar.title('Navigation')
options = st.sidebar.radio('Pages', options = ['Maps', 'Snapshot Data', 'Time Series Data', 'Labour Force Data', 'Employment by Industry', 'Employment Projections', 'Largest Employing Occupations', 'Current Employing Occupations'])

if options == 'Snapshot Data':
    snapshot_func()
elif options == 'Maps':
    map_func()
elif options == 'Time Series Data':
    timeseries_func()
elif options == 'Labour Force Data':
    labourforce_func()
elif options == 'Employment by Industry':
    employmentindustry_func()
elif options == 'Employment Projections':
    employmentprojections_func()
elif options == 'Largest Employing Occupations':
    largestoccupations_func()
elif options == 'Current Employing Occupations':
    employingoccupations_func()
