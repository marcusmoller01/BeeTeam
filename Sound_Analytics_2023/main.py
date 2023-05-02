import numpy as np
import librosa
import shutil
import os
from KNN_model import KNN_model
from Anomaly_model import anomaly_model
from OWL_communication import post_list_to_OWL
import time
import sys

"""
Reads the .wav-file and returns an tuple with the amplitudes values (np_arr) and sample-rate (int)
"""
def getAudioFile(path):
    audioFile, sample_rate = librosa.load(path, offset=1, duration=8)
    #audioFile = scipy.signal.savgol_filter(audioFile, 9, 8)
    return [audioFile, sample_rate]

"""
Function takes the files amplitude input as np array and returns the mfcc features as np array. 
"""
def mfcc(data):
    mfccs = np.mean(librosa.feature.mfcc(y=data[0], sr=data[1], n_mfcc=20).T, axis=0)
    return mfccs

"""Saves the analysed file to a separate folder based on the analysis
remove_file indicates if the file should be removed when saved.
"""
def save_in_folder(folder_name, file_name, file_path, remove_file):
    #print("The file is saved in folder " + folder_name)

    bee_folder_path = 'bees/'+ file_name
    bird_folder_path = 'birds/' + file_name
    anomalies_folder_path = 'anomalies/' + filename

    if folder_name == "bin lugnt":
        if remove_file:
            shutil.move(file_path, bee_folder_path)
        else:
            shutil.copy(file_path, bee_folder_path)

    elif folder_name == "Fågel":

        if remove_file:
            shutil.move(file_path, bird_folder_path)
        else:
            shutil.copy(file_path, bird_folder_path)

    elif folder_name == "Detected anomalies":
        if remove_file:
            shutil.move(file_path, anomalies_folder_path)
        else:
            shutil.copy(file_path, anomalies_folder_path)

"""Sends filename and class to defined beehive"""
def to_owl(KNN_class, filename, kupa_nr):
    kupor = ["sound_Apiary-LE_1","sound_Apiary-LE_2","sound_Apiary-LE_3","sound_Beehive-LN"]

    message_in_owl = "Anomaly detected in file " + filename + ", which has been classified as a " + KNN_class
    status = post_list_to_OWL(
        [kupor[kupa_nr]],
        [[filename,KNN_class[0]]],
        'auto_sound',
        True)

"""
Checks if there is a file in the folder to analyse
"""
def is_file_in_folder(folder_path):
    files = os.listdir(folder_path)
    if files == []:
        return False
    else:
        return True


"""
Initialise the input arguments

Run command syntax: 
run main.py folder_path remove_file kupa_nr 
Where: 
Folder_path = (string) path of folder on raspberry pi where the program reads the files 
remove_file = (boolean) True if the program should remove the read file from the folder otherwise False
kupa_nr = (int) number to indicate on which beehive the program is running, this to communicate correctly with OWL. 
0 = sound_Apiary-LE_1
1 = sound_Apiary-LE_2
2 = sound_Apiary-LE_3
3 = sound_Beehive-LN
"""
folder_path = str(sys.argv[1])
remove_file = eval(sys.argv[2])
kupa_nr = int(sys.argv[3])

file = None

while(True):
    if is_file_in_folder(folder_path):

        filename = os.listdir(folder_path)[0]
        file_path = folder_path + filename
        audio_data = getAudioFile(file_path)
        mfcc_data = mfcc(audio_data)

        KNN_class = KNN_model(mfcc_data)
        is_anomaly = anomaly_model(mfcc_data, filename)
        if is_anomaly:
            save_in_folder("Detected anomalies", filename, file_path, remove_file)
            to_owl(KNN_class, filename, kupa_nr)
        else:
            save_in_folder(KNN_class, filename, file_path, remove_file)

    time.sleep(5)