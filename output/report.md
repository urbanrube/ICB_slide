# Penguins Dataset Analysis

## Quick info
- Observations (after dropna): 333

## Crosstab: species x island

```
| species   |   Biscoe |   Dream |   Torgersen |
|:----------|---------:|--------:|------------:|
| Adelie    |       44 |      55 |          47 |
| Chinstrap |        0 |      68 |           0 |
| Gentoo    |      119 |       0 |           0 |
```

## Pivot table: mean body_mass_g (island x species)

```
| island    |   Adelie |   Chinstrap |   Gentoo |
|:----------|---------:|------------:|---------:|
| Biscoe    |  3709.66 |      nan    |  5092.44 |
| Dream     |  3701.36 |     3733.09 |   nan    |
| Torgersen |  3708.51 |      nan    |   nan    |
```

## Plots

## Insights (교차표 및 피봇)

교차표(species x island)는 종과 섬 간의 분포 관계를 보여주어 특정 종이 특정 섬에 집중 분포하는지 확인할 수 있습니다. 이 패턴은 서식지 선호나 표본 수집 편향을 반영할 수 있으므로, 보전 계획이나 추가 표본 설계 시 중요한 단서를 제공합니다.

피봇테이블(섬 x 종의 평균 체중)은 지역별로 동일 종의 체중 차이를 비교하게 해줍니다. 섬 간 평균 체중 차이는 지역 생태계의 차이를 시사하므로, 통계적 유의성 검정(ANOVA 등)을 통해 차이가 유의한지 확인하는 후속 분석을 권장합니다.

### hist_body_mass.png
펭귄의 체중(body_mass_g) 분포를 보면 중심 경향은 평균 4207.1g, 중앙값 4050.0g로 관측됩니다. 히스토그램은 완만한 우측편향을 보이며, 저체중~중체중군이 주를 이룹니다. 종(species) 간 차이를 함께 고려하면 Adelie와 Chinstrap은 상대적으로 체중이 낮고, Gentoo가 평균적으로 높은 편입니다. 이 분포는 개체군의 생태적 적응(먹이, 서식지 등)과 연관되어 해석할 수 있으며, 이상치(고체중)는 표본 측정 오류 또는 특이 개체일 가능성을 검토해야 합니다.

![hist_body_mass.png](output/hist_body_mass.png)

### kde_flipper_by_species.png
지느러미 길이(flipper_length_mm)의 KDE를 종별로 비교하면 종별 분포가 뚜렷히 구분됩니다. 예를 들어 평균 지느러미 길이는 Gentoo가 가장 길고(평균 약 217.2mm), Adelie와 Chinstrap는 짧은 편입니다. 분포의 폭과 다중봉(다중 모드) 여부는 개체군 내 이질성 또는 측정 환경 차이를 시사할 수 있습니다. 종 간 겹침은 일부 특징이 상호 대체 가능함을 의미하지만, 전체적으로 종 판별에 유용한 변수임을 보여줍니다.

![kde_flipper_by_species.png](output/kde_flipper_by_species.png)

### scatter_flipper_bodymass.png
지느러미 길이와 체중의 산점도는 두 변수 사이에 양의 상관 경향이 있음을 보여줍니다. 즉, 지느러미가 긴 개체일수록 체중이 큰 경향이 있어 체형(크기)의 전반적 스케일과 연관됩니다. 다만 종(species) 또는 성별(sex)에 따라 군집이 형성되어 동일한 지느러미 길이에서 종별 체중 차이가 발생할 수 있으므로 군집별 회귀나 상호작용을 추가 분석하면 더 유의미한 해석이 가능합니다.

![scatter_flipper_bodymass.png](output/scatter_flipper_bodymass.png)

### pairplot.png
페어플롯은 다수의 연속형 특성 간 관계와 종별 분리를 한눈에 보여줍니다. 특히 bill_length_mm, bill_depth_mm, flipper_length_mm, body_mass_g 간의 산점도에서 일부 변수 쌍은 선형적 관계를 띠고, 일부는 상관이 약합니다. 종별 색상 분포는 변수 조합에 따라 종 분리가 잘되는 쌍이 있고 그렇지 않은 쌍이 있음을 나타내며, 이는 분류 모델에서 변수 선택에 유용한 정보를 제공합니다.

