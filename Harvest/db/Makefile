DBDIR=./data
DB=$(DBDIR)/WCM.sqlite3
PY=python3
CREATOR=./create.py
RM=rm -rfi

all: $(DB)

$(DB): $(CREATOR) 
	$(PY) $(CREATOR) $(DB)

clean:
	$(RM) $(DB)

.PHONY: clean
