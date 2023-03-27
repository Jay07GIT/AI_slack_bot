# AI Slack bot

### Steps to setup env.
1. Install Conda: [miniconda](https://docs.conda.io/en/latest/miniconda.html) (download sh file and give command ```./<conda.sh file name>```) <br />
> Check the conda path in your local machine- ```User/<userName>/miniconda3/envs``` <br />
2. Install dependencies: <br />
```sh
cd <project folder>
```
```sh
conda env create -f environment.yml 
```
```sh
conda activate aislackbot 
```
3. Setup ```.env``` file with bot credentials.
```
# General Settings
DEBUG=False
PORT=5050

# Slack Credentials
SLACK_API_TOKEN=
SLACK_BOT_TOKEN=
SLACK_USER_TOKEN=
SLACK_SIGNING_SECRET=
TARGET_CHANNELS=
LISTENING_CHANNELS=
BOT_ID=
ADMIN_USERS='[""]'
```
run ``` ./train.sh ``` <br />

4. Ngrok setup
> this step help us to run the port in public fqdn which we can get event response from slack.
  1. Install ngrok.
```sh
brew install ngrok/ngrok/ngrok
```
  2. Follow the steps to setup ngrok : [ngrok](https://ngrok.com/download)
  3. Setup ngrok url to <b>5050</b>
5.  NGIX will be run in <b>5051</b>
6.  Configure slack/event url in [event-subscriptions](https://api.slack.com/apps/<appId>/event-subscriptions?)
> Should get success.

### Additional configurations
```sh
pip install xgboost==1.4.2
brew install libomp.
```
