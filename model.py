from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

##############################################################################
# Model definitions


class User(db.Model):
    """User login information."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s email=%s>" % (self.user_id, self.email)


class SavedPhoto(db.Model):
    """User's saved photos."""

    __tablename__ = "saved_photos"

    saved_photos_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'))
    photo_id = db.Column(db.String(200))

    img_src = db.Column(db.String(200), nullable=False)

    user = db.relationship("User",
                           backref=db.backref("saved_photos",
                                              order_by=saved_photos_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Photo photo_id=%s img_src=%s>" % (self.photo_id, self.img_src)


################################################################################
# Helper functions


def connect_to_db(app, db_uri=None):
    """Connect the database to Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri or 'postgresql:///pocketpassport'
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


def example_data():
    """Example data for testing"""
    ron = User(first_name='Ron',
               last_name='Weasley',
               email='rweasley@gmail.com',
               password='magic')
    harry = User(first_name='Harry',
                 last_name='Potter',
                 email='hpotter@gmail.com',
                 password='gryff11')

    db.session.add_all([ron, harry])
    db.session.commit()

if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
    