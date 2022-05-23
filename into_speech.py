from flask import Flask
from flask_restful import Api, Resource, reqparse
from rutermextract import TermExtractor
import speech_recognition as sr
import soundfile
import librosa
import os
import time

app = Flask(__name__)
api = Api()
directoryName = "telegram_data"
problems = {}


def translate(problem_id, user_id):
    filePath = f'{directoryName}/{user_id}'
    data, samplerate = librosa.load(f'{filePath}/{problem_id}.ogg', sr=None)
    soundfile.write(f'{filePath}/new_voice.wav', data, samplerate, subtype='PCM_16')
    r = sr.Recognizer()
    with sr.AudioFile(f'{filePath}/new_voice.wav') as source:
        file = r.record(source)
    line = r.recognize_google(file, language='ru-RU')
    os.remove(f'{filePath}/new_voice.wav')
    return line


def keyword(question):
    kw = []
    term_extractor = TermExtractor()
    for term in term_extractor(question):
        kw.append(term.normalized)
    return kw


class Main(Resource):
    def get(self, problem_id, user_id):
        start_time = time.process_time()
        dataList = []
        dataText = str(translate(str(problem_id), str(user_id)))
        dataList.append({'text': dataText})
        dataList.append({'keyword': keyword(dataText)})
        problems[problem_id] = dataList
        print(str(time.process_time() - start_time) + " секунд")
        if problem_id == 0:
            return problems
        else:
            return problems[problem_id]

    def post(self, problem_id):
        return problems


api.add_resource(Main, "/api/translate_q/<int:user_id>/<int:problem_id>")
api.init_app(app)

app.run(debug=True, port=3001, host="127.0.0.1")
