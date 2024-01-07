from flask import Flask, redirect, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Playlist, Song, PlaylistSong
from forms import NewSongForPlaylistForm, SongForm, PlaylistForm

app = Flask(__name__)
# adding personal db credential
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost/playlist-app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = "I'LL NEVER TELL!!"

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
#
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.route("/")
def root():
    """Homepage: redirect to /playlists."""

    return redirect("/playlists")


##############################################################################
# Playlist routes


@app.route("/playlists")
def show_all_playlists():
    """Return a list of playlists."""

    playlists = Playlist.query.all()
    return render_template("/playlists.html", playlists=playlists)


@app.route("/playlists/<int:playlist_id>")
def show_playlist(playlist_id):
    """Show detail on specific playlist."""

    playlist = Playlist.query.get_or_404(playlist_id)
    return render_template("playlist.html", playlist=playlist)


@app.route("/playlists/add", methods=["GET", "POST"])
def add_playlist():
    """Handle add-playlist form:

    - if form not filled out or invalid: show form
    - if valid: add playlist to SQLA and redirect to list-of-playlists
    """

    form = PlaylistForm()

    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data

        # Create a new playlist with the form data
        playlist = Playlist(name=name, description=description)

        db.session.add(playlist)
        db.session.commit()
        flash("Playlist created successfully!", "success")
        return redirect("/playlists")

    return render_template("/new_playlist.html", form=form)



##############################################################################
# Song routes


@app.route("/songs")
def show_all_songs():
    """Show list of songs."""

    songs = Song.query.all()
    return render_template("songs.html", songs=songs)


@app.route("/songs/<int:song_id>")
def show_song(song_id):
    """Show detail on specific song."""

    song = Song.query.get_or_404(song_id)
    return render_template("song.html", song=song)


@app.route("/songs/add", methods=["GET", "POST"])
def add_song():
    """Handle add-song form:

    - if form not filled out or invalid: show form
    - if valid: add song to SQLA and redirect to list-of-songs
    """

    form = SongForm()

    if form.validate_on_submit():
        title = form.title.data
        artist = form.artist.data

        # Create a new song with the form data
        song = Song(title=title, artist=artist)

        db.session.add(song)
        db.session.commit()

        return redirect("/songs")

    return render_template("new_song.html", form=form)


@app.route("/playlists/<int:playlist_id>/add-song", methods=["GET", "POST"])
def add_song_to_playlist(playlist_id):
    """Add a song to a playlist and redirect to the playlist details."""

    playlist = Playlist.query.get_or_404(playlist_id)
    form = NewSongForPlaylistForm()

    # Get the songs that are already on this playlist
    curr_on_playlist = [song.id for song in playlist.songs]

    # Restrict form choices to songs not already on this playlist
    form.song.choices = [(song.id, song.title) for song in Song.query.filter(Song.id.notin_(curr_on_playlist)).all()]

    if form.validate_on_submit():
        # Get the selected song ID from the form
        selected_song_id = form.song.data
        selected_song = Song.query.get(selected_song_id)

        if selected_song:
            # Add the selected song to the playlist
            playlist_song = PlaylistSong(playlist_id=playlist.id, song_id=selected_song.id)

            db.session.add(playlist_song)
            db.session.commit()

        return redirect(f"/playlists/{playlist_id}")

    return render_template("add_song_to_playlist.html",
                           playlist=playlist,
                           form=form)
