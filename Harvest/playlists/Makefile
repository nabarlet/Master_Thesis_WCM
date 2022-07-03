PLOTDIR=./plots
COUNT=1000
PROGRESS=./progress.txt
PLAYLIST_TYPES=PathPlaylist ZonePathPlaylist MovementPathPlaylist ZonePlaylist StrictPathPlaylist MovementPlaylist RandomPlaylist
PYTHON=python3
PYSCRIPT=playlist_generator.py

all: plots

plots:
	for ptype in $(PLAYLIST_TYPES); do\
		$(PYTHON) $(PYSCRIPT) $$ptype $(COUNT); \
	done 6> $(PROGRESS)

clean:
	$(RM) $(PLOTDIR)/*.png $(PROGRESS)

.PHONY: plots clean
