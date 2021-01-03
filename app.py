from flask import Flask, render_template, redirect
app = Flask(__name__)


@app.route('/index', methods=['GET'])
def index():
    return redirect('/')


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/detail', methods=['GET'])
def detail():
    return render_template('detail.html')


@app.route('/edit', methods=['GET'])
def edit():
    return render_template('edit.html')


@app.route('/new', methods=['GET'])
def new():
    return render_template('new.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0")
