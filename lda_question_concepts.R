#!/usr/bin/env Rscript
library(tm)
library(topicmodels)
library(SnowballC)
library(clue)
library(lsa)
library(proxy)
# library(pbdDMAT, quiet = TRUE)

#setwd("/home/irlabuser/Desktop/IR_lab/scripts")
corpusRaw <- Corpus(DirSource("text_files"), readerControl = list(reader = readPlain, language = "en", load = TRUE))

# transform the corpus to lowercase
corpus <- tm_map(corpusRaw, tolower)

replaceNonAlphanum <- function(x) {
  gsub("[^a-zA-Z0-9]", " ", x)
}

corpus <- tm_map(corpus, replaceNonAlphanum)

# remove numbers from corpus
corpus <- tm_map(corpus, removeNumbers)

# get the default list of English stopwords
mystopwords <- stopwords(kind = "en")

# remove stopwords from corpus
corpus <- tm_map(corpus, removeWords, mystopwords)

# stem the corpus
corpus <- tm_map(corpus, stemDocument)

# strip consecutive whitespace in the corpus
corpus <- tm_map(corpus, stripWhitespace)

# inspect the preprocessed corpus vs the raw corpus
tempPre <- data.frame(matrix(unlist(corpus), byrow=T))
tempRaw <- data.frame(matrix(unlist(corpusRaw), byrow=T))
colnames(tempPre) <- c("preprocessed text")
colnames(tempRaw) <- c("original text")
# View(tempPre) # Row 31 seems to be an undesired output. However, since temp is only used for verification, this issue can be ignored.
# View(tempRaw) # Row 31 seems to be an undesired output. However, since temp is only used for verification, this issue can be ignored.

# write.table(tempPre, "output/tempPre.txt", sep="\t")
# write.table(tempRaw, "output/tempRaw.txt", sep="\t")

#construct the document-term matrix, using the tfIdf weighting
corpusDTM <- DocumentTermMatrix(corpus)

dim(corpusDTM)

#compute LDA with 30 topics
lda <- LDA(corpusDTM, k = 30)
lda

#obtain the most likely topic for each document
Topic <- topics(lda,1)
# View(as.data.frame(Topic))

write.table(as.data.frame(Topic), "output/concept/Topic.txt", sep="\t")

#obtain the five most frequent words for each topic
Terms <- terms(lda, 7)
# View(t(Terms[,1:30]))

write.table(t(Terms[,1:30]), "output/concept/Terms.txt", sep="\t")

r <- cbind(as.vector(data$Title), as.vector(data$Subject), as.vector(data$Topic.Code), as.vector(terms[topics]))
hr <- head(r)
write.table(r, "output/lda_topics.txt", sep="\t")
write.table(head(r), "output/lda_topics_head.txt", sep="\t")
