from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request
from flask_pymongo import PyMongo
import urllib.parse
from io import BytesIO


SCOPES = ['https://www.googleapis.com/auth/drive.file']
app = Flask(__name__)
app.secret_key = 'd1088b5fb4504264963061ff88dfef5a'
username = urllib.parse.quote_plus('sftghsffth')

password = urllib.parse.quote_plus('giHkXMkhFVwBdfLb')

# Initialize MongoDB collections MongoDB Atlas connection string


app.config["MONGO_URI"] = f"mongodb+srv://{username}:{password}@cluster0.m8r2cjv.mongodb.net/dbname?retryWrites=true&w=majority"

mongo = PyMongo(app)

db = mongo.db

collection = db['drive']

collection2 = db['test3']

UPLOAD_FOLDER = 'uploads/'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

userid=""
userpass=""


if not os.path.exists(UPLOAD_FOLDER):

    os.makedirs(UPLOAD_FOLDER)

def split(st):
    ss = len(st)
    print(ss)
    com = False
    filen = ''  # Initialize the variable before use
    for i in range(ss):
        if st[i] == '.':
            com = True
        if com:
            filen += st[i]
    return(filen)
@app.route('/')
def home():
    return render_template('login.html')

@app.route("/login", methods=["GET", "POST"])

def login():
    global userid,userpass
    
    userid=request.form['id']
    userpass=request.form['pass']
    name = collection.find_one({'id': userid,'pass': userpass})
    if name :
        return redirect(url_for('dashboard'))

    else:

        return render_template('error.html')
def get_drive_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('henryrichar2@gmail.com.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('drive', 'v3', credentials=creds)

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    service = get_drive_service()

    if request.method == 'POST':
        file = request.files['file'] 
        if file:
            path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(path)
            # Use MediaFileUpload and create file
            media = MediaFileUpload(path, resumable=True)
            request_drive = service.files().create(body={'name': file.filename}, media_body=media)
            print(service.files().create(body={'name': file.filename}, media_body=media, fields='id').execute().get('id'))
            new_data = collection.find_one({"id": userid,"pass":userpass})
            new_data['fileids'].append(service.files().create(body={'name': file.filename}, media_body=media, fields='id').execute().get('id'))
            result = collection.update_one({'id': userid}, {'$set': new_data})
            response = None
            while response is None:
                status, response = request_drive.next_chunk()
    
            # Close the file used by MediaFileUpload
            if media._fd:
                media._fd.close()
    
            try:
                os.remove(path)
            except PermissionError:
                print(f"Still in use: {path}")
    
            return redirect(url_for('dashboard'))

    files=[]
    data=collection.find_one({"id": userid,"pass":userpass})
    data2=data['fileids']
    for i in data2:
        files2=service.files().get(fileId=i, fields='id, name').execute()
        files.append(files2)
    # results = service.files().list(pageSize=10, fields="files(id, name)").execute()
    # files = results.get('files', [])
    return render_template('index.html', files=files,id=userid)
@app.route('/download/<file_id>')
def download_file(file_id):
    service = get_drive_service()
    file_metadata = service.files().get(fileId=file_id, fields='name').execute()
    filename2 = file_metadata.get('name')
    request_drive = service.files().get_media(fileId=file_id)
    fh = BytesIO()
    print(request_drive)
    downloader = MediaIoBaseDownload(fh, request_drive)

    done = False
    while not done:
        status, done = downloader.next_chunk()
    fh.seek(0)
    filename=split(file_id)
    print(filename)
    return send_file(fh, as_attachment=True, download_name=f"{filename2}")
@app.route('/delete/<file_id>')
def delete_file(file_id):
    service = get_drive_service()
    try:
        service.files().delete(fileId=file_id).execute()
        data= collection.update_one({'fileids': file_id},{'$pull': {'fileids': file_id}})
        flash('File deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting file: {e}', 'danger')
    return redirect(url_for('dashboard' ,id=userid))
    
if __name__ == '__main__':

    app.run(debug=True,host='0.0.0.0')