from flask import render_template, url_for, flash, request, redirect, jsonify, send_file
from Main.forms import getCSV
from Main.extract import converter
from Main import app
from PIL import Image
import secrets, os
from werkzeug.utils import secure_filename
UPLOAD_FOLDER = 'uploads/'

@app.route('/home', methods=['GET', 'POST'])
def home():
    form = getCSV()
    if form.validate_on_submit():
        if form.picture.data:
            converter(form.picture.data)
            with open("table1.csv", "wb") as fp:
                fp.write(request.data)
    return render_template('home.html', form=form)




@app.route('/uploadfile', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print('no file')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print('no filename')
            return redirect(request.url)
        else:

            filename = secure_filename(file.filename)

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print(os.path.abspath(filename))
            print("saved file successfully")
            converter(filename)
            filename = filename[:-4]+'.csv'
      #send file name as parameter to downlad
            return redirect('/downloadfile/'+ filename)
    return render_template('upload.html')

@app.route("/downloadfile/<filename>", methods = ['GET'])
def download_file(filename):
    return render_template('download.html',value=filename)

@app.route('/return-files/<filename>')
def return_files_tut(filename):
    print('hellooooo')
    filepath = os.path.join(os.getcwd(),'CSVs/'+filename)
    print(filepath)
    return send_file(filepath, as_attachment=True, attachment_filename='')