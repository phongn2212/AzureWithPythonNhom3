import speech_recognition as sr
from flask import Flask, redirect, render_template, request, flash
import os
import io

app = Flask(__name__)
# app.config['SECRET_KEY'] = '21f6c92c5fa5cecb12e0d62498e35cac2c30414f0a8d78081af34a78a649'

path_file_txt = 'text.txt'
path_file_wav = 'recorded.wav'


def record():
    text = ""
    print("Method recognizing start .... ")
    r = sr.Recognizer()

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Please say something")
        # flash('Please say something')
        audio = r.listen(source, phrase_time_limit=100)
        print("Recognizing Now .... ")
        # recognize speech using google

        try:
            text = r.recognize_google(audio, language="vi-VN")
            print(text)
            # return text
            print("Audio Recorded Successfully \n ")
        except Exception as e:
            print("Error :  " + str(e))
            return "Try again..."

        # write audio
        with open("recorded.wav", "wb") as f:
            f.write(audio.get_wav_data())
        if os.path.exists(path_file_txt):
            os.remove(path_file_txt)
        with io.open(path_file_txt, "w", encoding="utf-8") as f:
            f.write(text)
    return text


@app.route("/", methods=["GET"])
def root():
    return render_template('index.html')


@app.route("/record_wav", methods=["GET", "POST"])
def record_wav():
    transcript = ""
    if request.method == "POST":
        transcript = record()
    return render_template('index.html', transcript=transcript)


@app.route("/file", methods=["GET", "POST"])
def read_file():
    check_file = request.files.getlist(key="file")
    print(len(check_file))
    if len(check_file) == 0:
        return render_template('index.html', transcript="No input file...")
    file = request.files["file"]
    if file.filename == "":
        return redirect(request.url)

    if file:
        recognizer = sr.Recognizer()
        audioFile = sr.AudioFile(file)
        with audioFile as source:
            data = recognizer.record(source)
        transcript = recognizer.recognize_google(
            data, language="vi-VN")
        print(transcript)
    return render_template('index.html', transcript=transcript)


if __name__ == "__main__":
    # main()
    # read_file_wav()
    app.run(debug=True)
