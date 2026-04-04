from pymongo import MongoClient
import os
import certifi

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")

if "mongodb+srv" in MONGO_URI or "mongodb.net" in MONGO_URI:
    client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
else:
    client = MongoClient(MONGO_URI)

db = client["college_management"]

users_col       = db["users"]
students_col    = db["students"]
faculty_col     = db["faculty"]
courses_col     = db["courses"]
attendance_col  = db["attendance"]
marks_col       = db["marks"]
fees_col        = db["fees"]