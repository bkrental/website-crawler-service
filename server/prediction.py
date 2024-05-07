import pickle
import pandas as pd
from sklearn.preprocessing import LabelEncoder


def predict_price(data):
    model = pickle.load(open("../website_scraper/models/re_model.pkl", "rb"))
    encoders = pickle.load(open("../website_scraper/models/label_encoder.pkl", "rb"))
    print(f"In predict_price:\n {data}\n")

    if type(data) == dict:
        data = pd.DataFrame(data, index=[0])
        data["district"] = encoders["le_district"].transform(data["district"])
        print(data)
        data["province"] = encoders["le_province"].transform(data["province"])
        data["ward"] = encoders["le_ward"].transform(data["ward"])
        print(f"data after label encoding:\n{data}\n")

    print(f"model:{model}\n")
    prediction = model.predict(data)
    print(f"Prediction:\n{prediction}")
    return {"price": prediction[0]}
