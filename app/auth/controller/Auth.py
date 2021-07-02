#
#@KELVIN Authentication module for registartion , login, validation , splashscreen, token Resend 
#
from flask import request,json, jsonify,make_response,send_file
from flask_restful import Resource
from flask import Flask
import os,subprocess
import urllib.request,uuid
from werkzeug.utils import secure_filename
from datetime import datetime as datetimer ,date
import PIL
from PIL import Image
import math

UPLOAD_FOLDER = './app/static/uploads/videos'

UPLOAD_FOLDER_IMAGE = './app/static/uploads/images'

ALLOWED_VIDEO_EXTENSIONS = set(['mov','mp4','wmv','flv'])
ALLOWED_IMAGE_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

width=2666
heigth =3332

 
def allowed_file_video(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_VIDEO_EXTENSIONS

def allowed_file_image(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS


class VideoResource(Resource):

    def get(self):
       return ""

    def post(self):

        if 'files[]' not in request.files:
            resp = jsonify({'message' : 'No file part in the request'})
            resp.status_code = 400
            return resp

        files = request.files.getlist('files[]')
        errors = {}
        success = False
        unique_str= uuid.uuid1()
        for file in files:      
            if file and allowed_file_video(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                success = True
            else:
                errors[file.filename] = 'File type is not allowed'

        if success and errors:
            errors['message'] = 'File(s) successfully uploaded'
            resp = jsonify(errors)
            resp.status_code = 500
            return resp
        if success:
        # if successfully upload start compressor
            readPath="./app/static/uploads/videos/"+filename
            
            # get extension
            file_extension = os.path.splitext(readPath)[-1].lower()
            writePath="./app/static/uploads/videos/"+str(unique_str)+"_resized"+file_extension
            subprocess.run("ffmpeg -i " + readPath.replace(" ","\\ ") + " -vcodec libx264 -crf 35 " + writePath.replace(" ","\\ "), shell=True)
            #GET THE COMPRESS FILE
            getPath="static/uploads/videos/"+str(unique_str)+"_resized"+file_extension
            resp = jsonify({'message' : 'Files successfully uploaded', 'name':filename,'file_extension':file_extension})
            resp.status_code = 201
            if os.path.exists(readPath):
                os.remove(readPath)
            else:
                print("The file does not exist")

            return send_file(getPath, as_attachment=True)
        else:
            resp = jsonify(errors)
            resp.status_code = 500
            return resp




class ImageResource(Resource):

    def get(self):
        
        return ""

    def post(self):

        if 'files[]' not in request.files:
            resp = jsonify({'message' : 'No file part in the request'})
            resp.status_code = 400
            return resp

        files = request.files.getlist('files[]')
        errors = {}
        success = False
        unique_str= uuid.uuid1()
        for file in files:      
            if file and allowed_file_image(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER_IMAGE, filename))
                file.seek(0, 2)
                file_length = file.tell()
                print(file_length)
                success = True
            else:
                errors[file.filename] = 'File type is not allowed'

        if success and errors:
            errors['message'] = 'File(s) successfully uploaded'
            resp = jsonify(errors)
            resp.status_code = 500
            return resp

        #Validate Size 
        if file_length < 999999:
            SizeCheck=False
        else:
            SizeCheck=True

        if SizeCheck:
        # if successfully upload start compressor
            readPath="./app/static/uploads/images/"+filename
            
            # get extension
            file_extension = os.path.splitext(readPath)[-1].lower()
            writePath="./app/static/uploads/images/"+str(unique_str)+"_resized"+file_extension
            img = Image.open(readPath)
            base_width =  int(float(img.size[0])/1.4)
            width_percent = (base_width / float(img.size[0]))
            hsize = int((float(img.size[1]) * float(width_percent)))
            # print(img.size[0])
            img = img.resize((base_width, hsize),PIL.Image.ANTIALIAS)
            img.save(writePath,optimize=True,quality=40)
               #GET THE COMPRESS FILE
            getPath="static/uploads/images/"+str(unique_str)+"_resized"+file_extension
            resp = jsonify({'message' : 'Files successfully uploaded', 'name':filename,'file_extension':file_extension})
            resp.status_code = 201

            if os.path.exists(readPath):
                os.remove(readPath)
            else:
                print("The file does not exist")
           
            return send_file(getPath, as_attachment=True)
        else:
            #Return Same image without compressing 
             # get extension
            readPath="static/uploads/images/"+filename
            return send_file(readPath, as_attachment=True)

