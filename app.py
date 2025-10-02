# app.py
from flask import Flask, render_template, request, send_file
from parser import parse_kivano as parse_store
import pandas as pd
import os

app = Flask(__name__)
EXCEL_PATH = "static/results.xlsx"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form.get('query', '').strip()
        if not query:
            return render_template('index.html', error="Введите запрос!")

        products = parse_store(query)
        summary = f"Найдено {len(products)} товаров по запросу '{query}'."

        if products:
            df = pd.DataFrame(products)
            df.to_excel(EXCEL_PATH, index=False)

        return render_template('index.html', summary=summary, products=products[:5], query=query)

    return render_template('index.html')

@app.route('/download')
def download():
    if os.path.exists(EXCEL_PATH):
        return send_file(EXCEL_PATH, as_attachment=True)
    return "Файл не найден", 404

if __name__ == '__main__':
    app.run(debug=True)