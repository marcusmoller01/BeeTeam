import joblib

def KNN_model(file_features):
    knn = joblib.load('KNN_sound_model.pkl')
    y_pred = knn.predict([file_features])
    return y_pred