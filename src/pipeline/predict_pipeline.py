import pandas as pd
from src.utils import load_object
from src.logger import logging
from src.exception import CustomException
from src.components.data_transformation import TimestampTransformer, InteractionTransformer, CubeRootTransformer

class PredictPipeline():
    def __init__(self, data):
        try:
            assert list(data.keys()) == ['Time_step', 'Transaction_Id', 'Sender_Id', 'Sender_Account', 'Sender_Country', 'Sender_Sector', 
                                'Sender_lob', 'Bene_Id', 'Bene_Account', 'Bene_Country', 'USD_amount', 'Transaction_Type']
            self.df = pd.DataFrame(data, index=[0])
        
        except Exception as e:
            logging.error(CustomException(e))
            raise e

    def predict(self):
        model_pipeline = load_object("artifacts/model_pipeline.pkl")
        prediction = model_pipeline.predict(self.df)
        return prediction

if __name__=="__main__":
    data = {
    "Time_step": "26-01-2054  18:27:21",
    "Transaction_Id": "PAY-BILL-2143836",
    "Sender_Id": "JPMC-CLIENT-2143803",
    "Sender_Account": "ACCOUNT-2143814",
    "Sender_Country": "USA",
    "Sender_Sector": 7117,
    "Sender_lob": "CCB",
    "Bene_Id": "COMPANY-2143807",
    "Bene_Account": "ACCOUNT-2143812",
    "Bene_Country": "USA",
    "USD_amount": 853.77,
    "Transaction_Type": "MAKE-PAYMENT"
    }

    try:
        prediction_pipeline = PredictPipeline(data)
        prediction = prediction_pipeline.predict()
        logging.info("Prediction done")

    except Exception as e:
        logging.error(CustomException(e))
        raise e

    if prediction == 1:
        print('Not Anomaly')
    else:
        print('Anomaly')