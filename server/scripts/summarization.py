import re
import nltk
import math
import heapq

article_text = """
The first science fiction (sf) magazine, Amazing Stories, was published in 1926, and it was soon followed by the appearance of organized groups of science fiction fans, who contacted each other by mail, using the addresses published in the letter columns of the professional magazines. Amateur magazines, eventually known as fanzines, quickly followed. William L. Crawford was an early science fiction fan, who, unusually, had enough money to acquire his own printing press. In late 1933, with the help of another fan, Lloyd Arthur Eshbach, Crawford prepared a flyer announcing a new magazine, to be titled Unusual Stories. He intended to print fantasy and horror in addition to science fiction; sf historian Sam Moskowitz suggests that this was an attempt to broaden the potential subscription base for the magazine. Crawford could not afford to pay for the stories, but offered contributors a lifetime subscription instead.

In the flyer, which appeared in November 1933, Crawford complained that science fiction in the professional magazines was being stifled by publishing taboos, and asserted that no such taboos would apply to Unusual Stories. The flyer listed the names of several well-known writers of the day, including H. P. Lovecraft, Clifford D. Simak, and Robert E. Howard, and also included a page from P. Schuyler Miller's story "The Titan", which Miller had been unable to publish because of its sexual content. Science fiction historian Mike Ashley speculates that the flyer may have influenced two editors of professional sf magazines: Desmond Hall, an assistant editor at Astounding Stories, where a "thought variant" policy was announced in the December 1933 issue, aimed at publishing more original stories; and Charles Hornig, who was shortly to become editor of Wonder Stories, where he instituted a "new policy" in the January 1934 issue which emphasized originality and barred stories that merely reworked well-worn ideas. Crawford followed the flyer with the first issue of Unusual Stories, dated March 1934; it was mailed out in two parts, which when combined included one full story: "When the Waker Sleeps", by Cyril G. Wates. Not every subscriber received the second part of the issue. It was apparent that more parts of the issue were planned, but they never appeared, and an incomplete story, "Tharda, Queen of the Vampires", by Richard Tooker, never saw full publication.

Two months later Crawford issued the first issue of Marvel Tales, dated May 1934. This included material that had been planned for Unusual Stories, so it seemed that this was the same magazine under a new title. David H. Keller's "Binding Deluxe", which was horror, rather than sf, appeared, along with a story by H. P. Lovecraft, "Celephais", that had previously only been published in an amateur magazine edited by his wife, Sonia Greene. A second issue of Marvel Tales, which Crawford printed with two different covers, appeared a couple of months later, dated July/August 1934, with the number of pages increased from 40 to 60] This featured stories by Frank Belknap Long and Manly Wade Wellman, along with Robert E. Howard's "The Garden of Fear", printed under the pseudonym "James Allison"; this was the only publication of "The Garden of Fear" until Crawford reprinted it in an anthology in 1946. Crawford also announced a story competition. The third issue, dated Winter 1934, increased in size again, this time to 68 pages. "The Titan", by P. Schuyler Miller, which had been advertised in the original flyer for Unusual Stories, began serialization, and Robert Bloch's first published fiction, "Lilies", appeared, along with "The Golden Bough" by David H. Keller. Four winners of the story competition were announced, though only two ever saw print: Crawford printed "The Elfin Lights" by W. Anders Drake (a pseudonym for Eshbach), and R. DeWitt Miller's submission, "The Shapes", appeared in Astounding Stories the following February.
"""

# per https://www.kaggle.com/code/imkrkannan/text-summarization-with-nltk-in-python/notebook

def get_summary(paragraph):
    sentence_list = nltk.sent_tokenize(paragraph)

    output_sentence_count = math.ceil(
        len(sentence_list) / 2
    )
    stopwords = nltk.corpus.stopwords.words('english')


    word_frequencies = {}
    for word in nltk.word_tokenize(paragraph):
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1
        maximum_frequncy = max(word_frequencies.values())

    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)

    sentence_scores = {}

    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                # if len(sent.split(' ')) < 30:
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word]
                else:
                    sentence_scores[sent] += word_frequencies[word]

    return ' '.join(heapq.nlargest(output_sentence_count, sentence_scores, key=sentence_scores.get))

# remove some punctuation and numbers
# article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)

# split text into paragraphs
paragraphs = re.split("\n\s*", article_text)
paragraphs = [paragraph for paragraph in paragraphs if paragraph != '']

summary = ""
for paragraph in paragraphs:
    summary += get_summary(paragraph) + "\n\n"

print(len(summary) * 100 / len(article_text))
print(summary)
