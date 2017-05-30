from flask import (Flask, render_template, redirect, flash, session, request)

from flask_debugtoolbar import DebugToolbarExtension

from jinja2 import StrictUndefined

from model import connect_to_db, db, User

from flickr_functions import (get_photos, get_url, get_location)

from saving_photos import (get_pic, save_pic, remove_pic, check_saved)

import os

import requests

google_maps_api_key = os.environ['GOOGLE_KEY']

from geocode_functions import reverse_geo_location

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    if session.get('user_id'):
        return redirect("/user/%s" % session['user_id'])

    return render_template("homepage.html")


@app.route('/register', methods=['GET'])
def register_form():
    """Show registration form."""

    return render_template("register-form.html")


@app.route('/register', methods=["POST"])
def process_registration():
    """Process registration for new users."""

    email = request.form["email"]
    password = request.form["password"]
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]

    new_user = User(email=email, first_name=first_name, last_name=last_name, password=password)

    db.session.add(new_user)
    db.session.commit()

    flash('Welcome to Pocket Passport!')
    flash("User %s added." % email)
    return redirect("/")


@app.route('/login', methods=['GET'])
def login_form():
    """Show form for user login."""

    return render_template("login-form.html")


@app.route('/login', methods=["POST"])
def process_login():
    """Processes login for users."""

    email = request.form["email"]
    password = request.form["password"]
    user = User.query.filter_by(email=email).first()

    if not user:
        flash('No email found, please try again.')
        return redirect("/login")

    if user.password != password:
        flash('Incorrect password')
        return redirect("/login")

    session['user_id'] = user.user_id

    return redirect("/user/%s" % (user.user_id))


@app.route('/user/<user_id>')
def user_profile(user_id):
    """Show user profile."""

    user = User.query.get(user_id)

    #gets users saved pics by ID
    users_saved_pics = get_pic(user_id)

    return render_template("user-profile.html",
                           user=user,
                           users_saved_pics=users_saved_pics)


@app.route('/search-results')
def search_city():
    """Return categories after location search."""

    search = request.args.get('location')
    name = search
    return render_template("categories.html",
                           name=name,
                           search=search
                           )


@app.route('/food')
def search_food():
    """Return photo results from location search + food"""
    search = request.args.get('locate')
    name = search
    # returns search location plus the tags
    image_urls = get_photos(search, "food, restaurants")

    return render_template("search-results.html",
                           name=name,
                           image_urls=image_urls,
                           search=search)


@app.route('/landmarks')
def search_landmarks():
    """Return photo results from location search + landmarks"""
    search = request.args.get('locate')
    name = search
    image_urls = get_photos(search, "landmarks")
    return render_template("search-results.html",
                           name=name,
                           image_urls=image_urls,
                           search=search)


@app.route('/fashion')
def search_fashion():
    """Return photo results from location search + fashion"""
    search = request.args.get('locate')
    name = search
    image_urls = get_photos(search, "style, fashion")
    return render_template("search-results.html",
                           name=name,
                           image_urls=image_urls,
                           search=search)


@app.route('/coffee')
def search_coffee():
    """Return photo results from location search + coffee"""
    search = request.args.get('locate')
    name = search
    image_urls = get_photos(search, "coffee, cafe")
    return render_template("search-results.html",
                           name=name,
                           image_urls=image_urls,
                           search=search)


@app.route('/hikes')
def search_hikes():
    """Return photo results from location search + hikes"""
    search = request.args.get('locate')
    name = search
    image_urls = get_photos(search, "hiking, trails")
    return render_template("search-results.html",
                           name=name,
                           image_urls=image_urls,
                           search=search)


@app.route('/bars')
def search_bars():
    """Return photo results from bar search + hikes"""
    search = request.args.get('locate')
    name = search
    image_urls = get_photos(search, "bars, clubs")
    return render_template("search-results.html",
                           name=name,
                           image_urls=image_urls,
                           search=search)


