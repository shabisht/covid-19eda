# COVID-19 EDA Analysis

import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st 
import plotly.graph_objs as gobj
import calendar

@st.cache(persist=True)
def load_data_global():
	URL = "https://covid19.who.int/WHO-COVID-19-global-data.csv"
	try:
		df = pd.read_csv(URL)
	except:
		df = pd.read_csv('WHO-COVID-19-global-data.csv')

	df = df.rename(columns = {'Date_reported':'date', 'Country':'location', 'Cumulative_cases':'cases', 'Cumulative_deaths':'deaths'})
	
	# adding continent and iso3_code
	df2 = pd.read_csv("Continent_iso3.csv")
	df = df.set_index('location').join(df2.set_index('location'))

	# above line will make location as index but we have to make it a column again
	df = df.reset_index()

	df['date'] = pd.to_datetime(df['date'] , format = "%Y-%m-%d")
	df['year'] = pd.DatetimeIndex(df['date']).year
	df['month'] = pd.DatetimeIndex(df['date']).month
	
	return df

@st.cache(persist=True)
def load_data_india():
	url = 'https://api.covid19india.org/csv/latest/state_wise.csv'
	df = pd.read_csv(url)
	df = df.rename(columns = {'State':'States', 'Deaths':'Deceased'})
	df = df[['States', 'Confirmed', 'Recovered', 'Deceased', 'Active']]
	
	filter1 = df['States'].isin(['Total','State Unassigned'])
	df = df.drop(index = df[filter1].index)
	df = df.reset_index(drop=True)
	return df
	# url = 'https://covid19india.org/'
	# header = {
	#   "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
	#   "X-Requested-With": "XMLHttpRequest"
	# }
	# r = requests.get(url, headers=header)
	# df = pd.read_html(r.text)
	# df = pd.DataFrame(df[0])
	# df = df.rename(columns = {'State':'States','Confirmed Cases':'Confirmed' , 'Recoveries':'Recovered' , 'Deaths':'Deceased'})
	# df['Active'] = df.Confirmed - (df.Recovered + df.Deceased)
	# df = df.drop(index = [len(df)-1,len(df)-2])

def plotBarFunc(df):
	df = df.sort_values(by="New_cases", ascending=False)
	fig = go.Figure()
	fig.add_trace(go.Bar(
	    x=df.index,
	    y=df.New_cases,
	    name='Confirmed',
	    marker_color='ORANGE'
	))
	fig.add_trace(go.Bar(
	    x=df.index,
	    y=df.New_deaths,
	    name='Deceased',
	    marker_color='PURPLE'
	))

	# Here we modify the tickangle of the xaxis, resulting in rotated labels.
	fig.update_layout(
	                    barmode='group',
	                    xaxis_tickangle=-90,
	                    title = "COVID-19 Pandemic affected Continents",
	                    plot_bgcolor = '#FFEEFF'
	                )

	st.plotly_chart(fig, use_container_width=True)


def plot_country_map(countries,continent,figure):

	# countries = [x.replace('_',' ') for x in countries]
	text,title,z = 'Deceased','No. of Deaths',np.array(figure.New_deaths)

	if(get_status() == "Confirmed Cases"):
		text,title,z = 'Confirmed','No. of Confirmed Cases',np.array(figure.New_cases)

	data = dict(type = 'choropleth',
            locations = countries,
            locationmode = 'country names',
            colorscale= 'Portland',
            text= text,
            z=z,
            colorbar = {'title':title, 'len':200,'lenmode':'pixels' }
            )
	
	#initializing the layout variable
	continent = continent.lower()
	if continent == 'america' or continent == 'oceania':
		continent = 'world'
		
	layout = dict(geo = {'scope':continent})
	
	# Initializing the Figure object by passing data and layout as arguments.
	col_map = gobj.Figure(data = [data],layout = layout)

	st.write(col_map)

def get_status():
	return status

def get_status2():
	return status2

def get_status4():
	return status4

def draw_scatter(df):
	fig = go.Figure(data=go.Scatter(x=df.index,
                                y=df,
                                mode='markers+lines',
                                marker=dict(
                                    size=13,
                                    color=np.random.randn(len(df)), #set color equal to a variable
                                    colorscale='reds' # one of plotly colorscales
                                    )
                                ))

	fig.update_layout(title="Top {} Affected Countries".format(number))
	st.write(fig)

def plot_states(df , caseType):
	y, title = df.Confirmed, 'Confirmed COVID-19 Cases Till Now in India'
	if caseType == 'a':
		y, title = df.Active, 'Active COVID-19 Cases Till Now in India'
	elif caseType == 'd':
		y, title = df.Deceased, 'Deceased COVID-19 Cases Till Now in India'
	elif caseType == 'r':
		y, title = df.Recovered, 'Recovered COVID-19 Cases Till Now in India'

	fig = go.Figure(data=go.Scatter(x=df.States,
                                y=y,
                                mode='markers+lines',
                                marker=dict(
                                    size=10,
                                    color=np.random.randn(len(df)), #set color equal to a variable
                                    colorscale='inferno', # one of plotly colorscales
                                    )
                                ))

	fig.update_layout(title=title)
	st.write(fig)


