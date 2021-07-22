import datetime
from flask import Blueprint
from flask import render_template, request, redirect, url_for, jsonify
from flask import g
from . import db

bp = Blueprint("task", "task", url_prefix="")
max=0

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
                due =  due,
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
       
        details = request.form.get('details')
        creation = datetime.datetime.today().strftime("%Y-%m-%d %H:%M")
        taskname= request.form.get("taskname")
        due=request.form.get("due")
        if(not taskname or not due):
            return redirect(url_for("task.dashboard"), 302)
        due=due.replace("T","\t")
        global max
        max+=1
        progress="in progress"
        cursor.execute("INSERT INTO  TASKTABLE  (taskname, creation, due, details,progress) VALUES (?,?,?,?,?)",(taskname, creation, due, details,progress))        
        conn.commit()
        return redirect(url_for("task.dashboard"), 302)
        
@bp.route("/<id>/edit", methods=["GET", "POST"])
def edit(id):
    conn = db.get_db()
    cursor = conn.cursor()
    if request.method == "GET":
        cursor.execute("select id,taskname,creation,due,details,progress from TASKTABLE where id=?", [id])
        task = cursor.fetchone()
        id,taskname,creation,due,details,progress = task
        data = dict(id = id,
                    taskname = taskname,
                    creation = creation,
                    due = due,
                    details = details,
                    progress = progress)
        return render_template("updatetask.html", **data)
    elif request.method == "POST":
        taskname=request.form.get('taskname')
        details = request.form.get('details')
        due = request.form.get("due")
        due=due.replace("T","\t")
        id=id
        cursor.execute("update TASKTABLE set taskname = ? where id = ?",(taskname,id))
        cursor.execute("update TASKTABLE set details = ? where id = ?",(details,id))    
        if(due):
            cursor.execute("update TASKTABLE set due = ? where id = ?", (due, id))    
        conn.commit()
        return redirect(url_for("task.task_details",id=id), 302)
    



