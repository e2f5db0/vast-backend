from application import app
from flask import Flask, jsonify, send_file
from application.lines.models import Line
from application.lines.models import Music
from io import BytesIO

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

@app.route('/lines/<name>/')
def get_line_file(name):
    music = Music.query.filter_by(name=name).first()
    if music:
        return send_file(BytesIO(music.data), attachment_filename=music.name, as_attachment=True)
    else:
        abort(404)
