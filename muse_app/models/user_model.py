from muse_app import db

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    
    playlists = db.relationship("Playlist", backref="User", cascade='all, delete')
    recommends = db.relationship("Recommend", backref="User", cascade='all, delete')

    def __repr__(self):
        return f"User {self.id}"
