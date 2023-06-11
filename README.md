👉 Set Up for Unix, MacOS

1.  Install modules via VENV

    $ virtualenv env
    $ source env/bin/activate
    $ pip3 install -r requirements.txt

2.  Set Up Flask Environment

    $ export FLASK_APP=run.py
    $ export FLASK_ENV=development

3.  Start the app

    $ flask run
    // OR
    $ flask run --cert=adhoc # For HTTPS server

At this point, the app runs at http://127.0.0.1:5000/.


👉 Set Up for Windows

1. Install modules via VENV (windows)

    $ virtualenv env
    $ .\env\Scripts\activate
    $ pip3 install -r requirements.txt

2.  Set Up Flask Environment

    $ # CMD 
    $ set FLASK_APP=run.py
    $ set FLASK_ENV=development
    $
    $ # Powershell
    $ $env:FLASK_APP = ".\run.py"
    $ $env:FLASK_ENV = "development"

3.  Start the app

    $ flask run
    // OR
    $ flask run --cert=adhoc # For HTTPS server
    At this point, the app runs at http://127.0.0.1:5000/.

