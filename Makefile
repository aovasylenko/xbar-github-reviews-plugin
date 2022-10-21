FILENAME = onduty.5m.py
CONFIG = ${FILENAME}.vars.json
PLUGINS_DIR = "$(HOME)/Library/Application Support/xbar/plugins"
INSTALLED_CONFIG = ${PLUGINS_DIR}/${CONFIG}

default: install

${INSTALLED_CONFIG}: ${CONFIG}
	@ cp -av ${CONFIG} ${INSTALLED_CONFIG}

install: ${INSTALLED_CONFIG}
	@ cp -av ${FILENAME} ${PLUGINS_DIR}
