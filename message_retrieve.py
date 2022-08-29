import logging
import os
import csv
from dotenv import load_dotenv
# Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
# WebClient instantiates a client that can call API methods
# When using Bolt, you can use either `app.client` or the `client` passed to listeners.
load_dotenv()
SLACK_USER_TOKEN = os.getenv('SLACK_USER_TOKEN')
LISTENING_CHANNELS = os.getenv('LISTENING_CHANNELS')

print(SLACK_USER_TOKEN)
client = WebClient(token=SLACK_USER_TOKEN)
logger = logging.getLogger(__name__)
# ID of channel that the message exists in

message = []
conversation_id = LISTENING_CHANNELS
fields = ['Messages'] 

try:
    # Call the conversations.history method using the WebClient
    # The client passes the token you included in initialization
    result = client.conversations_history(
        channel=conversation_id
    )

    filename = "./data/answers.csv"
    with open(filename, 'w',encoding='UTF8', newline='') as f1:
                # creating a csv writer object
        csvwriter = csv.writer(f1, delimiter='\t')
                # writing the fields
        csvwriter.writerow(fields)
        for message in range(len(result["messages"])):
            slackMessage = result["messages"][message]
                        # Print message text
            csvwriter.writerow(slackMessage["text"])
            
except SlackApiError as e:
    print(f"Error: {e}")
    
# field names 
    
# data rows of csv file 

    
# name of csv file 
  