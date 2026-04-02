# 🎓 College Management System

A web-based College Management System built with **Flask**, **MongoDB**, and **Python**.

## 🌐 Live Demo
[https://college-management-system-y4q5.onrender.com](https://college-management-system-y4q5.onrender.com)

## ✨ Features
- Admin login with session management
- Student management (Add, View, Delete)
- Faculty management
- Course & Enrollment tracking
- Attendance marking
- Marks & Grades recording
- Fee management

## 🛠️ Tech Stack
- **Backend:** Python, Flask
- **Database:** MongoDB Atlas
- **Frontend:** HTML, CSS, JavaScript (Jinja2 templates)
- **Deployment:** Render

## 🚀 Run Locally

1. Clone the repo
```bash
   git clone https://github.com/Adhithyan10ig/College-management-system.git
   cd College-management-system
```

2. Install dependencies
```bash
   pip install -r requirements.txt
```

3. Create a `.env` file
```
   MONGO_URI=mongodb://localhost:27017/
   SECRET_KEY=yoursecretkey
```

4. Run the app
```bash
   python app.py
```

5. Open browser at `http://localhost:5000`
   - Login: `admin` / `admin123`

## 📁 Project Structure
```
college-management/
├── app.py               # Main Flask app & routes
├── config.py            # MongoDB connection
├── requirements.txt
├── Procfile             # For Render deployment
└── templates/
    ├── login.html
    ├── base.html        # Sidebar layout
    ├── dashboard.html
    ├── students.html
    ├── faculty.html
    ├── courses.html
    ├── attendance.html
    ├── marks.html
    └── fees.html
```

## 📸 Screenshots
> Login page and dashboard coming soon

## 👤 Author
**Adhithyan** — B.Tech CSE @ Adi Shankara Institute of Engineering and Technology