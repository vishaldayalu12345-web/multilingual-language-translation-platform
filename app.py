from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():

    if request.method == 'POST':

        text = request.form['text']
        source_language = request.form['source_language']
        target_language = request.form['target_language']

        return render_template(
            'index.html',
            text=text,
            source_language=source_language,
            target_language=target_language
        )

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)