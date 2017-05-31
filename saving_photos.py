# functions for users to save photos to users' profile to be used in server.py
from jinja2 import StrictUndefined

from flask import (Flask, session)

from model import SavedPhoto, db

app = Flask(__name__)

app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined


def get_pic(user_id):
    """Shows users saved photos"""

    # find all photos saved by the user id
    saved_pics = SavedPhoto.query.filter(SavedPhoto.user_id == user_id).all()

    users_saved_pics = []

    # add photo to user's list of saved pics including photo id, user id, and img src
    for saved_pic in saved_pics:
        users_saved_pics.append({'photo_id': saved_pic.photo_id,
                                 'img_src': saved_pic.img_src,
                                 'user_id': saved_pic.user_id
                                 })

    return users_saved_pics


def save_pic(img_src, photo_id, user_id):
    """Save photo to database."""

    # pic = SavedPhoto(user_id=user_id, photo_id=photo_id)
    print user_id
    #checks if photo is there, if not add to the database
    if not SavedPhoto.query.filter(SavedPhoto.photo_id == photo_id).all():
        # print "doesn't exist"
        new_pic = SavedPhoto(user_id=int(user_id), img_src=img_src, photo_id=photo_id)
        db.session.add(new_pic)
    new_pic = None
    # print new_pic

    # db.session.add(pic)
    db.session.commit()


def remove_pic(photo_id, user_id):
    """Remove photo from database."""

    pic = SavedPhoto.query.filter(SavedPhoto.photo_id == photo_id, SavedPhoto.user_id == user_id).first()
    db.session.delete(pic)
    db.session.commit()


def check_saved(photo_id):
    """Check if photo has been saved by current user."""

    saved = SavedPhoto.query.filter(SavedPhoto.user_id == int(session['user_id']), SavedPhoto.photo_id == str(photo_id)).first()

    return saved
