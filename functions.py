import cv2 as cv
import base64
import numpy as np
import string
from database import get_user_by_name


def readb64(uri):
    encoded_data = uri.split(',')[1]
    nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
    img = cv.imdecode(nparr, cv.IMREAD_COLOR)
    return img


def allowed_info(username, psw, rpsw):
    if get_user_by_name(username) is not None:
        return "That username is already taken"
    if psw != rpsw:
        return "Passwords don't match"
    if len(psw) < 8:
        return "Password should be at least 8 characters"
    allowed = string.ascii_letters + string.digits + string.punctuation
    for letter in psw:
        if letter not in allowed:
            return "Information can only contain Alphanumeric characters"
    for letter in username:
        if letter not in allowed:
            return "Information can only contain Alphanumeric characters"
    return True


def allowed_question(title, details):
    allowed = string.ascii_letters + string.digits + string.punctuation + string.whitespace
    for letter in title:
        if letter not in allowed:
            print(letter)
            return "Title can only contain Alphanumeric characters"
    for letter in details:
        if letter not in allowed:
            return "Details can only contain Alphanumeric characters"
    return True


def correct_info(name, psw):
    user = get_user_by_name(name)
    if user is None or user.password != psw:
        return "Username and/or Password invalid"
    return True
