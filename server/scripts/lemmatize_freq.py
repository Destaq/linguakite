import spacy

nlp = spacy.load("en_core_web_sm")

file = open(
    "/Users/simonilincev/Desktop/School/IA/CS/Code/linguakite/server/data/wiki-100k.txt", "r"
)
write_file = open(
    "/Users/simonilincev/Desktop/School/IA/CS/Code/linguakite/server/data/lemma_freq_list.csv", "w+"
)

write_file.write("lemma,rank,wordrank\n")

# read lines from input file
lines = file.readlines()

# watch for duplicates
current = 1
wordrank = 1
lemmas = []

# split each line in lines into a list of two by comma
for line in lines:
    line = line.rstrip()
    # lemmatize the word
    lemma = nlp(line)[0].lemma_

    if current % 100 == 0:
        print(current, end="\r")

    # we don't want to allow duplicate lemmas
    if lemma not in lemmas:
        lemmas.append(lemma)
        # write the lemmatized word to the output file
        write_file.write(f"{lemma},{current},{wordrank}\n")
        current += 1
    else:
        pass

    wordrank += 1  # used for when user inputs their estimated vocab size

print(len(lemmas))

file.close()
write_file.close()
