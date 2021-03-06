from application import app, db, bcrypt
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import current_user, logout_user, login_required
from application.user.UserModel import User
from application.user.EditUserForm import EditUserForm

@app.route("/editUserInfo")
@login_required
def edit_userinfo_form():
    return render_template("user/editUserInfo.html", form = EditUserForm())

@app.route("/editUserInfo", methods=["POST"])
@login_required
def edit_userinfo():

    form = EditUserForm(request.form)

    new_username = form.username.data
    new_password = form.password.data

    hashed_new_password = bcrypt.generate_password_hash(new_password, 10)

    utf8_hashed_password = hashed_new_password.decode("utf-8", "ignore")

    user = User.query.get(current_user.id)

    user.username = new_username
    user.password = utf8_hashed_password
    
    db.session().commit()

    return render_template("user/editUserInfo.html", form = EditUserForm(), message="Käyttäjän tiedot muokattiin onnistuneesti!")

@app.route("/editUserInfo/delete", methods=["POST"])
@login_required
def delete_user_account():

    deleted_user = User.query.filter_by(id=current_user.id).first()

    db.session.delete(deleted_user)
    db.session.commit()
    
    logout_user()
    return redirect(url_for("index"))
