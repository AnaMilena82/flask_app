from flask import render_template, session, request, redirect, flash, url_for
from flask_app import app
from flask_app.models.model_users import User
from flask_app.models.model_bands import Bands
from flask_app.models.model_joins import Join


def join(user_id, band_id):
    user = User.get_one_with_id({'id': user_id})
    band = Bands.get_one_band({'id': band_id})

    if user and band:
        if not Join.is_joined(user.id, band.id):
            band.add_join(user.id)
     
    else:
        flash('Invalid user or band.', 'error_join')

def get_joins(band_id):
    joins = Join.get_joins_by_band_id(band_id)
    return joins
