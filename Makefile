buildui:
	pyuic5 web.ui -o web.py

testinstall: build testclean
	cp -r build/dist21 ~/.local/share/Anki2/addons21/syllabus-test

test: testinstall
	anki
