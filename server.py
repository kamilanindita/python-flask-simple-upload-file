import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from os.path import join, dirname, realpath


UPLOAD_FOLDER = join(dirname(realpath(__file__)), "files/uploads")
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'} #file yang di izinkan


app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024 #max 2 mb


def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def allowed_filesize(filesize):
    if int(filesize) <= app.config["MAX_CONTENT_LENGTH"]:
        return True
    else:
        return False

@app.route("/")
def index():
    title="Index"
    return render_template("index.html",title=title)

@app.route("/upload")
def upload():
    title="Upload"
    return render_template("upload.html",title=title)

@app.route("/upload/proses", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        #cek ukuran file
        if "filesize" in request.cookies:
            if not allowed_filesize(request.cookies["filesize"]):
                print("ukuran file terlalu besar")
                return redirect(request.url)

            #jika tidak ada file request
            if 'file' not in request.files:
                print("tidak ada file request")
                return redirect(request.url)

            #jika ada file request
            file = request.files["file"]

            # jika file kosong
            if file.filename == "":
                print("tidak ada file yang dipilih")
                return redirect(request.url)
            #jika file ada cek apakah di ijikan
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                return redirect(url_for("index"))

        

if __name__ == '__main__':
    app.run(debug=True)
