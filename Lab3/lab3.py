from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
from sklearn.cluster import MiniBatchKMeans

train = fetch_20newsgroups(subset="train")

test = fetch_20newsgroups(subset="test")

vectorizer = TfidfVectorizer( use_idf=False )
trainvec = vectorizer.fit_transform(train.data)
testvec = vectorizer.transform(test.data)

classifier = MultinomialNB()
classifier.fit(trainvec, train.target)
classes = classifier.predict(testvec)

print (metrics.accuracy_score(test.target, classes))
print (metrics.classification_report(test.target, classes))

cluster = MiniBatchKMeans(20)
print(cluster.fit(trainvec))
