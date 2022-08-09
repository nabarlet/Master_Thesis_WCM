PLOTDIR=./plots
PYTHON=python3
TOP_CHARTS=top_chart.py
TOP_ERAS=top_eras.py

all: charts eras

charts:
	$(PYTHON) $(TOP_CHARTS)

eras:
	$(PYTHON) $(TOP_ERAS)

clean:
	$(RM) $(PLOTDIR)/*

.PHONY: charts eras clean
