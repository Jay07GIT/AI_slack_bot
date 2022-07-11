from oauth2client.service_account import ServiceAccountCredentials
from sklearn.feature_extraction.text import CountVectorizer
from dotenv import load_dotenv
from slack_bolt import App
from datetime import date
from model import model
from slack_message_helper import SlackMessageHelper
import pandas as pd
import numpy as np
import subprocess
import datetime
import gspread
import logging
import pickle
import json
import os
import json

load_dotenv()

LISTENING_CHANNELS = os.getenv('LISTENING_CHANNELS').split(',')
TARGET_CHANNELS = os.getenv('TARGET_CHANNELS').split(',')
SLACK_API_TOKEN = os.getenv('SLACK_BOT_TOKEN')
SIGNING_SECRET = os.getenv('SLACK_SIGNING_SECRET')
CLIENT_SECRET_FILE = os.getenv('CLIENT_SECRET')
DEBUG = os.getenv('DEBUG') == 'True'
BOT_ID = os.getenv('BOT_ID')
PORT = int(os.getenv('PORT'))

print(SLACK_API_TOKEN,SIGNING_SECRET)

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

app = App(token=SLACK_API_TOKEN, signing_secret=SIGNING_SECRET)

slack_message_helper = SlackMessageHelper()
print(SLACK_API_TOKEN,SIGNING_SECRET)

@app.event("app_mention") 
def event_test(say):     
    say("Hi there!")

@app.event("message")
def message(payload, say, client):
    print("suma",client)
    channel_id = payload['channel']
    print(channel_id)
    user_id = payload['user']
    print(user_id)
    try:
    # Call the users.info method using the WebClient
        result = client.users_info(
            user=user_id
        )
        print(result)

    except SlackApiError as e:
        print("Error fetching conversations: {}".format(e))
    print(result)
    user_name = result["user"]["real_name"]
    print(user_name)
    text = payload['text']
    print(text)
    say("Hi there!")
    no_reply_team_members = ["jay.applemai"]
    print(user_id,channel_id,user_name,text)

    if 'parent_user_id' not in payload.keys() and user_name not in no_reply_team_members:
        print("if",BOT_ID,user_id,text,channel_id,TARGET_CHANNELS)
        if channel_id in TARGET_CHANNELS:
            print("if0",channel_id,TARGET_CHANNELS,text,BOT_ID != user_id and text)
            if BOT_ID != user_id and text:
                print("if1",BOT_ID,user_id,text)
                ts = payload['event_ts']
                print("if6",ts)

                res, intent, prob = slack_message_helper.get_response(text)

                if DEBUG:
                    print("if2",BOT_ID,user_id,text)
                    say(thread_ts=ts, text=res)
                else:
                    print("if3",BOT_ID,user_id,text)
                    if intent not in ['irrelevant', 'no-reply'] and prob >= 0.50:
                        say(thread_ts=ts, text=res)

                    print("if4",BOT_ID,user_id,text)

                    slack_message_helper.get_sheet_cover(text, intent, channel_id, user_name, ts, prob)

        elif channel_id in LISTENING_CHANNELS:
            print(BOT_ID,user_id,text)
            if BOT_ID != user_id and text:

                res, intent, prob = slack_message_helper.get_response(text)
                print(BOT_ID,user_id,text)

                ts = payload['event_ts']

                slack_message_helper.get_sheet_cover(text, intent, channel_id, user_name, ts, prob)

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO,
                        filename='./logs/app_logs/' + date.today().strftime("%d-%m-%Y") + '.log',
                        filemode='a')

    logging.info("App is running!")
    app.start(port=5050)