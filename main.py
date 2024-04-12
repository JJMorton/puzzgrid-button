from pathlib import Path
from typing import Optional
import webbrowser

import tkinter as tk
from PIL import ImageTk, Image

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

    weekly = api.get_weekly()
    if weekly and not weekly.id in IDs.ids:
        IDs.add(weekly.id)
        return weekly.id

    daily = api.get_daily()
    if daily and not daily.id in IDs.ids:
        IDs.add(daily.id)
        return daily.id

    all_grids = api.get_grids(
        min_difficulty=config.MIN_DIFFICULTY,
        min_quality=config.MIN_QUALITY,
        max_results=config.GRID_SEARCH_SIZE,
    )
    for grid in all_grids:
        if not grid.id in IDs.ids:
            IDs.add(grid.id)
            return grid.id

    return None


def open_next_grid():
    grid_id = get_next_grid_id()
    if not grid_id or grid_id < config.OLDEST_ID:
        print("Sorry, no new grids :(((")
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
