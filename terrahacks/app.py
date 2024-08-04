# app.py
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from scraper import *
from Aichatbot import *

app = Flask(__name__,static_url_path='/static')
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')



@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/process-data', methods=['POST'])
def process_data():
    if request.method == 'POST':
        inData = request.form.get("in")

    x = get_results(inData)
    if not x  : 
        return render_template("query.html", FridgeModel = "MODEL NOT FOUND.", ProductDescription = 'NO AI ANALYSIS.')
    else : 
        y = (scrape_energystar_product(x))
        a, b = split_and_process_array(y)
        formatted_result = format_arrays(a, b)
        print(formatted_result)
        b = chat(inData)
        return render_template("query.html", FridgeModel = formatted_result, ProductDescription = b)
def execute_script(data):
    # Example script logic
    input_value = data.get('search-input')
    processed_value = f"Processed: {input_value} is a banana"
    return {"message": "Data processed successfully", "processed_data": processed_value}

if __name__ == '__main__':
    app.run(debug=True)
