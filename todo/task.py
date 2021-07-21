import datetime
from flask import Blueprint
from flask import render_template, request, redirect, url_for, jsonify
from flask import g
from . import db

bp = Blueprint("task", "task", url_prefix="")
max=0
def format_date(d):
    if d:
        v = d.strftime('%Y-%m-%d %H:%M:%S')
        return v
    else:
        return None

@bp.route("/")
def dashboard():
    conn = db.get_db()
    cursor = conn.cursor()
    oby = request.args.get("order_by", "id")
    order = request.args.get("order", "asc")
    if order == "asc":
        cursor.execute(f"select id,taskname,creation,due,progress from TASKTABLE  order by {oby}")
    else:
        cursor.execute(f"select id,taskname,creation,due,progress from TASKTABLE  order by {oby} desc")
    data = cursor.fetchall()
    return render_template('index.html', TASKTABLE = data, order="desc" if order=="asc" else "asc")

@bp.route("/<id>")
def task_details(id): 
    conn = db.get_db()
    cursor = conn.cursor()
    cursor.execute("select id,taskname,creation,due,details,progress from TASKTABLE where id = ?",[id])
    task = cursor.fetchone()
    id,taskname,creation,due,details,progress = task
    id = int(id)
    global max
    if(id>max):
        max=id
    if id == 1:
        prev = None
    else:
        prev = id - 1
    next = id + 1
    if (next>max):
        next= None
    data = dict(id = id,
                name = taskname,
                creation = datetime.datetime.strptime(creation, '%Y-%m-%d %H:%M'),
                due =  datetime.datetime.strptime(due, '%Y-%m-%d\t%H:%M'),
                details = details, 
                progress = progress
                )
    return render_template("taskdetails.html", **data,prev=prev,next=next)

@bp.route("/add", methods=["GET","POST"])
def add():
    conn = db.get_db()
    cursor = conn.cursor()
    if request.method == "GET":
        cursor.execute("select id,taskname,creation,due,details,progress from TASKTABLE")
        task = cursor.fetchone()

        data = dict(
                    taskname = "",
                    creation="",
                    due="",
                    details="",
                    progress="")
        return render_template("edittask.html", **data)

    elif request.method == "POST":
        global max
        max+=1
        details = request.form.get('details')
        creation = datetime.datetime.today().strftime("%Y-%m-%d %H:%M")
        taskname= request.form.get("taskname")
        due=request.form.get("due")
        due=due.replace("T","\t")
        progress="in progress"
        cursor.execute("INSERT INTO  TASKTABLE  (taskname, creation, due, details,progress) VALUES (?,?,?,?,?)",(taskname, creation, due, details,progress))        
        conn.commit()
        return redirect(url_for("task.dashboard"), 302)
        
    



