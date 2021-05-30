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

frequency="1_day" #"1_minute", "1_day" , "1_week", "1_month" #You can't exceed 5000 bars with a free account no matter the bar frequency. So one-minute data will be approximately 10 to 12 days of history. For 30 minute you will get around 13 months of data. 

By default it try to fetch max bars allowed by TradingView, if you need lower number of bars (less than 5k) then change line 50 bars=10000 to bars=your desired number 

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

It will look like this (arrow_1)

![image](https://user-images.githubusercontent.com/28746824/120113544-97bf0480-c198-11eb-82a8-909a4b07fb6d.png)

In the image, the top arrow_2 is where you have to click ('network' tab) , 

Then click on 'ws' ( arrow_3)

'ws' stands for WebSocket and TradingView chart gets the data through WebSocket

WebSocket code has a typical format. You can copy the code in tv_get_csv.py and make few changes

 Something like this

![image](https://user-images.githubusercontent.com/28746824/120108510-11e48e80-c183-11eb-8778-839e4dbeb00b.png)

In the image Arrow_1 = scroll the cursor up

Arrow_2 click 'chart_create_session'

Arrow_3 Text will apear. Observe the text and see the see the similarities b/w our code 

sendMessage(ws, "chart_create_session", [chart_session, ""]) #chart session is dynamically generated with this line  chart_session = generateChartSession() 

Another example (felt above one wasn't that clear )

![image](https://user-images.githubusercontent.com/28746824/120113816-ddc89800-c199-11eb-8a12-f4cd76941329.png)

In the above chart, Arrow_1 is pointing at a small red bar in websocket response- indicates message came from server & Arrow_2 pointing at green bar indicates message sending to the server. So in our code all our sendMessage() are copied from message in front of green bars

Let's click Arrow_3

Arrow_4 click there to expand the message

Let's get back to our code tv_get_csv.py where we are writing websocket sendMessage(), check this line  


sendMessage(ws, "create_series", [chart_session, "sds_1", "s1", "sds_sym_1", fr, bars])

This is what exactly written at Arrow_4

Similarly, observe other lines near to that line in the code and match with 'ws' tab in the browser. This is where changes will trigger 1st when Tradingview add or remove the features or change the user interface.
