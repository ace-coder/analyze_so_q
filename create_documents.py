#!/usr/bin/python
import psycopg2, re

from dbconnect import dbconfig
from bs4 import BeautifulSoup

params = dbconfig()
conn = psycopg2.connect(**params)

def extractTextFromHTML(html):
    soup = BeautifulSoup(html, "html.parser")

    code = []
    for script in soup(["code"]):
        code_txt = script.get_text()
        code_lines = (line.strip() for line in code_txt.splitlines())
        code_chunks = (phrase.strip() for line in code_lines for phrase in line.split("  "))
        code_text = " ".join(chunk for chunk in code_chunks if chunk)
        code.append(code_text)
        script.extract()  # rip it out

    for script in soup(["script", "style"]):
        script.extract()  # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = " ".join(chunk for chunk in chunks if chunk)
    full_code = " ".join(code)
    return [text, full_code]

def getTextFromAnswers(q_id):
    cur2 = conn.cursor()
    query = "select body from posts where parent_id = %d" % (q_id)
    cur2.execute(query)

    returnText = []
    returnCode = []
    for row in cur2:
        q_text = extractTextFromHTML(row[0])
        returnText.append(q_text[0])
        returnCode.append(q_text[1])
    cur2.close()
    return [returnText, returnCode]

def getDocumentForTags(query):
    cur = conn.cursor()
    cur.execute(query)
    texts = []
    code = []
    for row in cur:
        title = row[1]
        q_text = extractTextFromHTML(row[3])
        texts.append(title);
        texts.append(q_text[0]);
        code.append(q_text[1]);
        tags = re.findall(r'<(.+?)>', str(row[2]))
        if (row[4] is not None and int(row[4]) > 0):
            a_text = getTextFromAnswers(row[0])
            texts.extend(a_text[0])
            code.extend(a_text[1])
    cur.close()
    return [texts, code];


q_select = "SELECT id, title, tags, body, answer_count FROM posts WHERE post_type_id = 1 AND "
q_limit = " LIMIT 25000"
dic_query = {}
dic_query['Java'] = " (tags like '%<java-ee>%' or tags like '%<java>%')"
dic_query['Python'] = " (tags like '%<python>%')"
dic_query['CSS'] = " (tags like '%<css>%' or tags like '%<css3>%')"
dic_query['SQL'] = " (tags like '%<sql>%' or tags like '%<mysql>%' or tags like '%<sql-server>%' or tags like '%<postgresql>%' or tags like '%<databases>%')"
dic_query['VCS'] = " (tags like '%<git>%' or tags like '%<mercurial>%' or tags like '%<svn>%')"
dic_query['BuildTools'] = " (tags like '%<ant>%' or tags like '%<maven>%')"

for key, value in dic_query.items():
    txt_list = getDocumentForTags(q_select + value + q_limit);
    file = "text_files/%s.txt"%(key)
    fo = open(file, "w", encoding='utf-8')
    fo.write(" ".join(txt_list[0]))
    fo.close()

    if key == "Java":
        file = "code_files/%s.txt" % (key)
        fo = open(file, "w", encoding='utf-8')
        fo.write(" ".join(txt_list[1]))
        fo.close()
