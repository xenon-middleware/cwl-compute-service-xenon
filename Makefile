.PHONY: install serve

install:
	pip install -r requirements.txt

serve:
	python -m bottle app.app --bind localhost:3596 -s gevent
