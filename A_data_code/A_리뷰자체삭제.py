# -*- coding: utf-8 -*-
"""1단계_인기상품.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1vbGdt2PE1bhtesGig1W59IN06Mw008NO

# Install libraries
"""

!pip install konlpy

from konlpy.tag import Okt
import os
import numpy as np
import pandas as pd
from datetime import datetime
import json
import re
from tqdm.notebook import tqdm

"""# Prepare data"""

df_pop = pd.read_csv('popular_40.csv')
df_pop

df_pop['pos/neg'] = np.where(df_pop['score'] >= 4, 1, 0)
df_pop[['content','score','pos/neg']]

pos_reviews = list(df_pop['content'][df_pop['pos/neg'] == 1])
neg_reviews = list(df_pop['content'][df_pop['pos/neg'] == 0])
pos_reviews

# 정규표현식을 사용한 전처리

pos_reviews_new = []
for pos_review in pos_reviews:
    pos_reviews_new.append(re.sub("[^가-힣0-9A-Za-z\?\!\.\,]", "", pos_review))
print(len(pos_reviews_new))

"""# Tokenization"""

positive_reviews = []
for positive in pos_reviews_new:
    # Okt 형태소 분석기 사용
    okt = Okt()
    # stem : 통일화 여부 
    # 품사 태깅 (pos)
    positive_reviews.append(okt.pos((positive), stem= True))

positive_reviews

# 불용어사전 

stopwords_pos = pd.read_table('stopwords of positive reviews.txt', sep = '\n', header = None)
stopwords_pos

# 토큰의 길이가 2개 이상이고, 토큰이 stopwords 안에 없을때만 출력 => 불용어 아닌 것 출력
all_pos_words = []

for i in positive_reviews:
        pos_words =[]
        for token, pos in i:
            if (pos == 'Noun' or pos == 'Adjective') and len(token) >= 2 and not token in stopwords_pos:
                pos_words.append(token)
        all_pos_words.append(pos_words)
len(all_pos_words)

all_pos_words

# 38309번째 리뷰 토큰 확인

all_pos_words[38309]

"""# 리뷰 내 부정어가 섞여 있는 경우, 해당 리뷰 삭제"""

# 부정어 사전

neg_words_lst = pd.read_table('negative words.txt', sep = '\n', header = None)
neg_words_lst

neg = []
for i in all_pos_words:
    for j in i:
        if j in neg_words_lst:
            neg.append(i)
            break
len(neg)

for i in neg :
    all_pos_words.remove(i)
len(all_pos_words)

# 순수 긍정 내용이 담긴 리뷰 키워드 

pos_keywords = []
for i in all_pos_words:
    pos_keywords.extend(i)
pos_keywords

from collections import Counter

c = Counter(pos_keywords)
c

from collections import Counter
c = Counter(pos_keywords)
# positive_count = c.most_common() # 상위 10개 출력하기

dic_pos_a = {'키워드':[], 
       '빈도':[]}
for i in c:
    dic_pos_a['키워드'].append(i[0])
    dic_pos_a['빈도'].append(i[1])
dic_pos_a

df_pos_a = pd.DataFrame(dic_pos_a)
df_pos_a

df_pos_a.to_csv('A_positive_keywords.csv', encoding='cp949')