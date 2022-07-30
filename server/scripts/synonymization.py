import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import brown
from nltk.probability import *

words = FreqDist()

# this is not how it will be done
# we will be reading freq from the SQL database instead
for sentence in brown.sents():
    for word in sentence:
        words[word.lower()] += 1


# nltk.download("popular")

# https://stackoverflow.com/questions/63666191/using-wordnet-with-nltk-to-find-synonyms-that-make-sense


def get_synonyms(word, pos):
    for synset in wn.synsets(word, pos=pos2wordnetpos(pos)):
        for lemma in synset.lemmas():
            yield lemma.name()


def pos2wordnetpos(penntag):
    if penntag == "NNP":
        # this is a person, skip
        return ""
    morphy_tag = {"NN": wn.NOUN, "JJ": wn.ADJ, "VB": wn.VERB, "RB": wn.ADV}
    try:
        return morphy_tag[penntag[:2]]
    except:
        return ""

text = """
President George Herbert Walker Bush was the 41st President of the United States of America. President Bush assumed office on January 20 1989, serving for one term until January 20 1993. Prior to winning the presidency, Bush had served as the vice president under President Ronald Reagan from 1981 to 1989.

President Bush ran on a Republican Party ticket, a party he joined early on in his business as well as political career. He is the father of President George W. Bush, the 43rd President of the United States of America.

George Herbert Walker Bush was born on June 12 1924, in Massachusetts to Prescott and Dorothy Bush. His father was the US senator for Connecticut from 1959 to 1963. George H. W. Bush attended schools within Massachusetts, and at eighteen years, he was accepted into Yale University. However, the Pearl Harbor attack of 1941 saw him halt his plans to join the prestigious University and enlist in the US navy, where at 18, he was one of the youngest enlistees in the Navy’s history.

George H. W. Bush served in the navy until the end of the Second World War in 1945. Upon his return home, he soon married Barbara Bush, and he subsequently rejoined Yale University and completed his degree studies in two through an accelerated program.

He later moved his family to Texas, where he wanted to establish a career in the oil industry. He worked for several oil companies as he established contacts that enabled him establish an oil drilling company with a partner. He made a fortune in the oil business and then set his sights on a political career, a step he had desired to take for a long time.

In 1966, while he was still chairperson of the Republican Party in Texas’ Harris County, he ran for the office of the congressional representative for Texas’ seventh district and won. He was re-elected to the same seat in 1968. Because this was his first political office on a national scale, the political views, beliefs, and policies that would shape his presidency began to emerge.

Even this early, George H. W. Bush identified with the conservative policies of the Republican Party to which he belonged (Solomon, 2011, p.51). He identified with the President Nixon’s policies in the Vietnam War, a war that was hugely unpopular with the American public in its later stages. His position on the military draft leaned on its abolition, and he voted to support the same.

Although a conservative, he broke ranks with the Republican Party on the issue of birth control, which he supported. George H. W. Bush as the first republican to represent Houston in the House of Representatives, all the previous posts having been held by Democrats.

Bush then set his sights on Texas senate seat, and contested in the 1970 elections, after resigning from his Congressional representative position. Although he easily won his party’s primary elections to earn a ticket for the senate contest, democrat Lloyd Bentsen subsequently defeated him.

Following his electoral defeat by congressional representative Bentsen, Bush was jobless on the political front, having relinquished his seat as the congressional representative for Texas’ seventh District.

However, by this time he had sufficiently raised his political profile on the national scene, and he was widely known throughout the country. He had also gained political friends in the highest of offices, and he was close to President Nixon.

President Nixon subsequently nominated him to the post of US ambassador to the UN, and his subsequent unanimous confirmation by the Senate was testament to the bi-partisan appeal that he radiated as a politician (Wiener, 2010, p.29). He served as the US ambassador to the UN for two years, and he ably represented the nation in during his brief tenure.

George H. W. Bush’s profile in the Republican Party, beginning with his years as the Chairman of the Republican Party for Harris County in Texas had risen over the years.

He was a vigorous campaigner, contributed funds, and spent his time advocating for the party’s various causes. Therefore, in 1973, he was the Republican Party’s unanimous choice for leadership, and he assumed the position of chairman of the Republican National Committee.

The Watergate scandal soon came to the public’s attention, and Bush was split between supporting his friend President Nixon, and saving the public face of the Republican Party as more investigations revealed Nixon’s culpability (Wiener, 2010, p.29). As chair of the party’s national committee, Bush asked President Nixon to resign in order to save the Party, and Nixon soon resigned.

Having proved his mettle as the US envoy to the United Nations, Bush was appointed as the US ambassador to China. His office was based in Taiwan and he initiated relations with the People’s Republic of China, with set the stage for full diplomatic relations between the US and China in later years, which prior to his appointment was non existent.

The experiences he underwent, in his various postings in foreign nations, would give him an edge in foreign policy when he eventually ran for president in 1989. George H. W. Bush served as US envoy to China for slightly over a year, before returning to the US to serve as Director of the Central Intelligence Agency (CIA), a post appointed by Nixon’s successor President Gerald Ford.
"""

# Tokenize text
import time
from string import punctuation
import re

punctuation = list(punctuation)

punctuation.append("“")
punctuation.append("”")
punctuation.append("’")
punctuation.append("‘")

# and remove []() from punctuation
punctuation.remove("[")
punctuation.remove("]")
punctuation.remove("(")
punctuation.remove(")")

punctuation = ''.join(punctuation)

t1 = time.time()
# split text into paragraphs
paragraphs = re.split("\n\s*", text)
paragraphs = [paragraph for paragraph in paragraphs if paragraph != '']

output_text = ""

for paragraph in paragraphs:
    paragraph = nltk.word_tokenize(paragraph)

    for word, tag in nltk.pos_tag(paragraph):
        # Filter for unique synonyms not equal to word and sort.
        unique = sorted(
            set(
                "".join(synonym.split("_"))
                for synonym in get_synonyms(word, tag)
                if synonym != word
                and synonym != word.lower()
            )
        )

        # get the highest frequency synonym (aka easiest)
        if len(unique) > 0:
            highest_freq_synonym = max(unique, key=lambda x: words[x])
            if words[highest_freq_synonym] > words[word]:  # more freq alternative
                output_text += highest_freq_synonym + " "
            else:
                output_text += word + " "
        else:
            output_text += word + " "

        if word in punctuation:
            output_text = output_text[:-3] + word + " "

    output_text = output_text[:-1] + "\n\n"

output_text = output_text[:-2]

t2 = time.time()
print(f"Time taken: {t2 - t1}")  # one second for a full one, good

print(output_text)
