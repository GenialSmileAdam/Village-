from flask_jwt_extended import create_access_token, create_refresh_token
from flask import jsonify


class ResponseHelper():
    def __init__(self, data= None, message= "Success", status_code= 200,
                     add_access_token = False,
                     user= None):
        self.data = data
        self.message = "Success"
        self.status_code = status_code
        self.add_access_token= add_access_token
        self.user= user
        self.response = {
            "message": self.message,
                    "data":self.data,
        }

    def respond(self):
        if self.message == "Success":
            self.success_response()
        return jsonify(self.response), self.status_code




    def success_response(self):

        if self.add_access_token and self.user:

            access_token = create_access_token(self.user)
            refresh_token = create_refresh_token(self.user)

            self.response.update({
                "access_token": access_token,
                "refresh_token": refresh_token
            })

