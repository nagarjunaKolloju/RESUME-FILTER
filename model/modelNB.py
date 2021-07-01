import pandas as pd
import nltk
import string
from wordcloud import STOPWORDS
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.svm import SVC
pd.options.mode.chained_assignment = None 

df = pd.read_csv('./dataSet/clean_data.csv')
df = df.drop(['Resume'],axis=1)
df.rename(columns={'newer_res':'Resume'},inplace=True)
resume_punc = df["Resume"].copy(deep  = True)

def rem_punc(s):
    punc = string.punctuation
    return [i for i in s if i not in punc]

# Remove punctaution for further processing
for ind,i in enumerate(df.itertuples()):
    token = nltk.word_tokenize(i[4])
    #print(token)
    df["Resume"][ind] = " ".join(rem_punc(token))


def rem_punc(s):
    punc = string.punctuation
    return [i for i in s if i not in punc]

def rem_sw(s):
    sw = set(STOPWORDS)
    return [i for i in s if i not in sw]

def preprocess(eval_res):
    try:
        eval_res = eval(eval_res).decode()
    except:
        pass
    eval_res = eval_res.encode("ASCII","ignore").decode()
    length = len(eval_res)
    eval_res = " ".join(eval_res.split("\n"))
    token = rem_sw(nltk.word_tokenize(eval_res)) #Removing punctaution later since we need punctaution for sentence tokenization
    eval_res = " ".join(token).lower()
    return eval_res

# Cleaning data and adding in ID for category
col = ['Category', 'Resume']
df = df[col]
df = df[pd.notnull(df['Resume'])]
df.columns = ['Category', 'Resume']
df['category_id'] = df['Category'].factorize()[0]
category_id_df = df[['Category', 'category_id']].drop_duplicates().sort_values('category_id')
category_to_id = dict(category_id_df.values)
id_to_category = dict(category_id_df[['category_id', 'Category']].values)


res_train, res_test, cat_train, cat_test=  train_test_split(df['Resume'], df['Category'], test_size=0.2, random_state=10)

vectorizer= CountVectorizer()
res_counts= vectorizer.fit_transform(res_train)

tfidf= TfidfTransformer()
res_tfidf= tfidf.fit_transform(res_counts)


classifier= SVC(kernel='linear')
classifier.fit(res_counts, cat_train)

def predict(test_resume):
    return classifier.predict(vectorizer.transform([test_resume]))
