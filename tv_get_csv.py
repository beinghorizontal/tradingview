from websocket import create_connection
import json
import random
import string
import re
import pandas as pd
import datetime
from time import sleep
from token_generate import get_token
import os,pickle,shutil,time

def generateSession():
    stringLength = 12
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(stringLength))
    return "qs_" + random_string


def generateChartSession():
    stringLength = 12
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(stringLength))
    return "cs_" + random_string


def prependHeader(st):
    return "~m~" + str(len(st)) + "~m~" + st


def constructMessage(func, paramList):
    # json_mylist = json.dumps(mylist, separators=(',', ':'))
    return json.dumps({
        "m": func,
        "p": paramList
    }, separators=(',', ':'))


def createMessage(func, paramList):
    return prependHeader(constructMessage(func, paramList))


def sendRawMessage(ws, message):
    ws.send(prependHeader(message))


def sendMessage(ws, func, args):
    ws.send(createMessage(func, args))

def start_ws(symbol_name='',frequency='',my_token=''):
    bars = 10000
    if frequency.split('_')[-1]=='minute':
        fr = frequency.split('_')[0]
    if frequency.split('_')[-1]=='day':
        fr = frequency.split('_')[0]+"D"
    if frequency.split('_')[-1] == 'week':
        fr = frequency.split('_')[0] + "W"
    if frequency.split('_')[-1] == 'month':
        fr = frequency.split('_')[0] + "M"


    # Initialize the headers needed for the websocket connection
    headers = json.dumps({
        'Origin': 'https://data.tradingview.com'
    })

    # Then create a connection to the tunnel
    ws = create_connection(
        'wss://data.tradingview.com/socket.io/websocket', headers=headers)
    # ws = create_connection(
    # 'wss://data.tradingview.com/socket.io/websocket?from=chart%2F8h3l56mv%2F&date=2021_05_28-12_54', headers=headers)
    session = generateSession()
    print("session generated {}".format(session))

    chart_session = generateChartSession()
    print("chart_session generated {}".format(chart_session))

    # Then send a message through the tunnel
    sendMessage(ws, "set_auth_token", [my_token])
    # sendMessage(ws, "set_auth_token", ["unauthorized_user_token"])

    sendMessage(ws, "chart_create_session", [chart_session, ""])
    sendMessage(ws, "switch_timezone", [chart_session, "Asia/Kolkata"])

    sendMessage(ws, "quote_create_session", [session])
    sendMessage(ws, "quote_set_fields",
                [session, "ch", "chp", "current_session", "description", "local_description", "language", "exchange",
                 "fractional", "is_tradable", "lp", "lp_time", "minmov", "minmove2", "original_name", "pricescale",
                 "pro_name", "short_name", "type", "update_mode", "volume", "currency_code", "rchp", "rtc"])
    sendMessage(ws, "quote_add_symbols", [session, symbol_name, {"flags": ['force_permission']}])

    sendMessage(ws, "resolve_symbol",
                [chart_session, "sds_sym_1", "={\"symbol\":\""+symbol_name+"\",\"adjustment\":\"splits\",\"session\":\"extended\"}"])

    # sendMessage(ws, "resolve_symbol",
    #             [chart_session, "sds_sym_1", "={\"symbol\":\""+symbol_name+"\",\"adjustment\":\"splits\"}"])


    sendMessage(ws, "create_series", [chart_session, "sds_1", "s1", "sds_sym_1", fr, bars])


    # sendMessage(ws, "request_more_data", [session, "sds_1", 1400])
    #
    # sendMessage(ws, "request_more_tickmarks", [session, "sds_1", 10])
    sendMessage(ws, "quote_fast_symbols", [session, symbol_name])


    sendMessage(ws, "create_study", [chart_session, "st5", "st1", "sds_1", "Volume@tv-basicstudies-124",
                                     {"length": 20, "col_prev_close": "false"}])

    sendMessage(ws, "quote_hibernate_all", [session])

    #create csv
    while True:
        try:
            sleep(1)
            result = ws.recv()
            pattern = re.compile("~m~\d+~m~~h~\d+$")
            if pattern.match(result):
                ws.recv()
                ws.send(result)
                print("\n\n\n " + str(result) + "\n\n")
            print(result)
        except Exception as e:
            print(e)
            break

        catch = re.search('\"m\":(.+?)\,\"p\"', result)
        if catch:
            catch_text = catch.group(1)
        else:
            catch_text='error'

        if catch_text == '"timescale_update"':#desired message contains timescale_update then we break the loop
            break
    return result

