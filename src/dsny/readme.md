
# How to build the site

## Manually

1) Run process.py
2) Run make_html.py
3) Move index.html to the root folder

## Command Line

Build:

	cd /path/to/this/repo
	cd src/dsny
	python process.py
	python make_html.py
	cp index.html ../../
	
Clean:

	cd /path/to/this/repo
	cd src/dsny
	rm -r html/ html_raw/ index.html

## Run the site

	cd /path/to/this/repo
	python -m SimpleHTTPServer

Then open a browser and go to http://localhost:8000/
