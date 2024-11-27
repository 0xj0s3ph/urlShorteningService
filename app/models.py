from . import db
from datetime import datetime

class URL(db.Model):
    __tablename__ = 'urls'

    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.Text, nullable=False)
    short_code = db.Column(db.String(10), unique=True, nullable=False)
    # rather than storing shortened_url, I can just store a short code, then conbine donamin name with the short code
    accessed_times = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Set when row is created
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Updated when row changes

    def __repr__(self):
        return f'<URL {self.short_code}>'

    def to_dict(self):
        return {
            'id': self.id,
            'original_url': self.original_url,
            'accessed_times': self.accessed_times,
            'short_code': self.short_code,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }
