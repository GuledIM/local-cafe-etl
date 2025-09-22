from flask import Flask, render_template, request, redirect, url_for, flash
from utils.etl import extract , transform, normalisation, load
from utils.db_utils import *
from dotenv import load_dotenv
import os



def flask_app(conn, cursor):
    app = Flask(__name__)
    
    load_dotenv(dotenv_path=r"C:\Users\Gen-UK-Student\Documents\Projects\local-cafe-etl\week-5\src\secrets\.env")
    app.secret_key = os.environ.get("MYSECRECTAPI")
    
    state = {}

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/extract", methods=["POST"])
    def run_extract():
        state["raw"] = extract()
        flash("Extraction complete!")
        return redirect(url_for("index"))

    @app.route("/transform", methods=["POST"])
    def run_transform():
        if "raw" not in state:
            flash("Please run extract first!")
            return redirect(url_for("index"))
        state["transformed"] = transform(state["raw"])
        flash("Transformation complete!")
        return redirect(url_for("index"))

    @app.route("/load", methods=["POST"])
    def run_load():
        if "transformed" not in state:
            flash("Please run transform first!")
            return redirect(url_for("index"))
        load(conn, cursor, state["transformed"])
        flash("Load step complete!")
        return redirect(url_for("index"))

    @app.route("/shutdown", methods=["POST"])
    def shutdown():
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            return "Server shutdown not available in this environment."
        func()
        return "Server shutting down..."

    app.run(debug=True, host='0.0.0.0', port=5902)
