#!/usr/bin/python
import psycopg2, re
import nltk
nltk.download('wordnet')
from dbconnect import dbconfig
from bs4 import BeautifulSoup
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem import PorterStemmer, WordNetLemmatizer
from gensim import corpora, models
import gensim
import snowballstemmer
import operator



tokenizer = RegexpTokenizer(r'\w+')

# create English stop words list
en_stop = get_stop_words('en')

# Create p_stemmer of class PorterStemmer
p_stemmer = PorterStemmer()
stemmer = snowballstemmer.stemmer('english')
wnl = WordNetLemmatizer()

params = dbconfig()
conn = psycopg2.connect(**params)
cur = conn.cursor()

def extractTextFromHTML(html):
    soup = BeautifulSoup(html, "html5lib")

    # kill all script and style elements
    for script in soup(["script", "style", "code"]):
        script.extract()  # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text

def getTextFromAnswers(q_id):
    cur2 = conn.cursor()
    query = "select body from posts where parent_id = %d" % (q_id)
    cur2.execute(query)

    returnText = []
    for row in cur2:
        q_text = extractTextFromHTML(row[0])
        returnText.append(q_text)

    cur2.close()
    return returnText



query = "SELECT id, title, tags, body, answer_count FROM posts WHERE post_type_id = 1 AND (tags like '%<java-ee>%' or tags like '%<java>%') limit 100"
cur.execute(query)
# java_questions = cur.fetchall()

java_texts = []
for row in cur:
    title = row[1]
    q_text = extractTextFromHTML(row[3])
    java_texts.append(title);
    java_texts.append(q_text);
    tags = re.findall(r'<(.+?)>', str(row[2]))
    if(row[4] is not None and int(row[4]) > 0):
        a_text = getTextFromAnswers(row[0])
        java_texts.extend(a_text)

cur.close()


# list for tokenized documents in loop
texts = []

# loop through document list
for i in java_texts:
    # clean and tokenize document string
    raw = i.lower()
    tokens = tokenizer.tokenize(raw)

    # remove stop words from tokens
    stopped_tokens = [i for i in tokens if not i in en_stop]

    # stem tokens
    # stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]
    stemmed_tokens = [wnl.lemmatize(i) if wnl.lemmatize(i).endswith('e') else p_stemmer.stem(i) for i in stopped_tokens]
    # stemmed_tokens = stemmer.stemWords(stopped_tokens)  # [stemmer.stemWords("We are the world".split()) for i in stopped_tokens]

    # add tokens to list
    texts.append(stemmed_tokens)

# turn our tokenized documents into a id <-> term dictionary
dictionary = corpora.Dictionary(texts)

# convert tokenized documents into a document-term matrix
corpus = [dictionary.doc2bow(text) for text in texts]

# generate LDA model
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=15, id2word=dictionary, passes=1000)

for topic in ldamodel.show_topics(num_topics=15, formatted=False, num_words=7):
    # print ("Topic #", topic[0], ":",)
    # topic[1].sort(key=operator.itemgetter(1), reverse=True)
    lst = [i[0] for i in topic[1] if len(i[0]) > 1]
    print(", ".join(lst))

