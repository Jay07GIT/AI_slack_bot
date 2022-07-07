FROM continuumio/miniconda:latest

WORKDIR /app

COPY environment.yml ./
COPY .env ./.env
COPY bot.py ./
COPY run.sh ./
COPY ./data ./data
COPY ./model ./model
COPY ./logs ./logs
COPY ./channels_info.json ./channels_info.json
COPY ./slack_message_helper.py ./

RUN ["chmod", "+x", "./run.sh"]

RUN conda env create -f environment.yml

SHELL ["conda", "run", "-n", "aislackbot", "/bin/bash", "-c"]

ENV PATH /opt/conda/envs/aislackbot/bin:$PATH

EXPOSE 5050

RUN source activate aislackbot

ENTRYPOINT ["python"]
CMD ["bot.py"]
