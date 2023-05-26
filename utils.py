# import sqlite3
import requests
# import os
# from gtts import gTTS
# from playsound import playsound
import time
import wget
import subprocess
# import pandas as pd

# src tu bot - vi tu user - en
# def transText(text_input, scr_input='bot'):
#     from googletrans import Translator
#     # define a translate object
#     translate = Translator()
#     # Translate some text
#     # scr_input = translate.detect(text_input)
#     if scr_input == "bot":
#         result = translate.translate(text_input, src='en', dest='vi')
#         result = result.text
#     elif scr_input == "user":
#         result = translate.translate(text_input, src='vi', dest='en')
#         result = result.text
#     else:
#         result = "We not support this language, please use English or Vietnamese!"
#     return result

# Write error to txt


def save_error(message, error_source):
    f = open("error_log.txt", "a")
    # writing in the file
    f.write(error_source)
    f.write(str(message))
    f.write('\n')
    # closing the file
    f.close()

# Text to Speech using FPT_AI api
def tts_fptAI(msg):
    while True:
        try:
            url = 'https://api.fpt.ai/hmi/tts/v5'
            headers = {
                'api-key': 'OaGgkRmCMzOoZbnwgX70IDWo77t0g5SW',
                'speed': '',
                'voice': 'banmai'
            }

            response = requests.request('POST', url, data=msg.encode('utf-8'), headers=headers)
            response = response.json()
            file = response['async']
        except:
            time.sleep(1)
            continue
        break
    while True:
        try:
            wget.download(file, out="data/audio")
        except:
            time.sleep(0.1)
            # print('Co loi. Thu lai', end='')
            continue
        break
    # print(resp)
    file_name = file.split('/')[-1]
    # playsound(file_name)
    return file_name

def play_mp3(path):
    subprocess.Popen(['mpg123', '-q', path]).wait()

# def event_response(tag):
#     con = sqlite3.connect("apps/db.sqlite3")
#     df = pd.read_sql_query("SELECT * from Events", con)
#     df = df.drop(['oauth_github'], axis=1)
#     if tag == "Golf_session_01":
#         res = ["Vâng, tuần này CLB có tổ chức môt buổi " + df.eventName.values[-1], "act01/Golf_session_01"]
#     elif tag == "Golf_session_02":
#         res = ["Buổi chơi golf sẽ diễn ra tại " + df.address.values[-1] + " vào lúc " + df.dateTime.values[-1], "act01/Golf_session_02"]
#     elif tag == "Golf_session_03":
#         res = ["Buổi chơi golf nhằm " + df.content.values[-1], "act01/Golf_session_03"]
#     else:
#         res = "None"

#     return res

if __name__ == "__main__":
    print("Test function")

