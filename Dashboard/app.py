from flask import Flask,render_template,request,jsonify
from textrank4zh import TextRank4Keyword, TextRank4Sentence

import json

app = Flask(__name__)
app.config["MYSTATIC"] = "static"
app.jinja_env.auto_reload = True
import re
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize, word_tokenize

def clean_citation(sentences):
    pattern = re.compile('\[\d+\]')
    pattern2 = re.compile("\[\d+.\d.\]")
    if pattern.findall(sentences):
        sentences = re.sub(pattern, "", sentences)
        print(1)
    if pattern2.findall(sentences):
        sentences = re.sub(pattern2, "", sentences)
    return sentences

### 去除换行
def clean_space(sentences):
    if "\n" in sentences:
        sentences = sentences.replace("\n", "")
        return sentences
    else:
        pass



## 断句
def cut_sentence(sentences):
    sen = sent_tokenize(sentences)
    return sen




@app.route('/')
def Home():
    return render_template('front_end.html')

@app.route('/summary/' , methods = ["GET","POST"])
def Summarize():
    results = {}
    tr4s = TextRank4Sentence()
    if request.method == 'GET':
        return render_template("summary.html")
    if request.method == "POST":
        data = json.loads(request.form.get('data'))
        print(data)
        content = data['text']
        print(content)
        param = data['parm']
        score = data['score']
        print(param)
        try:
            param = int(param)
        except ValueError:
            param = 1
        print(score)
        sens = ""
        score = 0
        print(content)
        content = clean_citation(content)
        tr4s.analyze(text=content, lower=True)
        numbers = len(content)
        print(numbers)
        for item in tr4s.get_key_sentences(num=param):
            sens += item.sentence
            score += item.weight
            print(item.index, item.weight, item.sentence)
        try:
            if sens[-1] not in [".", "!", "?", "。"]:
                sen = sens.split("." or "。")[:-1]
                sens = "".join(sen)
        except IndexError:
            pass
        results["result"] = sens
        results["score"] = score
        print(results["result"])
    return jsonify(results)
    # return json.dumps(results)



if __name__ == '__main__':
    app.run(debug="True")
