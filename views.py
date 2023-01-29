from flask import request, render_template
from app import app
from utils import *

@app.route('/')
def home():
    # run face recognition
    run_recognition()

    return "RUNNING FACE RECOGNITION..."

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/register-submit', methods=['POST'])
def register_submit():
    image = request.files['image']
    firstname = request.form['firstname']
    lastname = request.form['lastname']

    # remove spaces before and after strings
    firstname = firstname.strip()
    lastname = lastname.strip()

    # fix capitalizations for fullname
    fullname = (f'{firstname} {lastname}').title()

    # prepare image filename with JPG extension
    image_filename = fullname + '.jpg'

    # does the image filename exist?
    if image_filename in os.listdir(PATH):
        return 'USER IS ALREADY REGISTERED.'
    else:
        # save image
        if image.filename != '':
            image.save(os.path.join(PATH, image_filename))
            image.stream.seek(0)

    return 'USER HAS BEEN REGISTERED SUCCESSFULLY'

@app.route('/unregister')
def unregister():
    # get all fullnames
    fullnames = []
    for image_filename in os.listdir(PATH):
        fullname, extension = splitext(image_filename)
        fullnames.append(fullname)

    return render_template("unregister.html", fullnames=fullnames)

@app.route('/unregister_submit', methods=['POST'])
def unregister_submit():
    fullname = request.form['fullname']

    # prepare image filename with JPG extension
    image_filename = fullname + '.jpg'

    # delete
    if image_filename in os.listdir(PATH):
        os.remove(os.path.join(PATH, image_filename))

    return 'USER HAS BEEN DELETED'


