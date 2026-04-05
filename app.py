import pandas as pd
import streamlit as st
import plotly.express as px

# Page config
st.set_page_config(page_title="Job Recommender", layout="wide")

# Title
st.markdown("<h1 style='text-align:center;'>💼 Job Recommendation System</h1>", unsafe_allow_html=True)

# Load data
df = pd.read_csv("jobs.csv")
df['skills'] = df['skills'].apply(lambda x: x.split(','))

# 🔥 TOP FILTER BAR (NOT SIDEBAR)
col1, col2, col3, col4 = st.columns(4)

with col1:
    user_skills = st.text_input("Skills", "python")

with col2:
    user_exp = st.slider("Experience", 1, 4, 1)

with col3:
    location = st.selectbox("Location", df['location'].unique())

with col4:
    job_type = st.selectbox("Job Type", df['job_type'].unique())

# Button
search = st.button("🚀 Search Jobs")

# Match function
def match_score(job_skills, user_skills):
    return len(set(job_skills).intersection(set(user_skills)))

if search:
    user_skills = [s.strip().lower() for s in user_skills.split(',')]

    df['score'] = df['skills'].apply(lambda x: match_score(x, user_skills))

    result = df[
        (df['score'] > 0) &
        (df['experience'] <= user_exp) &
        (df['location'] == location) &
        (df['job_type'] == job_type)
    ]

    result = result.sort_values(by=['score','rating','salary'], ascending=False)

    st.success(f"🔥 {len(result)} Jobs Found")

    # 🔥 JOB CARDS
    for _, row in result.head(10).iterrows():
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg,#1f1f1f,#2c2c2c);
            padding:20px;
            border-radius:12px;
            margin-bottom:12px;
            color:white;
            box-shadow:0 4px 10px rgba(0,0,0,0.4);
        ">
        <h3>{row['job_title']}</h3>
        💰 Salary: ₹{row['salary']} <br>
        🏢 {row['company']} | 📍 {row['location']} <br>
        ⭐ Rating: {row['rating']} <br>
        🧠 Skills: {", ".join(row['skills'])}
        </div>
        """, unsafe_allow_html=True)

    # 🔥 PLOTLY CHARTS (INTERACTIVE)
    st.markdown("## 📊 Analytics Dashboard")

    colA, colB = st.columns(2)

    with colA:
        fig1 = px.histogram(result, x="salary", title="Salary Distribution")
        st.plotly_chart(fig1, use_container_width=True)

    with colB:
        fig2 = px.bar(result.head(10), x="job_title", y="salary", title="Top Jobs Salary")
        st.plotly_chart(fig2, use_container_width=True)

    # 🔥 BONUS: SKILL COUNT
    all_skills = []
    for skills in result['skills']:
        all_skills.extend(skills)

    skill_df = pd.DataFrame(all_skills, columns=["skill"])
    skill_count = skill_df['skill'].value_counts().reset_index()

    fig3 = px.pie(skill_count.head(5), values='count', names='skill', title="Top Skills")
    st.plotly_chart(fig3, use_container_width=True)