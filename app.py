from flask import Flask, render_template, request
from textblob import TextBlob, Word
import nltk
import textblob

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
nltk.download('words')
nltk.download('wordnet')
textblob.download_corpora

#Initialize the app
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/word_counter',methods = ['POST','GET'])
def word_counter():
    if request.method == 'GET':
        return render_template('wordcounter.html')

    if request.method == 'POST':
        text = request.form.get('Enter Text')
        if 'sub' in request.form:
            sent = len(nltk.sent_tokenize(text))
            words = len(nltk.word_tokenize(text))

            return render_template('wordcounter.html',sent_freq = f'No. of sentences:{sent}',word_freq=f'No. of words:{words}')  

@app.route('/language_trans_detect', methods = ['POST','GET'])
def lang():
    if request.method == 'GET':

        return render_template('lang.html')

    if request.method == 'POST':  

        texts = request.form.get('Enter the text')
        lang = request.form.get('Language')
        
        input = TextBlob(texts)
        output = input.translate(to = lang)
        detect = input.detect_language()

        return render_template('lang.html' , out_data = f'Translated Text:{output}', in_data = f'Your input text is in:{detect}')


@app.route('/worddict',methods=['POST','GET'])
def word_dict():
    if request.method == 'GET':
        return render_template('dict.html')

    if request.method == 'POST':
        words = request.form.get('Enter the word')
        defi = Word(words).definitions
        out = [i for i in defi]


        return render_template('dict.html', output = f'{out}')

@app.route('/spellcorr', methods= ['POST','GET'])
def spell_corr():
    if request.method == 'GET':
        return render_template('spell.html')

    if request.method == 'POST':
        txt = request.form.get('Enter text')
        text = TextBlob(txt).lower()
        if "spell" in request.form:
            cor_txt = text.correct()
        elif 'reset' in request.form:
            render_template('spell.html')

    return render_template('spell.html', inp = f'The original text: {txt}', output = f'The corrected text: {cor_txt}')

@app.route('/singplu',methods=['POST','GET'])
def sing_plu():
    if request.method == 'GET':
        return render_template('singplu.html')

    if request.method == 'POST':
        w = TextBlob(request.form.get('Enter text'))
        m = int(request.form.get('Enter which word'))
        n = m-1
        if 'singular' in request.form:
            out_word = w.words[n].singularize()
        elif 'plural' in request.form:
            out_word = w.words[n].pluralize()
    
    return render_template('singplu.html', output = f'{out_word}')
        


if __name__ == '__main__':
    app.run()