import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import spacy

nlp = spacy.load("en_core_web_sm")

# load textbank.csv into df
df = pd.read_csv("textbank.csv")

# only take those where the charcount is > 1000
df = df[df["charcount"] > 1000]

# set charcount in df to charcount[:1000] for every element
df["lemmatized_content"] = df["lemmatized_content"].apply(lambda x: x[:1000])

df = df.head(1000)

def calculate_difficulty(row):
    return (
        row["unique_words"]
        / row["total_words"]
        * row["average_word_length"]
        * (row["average_sentence_length"] ** 0.1)
    )

# add another column to df based on above function
df["difficulty"] = df.apply(calculate_difficulty, axis=1)

df = df.sort_values(by="difficulty", ascending=False)

# split into 4 equally sized groups
df = df.groupby(df.index // (len(df) // 5)).apply(lambda x: x.reset_index(drop=True))

# print head of four groups
print(df.iloc[0]['lemmatized_content'], end="\n\n")
print(df.iloc[249]['lemmatized_content'], end="\n\n")
print(df.iloc[499]['lemmatized_content'], end="\n\n")
print(df.iloc[749]['lemmatized_content'], end="\n\n")

# plot a histogram of unique_words / charcount[:1000] with seaborn
sns.set(style="whitegrid")
ax = sns.distplot(df["difficulty"], bins=100)
plt.show()
