import math
import numpy as np
import nltk
import re
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS as sklearn_stop_words
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer

# download necessary nltk data files
nltk.download('punkt')
nltk.download('wordnet')

class TextSimilarityCalculation:
    def __init__(self, str1:str, str2:str) -> None:
        self.str1 = str1
        self.str2 = str2

    @staticmethod
    def preprocess_text(text:str) -> list:
        """
        Description: Preprocesses data for cosine similarity calculation
        Operations: Tokenization, Lowercasing, Removing stopwords, Removing punctuations, Stemming & Lemmatization
        """
        # Tokenization, Lowercasing, and Removing Punctuation
        tokenized = [word.lower() for word in text.split()]
        tokens = [re.sub(r'\W+', '', token) for token in tokenized if re.sub(r'\W+', '', token)]
     
        # Removing stop words
        stop_words = set(stopwords.words('english')).union(sklearn_stop_words)
        filtered_tokens = [token for token in tokens if token not in stop_words]

        # Stemming & Lemmatization
        preprocessed = [WordNetLemmatizer().lemmatize(PorterStemmer.stem(token)) for token in filtered_tokens]

        return preprocessed
    
    @staticmethod
    def calculate_tf_idf(document:list[list[str]]):
        """Description: Calculates TF-IDF for each token in a document"""
        n, tf = 0, {}
        # calculate the term frequency
        for row_index, listofwords in enumerate(document):
            for col_index, word in enumerate(listofwords):
                n += 1 #corpus length
                if word not in tf:
                    tf[word] = [1, (row_index,col_index)]
                else:
                    tf[word] = d[word][0] + 1
        
                
        

