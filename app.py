# Import needed libraries
import pandas as pd
import requests
from bs4 import BeautifulSoup
import streamlit as st
import plotly.express as px
import folium
import geopandas
from streamlit_folium import st_folium

# Sets the default page layout to wide to use
st.set_page_config(layout="wide")

#hide hamburger menu so that users can't rerun the application themselves
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

# Funtion to create a list of all the excel files locations on labour market insights webpage
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

# Create a date from a file source, uses the date on the end of the excel document, will break if they change their naming conventions
@st.cache_data
def make_date(anylink):
    dateString = anylink.partition('_')[2]
    dateString = dateString.partition('.')[0]
    dateString = dateString.capitalize()
    return dateString

# Create the dataframe for the snapshot of Queensland
@st.cache_data
def make_qldsnapshotdf(link):
    df = pd.read_excel(link, sheet_name=2)
    df.drop(df[df['Region'] != "Queensland"].index, inplace = True)
    df.reset_index(drop=True, inplace=True)
    return df

# Create a dataframe for the snapshot of regional areas
@st.cache_data
def make_regionsnapshotdf(link):
    df = pd.read_excel(link, sheet_name=1)
    return df

# Create a dataframe for Maranoa snapshot
@st.cache_data
def make_Msnap(dataFrame):
    df = dataFrame.loc[dataFrame['Region'] == "Darling Downs - Maranoa"]
    df = df.drop('State/Territory', axis=1)
    df.reset_index(drop=True, inplace=True)
    return df

#Create a dataframe for Toowoomba snapshot
@st.cache_data
def make_Tsnap(dataFrame):
    df = dataFrame.loc[dataFrame['Region'] == "Toowoomba"]
    df = df.drop('State/Territory', axis=1)
    df.reset_index(drop=True, inplace=True)
    return df

#Create a dataframe for the time series data of Queensland
@st.cache_data
def make_qtimedf(link):
    df = pd.read_excel(link, sheet_name=2)
    df = df.sort_values(by=['Date'])
    df.drop(df[df['State/Territory'] != "QLD"].index, inplace = True)
    df = df.tail(60)
    df.reset_index(drop=True, inplace=True)
    return df

#Create a dataframe for the time series data of the regional areas
@st.cache_data
def make_regiontdf(link):
    df = pd.read_excel(timelink, sheet_name=1)
    return df

#Create a dataframe of the timeseries data for Maranoa
@st.cache_data
def make_mtimedf(dataFrame):
    df = dataFrame.loc[dataFrame['Region'] == "Darling Downs - Maranoa"]
    df = df.sort_values(by=['Date'])
    df = df.drop('State/Territory', axis=1)
    df = df.tail(60)
    df.reset_index(drop=True, inplace=True)
    return df

#Create a dataframe of the timeseries data for Toowoomba
@st.cache_data
def make_ttimedf(dataFrame):
    df = dataFrame.loc[dataFrame['Region'] == "Toowoomba"]
    df = df.sort_values(by=['Date'])
    df = df.drop('State/Territory', axis=1)
    df = df.tail(60)
    df.reset_index(drop=True, inplace=True)
    return df

#Create a dataframe for the labour force data of Queensland
@st.cache_data
def make_qldlfdf():
    df = pd.read_excel(labourforcelink, sheet_name=2)
    df.drop(df[df['Region Name'] != "Queensland"].index, inplace = True)
    df.reset_index(drop=True, inplace=True)
    return df

#Create a dataframe for the labour force data of the regional areas
@st.cache_data
def make_regionlfdf():
    df = pd.read_excel(labourforcelink, sheet_name=1)
    return df

#Create a dataframe for the labour force data of Maranoa
@st.cache_data
def make_mlfdf(dataFrame):
    df = dataFrame.loc[dataFrame['Region Name'] == "Darling Downs - Maranoa"]
    df = df.drop('State/Territory', axis=1)
    df.reset_index(drop=True, inplace=True)
    return df

#Create a dataframe for the labour force data of Toowoomba
@st.cache_data
def make_tlfdf(dataFrame):
    df = dataFrame.loc[dataFrame['Region Name'] == "Toowoomba"]
    df = df.drop('State/Territory', axis=1)
    df.reset_index(drop=True, inplace=True)
    return df

#Create a dataframe for the labour force age data of Queensland
@st.cache_data
def make_qldagedf():
    df = pd.read_excel(agelink, sheet_name=2)
    df.drop(df[df['Region Name'] != "Queensland"].index, inplace = True)
    df = df.sort_values(by='Age Group', ascending=False)
    df.reset_index(drop=True, inplace=True)
    return df

#Create a dataframe for the labour force age data of the regional areas
@st.cache_data
def make_regionagedf():
    df = pd.read_excel(agelink, sheet_name=1)
    return df

#Create a dataframe for the labour force age data of Maranoa
@st.cache_data
def make_magedf(dataFrame):
    df = dataFrame.loc[dataFrame['Region Name'] == "Darling Downs - Maranoa"]
    df = df.drop('State/Territory', axis=1)
    df = df.sort_values(by='Age Group', ascending=False)
    df.reset_index(drop=True, inplace=True)
    return df

