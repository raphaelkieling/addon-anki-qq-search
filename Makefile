buildui:
	pyuic5 web.ui -o web.py

release:
	zip -r ./qqsearch.ankiaddon *

test: testinstall
	anki
