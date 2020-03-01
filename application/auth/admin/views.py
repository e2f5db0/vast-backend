from application import app, db
from flask import Flask, session, make_response, flash, jsonify
from flask import render_template, request, redirect, url_for, send_file, abort
from application.lines.models import Line
from application.lines.models import Music
from application.auth.admin.forms import LineForm
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from io import BytesIO

from application import app
from application.auth.admin.forms import AdminLoginForm

from flask_sqlalchemy import SQLAlchemy
import bcrypt
from os import urandom

import os

admin_token = urandom(32)

authenticator = IAMAuthenticator(os.getenv('API_KEY'))
text_to_speech = TextToSpeechV1(
    authenticator=authenticator
)
text_to_speech.set_service_url(os.getenv('API_URL'))
text_to_speech.set_default_headers({'Access-Control-Allow-Origin': "*"})

@app.route('/auth/admin/', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'GET':
        return render_template('auth/admin/admin_login.html', form = AdminLoginForm())

    form = AdminLoginForm(request.form)

    username_checks = bcrypt.checkpw(form.username.data.encode('utf-8'),
                                     os.getenv('ADMIN_U').encode('utf-8'))
    password_checks = bcrypt.checkpw(form.password.data.encode('utf-8'),
                                     os.getenv('ADMIN_P').encode('utf-8'))

    if username_checks and password_checks:
        session['admin_token'] = admin_token
        return redirect(url_for('manage'))
    else:
        flash(f'Bad credentials.', 'danger')
        return redirect(url_for('admin_login'))

@app.route('/auth/admin/manage/', methods=['GET', 'POST'])
def manage():
    if request.method == 'GET':
        if session['admin_token'] and session['admin_token'] == admin_token:
            page = request.args.get('page', 1, type=int)
            lines = Line.query.order_by(Line.date_created.desc()).paginate(page=page, per_page=4)
            return render_template('/auth/admin/admin_manage.html', lines=lines, sort_by='date', form=LineForm())
        else:
            abort(403)
    
    form = LineForm(request.form)

    l = Line(form.filename.data,
                   form.duration.data,
                   form.text.data,
                   form.choice1.data,
                   form.choice2.data,
                   form.choice3.data)

    l_id = request.form.get('id')
    line = Line.query.filter_by(id=l_id).first()

    if session['admin_token'] and session['admin_token'] == admin_token and form.validate_on_submit():
        if l.filename != line.filename:
            line.filename = l.filename
        if l.duration != line.duration:
            line.duration = l.duration
        if l.text != line.text:
            line.text = l.text
        if l.choice1 != line.choice1:
            line.choice1 = l.choice1
        if l.choice2 != line.choice2:
            line.choice3 = l.choice3
        if l.choice3 != line.choice3:
            line.choice3 = l.choice3
        db.session.commit()
    else:
        flash(f'Something went wrong...', 'danger')
        return redirect(url_for('manage'))
    
    flash(f'Line updated.', 'success')
    return redirect(url_for('manage'))

@app.route('/auth/admin/upload/', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return render_template('auth/admin/admin_upload.html', form=LineForm())

    form = LineForm(request.form)

    # Create an audio file
    filename = str(form.filename.data) + '.wav'
    filepath = './audio/' + filename

    with open(filepath, 'wb') as audio_file:
        audio_file.write(
            text_to_speech.synthesize(
                form.text.data,
                voice='en-GB_KateV3Voice',
                accept='audio/wav'
            ).get_result().content)

    # Read the created audio file
    audio = open(filepath, 'rb').read()

    music = Music(name=filename, data=audio)

    l = Line(form.filename.data, form.duration.data, form.text.data, form.choice1.data, form.choice2.data, form.choice3.data)
    l.music = music

    if form.validate_on_submit():
        db.session().add(l)
        db.session().add(music)
        db.session().commit()
        flash(f'File uploaded.', 'success')
        return redirect(url_for('upload'))
    else:
        flash(f'Something went wrong.', 'danger')
        return render_template('auth/admin/admin_upload.html', form=form)

@app.route('/auth/admin/delete/<id>/')
def admin_delete_line(id):
    if session['admin_token'] and session['admin_token'] == admin_token:
        l = Line.query.get_or_404(id)
        m = Music.query.filter_by(line_id=l.id).first()
        db.session.delete(l)
        db.session.delete(m)
        db.session.commit()

    return redirect(url_for('manage'))

@app.route('/auth/admin/logout/')
def admin_logout():
    if session['admin_token']:
        session.pop('admin_token', None)
        return redirect(url_for('admin_login'))
    else:
        abort(403)

@app.route('/auth/admin/confirmation/<id>/')
def admin_confirmation(id):
    if session['admin_token'] and session['admin_token'] == admin_token:
        line = Line.query.get_or_404(id)
        return render_template('/auth/admin/admin_confirmation.html', line=line)
    else:
        abort(403)

@app.route('/auth/admin/edit/', methods=['POST'])
def admin_edit():
    edit_id = request.form.get('id')
    line = Line.query.filter_by(id=edit_id).first()

    edit_form = LineForm()
    edit_form.filename.data = line.filename
    edit_form.duration.data = line.duration
    edit_form.text.data = line.text
    edit_form.choice1.data = line.choice1
    edit_form.choice2.data = line.choice2
    edit_form.choice3.data = line.choice3

    if session['admin_token'] and session['admin_token'] == admin_token:
        return render_template('/auth/admin/admin_edit.html', form = edit_form,
                               default = line)
