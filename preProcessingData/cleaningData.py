import pandas as pd 
import numpy as np 
import re
import nltk
import string
from wordcloud import WordCloud,STOPWORDS

df_orig = pd.read_csv("./dataSet/resume_dataset.csv")
df = df_orig.copy(deep = True)

length = df["Resume"].shape
length

df["res_new"] = df["Resume"]
eval_res = df["res_new"].copy(deep=True)

def rem_punc(s):
    punc = string.punctuation
    return [i for i in s if i not in punc]

def rem_sw(s):
    sw = set(STOPWORDS)
    return [i for i in s if i not in sw]

j=0
i=0
l=[]
for i in range(length[0]):
    try:
        eval_res[i] = eval(eval_res[i]).decode()
    except:
        l.append(i)
        pass

df["res_new"] = eval_res
df = df.drop(l,axis=0)
df = df.reset_index(drop = True)

# Records with missing data ie. resumes must be dealt with. We simply delete these columns.
df = df[["ID","Category","res_new","Resume"]]
df['res_new'].replace('', np.nan, inplace=True)
df.dropna(subset=['res_new'], inplace=True)
df = df.reset_index(drop = True)

length = df["res_new"].shape
eval_res = df["res_new"].copy(deep=True)

for i in range(length[0]):
    eval_res[i] = " ".join(eval_res[i].split("\n"))
    token = rem_sw(nltk.word_tokenize(eval_res[i])) #Removing punctaution later since we need punctaution for sentence tokenization
    eval_res[i] = " ".join(token).lower()
eval_res_backup  = eval_res.copy(deep = True)

for i in range(length[0]):
    eval_res[i] = (eval_res[i].encode("ASCII","ignore")).decode() #encoding the text to ascii.
eval_res.shape

df["res_new"] = eval_res

df_cols = ["ID","Category","res_new","Resume"]
df = df[df_cols]

# Details like email id, phone number, and noisy regions like censoring with 'x' could be tacked with some reglaur expressions since they seem to follow a pattern.
REGEX_SPACE = re.compile("[ ][ ]+")
REGEX_JUNK = re.compile("[^A-WX-wyz][xX][^A-WX-wyz]+[ ]*|[.\-\_][.\-\_]+")
REGEX_EMAIL = re.compile("[Xx]+[._]?[Xx]+.@.[Xx]+\.?[Xx]+")
REGEX_PNO = re.compile("[(][xX][xX][xX][)][xX][xX][xX][xX][xX][xX][xX]|[xX][xX][xX][xX][xX][xX][xX][xX][xX][xX]|[xX][xX][xX][\-][xX][xX][xX]+[-][xX][xX][xX]+")

df["newer_res"] = df["res_new"] 
for i,j in enumerate(df.itertuples()):
    strin = re.sub(REGEX_PNO,"",j[3])
    strin = re.sub(REGEX_EMAIL,"",strin)
    strin = re.sub(REGEX_SPACE,"",strin)
    strin  =re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]', '', strin)
    strin = re.sub(REGEX_JUNK, "" ,strin)
    df["newer_res"][i] = strin

df = df[["ID","Category","newer_res","Resume"]]

df = df[["ID","Category","newer_res","Resume"]]
df['newer_res'].replace('', np.nan, inplace=True)
df.dropna(subset=['newer_res'], inplace=True)
df = df.reset_index(drop = True)

df.to_csv("./dataSet/clean_data.csv")
print("Cleaned dataset written to cleaned_data.csv")


