VIRTUALENV = $(shell which virtualenv)

ifeq ($(strip $(VIRTUALENV)),)
  VIRTUALENV = /usr/local/python/bin/virtualenv
endif


install: venv
	. venv/bin/activate; pip install -r requirements.txt \
		--download-cache /tmp/pipcache
	. venv/bin/activate; python install.py
	. venv/bin/activate; python setup.py install

develop: venv
	. venv/bin/activate; pip install -r requirements.txt \
		--download-cache /tmp/pipcache
	. venv/bin/activate; pip install -r tests/requirements.txt
	. venv/bin/activate; python install.py
	. venv/bin/activate; python setup.py develop

venv:
	$(VIRTUALENV) venv

serve: venv
	. venv/bin/activate; python rapid_response_kit/app.py

debug: venv
	. venv/bin/activate; python rapid_response_kit/app.py --debug

test: venv
	. venv/bin/activate; nosetests tests

coverage: venv
	. venv/bin/activate; nosetests --with-coverage --cover-package=rapid_response_kit

htmlcov: venv
	. venv/bin/activate; nosetests --with-coverage --cover-html --cover-package=rapid_response_kit
	open cover/index.html


flake: venv
	. venv/bin/activate; flake8 --ignore=F401 rapid_response_kit

clean:
	rm -rf *.pyc
	rm -rf cover/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf build/

uninstall: clean
	rm -rf venv
