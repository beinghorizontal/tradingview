# tradingview
# Download this Github folder https://github.com/beinghorizontal/tradingview as a zip, then unzip to a local folder on PC

# Go to that folder and open command prompt from there (shift+right click in Windows)

# In cmd write: 
pip install -r requirements.txt

This will install all required libraries and you are all set

## Example:
#Open main.py

from tv_get_csv import generate_csv

"inputs:"

symbol_name="MCX:GOLD1!" #symbol structure is exchange name:Symbol that you see on the chart. For the continuous futures chart add !  

"(symbol_name="NSE:NIFTY1!")"

username = 'your_emial id or user name'

password = 'trading view password'

df =generate_csv(username,password,symbol_name,frequency) #You will get dataframe with datetime, O,H,L,C,V and one csv copy will get exported to user folder that it made above

frequency="1_day" #"1_minute", "1_day" , "1_week", "1_month" #You can't exceed 5000 bars with a free account no matter the bar frequency. So one-minute data will be approximately 10 to 12 days of history. For 30 minute you will get around 13 months of data

## Few notes

The first time when you run the above main.py code it will do these few things which are one time:
a) It will create a new folder in user directory ("c:/user/your_pc_name/_trading_view/")

b) It needs selenium to authenticate (It's headless so you wouldn't see it is running), and code assumes you don't have chromedriver.exe for it, so it installs chromedriver.exe matching the exact version of your Chrome web browser. It's a 12MB file, it avoids all file_path errors which is annoying with Selenium.

c)At the beginning of the day it will do fresh authentication as tokens get expire, so be patient it takes a lot of time - near about a half minute afterwards every subsequent execution will be fast. You can tweak with time.sleep setting in token_generate.py

## Now the tutorial part about how to make the web scraper like this 

Think about web scraping is sooner or later they gonna change the website design and any small change will make the entire code useless so you have to know where to look at it and how to edit the code.

The best part is it's all really simple.

Open tradingview chart
Then press Ctrl+Shift+i (after Right Click inspect tab)
A small window will appear inside the existing browser tab.

It will look like this

![image](https://user-images.githubusercontent.com/28746824/120108487-f4172980-c182-11eb-8f94-77f20bc4a249.png)

In the image, the top arrow is where you have to click ('network' tab) , 

Then click on 'ws' ( second arrow)

'ws' stands for WebSocket and TradingView chart gets the data through WebSocket

WebSocket code has a typical format. You can copy the code in tv_get_csv.py and make few changes

 Something like this

![image](https://user-images.githubusercontent.com/28746824/120108510-11e48e80-c183-11eb-8778-839e4dbeb00b.png)

In the image Arrow_1 = scroll the cursor up

Arrow_2 click 'chart_create_session'

Arrow_3 Text will apear. Observe the text and see the see the similarities b/w our code 

sendMessage(ws, "chart_create_session", [chart_session, ""]) #chart session is dynamically generated with this line  chart_session = generateChartSession() 
 
Similarly, observe other lines near to that line in the code and match with 'ws' tab in the browser. This is where changes will trigger 1st when Tradingview add or remove the features or change the user interface.
