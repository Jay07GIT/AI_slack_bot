AI Slack bot


Steps to setup env.
1. Install Conda:
https://docs.conda.io/en/latest/miniconda.html (download sh file and give command ./<conda.sh file name>)
Check the conda path in your local machine- User/<user name>/miniconda3/envs
2. Install dependencies:
 Cd <project folder>
conda env create -f environment.yml
conda activate aislackbot
3. Setup .env file with bot credentials.
     run ./train.sh
4. Install ngrok.
    brew install ngrok/ngrok/ngrok
    Follow the steps to setup ngrok : https://ngrok.com/download
5.  Setup ngrok url to 5050
6.  NGIX will be run in 5051
7.  Configure slack/event url in https://api.slack.com/apps/A02QU29M7LY/event-subscriptions?
Should get success.
8. pip install xgboost==1.4.2
9. brew install libomp.
