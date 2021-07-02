#
#@KEVIN DataBase Module
#
from flask import Flask
from app import  db,ma
from marshmallow import Schema, fields, pre_load, validate,ValidationError
from datetime import datetime



def must_not_be_blank(data):
    if not data:
        raise ValidationError("Data not provided.")
    


class UploadSchema(ma.Schema):
    id = fields.Integer()
    country = fields.String(required=True,validate=must_not_be_blank)
    state = fields.String(required=True,validate=must_not_be_blank)
    city = fields.String(required=True,validate=must_not_be_blank)


  

     


