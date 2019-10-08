from application import db

class Line(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)

    filename = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.String(50), nullable=False)
    text = db.Column(db.String(510), nullable=False)
    choice1 = db.Column(db.String(150), nullable=False)
    choice2 = db.Column(db.String(150), nullable=False)
    choice3 = db.Column(db.String(150), nullable=False)
    music = db.relationship('Music', backref='line', uselist=False)

    def __init__(self, filename, duration, text, choice1,
                 choice2, choice3):
        self.filename = filename
        self.duration = duration
        self.text = text
        self.choice1 = choice1
        self.choice2 = choice2
        self.choice3 = choice3

class Music(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    data = db.Column(db.LargeBinary, nullable=False)

    line_id = db.Column(db.Integer, db.ForeignKey('line.id'))

    def __init__(self, name, data):
        self.name = name
        self.data = data