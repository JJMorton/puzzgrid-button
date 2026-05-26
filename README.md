A button to open recent unplayed grids from [puzzgrid.com](https://puzzgrid.com/).

---

Check `pyproject.toml` for the requirements of this project.
You will additionally need tkinter installed, check this by running
```
python3 -m tkinter
```
and ensuring that a window spawns.

To run this project, use your favourite python project/package manager.
`pip` can do this in an existing python environment with (assuming your working directory is this project's root):
```
python3 -m pip install .
```
and the project can be run with
```
python3 main.py
```
Alternatively, [uv](https://docs.astral.sh/uv/) can initialise a new python environment and run the project with
```
uv run main.py
```

---

Behaviour can be changed in `config.py`, where the following variables should be set:
 - `GRID_SEARCH_SIZE`: maximum number of grids to look through, to find one that is unplayed
 - `MIN_DIFFICULTY`: minimum difficulty rating to find, 0.0–5.0, where 0.0 yields every grid
 - `MIN_QUALITY`: minimum quality to search for, 0.0–5.0, where 0.0 yields every grid
 - `COMPLETED_GRIDS_FILE`: path to file where the IDs of visited grids are stored
 - `IGNORE_LADDERS`: do not open ladder puzzles
 - `BANNED_TAGS`: do not open puzzles with any of these tags

For example, to ban only slow grids, set `BANNED_TAGS = ["slow"]`.

Alternatively, learn to live without constant stimulation and just play them – a superior slow grid enjoyer.

---

I was told that I cannot finish my PhD without adding a `README` to this button's project, so here it is.
If puzzgrid changes their API, it'll be up to you to fix this script.
I'm sure you can manage `:)`
