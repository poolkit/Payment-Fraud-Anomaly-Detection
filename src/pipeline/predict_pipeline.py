import pandas as pd
from src.utils import load_object
from src.logger import logging
from src.exception import CustomException
from src.components.data_transformation import TimestampTransformer, InteractionTransformer, CubeRootTransformer

class PredictPipeline():
    def __init__(self, df):
        self.df = df

    def predict(self):
        model_pipeline = load_object("artifacts/model_pipeline.pkl")
        prediction = model_pipeline.predict(self.df)
        return prediction

if __name__=="__main__":
    data = {
    "Time_step": "07-11-2026  01:14:29",
    "Transaction_Id": "MAKE-PAYMENT-318236",
    "Sender_Id": "JPMC-CLIENT-318205",
    "Sender_Account": "ACCOUNT-318216",
    "Sender_Country": "USA",
    "Sender_Sector": 36226,
    "Sender_lob": "CCB",
    "Bene_Id": "JPMC-CLIENT-318207",
    "Bene_Account": "ACCOUNT-318219",
    "Bene_Country": "USA",
    "USD_amount": 574.44,
    "Transaction_Type": "MAKE-PAYMENT"
    }
    df = pd.DataFrame(data, index=[0])

    try:
        prediction_pipeline = PredictPipeline(df)
        prediction = prediction_pipeline.predict()
    except Exception as e:
        logging.error(CustomException(e))
        raise e

    if prediction == 1:
        print('Not Anomaly')
    else:
        print('Anomaly')