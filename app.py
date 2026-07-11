from flask import Flask, render_template, request, redirect
from deep_translator import GoogleTranslator
import mysql.connector

app = Flask(__name__)

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="tiger",
    database="translator_db"
)

cursor = connection.cursor()


@app.route('/', methods=['GET', 'POST'])
def home():

    language_codes = {
        "English": "en",
        "Kannada": "kn",
        "Telugu": "te",
        "Marathi": "mr",
        "Hindi": "hi",
        "Punjabi": "pa"
    }

    # Default values
    text = ""
    translated_text = ""
    source_language = "English"
    target_language = "Hindi"

    if request.method == 'POST':

        text = request.form['text']
        source_language = request.form['source_language']
        target_language = request.form['target_language']

        # Create translator
        translator = GoogleTranslator(
            source=language_codes[source_language],
            target=language_codes[target_language]
        )

        # Translate
        translated_text = translator.translate(text)

        # Save into MySQL
        query = """
        INSERT INTO translations
        (input_text, source_language, target_language, translated_text)
        VALUES (%s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (text, source_language, target_language, translated_text)
        )

        connection.commit()

    # Read all translations from MySQL
    cursor.execute("SELECT * FROM translations")
    history = cursor.fetchall()

    return render_template(
        "index.html",
        text=text,
        translated_text=translated_text,
        source_language=source_language,
        target_language=target_language,
        history=history
    )


@app.route('/delete/<int:id>')
def delete(id):

    query = "DELETE FROM translations WHERE id = %s"

    cursor.execute(query, (id,))

    connection.commit()

    return redirect('/')

@app.route('/clear')
def clear():

    cursor.execute("DELETE FROM translations")

    connection.commit()

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)