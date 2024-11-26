from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################
@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################
@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500

######################################################################
# GET ALL PICTURES
######################################################################
def get_pictures():
    """Return the entire list of pictures"""
    return data

@app.route("/picture", methods=["GET"])
def list_pictures():
    """Route handler for retrieving pictures"""
    return jsonify(get_pictures()), 200

######################################################################
# GET A PICTURE
######################################################################
def get_picture_by_id(id):
    """Find and return a picture by its ID"""
    for picture in data:
        if picture['id'] == id:
            return picture
    return None

@app.route("/picture/<int:id>", methods=["GET"])
def retrieve_picture(id):
    """Route handler for retrieving a specific picture by ID"""
    picture = get_picture_by_id(id)
    if picture:
        return jsonify(picture), 200
    else:
        return {"message": "Picture not found"}, 404

######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    """Create a new picture"""
    picture = request.json
    
    # Check if picture is None or doesn't have an ID
    if not picture or 'id' not in picture:
        return {"Message": "Invalid picture data"}, 400
    
    # Check if picture with given ID already exists
    for existing_pic in data:
        if existing_pic['id'] == picture['id']:
            return {"Message": f"picture with id {picture['id']} already present"}, 302
    
    # Add new picture to the data list
    data.append(picture)
    return jsonify(picture), 201

######################################################################
# UPDATE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    """Update an existing picture"""
    picture = request.json
    
    # Find the picture with the given ID
    for idx, existing_pic in enumerate(data):
        if existing_pic['id'] == id:
            # Update the picture
            data[idx] = picture
            return jsonify(picture), 200
    
    # If no picture found, return 404
    return {"message": "Picture not found"}, 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    """Delete a picture by ID"""
    for idx, picture in enumerate(data):
        if picture['id'] == id:
            # Remove the picture from the list
            del data[idx]
            return "", 204
    
    # If no picture found, return 404
    return {"message": "Picture not found"}, 404