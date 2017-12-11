###BLOCK 1 OF CODE

#These are all the imports that we will be using throughout the program. There are various different imports due 
# to the functionality we needed to pull data from the web. These imports range from importing json to regex and
# many in between.

import re
import json
import requests
import pandas as pd
from skimage import io

import plotly 
plotly.tools.set_credentials_file(username='jos.auve', api_key='EzZSMetOMn67wMgtmPJq')
import plotly.plotly as py
import plotly.graph_objs as go
from datetime import datetime
import pandas_datareader.data as web

import warnings
warnings.filterwarnings('ignore')



#This is the program introduction, 'Try it out!"
print("This program will show you Earnings Releases and corresponding stock data for the companies. Try it out!")
print("***" * 20)
print(" ")
print("ENTER any historical date OR \n ENTER a date within two weeks from today.")
print("---" * 20)



#This prompts the user for which earnings release date they would like to view.
month_prompt = input("Enter a month (Ex: December): ")
day_prompt = input("Enter a weekday (Ex: 12): ")
year_prompt = input("Enter a year (Ex: 2017): ")
print(" ")



#This formats the user input to replace it into the nasdaq (website) link below. In a "Dec-12-2017" format 
# (Other variations are accepted)
stock_date = ''+ year_prompt +'-'+ month_prompt +'-'+ day_prompt +''



#This sees if the data frame, data[3], is the correct html dataframe that we are looking for on the webpage. If it is 
# not, then perhaps the date is a weekend, or too far in advance.
try:
    website = 'http://www.nasdaq.com/earnings/earnings-calendar.aspx?date='+ stock_date +''
    data = pd.read_html(website)
    df = data[3]
    validator = df.columns[0].split()
    i = ['Time']
    for i in validator:
        print('Here are all of the companies releasing earnings on '+ month_prompt +' '+ day_prompt +', '+ year_prompt +'.')
except AttributeError:
    print('We do not have any data for earnings releases on '+ month_prompt +' '+ day_prompt +', '+ year_prompt +'. \n Please choose a weekday within 2 weeks from today.')
except Exception as e:
    print("Oops! Looks like you did not enter a valid date. \n Make sure to follow the guidelines for all inputs. \n We are displaying your previous search for your convenience.")
    


    
#This block of code creates a "Valid Choices" list pulled from the dataframe from NASDAQ (data[3]) above. If it is not
# the correct dataframe, the code will pass. If the list is created, the user may only input stocks off of this list
# to view the code.
try:      
    earnings_data = pd.DataFrame()
    classes = earnings_data.append(data[3], ignore_index=True)
    classes.columns = ['Time','Company Name (Symbol)','Reported Date','Fiscal Quarter Ending','Consensus EPS Forecast','Num. of Ests','Last Years Report Date','EPS','Percent Surprise']
    company_names = classes['Company Name (Symbol)']
    company_data = str(company_names)
    company_symbol = company_data.replace(r'[^(]*\(|\)[^)]*', '')
    text_list = company_symbol.split()
    valid_choices = []
    exp = '\(([A-Z]+)\)'
    pattern = re.compile(exp)
    for text in text_list:
        result = re.findall(pattern, text)
        if result:
            valid_choices.append(result[0])
except:
    pass
    
    
    
    
