from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI, tls=True, tlsAllowInvalidCertificates=True)
db = client["college_management"]

# Collections
users_col       = db["users"]
students_col    = db["students"]
faculty_col     = db["faculty"]
courses_col     = db["courses"]
attendance_col  = db["attendance"]
marks_col       = db["marks"]
fees_col        = db["fees"]