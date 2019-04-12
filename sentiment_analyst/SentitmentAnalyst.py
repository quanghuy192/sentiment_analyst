import pandas as pd
import nltk
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# import numpy as np

CSV_df = pd.read_csv('Reviews_Products.csv')
CSV_df = CSV_df[["name", "reviews.title", "reviews.text"]]

# product
product_df = CSV_df[["name"]].drop_duplicates()

# Fire HDX 8.9 Tablet
tablet_df = CSV_df[CSV_df.name == 'Amazon - Echo Plus w/ Built-In Hub - Silver']

tablet_df['POS_tagger'] = tablet_df.apply(lambda f: nltk.pos_tag(nltk.word_tokenize(f['reviews.text'])), axis=1)
# tokens = nltk.word_tokenize("Good morning, i'm Huy, how old are you.")
print(tablet_df)


