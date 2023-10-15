import pandas as pd
import numpy as np
from pathlib import Path
from src.logger import logging
from src.exception import CustomException
from sklearn.model_selection import train_test_split

class DataLoader():
    def __init__(self, path:Path, train=True):
        self.path = path
        self.train = train

    def load_data(self):
        try:
            df = pd.read_csv(self.path)
        except Exception as e:
            logging.error(CustomException(e))
            raise e

        if self.train:
            assert all(df.columns == ['Time_step', 'Transaction_Id', 'Sender_Id', 'Sender_Account','Sender_Country', 
            'Sender_Sector', 'Sender_lob', 'Bene_Id', 'Bene_Account', 'Bene_Country', 'USD_amount', 'Label','Transaction_Type'])
        else:
            assert all(df.columns == ['Time_step', 'Transaction_Id', 'Sender_Id', 'Sender_Account','Sender_Country', 
            'Sender_Sector', 'Sender_lob', 'Bene_Id', 'Bene_Account', 'Bene_Country', 'USD_amount', 'Transaction_Type'])

        df = df[df.Transaction_Type.isin(['PAY-CHECK', 'MOVE-FUNDS', 'QUICK-PAYMENT', 'MAKE-PAYMENT'])]

        print(f"Shape of dataframe: {df.shape}")
        logging.info("Loaded the data successfully.")
        return df

    def split_data(self, df, test_size=0.2, random_state=42):
        try:
            train, test = train_test_split(df, test_size=test_size, random_state=random_state)
        except Exception as e:
            logging.error(CustomException(e))
            raise e

        print(f"Train shape: {train.shape}")
        print(f"Test shape: {test.shape}")

        logging.info("Splitting into train-test done.")
        return train, test


if __name__=="__main__":
    filepath = Path("data/original/training_data.csv")
    obj = DataLoader(filepath)
    x = obj.load_data()
    a,b = obj.split_data(x)
    print(a.head())