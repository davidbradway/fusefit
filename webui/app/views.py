import os
# We'll render HTML templates and access data sent by POST
# using the request object from flask. Redirect and url_for
# will be used to redirect the user once the upload is done
# and send_from_directory will help us to send/show on the
# browser the file that the user just uploaded
from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory
from app import app
from werkzeug.utils import secure_filename

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


# This route will show a form to perform an AJAX request
# jQuery is loaded to execute the request and update the
# value of the operation
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():
    # check if the post request has the file part
    if 'filewohr' not in request.files or 'filewhr' not in request.files:
        flash('No file part')
        return redirect(request.url)
    # Get the name of the uploaded file
    filewohr = request.files['filewohr']
    filewhr = request.files['filewhr']
    # if user does not select file, browser also
    # submit a empty part without filename
    if filewohr.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if filewhr.filename == '':
        flash('No selected file')
        return redirect(request.url)
    # Check if the file is one of the allowed types/extensions
    if filewohr and allowed_file(filewohr.filename):
        # Make the filename safe, remove unsupported chars
        filenamewohr = secure_filename(filewohr.filename)
        # Move the file form the temporal folder to
        # the upload folder we setup
        filewohr.save(os.path.join(app.config['UPLOAD_FOLDER'], filenamewohr))
        # Redirect the user to the uploaded_file route, which
        # will basicaly show on the browser the uploaded file
        if filewhr and allowed_file(filewhr.filename):
            # Make the filename safe, remove unsupported chars
            filenamewhr = secure_filename(filewhr.filename)
            # Move the file form the temporal folder to
            # the upload folder we setup
            filewhr.save(os.path.join(app.config['UPLOAD_FOLDER'], filenamewhr))
            # Redirect the user to the uploaded_file route, which
            # will basicaly show on the browser the uploaded file
        return redirect(url_for('uploaded_file',
                                filenamewohr=filenamewohr,
                                filenamewhr=filenamewhr))

# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
@app.route('/uploads/<filenamewohr>/<filenamewhr>')
def uploaded_file(filenamewohr,filenamewhr):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filenamewohr,filenamewhr)
    # return render_template('file.html',folder = app.config['UPLOAD_FOLDER'], file = filename)
