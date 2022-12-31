# TextMining-Review-Analysis  
  
  
* [개요](#1-개요)   
* [데이터셋](#3-데이터셋)
* [전처리](#4-데이터-전처리)  
* [모델 학습 및 예측](#5-모델-학습-및-예측)  
    * [Transformer](#5-1-transformer)
    * [KoGPT2](#5-2-gpt2)
    * [KoBART](#5-3-bart)
* [모델 선정](#6-모델-선정)
* [Demo](#7-demo)  
* [멤버](#8-멤버)       
  
  
## 1. 개요  

**주제 : 네이버 쇼핑의 리뷰 키워드 분석을 통한 제품 개선 방안 모색**
  
 코로나19의 영향으로 인터넷 방송, 유튜버, PC방 등 여가 활동의 트렌드 변화로 **게이밍 의자의 수요 증가**  
  
→ 게이밍 의자의 리뷰 데이터 기반 인기 제품에 대한 소비자의 실구매 후기, 제품 특징 등을 분석한다.  
→ 네이버 쇼핑 랭킹 후순위에 있는 비인기 제품의 특징과 cross-match하여 개선점 및 판매 증대 방안을 모색한다.  
  
  <img width="654" alt="스크린샷 2022-12-31 오후 6 55 07" src="https://user-images.githubusercontent.com/114709620/210132474-0fcaf9a6-a1a5-4110-9932-ceeb1b7ea643.png">  
  
  
  
## 2. 데이터 수집 (Crawling)
  
  
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
# 네이버 쇼핑의경우  
  
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
  

<img width="460" alt="스크린샷 2022-12-31 오후 8 28 50" src="https://user-images.githubusercontent.com/114709620/210135065-1f862ca8-b1d7-457a-9273-710a4f3df8d5.png">

3-1. 






















