import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn import metrics

df = pd.read_csv("en_docs_clean.csv")
y = df.party
X = df.text
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
print("\nX_train:\n")
print(X_train.head())
print(X_train.shape)

print("\nX_test:\n")
print(X_test.head())
print(X_test.shape)
vectorizer = TfidfVectorizer(use_idf=False)
trainvec = vectorizer.fit_transform(X_train)
testvec = vectorizer.transform(X_test)
classifier = MultinomialNB()
classifier.fit(trainvec, y_train)
classes = classifier.predict(testvec)
print(metrics.accuracy_score(y_test, classes))
print(metrics.classification_report(y_test, classes))

