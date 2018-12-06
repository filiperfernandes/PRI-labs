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
 
  - ````python3 search.py keyword1, keyword2, keyword3, etc.````
 
 ---
 
### Exercise B
````classification.py:````


##### Libraries used:

 - pandas
 - sklearn
 
 ##### Usage:
 
  - ````python3 classification.py````
  
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
  ```[-m  Which party is mentioned more times by the other parties?```