#Create a dataframe for the labour force age data of Toowoomba
@st.cache_data
def make_tagedf(dataFrame):
    df = dataFrame.loc[dataFrame['Region Name'] == "Toowoomba"]
    df = df.drop('State/Territory', axis=1)
    df = df.sort_values(by='Age Group', ascending=False)
    df.reset_index(drop=True, inplace=True)
    return df

#Create a dataframe for the employment by industry data of Queensland
@st.cache_data
def make_qeidf():
    df = pd.read_excel(employmentindustrylink, sheet_name=2)
    df.drop(df[df['Region Name'] != "Queensland"].index, inplace = True)
    df.reset_index(drop=True, inplace=True)
    return df

#Create a dataframe for the employment by industry data of the regional areas
@st.cache_data
def make_regioneidf():
    df = pd.read_excel(employmentindustrylink, sheet_name=1)
    return df

#Create a dataframe for the employment by industry data of Maranoa
@st.cache_data
def make_meidf(dataFrame):
    df = dataFrame.loc[dataFrame['Region Name'] == "Darling Downs - Maranoa"]
    df = df.drop('State/Territory', axis=1)
    df.reset_index(drop=True, inplace=True)
    return df

#Create a dataframe for the employment by industry data of Toowoomba
@st.cache_data
def make_teidf(dataFrame):
    df = dataFrame.loc[dataFrame['Region Name'] == "Toowoomba"]
    df = df.drop('State/Territory', axis=1)
    df.reset_index(drop=True, inplace=True)
    return df

#Create a dataframe for the employment projections of the regional areas of which include Maranoa and Toowoomba
@st.cache_data
def make_mtepdf():
    df = pd.read_excel(employmentprojectionlink, sheet_name=1, skiprows=[0,1], header=0, names=['Region Name','Proxy Region (Greater City / Rest of State)','State/Territory','Industry','Projected Growth (\'000)','Projected Growth (%)'])
    df2 = df.loc[df['Region Name'] == "Darling Downs - Maranoa"]
    df2 = df2.drop('State/Territory', axis=1)
    df2 = df2.drop('Proxy Region (Greater City / Rest of State)', axis=1) 
    df2.reset_index(drop=True, inplace=True)
    return df2

#Create a dataframe for the largest employment occupations data of Queensland
@st.cache_data
def make_qodf():
    df = pd.read_excel(occupationlink, sheet_name=2)
    df.drop(df[df['Region Name'] != "Queensland"].index, inplace = True)
    df.reset_index(drop=True, inplace=True)
    return df

#Create a dataframe for the largest employment occupations data of the regional areas
@st.cache_data
def make_regionodf():
    df = pd.read_excel(occupationlink, sheet_name=1)
    return df

#Create a dataframe for the largest employment occupations data of Maranoa
@st.cache_data
def make_todf(dataFrame):
    df = dataFrame.loc[dataFrame['Region Name'] == "Toowoomba"]
    df = df.drop('State/Territory', axis=1)
    df.reset_index(drop=True, inplace=True)
    return df

#Create a dataframe for the largest employment occupations data of Toowoomba
@st.cache_data
def make_modf(dataFrame):
    df = dataFrame.loc[dataFrame['Region Name'] == "Darling Downs - Maranoa"]
    df = df.drop('State/Territory', axis=1)
    df.reset_index(drop=True, inplace=True)
    return df

#Create a dataframe for the occupation by employment data of Queensland
@st.cache_data
def make_qoedf():
    df = pd.read_excel(occupationemploymentlink, sheet_name=2)
    df.drop(df[df['Region Name'] != "Queensland"].index, inplace = True)
    df.reset_index(drop=True, inplace=True)
    return df

#Create a dataframe for the occupation by employment data of the regional areas
@st.cache_data
def make_regionoedf():
    df = pd.read_excel(occupationemploymentlink, sheet_name=1)
    return df

#Create a dataframe for the occupation by employment data of Toowoomba
@st.cache_data
def make_toedf(dataFrame):
    df = dataFrame.loc[dataFrame['Region Name'] == "Toowoomba"]
    df = df.drop('State/Territory', axis=1)
    df.reset_index(drop=True, inplace=True)
    return df

#Create a dataframe for the occupation by employment data of Maranoa
@st.cache_data
def make_moedf(dataFrame):
    df = dataFrame.loc[dataFrame['Region Name'] == "Darling Downs - Maranoa"]
    df = df.drop('State/Territory', axis=1)
    df.reset_index(drop=True, inplace=True)
    return df

#Create a dataframe for geopandas containing the shapes of SA4 sreas in Australia
@st.cache_data
def make_sa4Areas():
    sa4Areas = geopandas.read_file('https://www.abs.gov.au/statistics/standards/australian-statistical-geography-standard-asgs-edition-3/jul2021-jun2026/access-and-downloads/digital-boundary-files/SA4_2021_AUST_SHP_GDA2020.zip')
    return sa4Areas

