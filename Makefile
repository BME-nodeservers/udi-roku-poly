udi-roku-poly.zip: server.json
	cp README.md ../docs/udi-roku-poly.md
	zip -r ../udi-roku-poly.zip LICENSE POLYGLOT_CONFIG.md \
		README.md  roku.py install.sh nodes profile write_profile.py \
		requirements.txt server.json
