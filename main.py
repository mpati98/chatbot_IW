from flask import Flask, jsonify, render_template, request
from flask_restful import Resource, Api
import nltk
nltk.download('popular')
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np
# Load data
from keras.models import load_model
model = load_model('data/model/model_May26.h5')
import json
intents = json.loads(open('data/intents/intents_May_26_2023.json').read())
words = pickle.load(open('data/model/textsMay26.pkl','rb'))
classes = pickle.load(open('data/model/labelsMay26.pkl','rb'))

def transText(text_input, scr_input='user'):
    from googletrans import Translator
    # define a translate object
    translate = Translator()
    if scr_input == "bot":
        result = translate.translate(text_input, src='en', dest='vi')
        result = result.text
    elif scr_input == "user":
        result = translate.translate(text_input, src='vi', dest='en')
        result = result.text
    else:
        result = "We not support this language, please use English or Vietnamese!"
    return result

def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.6
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = i['responses']
            break
    return result, tag

def chatbot_response(msg):
    ints = predict_class(msg, model)
    print(ints)
    if ints:
        res, tag = getResponse(ints, intents)
    else:
        res = "Rất xin lỗi vì thông tin bạn cần không tồn tại trong hệ thống, chúng tôi sẽ kiểm tra và cập nhật trong thời gian tới. Bạn còn muốn biết thêm thông tin gì khác không?"
        tag = "Other"
    return res, tag


app = Flask(__name__)
api = Api(app)



@app.route("/")
def home():
    return render_template("index.html")

@app.route('/welcome', methods=["POST"])
def voice_welcome():
    resp = "Nước Ion Mũi Né xin kính chào quý khách, bạn đã biết đến nước Ion và những ích lợi tuyệt vời cho sức khoẻ mà nước Ion mang lại chưa?"
    output = {
            "res_text": resp,
            "res_audio": "IW_welcome"
        }
    return jsonify(output)


class Chatbot(Resource):

    def post(self):

        text_input = request.get_json().get("message")
        text_input = transText(text_input)
        try:
            if text_input.isnumeric():
                resp = ["Cảm ơn bạn đã tin tưởng sử dụng dịch vụ. Chúng tôi sẽ liên hệ lại ngay khi có thể. Chúc bạn một ngày mới vui vẻ và gặp nhiều may mắn nhé!", "a991cca9-a897-4a2a-a214-5109cf04c193"]
                tag = "IW_Thanks"
            else:
                resp, tag = chatbot_response(text_input)
        except:
            resp = ["Tín hiệu không ổn định, vui lòng lặp lại rõ hơn nhé", "fbad6e35-3933-4388-be7b-d6dda276e114"]
            tag = "Error"
        output = {
            "res_text": resp[0],
            "audio_token": resp[1],
            "res_audio": tag
        }
        return jsonify(output)

api.add_resource(Chatbot, '/response')

if __name__ == "__main__":
    app.run(debug=True)