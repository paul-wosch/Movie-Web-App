"""Database models for the movie application using Flask-SQLAlchemy.

This module defines the main database entities:
- User: represents an application user.
- Movie: represents a movie in the database.
- Favorites: association table for many-to-many relationship
  between users and movies.
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Favorites(db.Model):
    """Association table for many-to-many relationship between User and Movie.

    Attributes:
        user_id (int): Foreign key referencing User.id.
        movie_id (int): Foreign key referencing Movie.id.
    """
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        primary_key=True,
        doc="Foreign key referencing User.id"
    )
    movie_id = db.Column(
        db.Integer,
        db.ForeignKey('movie.id'),
        primary_key=True,
        doc="Foreign key referencing Movie.id"
    )


class User(db.Model):
    """Represents a user of the application.

    Attributes:
        id (int): Primary key for the user.
        name (str): Name of the user (max 100 characters, not nullable).
        movies (list of Movie): Movies favorited by the user.

    Relationships:
        movies: many-to-many relationship with Movie via Favorites table.
    """
    id = db.Column(
        db.Integer,
        primary_key=True,
        doc="Primary key for the user"
    )
    name = db.Column(
        db.String(100),
        nullable=False,
        doc="Name of the user (max 100 characters, not nullable)"
    )
    movies = db.relationship(
        'Movie',
        secondary='favorites',
        back_populates='users',
        lazy='dynamic',
        doc=(
            "Many-to-many relationship with Movie. "
            "Uses the 'favorites' association table. "
            "Back-populates 'users' on Movie model."
        )
    )


class Movie(db.Model):
    """Represents a movie in the database.

    Attributes:
        id (int): Primary key for the movie.
        name (str): Name of the movie (max 200 characters, not nullable).
        director (str): Director of the movie (max 100 characters).
        year (int): Release year of the movie.
        poster_url (str): URL of the movie poster image (max 200 characters).
        users (list of User): Users who have favorited this movie.

    Relationships:
        users: many-to-many relationship with User via Favorites table.
    """
    id = db.Column(
        db.Integer,
        primary_key=True,
        doc="Primary key for the movie"
    )
    name = db.Column(
        db.String(200),
        nullable=False,
        doc="Name of the movie (max 200 characters, not nullable)"
    )
    director = db.Column(
        db.String(100),
        doc="Director of the movie (max 100 characters)"
    )
    year = db.Column(
        db.Integer,
        doc="Release year of the movie"
    )
    poster_url = db.Column(
        db.String(200),
        doc="URL of the movie poster image (max 200 characters)"
    )
    users = db.relationship(
        'User',
        secondary='favorites',
        back_populates='movies',
        lazy='dynamic',
        doc=(
            "Many-to-many relationship with User. "
            "Uses the 'favorites' association table. "
            "Back-populates 'movies' on User model."
        )
    )
