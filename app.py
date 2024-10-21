from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run-scripts', methods=['POST'])
def run_scripts():
    # Run the scripts
    subprocess.run(['python3', 'check_and_trigger.py'])
    subprocess.run(['python3', 'maha.py'])
    
    # You can modify this to return real data or results from your scripts
    return render_template('index.html', message="Scripts have been run successfully!")

if __name__ == '__main__':
    app.run(debug=True)

