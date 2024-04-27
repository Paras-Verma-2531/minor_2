import os
from flask import Flask, request, redirect, url_for, render_template, send_file
from werkzeug.utils import secure_filename
import DH
import pickle
import random

UPLOAD_FOLDER = './media/text-files/'
UPLOAD_KEY = './media/public-keys/'
ALLOWED_EXTENSIONS = {'txt'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# PAGE REDIRECTS
def post_upload_redirect():
    return render_template('post-upload.html')

@app.route('/register')
def call_page_register_user():
    return render_template('register.html')

@app.route('/home')
def back_home():
    return render_template('index.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload-file')
def call_page_upload():
    return render_template('upload.html')

# DOWNLOAD KEY-FILE
@app.route('/public-key-directory/retrieve/key/<username>')
def download_public_key(username):
    for root, dirs, files in os.walk('./media/public-keys/'):
        for file in files:
            user_info = file.split('-')
            if user_info[0] == username:
                filename = os.path.join(UPLOAD_KEY, file)
                return send_file(filename, as_attachment=True)

@app.route('/file-directory/retrieve/file/<filename>')
def download_file(filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.isfile(filepath):
        return send_file(filepath, as_attachment=True)
    else:
        return render_template('file-list.html', msg='An issue encountered, our team is working on that')

# BUILD - DISPLAY FILE - KEY DIRECTORY
@app.route('/public-key-directory/')
def downloads_pk():
    username = []
    if os.path.isfile("./media/database/database_1.pickle"):
        with open("./media/database/database_1.pickle", "rb") as pickleObj:
            username = pickle.load(pickleObj)
    if len(username) == 0:
        return render_template('public-key-list.html', msg='Aww snap! No public key found in the database')
    else:
        return render_template('public-key-list.html', msg='', itr=0, length=len(username), directory=username)

@app.route('/file-directory/')
def download_f():
    for root, dirs, files in os.walk(UPLOAD_FOLDER):
        if len(files) == 0:
            return render_template('file-list.html', msg='Aww snap! No file found in directory')
        else:
            return render_template('file-list.html', msg='', itr=0, length=len(files), list=files)

# UPLOAD ENCRYPTED FILE
@app.route('/data', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return post_upload_redirect()
        return 'Invalid File Format!'

# REGISTER UNIQUE USERNAME AND GENERATE PUBLIC KEY WITH FILE
@app.route('/register-new-user', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        privatekeylist = []
        usernamelist = []
        if os.path.isfile("./media/database/database.pickle"):
            with open("./media/database/database.pickle", "rb") as pickleObj:
                privatekeylist = pickle.load(pickleObj)
        if os.path.isfile("./media/database/database_1.pickle"):
            with open("./media/database/database_1.pickle", "rb") as pickleObj:
                usernamelist = pickle.load(pickleObj)
        username = request.form['username']
        if username in usernamelist:
            return render_template('register.html', name='Username already exists')
        firstname = request.form['first-name']
        secondname = request.form['last-name']
        pin = random.randint(1, 128) % 64
        privatekey = DH.generate_private_key(pin)
        while privatekey in privatekeylist:
            pin = random.randint(1, 128) % 64
            privatekey = DH.generate_private_key(pin)
        privatekeylist.append(str(privatekey))
        usernamelist.append(username)
        with open("./media/database/database.pickle", "wb") as pickleObj:
            pickle.dump(privatekeylist, pickleObj)
        with open("./media/database/database_1.pickle", "wb") as pickleObj:
            pickle.dump(usernamelist, pickleObj)
        publickey = DH.generate_public_key(privatekey)
        filename = os.path.join(UPLOAD_KEY, f"{username}-{secondname.upper()}{firstname.lower()}-PublicKey.pem")
        with open(filename, "w", encoding='utf-8') as fileObject:
            fileObject.write(str(publickey))
        return render_template('key-display.html', privatekey=str(privatekey))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