#Create dataframe of a specific shape of an SA4 area, input is geopandas shape dataframe from australia and the ASGS code
@st.cache_data
def make_mapArea(_dataFrame, sa4Code):
    df = _dataFrame.loc[_dataFrame['SA4_CODE21'] == sa4Code]
    return df

# Initialise variable of every excel document location, alternatively you could manually place links here for each xlsx file
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

# Create dataframe for Queensland snapshot data
qldsnapshotdf = make_qldsnapshotdf(snapshotlink)

# Create dataframe for all regions of snapshot data
regionsnapshotdf = make_regionsnapshotdf(snapshotlink)

# Create dataframe for snapshot of Maranoa
maranoasnapshotdf = make_Msnap(regionsnapshotdf)

# Create dataframe for snapshot of Toowoomba
toowoombasnapshotdf = make_Tsnap(regionsnapshotdf)

# Create dataframe for time series of Queensland
qldtimedf = make_qtimedf(timelink)

#Create min and max values for Queensland timeseries
qtUEmaxdf = qldtimedf[qldtimedf.iloc[:,3] == qldtimedf.iloc[:,3].max()]
qtUEmindf = qldtimedf[qldtimedf.iloc[:,3] == qldtimedf.iloc[:,3].min()]
qtEmaxdf = qldtimedf[qldtimedf.iloc[:,2] == qldtimedf.iloc[:,2].max()]
qtEmindf = qldtimedf[qldtimedf.iloc[:,2] == qldtimedf.iloc[:,2].min()]
qtPmaxdf = qldtimedf[qldtimedf.iloc[:,4] == qldtimedf.iloc[:,4].max()]
qtPmindf = qldtimedf[qldtimedf.iloc[:,4] == qldtimedf.iloc[:,4].min()]

# Create dataframe for time series of region
regiontimedf = make_regiontdf(timelink)

# Create dataframe for time series of Maranoa
maranoatimedf = make_mtimedf(regiontimedf)

#Create min and max values for Maranoa timeseries
mtUEmaxdf = maranoatimedf[maranoatimedf.iloc[:,3] == maranoatimedf.iloc[:,3].max()]
mtUEmindf = maranoatimedf[maranoatimedf.iloc[:,3] == maranoatimedf.iloc[:,3].min()]
mtEmaxdf = maranoatimedf[maranoatimedf.iloc[:,2] == maranoatimedf.iloc[:,2].max()]
mtEmindf = maranoatimedf[maranoatimedf.iloc[:,2] == maranoatimedf.iloc[:,2].min()]
mtPmaxdf = maranoatimedf[maranoatimedf.iloc[:,4] == maranoatimedf.iloc[:,4].max()]
mtPmindf = maranoatimedf[maranoatimedf.iloc[:,4] == maranoatimedf.iloc[:,4].min()]

# Create dataframe for time series of Toowoomba
toowoombatimedf = make_ttimedf(regiontimedf)

#Create min and max values for Toowoomba timeseries
ttUEmaxdf = toowoombatimedf[toowoombatimedf.iloc[:,3] == toowoombatimedf.iloc[:,3].max()]
ttUEmindf = toowoombatimedf[toowoombatimedf.iloc[:,3] == toowoombatimedf.iloc[:,3].min()]
ttEmaxdf = toowoombatimedf[toowoombatimedf.iloc[:,2] == toowoombatimedf.iloc[:,2].max()]
ttEmindf = toowoombatimedf[toowoombatimedf.iloc[:,2] == toowoombatimedf.iloc[:,2].min()]
ttPmaxdf = toowoombatimedf[toowoombatimedf.iloc[:,4] == toowoombatimedf.iloc[:,4].max()]
ttPmindf = toowoombatimedf[toowoombatimedf.iloc[:,4] == toowoombatimedf.iloc[:,4].min()]

#Create labour force dataframes
qldlfdf = make_qldlfdf()
regionlfdf = make_regionlfdf()
mlfdf = make_mlfdf(regionlfdf)
tlfdf = make_tlfdf(regionlfdf)

#Create labourforce age dataframes
qagedf = make_qldagedf()
regionagedf = make_regionagedf()
magedf = make_magedf(regionagedf)
tagedf = make_tagedf(regionagedf)

#Create Employment by Industry dataframes
qeidf = make_qeidf()
regioneidf = make_regioneidf()
meidf = make_meidf(regioneidf)
teidf = make_teidf(regioneidf)

#Create employment projection dataframe
mtepdf = make_mtepdf()

#Create Largest Employment OCcupation dataframes
qodf = make_qodf()
regionodf = make_regionodf()
modf = make_modf(regionodf)
todf = make_todf(regionodf)

#Create Employment by Occupation dataframes
qoedf = make_qoedf()
regionoedf = make_regionoedf()
moedf = make_moedf(regionoedf)
toedf = make_toedf(regionoedf)

#String variable for adding a percentage sign
strPercent = '%'

#Title for dashboard
st.title('Employment Dashboard')

