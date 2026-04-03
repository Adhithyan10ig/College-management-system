from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")

if "mongodb+srv" in MONGO_URI:
    client = MongoClient(
        MONGO_URI,
        tls=True,
        tlsAllowInvalidCertificates=True,
        serverSelectionTimeoutMS=5000,
        connectTimeoutMS=5000,
        socketTimeoutMS=5000
    )
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