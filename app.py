# Import needed libraries
import streamlit as st
import pandas as pd
import requests
import openpyxl
from bs4 import BeautifulSoup
import plotly.express as px

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
    df.reset_index(drop=True, inplace=True)
    return df

@st.cache_data
def make_tagedf(dataFrame):
    df = dataFrame.loc[dataFrame['Region Name'] == "Toowoomba"]
    df = df.drop('State/Territory', axis=1)
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

# Initialise variable of every list item, alternatively you could manually place links here for each xlsx file
snapshotlink = make_list()[0]
timelink = make_list()[1]
labourforcelink = make_list()[2]
agelink = make_list()[3]
employmentindustrylink = make_list()[4]
employmentprojectionlink = make_list()[5]
#occupationlink = make_list()[6]
#occupationemploymentlink = make_list()[7]

#Create a string that contains the date of the data
dateString = make_date(snapshotlink)
dateStringProjections = make_date(employmentprojectionlink)
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

st.title('Employment Dashboard')

@st.cache_data
def map_func():
    st.markdown('# Map Information')
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.image("https://www.billcahill.com.au/wp-content/uploads/2020/01/image.png", caption='Toowoomba')
            with st.expander("More Information"):
                st.write('More information on this object :)')

        with col2:
            st.image("https://www.billcahill.com.au/wp-content/uploads/2020/01/image.png", caption='Darling Downs - Maranoa')
            with st.expander("More Information"):
                st.write('More information on this object :)')

