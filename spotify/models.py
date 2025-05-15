from extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    spotify_id = db.Column(db.String, unique=True)
    display_name = db.Column(db.String)
    access_token = db.Column(db.String)
    refresh_token = db.Column(db.String)

    def __repr__(self):
        return f'<User {self.display_name}>'