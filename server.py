from flask import Flask, render_template, redirect, request, send_from_directory
import os
from route import index, loginAdmin, loginUser, signupUser, homeAdmin, homeUser, logout, addAdmin, homeAdminUsers, homeAdminTitles, userFirst, userSecond, userThird, userClose, selectTitle, searchThesis, homeAdminDelete, homeAdminUsersDelete, homeAdminTitleView, approvedThesisByAdmin, notiUser

app = Flask(__name__, static_folder='static', static_url_path='')

app.config.setdefault('MYSQL_HOST', 'localhost')
app.config.setdefault('MYSQL_USER', "root")
app.config.setdefault('MYSQL_PASSWORD', "root")
app.config.setdefault('MYSQL_DB', "pmsdb")
app.config.setdefault('MYSQL_PORT', 3306)
app.config.setdefault('MYSQL_UNIX_SOCKET', None)
app.config.setdefault('MYSQL_CONNECT_TIMEOUT', 10)
app.config.setdefault('MYSQL_READ_DEFAULT_FILE', None)
app.config.setdefault('MYSQL_USE_UNICODE', True)
app.config.setdefault('MYSQL_CHARSET', 'utf8')
app.config.setdefault('MYSQL_SQL_MODE', None)
app.config.setdefault('MYSQL_CURSORCLASS', None)

app.add_url_rule("/", "index", index, methods=["GET", "POST"])

app.add_url_rule("/loginAdmin", "loginAdmin", loginAdmin, methods=["GET", "POST"])

app.add_url_rule("/loginUser", "loginUser", loginUser, methods=["GET", "POST"])

app.add_url_rule("/logout", "logout", logout, methods=["GET", "POST"])

app.add_url_rule("/signupUser", "signupUser", signupUser, methods=["GET", "POST"])

app.add_url_rule("/homeAdmin", "homeAdmin", homeAdmin, methods=["GET", "POST"])

app.add_url_rule("/homeAdminDelete/<email>", "homeAdminDelete", homeAdminDelete, methods=["GET", "POST"])

app.add_url_rule("/homeUser", "homeUser", homeUser, methods=["GET", "POST"])

app.add_url_rule("/noti", "noti", notiUser, methods=["GET", "POST"])

app.add_url_rule("/homeAdminUsers", "homeAdminUsers", homeAdminUsers, methods=["GET", "POST"])

app.add_url_rule("/homeAdminUsersDelete/<email>", "homeAdminUsersDelete", homeAdminUsersDelete, methods=["GET", "POST"])

app.add_url_rule("/homeAdminTitles", "homeAdminTitles", homeAdminTitles, methods=["GET", "POST"])

app.add_url_rule("/homeAdminTitleView/<email>/<title>", "homeAdminTitleView", homeAdminTitleView, methods=["GET", "POST"])

app.add_url_rule("/addAdmin", "addAdmin", addAdmin, methods=["GET", "POST"])

app.add_url_rule("/userFirst", "userFirst", userFirst, methods=["GET", "POST"])

app.add_url_rule("/userSecond", "userSecond", userSecond, methods=["GET", "POST"])

app.add_url_rule("/userThird", "userThird", userThird, methods=["GET", "POST"])

app.add_url_rule("/userClose", "userClose", userClose, methods=["GET", "POST"])

app.add_url_rule("/selectTitle", "selectTitle", selectTitle, methods=["POST"])

app.add_url_rule("/searchThesis/<inputTitle>", "searchThesis", searchThesis, methods=["GET"])

app.add_url_rule("/approvedThesisByAdmin/<email>/<boolean>", "approvedThesisByAdmin", approvedThesisByAdmin, methods=["GET"])


if __name__ == "__main__":
   app.run(debug=True)