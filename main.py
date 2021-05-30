from tv_get_csv import generate_csv

#inputs
symbol_name="MCX:GOLD1!"
username = 'your_emial id or user name'
password = 'trading view password'

# symbol_name="NSE:NIFTY1!"
frequency="1_day" #"1_minute", "1_day" , "1_week", "1_month"

df =generate_csv(username,password,symbol_name,frequency)
