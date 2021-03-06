import copy
from flask import Flask, render_template, redirect, flash, request, url_for
from helpers import JinjaHelpers
from models import Journal


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
    return render_template('index.html', entries=journal_entries)


@app.route('/entries/new', methods=['POST'])
def create():
    journal_entry = request.form.to_dict(flat=True)
    journal_entry_copy = copy.deepcopy(journal_entry)
    for key, val in journal_entry_copy.items():
        if not bool(val):
            journal_entry.pop(key, None)
    entry_id, is_error = Journal.create_record(journal_entry)
    if is_error:
        flash('Error occured while Creating entry', 'error')
        return redirect(url_for('index'))
    return redirect(url_for('details', journal_id=str(entry_id)))


@app.route('/entries/<int:journal_id>/edit', methods=['GET'])
def edit(journal_id):
    journal, is_error = Journal.get_record_by_id(journal_id)
    if is_error:
        flash('Journal Not Found!', 'error')
        return redirect(url_for('index'))
    return render_template('edit.html', entry=journal)


@app.route('/entries/<int:journal_id>/edit', methods=['POST'])
def update(journal_id):
    if not request.form['_METHOD'] == 'PUT':
        flash('ERROR 405 METHOD NOT ALLOWED', 'error')
        return redirect(url_for('index'))
    updated_journal_entry = request.form.to_dict(flat=True)
    updated_journal_entry.pop('_METHOD', None)
    err_msg, is_error = \
        Journal.update_record(journal_id, updated_journal_entry)
    if is_error:
        flash(f'Could not Update! {err_msg}', 'error')
    else:
        flash(f'Successfully Updated Journal {journal_id}', 'success')
    return redirect(url_for('index'))


@app.route('/entries/new', methods=['GET'])
def new():
    return render_template('new.html')


@app.route('/entries/<int:journal_id>', methods=['GET'])
def details(journal_id):
    journal, is_error = Journal.get_record_by_id(journal_id)
    if is_error:
        flash('Journal Not Found!', 'error')
        return redirect(url_for('index'))
    return render_template('detail.html', entry=journal)


@app.route('/entries/<int:journal_id>/delete', methods=['POST'])
def delete_entry(journal_id):
    if not request.form['_METHOD'] == 'DELETE':
        flash('ERROR 405 METHOD NOT ALLOWED', 'error')
        return redirect(url_for('index'))
    Journal.delete_record(journal_id)
    flash(f'Successfully deleted {journal_id}', 'success')
    return redirect(url_for('index'))


if __name__ == '__main__':
    helpers = JinjaHelpers(app)
    helpers.register()
    Journal.initialize()
    Journal.import_database_by_csv('storage/seed.csv')
    app.run(debug=True, port=5000, host="0.0.0.0")
