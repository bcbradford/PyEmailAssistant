''' Module used to wrap a machine learning model and its dataset preprocessing objects. '''

import pandas as pd
import numpy as np
from joblib import load
from torch import cuda
from pyemailassistant.errors import *

class Model:

    def __init__(self, config, logger):
        self._model_type = config["TYPE"]
        self._logger = logger
        self._obj_dict = self._init_obj_dict(config)

    def _init_obj_dict(self, config):
        self._logger.info("Initializing object dict.")

        try:
            obj_dict = {}
            for key, file in config["FILES"].items():
                obj_dict[key] = load(file)
            return obj_dict
        except Exception as e:
            desc = "An error occured while loading the model's training files."
            error = TrainingFileLoadError(desc, str(e))
            raise error

        self._logger.info("Object dict initialization complete.")

    def get_model_type(self):
        return self._model_type

    def predict(self, dataframe):
        self._logger.info("Making prediction")
        y = None

        try:
            dataframe = self._preprocess_data(dataframe)

            # set device to cpu if the user doesn't have a cuda device.
            if not cuda.is_available():
                model.set_params(tree_method="hist", predictor="cpu_predictor")

            model = self._obj_dict["MODEL_FILE"]
            y = model.predict(dataframe)
        except ModelPreprocessingError as e:
            raise e
        except Exception as e:
            desc = "An error was encountered during model prediction."
            error = ModelPredictionError(desc, str(e))
            raise error

        self._logger.info("Prediction complete.")
        return y

    def _preprocess_data(self, dataframe):
        self._logger.info("Preprocessing data.")

        categorical_cols = ["domain", "urls", "subject"]
        text_cols = ["body"]

        try:

            for col in categorical_cols:
                self._logger.info(f"Preprocessing {col}")
                encoder = self._obj_dict[f"{col.upper()}_ENCODER"]
                text = dataframe[col][0]

                text = text if text in encoder.classes_ else "unkown"
                encoded = encoder.transform([text])[0]

                dataframe[col] = encoded
        
            for col in text_cols:
                self._logger.info(f"Preprocessing {col}")
                vectorizer = self._obj_dict[f"{col.upper()}_VECTORIZER"]
                text_col = dataframe[col]

                encoded = vectorizer.transform(text_col)
                feature_cols = [f"{col}_{word}" for word in vectorizer.get_feature_names_out()]
                df_vectorized = pd.DataFrame(encoded.toarray(), columns=feature_cols)

                dataframe.drop(columns=[col], inplace=True)
                dataframe = pd.concat([dataframe, df_vectorized], axis=1)

            self._logger.info("Reordering columns")
            # reorder columns
            model = self._obj_dict["MODEL_FILE"]
            training_features = model.get_booster().feature_names
            dataframe = dataframe[training_features]

        except Exception as e:
            desc = "An error was encountered while preprocessing data"
            error = ModelPreprocessingError(desc, str(e))
            raise error

        self._logger.info("Preprocessing complete.")
        return dataframe

        
def init_model(config, logger):
    logger.info("Creating model.")
    model = Model(config, logger)
    logger.info("Model creation complete.")
    return model
