import resumeFilter
from flask import Flask,flash,render_template,url_for,request,redirect,session
import os
import json
from core import printByRanks
from utils import file_utils
from constants import file_constants as cnst
import waitress

app = Flask(__name__)
app.secret_key = "secret key"
ALLOWED_EXTENSIONS = set(['pdf','xlsx'])
app.config['UPLOAD_FOLDER'] = cnst.UPLOAD_FOLDER
app.config['UPLOAD_FOLDER_JD_REQ'] = cnst.UPLOAD_FOLDER_JD_REQ

def allowed_file(filename):
   return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def uploader_form():
    return render_template('resume_loader.html')


@app.route('/failure')
def failure():
   return 'No files were selected'

@app.route('/success/<name>')
def success(name):
   return 'Files %s has been selected' %name

@app.route('/results')
def goHome():
    messages = request.args['messages']  
    messages = session['messages']  
    # session.clear()    
    result = json.loads(messages)
    print(result)
    return render_template("resume_results.html", result=result)

@app.route('/', methods=['POST', 'GET'])
def check_for_file():
    if request.method == 'POST':
        if 'reqFile' not in request.files:
           flash('Requirements document can not be empty')
           return redirect(request.url)
        if 'resume_files' not in request.files:
           flash('Select at least one resume File to proceed further')
           return redirect(request.url)
        file = request.files['reqFile']
        if file.filename == '':
           flash('Requirement document has not been selected')
           return redirect(request.url)
        resume_files = request.files.getlist("resume_files")
        if len(resume_files) == 0:
            flash('Select atleast one resume file to proceed further')
            return redirect(request.url)
        if ((file and allowed_file(file.filename)) and (len(resume_files) > 0)):
           filename = file.filename
           file.save(os.path.join(app.config['UPLOAD_FOLDER_JD_REQ'], filename))
           for resumefile in resume_files:
               filename = resumefile.filename
               resumefile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
           resumeFilter.filterResume()
           result = printByRanks()
           print("firstCheck :")
           for item in result :
               print(item)
           messages = json.dumps(result)
           session['messages'] = messages
           #oldPath = os.getcwd()
           resume =  "./resumes"
           resumeFinal =  "./resumeFiltered"
           jobDes =  "./jobReq"
           for path in os.listdir(resume):
               full_path = os.path.join(resume, path)
               file_utils.delete_file(full_path)
           for path in os.listdir(resumeFinal):
               full_path = os.path.join(resumeFinal, path)
               file_utils.delete_file(full_path)
           for path in os.listdir(jobDes):
               full_path = os.path.join(jobDes, path)
               file_utils.delete_file(full_path)
           i = 0
           for item in result:
              print(i)
              print(item[0])
              print(item[1])
              print(item[2])
              i += 1
    return redirect(url_for('.goHome', messages=messages))


if __name__ == "__main__":
    app.debug = False
    port = int(os.environ.get('PORT', 33507))
    waitress.serve(app, port=port)