import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import Perceptron
from sklearn.svm import LinearSVC

import argparse

def get_parser():

    parser = argparse.ArgumentParser(description="""PRI classification tool""")
    parser.add_argument('-f', '--file', dest='file', help="""receive file from stdin [default: no]""",
                        action="store")
    parser.add_argument('-s', '--size', dest='size', help="""Specify training and test percentage [default: 0.5]""",
                        action="store")
    parser.add_argument('-K', '--KNC', help="""KNeighborsClassifier""",
                        action="store_true")
    parser.add_argument('-P', '--PER', help="""Perceptron""",
                        action="store_true")
    parser.add_argument('-M', '--multi', help="""MultinomialNB""",
                        action="store_true")
    parser.add_argument('-lin', '--linear', help="""LinearSVC""",
                        action="store_true")
    parser.add_argument('-l', '--language', dest='language', help="""Specify language 'en' or 'pt'""",
                        action="store", required=True)
    return parser


def main():

    parser = get_parser()
    args = vars(parser.parse_args())
    file = args['file']
    knc = args['KNC']
    per = args['PER']
    multi = args['multi']
    linear = args['linear']
    size = args['size']
    language = args['language']

    if file:
        print("Using file " + file)
        FILE_PATH = "pri_project_data/"+file
    else:
        FILE_PATH = "pri_project_data/en_docs_clean.csv"

    if language is not None and language == "pt" and not file:
        FILE_PATH = "pri_project_data/pt_docs_clean.csv"
    elif language is not None and language == "en" and not file:
        FILE_PATH = "pri_project_data/en_docs_clean.csv"
    else:
        print("Language must be 'en' or 'pt'")

    df = pd.read_csv(FILE_PATH)
    y = df.party
    X = df.text

    if size is not None:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=float(size))
    else:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5)
    vectorizer = TfidfVectorizer(use_idf=False)
    trainvec = vectorizer.fit_transform(X_train)
    testvec = vectorizer.transform(X_test)

    if knc:
        classifier = KNeighborsClassifier()
    elif per:
        classifier = Perceptron()
    elif multi:
        classifier = MultinomialNB()
    elif linear:
        classifier = LinearSVC()
    else:
        print("No classifier specified, using LinearSVC")
        classifier = LinearSVC()
    classifier.fit(trainvec, y_train)
    classes = classifier.predict(testvec)
    print(metrics.accuracy_score(y_test, classes))
    print(metrics.classification_report(y_test, classes))
    print(metrics.confusion_matrix(y_test, classes))


if __name__ == "__main__":
    main()
