import os
# We'll render HTML templates and access data sent by POST
# using the request object from flask. Redirect and url_for
# will be used to redirect the user once the upload is done
# and send_from_directory will help us to send/show on the
# browser the file that the user just uploaded
from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory
from app import app
from werkzeug.utils import secure_filename
import fusefit

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.route('/', methods=['GET','POST'])
@app.route('/index', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        # check if the post request has the file part
        filename = []
        for upfile in ['filewohr','filewhr']:
            if upfile not in request.files:
                flash('No file part')
                return redirect(request.url)
            # Get the name of the uploaded file
            file = request.files[upfile]
            # if user does not select file, browser also
            # submits a empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            # Check if the file is one of the allowed types/extensions
            if file and allowed_file(file.filename):
                # Make the filename safe, remove unsupported chars
                filename.append(secure_filename(file.filename))
                # Move the file form the temporary folder to the upload folder
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename[-1]))
            else:
                flash('Not allowed file')
                return redirect(request.url)
        outfilename = []
        outfilename = fusefit.mergeUploaded(app.config['UPLOAD_FOLDER'],filename)

        # Render the file template
        return render_template('file.html',
            folder = app.config['UPLOAD_FOLDER'],
            outfilename = outfilename,
            scroll = 'results')
    return render_template('index.html')
