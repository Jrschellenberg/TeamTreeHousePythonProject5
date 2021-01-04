from flask import Flask, render_template, redirect, flash, request
from services import JournalService


app = Flask(__name__)
app.secret_key = "my_not_so_safe_secret_key_since_this_is_development"


@app.route('/', methods=['GET'])
def home():
    return redirect('/entries')


@app.route('/entries', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/entries/<journal_id>/delete', methods=['DELETE', 'GET'])
def delete_entry(journal_id):
    print(f'Journal id {journal_id}')
    JournalService.delete_record(journal_id)
    return redirect('/entries')


@app.route('/entries/new', methods=['POST'])
def create():
    journal_entry = request.form.to_dict(flat=True)
    entry_id, is_error = JournalService.create_record(journal_entry)
    if is_error:
        flash('Error occured while Creating entry', 'error');
        return redirect('/')
    return redirect(f'/entries/{entry_id}')


@app.route('/entries/<journal_id>', methods=['GET'])
def detail(journal_id):
    journal, is_error = JournalService.get_record_by_id(journal_id)
    if is_error:
        flash('Journal Not Found!', 'error')
        return redirect('/')
    return render_template('detail.html')


@app.route('/edit', methods=['GET'])
def edit():
    return render_template('edit.html')


@app.route('/new', methods=['GET'])
def new():
    return render_template('new.html')


if __name__ == '__main__':
    JournalService.import_database_by_csv('storage/seed.csv')
    app.run(debug=True, port=5000, host="0.0.0.0")
