from itertools import count
import logging
import os
import csv
from dotenv import load_dotenv
import pandas as pd
import numpy as np
# Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
# WebClient instantiates a client that can call API methods
# When using Bolt, you can use either `app.client` or the `client` passed to listeners.

load_dotenv()
SLACK_USER_TOKEN = os.getenv('SLACK_USER_TOKEN')
LISTENING_CHANNELS = os.getenv('LISTENING_CHANNELS')

client = WebClient(token=SLACK_USER_TOKEN)
logger = logging.getLogger(__name__)
# ID of channel that the message exists in

message = []
conversation_id = LISTENING_CHANNELS
category_enc=[]
reply=[]
parent=[]
slackReply=""
slackParent=""

try:
    # Call the conversations.history method using the WebClient
    # The client passes the token you included in initialization
    result = client.conversations_history(
        channel=conversation_id
    )

    filename = "./data/questions.csv"
    with open(filename, 'w',encoding='UTF8', newline='') as f1:

        
        for messages in range(len(result["messages"])):
            slackMessage = result["messages"][messages]
            slackMessageTs = slackMessage["ts"]
            resultSlackReply = client.conversations_replies( channel = conversation_id, ts=slackMessageTs)

            for message in range(len(resultSlackReply["messages"])):
                slackMessageReply= resultSlackReply["messages"][message]
                slackReplyTs = slackMessageReply["ts"]            

                if slackMessageTs!= slackReplyTs :
                        slackReply=slackMessageReply["text"]
                        reply.append(slackReply)
                        parent.append(slackParent)
                    
                else :                   
                        slackParent=slackMessageReply["text"]
                        parent.append(slackParent)
                        reply.append("")


        
        df = pd.DataFrame(parent,columns = ['category'])
        df['question'] = reply
        df['question']= df['question'].replace('', np.nan)
        df = df.dropna(axis=0, subset=['question'])

        for enc in range(len(df.index)) :
                category_enc.append(enc)  
        
        df['category_enc'] = category_enc        

        df.to_csv(f1, header=True, index=False)     

            
except SlackApiError as e:
    print(f"Error: {e}")
  
    
  