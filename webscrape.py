from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/search_deal', methods=['POST'])
def get_input():
    origin = request.forms.get('origin')
    destination = request.forms.get('destination')
    print(origin)
