from oauth2client.service_account import ServiceAccountCredentials
from sklearn.feature_extraction.text import CountVectorizer
from dotenv import load_dotenv
from slack_bolt import App
from datetime import date
from model import model
from pandas import DataFrame, concat
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

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

app = App(token=SLACK_API_TOKEN, signing_secret=SIGNING_SECRET)

slack_message_helper = SlackMessageHelper()

@app.event("message")
def message(payload, say, client):
    channel_id = payload['channel']
    user_id = payload['user']
    try:
    # Call the users.info method using the WebClient
        result = client.users_info(
            user=user_id
        )

    except SlackApiError as e:
        print("Error fetching conversations: {}".format(e))
    user_name = result["user"]["real_name"]
    text = payload['text']
    no_reply_team_members = ["jay.applemai"]

    if 'parent_user_id' not in payload.keys() and user_name not in no_reply_team_members:
        if channel_id in TARGET_CHANNELS:
            if BOT_ID != user_id and text:
                ts = payload['event_ts']

                res, intent, prob = slack_message_helper.get_response(text)
                csv = pd.read_csv("""./data/questions.csv""")
                category_index = csv[csv['category'] == intent].index[2]
                category_enc = csv.loc[category_index, ['category_enc']].to_string(index = False)
                df = pd.DataFrame(csv)
                newLine = DataFrame({'category': intent,'category_enc' : category_enc,'question': text}, index=[csv[csv['category'] == intent].index[2]])
                newDf= concat([df.iloc[:csv[csv['category'] == intent].index[2]], newLine, df.iloc[csv[csv['category'] == intent].index[2]:]]).reset_index(drop=True)
                newDf.to_csv('./data/questions.csv',index=False)
                if DEBUG:
                    say(thread_ts=ts, text=res)
                else:
                    if intent not in ['irrelevant', 'no-reply'] :
                        say(thread_ts=ts, text=res)

                    slack_message_helper.get_sheet_cover(text, intent, channel_id, user_name, ts, prob)

        elif channel_id in LISTENING_CHANNELS:
            if BOT_ID != user_id and text:

                res, intent, prob = slack_message_helper.get_response(text)
                ts = payload['event_ts']

                slack_message_helper.get_sheet_cover(text, intent, channel_id, user_name, ts, prob)

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO,
                        filename='./logs/app_logs/' + date.today().strftime("%d-%m-%Y") + '.log',
                        filemode='a')

    logging.info("Bot is running successfully!")
    app.start(port=5050)