#Function for map page
def map_func():
    st.markdown('# Map Information')
    with st.container():
        col1,col2 = st.columns(2)
        with col1:
            st.write('## Toowoomba SA4')
            sa4AreasT = make_sa4Areas()
            sa4AreasT = make_mapArea(sa4AreasT, '317')
            mapt = folium.Map(location=[-27.566668, 151.949997], zoom_start=9)
            folium.GeoJson(data=sa4AreasT["geometry"]).add_to(mapt)
            st_data = st_folium(mapt, returned_objects=[])
            with st.expander("More Information"):
                st.write('The Toowoomba Statistical Area (SA4) is located in the Darling Downs region of Queensland, Australia. It covers an area of approximately 13,000 square kilometers and encompasses the City of Toowoomba, as well as several other local government areas such as the Lockyer Valley, Southern Downs, and Goondiwindi.') 
                st.write('The area is predominantly characterized by its inland location and its rolling hills and flat plains. The landscape is mainly used for agriculture, with a variety of crops grown such as wheat, sorghum, cotton, and vegetables. There are also some areas of natural bushland, parks, and nature reserves, including the Toowoomba Range National Park and the Crows Nest National Park. ')
                st.write('Toowoomba itself is situated on a plateau about 700 meters above sea level, making it one of the higher cities in Australia. It is known for its temperate climate, with mild to warm summers and cool winters. The city is also often referred to as the "Garden City" due to its many parks and gardens, including the Japanese Garden and the Botanic Gardens.')
        
        with col2:
            st.write('## Darling Downs - Maranoa SA4')
            sa4AreasM = make_sa4Areas()
            sa4AreasM = make_mapArea(sa4AreasM, '307')
            mapm = folium.Map(location=[-27.529991, 150.582068], zoom_start=6)
            folium.GeoJson(data=sa4AreasM["geometry"]).add_to(mapm)
            st_data = st_folium(mapm, returned_objects=[])
            with st.expander("More Information"):
                st.write('The Darling Downs-Maranoa Statistical Area (SA4) is located in the southern part of Queensland, Australia, covering an area of approximately 268,000 square kilometers. The region is one of the largest in Queensland and encompasses a diverse range of landscapes, from the rolling hills of the Darling Downs to the rugged mountains of the Great Dividing Range')
                st.write('The Darling Downs is the southernmost part of the region and is a vast expanse of flat to undulating agricultural land. It is known for its fertile soils and is an important agricultural region, with crops such as wheat, sorghum, cotton, and vegetables grown throughout the area. The region is also home to a number of important natural features, including the Bunya Mountains National Park and the Carnarvon Gorge.')
                st.write('The Maranoa region is located to the west of the Darling Downs and is a semi-arid landscape dominated by grasslands and woodlands. The region is characterized by its rugged mountain ranges, including the Great Dividing Range, the Carnarvon Range, and the Expedition Range. The Maranoa is also home to several national parks, including the Maranoa-Balonne and the Idalia National Parks.')

#Function for snapshot page
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
            st.write('The unemployment rate is a measure of the percentage of the labor force that is currently unemployed but actively seeking employment.')
            st.write('To calculate the unemployment rate, the number of unemployed individuals is divided by the total labor force and multiplied by 100. The labor force includes all individuals who are employed or actively seeking employment.')
            st.write('The rate presented is an average of the last 6 months of original data')
            st.write('Queensland data has been seasonally adjusted and based on the last 3 months of original data')

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
            st.write('The employment rate is a measure of the percentage of the working-age population that is currently employed.')
            st.write('To calculate the employment rate, the number of employed individuals is divided by the total working-age population and multiplied by 100. The working-age population includes all individuals who are of working age and are not institutionalized.')
            st.write('The rate presented is an average of the last 6 months of original data')
            st.write('Queensland data has been seasonally adjusted and based on the last 3 months of original data')

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
            st.write('The labor force participation rate is a measure of the percentage of the working-age population that is either employed or actively seeking employment.')
            st.write('To calculate the labor force participation rate, the labor force (which includes employed individuals and those who are unemployed but actively seeking employment) is divided by the total working-age population and multiplied by 100.')
            st.write('The rate presented is an average of the last 6 months of original data')
            st.write('Queensland data has been seasonally adjusted and based on the last 3 months of original data')

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
            st.write('The youth unemployment rate is a measure of the percentage of young people (individuals between the ages of 15 and 24) who are unemployed but actively seeking employment.')
            st.write('To calculate the youth unemployment rate, the number of unemployed youth is divided by the total youth labor force (which includes all youth who are either employed or actively seeking employment) and multiplied by 100.')
            st.write('The youth unemployment rate presented is an average of the last 12 months of original data')
            st.write('The working-age population as those individuals who are between the ages of 15 and 64 and who are not institutionalized.')
            st.write('The working-age population is the must current record of original data')
            st.write('the employed population as individuals who meet the following criteria:')
            st.write('+ Worked for at least one hour in a job for pay or profit during the reference week (the week preceding the survey week)')
            st.write('+ Were on paid or unpaid leave from their job during the reference week')
            st.write('+ Were away from their job for a short time, such as on holiday or sick leave, during the reference week')
            st.write('+ Had a job but were temporarily not working during the reference week, such as being on strike or locked out by their employer.')
            st.write('It also includes individuals who are self-employed, such as small business owners and contractors.')
            st.write('The employed population is the must current record of original data')
            st.write('Queensland data has been seasonally adjusted')

