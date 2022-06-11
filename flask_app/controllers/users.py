from flask_app import app
from flask import render_template, redirect, request
from flask_app.models.user import User

# root
@app.route('/')
def root():
    users=User.get_all()
    return render_template('read.html', users=users)

#Create
@app.route('/create', methods=['POST'])
def create_new_user():
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email']
    }
    User.save(data)
    id_dict=User.get_id_by_email(data)
    id=str(id_dict['id'])
    return redirect('/show/' + id)

@app.route('/user/new')
def display_form():
    return render_template('create.html')

#Read
@app.route('/show/<int:id>')
def show_user(id):
    user_to_display=User.get_one_user_by_id(id)
    return render_template('user_display.html', user_to_display=user_to_display)

#Update
@app.route('/edit/<int:id>')
def update_user(id):
    user_to_update=User.get_one_user_by_id(id)
    return render_template('edit_user.html', user_to_update=user_to_update)

@app.route('/user/update', methods=['POST'])
def update_user_info():
    User.update_by_id(request.form)
    id=request.form['id']
    return redirect('/show/' + id)

#Delete
@app.route('/delete/<int:id>')
def delete_user(id):
    User.delete_by_id(id)
    return redirect('/')