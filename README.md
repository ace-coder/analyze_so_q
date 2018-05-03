This is a term project for the course "Data Mining Applications for Software Engineering"
#
The task is to implement the paper "Why, When, and What: Analyzing Stack Overflow Questions by Topic, Type, and Code"  
#  
  
Developed and maintained by:  
Md Mainuddin  
FSUID: mm15ar  
Dept. of Computer Science  
Florida State University  
# 
##  
  
List of files and directories:  
Directories:
1. text_files		Text extracted from Stack Overflow questions and answers are stored in this folder.  
2. code_files	Code extracted from Stack Overflow questions and answers are stored in this folder.  
3. output			The output of LDA models are saved in this folder.  
  
Files:  
1. create_documents.py		Gets data from database and extract text from the title, body of the questions and answers of Stack Overflow data; then creates text documents to be used for LDA models. Text data from questions and answers are saved in files under "text_files" directory, code documents are saved in "code_files" directory.  
2. lda_question_concepts.R	Uses the documents from "text_files" directory and creates LDA model for question concepts. The output is saved in files under "output" directory.  
3. lda_code_text_topics.R		Uses the documents from "text_files" for text and from "code_files" for code and creates LDA model for Code Text topics. The output is saved under "output" directory.  
4. hobby_or_serious.py		Uses SQL query to form the results of comparative busy days for different programming languages.  
#####  
Report of the project: Project Report.pdf  