#Function for timeseries page
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
            st.write('The employment rate is a measure of the percentage of the working-age population that is currently employed.')
            st.write('To calculate the employment rate, the number of employed individuals is divided by the total working-age population and multiplied by 100. The working-age population includes all individuals who are of working age and are not institutionalized.')
            st.write('The unemployment rate is a measure of the percentage of the labor force that is currently unemployed but actively seeking employment.')
            st.write('To calculate the unemployment rate, the number of unemployed individuals is divided by the total labor force and multiplied by 100. The labor force includes all individuals who are employed or actively seeking employment.')
            st.write('The labor force participation rate is a measure of the percentage of the working-age population that is either employed or actively seeking employment.')
            st.write('To calculate the labor force participation rate, the labor force (which includes employed individuals and those who are unemployed but actively seeking employment) is divided by the total working-age population and multiplied by 100.')
            st.write('The data above is a rolling average of the previous 6 months of original data')
    
    with st.container():
        st.write('### Darling Downs - Maranoa SA4')
        st.write('Data from: ', dateString, ', displaying the last 5 years')
        y_axis_valuem = st.selectbox('Select Darling Downs - Maranoa Time Series Data', options=maranoatimedf.columns[-3:])
        y_axis_valuem_title = y_axis_valuem + percent_label
        figtm = px.line(maranoatimedf, x='Date', y=y_axis_valuem).update_layout(yaxis_title=y_axis_valuem_title)
        st.plotly_chart(figtm)
        with st.expander("More Information"):
            st.write('The employment rate is a measure of the percentage of the working-age population that is currently employed.')
            st.write('To calculate the employment rate, the number of employed individuals is divided by the total working-age population and multiplied by 100. The working-age population includes all individuals who are of working age and are not institutionalized.')
            st.write('The unemployment rate is a measure of the percentage of the labor force that is currently unemployed but actively seeking employment.')
            st.write('To calculate the unemployment rate, the number of unemployed individuals is divided by the total labor force and multiplied by 100. The labor force includes all individuals who are employed or actively seeking employment.')
            st.write('The labor force participation rate is a measure of the percentage of the working-age population that is either employed or actively seeking employment.')
            st.write('To calculate the labor force participation rate, the labor force (which includes employed individuals and those who are unemployed but actively seeking employment) is divided by the total working-age population and multiplied by 100.')
            st.write('The data above is a rolling average of the previous 6 months of original data')
    
    with st.container():
        st.write('### Queensland SA4')
        st.write('Data from: ', dateString, ', displaying the last 5 years')
        y_axis_valueq = st.selectbox('Select Queensland Time Series Data', options=qldtimedf.columns[-3:])
        y_axis_valueq_title = y_axis_valueq + percent_label
        figtq = px.line(qldtimedf, x='Date', y=y_axis_valueq).update_layout(yaxis_title=y_axis_valueq_title)
        st.plotly_chart(figtq)
        with st.expander("More Information"):
            st.write('The employment rate is a measure of the percentage of the working-age population that is currently employed.')
            st.write('To calculate the employment rate, the number of employed individuals is divided by the total working-age population and multiplied by 100. The working-age population includes all individuals who are of working age and are not institutionalized.')
            st.write('The unemployment rate is a measure of the percentage of the labor force that is currently unemployed but actively seeking employment.')
            st.write('To calculate the unemployment rate, the number of unemployed individuals is divided by the total labor force and multiplied by 100. The labor force includes all individuals who are employed or actively seeking employment.')
            st.write('The labor force participation rate is a measure of the percentage of the working-age population that is either employed or actively seeking employment.')
            st.write('To calculate the labor force participation rate, the labor force (which includes employed individuals and those who are unemployed but actively seeking employment) is divided by the total working-age population and multiplied by 100.')
            st.write('The data above is a rolling average of the previous 3 months of original data')
            st.write('Data has been seasonally adjusted')

