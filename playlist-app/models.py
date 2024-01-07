"""Models for Playlist app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Playlist(db.Model):
    """Playlist model."""

    __tablename__ = "playlists"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))

    # Define the relationship between Playlist and PlaylistSong
    songs = db.relationship('PlaylistSong', back_populates='playlist')


class Song(db.Model):
    """Song model."""

    __tablename__ = "songs"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    artist = db.Column(db.String(100), nullable=False)

    # Define the relationship between Song and PlaylistSong
    playlists = db.relationship('PlaylistSong', back_populates='song')


class PlaylistSong(db.Model):
    """Mapping of a playlist to a song."""

    __tablename__ = "playlists_songs"

    id = db.Column(db.Integer, primary_key=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlists.id'), nullable=False)
    song_id = db.Column(db.Integer, db.ForeignKey('songs.id'), nullable=False)

    # Define relationships with Playlist and Song
    playlist = db.relationship('Playlist', back_populates='songs')
    song = db.relationship('Song', back_populates='playlists')

# DO NOT MODIFY THIS FUNCTION
def connect_db(app):
    """Connect to the database."""
    db.app = app
    db.init_app(app)
