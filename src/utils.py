import pickle
import os
from sklearn.metrics import confusion_matrix, classification_report, recall_score
from src.logger import logging
from src.exception import CustomException

def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)

    except Exception as e:
        logging.error(CustomException(e))
        raise e

def load_object(file_path):
    try:
        with open(file_path, "rb") as file_obj:
            return pickle.load(file_obj)

    except Exception as e:
        logging.error(CustomException(e))
        raise e

def evaluate(y_test, y_pred):
    try:
        print(confusion_matrix(y_test, y_pred))
        print(classification_report(y_test, y_pred))
        recall = recall_score(y_test, y_pred)
        return recall
    except Exception as e:
        logging.error(CustomException(e))
        raise e