@st.cache_data
def snapshot_func():
    st.markdown('# Snapshot Data')
    st.markdown('## Unemployment Rate')
    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write('Toowoomba SA4')
            st.write('Data from: ', dateString)
            st.write(toowoombasnapshotdf.iloc[0][5], '%')
            st.write('Last 5 years')
            st.write('Minimum Unemployment Rate: ', ttUEmindf.iloc[-1][3],'%',' on ',ttUEmindf.iloc[-1,1].strftime('%B-%Y'))
            st.write('Maximum Unemployment Rate: ', ttUEmaxdf.iloc[-1][3],'%',' on ',ttUEmaxdf.iloc[-1,1].strftime('%B-%Y'))
            with st.expander("More Information"):
                st.write('More information on this object :)')

        with col2:
            st.write('Darling Downs - Maranoa SA4')
            st.write('Data from: ', dateString)
            st.write(maranoasnapshotdf.iloc[0][5], '%')
            st.write('Last 5 years')
            st.write('Minimum Unemployment Rate: ', mtUEmindf.iloc[-1][3],'%',' on ',mtUEmindf.iloc[-1,1].strftime('%B-%Y'))
            st.write('Maximum Unemployment Rate: ', mtUEmaxdf.iloc[-1][3],'%',' on ',mtUEmaxdf.iloc[-1,1].strftime('%B-%Y'))
            with st.expander("More Information"):
                st.write('More information on this object :)')

        with col3:
            st.write('Queensland')
            st.write('Data from: ', dateString)
            st.write(qldsnapshotdf.iloc[0][5], '%')
            st.write('Last 5 years')
            st.write('Minimum Unemployment Rate: ', qtUEmindf.iloc[-1][3],'%',' on ',qtUEmindf.iloc[-1,1].strftime('%B-%Y'))
            st.write('Maximum Unemployment Rate: ', qtUEmaxdf.iloc[-1][3],'%',' on ',qtUEmaxdf.iloc[-1,1].strftime('%B-%Y'))
            with st.expander("More Information"):
                st.write('More information on this object :)')

    st.markdown('## Employment Rate')
    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write('Toowoomba SA4')
            st.write('Data from: ', dateString)
            st.write(toowoombasnapshotdf.iloc[0][3], '%')
            st.write('Last 5 years')
            st.write('Minimum Employment Rate: ', ttEmindf.iloc[-1][2],'%',' on ',ttEmindf.iloc[-1,1].strftime('%B-%Y'))
            st.write('Maximum Employment Rate: ', ttEmaxdf.iloc[-1][2],'%',' on ',ttEmaxdf.iloc[-1,1].strftime('%B-%Y'))
            with st.expander("More Information"):
                st.write('More information on this object :)')

        with col2:
            st.write('Darling Downs - Maranoa SA4')
            st.write('Data from: ', dateString)
            st.write(maranoasnapshotdf.iloc[0][3], '%')
            st.write('Last 5 years')
            st.write('Minimum Employment Rate: ', mtEmindf.iloc[-1][2],'%',' on ',mtEmindf.iloc[-1,1].strftime('%B-%Y'))
            st.write('Maximum Employment Rate: ', mtEmaxdf.iloc[-1][2],'%',' on ',mtEmaxdf.iloc[-1,1].strftime('%B-%Y'))
            with st.expander("More Information"):
                st.write('More information on this object :)')

        with col3:
            st.write('Queensland')
            st.write('Data from: ', dateString)
            st.write(qldsnapshotdf.iloc[0][3], '%')
            st.write('Last 5 years')
            st.write('Minimum Employment Rate: ', qtEmindf.iloc[-1][2],'%',' on ',qtEmindf.iloc[-1,1].strftime('%B-%Y'))
            st.write('Maximum Employment Rate: ', qtEmaxdf.iloc[-1][2],'%',' on ',qtEmaxdf.iloc[-1,1].strftime('%B-%Y'))
            with st.expander("More Information"):
                st.write('More information on this object :)')

    st.markdown('## Participation Rate')
    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write('Toowoomba SA4')
            st.write('Data from: ', dateString)
            st.write(toowoombasnapshotdf.iloc[0][4], '%')
            st.write('Last 5 years')
            st.write('Minimum Participation Rate: ', ttPmindf.iloc[-1][4],'%',' on ',ttPmindf.iloc[-1,1].strftime('%B-%Y'))
            st.write('Maximum Participation Rate: ', ttPmaxdf.iloc[-1][4],'%',' on ',ttPmaxdf.iloc[-1,1].strftime('%B-%Y'))
            with st.expander("More Information"):
                st.write('More information on this object :)')

        with col2:
            st.write('Darling Downs - Maranoa SA4')
            st.write('Data from: ', dateString)
            st.write(maranoasnapshotdf.iloc[0][4], '%')
            st.write('Last 5 years')
            st.write('Minimum Participation Rate: ', mtPmindf.iloc[-1][4],'%',' on ',mtPmindf.iloc[-1,1].strftime('%B-%Y'))
            st.write('Maximum Participation Rate: ', mtPmaxdf.iloc[-1][4],'%',' on ',mtPmaxdf.iloc[-1,1].strftime('%B-%Y'))
            with st.expander("More Information"):
                st.write('More information on this object :)')

        with col3:
            st.write('Queensland')
            st.write('Data from: ', dateString)
            st.write(qldsnapshotdf.iloc[0][4], '%')
            st.write('Last 5 years')
            st.write('Minimum Participation Rate: ', qtEmindf.iloc[-1][4],'%',' on ',qtPmindf.iloc[-1,1].strftime('%B-%Y'))
            st.write('Maximum Participation Rate: ', qtEmaxdf.iloc[-1][4],'%',' on ',qtPmaxdf.iloc[-1,1].strftime('%B-%Y'))
            with st.expander("More Information"):
                st.write('More information on this object :)')

    st.markdown('### Other Key Figures')
    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write('Toowoomba SA4')
            st.write('Data from: ', dateString)
            st.write('Youth Unemployment (15-24yrs): ', toowoombasnapshotdf.iloc[0][6], '%')
            st.write('Working Age Population (15-64yrs): ', toowoombasnapshotdf.iloc[0][1])
            st.write('Employed (15+ yrs): ', toowoombasnapshotdf.iloc[0][2])
            with st.expander("More Information"):
                st.write('More information on this object :)')

        with col2:
            st.write('Darling Downs - Maranoa SA4')
            st.write('Data from: ', dateString)
            st.write('Youth Unemployment (15-24yrs): ', maranoasnapshotdf.iloc[0][6], '%')
            st.write('Working Age Population (15-64yrs): ', maranoasnapshotdf.iloc[0][1])
            st.write('Employed (15+ yrs): ', maranoasnapshotdf.iloc[0][2])
            with st.expander("More Information"):
                st.write('More information on this object :)')

        with col3:
            st.write('Queensland')
            st.write('Data from: ', dateString)
            st.write('Youth Unemployment (15-24yrs): ', qldsnapshotdf.iloc[0][6], '%')
            st.write('Working Age Population (15-64yrs): ', qldsnapshotdf.iloc[0][1])
            st.write('Employed (15+ yrs): ', qldsnapshotdf.iloc[0][2])
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
            st.write('Toowoomba SA4')
            st.write('Data from: ', dateString)
            tlftotal = tlfdf.iloc[0][2] + tlfdf.iloc[1][2] + tlfdf.iloc[2][2] + tlfdf.iloc[3][2]
            st.write(tlfdf.iloc[0][1], ': ', tlfdf.iloc[0][2], 'persons.', ' ', round((tlfdf.iloc[0][2]/tlftotal*100), 1), '%')
            st.write(tlfdf.iloc[1][1], ': ', tlfdf.iloc[1][2], 'persons.', ' ', round((tlfdf.iloc[1][2]/tlftotal*100), 1), '%')
            st.write(tlfdf.iloc[2][1], ': ', tlfdf.iloc[2][2], 'persons.', ' ', round((tlfdf.iloc[2][2]/tlftotal*100), 1), '%')
            st.write(tlfdf.iloc[3][1], ': ', tlfdf.iloc[3][2], 'persons.', ' ', round((tlfdf.iloc[3][2]/tlftotal*100), 1), '%')
            with st.expander("More Information"):
                st.write('More information on this object :)')

        with col2:
            st.write('Darling Downs - Maranoa SA4')
            st.write('Data from: ', dateString)
            mlftotal = mlfdf.iloc[0][2] + mlfdf.iloc[1][2] + mlfdf.iloc[2][2] + mlfdf.iloc[3][2]
            st.write(mlfdf.iloc[0][1], ': ', mlfdf.iloc[0][2], 'persons', ' ', round((mlfdf.iloc[0][2]/mlftotal*100), 1), '%')
            st.write(mlfdf.iloc[1][1], ': ', mlfdf.iloc[1][2], 'persons', ' ', round((mlfdf.iloc[1][2]/mlftotal*100), 1), '%')
            st.write(mlfdf.iloc[2][1], ': ', mlfdf.iloc[2][2], 'persons', ' ', round((mlfdf.iloc[2][2]/mlftotal*100), 1), '%')
            st.write(mlfdf.iloc[3][1], ': ', mlfdf.iloc[3][2], 'persons', ' ', round((mlfdf.iloc[3][2]/mlftotal*100), 1), '%')
            with st.expander("More Information"):
                st.write('More information on this object :)')

        with col3:
            st.write('Queensland')
            st.write('Data from: ', dateString)
            qlftotal = qldlfdf.iloc[0][2] + qldlfdf.iloc[1][2] + qldlfdf.iloc[2][2] + qldlfdf.iloc[3][2]
            st.write(qldlfdf.iloc[0][1], ': ', qldlfdf.iloc[0][2], 'persons', ' ', round((qldlfdf.iloc[0][2]/qlftotal*100), 1), '%')
            st.write(qldlfdf.iloc[1][1], ': ', qldlfdf.iloc[1][2], 'persons', ' ', round((qldlfdf.iloc[1][2]/qlftotal*100), 1), '%')
            st.write(qldlfdf.iloc[2][1], ': ', qldlfdf.iloc[2][2], 'persons', ' ', round((qldlfdf.iloc[2][2]/qlftotal*100), 1), '%')
            st.write(qldlfdf.iloc[3][1], ': ', qldlfdf.iloc[3][2], 'persons', ' ', round((qldlfdf.iloc[3][2]/qlftotal*100), 1), '%')
            with st.expander("More Information"):
                st.write('More information on this object :)')

    st.markdown('# Labour Force Age Data')
    with st.container():
            st.write('### Toowoomba SA4')
            st.write('Data from: ', dateString)
            st.write(tagedf.columns[1],': ', tagedf.iloc[0][1], ' years', ': ', tagedf.iloc[0][2], ', ', tagedf.iloc[0][3], '%')
            st.write(tagedf.columns[1],': ', tagedf.iloc[1][1], ' years', ': ', tagedf.iloc[1][2], ', ', tagedf.iloc[1][3], '%')
            st.write(tagedf.columns[1],': ', tagedf.iloc[2][1], ' years', ': ', tagedf.iloc[2][2], ', ', tagedf.iloc[2][3], '%')
            st.write(tagedf.columns[1],': ', tagedf.iloc[3][1], ' years', ': ', tagedf.iloc[3][2], ', ', tagedf.iloc[3][3], '%')
            st.write(tagedf.columns[1],': ', tagedf.iloc[4][1], ' years', ': ', tagedf.iloc[4][2], ', ', tagedf.iloc[4][3], '%')
            st.write(tagedf.columns[1],': ', '65 years and over', ': ', tagedf.iloc[5][2], ', ', tagedf.iloc[5][3], '%')
            st.write(' ')
            st.write(tagedf.columns[1],': Mature 55 years and over:', tagedf.iloc[5][2]+tagedf.iloc[4][2], ', ', tagedf.iloc[5][3]+tagedf.iloc[4][3], '%')
            with st.expander("More Information"):
                st.write('More information on this object :)')
    with st.container():
            st.write('### Darling downs - Maranoa SA4')
            st.write('Data from: ', dateString)
            st.write(magedf.columns[1],': ', magedf.iloc[0][1], ' years', ': ', magedf.iloc[0][2], ', ', magedf.iloc[0][3], '%')
            st.write(magedf.columns[1],': ', magedf.iloc[1][1], ' years', ': ', magedf.iloc[1][2], ', ', magedf.iloc[1][3], '%')
            st.write(magedf.columns[1],': ', magedf.iloc[2][1], ' years', ': ', magedf.iloc[2][2], ', ', magedf.iloc[2][3], '%')
            st.write(magedf.columns[1],': ', magedf.iloc[3][1], ' years', ': ', magedf.iloc[3][2], ', ', magedf.iloc[3][3], '%')
            st.write(magedf.columns[1],': ', magedf.iloc[4][1], ' years', ': ', magedf.iloc[4][2], ', ', magedf.iloc[4][3], '%')
            st.write(magedf.columns[1],': ', '65 years and over', ': ', magedf.iloc[5][2], ', ', magedf.iloc[5][3], '%')
            st.write(' ')
            st.write(magedf.columns[1],': Mature 55 years and over:', magedf.iloc[5][2]+magedf.iloc[4][2], ', ', magedf.iloc[5][3]+magedf.iloc[4][3], '%')
            with st.expander("More Information"):
                st.write('More information on this object :)')
    with st.container():
            st.write('### Queensland')
            st.write('Data from: ', dateString)
            st.write(qagedf.columns[1],': ', qagedf.iloc[0][1], ' years', ': ', qagedf.iloc[0][2], ', ', qagedf.iloc[0][3], '%')
            st.write(qagedf.columns[1],': ', qagedf.iloc[1][1], ' years', ': ', qagedf.iloc[1][2], ', ', qagedf.iloc[1][3], '%')
            st.write(qagedf.columns[1],': ', qagedf.iloc[2][1], ' years', ': ', qagedf.iloc[2][2], ', ', qagedf.iloc[2][3], '%')
            st.write(qagedf.columns[1],': ', qagedf.iloc[3][1], ' years', ': ', qagedf.iloc[3][2], ', ', qagedf.iloc[3][3], '%')
            st.write(qagedf.columns[1],': ', qagedf.iloc[4][1], ' years', ': ', qagedf.iloc[4][2], ', ', qagedf.iloc[4][3], '%')
            st.write(qagedf.columns[1],': ', '65 years and over', ': ', qagedf.iloc[5][2], ', ', qagedf.iloc[5][3], '%')
            st.write(' ')
            st.write(qagedf.columns[1],': Mature 55 years and over:', qagedf.iloc[5][2]+qagedf.iloc[4][2], ', ', qagedf.iloc[5][3]+qagedf.iloc[4][3], '%')
            with st.expander("More Information"):
                st.write('More information on this object :)')