def plot_world_data(df):
	fig = go.Figure(data=go.Choropleth(
    locations = df.iso_code,
    z = df.New_cases,
    text = df.index,
    colorscale = 'greens',
    autocolorscale=False,
    reversescale=True,
    marker_line_color='darkgray',
    marker_line_width=0.5,
    colorbar_title = 'population affected',
	))

	fig.update_layout(
    title_text='Countries Affected by COVID-19',
    geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='equirectangular'
    ),
    annotations = [dict(
        x=0.55,
        y=0.1,
        xref='paper',
        yref='paper',
        text="",
        showarrow = False
    )]
	)

	st.write(fig)

# sets layout to full width
# st.set_page_config(layout="wide")
data_global = load_data_global()
#print(data_global)
# allStatesData = load_data_india()
country_grp = data_global.groupby("location")

#--------------- CSS properties---------------------------------------------------------------------
st.markdown('''
			<style>
				body {background-color: #dce8f3;}
				h2 {color: green;}
				h4 {color: purple;}
				p {color: blue;}
				.blk{color: black;}
				.wht{color: white;}
				.note {color: red;font-size: 22px;font-weight: bold;}
				.active {background-color: #005c25;color: white;}
				.recover {background-color: #5aab38;color: white;}
				.outer {display: flex;flex-direction: row;flex-wrap: wrap;}
				
				.outer .confirm {background-color: #D3212D;width: 40%;margin: 10px;
  							text-align: center;line-height: 50px;font-size: 30px;border-radius: 30px;}

  				.outer .death {background-color: #582801;width: 40%;margin: 10px;
  							text-align: center;line-height: 50px;font-size: 30px;border-radius: 30px;}

  				.outer .active {background-color: #002c57;width: 40%;margin: 10px;
  							text-align: center;line-height: 50px;font-size: 30px;border-radius: 30px;}

  				.outer .recover {background-color: #005c25;width: 40%;margin: 10px;
  							text-align: center;line-height: 50px;font-size: 30px;border-radius: 30px;}
			</style>

			''', unsafe_allow_html=True)

#---------------End of Css properties-------------------------------------------------------------------

	#-----------------main body heading-------------------------------------
st.title("COVID-19 UPDATES AND INSIGHTS")
st.subheader("Get latest updates on COVID-19 WorldWide")
st.image("cv.png", width=620)
	#-----------end of main body-------------------------------------------

#-----------------SIDE BAR ------------------------------------------------------------------------

st.sidebar.title("COVID-19 ANALYSIS")
check1, check2 = False, False
selection = st.sidebar.radio("", ('WORLD', 'INDIA'))

