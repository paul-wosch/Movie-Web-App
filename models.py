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

    def __repr__(self):
        """Return a string representation of the Favorites association.

        Shows the linked user_id and movie_id for debugging and logging.
        """
        return f"<Favorites user_id={self.user_id} movie_id={self.movie_id}>"

    def __str__(self):
        """Return a human-readable description of the Favorites association."""
        return f"User {self.user_id} favorited Movie {self.movie_id}"


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

    def __repr__(self):
        """Return a string representation of the User instance.

        Includes the user's id and name for easier debugging and logging.
        """
        return f"<User id={self.id} name='{self.name}'>"

    def __str__(self):
        """Return a human-readable description of the User instance."""
        return f"User {self.name} (ID: {self.id})"


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

    def __repr__(self):
        """Return a string representation of the Movie instance.

        Includes the movie's id, name, and year for debugging and logging.
        """
        return f"<Movie id={self.id} name='{self.name}' year={self.year}>"

    def __str__(self):
        """Return a human-readable description of the Movie instance."""
        if self.year and self.director:
            return f"'{self.name}' ({self.year}), directed by {self.director}"
        if self.year:
            return f"'{self.name}' ({self.year})"
        return f"'{self.name}'"