![pairplot.png](output/pairplot.png)

### box_bodymass_by_species.png
종별 체중 박스플롯은 중앙값과 분포 범위를 비교하기에 적합합니다. Gentoo는 중앙값과 사분범위가 모두 높아 전반적으로 더 무겁고 변이도 큽니다. Adelie와 Chinstrap는 중앙값이 낮고 변이가 상대적으로 작아 표준화된 생태적 지위 차이를 반영할 수 있습니다. 이상치는 개체 수준의 예외 사례로 다루어야 합니다.

![box_bodymass_by_species.png](output/box_bodymass_by_species.png)

### violin_flipper_by_species.png
바이올린 플롯은 지느러미 길이의 분포 형태를 종별로 상세히 보여줍니다. 밀도의 높고 낮음과 꼬리 길이를 통해 내부 구조(예: 다중 모드, 편향)를 파악할 수 있으며, Gentoo의 분포가 명확히 오른쪽으로 치우치거나 폭이 넓다면 개체군 내 이질성이 큽니다.

![violin_flipper_by_species.png](output/violin_flipper_by_species.png)

### count_species.png
종별 개수(Count)를 보면 표본에서 관측된 종의 상대적 빈도를 확인할 수 있습니다. 본 데이터에서는 Adelie:146, Gentoo:119, Chinstrap:68로 관측되어 특정 종이 더 많이 샘플링되었음을 알 수 있습니다. 샘플링 편향 여부는 이후 분석(예: 분류, 평균 비교)에 영향을 줄 수 있으므로 가중치 보정이나 재표본추출을 고려할 수 있습니다.

![count_species.png](output/count_species.png)

### bar_bodymass_by_island.png
섬(island)별 평균 체중 비교에서는 지역별 자원 차이나 서식 환경이 반영될 가능성이 있습니다. 예컨대 각 섬의 평균 체중은 Biscoe:4719.2g, Dream:3718.9g, Torgersen:3708.5g로 계산되어 섬 간 차이가 존재합니다. 이 차이는 먹이 가용성, 경쟁, 기후 등 생태적 요인으로 추가 조사할 만합니다.

![bar_bodymass_by_island.png](output/bar_bodymass_by_island.png)

### swarm_bill_length_by_species.png
스웜플롯은 개체 수준의 분포와 군집을 보여주며 성별(sex)에 따른 차이를 시각화합니다. 동일 종 내에서도 성별에 따라 부리 길이 분포가 달라지는 경향이 보이면 성별을 고려한 분석이 필요합니다. 이는 생태적 역할 분화 또는 성적 이형성의 징후일 수 있습니다.

![swarm_bill_length_by_species.png](output/swarm_bill_length_by_species.png)

### kde_body_mass_by_species.png
종별 체중 KDE는 연속 밀도 비교를 통해 종 간 차이를 부드럽게 보여줍니다. 중첩되는 부분이 있지만 피크 위치와 폭에서 종별 특성이 드러나며, 이것은 분류나 군집화에서 유용한 연속형 특징입니다.

![kde_body_mass_by_species.png](output/kde_body_mass_by_species.png)

### heatmap_corr.png
상관행렬 히트맵은 변수들 간 선형 상관 관계의 강도를 직관적으로 보여줍니다. 예를 들어 flipper_length_mm과 body_mass_g 간의 상관계수는 0.87로, 비교적 강한 양의 상관을 시사합니다. 이 정보는 차원 축소나 다중공선성 검사, 회귀 모델 변수 선택에 참고할 수 있습니다.

![heatmap_corr.png](output/heatmap_corr.png)

### facet_bill_scatter.png
종별로 분할된 산점도는 같은 변수 쌍에서 종별 패턴의 차이를 확인할 수 있게 해줍니다. 종별로 점들의 위치나 분포가 다르면 변수의 종 판별력이 높다는 의미이며, 성별로 색을 나누면 추가적인 이질성도 파악됩니다.

![facet_bill_scatter.png](output/facet_bill_scatter.png)

