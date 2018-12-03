from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
train = fetch_20newsgroups(subset='train')
test = fetch_20newsgroups(subset='test')
print(train)