#Function for labour force page
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
            st.write('+ Employed full-time: Individuals who work 35 hours or more per week in their main job.')
            st.write('+ Employed part-time: Individuals who work less than 35 hours per week in their main job.')
            st.write('+ Unemployed: Individuals who are currently not working but are actively seeking work and are available to start work within the next four weeks.')
            st.write('+ Not in the workforce: Individuals who are not employed or unemployed. This includes individuals who are not actively seeking work, such as full-time students, homemakers, and retirees, as well as individuals who are unable to work due to disability, illness, or other reasons.')
            st.write('Whilst Toowoomba and Darling Downs - Maranoa are based on 6 month averages of original data, Queensland is based on current data and seasonally adjusted')
            st.write('The percentage is a representation of the distribution of the 4 categories presented')

    st.markdown('# Labour Force Age Data')
    with st.container():
            st.write('### Toowoomba SA4')
            st.write('Data from: ', dateStringAge)
            figat = px.bar(tagedf, x=tagedf.columns[2], y=tagedf.columns[1], text=tagedf.columns[3])
            st.plotly_chart(figat)
            st.metric(label='Combined Age Group total of (55 to 64) and (over 65) years old:', value=str(tagedf.iloc[0][2]+tagedf.iloc[1][2])+', '+str(tagedf.iloc[0][3]+tagedf.iloc[1][3])+strPercent)
            with st.expander("More Information"):
                st.write('Figures based on an average of the last 12 months, with the percentage representing the portion of the categories avaliable.')
    with st.container():
            st.write('### Darling downs - Maranoa SA4')
            st.write('Data from: ', dateStringAge)
            figam = px.bar(magedf, x=magedf.columns[2], y=magedf.columns[1], text=magedf.columns[3])
            st.plotly_chart(figam)
            st.metric(label='Combined Age Group total of (55 to 64) and (over 65) years old:', value=str(magedf.iloc[0][2]+magedf.iloc[1][2])+', '+str(magedf.iloc[0][3]+magedf.iloc[1][3])+strPercent)
            with st.expander("More Information"):
                st.write('Figures based on an average of the last 12 months, with the percentage representing the portion of the categories avaliable.')
    with st.container():
            st.write('### Queensland SA4')
            st.write('Data from: ', dateStringAge)
            figaq = px.bar(qagedf, x=qagedf.columns[2], y=qagedf.columns[1], text=qagedf.columns[3])
            st.plotly_chart(figaq)
            st.metric(label='Combined Age Group total of (55 to 64) and (over 65) years old:', value=str(qagedf.iloc[0][2]+qagedf.iloc[1][2])+', '+str(qagedf.iloc[0][3]+qagedf.iloc[1][3])+strPercent)
            with st.expander("More Information"):
                st.write('Figures based on an average of the last 12 months, with the percentage representing the portion of the categories avaliable.')

#Function for employment by industry page
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
            st.write('+ Employed full-time: Individuals who work 35 hours or more per week in their main job.')
            st.write('+ Employed part-time: Individuals who work less than 35 hours per week in their main job.')
            st.write('+ Employed male: Reported sex.')
            st.write('+ Employed female: Reported sex.')
            st.write('Figures are based on four-quarter averages.')
    
    with st.container():
        st.write('### Darling downs - Maranoa SA4')
        st.write('Data from: ', dateStringEI)
        x_axis_value = st.selectbox('Select Darling Down - Maranoa Industry Employment Figure', options=meidf.columns[2:7])
        figeim = px.bar(meidf, x=x_axis_value, y=meidf.columns[1])
        st.plotly_chart(figeim)
        figeipiem = px.pie(meidf, values=meidf.columns[7], names=meidf.columns[1], title=meidf.columns[7]).update_layout(legend_itemclick=False)
        st.plotly_chart(figeipiem)
        with st.expander("More Information"):
            st.write('+ Employed full-time: Individuals who work 35 hours or more per week in their main job.')
            st.write('+ Employed part-time: Individuals who work less than 35 hours per week in their main job.')
            st.write('+ Employed male: Reported sex.')
            st.write('+ Employed female: Reported sex.')
            st.write('Figures are based on four-quarter averages.')

    with st.container():
        st.write('### Queensland SA4')
        st.write('Data from: ', dateStringEI)
        x_axis_value = st.selectbox('Select Queensland Industry Employment Figure', options=qeidf.columns[2:7])
        figeiq = px.bar(qeidf, x=x_axis_value, y=qeidf.columns[1])
        st.plotly_chart(figeiq)
        figeipieq = px.pie(qeidf, values=qeidf.columns[7], names=qeidf.columns[1], title=qeidf.columns[7]).update_layout(legend_itemclick=False)
        st.plotly_chart(figeipieq)
        with st.expander("More Information"):
            st.write('+ Employed full-time: Individuals who work 35 hours or more per week in their main job.')
            st.write('+ Employed part-time: Individuals who work less than 35 hours per week in their main job.')
            st.write('+ Employed male: Reported sex.')
            st.write('+ Employed female: Reported sex.')
            st.write('Figures are based on four-quarter averages.')

#Function for employment projections page
@st.cache_data
def employmentprojections_func():
    st.markdown('# Employment Projections for Next 5 Years')
    st.markdown('### Toowoomba and Darling Downs - Maranoa')
    st.write('Data from: ', dateStringProjections)
    mask = mtepdf[mtepdf['Industry'] != 'Total (industry)']
    figep = px.bar(mask, x=mask.columns[2], y=mask.columns[1])
    st.plotly_chart(figep)
    st.metric(label='Expected total job industry growth is:', value=str(int(mtepdf.iloc[19][2]*1000)))
    figep2 = px.bar(mtepdf, x=mtepdf.columns[3], y=mtepdf.columns[1])
    st.plotly_chart(figep2)
    with st.expander("More Information"):
            st.write('This data comes from Jobs and Skills Australia collected in 2020 and released in 2021.')
            st.write('The data here is an aggregate of of all the SA4 areas in Queensland except for those that are apart of Greater Brisbane.')