#This function gets stock data based on the stock picked by the user. The data is taken from the google financr API.
def GetStockData():
    try:
        stock_link = 'https://finance.google.com/finance?q='+ stock_choice +'&output=json'
        rsp = requests.get(stock_link)
        fin_data = json.loads(rsp.content[6:-2].decode('unicode_escape'))

        #Print Stock Data Output
        #Prints company name and industry
        print(" ")
        print("Here is the Stock Information for %s." % stock_choice)
        print(' ')
        print('***' * 10)
        #next print is Company Name
        print('{}'.format(fin_data['name']))
        #next print is Industry
        print('{}'.format(fin_data['sname']))
        print('***' * 10)
        print(' ')

        #Prints general and current company stock data
        print('Today')
        print('===' * 10)
        print('Current Trade Price: {}'.format(fin_data['l']))
        print('Opening Price: {}'.format(fin_data['op']))
        print('Todays Change: {}'.format(fin_data['c']))
        print('Todays Change Percentage: {}'.format(fin_data['cp']))
        print(' ')
        print(' ')

        #Prints general and relevant company data
        print('General')
        print('===' * 10)
        print('52-Week High: {}'.format(fin_data['hi52']))
        print('52-Week Low: {}'.format(fin_data['lo52']))
        print('Price/Earnings Ratio: {}'.format(fin_data['pe']))
        print('Earnings per Share: {}'.format(fin_data['eps']))
        print(' ')
        print(' ')

        #Prints companies previous margin data
        print('Previous')
        print('===' * 10)
        print('Recent Quarter Date: {}'.format(fin_data['kr_recent_quarter_date']))
        print(' ')
        print('Net Profit Margin (Recent Quarter): {}'.format(fin_data['keyratios'][0]['recent_quarter']))
        print('Net Profit Margin (Annual): {}'.format(fin_data['keyratios'][0]['annual']))
        print('Net Profit Margin (TTM): {}'.format(fin_data['keyratios'][0]['ttm']))
        print(' ')
        print('Operating Margin (Recent Quarter): {}'.format(fin_data['keyratios'][1]['recent_quarter']))
        print('Operating Margin (Annual): {}'.format(fin_data['keyratios'][1]['annual']))
        print('Operating Margin (TTM): {}'.format(fin_data['keyratios'][1]['ttm']))
        print(' ')
        print(' ')

        #Prints company description
        print('Description')
        print('===' * 10)
        print('{}'.format(fin_data['summary'][0]['overview']))
    except Exception as e:
        print(" ")
        print('Unfortunately, we do not have sufficient company data to show for: '+ stock_choice +'. \n Our engineers are working on this issue as we speak, and are able to offer you a Performance Graph. \n Please come back to try this company again soon.')

    

#This function gets the corresponding graph from Plotly as an image instead of an interactive graph, since in this way
# there is not a 25 call limit. Pulling as a png will give us 100 free calls to Plotly. This grahph is also pulled as
# an image to combat issues with jupyter being unable to continue the code after the object is printed. As a PNG, we
# allow the code to continue after the imaged is "showed."
def GraphPostOrPass():
    if stock_choice in valid_choices:
        try:
            df = web.DataReader(stock_choice, 'yahoo',
                            datetime(2017, 1, 1),
                            datetime(2018, 1, 1))
            data = [go.Scatter(x=df.index, y=df.High)]
            py.image.ishow(data, format='png', scale=2.5)
        except Exception as e:
            print(" ")
            print("We are unable to show a Performance Graph for this stock. We apologize for the inconvenience.")
    else:
        pass
    

    
#This function gets an analyst recommendation for the chosen stock by going to NASDAQ an dpulling an image of their
# analyst recommendation slider. This is what is printed on the bottom.
def AnalystRecommendation():
    rsp = requests.get('http://www.nasdaq.com/charts/'+ stock_choice +'_rm.jpeg')
    if rsp.status_code in (200,):
        print('Here is our Official NASDAQ Analyst Recommendation for '+ stock_choice +': ')
        io.imshow(io.imread('http://www.nasdaq.com/charts/'+ stock_choice +'_rm.jpeg'))
        io.show()
    else:
        print(" ")
        print('We do not have an Official NASDAQ Analyst Recommendation for '+ stock_choice +'')


#This finction will run all three of the above functions, if and only if the stock choice is in the list"Valid 
# Choices," otherwise it will print an "Oops" statment.
def GetAllData():
    if stock_choice in valid_choices:
        GetStockData() #Get the stock data
        GraphPostOrPass() #Get the Graph
        AnalystRecommendation() #Get the Recommendation
    else:
        print(" ")
        print('Oops! It doesnt look like the stock you entered is on the earnings calendar for '+ month_prompt +' '+ day_prompt +', '+ year_prompt +'. \n Please try again. Make sure you enter a symbol from the list above. \n If you did not type in all caps, please do so this time.')

    


#This prints the datafram from NASDAQ. We were forced to write our code this way since Jupyter would not allow us to
# display the df in a conditional statement. Due to this reason, we were unable to add the desired loops to our code.
#             ALSO
#If there is a name error when trying to run code for first couple times, we are not able to fix that since we can not
# display "df" in a try and except or any other conditional method.
df




###BLOCK 2 OF CODE

print(valid_choices) #This prints a list from the NASDAQ dataframe above
stock_choice = input("Please enter a stock from the list above (or below for your convenience): ")
GetAllData() #Calls function to run this second section of the code (If graph does not load - please try again.)
