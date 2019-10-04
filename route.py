from flask import Flask, render_template, request, make_response, send_from_directory, escape, redirect, url_for, jsonify
import os
import random
import datetime
from db import test, fetchAdminWithEmailPassword, fetchAdminWithEmail, saveAdmin, fetchAllAdminExceptMe, fetchAllUser, fetchUserWithEmailPassword, fetchUserWithEmail, saveUser, fetchAllThesis, saveThesis, fetchThesisWithEmail, saveStep, fetchStepByEmailStep, fetchAllThesisNotDone, deleteAdmin, deleteUser, updateThesisPending, fetchStepNoByEmailStep
from models import Admin
from brute import bruteForce

STEP_TITLE = "TITLE"
STEP_FIRST = "FIRST"
STEP_SECOND = "SECOND"
STEP_THIRD = "THIRD"
STEP_CLOSE = "CLOSE"

def index() :
    # test()
    # store_data = pd.read_csv('babystore.csv')
    # bruteForce("text", [])

    return render_template('index.html')

def loginAdmin() :
    if request.method == 'GET':
        return render_template('loginAdmin.html')
    else :
        email = request.form["email"]
        password = request.form["password"]
    
        admin = fetchAdminWithEmailPassword(email, password)
        if admin:
            response = make_response(redirect("/homeAdmin"))
            response.set_cookie("loggedEmail", email)
            response.set_cookie("loggedName", admin[1])
            return response
        else :
            return render_template('loginAdmin.html', email=email, errorText="User name or password does not match!")

def loginUser() :
    if request.method == 'GET':
        return render_template('loginUser.html')
    else :
        email = request.form["email"]
        password = request.form["password"]
        print(email,password)
        admin = fetchUserWithEmailPassword(email, password)
        if admin:
            response = make_response(redirect("/homeUser"))
            response.set_cookie("loggedEmail", email)
            response.set_cookie("loggedName", admin[1])
            return response
        else :
            return render_template('loginUser.html', email=email, errorText="User name or password does not match!")

def logout() :
    response = make_response(redirect("/"))
    response.set_cookie("loggedEmail", expires=0)
    response.set_cookie("loggedName", expires=0)
    return response

def signupUser() :
    if request.method == 'GET':
        return render_template('signupUser.html')
    else :
        email = request.form["email"]
        name = request.form["name"]
        rollNo = request.form["rollNumber"]
        password = request.form["password"]

        user = fetchUserWithEmail(email)
        if user:
            return render_template('signupUser.html', email=email, name=name, rollNumber=rollNo, errorText="Email already exists!")    
        else :
            saveUser(email, name, "6IST-"+rollNo, password)
            return redirect("/loginUser")

def homeAdmin() :
    loggedEmail = request.cookies.get("loggedEmail")
    adminList = fetchAllAdminExceptMe(loggedEmail)
    return render_template('homeAdmin.html', **request.args, adminList=adminList)

def homeAdminDelete(email) :
    loggedEmail = request.cookies.get("loggedEmail")
    deleteAdmin(email)
    return redirect("/homeAdmin")

def homeAdminUsers() :
    loggedEmail = request.cookies.get("loggedEmail")
    userList = fetchAllUser()
    return render_template('homeAdmin.html', **request.args, userList=userList)

def homeAdminUsersDelete(email) :
    loggedEmail = request.cookies.get("loggedEmail")
    deleteUser(email)
    return redirect("/homeAdminUsers")

def homeAdminTitles() :
    loggedEmail = request.cookies.get("loggedEmail")
    titleList = fetchAllThesisNotDone()
    return render_template('homeAdmin.html', **request.args, titleList=titleList)

def homeAdminTitleView(email, title):
    loggedEmail = request.cookies.get("loggedEmail")
    thesis = fetchThesisWithEmail(email)
    stepTitle = fetchStepByEmailStep(email, STEP_TITLE)
    stepFirst = fetchStepByEmailStep(email, STEP_FIRST)
    stepSecond = fetchStepByEmailStep(email, STEP_SECOND)
    stepThird = fetchStepByEmailStep(email, STEP_THIRD)
    stepClose = fetchStepByEmailStep(email, STEP_CLOSE)
    return render_template('homeAdmin.html', **request.args, thesis=thesis, stepTitle=stepTitle, stepFirst=stepFirst, stepSecond=stepSecond, stepThird=stepThird, stepClose=stepClose)

def addAdmin() :
    if request.method == 'GET':
        return redirect(url_for("homeAdmin", addAdminShow="show"))
    else :
        email = request.form["email"]
        name = request.form["name"]
        password = request.form["password"]

        admin = fetchAdminWithEmail(email)
        if admin :
            return redirect(url_for("homeAdmin", addAdminShow="show", email=email, name=name, errorText="Email already exists!"))
        else :
            saveAdmin(email, name, password)
            return redirect(url_for("homeAdmin", addAdminShow=None))

def homeUser() :
    loggedEmail = request.cookies.get("loggedEmail")
    if request.method == 'GET':
        thesis = fetchThesisWithEmail(loggedEmail)
        step = fetchStepByEmailStep(loggedEmail, STEP_TITLE)
        stepNo = fetchStepNoByEmailStep(loggedEmail)
       
        return render_template('homeUser.html', **request.args, thesis=thesis, step=step, stepNo=stepNo)
    else :
        selectedTitle = request.form["title"]
        userRaw = fetchUserWithEmail(loggedEmail)
        email = userRaw[0]
        name = userRaw[1]
        rollNo = userRaw[2]
        saveThesis(selectedTitle, email, name, rollNo, "2018-2019", 0)
        thesis = fetchThesisWithEmail(loggedEmail)
        return render_template('homeUser.html', **request.args, thesis = thesis)

