import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.tools as tls
from chart_studio import plotly as py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
import base64
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__,external_stylesheets=external_stylesheets)

df = pd.read_csv("C:/Users/User/Downloads/games.csv")
df = df.drop_duplicates()

# -------------------------------------------------------------------------------------------------------------- 

#											PART 1: DESIGN PARAMETERS

# --------------------------------------------------------------------------------------------------------------
# Here we will set the colors, margins, DIV height&weight and other parameters

colors = {
		'full-background': 	'#DCDCDC',
		'block-borders': 	'#7F7F7F',
        'text': '#0D2A63'
}

margins = {
		'block-margins': '10px 10px 10px 10px',
		'block-margins': '4px 4px 4px 4px'
}

sizes = {
		'subblock-heights': 320
}

# -------------------------------------------------------------------------------------------------------------- 

#											PART 2: ACTUAL LAYOUT

# --------------------------------------------------------------------------------------------------------------
# Here we will set the DIV-s and other parts of our layout
# We need too have a 2x2 grid
# I have also included 1 more grid on top of others, where we will show the title of the app



# -------------------------------------------------------------------------------------- DIV for TITLE
div_title = html.Div(children =	html.H1('Chess DataViz'),
					style = {
							'border': '3px {} solid'.format(colors['block-borders']),
							'margin': margins['block-margins'],
							'text-align': 'center',
                            'color': colors['text']
							}
					)

# -------------------------------------------------------------------------------------- DIV for first raw (1.1 and 1.2)
data = df.groupby(by=["rated", "winner"]).size().reset_index(name="counts")
data = data.sort_values('counts', ascending=True)
fig_1_1 =  px.bar(data, x="rated", y="counts", color = "winner",  barmode='group')
div_1_1 = dcc.Graph(children = 'block 1-1',
				    figure  = fig_1_1,
					style = {
							'border': '1px {} solid'.format(colors['block-borders']),
							'margin': margins['block-margins'],
							'width': '49%',
							'height': sizes['subblock-heights']
					})

fig_1_2 = go.Figure()
fig_1_2.add_trace(go.Histogram(x=df["white_rating"], cumulative_enabled=True))
fig_1_2.update_layout(title="Cumulative Distribution of White Player`s Ratings")
div_1_2 = dcc.Graph(children = 'block 1-2',
					figure  = fig_1_2,
					style = {
							'border': '1px {} solid'.format(colors['block-borders']),
							'margin': margins['block-margins'],
							'width': '49%',
							'height': sizes['subblock-heights']
					}
				)



# Collecting DIV 1.1 and 1.2 into the DIV of first raw.
# Pay attention to the 'display' and 'flex-flaw' attributes.
# With this configuration you are able to let the DIV-s 1.1 and 1.2 be side-by-side to each other.
# If you skip them, the DIV-s 1.1 and 1.2 will be ordered as separate rows.
# Pay also attention to the 'width' attributes, which specifiy what percentage of full row will each DIV cover.
div_raw1 = html.Div(children =	[div_1_1,
								div_1_2
								],
					style ={
							'border': '3px {} solid'.format(colors['block-borders']),
							'margin': margins['block-margins'],
							'display': 'flex',
							'flex-flaw': 'row-wrap'
							})


# -------------------------------------------------------------------------------------- DIV for second raw (2.1 and 2.2)
fig_2_1 = px.scatter( df, x="black_rating", y="white_rating", color="opening_ply")
div_2_1 = dcc.Graph(children = 'block 2-1',
				    figure = fig_2_1,
					style = {
							'border': '1px {} solid'.format(colors['block-borders']),
							'margin': margins['block-margins'],
							'width': '49%',
							'height': sizes['subblock-heights']
					}
				)

sns.boxplot(x="winner", y="turns",
			data=df, palette="Set3")
plt.savefig("mpl_fig.png")
image_data = 'mpl_fig.png'
encoded = base64.b64encode(open(image_data, 'rb').read()).decode()

div_2_2= html.Img(src='data:image/png;base64,{}'.format(encoded),
					style = {
							'border': '1px {} solid'.format(colors['block-borders']),
							'margin': margins['block-margins'],
							'width': '49%',
							'height': sizes['subblock-heights']
					}
				)


div_raw2 = html.Div(children =	[div_2_1,
								div_2_2
								],
					style ={
							'border': '3px {} solid'.format(colors['block-borders']),
							'margin': margins['block-margins'],
							'display': 'flex',
							'flex-flaw': 'row-wrap'
							})

# -------------------------------------------------------------------------------------- Collecting all DIV-s in the final layout
# Here we collect all DIV-s into a final layout DIV

app.layout = html.Div([
						div_title,
						div_raw1,
						div_raw2
						],
						style = {
							'backgroundColor': colors['full-background']
						}
					)




# -------------------------------------------------------------------------------------------------------------- 

#											PART 3: RUNNING THE APP

# --------------------------------------------------------------------------------------------------------------
# >> use __ debug=True __ in order to be able to see the changes after refreshing the browser tab,
#			 don't forget to save this file before refreshing
# >> use __ port = 8081 __ or other number to be able to run several apps simultaneously
app.run_server(debug=True, port = 8081)