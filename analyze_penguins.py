import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import koreanize_matplotlib
import urllib.request
from pathlib import Path
import matplotlib as mpl
import matplotlib.font_manager as fm


def ensure_dir(p):
    os.makedirs(p, exist_ok=True)


def savefig(figpath):
    plt.tight_layout()
    plt.savefig(figpath, dpi=150)
    plt.close()


def main():
    output_dir = "output"
    ensure_dir(output_dir)

    # 한글 폰트 설정 (koreanize-matplotlib 사용), seaborn 스타일 사용 안 함
    koreanize_matplotlib.koreanize()
    plt.style.use('default')

    # 로컬에 한글 폰트가 없으면 Noto Sans KR을 다운로드하여 matplotlib에 등록
    font_dir = Path("fonts")
    font_dir.mkdir(exist_ok=True)
    font_path = font_dir / "NotoSansKR-Regular.otf"
    if not font_path.exists():
        url = "https://github.com/googlefonts/noto-cjk/raw/main/Sans/OTF/Korean/NotoSansKR-Regular.otf"
        try:
            urllib.request.urlretrieve(url, str(font_path))
        except Exception:
            pass
    try:
        fm.fontManager.addfont(str(font_path))
        font_name = fm.FontProperties(fname=str(font_path)).get_name()
        mpl.rcParams['font.family'] = font_name
    except Exception:
        pass

    # 시스템에 설치된 한글 글꼴(nanum, noto 등)을 찾아 우선적으로 사용하도록 설정
    try:
        system_fonts = fm.findSystemFonts()
        preferred = None
        for fp in system_fonts:
            try:
                name = fm.FontProperties(fname=fp).get_name()
            except Exception:
                continue
            lname = name.lower()
            if 'nanum' in lname or 'noto' in lname or 'nanum gothic' in lname or 'noto sans' in lname:
                preferred = name
                break
        if preferred:
            mpl.rcParams['font.family'] = preferred
    except Exception:
        pass
    penguins = sns.load_dataset("penguins")

    # Basic cleaning
    df = penguins.copy()
    df = df.dropna()

    # Summary CSV
    df.describe(include='all').to_csv(os.path.join(output_dir, "summary.csv"))

    images = []

    # 1 Histogram: body_mass_g
    plt.figure()
    sns.histplot(df['body_mass_g'], kde=True, bins=20)
    plt.title('체중 분포 (g)')
    p = os.path.join(output_dir, "hist_body_mass.png")
    savefig(p)
    images.append(p)

    # 2 Histogram: flipper_length_mm by species (stacked via facet)
    g = sns.displot(df, x='flipper_length_mm', hue='species', kind='kde', fill=True)
    g.fig.suptitle('지느러미 길이 KDE (종별)')
    p = os.path.join(output_dir, "kde_flipper_by_species.png")
    g.tight_layout()
    g.savefig(p)
    plt.close()
    images.append(p)

    # 3 Scatter: body_mass vs flipper_length colored by species
    plt.figure()
    sns.scatterplot(data=df, x='flipper_length_mm', y='body_mass_g', hue='species', style='sex')
    plt.title('지느러미 길이 vs 체중 (종별)')
    p = os.path.join(output_dir, "scatter_flipper_bodymass.png")
    savefig(p)
    images.append(p)

    # 4 Pairplot
    pp = sns.pairplot(df[['bill_length_mm','bill_depth_mm','flipper_length_mm','body_mass_g','species']], hue='species')
    pp.fig.suptitle('특성 간 관계 (종별)')
    p = os.path.join(output_dir, "pairplot.png")
    pp.tight_layout()
    pp.savefig(p)
    plt.close()
    images.append(p)

    # 5 Boxplot: body_mass_g by species
    plt.figure()
    sns.boxplot(data=df, x='species', y='body_mass_g')
    plt.title('종별 체중 분포 (박스)')
    p = os.path.join(output_dir, "box_bodymass_by_species.png")
    savefig(p)
    images.append(p)

    # 6 Violin: flipper_length_mm by species
    plt.figure()
    sns.violinplot(data=df, x='species', y='flipper_length_mm')
    plt.title('종별 지느러미 길이 분포 (바이올린)')
    p = os.path.join(output_dir, "violin_flipper_by_species.png")
    savefig(p)
    images.append(p)

    # 7 Countplot (bar chart): species counts
    plt.figure()
    sns.countplot(data=df, x='species')
    plt.title('종별 개수')
    p = os.path.join(output_dir, "count_species.png")
    savefig(p)
    images.append(p)

    # 8 Barplot: mean body_mass_g by island (bar chart)
    plt.figure()
    sns.barplot(data=df, x='island', y='body_mass_g', errorbar='sd')
    plt.title('섬별 평균 체중 (g)')
    p = os.path.join(output_dir, "bar_bodymass_by_island.png")
    savefig(p)
    images.append(p)

    # 9 Swarmplot: bill_length_mm by species
    plt.figure(figsize=(8,5))
    sns.swarmplot(data=df, x='species', y='bill_length_mm', hue='sex', dodge=True)
    plt.title('종별 부리 길이 (성별 구분)')
    p = os.path.join(output_dir, "swarm_bill_length_by_species.png")
    savefig(p)
    images.append(p)

    # 10 KDE of body_mass_g
    plt.figure()
    sns.kdeplot(data=df, x='body_mass_g', hue='species', fill=True)
    plt.title('종별 체중 KDE')
    p = os.path.join(output_dir, "kde_body_mass_by_species.png")
    savefig(p)
    images.append(p)

    # 11 Correlation heatmap
    plt.figure(figsize=(6,5))
    corr = df[['bill_length_mm','bill_depth_mm','flipper_length_mm','body_mass_g']].corr()
    sns.heatmap(corr, annot=True, cmap='vlag')
    plt.title('특성 상관행렬')
    p = os.path.join(output_dir, "heatmap_corr.png")
    savefig(p)
    images.append(p)

    # 12 FacetGrid scatter: bill_length vs bill_depth per species
    g = sns.FacetGrid(df, col='species')
    g.map_dataframe(sns.scatterplot, 'bill_length_mm', 'bill_depth_mm', hue='sex')
    g.fig.suptitle('부리 길이 vs 부리 깊이 (종별)')
    p = os.path.join(output_dir, "facet_bill_scatter.png")
    g.tight_layout()
    g.savefig(p)
    plt.close()
    images.append(p)

    # Crosstab and pivot for bar charts
    ctab = pd.crosstab(df['species'], df['island'])
    pivot = pd.pivot_table(df, index='island', columns='species', values='body_mass_g', aggfunc='mean')

    # Save tables as CSV and markdown
    ctab.to_csv(os.path.join(output_dir, 'crosstab_species_island.csv'))
    pivot.to_csv(os.path.join(output_dir, 'pivot_island_species_bodymass_mean.csv'))

    try:
        ctab_md = ctab.to_markdown()
        pivot_md = pivot.to_markdown()
    except Exception:
        ctab_md = ctab.to_csv(sep='|')
        pivot_md = pivot.to_csv(sep='|')

    # Create report markdown
    report_path = os.path.join(output_dir, 'report.md')
    # 통계값 계산 (인사이트용)
    overall_n = len(df)
    species_counts = df['species'].value_counts().to_dict()
    species_means = df.groupby('species')['body_mass_g'].mean().round(1).to_dict()
    island_means = df.groupby('island')['body_mass_g'].mean().round(1).to_dict()
    corr_vals = corr.stack().round(2).to_dict()

    # 인사이트 텍스트 (한글, 각 항목 약 500자 내외)
    insights = {}
    insights['hist_body_mass.png'] = (
        f"펭귄의 체중(body_mass_g) 분포를 보면 중심 경향은 평균 {df['body_mass_g'].mean():.1f}g, "
        f"중앙값 {df['body_mass_g'].median():.1f}g로 관측됩니다. 히스토그램은 완만한 우측편향을 보이며, 저체중~중체중군이 주를 이룹니다. "
        "종(species) 간 차이를 함께 고려하면 Adelie와 Chinstrap은 상대적으로 체중이 낮고, Gentoo가 평균적으로 높은 편입니다. "
        "이 분포는 개체군의 생태적 적응(먹이, 서식지 등)과 연관되어 해석할 수 있으며, 이상치(고체중)는 표본 측정 오류 또는 특이 개체일 가능성을 검토해야 합니다."
    )

    insights['kde_flipper_by_species.png'] = (
        f"지느러미 길이(flipper_length_mm)의 KDE를 종별로 비교하면 종별 분포가 뚜렷히 구분됩니다. "
        f"예를 들어 평균 지느러미 길이는 Gentoo가 가장 길고(평균 약 {df[df['species']=='Gentoo']['flipper_length_mm'].mean():.1f}mm), Adelie와 Chinstrap는 짧은 편입니다. "
        "분포의 폭과 다중봉(다중 모드) 여부는 개체군 내 이질성 또는 측정 환경 차이를 시사할 수 있습니다. 종 간 겹침은 일부 특징이 상호 대체 가능함을 의미하지만, 전체적으로 종 판별에 유용한 변수임을 보여줍니다."
    )

    insights['scatter_flipper_bodymass.png'] = (
        "지느러미 길이와 체중의 산점도는 두 변수 사이에 양의 상관 경향이 있음을 보여줍니다. "
        "즉, 지느러미가 긴 개체일수록 체중이 큰 경향이 있어 체형(크기)의 전반적 스케일과 연관됩니다. "
        "다만 종(species) 또는 성별(sex)에 따라 군집이 형성되어 동일한 지느러미 길이에서 종별 체중 차이가 발생할 수 있으므로 군집별 회귀나 상호작용을 추가 분석하면 더 유의미한 해석이 가능합니다."
    )

    insights['pairplot.png'] = (
        "페어플롯은 다수의 연속형 특성 간 관계와 종별 분리를 한눈에 보여줍니다. "
        "특히 bill_length_mm, bill_depth_mm, flipper_length_mm, body_mass_g 간의 산점도에서 일부 변수 쌍은 선형적 관계를 띠고, 일부는 상관이 약합니다. "
        "종별 색상 분포는 변수 조합에 따라 종 분리가 잘되는 쌍이 있고 그렇지 않은 쌍이 있음을 나타내며, 이는 분류 모델에서 변수 선택에 유용한 정보를 제공합니다."
    )

    insights['box_bodymass_by_species.png'] = (
        f"종별 체중 박스플롯은 중앙값과 분포 범위를 비교하기에 적합합니다. Gentoo는 중앙값과 사분범위가 모두 높아 전반적으로 더 무겁고 변이도 큽니다. "
        "Adelie와 Chinstrap는 중앙값이 낮고 변이가 상대적으로 작아 표준화된 생태적 지위 차이를 반영할 수 있습니다. 이상치는 개체 수준의 예외 사례로 다루어야 합니다."
    )

    insights['violin_flipper_by_species.png'] = (
        "바이올린 플롯은 지느러미 길이의 분포 형태를 종별로 상세히 보여줍니다. "
        "밀도의 높고 낮음과 꼬리 길이를 통해 내부 구조(예: 다중 모드, 편향)를 파악할 수 있으며, Gentoo의 분포가 명확히 오른쪽으로 치우치거나 폭이 넓다면 개체군 내 이질성이 큽니다."
    )

    insights['count_species.png'] = (
        f"종별 개수(Count)를 보면 표본에서 관측된 종의 상대적 빈도를 확인할 수 있습니다. 본 데이터에서는 {', '.join([f'{k}:{v}' for k,v in species_counts.items()])}로 관측되어 특정 종이 더 많이 샘플링되었음을 알 수 있습니다. "
        "샘플링 편향 여부는 이후 분석(예: 분류, 평균 비교)에 영향을 줄 수 있으므로 가중치 보정이나 재표본추출을 고려할 수 있습니다."
    )

    insights['bar_bodymass_by_island.png'] = (
        f"섬(island)별 평균 체중 비교에서는 지역별 자원 차이나 서식 환경이 반영될 가능성이 있습니다. 예컨대 각 섬의 평균 체중은 {', '.join([f'{k}:{v}g' for k,v in island_means.items()])}로 계산되어 섬 간 차이가 존재합니다. "
        "이 차이는 먹이 가용성, 경쟁, 기후 등 생태적 요인으로 추가 조사할 만합니다."
    )

    insights['swarm_bill_length_by_species.png'] = (
        "스웜플롯은 개체 수준의 분포와 군집을 보여주며 성별(sex)에 따른 차이를 시각화합니다. "
        "동일 종 내에서도 성별에 따라 부리 길이 분포가 달라지는 경향이 보이면 성별을 고려한 분석이 필요합니다. 이는 생태적 역할 분화 또는 성적 이형성의 징후일 수 있습니다."
    )

    insights['kde_body_mass_by_species.png'] = (
        "종별 체중 KDE는 연속 밀도 비교를 통해 종 간 차이를 부드럽게 보여줍니다. "
        "중첩되는 부분이 있지만 피크 위치와 폭에서 종별 특성이 드러나며, 이것은 분류나 군집화에서 유용한 연속형 특징입니다."
    )

    insights['heatmap_corr.png'] = (
        "상관행렬 히트맵은 변수들 간 선형 상관 관계의 강도를 직관적으로 보여줍니다. "
        f"예를 들어 flipper_length_mm과 body_mass_g 간의 상관계수는 {corr.loc['flipper_length_mm','body_mass_g']:.2f}로, 비교적 강한 양의 상관을 시사합니다. "
        "이 정보는 차원 축소나 다중공선성 검사, 회귀 모델 변수 선택에 참고할 수 있습니다."
    )

    insights['facet_bill_scatter.png'] = (
        "종별로 분할된 산점도는 같은 변수 쌍에서 종별 패턴의 차이를 확인할 수 있게 해줍니다. "
        "종별로 점들의 위치나 분포가 다르면 변수의 종 판별력이 높다는 의미이며, 성별로 색을 나누면 추가적인 이질성도 파악됩니다."
    )

    insights['crosstab'] = (
        "교차표(species x island)는 종과 섬 간의 분포 관계를 보여주어 특정 종이 특정 섬에 집중 분포하는지 확인할 수 있습니다. "
        "이 패턴은 서식지 선호나 표본 수집 편향을 반영할 수 있으므로, 보전 계획이나 추가 표본 설계 시 중요한 단서를 제공합니다."
    )

    insights['pivot'] = (
        "피봇테이블(섬 x 종의 평균 체중)은 지역별로 동일 종의 체중 차이를 비교하게 해줍니다. "
        "섬 간 평균 체중 차이는 지역 생태계의 차이를 시사하므로, 통계적 유의성 검정(ANOVA 등)을 통해 차이가 유의한지 확인하는 후속 분석을 권장합니다."
    )
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('# Penguins Dataset Analysis\n\n')
        f.write('## Quick info\n')
        f.write(f'- Observations (after dropna): {len(df)}\n')
        f.write('\n')
        f.write('## Crosstab: species x island\n')
        f.write('\n')
        f.write('```\n')
        f.write(ctab_md)
        f.write('\n```\n')
        f.write('\n')
        f.write('## Pivot table: mean body_mass_g (island x species)\n')
        f.write('\n')
        f.write('```\n')
        f.write(pivot_md)
        f.write('\n```\n')
        f.write('\n')
        f.write('## Plots\n')
        f.write('\n')
        # 테이블 인사이트 삽입
        f.write('## Insights (교차표 및 피봇)\n\n')
        f.write(insights['crosstab'] + '\n\n')
        f.write(insights['pivot'] + '\n\n')

        # 플롯 이미지와 각 이미지 인사이트 삽입
        for img in images:
            name = os.path.basename(img)
            f.write(f'### {name}\n')
            key = name
            text = insights.get(key, '')
            if text:
                f.write(text + '\n\n')
            f.write(f'![{name}]({img})\n\n')

    print(f'Report and images written to: {output_dir}')


if __name__ == '__main__':
    main()
