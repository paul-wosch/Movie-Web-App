"""app.py

Provide a Flask web application for managing users and their favorite movies.

This module defines routes to view users, add new users, view movies
for a specific user, add movies to a user's collection using the OMDB
API, and remove movies from a user's collection. Uses SQLAlchemy for
database interactions and DataManager for data operations.
"""
from flask import Flask, render_template, request, redirect, url_for, flash
from data_manager import DataManager
from models import db, Movie
from api import fetch_omdb_by_title
from config import DB_FILE_PATH, FLASK_SECRET_KEY, STATIC_PATH, TEMPLATES_PATH

FLASK_DEBUG_MODE = True

app = Flask(__name__, static_folder=STATIC_PATH, template_folder=TEMPLATES_PATH)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{str(DB_FILE_PATH)}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = FLASK_SECRET_KEY
db.init_app(app)
data_manager = DataManager()


@app.route('/')
def index():
    """Display a list of all users.

    Returns:
        Rendered HTML template 'index.html' with users context.
    """
    users = data_manager.get_users()
    return render_template('index.html', users=users)


@app.route('/users', methods=['POST'])
def create_user():
    """Create a new user with the name provided in the form.

    Returns:
        Redirect to the index page.
    """
    name = request.form.get("name")
    if name:
        data_manager.create_user(name)
    return redirect(url_for('index'))


@app.route('/users/<int:user_id>/movies', methods=['GET'])
def get_movies(user_id):
    """Display all movies for a specific user.

    Args:
        user_id (int): ID of the user whose movies are displayed.

    Returns:
        Rendered HTML template 'movies.html' with user_id and movies context.
    """
    movies = data_manager.get_movies(user_id)
    return render_template('movies.html', user_id=user_id, movies=movies)


@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie(user_id):
    """Add a movie to a user's collection using the title provided in the form.

    Queries the OMDB API to fetch movie metadata. If the movie does not
    exist in the database, it is created. Adds the movie to the user's list.

    Args:
        user_id (int): ID of the user to add the movie to.

    Returns:
        Redirect to the user's movies page.
    """
    title = request.form.get("title", "").strip()
    if not title:
        flash("Please provide a movie title.")
        return redirect(url_for('get_movies', user_id=user_id))
    try:
        meta = fetch_omdb_by_title(title)
    except Exception as e:
        flash(str(e))
        return redirect(url_for('get_movies', user_id=user_id))

    movie = (
        data_manager.get_movie_by_title_and_director(meta["name"], meta["director"], meta["year"])
        or data_manager.create_movie(meta["name"], meta["director"], meta["year"], meta["poster_url"])
    )
    data_manager.add_movie_to_user(user_id, movie)
    return redirect(url_for('get_movies', user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id, movie_id):
    """Remove a movie from a user's collection.

    Args:
        user_id (int): ID of the user whose movie is to be removed.
        movie_id (int): ID of the movie to remove.

    Returns:
        Redirect to the user's movies page.
    """
    data_manager.remove_movie_from_user(user_id, movie_id)
    return redirect(url_for('get_movies', user_id=user_id))


def main():
    """Initialize the database and start the Flask development server."""
    with app.app_context():
        db.create_all()
    app.run(debug=FLASK_DEBUG_MODE, host='0.0.0.0', port=5000)


if __name__ == '__main__':
    main()