def commaSeparatedListString(stringList):
    listString = ""
    for i,s in enumerate(stringList):
        if i==0:
            listString += s
        else:
            listString += ","+s
    return listString

def selectTitle() : 
    loggedEmail = request.cookies.get("loggedEmail")
    expectedOutput = request.form["expectedOutput"]
    deadline = request.form["deadline"]
    taskRaw = request.form.getlist("task")

    if len(taskRaw)>0 :
        tasks = commaSeparatedListString(taskRaw)
        saveStep(loggedEmail, STEP_TITLE, deadline, tasks, expectedOutput)
    return redirect(url_for('homeUser', **request.args, selectedTitle="Project Management System"))

def userFirst() :
    loggedEmail = request.cookies.get("loggedEmail")
    if request.method == 'GET':
        loggedEmail = request.cookies.get("loggedEmail")
        thesis = fetchThesisWithEmail(loggedEmail)
        step = fetchStepByEmailStep(loggedEmail, STEP_FIRST)
        stepNo = fetchStepNoByEmailStep(loggedEmail)
        return render_template('homeUser.html', **request.args, step=step, thesis=thesis, stepNo=stepNo)
    else :
        deadline = request.form["deadline"]
        taskRaw = request.form.getlist("task")

        if len(taskRaw)>0 :
            tasks = commaSeparatedListString(taskRaw)
            saveStep(loggedEmail, STEP_FIRST, deadline, tasks, "")
            return redirect("/userFirst")

def userSecond() :
    loggedEmail = request.cookies.get("loggedEmail")
    if request.method == 'GET':
        loggedEmail = request.cookies.get("loggedEmail")
        thesis = fetchThesisWithEmail(loggedEmail)
        step = fetchStepByEmailStep(loggedEmail, STEP_SECOND)
        stepNo = fetchStepNoByEmailStep(loggedEmail)
        return render_template('homeUser.html', **request.args, step=step, thesis=thesis, stepNo=stepNo)
    else :
        deadline = request.form["deadline"]
        taskRaw = request.form.getlist("task")

        if len(taskRaw)>0 :
            tasks = commaSeparatedListString(taskRaw)
            saveStep(loggedEmail, STEP_SECOND, deadline, tasks, "")
            return redirect("/userSecond")

def userThird() :
    loggedEmail = request.cookies.get("loggedEmail")
    if request.method == 'GET':
        loggedEmail = request.cookies.get("loggedEmail")
        thesis = fetchThesisWithEmail(loggedEmail)
        step = fetchStepByEmailStep(loggedEmail, STEP_THIRD)
        stepNo = fetchStepNoByEmailStep(loggedEmail)
        return render_template('homeUser.html', **request.args, step=step, thesis=thesis, stepNo=stepNo)
    else :
        deadline = request.form["deadline"]
        taskRaw = request.form.getlist("task")

        if len(taskRaw)>0 :
            tasks = commaSeparatedListString(taskRaw)
            saveStep(loggedEmail, STEP_THIRD, deadline, tasks, "")
            return redirect("/userThird")
        
def userClose() :
    loggedEmail = request.cookies.get("loggedEmail")
    if request.method == 'GET':
        loggedEmail = request.cookies.get("loggedEmail")
        thesis = fetchThesisWithEmail(loggedEmail)
        step = fetchStepByEmailStep(loggedEmail, STEP_CLOSE)
        stepNo = fetchStepNoByEmailStep(loggedEmail)
        return render_template('homeUser.html', **request.args, step=step, thesis=thesis, stepNo=stepNo)
    else :
        deadline = request.form["deadline"]
        taskRaw = request.form.getlist("task")
        print("deadline: ", deadline)

        if len(taskRaw)>0 :
            tasks = commaSeparatedListString(taskRaw)
            saveStep(loggedEmail, STEP_CLOSE, deadline, tasks, "")
            return redirect("/userClose")

# def searchThesis(inputTitle):
#     loggedEmail = request.cookies.get("loggedEmail")
#     thesisList = fetchAllThesis()

#     thesisSearchResult = []
#     for t in thesisList:
#         if len(thesisSearchResult) >=5:
#             break
#         elif inputTitle.lower().strip() in t.title.lower().strip():
#             thesis = {
#                 "title": t.title,
#                 "name": t.name,
#                 "rollNo": t.rollNo,
#                 "year": t.year
#             }
#             thesisSearchResult.append(thesis)
        
#     return jsonify(thesisSearchResult)

def searchThesis(inputTitle):
    loggedEmail = request.cookies.get("loggedEmail")
    thesisList = fetchAllThesis()

    thesisSearchResult = []
    for t in thesisList:
        if len(thesisSearchResult) >=5:
            break
        elif bruteForce(str(inputTitle), str(t.title)):
            thesis = {
                "title": t.title,
                "name": t.name,
                "rollNo": t.rollNo,
                "year": t.year
            }
            thesisSearchResult.append(thesis)
    
    return jsonify(thesisSearchResult)


def approvedThesisByAdmin(email, boolean) :
    updateThesisPending(email, boolean)
    return redirect("/homeAdminTitles")