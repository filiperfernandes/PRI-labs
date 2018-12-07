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
        - ````python3 search.py [-h] [-f FILE] -l LANGUAGE [-t] [-b] [-fr] -i INPUT_ARGS````
 - Flags meaning:
    - h: print help
    - f: specify input file, must be in ./pri_project_data/ directory, optional
    - l: specify input language, must be 'en' or 'pt', required
    - t: specify TF_IDF as the ranking function, optional
    - b: specify BM25F as the ranking function, optional
    - fr: specify Frequency as the ranking function, optional
    
    Note: although last four flags are optional, exactly one must be specified
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
    - ```python3  classification.py [-h] [-f FILE] [-s SIZE] [-K] [-P] [-M] [-lin] -l LANGUAGE```
- Flags meaning:
    - h: print help
    - f: specify input file, must be in ./pri_project_data/ directory, optional
    - l: specify input language, must be 'en' or 'pt', required
    - K: specify KNeighbors as the classifier function, optional
    - P: specify Perceptron as the classifier function, optional
    - M: specify MultinomialNB as the classifier function, optional
    - lin: specify LinearSVC as the classifier function, optional
    
    Note: although last four flags are optional, exactly one must be specified
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
    - ```python3 analysis.py [-h] [-f FILE] -l LANGUAGE [-p] [-g] [-t] [-m]```
 - Flags meaning:
    - h: print help
    - f: specify input file, must be in ./pri_project_data/ directory, optional
    - l: specify input language, must be 'en' or 'pt', required
    - p: Get what are the most mentioned entities for each party, optional
    - g: Get what are the most mentioned entities globally, optional
    - t: Get how many times does any given party mention other parties, optional
    - m: Get which party is mentioned more times by the other parties, optional

    Note: although last four flags are optional, exactly one must be specified
