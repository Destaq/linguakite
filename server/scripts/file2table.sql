-- this file takes `../data/lemma_freq_list.csv`, a csv file of the most common English lemmas (drawn from unigram_freq.csv)
-- and converts it to a table in the postgres database
-- which is a table of lemmas (and hence shorter than 333k)
-- lemmas which have updated frequencies

COPY word(lemma, lemma_rank, word_rank)
FROM '/Users/simonilincev/Desktop/School/IA/CS/Code/linguakite/server/data/lemma_freq_list.csv'
DELIMITER ','
CSV HEADER;
