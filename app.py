##############################################################
# Purpose: demo of building a web app using Flask and deploy it using Heroku
# Reference:
            # QUANDL API: https://docs.quandl.com/docs/in-depth-usage
			# https://github.com/bev-a-tron/MyFlaskTutorial
			# http://virantha.com/2013/11/14/starting-a-simple-flask-app-with-heroku/
            # http://bokeh.pydata.org/en/latest/docs/gallery/stocks.html
            # https://bokeh.pydata.org/en/latest/docs/user_guide/embed.html
            # http://biobits.org/bokeh-flask.html
            # https://groups.google.com/a/continuum.io/forum/#!topic/bokeh/0yN25ZoCyiY
            # https://davidhamann.de/2018/02/11/integrate-bokeh-plots-in-flask-ajax/
# Example page: http://lemurian.herokuapp.com
# Enhancement:
    # - add date range
    # - add try exception logic for invalid ticker input
    # - resize the plot
    # - add tooltip
##############################################################

from flask import Flask, render_template, request, redirect
import requests
# import simplejson
import pandas as pd
from bokeh.plotting import figure, reset_output
from bokeh.models import HoverTool
from bokeh.io import output_file, show
from bokeh.embed import components

def get_price(ticker):
        # time-series for one stock
    # url = "https://www.quandl.com/api/v3/datasets/WIKI/FB/data.json?api_key=x_PTzbJS8kbBw9yszh6s"
    # time-series for one stock and its metadata
    url = "https://www.quandl.com/api/v3/datasets/WIKI/{t1}.json?api_key=x_PTzbJS8kbBw9yszh6s".format(t1=ticker)

    # Package the request, send the request and catch the response: r
    r = requests.get(url)

    # Decode the JSON data into a dictionary: json_data
    json_data = r.json()
    json_data = json_data['dataset']

    # create dataframe of prices
    df = pd.DataFrame(json_data['data'], columns=json_data['column_names'])
    ticker_name = json_data['dataset_code']
    data_from = json_data['oldest_available_date']
    data_to = json_data['newest_available_date']
    freq = json_data['frequency']

    # convert date column to datetime format
    df['date_t']=pd.to_datetime(df.Date)
    return df, ticker_name

def create_graph(t1, t2):
    df1, ticker1 = get_price(t1)
    df2, ticker2 = get_price(t2)

    # reset the html page otherwise multiple plots will appear
    reset_output()
    # p = figure(x_axis_type='datetime', y_axis_label='Price')
    p = figure(x_axis_type='datetime', y_axis_label='Price')
    p.line(df1['date_t'], df1['Close'], color='FireBrick', legend=ticker1)
    p.line(df2['date_t'], df2['Close'], color='DarkBlue', legend=ticker2)
    p.legend.location = "top_left"

    # output_file('stock_app.html')
    # show(p)
    return p


app = Flask(__name__)

@app.route('/')
def index():
    # load template file index.html
    return render_template('index.html')

# have to add methods so the page can get input from previous page
@app.route('/graph', methods=['GET','POST'])
def display():
    # assign user input to variables of app
    app.symbol1 = request.form['symbol1']
    app.symbol2 = request.form['symbol2']

    # create plot using inputs from users
    plot = create_graph(app.symbol1, app.symbol2)

    # Embed plot into HTML via Flask Render
    script, div = components(plot)

    return render_template('graph.html', script=script, div=div)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)
    # app.run(port=33507, debug=True)

# what are the port numbers?