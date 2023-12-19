### Project Title

Music Recommendation App Project

### Overview

- 기간  |  2021. 03 ~ 2021. 03
- 담당 파트 |  개인프로젝트
- 플랫폼 |  Python, Flask
- 웹 주소 | [Link](https://muse-haebing25.koyeb.app)
  
### Background 

1. Spotify를 포함한 Youtube, Netflix 등의 서비스 플랫폼은 추천 알고리즘을 통해 소비자 개개인의 취향에 맞는 컨텐츠를 제공함
2. 음악, 영화 등의 주관적 취향을 분석하고 추천하는 큐레이팅 알고리즘을 구현하고 배포함으로서 추천시스템의 상업적 활용 가능성을 탐구하고자 함

### Audio Features in Spotipy

```
1. Danceability : 템포, 리듬 안정성, 비트 강도 및 전체적인 규칙성을 포함한 음악적 요소의 조합을 기반으로 트랙이 춤에 얼마나 적합한지를 설명
2. Energy : 활기찬 트랙일수록 빠르고 시끄러움
3. Instrumentalness : 트랙에 보컬이 있는지 없는지의 정도
4. Liveness : 값이 높을수록 트랙이 라이브로 수행 될 확률이 높아짐
5. Loudness : 데시벨(dB) 단위의 트랙 전체 소리 크기 
6. Speechiness : Speechiness는 트랙에서 말한 단어의 존재를 감지
7. Valence : 트랙이 전달하는 음악적 긍정적인 정도를 설명
8. Acousticness :  전자 음악이 아닌 어쿠스틱 음악일수록 수치가 높아짐
```

### Algorithm

1.  Kaggle(https://www.kaggle.com/yamaerenay/spotify-dataset-19212020-160k-tracks)에서 Spotify audio features 추천 데이터셋 확보 
2. 사용자가 검색한 음악에 대한 데이터를 Spotipy로부터 수집한 후, audio features를 벡터화한 값의 평균을 구함
3. 추천 데이터셋의 모든 audio features를 벡터화 함
4. 추천 데이터셋의 벡터화 된 값 중 이용자 플레이리스트의 평균 벡터값과 유클리디안 거리로 가장 가까운 값 n개를 인덱스 형식으로 반환
5. 인덱스에 매칭하는 음악 추천 리스트 결과를 도출 

<p align="center">
  <img src="https://github.com/mugan1/muse_spotipy_recommendation/assets/71809159/583797f7-de67-4a52-8dc1-cf3afe7988cf" alt="text" width="number" />
</p>

### Result

1. 로그인 및 회원가입 페이지 : 사용자 입력 정보를 DB에 저장. DB에 저장된 사용자만이 로그인하여 서비스를 이용할 수 있게 시스템 구축
  
<p align="center">
  <img src="https://github.com/mugan1/muse_spotipy_recommendation/assets/71809159/f2cbfd69-3f9f-4865-b870-9a0018fc4a74" alt="text" width="number" />
</p>

2. 검색창 및 검색결과 페이지 : Spotipy로부터 사용자가 검색한 아티스트 혹은 음악의 결과를 출력하고, 원하는 음악을 select하여 저장할 수 있게끔 설계함
   
<p align="center">
  <img src="https://github.com/mugan1/muse_spotipy_recommendation/assets/71809159/e4c9de79-60e1-4409-9446-d779fee2bcbc" alt="text" width="number" />
</p>

<p align="center">
  <img src="https://github.com/mugan1/muse_spotipy_recommendation/assets/71809159/f76c2985-c3f5-47a9-9e7f-1037b7cf7a94" alt="text" width="number" />
</p>

3. 사용자 플레이리스트와 추천 리스트 페이지 : 사용자의 플레이리스트를 볼 수 있고, 원하지 않는 음악은 삭제할 수 있게끔 함. 추천 리스트는 웹페이지 상단의 ‘recommend’를 클릭하면 알고리즘을 통해 자동으로 결과가 노출될 수 있도록 구

<p align="center">
  <img src="https://github.com/mugan1/muse_spotipy_recommendation/assets/71809159/b1d523b8-bf9f-42e9-a0f0-a97cb6daea6f" alt="text" width="number" />
</p>

4. 통계 그래프 페이지 : 사용자 플레이리스트와 추천 리스트 Audio Features를 비교 분석할 수 있게끔 JS를 통해 구현

<p align="center">
  <img src="https://github.com/mugan1/muse_spotipy_recommendation/assets/71809159/e4706f51-026b-4720-aaec-72c93e2a5aa2" alt="text" width="number" />
</p>

### Conclusion

  - 간단한 알고리즘을 활용한 웹 어플리케이션을 구축하면서, 큐레이션 시스템에 대한 기본 이해를 익힐 수 있었음
  - 추천 알고리즘에 대한 연구와 고도화는 지속적으로 데이터를 활용한 콘텐츠 산업 발전에 많은 영향을 미칠 것으로 보임 
