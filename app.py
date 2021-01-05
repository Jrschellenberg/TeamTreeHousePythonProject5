from flask import Flask, render_template, redirect, flash, request, url_for
from models import Journal
from helpers.jinja import JinjaHelpers


app = Flask(__name__)
app.secret_key = "my_not_so_safe_secret_key_since_this_is_development"


@app.before_request
def before_request():
    Journal.connect()


@app.after_request
def after_request(response):
    Journal.close()
    return response


@app.route('/', methods=['GET'])
def home():
    return redirect('/entries')


@app.route('/entries', methods=['GET'])
def index():
    journal_entries = Journal.get_all_records()
    return render_template('index.html', articles=journal_entries)


@app.route('/entries/new', methods=['POST'])
def create():
    journal_entry = request.form.to_dict(flat=True)
    entry_id, is_error = Journal.create_record(journal_entry)
    if is_error:
        flash('Error occured while Creating entry', 'error')
        return redirect('/')
    return redirect(f'/entries/{entry_id}')


@app.route('/entries/<int:journal_id>/edit', methods=['GET'])
def edit(journal_id):
    journal, is_error = Journal.get_record_by_id(journal_id)
    if is_error:
        flash('Journal Not Found!', 'error')
        return redirect('/')
    return render_template('edit.html', journal=journal)


@app.route('/entries/<int:journal_id>/edit', methods=['POST'])
def update(journal_id):
    if not request.form['_METHOD'] == 'PUT':
        flash('ERROR 405 METHOD NOT ALLOWED', 'error')
        return redirect(url_for('index'))
    updated_journal_entry = request.form.to_dict(flat=True)
    updated_journal_entry.pop('_METHOD', None)
    journal, is_error = Journal.update_record(journal_id, updated_journal_entry)
    if is_error:
        flash('Journal Not Found!', 'error')
    else:
        flash(f'Successfully Updated Journal {journal}', 'success')
    return redirect('/')


@app.route('/entries/new', methods=['GET'])
def new():
    return render_template('new.html')


@app.route('/entries/<int:journal_id>', methods=['GET'])
def details(journal_id):
    journal, is_error = Journal.get_record_by_id(journal_id)
    if is_error:
        flash('Journal Not Found!', 'error')
        return redirect('/')
    return render_template('detail.html', journal=journal)


@app.route('/entries/<int:journal_id>/delete', methods=['DELETE'])
def delete_entry(journal_id):
    print(f'Journal id {journal_id}')
    Journal.delete_record(journal_id)
    return redirect('/entries')


if __name__ == '__main__':
    helpers = JinjaHelpers(app)
    helpers.register()
    Journal.initialize()
    Journal.import_database_by_csv('storage/seed.csv')
    app.run(debug=True, port=5000, host="0.0.0.0")
