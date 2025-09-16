from flask import Flask, render_template
import os

# Get the absolute path to the directory containing this script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Set the template folder to be relative to the script's directory
app = Flask(__name__, template_folder=os.path.join(script_dir, 'templates'))

@app.route('/')
def index():
    return render_template('introduction.html')

@app.route('/<page_name>.html')
def serve_page(page_name):
    return render_template(f'{page_name}.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


