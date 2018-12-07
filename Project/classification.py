import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import Perceptron
from sklearn.svm import LinearSVC

FILE_PATH = "pri_project_data/en_docs_clean.csv"

df = pd.read_csv(FILE_PATH)
y = df.party
X = df.text
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5)
vectorizer = TfidfVectorizer(use_idf=False)
trainvec = vectorizer.fit_transform(X_train)
testvec = vectorizer.transform(X_test)
#classfier = KNeighborsClassifier()
#classifier = Perceptron()
#classifier = MultinomialNB()
classifier = LinearSVC()
classifier.fit(trainvec, y_train)
classes = classifier.predict(testvec)
print(metrics.accuracy_score(y_test, classes))
print(metrics.classification_report(y_test, classes))
print(metrics.confusion_matrix(y_test, classes))
