from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from app.models import Tasks
from app import db

tasks_bp= Blueprint("tasks", __name__)

@tasks_bp.route('/')
def view_tasks():
    user_id = session.get('user_id')
    if user_id is None:
        flash("Please log in to view your tasks.", "warning")
        return redirect(url_for('auth.login'))

    
    tasks = Tasks.query.filter_by(user_id=user_id).all()
    return render_template('tasks.html', tasks=tasks)
   

@tasks_bp.route('/add', methods=['POST'])
def add_task():

    user_id = session.get('user_id')
    if user_id is None:
        flash("Please log in to add tasks.", "warning")
        return redirect(url_for('auth.login'))
    

    title = request.form.get('title')
    if title:
        new_task = Tasks(title=title, user_id=user_id)
        db.session.add(new_task)
        db.session.commit()
        flash('Task added successfully!', 'success')
   

    return redirect(url_for('tasks.view_tasks'))

@tasks_bp.route("/toggle/<int:task_id>", methods=["POST"])

def toggle_task(task_id):
    user_id = session.get('user_id')
    if user_id is None:
        flash("Please log in first.", "warning")
        return redirect(url_for('auth.login'))

    task = Tasks.query.filter_by(id=task_id, user_id=user_id).first()

    if task:
        if task.status == "Pending":
            task.status = "Working"
        elif task.status == "Working":
            task.status = "Completed"
        else:
            task.status = "Pending"
        db.session.commit()
        flash("Task status updated.", "success")
    else:
        flash("Task not found or unauthorized.", "danger")

    return redirect(url_for('tasks.view_tasks'))

@tasks_bp.route('/clear', methods=['POST'])
def clear_tasks():


    user_id = session.get('user_id')
    if user_id is None:
        flash("Please log in to clear your tasks.", "warning")
        return redirect(url_for('auth.login'))

    Tasks.query.filter_by(user_id=user_id).delete()
    db.session.commit()
    flash('All your tasks have been cleared!', 'success')

    return redirect(url_for('tasks.view_tasks'))

@tasks_bp.route('/reset-db')  # ⚠️ Development only — remove in production
def reset_db():
    db.drop_all()
    db.create_all()
    return "✅ Database reset!"