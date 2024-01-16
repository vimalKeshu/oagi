import os  
import base64
import google.generativeai as genai

from flask import Flask, request, jsonify

GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')
prompt = """What is the probability of retrying below operation resolve the issue ? please answer in json.
Do not include any explanations, only provide a  RFC8259 compliant JSON response  following this format without deviation:
{"retry": probability in float}
Error:
"""

app = Flask(__name__)

@app.route("/")
def hello_oagi():
    return "Welcome to OAGI server!"

@app.route("/retry", methods=['POST'])
def retry():
    try:
        json_data = request.get_json()
        print(json_data)
        base64_error = json_data.get('error')
        error = base64.b64decode(base64_error).decode()
        print(error)
        query = prompt+error
        response = model.generate_content(query,generation_config=genai.types.GenerationConfig(temperature=0.0))
        print(response.text)
        return response.text
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)