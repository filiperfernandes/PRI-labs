# PRI Project instructions:

##### Pre-requisites:

 - Install python3
 - Intall python3-pip
 - Install requirements in requirements.txt
    - ```pip3 install -r requirements.txt)```
 
 ---

### Exercise A

````search.py:````


##### Libraries used:

 - whoosh
 
 ##### Usage:
 
 - To print help
    - ````python search.py [-h] ````
 - Global usage
        - ````python search.py [-h] [-f FILE] [-l LANGUAGE] [-t TF_IDF] [-b BM-25F] [-fr Frequency] -i INPUT_ARGS````
 ---
 
### Exercise B
````classification.py:````


##### Libraries used:

 - pandas
 - sklearn
 
 ##### Usage:
 
  - To print help
    - ````python3 classification.py -h````
 - Global usage
    - ```usage: classification.py [-h] [-f FILE] [-s SIZE] [-K KNeighborsClassifier] [-P Perceptron] [-m MultinomialNB] [-l LinearSVC]```

 ---
 
### Exercise C
````analysis.py:````
 
##### Libraries used:

 - spacy
 - collections.Counter
 - collections.defaultdict
 
 
 ##### Usage:
 
 - To print help
    - ````python3 analysis.py -h````
 - Global usage
    - ```python3 analysis.py [-h help] [-f file] [-l language] [-p What are the most mentioned entities for each party?]```
  ``` [-g  What are the most mentioned entities globally?]``` 
  ```[-t How many times does any given party mention other parties?] ```
  ```[-m  Which party is mentioned more times by the other parties?]```