def employmentindustry_func():
    st.markdown('# Employment by Industry')
    with st.container():
        st.write('### Toowoomba SA4')
        st.write('Data from: ', dateString)
        x_axis_value = st.selectbox('Select Toowoomba Industry Employment Figure', options=teidf.columns[2:7])
        figeit = px.bar(teidf, x=x_axis_value, y=teidf.columns[1])
        st.plotly_chart(figeit)
        figeipiet = px.pie(teidf, values=teidf.columns[7], names=teidf.columns[1], title=teidf.columns[7])
        st.plotly_chart(figeipiet)
        with st.expander("More Information"):
            st.write('More information on this object :)')
    
    with st.container():
        st.write('### Darling downs - Maranoa SA4')
        st.write('Data from: ', dateString)
        x_axis_value = st.selectbox('Select Darling Down - Maranoa Industry Employment Figure', options=meidf.columns[2:7])
        figeim = px.bar(meidf, x=x_axis_value, y=meidf.columns[1])
        st.plotly_chart(figeim)
        figeipiem = px.pie(meidf, values=meidf.columns[7], names=meidf.columns[1], title=meidf.columns[7])
        st.plotly_chart(figeipiem)
        with st.expander("More Information"):
            st.write('More information on this object :)')

    with st.container():
        st.write('### Queensland')
        st.write('Data from: ', dateString)
        x_axis_value = st.selectbox('Select Queensland Industry Employment Figure', options=qeidf.columns[2:7])
        figeiq = px.bar(qeidf, x=x_axis_value, y=qeidf.columns[1])
        st.plotly_chart(figeiq)
        figeipieq = px.pie(qeidf, values=qeidf.columns[7], names=qeidf.columns[1], title=qeidf.columns[7])
        st.plotly_chart(figeipieq)
        with st.expander("More Information"):
            st.write('More information on this object :)')

st.sidebar.title('Navigation')
options = st.sidebar.radio('Pages', options = ['Maps', 'Snapshot Data', 'Time Series Data', 'Labour Force Data', 'Employment by Industry'])

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
