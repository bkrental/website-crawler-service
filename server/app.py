from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
from flask_restful import Api, Resource
import prediction
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
cors = CORS(app)
api = Api(app)

current_env = os.getenv("FLASK_ENV", "production")  # Default to 'production' if not set
print(current_env)
print(app.config["DEBUG"])


class CheckHealth(Resource):
    def get(self):
        return {"status": "ok"}


class PricePrediction(Resource):
    def post(self):
        data = request.get_json()

        prediction_result = prediction.predict_price(data)
        return jsonify(prediction_result)


api.add_resource(CheckHealth, "/")
api.add_resource(PricePrediction, "/predict_price")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run()