#Function for largest employing occupations page
@st.cache_data
def largestoccupations_func():
    st.markdown('# Largest Employing Occupations')

    with st.container():
        st.markdown('### Toowoomba SA4')
        st.write('Data from: ', dateStringLO)
        figot = px.bar(todf, x=todf.columns[2], y=todf.columns[1])
        st.plotly_chart(figot)
        with st.expander("More Information"):
            st.write('Census data based on usual place of residence.')

    with st.container():
        st.markdown('### Darling Downs - Maranoa SA4')
        st.write('Data from: ', dateStringLO)
        figom = px.bar(modf, x=modf.columns[2], y=modf.columns[1])
        st.plotly_chart(figom)
        with st.expander("More Information"):
            st.write('Census data based on usual place of residence.')

    with st.container():
        st.markdown('### Queensland SA4')
        st.write('Data from: ', dateStringLO)
        figoq = px.bar(qodf, x=qodf.columns[2], y=qodf.columns[1])
        st.plotly_chart(figoq)
        with st.expander("More Information"):
            st.write('Census data based on usual place of residence.')

#Function for employment by occupation
def employingoccupations_func():
    st.markdown('# Employment by Occupations')
    with st.container():
        st.write('### Toowoomba SA4')
        st.write('Data from: ', dateStringOE)
        x_axis_value = st.selectbox('Select Toowoomba Occupation Employment Figure', options=toedf.columns[2:7])
        figoet = px.bar(toedf, x=x_axis_value, y=toedf.columns[1])
        st.plotly_chart(figoet)
        figoepiet = px.pie(toedf, values=toedf.columns[7], names=toedf.columns[1], title=toedf.columns[7]).update_layout(legend_itemclick=False)
        st.plotly_chart(figoepiet)
        with st.expander("More Information"):
            st.write('+ Employed total: All employed individuals.')
            st.write('+ Employed full-time: Individuals who work 35 hours or more per week in their main job.')
            st.write('+ Employed part-time: Individuals who work less than 35 hours per week in their main job.')
            st.write('+ Employed male: Reported sex.')
            st.write('+ Employed female: Reported sex.')
            st.write('Pie chart figure is based on distribution of \'Employment by Occupation - Total.\'')
            st.write('Figures are based on four-quarter averages.')
    
    with st.container():
        st.write('### Darling downs - Maranoa SA4')
        st.write('Data from: ', dateStringOE)
        x_axis_value = st.selectbox('Select Darling Down - Maranoa Occupation Employment Figure', options=moedf.columns[2:7])
        figoem = px.bar(moedf, x=x_axis_value, y=moedf.columns[1])
        st.plotly_chart(figoem)
        figoepiem = px.pie(moedf, values=moedf.columns[7], names=moedf.columns[1], title=moedf.columns[7]).update_layout(legend_itemclick=False)
        st.plotly_chart(figoepiem)
        with st.expander("More Information"):
            st.write('+ Employed total: All employed individuals.')
            st.write('+ Employed full-time: Individuals who work 35 hours or more per week in their main job.')
            st.write('+ Employed part-time: Individuals who work less than 35 hours per week in their main job.')
            st.write('+ Employed male: Reported sex.')
            st.write('+ Employed female: Reported sex.')
            st.write('Pie chart figure is based on distribution of \'Employment by Occupation - Total.\'')
            st.write('Figures are based on four-quarter averages.')

    with st.container():
        st.write('### Queensland SA4')
        st.write('Data from: ', dateStringOE)
        x_axis_value = st.selectbox('Select Queensland Occupation Employment Figure', options=qoedf.columns[2:7])
        figoeq = px.bar(qoedf, x=x_axis_value, y=qoedf.columns[1])
        st.plotly_chart(figoeq)
        figoepieq = px.pie(qoedf, values=qoedf.columns[7], names=qoedf.columns[1], title=qoedf.columns[7]).update_layout(legend_itemclick=False)
        st.plotly_chart(figoepieq)
        with st.expander("More Information"):
            st.write('+ Employed total: All employed individuals.')
            st.write('+ Employed full-time: Individuals who work 35 hours or more per week in their main job.')
            st.write('+ Employed part-time: Individuals who work less than 35 hours per week in their main job.')
            st.write('+ Employed male: Reported sex.')
            st.write('+ Employed female: Reported sex.')
            st.write('Pie chart figure is based on distribution of \'Employment by Occupation - Total.\'')
            st.write('Figures are based on four-quarter averages.')

