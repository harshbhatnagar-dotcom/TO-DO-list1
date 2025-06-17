from flask import Blueprint,render_template,redirect,url_for,flash ,request,session
from app.models import Users
from app import db

auth_bp= Blueprint("auth",__name__)


USER_CREDENTIALS={
    'username': 'admin',
    'password': 'admin123'
}
@auth_bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method=="POST":
        username=request.form.get('username')
        password=request.form.get('password')
        confirm_password=request.form.get('confirm_password')
        name=request.form.get('name')
        phone=request.form.get('phone')
        email=request.form.get('email')

        if password != confirm_password:
             flash('Passwords do not match!', 'danger')
             return render_template('register.html')
    
        existing_user=Users.query.filter_by(username=username).first()
        if existing_user:
             flash('Username already exists!', 'danger')
             return render_template('register.html')
    
        new_user=Users(username=username,password=password,name=name,phone=phone,email=email)
        db.session.add(new_user)    
        db.session.commit()
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')





@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=="POST":
        username = request.form.get('username')
        password = request.form.get('password')

        user=Users.query.filter_by(username=username).first()
        if user and user.password == password:
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Login successful!', 'success')
            return redirect(url_for('tasks.view_tasks'))  # Redirect to tasks view after successful login
        
        else:
            flash('Invalid credentials, please try again.', 'danger')
    
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.login'))

