import os
from flask import Flask,Blueprint
from flask_restful import reqparse, abort, Api, Resource

from app.auth.controller.Auth import *
app_service = Blueprint('api', __name__)
api = Api(app_service)


##
## Actually setup the Api resource routing here
##



##
## Other endpoint resource routing here
##

api.add_resource(VideoResource, '/v1/compressor/video')
api.add_resource(ImageResource, '/v1/compressor/image')



