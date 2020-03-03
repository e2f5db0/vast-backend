from application import app
from flask import Flask, jsonify, send_file, abort
from sqlalchemy import func
from application.lines.models import Line
from application.lines.models import Music
from io import BytesIO
import random

@app.route('/left-path/<id>/')
def left_path(id):
    name = 'left_path' + str(id)
    line = Line.query.filter_by(filename=name).first()
    if line:
        return jsonify(
            text = line.text,
            duration = line.duration,
            filename = line.filename,
            choice1 = line.choice1,
            choice2 = line.choice2,
            choice3 = line.choice3
        )
    else:
        abort(404)

@app.route('/center-path/<id>/')
def center_path(id):
    name = 'center_path' + str(id)
    line = Line.query.filter_by(filename=name).first()
    if line:
        return jsonify(
            text = line.text,
            duration = line.duration,
            filename = line.filename,
            choice1 = line.choice1,
            choice2 = line.choice2,
            choice3 = line.choice3
        )
    else:
        abort(404)

@app.route('/right-path/<id>/')
def right_path(id):
    name = 'right_path' + str(id)
    line = Line.query.filter_by(filename=name).first()
    if line:
        return jsonify(
            text = line.text,
            duration = line.duration,
            filename = line.filename,
            choice1 = line.choice1,
            choice2 = line.choice2,
            choice3 = line.choice3
        )
    else:
        abort(404)

@app.route('/prey-for-god/<id>')
def prey_for_god(id):
    name = 'prey' + str(id)
    wisdom = Music.query.filter(Music.name.contains(name)).first()
    if wisdom:
        return send_file(BytesIO(wisdom.data), attachment_filename=wisdom.name, as_attachment=True)
    else:
        abort(404)

@app.route('/lines/<name>/')
def get_line_file(name):
    music = Music.query.filter_by(name=name).first()
    if music:
        return send_file(BytesIO(music.data), attachment_filename=music.name, as_attachment=True)
    else:
        abort(404)

@app.route('/left-path/count/')
def get_count_left():
    count = Line.query.filter(Line.filename.contains('left_path')).count()
    return jsonify({'lines': count})

@app.route('/right-path/count/')
def get_count_right():
    count = Line.query.filter(Line.filename.contains('right_path')).count()
    return jsonify({'lines': count})

@app.route('/center-path/count/')
def get_count_center():
    count = Line.query.filter(Line.filename.contains('center_path')).count()
    return jsonify({'lines': count})
