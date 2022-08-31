PLOTDIR=./plots
COUNT=10000
PROGRESS=./progress.txt
PLAYLIST_TYPES=PathPlaylist ZonePathPlaylist ZonePlaylist MovementPlaylist MovementPathPlaylist RandomPlaylist StrictPathPlaylist
PYTHON=python3
PYSCRIPT=playlist_generator.py
ERRORS=errors.out

all: plots

plots:
	for ptype in $(PLAYLIST_TYPES); do\
		$(PYTHON) $(PYSCRIPT) $$ptype $(COUNT) 2>>$(ERRORS); \
	done

clean:
	$(RM) $(PLOTDIR)/*.png $(PROGRESS) $(ERRORS)

.PHONY: plots clean
