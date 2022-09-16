import logging
import os
import json
import csv
from dotenv import load_dotenv
import pandas as pd
# Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
# WebClient instantiates a client that can call API methods
# When using Bolt, you can use either `app.client` or the `client` passed to listeners.

load_dotenv()
SLACK_USER_TOKEN = os.getenv('SLACK_USER_TOKEN')
LISTENING_CHANNELS = os.getenv('LISTENING_CHANNELS')
ADMIN_USERS = json.loads(os.environ['ADMIN_USERS'])

print(SLACK_USER_TOKEN)
client = WebClient(token=SLACK_USER_TOKEN)
logger = logging.getLogger(__name__)
# ID of channel that the message exists in

message = []
conversation_id = LISTENING_CHANNELS
fields = ['S.No','Answers','Questions']
finalMessages=[]
slackReply=""
slackParent=""

try:
    # Call the conversations.history method using the WebClient
    # The client passes the token you included in initialization
    result = client.conversations_history(
        channel=conversation_id
    )

    filename = "./data/answers.csv"
    with open(filename, 'w',encoding='UTF8', newline='') as f1:

        for message in range(len(result["messages"])):
            slackMessage = result["messages"][message]
            slackMessageTs = slackMessage["ts"]
            resultSlackReply = client.conversations_replies(channel = conversation_id, ts=slackMessageTs)

            for message in range(len(resultSlackReply["messages"])):
                slackMessageReply = resultSlackReply["messages"][message]
                slackReplyTs = slackMessageReply["ts"]            

                slackQues = ""
                slackReply = ""

                # Parent of thread/Main question
                if slackMessageTs == slackReplyTs :
                    slackQues = slackMessageReply["text"]
                    
                # Thread answer
                elif slackMessageReply.__contains__("user") and slackMessageReply["user"] in ADMIN_USERS :                   
                    slackReply = slackMessageReply["text"]

                # Thread question
                else :
                    slackQues = slackMessageReply["text"]

                finalMessages.append({slackReply,slackQues})
                df = pd.DataFrame(finalMessages, columns=['Answers', 'Questions'])   

        df.to_csv(f1, header=True)     

            
except SlackApiError as e:
    print(f"Error: {e}")
  
    
  