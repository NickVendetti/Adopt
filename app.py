from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import Pet, db, connect_db 
from forms import AddPetForm, EditPetForm
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/adopt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mysecretkey'

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def show_homepage():
    pets = Pet.query.all()
    return render_template('homepage.html', pets=pets)

def save_image(image):
    if image:
        filename = secure_filename(image.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(filepath)
        return filepath 
    return None

@app.route('/add', methods=["GET", "POST"])
def add_pet():
    form = AddPetForm()

    if form.validate_on_submit():
        photo_url = form.photo_url.data
        if form.photo.data:
            photo_url = save_image(form.photo.data)

        new_pet = Pet(
            name=form.name.data,
            species=form.species.data,
            photo_url=form.photo_url.data,
            age=form.age.data,
            notes=form.notes.data,
            available=True
        )
        db.session.add(new_pet)
        db.session.commit()
        return redirect(url_for('show_homepage'))
    
    return render_template('add_pet.html', form=form)

@app.route('/<int:pet_id>', methods=["GET", "POST"])
def show_edit_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet) # pre-fill the form with the current pet data

    if form.validate_on_submit():
        pet.photo_url = form.photo_url.data
        if form.photo.data:
            pet.photo_url = save_image(form.photo.data)
        pet.notes = form.notes.data
        pet.available = form.available.data
        db.session.commit()
        return redirect(url_for('show_homepage'))
    
    return render_template('edit_pet.html', pet=pet, form=form)