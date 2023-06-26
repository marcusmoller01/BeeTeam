import numpy as np
import librosa
import os
import pandas as pd

from joblib import dump, load

def getAudioFile(path):
    audioFile, sample_rate = librosa.load(path, offset=1, duration=8)
    #audioFile = scipy.signal.savgol_filter(audioFile, 9, 8)
    spectrum = np.abs(librosa.stft(audioFile))
    return [audioFile, spectrum, sample_rate]

def mfcc(data):
    mfccs = np.mean(librosa.feature.mfcc(y=data[0], sr=data[2], n_mfcc=20).T, axis=0)
    return mfccs

def save_in_folder(folder_name):
    print("The file is saved in folder " + folder_name)

def to_owl(KNN_class, filename, file):
    message_in_owl = "Anomaly detected in file" + filename + ", which has been classified as a " + KNN_class
    print(message_in_owl)


def create_dataframe_from_folder(folder_path):
    data = []
    files  = os.listdir(folder_path)
    files.sort(reverse=True)
    for i, filename in enumerate(files):
        if i > 50:
            break
        if filename == ".DS_Store":
            continue
        file_path = os.path.join(folder_path, filename)

        # gets the filedata
        rawFileData = getAudioFile(file_path)
        file_data = mfcc(rawFileData)

        data.append({'file_id': filename, 'file_data': file_data})
    df = pd.DataFrame(data)
    return df

"""
This script initialises the cache memory for the anomaly model, you choose a file folder (folder path) and it creates
dataframe and saves it as pickel file
"""
folder_path = '/Users/marcusmoller/Desktop/AudioFiles/good_bee_sound/Apiary_LE_2'

df =  create_dataframe_from_folder(folder_path)
dump(df, "anomaly_model_data.pkl")

#Create a cache set
cache = set()
dump(cache, "file_cache.pkl")
