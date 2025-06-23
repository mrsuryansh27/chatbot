# api/wsgi.py
from app.main import app  # or wherever you instantiate FastAPI as `app`

# PythonAnywhere’s WSGI entrypoint expects a variable named `application`
application = app
