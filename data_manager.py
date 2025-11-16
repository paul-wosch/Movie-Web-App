"""data_manager.py

Module providing the DataManager class to handle CRUD operations
and queries for User and Movie models in a Flask-SQLAlchemy
application. This includes creating users and movies, managing
many-to-many relationships via the Favorites association table,
and fetching related objects with optional dynamic relationship
support.
"""
from models import db, User, Movie


class DataManager:
    """Encapsulate database operations for User and Movie models.

    Responsibilities:
    - Create, retrieve, and update User and Movie records.
    - Manage the many-to-many relationship between Users and Movies
      via the 'favorites' association table.
    - Provide query functions compatible with lazy='dynamic'
      relationships, returning either Query objects or lists as
      appropriate.

    Attributes:
        None (all methods operate on the database session and model classes)
    """
    def create_user(self, name):
        """Create a new user and commit to the database."""
        user = User(name=name)
        db.session.add(user)
        db.session.commit()
        return user

    def get_users(self):
        """Return a list of all users."""
        return User.query.all()

    def get_user(self, user_id):
        """Return a single user."""
        return User.query.get(user_id)

    def get_movies(self, user_id):
        """Return a list of movies for a given user.

        Uses .all() because User.movies is lazy='dynamic'.
        """
        user = User.query.get(user_id)
        return user.movies.all() if user else []

    def get_movie_by_title_and_director(self, name, director=None, year=None):
        """Return the first movie matching name,

        and optionally director/year."""
        q = Movie.query.filter(Movie.name == name)
        if director:
            q = q.filter(Movie.director == director)
        if year is not None:
            q = q.filter(Movie.year == year)
        return q.first()

    def create_movie(self, name, director=None, year=None, poster_url=None):
        """Create a new movie and commit to the database."""
        movie = Movie(name=name, director=director, year=year, poster_url=poster_url)
        db.session.add(movie)
        db.session.commit()
        return movie

    def add_movie_to_user(self, user_id, movie):
        """Add a movie to a user's favorites.

        Uses dynamic query to check for existing relationship.
        """
        user = User.query.get(user_id)
        if user and not user.movies.filter_by(id=movie.id).first():
            user.movies.append(movie)
            db.session.commit()

    def update_movie(self, movie_id, name=None, director=None, year=None, poster_url=None):
        """Update fields of a movie and commit changes."""
        movie = Movie.query.get(movie_id)
        if not movie:
            return None

        if name is not None:
            movie.name = name
        if director is not None:
            movie.director = director
        if year is not None:
            movie.year = year
        if poster_url is not None:
            movie.poster_url = poster_url

        db.session.commit()
        return movie

    def remove_movie_from_user(self, user_id, movie_id):
        """Remove a movie from a user's favorites.

        Uses dynamic query to check for existing relationship.
        """
        user = User.query.get(user_id)
        movie = Movie.query.get(movie_id)
        if user and movie and user.movies.filter_by(id=movie.id).first():
            user.movies.remove(movie)
            db.session.commit()
