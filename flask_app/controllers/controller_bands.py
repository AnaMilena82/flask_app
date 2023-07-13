from flask import render_template, session,flash,redirect, request, url_for
import re
from flask_app import app
from flask import get_flashed_messages
from flask_app.models.model_bands import Bands
from flask_app.models.model_bands import Join
from flask_app.controllers import controller_users


@app.route('/dashboard',methods=['GET'])
def dashboard():
    if 'id' in session:
        list_bands = Bands.get_allbands_with_user()
        mensaje = get_flashed_messages(category_filter=['error_join'])
        return render_template("dashboard.html", list_bands = list_bands, mensaje=mensaje)
    return redirect('/')

@app.route('/new/sighting',methods=['GET'])
def get_new_band():
    if 'id' in session:
        return render_template("add_band.html")
    return redirect('/')      

@app.route('/new/sighting',methods=['POST'])
def post_new_band():
    data = {
        **request.form,
        "user_id": session['id']
    }
    if Bands.validate_band(data) == False:
         return redirect('/new/sighting')
    else:
        id_band = Bands.new_band(data)
        return redirect('/dashboard')

@app.route('/edit/<int:id>',methods=['GET'])
def get_edit_band(id):
    if 'id' in session:
        data = {
        "id": id
        }
        band = Bands.show_one_band(data)  
        return render_template("edit_band.html", band = band)
    return redirect('/')  

@app.route('/edit/<int:id>', methods = ['POST'])
def edit_band(id):
    
    if Bands.validate_band(request.form) == False:
         return redirect(f'/edit/{id}')
    else:
        data = {
            **request.form,
            "id": id
           
        }
        Bands.edit_one_band(data)
        return redirect('/dashboard')
    

@app.route('/delete/<int:id>')
def delete_band(id):
    data = {
        "id": id
    }
    user_id = Bands.get_user_id_by_band_id(id)
    print("Deleting Band with ID:", id)
    Bands.delete_one_band(data)
    return redirect(url_for('dashboard'))


@app.route('/mybands/<int:id>',methods=['GET'])
def get_show_mybands(id):
    if 'id' in session:
        data = {
        "id": id
        }
        bands  = Bands.get_bands_by_user_id(session['id'])
        joined_bands = Bands.get_allbands_user_joined(session['id'])
        return render_template("mybands.html", bands  = bands, joined_bands = joined_bands )
    return redirect('/')  

@app.route('/join_band/<int:band_id>', methods=['GET'])
def join_band(band_id):
    if 'id' in session:
        user_id = session['id']
        band = Bands.get_one_band({'id': band_id})
        if band:
            band.add_join(user_id)
        else:
            flash("The band you are trying to join does not exist.", "error_join")
        return redirect('/dashboard')
    return redirect('/')

@app.route('/quit_band/<int:band_id>', methods=['GET'])
def quit_band(band_id):
    if 'id' in session:
        user_id = session['id']
        band = Bands.get_one_band({'id': band_id})
        if band:
            Join.remove_join(user_id, band_id)
        else:
            flash("The band you are trying to leave does not exist.", "error_leave")
        return redirect('/dashboard')
    return redirect('/')
