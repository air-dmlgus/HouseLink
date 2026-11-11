<div align="center">

# HouseLink
### AI 기반 주거지역 추천 서비스 · 포트폴리오 재구현

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Demo](https://img.shields.io/badge/Type-Portfolio%20Demo-0D9488)

**치안 · 교육 · 의료 지표를 사용자의 선호도에 맞춰 비교하는 주거지 추천 데모**

</div>

> **프로젝트 구분:** Microsoft AI School 팀 프로젝트 발표 자료를 참고해 새로 작성한 간소화 재구현입니다. 원본 코드·모델·실제 공공데이터는 포함되어 있지 않습니다.
>
> **데이터 주의:** 지역명과 점수는 모두 가상 예시입니다. 실제 지역의 치안·교육·의료 수준을 뜻하지 않으며 거주지 결정에 사용하면 안 됩니다.

## 프로젝트 소개

원본 **HouseLink(하우스링크)** 는 치안, 교육, 의료/복지 등 지역 데이터를 비교해 주거지 선택을 돕는 것을 목표로 한 팀 프로젝트입니다. 발표 자료에는 공공데이터 수집 및 전처리, scikit-learn을 활용한 K-Means 군집화, 추천 점수 계산, Gradio 인터페이스 등이 소개되어 있습니다.

이 저장소에서는 핵심 아이디어를 **별도의 실행 가능한 Python 웹 데모**로 단순화했습니다.

## 핵심 기능

| 기능 | 구현 내용 |
| --- | --- |
| 선호도별 추천 | 균형 / 치안 / 교육 / 의료 중심 가중치로 순위 산출 |
| 지표 시각화 | 각 가상 지역의 3가지 점수를 막대 그래프로 표시 |
| 유사 지역 묶기 | 간단한 K-Means 방식으로 3개 군집 생성 |
| API | `GET /api/recommend?profile=balanced` |
| 자동 테스트 | 데이터 검증, 선호도별 점수, 군집화 재현성 검사 |

추천 점수 = (치안 점수 × 치안 가중치) + (교육 점수 × 교육 가중치) + (의료 점수 × 의료 가중치)

**군집 번호는 지역의 우열이나 실제 안전도 등급을 의미하지 않습니다.**

## 실행 방법

Python 3.10 이상이 필요하며, 별도의 외부 패키지 설치는 필요하지 않습니다.

```bash
git clone https://github.com/air-dmlgus/HouseLink.git
cd HouseLink
python app.py
```

브라우저에서 **http://127.0.0.1:8000** 을 열면 됩니다.

### 테스트

```bash
python -m unittest discover -s tests -v
```

### API 예시

- `/api/recommend?profile=balanced`
- `/api/recommend?profile=safety`
- `/api/recommend?profile=education`
- `/api/recommend?profile=medical`

## 기술 스택

- **Python** — 추천 점수, 데이터 처리, K-Means 구현
- **HTML · CSS · JavaScript** — 추천 기준 선택 및 결과 시각화
- **CSV · unittest** — 샘플 데이터와 단위 테스트
- **Python 표준 라이브러리 HTTP 서버** — 웹 데모 및 API

## 폴더 구성

```text
HouseLink/
├── app.py
├── recommender.py
├── data/sample_areas.csv
├── tests/test_recommender.py
├── .gitignore
└── README.md
```

## 원본 팀 프로젝트에서 담당한 업무

**Microsoft AI School · Team14 · 이의현**

- 치안 관련 데이터 수집 (소방서·119안전센터, 경찰 관련 시설, CCTV)
- 서울 지역 관련 자료 추출, 데이터 전처리와 유사 데이터 병합
- 발표자료 제작 참여

원본 발표자료에는 송민규가 팀장으로 기재되어 있습니다. 원본 팀 프로젝트에서 담당한 업무와 **이 저장소의 새 코드 구현**을 구분해 설명합니다.

## 원본과 이 데모의 차이

| 구분 | 원본 프로젝트 | 이 저장소 |
| --- | --- | --- |
| 데이터 | 공공기관의 실제 시설 데이터 | 가상 지역·임의 점수 |
| 분석 | scikit-learn 기반 K-Means 등 | 직접 구현한 학습용 K-Means |
| UI | Gradio 등 사용 | Python 서버 + HTML/CSS/JS |
| 목적 | 실제 프로젝트 팀 작업 | 구현 흐름을 보여주는 포트폴리오 예제 |

## 향후 개선

1. 출처와 갱신일이 명시된 실제 공공데이터 연결
2. 시설까지의 거리·접근성 지표 설계 및 검증
3. 정규화와 가중치 선정 근거 공개
4. 지도 표시와 지역별 상세 비교 화면
5. 정식 데이터 검증과 성능 평가

---

**Portfolio reconstruction** · 원본 팀 프로젝트와 독립적으로 재구현한 학습용 데모
