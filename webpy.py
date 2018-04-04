from flask import Flask, render_template, request
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['DEBUG'] = True

@app.route('/', methods=['GET', 'POST'])
def subPerf():
    return render_template('venForm.html')

@app.route('/display', methods=['GET', 'POST'])
def display():
    return render_template('venDisplay.html', groupName=request.form['groupName'], performanceName=request.form['performanceName'], extraNotes=request.form['extraNotes'])

if __name__ == "__main__":
    app.run()