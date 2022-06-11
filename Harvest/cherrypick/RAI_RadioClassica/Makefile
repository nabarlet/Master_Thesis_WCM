PYTHON=python3
PROGRAM=main.py
TESTDIR=test
TEST_PARSER=parser_tester.py
TEST_LEXER=lexer_tester.py
TEST_SUBDIV=subdivider_tester.py
# TEST_ARG is empty on purpose
TEST_ARG=
REF_TEXT=reference_text.txt
REF_PRINTER=print_text.py
CD=cd

all:
	$(PYTHON) $(PROGRAM)

$(REF_TEXT):
	$(PYTHON) $(REF_PRINTER) > $@

parser_test:
	$(CD) $(TESTDIR) && $(PYTHON) $(TEST_PARSER) $(TEST_ARG)

lexer_test:
	$(CD) $(TESTDIR) && $(PYTHON) $(TEST_LEXER) $(TEST_ARG)

subdivider_test:
	$(CD) $(TESTDIR) && $(PYTHON) $(TEST_SUBDIV) $(TEST_ARG)

clean:
	$(RM) $(REF_TEXT)

.PHONY: all clean reference_text.txt parser_test lexer_test subdivider_test