#my_token = "eyJhbGciOiJSUzUxMiIsImtpZCI6IkdaeFUiLCJ0eXAiOiJKV1QifQ.eyJ1c2VyX2lkIjoxNTA2ODMsImV4cCI6MTYyMjMzNTUxNiwiaWF0IjoxNjIyMzIxMTE2LCJwbGFuIjoiIiwiZXh0X2hvdXJzIjoxLCJwZXJtIjoiIiwic3R1ZHlfcGVybSI6IiIsIm1heF9zdHVkaWVzIjozLCJtYXhfZnVuZGFtZW50YWxzIjowLCJtYXhfY2hhcnRzIjoxLCJtYXhfYWN0aXZlX2FsZXJ0cyI6MX0.Y7FRcowdVwknx2OSWHB8HL6Gbspc9Y4KJEBWSuadPEPY4hi3WAeXKXep25caTkXFdu2unlAf4mzDV2C0kZztW-RGbR3oM_iazqRVmLdNmZdCqu878h3qlwKSpoJs4jcTPcjcq5oSsErnr4IASkxosCC8X5Aur_YxlmRiCXpMiR4"
#get_token()

def generate_csv(username,password,symbol_name,frequency):
    path = os.path.join(os.path.expanduser('~'), '_trading_view/')
    if not os.path.exists(path):
        os.mkdir(path)

    chromedriver_path = path + 'chromedriver.exe'

    if not os.path.exists(chromedriver_path):
        os.system('pip install chromedriver-autoinstaller')
        import chromedriver_autoinstaller
        ch_path = chromedriver_autoinstaller.install(cwd=True)
        if ch_path is not None:
            # chromedriver_path_exe = os.path.join(ch_path, 'chromedriver.exe' if '.exe' in path else '')
            shutil.copy(ch_path, chromedriver_path)
            try:
                time.sleep(1)
                os.remove(ch_path)
            except:
                print(f"unable to remove file '{ch_path}', you may want to remove it manually")

    token_path = path + 'tv_token.pkl'
    csv_name=symbol_name.split(':')[-1][0:3]+frequency+'.csv'
    csv_path = path+csv_name

    if os.path.exists(token_path):
        with open(token_path, 'rb') as f:
            contents = pickle.load(f)
            if contents['date'] == datetime.date.today():
                token = contents['token']
            else:
                get_token(username, password, chromedriver_path, token_path)
                with open(token_path, 'rb') as f:
                    contents = pickle.load(f)
                    if contents['date'] == datetime.date.today():
                        token = contents['token']
    else:
        get_token(username, password, chromedriver_path, token_path)
        with open(token_path, 'rb') as f:
            contents = pickle.load(f)
            if contents['date'] == datetime.date.today():
                token = contents['token']

    my_token = token

    result = start_ws(symbol_name=symbol_name,frequency=frequency,my_token=my_token)

    m = re.search('\"s\"\:(.+?)\,\"ns\"', result)
    if m:
        des_text = m.group(1)
    else:
        print('error text')
    # print(des_text)
    try:
        json_1 = json.loads(des_text)
    except:
        print('Error. Check input parameters. Check tv_pkl file @ '+path+' with size = 1kb')
    df1 = pd.DataFrame(json_1)
    df = df1['v'].apply(pd.Series)
    df.columns = ['datetime','open','high','low','close','volume']
    #convert unix datetime to human redable format
    # df['datetime'] =pd.to_datetime(df['datetime'],unit='s')
    df['datetime'] =pd.to_datetime(df['datetime'],unit='s').dt.tz_localize('utc').dt.tz_convert('Asia/Kolkata')
    df['datetime']=df['datetime'].dt.tz_localize(None)
    #df['close'].plot()
    print('csv exported to '+path)
    df.to_csv(csv_path,header=True,index=None)
    return df

