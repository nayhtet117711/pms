from flask import Flask, render_template, request, make_response, send_from_directory, escape, redirect, url_for
import os
import random
import datetime
from flask_mysqldb import MySQL
from models import Admin, User, Thesis, Step

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)

mysql = MySQL(app)

def test() :
    df = pd.read_excel(r'2.xlsx', sheet_name='Sheet2')
    
    for row in range(df.shape[0]):
        name = df.iat[row, 1]
        rollNo = df.iat[row, 0]
        title = df.iat[row, 2]
        year = df.iat[row, 3]
        print("data: ", row, name, rollNo, title, year)

        cursor = mysql.connection.cursor()
        cursor.execute("insert into thesis(name, rollNo, title, year, done) values(%s, %s, %s, %s, %s)", (name, rollNo, title, year, True))
        mysql.connection.commit()
        cursor.close()

    return


def fetchAdminWithEmailPassword(email, password):
    cursor = mysql.connection.cursor()
    cursor.execute("select email, name from admin where email=%s and password=%s", (email, password))
    admin = cursor.fetchone()
    mysql.connection.commit()
    cursor.close()
    return admin

def fetchAdminWithEmail(email):
    cursor = mysql.connection.cursor()
    cursor.execute("select email, name from admin where email='%s'"%(email))
    admin = cursor.fetchone()
    mysql.connection.commit()
    cursor.close()
    return admin

def saveAdmin(email, name, password):
    cursor = mysql.connection.cursor()
    cursor.execute("insert into admin(email, name, password) values(%s, %s, %s)", (email, name, password))
    mysql.connection.commit()
    cursor.close()
    return

def fetchAllAdminExceptMe(email): 
    cursor = mysql.connection.cursor()
    cursor.execute("select email, name from admin where email!='%s'"%(email))
    adminListRaw = cursor.fetchall()
    mysql.connection.commit()
    cursor.close()

    adminList = []
    for admin in adminListRaw :
        a = Admin()
        a.email = admin[0]
        a.name = admin[1]
        adminList.append(a)
    return adminList

def fetchAllUser():
    cursor = mysql.connection.cursor()
    cursor.execute("select email, name, rollNo from user")
    userListRaw = cursor.fetchall()
    mysql.connection.commit()
    cursor.close()

    userList = []
    for user in userListRaw :
        u = User()
        u.email = user[0]
        u.name = user[1]
        u.rollNo = user[2]
        userList.append(u)
    return userList

def saveUser(email, name, rollNo, password):
    cursor = mysql.connection.cursor()
    cursor.execute("insert into user(email, name, rollNo, password) values(%s, %s, %s, %s)", (email, name, rollNo, password))
    mysql.connection.commit()
    cursor.close()
    return

def fetchUserWithEmailPassword(email, password):
    cursor = mysql.connection.cursor()
    cursor.execute("select email, name from user where email=%s and password=%s", (email, password))
    user = cursor.fetchone()
    mysql.connection.commit()
    cursor.close()
    return user

def fetchUserWithEmail(email):
    cursor = mysql.connection.cursor()
    cursor.execute("select email, name, rollNo from user where email='%s'"%(email))
    user = cursor.fetchone()
    mysql.connection.commit()
    cursor.close()
    return user

def fetchAllThesis():
    cursor = mysql.connection.cursor()
    cursor.execute("select title, name, rollNo, year, done, email, pending from thesis")
    thesisListRaw = cursor.fetchall()
    mysql.connection.commit()
    cursor.close()

    thesisList = []
    for thesis in thesisListRaw :
        t = Thesis()
        t.title = thesis[0]
        t.name = thesis[1]
        t.rollNo = thesis[2]
        t.year = thesis[3]
        t.done = thesis[4]
        t.email = thesis[5]
        t.pending = thesis[6]
        thesisList.append(t)

    return thesisList

def fetchAllThesisNotDone():
    cursor = mysql.connection.cursor()
    cursor.execute("select title, name, rollNo, year, done, email, pending from thesis where done=0")
    thesisListRaw = cursor.fetchall()
    mysql.connection.commit()
    cursor.close()

    thesisList = []
    for thesis in thesisListRaw :
        t = Thesis()
        t.title = thesis[0]
        t.name = thesis[1]
        t.rollNo = thesis[2]
        t.year = thesis[3]
        t.done = thesis[4]
        t.email = thesis[5]
        t.pending = thesis[6]
        thesisList.append(t)

    return thesisList

def saveThesis(title, email, name, rollNo, year, done):
    cursor = mysql.connection.cursor()
    cursor.execute("insert into thesis(title, email, name, rollNo, year, done) values(%s, %s, %s, %s, %s, %s)", (title, email, name, rollNo, year, done))
    mysql.connection.commit()
    cursor.close()
    return 

def fetchThesisWithEmail(email):
    cursor = mysql.connection.cursor()
    cursor.execute("select title, email, name, rollNo, year, done, pending from thesis where email='%s'"%(email))
    thesisRaw = cursor.fetchone()
    if thesisRaw is None:
        return None
    thesis = Thesis()
    thesis.title = thesisRaw[0]
    thesis.email = thesisRaw[1]
    thesis.name = thesisRaw[2]
    thesis.rollNo = thesisRaw[3]
    thesis.year = thesisRaw[4]
    thesis.done = thesisRaw[5]
    thesis.pending = thesisRaw[6]
    # print("thesis: ", thesis)
    mysql.connection.commit()
    cursor.close()
    return thesis

def updateThesisPending(email, boolean):
    cursor = mysql.connection.cursor()
    if int(boolean)==1 :
        cursor.execute("delete from thesis where email='%s'"%(email))
        cursor.execute("delete from step where email='%s'"%(email))
    else : 
        cursor.execute("update thesis set pending=0 where email='%s'"%(email))
        

    mysql.connection.commit()
    cursor.close()
    return

def saveStep(email, step, deadline, tasks, expectedOutput=""):
    cursor = mysql.connection.cursor()
    cursor.execute("insert into step(email,step, deadline, expectedOutput, tasks) values(%s, %s, %s, %s, %s)", ( email, step, deadline, expectedOutput, tasks))
    mysql.connection.commit()
    cursor.close()
    return 

def fetchStepByEmailStep(email, step):
    cursor = mysql.connection.cursor()
    cursor.execute("select email,step, deadline, expectedOutput, tasks from step where email='%s' and step='%s'"%(email, step))
    stepRaw = cursor.fetchone()
    if stepRaw is None :
        return None
    step = Step()
    step.email = stepRaw[0]
    step.step = stepRaw[1]
    step.deadline = stepRaw[2]
    step.expectedOutput = stepRaw[3]
    step.tasks = stepRaw[4].split(",")
    mysql.connection.commit()
    cursor.close()
    return step

def fetchStepNoByEmailStep(email):
    cursor = mysql.connection.cursor()
    cursor.execute("select count(*) from step where email='%s'"%(email))
    stepNo = cursor.fetchone()

    return stepNo[0]

def deleteAdmin(email):
    cursor = mysql.connection.cursor()
    cursor.execute("delete from admin where email='"+email+"'")
    mysql.connection.commit()
    cursor.close()
    return

def deleteUser(email):
    cursor = mysql.connection.cursor()
    cursor.execute("delete from user where email='"+email+"'")
    cursor.execute("delete from step where email='"+email+"'")
    cursor.execute("delete from thesis where email='"+email+"'")
    mysql.connection.commit()
    cursor.close()
    return