from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def create_table():
    conn = sqlite3.connect("complaints.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT,
            room_number TEXT,
            complaint TEXT,
            status TEXT DEFAULT 'Pending'
        )
    """)
    conn.commit()

    try:
        conn.execute(
            "ALTER TABLE complaints ADD COLUMN status TEXT DEFAULT 'Pending'"
        )
        conn.commit()
    except sqlite3.OperationalError:
        pass

    conn.close()


        
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form["student_name"]
    room = request.form["room_number"]
    complaint = request.form["complaint"]

    conn = sqlite3.connect("complaints.db")
    conn.execute(
        "INSERT INTO complaints (student_name, room_number, complaint) VALUES (?, ?, ?)",
        (name, room, complaint)
    )
    conn.commit()
    conn.close()

    return "<h2>Complaint submitted successfully!</h2><a href='/'>Go Back</a>"

@app.route("/warden")
def warden():
    conn = sqlite3.connect("complaints.db")
    complaints = conn.execute("SELECT * FROM complaints").fetchall()
    conn.close()
    return render_template("warden.html", complaints=complaints)
    
@app.route("/update_status/<int:id>", methods=["POST"])
def update_status(id):
    conn = sqlite3.connect("complaints.db")
    conn.execute(
        "UPDATE complaints SET status = 'Completed' WHERE id = ?",
        (id,)
    )
    conn.commit()
    conn.close()
    return redirect("/warden")



if __name__ == "__main__":
    create_table()
    app.run(debug=True)
