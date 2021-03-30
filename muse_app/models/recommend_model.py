from muse_app import db

class Recommend(db.Model):
    __tablename__ = 'recommend'

    id = db.Column(db.Integer, primary_key=True)
    track = db.Column(db.String(128), nullable=False)
    artist = db.Column(db.String(128), nullable=False)
    released = db.Column(db.String(128), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __repr__(self):
        return f"Recommend {self.id}"