@app.route('/nightlife')
def search_nightlife():
    """Return photo results from bar search + hikes"""
    search = request.args.get('locate')
    name = search
    image_urls = get_photos(search, "nightlife")
    return render_template("search-results.html",
                           name=name,
                           image_urls=image_urls,
                           search=search)


@app.route('/tourist')
def search_tourist():
    """Return photo results from search + tourist attractions"""
    search = request.args.get('locate')
    name = search
    image_urls = get_photos(search, "tourist attractions")
    return render_template("search-results.html",
                           name=name,
                           image_urls=image_urls,
                           search=search)


@app.route('/shops')
def search_shops():
    """Return photo results from search + tourist attractions"""
    search = request.args.get('locate')
    name = search
    image_urls = get_photos(search, "shops")
    return render_template("search-results.html",
                           name=name,
                           image_urls=image_urls,
                           search=search)


def get_yelp_access_token():
    """Get yelp business api access token"""
    app_id = '1aZ_5OVCRb0P7v3unYNIqA'
    app_secret = 'gXJgDy4eUkJZB4MM3vBWX1w7SHaeRiHGNhcL3cIv48wE9AFG8eT4IYPAtMZ5vOJm'

    data = {'grant_type': 'client_credentials',
            'client_id': app_id,
            'client_secret': app_secret}

    token = requests.post('https://api.yelp.com/oauth2/token', data=data)

    access_token = token.json()['access_token']

    return access_token


@app.route('/photo-info/<int:photo_id>')
def get_photo_info(photo_id):
    """Returns photo and additional information page"""
    # check if photo is saved to the user's profile
    saved = check_saved(photo_id)
    # use flickr api getinfo to get url of photo
    img_src = get_url(photo_id)
    # use flickr api getlocation to get location data of photo
    location = get_location(photo_id)

    # get lat and lng from flickr location api call
    lat = location['lat']
    lng = location['lng']

    address = reverse_geo_location(lat, lng)
    access_token = get_yelp_access_token()
    # use yelp api to search business info from lat/lng data
    url = 'https://api.yelp.com/v3/businesses/search'
    headers = {'Authorization': 'bearer %s' % access_token}
    params = {'limit': 1, 'sort_by': 'distance', 'radius': 10000, 'location': address}

    resp = requests.get(url=url, params=params, headers=headers)
    # get result in json format
    result = resp.json()['businesses']

    if len(result) == 0:
        yelplink = "No yelp data available"
    else:
        yelplink = result[0]['url']
    yelprating = result[0]['rating']
    yelpname = result[0]['name']
    print "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    print result
    return render_template("photo-info.html",
                           photo_id=photo_id,
                           img_src=img_src,
                           saved=saved,
                           lat=lat,
                           lng=lng,
                           yelplink=yelplink,
                           yelprating=yelprating,
                           yelpname=yelpname,
                           address=address,
                           google_maps_api_key=google_maps_api_key
                           )


@app.route('/save-pic', methods=["POST"])
def save_to_db():
    """Saves photo to database."""

    img_src = request.form.get("src")
    photo_id = request.form.get("id")
    user_id = session['user_id']

    save_pic(img_src=img_src, photo_id=photo_id, user_id=int(user_id))

    return "OK"


@app.route('/remove-pic', methods=["POST"])
def remove_photo():
    """Removes photo from database."""

    photo_id = request.form.get("id")
    user_id = session['user_id']

    remove_pic(photo_id, int(user_id))

    return "OK"


@app.route('/logout')
def logout():
    """Remove user_id from session and redirect to the home page."""

    del session['user_id']
    flash('You have successfully logged out.')

    return redirect("/")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    app.debug = True

    connect_to_db(app)

    # DebugToolbarExtension(app)

    # DEBUG_TB_INTERCEPT_REDIRECTS = False

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    PORT = int(os.environ.get("PORT", 5000))
    app.run(port=PORT, host='0.0.0.0')
