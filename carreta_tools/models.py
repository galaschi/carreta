from carreta_tools import db


class Hero(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hero_id = db.Column(db.Integer, unique=True)
    steamdb_name = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(100))


class Position(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)


class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer)
    match_id = db.Column(db.Integer)
    radiant_win = db.Column(db.Boolean, nullable=False)
    game_mode = db.Column(db.Integer)
    lobby_type = db.Column(db.Integer)
    hero_id = db.Column(db.String(100), nullable=False)
    start_time = db.Column(db.Integer, nullable=False)
    party_size = db.Column(db.Integer)
    leaver_status = db.Column(db.Boolean, nullable=False)
    mmr = db.Column(db.Integer)
