import re

#import chardet
from time import sleep

import requests
import subprocess
import datetime
import os,sys

#set your testbot settings here:
BOT_TOKEN = 'xxxxxx_bot_token'
BOT_NAME = 'xxxxxtestbot_name'
#ngrok can redirect to any IP:PORT in your LAN!
#if run on the same host use 127.0.0.1
REDIR_LOCAL_IP_PORT='192.168.1.100:8080'

BOT_URL = 'https://api.telegram.org/bot' + BOT_TOKEN + '/'
TELEG_URL = 'https://telegram.me'
#log file of ngrok where channel id can be found
NGROK_FILE_LOG = 'ngrok.log'
#file to keep track to restart on time
NGROK_RESTART_LOG = 'ngrok_restart.log'
TIME_PERIOD = 3
#if true -  then it gets restarted every time script executed
UNCOND = False

def subroutine(args):
    cmd = subprocess.Popen(args, stdout=subprocess.PIPE, shell=True) #чтобы можно было вводить с аргументами

    for line in cmd.stdout:
        print(line)

def webHook(channel_id):
    # setup webhook
    # ngrok must be set to tunnel on 8000 port localhost + path url (param1)
    param_path_url = '/webhooks/telegram_bot/'
    param_sethook_cmd = f'setWebhook?url={channel_id}'
    url = BOT_URL + param_sethook_cmd + param_path_url
    print(f'setting up url to telegram {url}')
    r = requests.get(url)
    print(r.content)

def update_restart_log(file_name):
    with open(file_name, 'w', encoding='utf-8') as FILE:
        time_now = datetime.datetime.now()
        time_now_str = time_now.strftime("%Y-%m-%d %H:%M:%S")
        print(f"Restarted: date and time : {time_now_str}")
        FILE.write(time_now_str)

def parse_str(text):
    link_pattern = r'url=(https://.+io)'
    if re.search(link_pattern, text):
        return re.search(link_pattern, text).group(1)

    return None

def parse_channel_id(file_name):
    with open(file_name, encoding='utf-8') as f_n:
        for el_str in f_n:
            #print(el_str, end='')
            channel_id = parse_str(el_str)
            if channel_id:
                return channel_id

    return None

def restart_ngrok(lcl_path):
    #kill ngrok old daemon
    ngrok_kill_str='killall ngrok'
    print(f'exec {ngrok_kill_str}')
    subroutine(ngrok_kill_str)

    print('ngrok killed')
    #start new daemon
    sleep(10)
    ngrok_start_str = f'{lcl_path}ngrok http {REDIR_LOCAL_IP_PORT} -log=stdout > {lcl_path}ngrok.log &'
    print(f'exec {ngrok_start_str}')
    subroutine(ngrok_start_str)

    print('ngrok started')

    sleep(15)
    #set ngroks new tunnel to webhook
    channel_id = parse_channel_id(f'{lcl_path}{NGROK_FILE_LOG}')

    if channel_id:
        webHook(channel_id)
        print('================================================')
        print(f'ngrok set to webhook on channel = {channel_id}')
        return True

    print('error channel_id not found.')
    return False

def check_period(file_name):

    time_now = datetime.datetime.now()
    print("Checking: \n Current date and time : ", end='')
    print(time_now.strftime("%Y-%m-%d %H:%M:%S"))

    try:
        with open(file_name, encoding='utf-8') as f_n:
            el_str = f_n.readline().strip() # get rid of \n
            print(f' Last time was : {el_str}')
            print(f' Time Period is set to {TIME_PERIOD} hrs, UNCOND flag is {UNCOND}')
            time_last = datetime.datetime.strptime(str(el_str), '%Y-%m-%d %H:%M:%S')

            diff = time_now - time_last

            hours = int(diff.seconds / (60 * 60)) + diff.days * 24

            print (f'there was {hours} hrs since last restart')

            if UNCOND:
                return True
            if hours >= TIME_PERIOD:
                return True
    except:
        #nofile create it and return true so it will call restart for the first time
        update_restart_log(file_name)
        return True


    return False


print(f'============={os.path.abspath(__file__)}==============')
print(f'script name: {os.path.basename(__file__)} ')

lcl_path = os.path.abspath(__file__).replace(os.path.basename(__file__),'')

print(f'script path: {lcl_path}')



if check_period(f'{lcl_path}{NGROK_RESTART_LOG}'):
    print('restart required')
    if restart_ngrok(lcl_path):
        #if successful put new time to NGROK_RESTART_LOG
        update_restart_log(f'{lcl_path}{NGROK_RESTART_LOG}')

else:
    print('no need to restart')

print(f'============={os.path.abspath(__file__)}==============\n')
