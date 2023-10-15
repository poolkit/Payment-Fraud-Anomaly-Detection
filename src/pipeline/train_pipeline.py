import numpy as np
from src.utils import evaluate, save_object
from src.logger import logging
from src.exception import CustomException
from src.components.data_ingestion import DataLoader
from src.components.data_transformation import GetXy, TimestampTransformer, InteractionTransformer, CubeRootTransformer
from src.components.data_transformation import TargetEncoder, ColumnDropper
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import IsolationForest
from pathlib import Path

def model_trainer_pipeline():
    filepath = Path("data/original/training_data.csv")

    data_loader = DataLoader(filepath)
    df = data_loader.load_data()
    train, test = data_loader.split_data(df)

    X_train, y_train, X_test, y_test = GetXy(train, test)

    dropping_columns = ['Transaction_Id', 'Time_step', 'Sender_lob']
    timestamp_columns = ['Time_step']
    target_encoding_columns = ['Sender_Id', 'Sender_Account', 'Sender_Country', 'Bene_Id', 'Bene_Account', 'Bene_Country']
    cube_root = ['USD_amount', 'Amount_Mean']

    numerical_columns = ['Sender_Id', 'Sender_Account', 'Sender_Country', 'Sender_Sector',
        'Bene_Id', 'Bene_Account', 'Bene_Country', 'USD_amount', 'DaySin', 'DayCos', 'HourSin', 'HourCos', 'DoWSin',
        'DoWCos', 'Interaction_Frequency', 'Amount_Mean']

    categorical_columns = ['Transaction_Type']

    feature_extraction_pipeline = Pipeline(
        steps = [
            ('target_encoder', TargetEncoder(target_encoding_columns)),
            ('time_extractor', TimestampTransformer(timestamp_columns)),
            ('interaction', InteractionTransformer()),
            ('cube_root', CubeRootTransformer(cube_root)),
            ('column_dropper', ColumnDropper(dropping_columns))
            ]
        )

    preprocessor = ColumnTransformer(
        [
            ('one_hot_encoder', OneHotEncoder(sparse=False, handle_unknown='ignore'), categorical_columns),
            ('scaler', StandardScaler(), numerical_columns)
        ],
        remainder = 'passthrough'
    )

    model_pipeline = Pipeline(
        steps = [
            ('feature_extraction', feature_extraction_pipeline),
            ('pre_process', preprocessor),
            ('isolation_forest', IsolationForest(contamination=0.25))
        ]
    )

    logging.info("Fitting the model pipeline...")

    try:
        model_pipeline.fit(X_train, y_train)
        logging.info("Isolation forest model fitted.")

    except Exception as e:
        logging.error(CustomException(e))
        raise e

    logging.info("Evaluating the model...")

    try:
        anomaly_score = model_pipeline.predict(X_test)
        y_pred = np.where(anomaly_score==1, 0, 1)
        recall = evaluate(y_test, y_pred)
        print(f"Recall : {recall}")

    except Exception as e:
        logging.error(CustomException(e))
        raise e

    return model_pipeline

if __name__=="__main__":
    model_pipeline = model_trainer_pipeline()
    save_object('artifacts/model_pipeline.pkl', model_pipeline)
    logging.info("Model saved.")