with st.spinner(f"{selection} ANALYSIS ..."):

	#----------------------World Analysis-----------------------------------------------------
	if selection == 'WORLD':
		st.title("COVID-19 Global Dashboard")
		confirm = int(data_global.New_cases.sum())
		death = int(data_global.New_deaths.sum())

		div_box = ''' <br>
					<div class='outer'>
						<div class="confirm">
							<h1 class="wht">{:,}</h1>
							<p class="wht">Confirmed Cases</p>
						</div>
						<div class="death">
							<h1 class="wht">{:,}</h1>
							<p class="wht">Deacesed Cases</p>
						</div>	
					</div>
					<br>
			 '''.format(confirm, death)

		st.markdown(div_box, unsafe_allow_html = True)

		st.sidebar.markdown("## CATEGORIES")

		options = st.sidebar.selectbox("",("--Select--","Continents Affected", "Top Most Affected Countries"), key="opt")
		
		#-----------------Continent wise------------------------------------------------------------
		if options == "--Select--":
			msg = '''<div class='outer'> <div style="font-size: 3em;text-align:center">👈</div> <div style="text-align:center;width:70%"><h3>Please visit the sidebar and interact with
				 Different Categories to see Detailed Analysis.</h3></div></div> <br>
				 '''
			st.markdown(msg, unsafe_allow_html=True)

			if st.checkbox("See the Map", False, key='world_map'):
				df = country_grp[['New_cases','New_deaths']].sum()
				df = df.merge(country_grp.first().iso_code , left_index=True, right_index=True)
				plot_world_data(df)
				
		elif options == "Continents Affected":
			continent_grp = data_global.groupby("continent")
			figure = continent_grp[['New_cases','New_deaths']].sum()
			#print(continent_grp.first())
			list_cont = ['All']
			list_cont.extend(sorted(figure.index.to_list()))
			
			country=""
			status=""
			select = st.sidebar.selectbox("Select Continent",list_cont)

			if select != 'All':
				list_cntry = ['All']
				list_cntry.extend(continent_grp.get_group(select).location.unique())

				country = st.sidebar.selectbox("Select Country",list_cntry)
				
				figure = data_global.groupby(['continent','location'])
				
				status = st.radio("See the count of",("Confirmed Cases","No. of Deaths"))

				if country == 'All':
					figure = figure[['New_cases','New_deaths']].sum().loc[(select), :]
					plot_country_map(list_cntry[1:],select,figure)

				else:
					figure = figure[['New_cases','New_deaths']].sum().loc[(select,country)]
					plot_country_map([country],select,figure)

			else:
				plotBarFunc(figure);

			if st.checkbox("See figures",False, key="key1"):
				st.subheader("Confirmed and Deceased cases in Different Continents")
				st.table(figure)
		#--------------------------------------------------------------------------------------------
		
		#-----------------Top Affected Countries------------------------------------------------------
		if options == "Top Most Affected Countries":
			st.title("Top Affected Countries In The World")
			status2 = st.radio("See the count of",("Confirmed Cases","No. of Deaths"),key='num')
			number = st.sidebar.slider("no. of countries", 10, 20)
			country_cases = country_grp.New_cases.sum().nlargest(number)
			country_deaths = country_grp.New_deaths.sum().nlargest(number)

			if(get_status2() == "Confirmed Cases"):
				draw_scatter(country_cases)
				if st.checkbox("See figures",False,key='top_fig'):
					st.subheader("Top {} Affected Countries".format(number))
					st.table(country_cases)
			else:
				draw_scatter(country_deaths)
				if st.checkbox("See figures",False,2):
					st.subheader("Top {} Affected Countries".format(number))
					st.table(country_deaths)
			#---------------------------------------------------------------------------------
	
	#-----------------------India Analysis-----------------------------------------------------
	else:
		
		st.title("COVID-19 India Dashboard")
		allStatesData = load_data_india()
		confirm = int(allStatesData.Confirmed.sum())
		death = int(allStatesData.Deceased.sum())
		active = int(allStatesData.Active.sum())
		recover = int(allStatesData.Recovered.sum())

		div_box = ''' <br>
					<div class='outer'>
						<div class="confirm">
							<h1 class="wht">{:,}</h1>
							<p class="wht">Confirmed Cases</p>
						</div>
						<div class="active">
							<h1 class="wht">{:,}</h1>
							<p class="wht">Active Cases</p>
						</div>
						<div class="recover">
							<h1 class="wht">{:,}</h1>
							<p class="wht">Recovered Cases</p>
						</div>
						<div class="death">
							<h1 class="wht">{:,}</h1>
							<p class="wht">Deacesed Cases</p>
						</div>	
					</div>

			 '''.format(confirm, active, recover, death)

		st.markdown(div_box, unsafe_allow_html = True)
		ind_grp = country_grp.get_group("India")
		st.title("COVID-19 Outbreak in India")
		st.sidebar.markdown("## CATEGORIES")
		choice = st.sidebar.radio("",("Daywise Analysis","Monthwise Analysis","State/UT-Wise"), key="wise")

		if choice == "Daywise Analysis":
			status3 = st.radio("See the count of",("Confirmed Cases","No. of Deaths"),key='Daywise')
			
			case_or_death, name, title = ind_grp['New_deaths'], 'deaths per day', 'COVID-19 Daywise deaths'
			
			if status3 == "Confirmed Cases":
				case_or_death, name, title = ind_grp['New_cases'], 'new cases per day', 'COVID-19 Daywise Confirmed Cases'

			fig = px.line(ind_grp, x='date', y=case_or_death, title=name)

			fig.update_xaxes(rangeslider_visible=True)

			# fig = go.Figure(go.Scatter(x = ind_grp['date'], y = case_or_death,name=name))

			# fig.update_layout(title=title,
			#                    plot_bgcolor='#FFEEFF', colorway = ['#000000'],
			#                    showlegend=True,)

			st.write(fig)

		elif choice == "Monthwise Analysis":
			monthwise = ind_grp.groupby(['year','month'])
			monthwise['cases'].sum()
			mnt = monthwise['cases'].sum().loc[2020]
			mnt.cumsum()
			mnt_deaths = monthwise['deaths'].sum().loc[2020]

			month=[calendar.month_name[x] for x in mnt.index]

			fig = go.Figure(data=[
			    go.Bar(name='Cases', x=month, y=mnt.cumsum()),
			    go.Bar(name='Deaths', x=month, y=mnt_deaths.cumsum())
			])
			# Change the bar mode
			fig.update_layout(title = 'Monthly Analysis of COVID-19 India for the year 2020',
			                  barmode='group' ,
			                  plot_bgcolor = '#FFEEFF',
			                  colorway = ['BLUE' , 'GREEN']
			                 )
			st.write(fig)

		else:
			st.subheader("Indian States/UT's vs COVID-19")

			filter1 = allStatesData.Confirmed != 0
			web_df = allStatesData[filter1]

			status4 = st.radio("See the count of",("Confirmed Cases", "Active Cases", "Recovered Cases", "No. of Deaths"),key='statewise')

			num2 = st.slider("", 10, len(web_df),key="states")

			if get_status4() == "Confirmed Cases":
				temp_df = web_df.sort_values(by='Confirmed' , ascending = False)
				plot_states(temp_df.iloc[0:num2],'c')

			elif get_status4() == "No. of Deaths":
				temp_df = web_df.sort_values(by='Deceased' , ascending = False)
				plot_states(temp_df.iloc[0:num2],'d')

			elif get_status4() == "Active Cases":
				temp_df = web_df.sort_values(by='Active' , ascending = False)
				plot_states(temp_df.iloc[0:num2],'a')

			else:
				temp_df = web_df.sort_values(by='Recovered' , ascending = False)
				plot_states(temp_df.iloc[0:num2],'r')

			if st.checkbox("See figures",False, key="statewisee"):
				st.subheader("Statewise Data")
				st.table(web_df)

			if st.sidebar.checkbox("COVID-19 Free State/UT in India", False, key='freeee'):
				st.title("COVID-19 Free State/UT in India")
				st.subheader("List of all those State/UT where there is no active case at present.")

				filter2 = allStatesData.Active == 0
				free_states = allStatesData[filter2]
				# print(free_states)

				if len(free_states) > 0:
					free_states.sort_values(by ='Confirmed' , ascending = False , inplace = True)
					fig = go.Figure()
					fig.add_trace(go.Bar(
					    x=free_states.States,
					    y=free_states.Confirmed,
					    name='Confirmed',
					    marker_color='RED'
					))
					fig.add_trace(go.Bar(
					    x=free_states.States,
					    y=free_states.Recovered,
					    name='Recovered',
					    marker_color='GREEN'
					))
					fig.add_trace(go.Bar(
					    x=free_states.States,
					    y=free_states.Deceased,
					    name='Deceased',
					    marker_color='BLUE'
					))

						# Here we modify the tickangle of the xaxis, resulting in rotated labels.
					fig.update_layout(
					                    barmode='group',
					                    xaxis_tickangle=-45,
					                    title = "Covid-19 Free States/UT's",
					                    plot_bgcolor = '#FFEEFF'
					                )
					st.write(fig)

					if st.checkbox("See figures",False, key="free_states"):
						st.subheader("COVID-19 Free State/UT")
						st.table(free_states.set_index('States'))
				else:
					st.markdown("Sorry, At Present None of the States/UT's are COVID-19 free.")

		


