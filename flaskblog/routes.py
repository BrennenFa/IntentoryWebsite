import os
import secrets
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login.utils import login_required
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, ItemForm
from flaskblog.models import User, Item
from flask_login import login_user, current_user, logout_user

@app.route("/")
def home():
  return render_template('home.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
  if current_user.is_authenticated:
    return redirect(url_for('home'))
  form = RegistrationForm()
  print(form.validate_on_submit())

  if form.validate_on_submit():
    hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    user = User(username=form.username.data, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('home'))
  return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(username=form.username.data).first()
    if user and bcrypt.check_password_hash(user.password, form.password.data):
      login_user(user)
      return redirect(url_for('home'))


  return render_template('login.html', title='Login', form=form)


@app.route("/logut")
def logout():
  logout_user()
  return redirect(url_for('home'))

#table

@app.route("/table", methods=['GET', 'POST'])
@login_required
def table():
  form = ItemForm()
  if form.validate_on_submit():
    item = Item(content=form.content.data, number=form.number.data, author=current_user)
    db.session.add(item)
    db.session.commit()
  items = Item.query.all()
  return render_template('table.html', items=items, form=form)

@app.route('/delete/<int:id>')
@login_required
def delete(id):
  item = Item.query.get_or_404(id)
  if item.author != current_user:
    abort(403)
  try:
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for("table"))
  except:
    return 'There was an error'

@app.route('/update/<int:id>', methods=["GET", "POST"])
@login_required
def update(id):
  item = Item.query.get_or_404(id)
  if request.method == 'POST':
    item.content = request.form['content']
    item.number = request.form['number']
  
    try:
      db.session.commit()
      return redirect(url_for('table'))
    except:
      return 'There was an error' 
  else:
    return render_template('update.html', item=item)