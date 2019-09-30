from flask import Flask, render_template, request, make_response, send_from_directory, escape, redirect, url_for
import os
import random
import datetime

app = Flask(__name__)

def index() :
    return render_template(
        'index.html',
    )