note1 = '''<h2 class="note">NOTE <span style="font-size: 1.5em;">ℹ</span></h2> '''
st.sidebar.markdown(note1, unsafe_allow_html = True)
st.sidebar.info(
    ''' Click on the expand icon
    	for fullscreen view. The icon will appear
    	on the top-right corner as you hover over the Chart/Map ''')

note2 = '''<h2>ABOUT </h2> '''
st.sidebar.markdown(note2, unsafe_allow_html = True)
st.sidebar.info(
    ''' 
    	This app is developed by Shailesh Bisht.
    	#### You can find me at
    	- [LinkedIn](https://www.linkedin.com/in/shailesh-bisht-b42a73184)
    	- mail id - peskyji@gmail.com
    	#### See some of my other works at
    	- [GitHub](https://www.github.com/peskyji)
    	- [GitLab](https://www.gitlab.com/peskyji)
     ''')

note3 = '''<h2> SOURCES </h2> '''
st.sidebar.markdown(note3, unsafe_allow_html = True)
st.sidebar.info(
    ''' 
    	COVID-19 data shown in this app is updated daily. 

    	It is taken from the following sources
    	#### WORLD
    	- [WHO COVID-19](https://covid19.who.int/data)
    	#### INDIA
    	- [Covid19India](https://covid19india.org/)
     ''')

note4 = '''<h2> CONTRIBUTE </h2> '''
st.sidebar.markdown(note4, unsafe_allow_html = True)
st.sidebar.info(
    ''' 
    	This an open source project and you are very welcome to 
    	contribute your awesome comments, questions, pull request
    	to make this app better.

    	- You can find the [Source Code](https://github.com/peskyji/covid-19eda) here.
     ''')


# st.sidebar.image('bot3.png' , use_column_width=True)
# if st.sidebar.button("Ask COBot (COVID-19 Bot) to Help"):
# 	wb.open("index.html")
#---------------END OF SIDE BAR-------------------------------------------------------------------

