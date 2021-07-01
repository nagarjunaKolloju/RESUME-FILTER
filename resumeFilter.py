import nltk 
import os
from os import path
import shutil
from model import modelNB
from preProcessingData import pdfToText
from string import punctuation
import pandas as pd


def filterResume():
    jdFolder = "./jobReq"
    clientReq = ""
    for file in os.listdir(jdFolder):
        data_set = pd.read_excel(jdFolder + "\\" + file)
        clientReq += data_set['Job Title'][0].lower()

    src = "./resumes"
    dst = "./resumeFiltered"
    print(clientReq)
    for path in os.listdir(src):
        full_path = os.path.join(src, path)

        test_resume = pdfToText.convertPDFtoText(full_path)

        predicted = modelNB.predict(test_resume)
        predicted = ' '.join([str(elem) for elem in predicted]).lower()
        print("Predicted: " + predicted)
        print("required :" + clientReq)
        if (predicted == clientReq):
            print("matched")
            shutil.copy(full_path, dst)
    return

#filterResume()








