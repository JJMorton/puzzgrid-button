import tkinter as tk
import webbrowser
from pathlib import Path
from typing import Optional

from PIL import Image, ImageTk

import api
import config


class SavedIDs:

    file: Path
    ids: set[int]

    def __init__(self, file: Path) -> None:
        self.file = file
        if not file.exists():
            with open(file, 'w') as f: pass
        with open(file, 'r') as f:
            self.ids = { int(l.strip()) for l in f }

    def add(self, id: int):
        self.ids.add(id)
        with open(self.file, 'a') as f:
            f.write(str(id) + '\n')

    def latest(self) -> int:
        return max(self.ids)


def get_next_grid_id() -> Optional[int]:

    IDs = SavedIDs(Path(config.COMPLETED_GRIDS_FILE))

    def should_open(grid: api.GridModel | api.SpecialGridModel):
        return not (
            # Any of these conditions mean we don't want to open the grid
            (grid.id in IDs.ids)
            or (grid.is_ladder and config.IGNORE_LADDERS)
            or (
                isinstance(grid, api.GridModel)
                and any(tag in config.BANNED_TAGS for tag in grid.tags)
            )
        )

    special = api.get_special()
    for grid in special:
        if should_open(grid):
            IDs.add(grid.id)
            return grid.id

    all_grids = api.get_grids(
        min_difficulty=config.MIN_DIFFICULTY,
        min_quality=config.MIN_QUALITY,
        max_results=config.GRID_SEARCH_SIZE,
    )
    for grid in all_grids:
        if should_open(grid):
            IDs.add(grid.id)
            return grid.id

    return None


def open_next_grid():
    grid_id = get_next_grid_id()
    if not grid_id:
        print("Sorry, no new grids :(((")
        return
    print(f"Opening grid {grid_id}...")
    webbrowser.open(f"https://puzzgrid.com/grid/{grid_id}")


if __name__ == "__main__":

    # create a tkinter window
    root = tk.Tk()
    root.geometry('120x120')
    root.title('')

    # Create buttons
    image = ImageTk.PhotoImage(Image.open("button_image.png"))  # PIL solution
    btn1 = tk.Button(root, image=image, bd='5', cursor='shuttle', command=open_next_grid)
    btn1.pack(side = 'bottom')

    # keep tkinter window on top of other windows
    root.wm_attributes("-topmost", 1)

    root.mainloop()
