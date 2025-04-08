import logging
import mlflow
import os

import pickle
import yaml
import os
import mlflow
import logging
from urllib.parse import urlparse
from dotenv import load_dotenv
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from mlflow.models import infer_signature

from src.data_prep.preparation import preprocess
from src.data_prep.data_split import split_data

load_dotenv(override=True)
# mlflow_uri = os.getenv('MLFLOW_TRACKING_URI')

## Load the parameters from params.yaml
params=yaml.safe_load(open("configs/params.yaml"))["train"]

def train_model():
    # Run preprocess in a separate thread
    df_processed = preprocess()
    
    # Start an experiment
    experiment_name = "promo_sales_predictor"
    mlflow.set_experiment(experiment_name)
    mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "/app/mlruns"))

    logging.info("START TRAINING")

    # with mlflow.start_run():
    #     run_name = mlflow.active_run().info.run_name
    #     experiment_id = mlflow.active_run().info.experiment_id
        
    #     logging.info(f"Experiment Name: {experiment_name}")
    #     logging.info(f"Run Name: {run_name}")
    #     logging.info(f"Experiment ID: {experiment_id}")

    #     mlflow.log_metric("example", 123)

    ## start the MLFLOW run
    with mlflow.start_run():
        # Log the name of the experiment and the run
        run_name = mlflow.active_run().info.run_name
        experiment_id = mlflow.active_run().info.experiment_id
        
        logging.info(f"Experiment Name: {experiment_name}")
        logging.info(f"Run Name: {run_name}")
        logging.info(f"Experiment ID: {experiment_id}")

        # #split the dataset into training and test sets
        train_df_lag_clean, test_df_lag_clean = split_data(df_prep_clean=df_processed)
        # We convert the data in the required format for the model (label y and features x)
        y_train, X_train = train_df_lag_clean['UnitSales'], train_df_lag_clean.drop(columns=['UnitSales'])
        y_test, X_test = test_df_lag_clean['UnitSales'], test_df_lag_clean.drop(columns=['UnitSales'])
        
        signature=infer_signature(X_train,y_train)

        # set model settings
        rfr = RandomForestRegressor(
            n_estimators=params["n_estimators"], max_features=round(len(X_train.columns)/3), max_depth=len(X_train.columns),
        )
        
        logging.info(f"Fitting random forest model")
        # Train the model. Takes a couple of minutes.
        logging.info("TRAINING")
        rf_model = rfr.fit(X_train, y_train)
        logging.info("TRAINED")

        # ## predict and evaluate the model
        rf_y_pred = rf_model.predict(X_test)

        # and the MAE
        logging.info(mean_absolute_error(rf_y_pred, y_test))

        ## Log additional metrics
        mlflow.log_metric("mean_absolute_error", mean_absolute_error(rf_y_pred, y_test))

        tracking_url_type_store=urlparse(mlflow.get_tracking_uri()).scheme

        if tracking_url_type_store!='file':
            mlflow.sklearn.log_model(rf_model,"model",registered_model_name="Best Model")
        else:
            mlflow.sklearn.log_model(rf_model, "model",signature=signature)

        ## create the directory to save the model
        model_path = params["model"]
        os.makedirs(os.path.dirname(model_path),exist_ok=True)

        # Save the model to disk
        pickle.dump(rf_model, open(model_path, 'wb'))

        logging.info(f"Model saved to {model_path}")



