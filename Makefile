FILENAME = onduty.5m.py*
PLUGINS_DIR = "$(HOME)/Library/Application Support/xbar/plugins"

default: install

install:
	cp $(FILENAME) $(PLUGINS_DIR)/
