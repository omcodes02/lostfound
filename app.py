from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# DATABASE CONNECTION
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345",
    database="lost_found",
    auth_plugin='mysql_native_password',
    charset='utf8',
    use_unicode=True
)

cursor = db.cursor()
