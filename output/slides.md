# 펭귄 데이터 분석 슬라이드

---

## 제목

펭귄 데이터셋 분석

저자: 분석 스크립트 자동 생성

---

## 개요

- 목적: 펭귄 데이터 시각화 및 인사이트 제공
- 포함: 교차표, 피봇, 12개 이상 시각화 및 분석 인사이트

---

## 요약 정보

- 결측치 제거 후 관측치 수: 333

---

## 데이터셋 설명

- 변수: species, island, bill_length_mm, bill_depth_mm, flipper_length_mm, body_mass_g, sex
- 출처: seaborn 내장 `penguins` 데이터셋

---

## 분석 방법론

- 데이터 정제: 결측값 제거
- 시각화: 히스토그램, KDE, 박스/바이올린, 산점도, 페어플롯, 히트맵 등
- 표: 교차표(species x island), 피봇(섬 x 종 평균 체중)

---

## 교차표: species x island

| species   |   Biscoe |   Dream |   Torgersen |
|:----------|---------:|--------:|------------:|
| Adelie    |       44 |      55 |          47 |
| Chinstrap |        0 |      68 |           0 |
| Gentoo    |      119 |       0 |           0 |

설명: 종별로 특정 섬에 편중된 표본 분포가 관측됩니다. 보전 및 추가 표본설계 시 참고하세요.

---

## 피봇테이블: 섬 x 종 평균 체중

| island    |   Adelie |   Chinstrap |   Gentoo |
|:----------|---------:|------------:|---------:|
| Biscoe    |  3709.66 |      nan    |  5092.44 |
| Dream     |  3701.36 |     3733.09 |   nan    |
| Torgersen |  3708.51 |      nan    |   nan    |

설명: 섬별로 동일 종의 평균 체중 차이가 존재할 수 있으며, 추가 통계 검정으로 확인 권장.

---

## 히스토그램: 체중 분포

![히스토그램: 체중 분포](output/hist_body_mass.png)

설명: 체중은 약간 우측편향이며 Gentoo가 상대적으로 더 무겁습니다.

---

## KDE: 지느러미 길이 (종별)

![KDE: 지느러미 길이(종별)](output/kde_flipper_by_species.png)

설명: Gentoo가 평균 지느러미 길이가 길며 종별 분포 차이가 뚜렷합니다.

---

## 산점도: 지느러미 길이 vs 체중

![산점도: 지느러미 vs 체중](output/scatter_flipper_bodymass.png)

설명: 양의 상관관계가 관찰되며 종별 군집이 존재합니다.

---

## 페어플롯

![페어플롯](output/pairplot.png)

설명: 변수쌍마다 종 분리력 차이가 있으며, 분류모형 변수 선택 시 참고됩니다.

---

## 박스플롯: 종별 체중

![박스플롯: 종별 체중](output/box_bodymass_by_species.png)

설명: Gentoo는 중앙값이 높고 변동성도 큽니다.

---

## 바이올린: 지느러미 길이(종별)

![바이올린: 지느러미 길이](output/violin_flipper_by_species.png)

설명: 분포 형태와 내부 구조(다중 모드 등)를 보여줍니다.

---

## 종별 카운트

![종별 카운트](output/count_species.png)

설명: Adelie 표본이 가장 많아 표본 편향 가능성이 있습니다.

---

## 섬별 평균 체중(바 차트)

![섬별 평균 체중](output/bar_bodymass_by_island.png)

설명: 섬 간 체중 차이는 지역적 생태 요인을 시사합니다.

---

## 스웜플롯: 부리 길이(종별)

![스웜플롯: 부리 길이](output/swarm_bill_length_by_species.png)

설명: 개체 수준 분포를 보여주며 성별/종별 차이를 파악할 수 있습니다.

---

## 종별 체중 KDE

![종별 체중 KDE](output/kde_body_mass_by_species.png)

설명: 연속 밀도 비교로 종별 특성 및 중첩 정도를 확인합니다.

---

## 상관행렬 히트맵

![상관행렬 히트맵](output/heatmap_corr.png)

설명: flipper_length_mm과 body_mass_g는 강한 양의 상관(약 0.87)을 보입니다.

---

## 종별 분할 산점도

![종별 분할 산점도](output/facet_bill_scatter.png)

설명: 종별 패턴 차이로 변수의 판별력을 확인할 수 있습니다.

---

## 요약 및 권장사항

- 주요 발견: 종별 체중 및 지느러미 길이 차이 뚜렷, 섬별 체중 차이 관찰, 표본 수 불균형.
- 권장: (1) 섬 간 차이 통계검정, (2) 표본 편향 보정, (3) 분류모델 실험(교차검증).

---

## 부록: 파일 및 테이블

- 결과 파일: `output/summary.csv`, `output/crosstab_species_island.csv`, `output/pivot_island_species_bodymass_mean.csv`
- 모든 시각화 이미지: output/ 폴더 참조
