from sklearn.ensemble import IsolationForest
import numpy as np
import pandas as pd
import joblib


def anomaly_model(file_features, filename):
    anomaly_data = joblib.load('anomaly_model_data.pkl')
    # Train the Isolation Forest model
    clf = IsolationForest()
    clf.fit(np.vstack(anomaly_data['file_data']))
    #Update the rolling data
    anomaly_data = anomaly_data.drop(index=anomaly_data.index[-1])
    new_entry = pd.DataFrame({'file_id': filename, 'file_data': [file_features]})
    anomaly_data = pd.concat([new_entry, anomaly_data]).reset_index(drop=True)
    joblib.dump(anomaly_data, "anomaly_model_data.pkl")
    # Predict if the audio file is an outlier or not
    prediction = clf.predict([file_features])

    if prediction == -1:
        return True
    else:
        return False