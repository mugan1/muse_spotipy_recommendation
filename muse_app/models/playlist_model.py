from muse_app import db

class Playlist(db.Model):
    __tablename__ = 'playlist'

    id = db.Column(db.Integer, primary_key=True)
    track = db.Column(db.String(64), nullable=False)
    artist = db.Column(db.String(64), nullable=False)
    released = db.Column(db.String(64), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __repr__(self):
        return f"Playlist {self.id}"

