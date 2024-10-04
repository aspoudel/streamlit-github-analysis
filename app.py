import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Github Dashboard", page_icon=":bar_chart:", layout="wide")

st.markdown(
  """
    <style>
        h1 {
            font-size: 20px;
            color: #4CAF50;
            text-align: center;
            margin-top: 10px;
            padding: 0;
        }
        
        .block-container {
            padding: 0px 20px;
        }
    </style>
  """, unsafe_allow_html=True
)

st.title("Github Repository Analytics Dashboard")

@st.cache_data
def get_data_from_csv():  
  df = pd.read_csv("repository_data.csv", skiprows = 0)
  df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
  df = df[df['created_at'].dt.year <= 2022]
  df = df.drop(columns=['languages_used'], errors='ignore')
  return df

df = get_data_from_csv()

# Primary language vs Count of repositories
top_languages = df['primary_language'].value_counts().head(30)

fig_top_languages = px.bar(
  top_languages,
  x = top_languages.index,
  y = top_languages.values,
  labels = {'primary_language': 'Primary Language', 'y': 'Count of repositories'},
  title = "Top 30 all time popular languages"
)

# Stars Count vs repo percentiles
sorted_df = df.sort_values(by="stars_count", ascending=False)

total_repos = len(sorted_df)

top_25_count = int(total_repos * 0.25)
top_50_count = int(total_repos * 0.50)
top_75_count = int(total_repos * 0.75)

total_stars_25 = sorted_df.iloc[:top_25_count]['stars_count'].sum()
total_stars_50 = sorted_df.iloc[:top_50_count]['stars_count'].sum()
total_stars_75 = sorted_df.iloc[:top_75_count]['stars_count'].sum()
total_stars_100 = sorted_df["stars_count"].sum()

quantile_df = pd.DataFrame({
  'Percentile': ['Top 25%', 'Top 50%', 'Top 75%', 'Top 100%'],
  'Stars Count': [total_stars_25, total_stars_50, total_stars_75, total_stars_100]
})

fig_quantile_stars = px.bar(
  quantile_df,
  x = 'Percentile',
  y = 'Stars Count',
  title = 'Total Stars by Repository Percentiles shows<br> that most of the stars belong to the top 25 percentile<br> of the repos',
  text = "Stars Count"
)

df['year'] = df['created_at'].dt.year

# Total number of repositories by year
repo_count_by_year = df.groupby('year').size().reset_index(name='count')

fig_repo_year = px.bar(
  repo_count_by_year,
  x = 'year',
  y = 'count',
  labels = {'year': 'Year', 'count': 'Repository Count'},
  title = 'Repository Count by Year showing a<br> spike during covid-19',
)

# Total number of stars by year
stars_by_year = df.groupby('year')['stars_count'].sum().reset_index()

fig_stars_year = px.bar(
  stars_by_year,
  x = 'year',
  y = 'stars_count',
  labels = {'year': 'Year', 'stars_count': 'Total Stars'},
  title = 'Total Stars by Year indicates that 2016 saw<br> an increase in the activity of people'
)

left_column1, left_column2, right_column1, right_column2 = st.columns(4)
left_column1.plotly_chart(fig_top_languages, use_container_width=True)
left_column2.plotly_chart(fig_quantile_stars, use_container_width=True)
right_column1.plotly_chart(fig_repo_year, use_container_width=True)
right_column2.plotly_chart(fig_stars_year, use_container_width=True)

# Number of forks count by primary language for the top 10 forks count
forks_by_language = df.groupby('primary_language')['forks_count'].sum().reset_index()

top_forks_by_language = forks_by_language.sort_values(by='forks_count', ascending=False).head(10)

bottom_forks_by_language = forks_by_language.sort_values(by='forks_count', ascending=False).tail(10)

top_forks_by_language['category'] = 'Top 10'
bottom_forks_by_language['category'] = 'Bottom 10'

combined_forks = pd.concat([top_forks_by_language, bottom_forks_by_language])

fig_forks_language = px.bar(
  combined_forks,
  x = 'primary_language',
  y = 'forks_count',
  color='category',
  labels = {'primary_language': 'Primary Language', 'forks_count': 'Total Forks', 'category': '<b>Category</b>'},
  title = 'Top 10 and Bottom 10 Total Forks by Primary<br> Language showing some language have grown very old'
)

# Pull requests vs primary language
pull_requests_by_language = df.groupby('primary_language')['pull_requests'].sum().reset_index()

top_pull_requests_by_language = pull_requests_by_language.sort_values(by="pull_requests", ascending=False).head(30)

fig_pull_requests_language = px.bar(
  top_pull_requests_by_language,
  x = 'primary_language',
  y = 'pull_requests',
  labels = {'primary_language': 'Primary Language', 'pull_requests': 'Pull Requests'},
  title = 'Top 30 Pull Requests by Language',
)

# Stars Count vs primary language
stars_count_by_language = df.groupby('primary_language')['stars_count'].sum().reset_index()

top_stars_count_by_language = stars_count_by_language.sort_values(by="stars_count", ascending=False).head(30)

fig_stars_language = px.bar(
  top_stars_count_by_language,
  x = 'primary_language',
  y = 'stars_count',
  labels = {'primary_language': 'Primary Language', 'stars_count': 'Stars Count'},
  title = 'Top 30 Stars Count by Language',
)

# Commit Count vs year
commit_count_by_year = df.groupby('year')['commit_count'].sum().reset_index()

fig_commit_year = px.bar(
  commit_count_by_year,
  x = 'year',
  y = 'commit_count',
  labels = {'commit_count': 'Commit Count', 'year': 'Year'},
  title = 'Commit Count by Year showing a peak during covid<br> which shows people putting in efforts during WHF',
)

top_5_languages = df['primary_language'].value_counts().head(5).index

df_top_languages = df[df['primary_language'].isin(top_5_languages)]

# Top 5 languages count by year
repo_count_by_lang_year = df_top_languages.groupby(['year', 'primary_language']).size().reset_index(name='repo_count')

fig_repo_count = px.bar(
    repo_count_by_lang_year,
    x='year',
    y='repo_count',
    color='primary_language',
    labels={'year': 'Year', 'repo_count': 'Repository Count', 'primary_language': 'Primary Language'},
    title='Repository Count per Top 5 Languages by Year showing<br> a neck to neck battle between Python and Javascript',
    barmode='stack'
)

# Top 5 languages count by commit count by year
commit_count_by_lang_year = df_top_languages.groupby(['year', 'primary_language'])['commit_count'].sum().reset_index()

fig_commit_count = px.bar(
    commit_count_by_lang_year,
    x='year',
    y='commit_count',
    color='primary_language',
    labels={'year': 'Year', 'commit_count': 'Commit Count', 'primary_language': 'Primary Language'},
    title='Commit Count per Top 5 Languages by Year<br> showing even though C++ and Java are not<br> at the top of repo counts, people are still<br> contributing to legacy repos',
    barmode='stack'
)

left_column1, left_column2, right_column1, right_column2 = st.columns(4)
left_column1.plotly_chart(fig_forks_language, use_container_width=True)
left_column2.plotly_chart(fig_commit_year, use_container_width=True)
right_column1.plotly_chart(fig_repo_count, use_container_width=True)
right_column2.plotly_chart(fig_commit_count, use_container_width=True)

hide_st_style = """
                <style>
                #MainMenu {visibility: collapse;}
                footer {visibility: collapse;}
                header {visibility: collapse;}
                </style>
                """

st.markdown(hide_st_style, unsafe_allow_html=True)