#Function for further links page
def furtherlinks_func():
    st.write('# Further Links')
    with st.container():
        st.write('## Australian Bureau of Statistics (ABS)')
        st.write('ABS provides a wide range of statistical data that can be searched by region.')
        st.write('[More Information on Toowoomba](https://dbr.abs.gov.au/region.html?lyr=sa4&rgn=317)')
        st.write('[More Information on Darling Downs - Maranoa](https://dbr.abs.gov.au/region.html?lyr=sa4&rgn=307)')
        st.write('[More Information on Queensland](https://dbr.abs.gov.au/region.html?lyr=ste&rgn=3)')
        with st.expander('Information from ABS'):
            st.write('1. Population: ABS provides population statistics for different regions in Australia. This includes data on the total population, population growth, and age distribution.')
            st.write('2. Employment: ABS provides employment data for different regions in Australia. This includes data on the number of people employed, the unemployment rate, and the industries that employ people in each region.')
            st.write('3. Income: ABS provides income data for different regions in Australia. This includes data on the average income per person, the median income, and the income distribution.')
            st.write('4. Education: ABS provides education data for different regions in Australia. This includes data on the number of people with different levels of education, the number of students enrolled in schools and universities, and the types of qualifications obtained by people in each region.')
            st.write('5. Housing: ABS provides housing data for different regions in Australia. This includes data on the number of dwellings, the types of dwellings, and the average cost of housing in each region.')
            st.write('6. Health: ABS provides health data for different regions in Australia. This includes data on the number of hospitals and health services, the number of doctors and nurses, and health outcomes such as life expectancy and mortality rates.')
            st.write('7. Crime: ABS provides crime data for different regions in Australia. This includes data on the number of crimes committed, the types of crimes, and the rates of crime in each region.')
            st.write('8. Environment: ABS provides environmental data for different regions in Australia. This includes data on the quality of air, water, and soil, as well as information on biodiversity and climate change.')

    with st.container():
        st.write('## Informed Decisions')
        st.write('Informed Decisions is a data analytics and visualization platform that provides a wide range of data that can be searched by region.')
        st.write('[More Information on Toowoomba](https://profile.id.com.au/toowoomba)')
        st.write('[More Information on Darling Downs - Maranoa](https://profile.id.com.au/rda-dd-sw)')
        st.write('[More Information on Queensland](https://profile.id.com.au/australia/about?WebID=120)')
        with st.expander('Information from Informed Decisions'):
            st.write('1. Demographics: ID Community provides demographic data for different regions in Australia. This includes data on population size, age distribution, gender, cultural diversity, and household composition.')
            st.write('2. Social: ID Community provides social data for different regions in Australia. This includes data on education, employment, income, housing, and health.')
            st.write('3. Economic: ID Community provides economic data for different regions in Australia. This includes data on the local economy, employment, industry sectors, business activity, and innovation.')
            st.write('4. Infrastructure: ID Community provides infrastructure data for different regions in Australia. This includes data on transport, energy, water, waste, and telecommunications.')
            st.write('5. Environment: ID Community provides environmental data for different regions in Australia. This includes data on climate, air and water quality, biodiversity, and land use.')
            st.write('6. Tourism: ID Community provides tourism data for different regions in Australia. This includes data on visitor numbers, expenditure, and key attractions.')
            st.write('7. Education: ID Community provides education data for different regions in Australia. This includes data on student enrolments, staff numbers, and academic achievement.')

    with st.container():
        st.write('## Queensland Government Statistician\'s Office')
        st.write('The Queensland Government Statistician\'s Office (QGSO) is the official statistics agency of the Queensland Government in Australia. The agency provides a wide range of statistical data and analysis across various topics.')
        st.write('Unfortunately QGSO does not provide data by region, regional information can be found on the site when looking at a topic of interest [QSGO Website](https://www.qgso.qld.gov.au/)')
        with st.expander('Information from the Queensland Government Statistician\'s Office'):
            st.write('1. Population and demographics: QGSO provides data on the population size, distribution, and characteristics of people living in Queensland. This includes information on age, gender, ethnicity, and religion.')
            st.write('2. Economy and industry: QGSO provides data on the Queensland economy and various industries, including employment, income, business activity, and trade.')
            st.write('3. Health and wellbeing: QGSO provides data on the health and wellbeing of the people in Queensland, including information on health services, health outcomes, and lifestyle factors.')
            st.write('4. Education and training: QGSO provides data on education and training in Queensland, including enrolment rates, student performance, and qualifications obtained.')
            st.write('5. Environment and natural resources: QGSO provides data on the environment and natural resources of Queensland, including information on climate, land use, and water resources.')
            st.write('6. Crime and justice: QGSO provides data on crime and justice in Queensland, including crime rates, types of offences, and the criminal justice system.')
            st.write('7. Transport and infrastructure: QGSO provides data on transport and infrastructure in Queensland, including information on roads, public transport, and the use of technology.')

#Navigation menu
st.sidebar.title('Navigation')
options = st.sidebar.radio('Pages', options = ['Maps', 'Snapshot Data', 'Time Series Data', 'Labour Force Data', 'Employment by Industry', 'Employment Projections', 'Largest Employing Occupations', 'Employment by Occupation', 'Further Links'])

#Options to control pages
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
elif options == 'Employment by Occupation':
    employingoccupations_func()
elif options == 'Further Links':
    furtherlinks_func()
