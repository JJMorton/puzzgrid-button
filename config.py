# The maximum number of grids to find from puzzgrid.com
# Note that only the needed number of grids will be
# requested, so no harm in setting this high
GRID_SEARCH_SIZE = 50

# The minimum difficulty of grids to search for, from 1 to 5
MIN_DIFFICULTY = 0

# The minimum quality of grid to search for, from 1 to 5
MIN_QUALITY = 2.5

# File to store the list of completed grid IDs in
COMPLETED_GRIDS_FILE = "completed_grids.txt"

# The oldest puzzle to use
# Just here to prevent puzzles we've already completed
# appearing on the first run, shouldn't need to change this.
OLDEST_ID = 95546
