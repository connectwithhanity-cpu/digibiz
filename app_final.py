from flask import Flask
import app_header as site
import ui_final

ui_final.install(site)

# Literal Flask application for Vercel Python runtime detection.
app = Flask(__name__)
app.wsgi_app = site.app.wsgi_app
application = app
