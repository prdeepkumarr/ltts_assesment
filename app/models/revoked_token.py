from app import db

class RevokedToken(db.Model):

    __tablename__ = "revoked_tokens"

    tokenid = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(100), nullable=False)