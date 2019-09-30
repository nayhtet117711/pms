from flask import Flask, render_template, redirect, request, send_from_directory
import os
from route import index

app = Flask(__name__)

app.add_url_rule("/", "index", index, methods=["GET", "POST"])


if __name__ == "__main__":
   app.run(debug=True)