buildui:
	pyuic5 web.ui -o web.py

release:
	zip -r . ../myaddon.ankiaddon

test: testinstall
	anki
