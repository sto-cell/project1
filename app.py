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
gmailsdb = db['gmail']

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
@app.route("/registor", methods=["GET", "POST"])

def registor():
    if request.method=="POST":
        global userid,userpass
        
        userid=request.form['id']
        userpass=request.form['pass']
        repass=request.form['repass']
        if userpass==repass:
            name = collection.find_one({'id': userid})
            if name == None:
                    collection.insert_one({"id": userid,"pass": userpass,"data": []})
                    return redirect(url_for('dashboard'))
            else:
                return render_template('error.html')
        else:

            return render_template('error.html')
    else:
        return render_template('registration.html')

def get_drive_service(credentials):
    creds = None
    if os.path.exists(f'{credentials}_token.json'):
        creds = Credentials.from_authorized_user_file(f'{credentials}_token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(f'{credentials}.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open(f'{credentials}_token.json', 'w') as token:
            token.write(creds.to_json())
    return build('drive', 'v3', credentials=creds)

def get_drive_space(gmail):
    service = get_drive_service(gmail)
    about = service.about().get(fields="storageQuota").execute()
    quota = about.get('storageQuota', {})
    
    used = int(quota.get('usage', 0))
    total = int(quota.get('limit', 0))
    free = total - used
    print(f"size is {used}")
    def format_bytes(size):
        
        # Convert bytes to human-readable format
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} PB"
    

    return {
        'used': format_bytes(used),
        'total': format_bytes(total),
        'free': format_bytes(free)
    }
def get_drive_space_num(gmail):
    service = get_drive_service(gmail)
    about = service.about().get(fields="storageQuota").execute()
    quota = about.get('storageQuota', {})
    
    used = int(quota.get('usage', 0))
    total = int(quota.get('limit', 0))
    free = total - used
    print(f"size is {used}")
    

    return {
        'used': used,
        'total': total,
        'free': free
    }

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    
    new_data = collection.find_one({"id": userid,"pass":userpass})
    
    if len(new_data['data'])==0:
        mails=gmailsdb.find_one({'space':{'$lt':14.8*1024*1024*1024}})
        mails['users'].append(userid)
        new_data['data'].append({'gmail':mails['id'],"fileids":[]})
        service = get_drive_service(mails['id'])
        gmailsdb.update_one({'id':mails['id'] }, {'$set': mails})
        collection.update_one({'id':userid }, {'$set': new_data})

    if request.method == 'POST':
        file = request.files['file'] 
        if file:
            new_data = collection.find_one({"id": userid,"pass":userpass})
            count=0
            for i in new_data['data']:
                space_check = get_drive_space_num(i['gmail'])
                check=14.8*1024*1024*1024
                if space_check['used']<check:#14.5*1024*1024*1024
                    break
                count+=1
            gmail= i['gmail']
            service = get_drive_service(gmail)
            path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(path)
            # Use MediaFileUpload and create file
            media = MediaFileUpload(path, resumable=True)
            request_drive = service.files().create(body={'name': file.filename}, media_body=media)
            print(service.files().create(body={'name': file.filename}, media_body=media, fields='id').execute().get('id'))
            new_data = collection.find_one({"id": userid,"pass":userpass})

            new_data['data'][count]['fileids'].append(service.files().create(body={'name': file.filename}, media_body=media, fields='id').execute().get('id'))
            result = collection.update_one({'id': userid}, {'$set': new_data})
            new_data = gmailsdb.find_one({"id": gmail})
            if new_data == None:
                gmailsdb.insert_one({'id':gmail,'fileids':[],'space':'','users':[]})
                new_data = gmailsdb.find_one({"id": gmail})
            new_data['fileids'].append(service.files().create(body={'name': file.filename}, media_body=media, fields='id').execute().get('id'))
            if userid in new_data['users']:
                print("")

            else:
                new_data['users'].append(userid)

            gmailsdb.update_one({'id':gmail }, {'$set': new_data})

            print(new_data)
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
            space=get_drive_space_num(gmail)
            new_data['space']=space['used']
            gmailsdb.update_one({'id':gmail }, {'$set': new_data})
            return redirect(url_for('dashboard'))

    files=[]
    data=collection.find_one({"id": userid,"pass":userpass})
    data2=data['data']
    for j in data2:
        service = get_drive_service(j['gmail'])
        for i in j['fileids']:
            files2=service.files().get(fileId=i, fields='id, name').execute()
            files.append(files2)
    # results = service.files().list(pageSize=10, fields="files(id, name)").execute()
    # files = results.get('files', [])
    space_info = get_drive_space('harrydie9831@gmail.com')
    return render_template('index.html', files=files,id=userid,space=space_info)
@app.route('/download/<file_id>')
def download_file(file_id):
    service = get_drive_service('harrydie9831@gmail.com')
    data=collection.find_one({"id": userid,"pass":userpass})
    data2=data['data']
    for j in data2:
        service = get_drive_service(j['gmail'])
        for i in j['fileids']:
            if file_id==i:
                file_metadata = service.files().get(fileId=file_id, fields='name').execute()
                filename2 = file_metadata.get('name')
                request_drive = service.files().get_media(fileId=file_id)
                break
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
    data=collection.find_one({"id": userid,"pass":userpass})
    data2=data['data']
    for j in data2:
        service = get_drive_service(j['gmail'])
        for i in j['fileids']:
            if file_id==i:
                service.files().delete(fileId=file_id).execute()
                #collection.update_one({"data": {"$elemMatch": {"fileids": "1KV3MQFULuiKuZxkmjbowkQ9pjotRQKEA"}}},{'$pull': {"data": {"$elemMatch": {"fileids": "1KV3MQFULuiKuZxkmjbowkQ9pjotRQKEA"}}}})
                
                collection.update_one({'id': userid, 'pass': userpass, 'data.gmail': j['gmail']},{'$pull': {'data.$.fileids': i}})
                data = gmailsdb.find_one({'id':j['gmail']})
                space=get_drive_space_num(j['gmail'])
                data['space']= space['used']
                gmailsdb.update_one({'id':j['gmail']},{'$set':data})
                break
    try:
        
        flash('File deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting file: {e}', 'danger')
    return redirect(url_for('dashboard' ))
    
if __name__ == '__main__':

    app.run(debug=True,host='0.0.0.0')
