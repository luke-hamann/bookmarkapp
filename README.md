# Bookmark App

A web application for managing bookmarks.

Users can:

* View bookmarks
* Add bookmarks
* Edit bookmarks
* Delete bookmarks
* Login
* Logout

## Development Installation

1. Ensure [Python], pip, and (optionally) git are installed.
2. Download the repository.
    - `git clone https://github.com/luke-hamann/bookmarkapp.git`
    - Or download and extract the [ZIP]
3. Change into the repository root directory.
    - `cd bookmarkapp`
4. (Optional) Create and activate a Python [virtual environment].
5. Install the application in editable mode.
    - `pip install --editable .`
6. Create `config.toml` in the repository root directory.
7. Supply a [SECRET_KEY] in `config.toml` using the format in `example.config.toml`.
7. Run the application.
    - `flask --app bookmarkapp run`

[Python]: https://www.python.org/
[ZIP]: https://github.com/luke-hamann/bookmarkapp/archive/refs/heads/master.zip
[virtual environment]: https://docs.python.org/3/library/venv.html
[SECRET_KEY]: https://flask.palletsprojects.com/config/#SECRET_KEY
