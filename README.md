# TextMining-Review-Analysis  
  
  
* [개요](#1-개요)   
* [데이터 수집](2-데이터-수집Crawling)
* [전처리](#3-데이터-전처리)  
* [형태소 분석 및 처리](#4-형태소-분석-및-처리)  
* [시각화](#5-시각화)
* [결과](#6-결과-정리)
  * [제품 방향성](#문스타의-제품-방향성)  
* [멤버](#7-멤버)       
  
  
## 1. 개요  

**주제 : 네이버 쇼핑의 리뷰 키워드 분석을 통한 제품 개선 방안 모색**
  
 코로나19의 영향으로 인터넷 방송, 유튜버, PC방 등 여가 활동의 트렌드 변화로 **게이밍 의자의 수요 증가**  
  
→ 게이밍 의자의 리뷰 데이터 기반 인기 제품에 대한 소비자의 실구매 후기, 제품 특징 등을 분석한다.  
→ 네이버 쇼핑 랭킹 후순위에 있는 비인기 제품의 특징과 cross-match하여 개선점 및 판매 증대 방안을 모색한다.  
  
  <img width="654" alt="스크린샷 2022-12-31 오후 6 55 07" src="https://user-images.githubusercontent.com/114709620/210132474-0fcaf9a6-a1a5-4110-9932-ceeb1b7ea643.png">  
  
  
  
## 2. 데이터 수집(Crawling)
  
  
[네이버 쇼핑 검색창에 "게이밍 의자" 검색](https://search.shopping.naver.com/search/all?query=%EA%B2%8C%EC%9D%B4%EB%B0%8D%20%EC%9D%98%EC%9E%90&cat_id=&frm=NVSHATC) 후 페이지에 먼저 노출되는 제품 기준으로 인기 및 비인기 제품 선정 (네이버 랭킹 기준 정렬)  
  
광고성 제품은 제외하고 소비자들의 실구매 후기만을 수집   
  
  
**<인기 제품>**   
  
  - 첫 페이지부터 상위 40개의 제품 리뷰 사용
      - 40개 제품의 별점 평균 : 4.62점  
      
  - 전체 리뷰 중, 별점이 4점 이상인 리뷰 크롤링 
      - 43,596개의 긍정 리뷰 데이터   
      
**<비인기 제품>**  
  
  - 2022년 7월 기준, 리뷰가 많고 별점이 낮은 제품 선택 -> *"문스타 게이밍 의자 A 컴퓨터 의자 학생 의자"*  
  
  - 전제 리뷰 중, 별점이 3점 이하인 리뷰 크롤링 
    - 423개의 부정 리뷰 데이터  
   
   
   
 <img width="824" alt="스크린샷 2022-12-31 오후 8 04 43" src="https://user-images.githubusercontent.com/114709620/210134458-befa57b9-5141-42f5-bebf-6ec32f6d17d4.png">  
  
  
<img width="824" alt="스크린샷 2022-12-31 오후 8 06 13" src="https://user-images.githubusercontent.com/114709620/210134482-4815c6ec-cf83-490e-b781-1b8498cc4e27.png">

  
  
#### **확인 사항**
  
상품을 클릭하면 이동하는 판매 사이트의 주소의 형태가 2가지(스마트 스토어 & 네이버 쇼핑)로 존재 
  
  
<img width="1080" alt="스크린샷 2022-12-31 오후 8 07 45" src="https://user-images.githubusercontent.com/114709620/210134524-1608e492-0715-4bb6-8282-d6e143200c40.png">


```python
# 스마트 스토어의 경우   
  
review_url = "https://smartstore.naver.com/i/v1/reviews/paged-reviews"
params = {
  "page" : page_num,
  "pageSize" : "20",
  "merchantNo" : merchanNo,
  "originProductNo" : originProductNo,
  "sortType" : "REVIEW_RANKING"
 }  
```   
   
```python
# 네이버 쇼핑의 경우  
  
review_url = "https://search.shopping.naver.com/api/review"
params = {
  "nvMid" : pro["id"],
  "reviewType" : "ALL",
  "sort" : "QUALITY",
  "isNeedAggregation" : "N",
  "isApplyFilter" : "Y",
  "page" : page_num,
  "pageSize" : "20
 }
```   
  
  
## 3. 데이터 전처리 
  
**리뷰 텍스트 내 불필요한 문자 제거**    
  
```python  
re.sub("[^가-힣0-9A-Za-z\?\!\.\,]", "", text)  
```  

    <br>초기불량 QC를 잘잡으신다면 아마 2022년까지는 이 의자가 게이밍 의자 원탑을 지키시지 않을까요?    
  
    => 초기불량 QC를 잘잡으신다면 아마 2022년까지는 이 의자가 게이밍 의자 원탑을 지키시지 않을까요?  

  
  
## 4. 형태소 분석 및 처리          
   
#### 4-1. 각 리뷰의 문장들을 의미있는 형태소 기준으로 토큰화(Tokenization)    
  
```python
positive_reviews = []  
  
for positive in pos_reviews_new:
    # Okt 형태소 분석기 사용
    okt = Okt()
    # stem : 통일화 여부 
    positive_reviews.append(okt.pos((positive), stem= True))
``` 

결과:  
  
```python
[[('우선', 'Noun'),  
  ('엄청', 'Adverb'),  
  ('편하다', 'Adjective'),  
  ('오래되다', 'Adjective')  
 ...
``` 
  
 
#### 4-2. 길이가 1인 토큰 제거 & 불용어 사전을 사용해 긍/부정 분석에서 큰 의미가 없는 토큰 제거  
  
<불용어 사전 예시>  
  
    "의자"
    "있다"
    "이다"  
    "게이"
    "아니다"
    "문제"
    "듭니"
    "제닉스"
    "만원"
    "때문"
    "에이"
    "이번"
    "이렇다"
    "안나"
    "드네"
    "서도"
    "울프"
    "야하다"
    ...   
  
  ```python
  for i in positive_reviews:
        pos_words =[]
        for token, pos in i:
            # 품사가 명사나 형용사고, 토큰 길이가 2 이상이고, 불용어 사전에 없는 토큰 출력 
            if (pos == 'Noun' or pos == 'Adjective') and len(token) >= 2 and not token in stopwords_pos:
                pos_words.append(token)
        all_pos_words.append(pos_words)
  ```
  
  
#### 4-3. 긍정(부정) 리뷰에 혼재된 부정(긍정)적인 내용 처리   

<하나의 리뷰 내 긍・부정이 혼재된 내용 예시>  
  
  _"앉는 부위 양옆으로 튀어나온게 좀 **불편해요**. 그래도 확실히 **튼튼한** 제품이여서 **좋아요**."_



구 분 | 내 용 | 효 과 
|------|------|--------|
방법1   | 단어가 긍정어(부정어) 사전에 존재한다면 해당 **리뷰 자체 삭제** | 긍・부정의 순수도(purity)는 높아지나, 데이터 수 감소       
방법2   | kss 라이브러리를 사용해 해당 리뷰를 **문장 단위로 분리하여 해당 문장만 삭제** | 한 문장에도 혼재된 내용이 포함될 수 있음        
방법3   | 문장에서 의미가 전환될 때 사용되는 **접속 부사(하지만, 그러나, 근데 등) 사전**을 이용해 혼재된 내용 분리 | 접속사가 존재하지 않는 경우에는 적용되지 않음        
방법4   | **N-gram**을 사용하여 문장 맥락 상 어울리는 단어들의 시퀀스만 추출 | 긍・부정을 가리키는 대상 확인 가능          
  
 
 
## 5. 시각화 
  
<방법 1>  
  
<img width="637" alt="스크린샷 2023-01-01 오후 9 55 08" src="https://user-images.githubusercontent.com/114709620/210171205-33a80ee5-864f-43f5-bdf6-4eb2f5cf33fc.png">

<방법 2>  
  
<img width="649" alt="스크린샷 2023-01-01 오후 9 57 32" src="https://user-images.githubusercontent.com/114709620/210171247-fac13bf0-58bf-48a8-9779-3cd2602b0bba.png">

<방법 3>  
  
<img width="644" alt="스크린샷 2023-01-01 오후 10 02 26" src="https://user-images.githubusercontent.com/114709620/210171413-d210ace8-e1be-4436-b9ad-68c754f08eab.png">  
  
<방법 4>  
  
2-gram   
<img width="644" alt="스크린샷 2023-01-01 오후 10 03 24" src="https://user-images.githubusercontent.com/114709620/210171451-a236bed3-2a78-429c-a491-87463da604f3.png">    
  
3-gram    
<img width="644" alt="스크린샷 2023-01-01 오후 10 03 32" src="https://user-images.githubusercontent.com/114709620/210171455-ea132c7d-41c8-4848-a897-3db54d7314b0.png">  


## 6. 결과 정리

게이밍 의자의 인기 제품과 비인기 제품을 정의 내린 후, 긍정・부정 리뷰 키워드 분석을 통해 각각의 특징과 소비자들의 니즈를 파악한 결과는 다음과 같다.  
  

<img width="399" alt="스크린샷 2023-01-01 오후 10 39 06" src="https://user-images.githubusercontent.com/114709620/210172595-93ae601a-d809-44c7-83dc-b075e3349849.png">  
  
  
#### "문스타"의 제품 방향성 
  
<img width="272" alt="스크린샷 2023-01-01 오후 10 42 05" src="https://user-images.githubusercontent.com/114709620/210172701-aa5333cb-085e-4c05-b312-f6793521a0e7.png">  
  
- 조립 : 쉽고 간결한 조립 설명서
- 포장/배송 : 깔끔한 포장과 빠른 배송
- 가성비 : 가격은 높더라도 우수한 품질
- 쿠션감 : 푹신한 착석감
- 고정력 : 발 받침, 허리 받침, 팔걸이의 견고함  
  


## 7. 멤버 












