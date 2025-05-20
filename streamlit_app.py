import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns

# Page Configuration
st.set_page_config(
    page_title="Cognitive Score Predictor",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# IT-themed Color Palette
primary_color = "#0078D7"
secondary_color = "#106EBE"
accent_color = "#2B88D8"
background_color = "#F5F5F5"
text_color = "#333333"

# Custom CSS
st.markdown(f"""
<style>
    body {{
        background-color: {background_color};
        color: {text_color};
    }}
    .main .block-container {{
        padding: 2rem;
        font-family: "Segoe UI", sans-serif;
    }}
    h1, h2, h3 {{
        color: {primary_color};
        font-weight: 700;
    }}
    .stButton>button {{
        background-color: {primary_color};
        color: white;
        border-radius: 10px;
        padding: 0.5rem 1.2rem;
        font-size: 1rem;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
    }}
    .stButton>button:hover {{
        background-color: {secondary_color};
        transition: 0.3s ease-in-out;
    }}
    .css-1v3fvcr, .css-1d391kg {{
        border: 1px solid {accent_color};
        border-radius: 1rem;
        padding: 1.2rem;
        background-color: #ffffff;
        box-shadow: 2px 2px 12px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
    }}
    .sidebar .sidebar-content {{
        background-color: {background_color};
    }}
</style>
""", unsafe_allow_html=True)

# Title
st.title("🧠 Cognitive Score Predictor")
st.markdown("Predict your cognitive score based on lifestyle and mental performance indicators.")

# Load Data (fallback to dummy if not found)
try:
    sample_data = pd.read_csv('/home/ubuntu/cognitive_app/data_subset.csv')
    has_sample_data = True
except:
    has_sample_data = False
    sample_data = pd.DataFrame({
        'Age': [18, 59],
        'Sleep_Duration': [4.0, 10.0],
        'Stress_Level': [1, 10],
        'Daily_Screen_Time': [1.0, 12.0],
        'Caffeine_Intake': [0, 500],
        'Reaction_Time': [200.0, 600.0],
        'Memory_Test_Score': [40, 100]
    })

# Sidebar Inputs
st.sidebar.header("🧾 Your Inputs")

with st.sidebar.expander("👤 Personal Information", expanded=True):
    age = st.slider("Age", 18, 59, 30)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])

with st.sidebar.expander("💬 Lifestyle Factors", expanded=True):
    sleep_duration = st.slider("Sleep Duration (hrs)", 4.0, 10.0, 7.0, 0.1)
    stress_level = st.slider("Stress Level (1-10)", 1, 10, 5)
    diet_type = st.selectbox("Diet Type", ["Non-Vegetarian", "Vegetarian", "Vegan"])
    daily_screen_time = st.slider("Screen Time (hrs)", 1.0, 12.0, 6.0, 0.1)
    exercise_frequency = st.selectbox("Exercise Frequency", ["Low", "Medium", "High"])
    caffeine_intake = st.slider("Caffeine Intake (mg)", 0, 500, 150)

with st.sidebar.expander("🧠 Cognitive Metrics", expanded=True):
    reaction_time = st.slider("Reaction Time (ms)", 200.0, 600.0, 350.0, 0.1)
    memory_test_score = st.slider("Memory Test Score", 40, 100, 70)

# Prediction Function
def predict_cognitive_score(age, gender, sleep_duration, stress_level, diet_type,
                            daily_screen_time, exercise_frequency, caffeine_intake,
                            reaction_time, memory_test_score):
    gender_factor = {'Male': 0, 'Female': 0, 'Other': 0}
    diet_factor = {'Non-Vegetarian': 0, 'Vegetarian': 0.5, 'Vegan': 1}
    exercise_factor = {'Low': 0, 'Medium': 0.5, 'High': 1}
    
    age_norm = 1 - ((age - 18) / (59 - 18))
    sleep_quality = 1 - abs(sleep_duration - 8) / 4
    stress_impact = 1 - (stress_level / 10)
    screen_impact = 1 - (daily_screen_time / 12)
    caffeine_impact = 1 - (abs(caffeine_intake - 200) / 300)
    reaction_impact = 1 - ((reaction_time - 200) / 400)
    memory_impact = memory_test_score / 100

    score = (
        0.10 * age_norm +
        0.15 * sleep_quality +
        0.15 * stress_impact +
        0.05 * diet_factor[diet_type] +
        0.10 * screen_impact +
        0.15 * exercise_factor[exercise_frequency] +
        0.05 * caffeine_impact +
        0.10 * reaction_impact +
        0.15 * memory_impact
    )
    
    return max(0, min(100, score * 100))

# Layout Columns
col1, col2 = st.columns([2, 1], gap="large")

with col1:
    st.header("🔍 Prediction")
    st.markdown("Click the button below to compute your cognitive score.")
    
    if st.button("Predict Cognitive Score"):
        prediction = predict_cognitive_score(
            age, gender, sleep_duration, stress_level, diet_type,
            daily_screen_time, exercise_frequency, caffeine_intake,
            reaction_time, memory_test_score
        )
        
        st.subheader("🎯 Your Predicted Score")
        fig, ax = plt.subplots(figsize=(10, 5), subplot_kw={'projection': 'polar'})
        theta = np.linspace(np.pi/2, -np.pi/2, 100)
        cmap = plt.cm.RdYlGn_r
        norm = plt.Normalize(0, 100)
        colors = cmap(norm(np.linspace(0, 100, 100)))
        ax.barh(0, 1, left=theta, height=0.1, color=colors)
        needle_theta = np.pi/2 - prediction/100 * np.pi
        ax.plot([0, needle_theta], [0, 0.8], 'k-', lw=3)
        ax.plot([needle_theta], [0.8], 'ko', ms=10)
        ax.set_ylim(0, 1)
        ax.set_frame_on(False)
        ax.axes.get_yaxis().set_visible(False)
        for score in [0, 25, 50, 75, 100]:
            angle = np.pi/2 - (score/100 * np.pi)
            ax.text(angle, 0.85, f"{score}", ha='center', va='center', fontsize=12, fontweight='bold')
        ax.text(0, -0.2, f"{prediction:.1f}", ha='center', va='center', fontsize=30, fontweight='bold')
        ax.text(0, -0.35, "Cognitive Score", ha='center', va='center', fontsize=14)
        st.pyplot(fig)
        
        # Interpretation
        st.subheader("📌 Interpretation")
        if prediction >= 80:
            st.success(f"Excellent cognitive score of {prediction:.1f}!")
        elif prediction >= 60:
            st.info(f"Good cognitive score of {prediction:.1f}.")
        elif prediction >= 40:
            st.warning(f"Moderate score of {prediction:.1f}.")
        else:
            st.error(f"Low cognitive score of {prediction:.1f}.")

        # Recommendations
        st.subheader("🛠 Recommendations")
        recs = []
        if sleep_duration < 7 or sleep_duration > 9:
            recs.append("Sleep 7–9 hours per night.")
        if stress_level > 6:
            recs.append("Reduce stress with meditation or exercise.")
        if daily_screen_time > 8:
            recs.append("Limit screen time to under 8 hours daily.")
        if exercise_frequency == "Low":
            recs.append("Increase physical activity (e.g., 30 mins/day).")
        if caffeine_intake > 400:
            recs.append("Reduce caffeine below 400 mg/day.")
        if reaction_time > 450:
            recs.append("Play focus and reflex games.")
        if memory_test_score < 60:
            recs.append("Practice memory-enhancing activities.")
        if recs:
            for i, r in enumerate(recs, 1):
                st.markdown(f"{i}. {r}")
        else:
            st.markdown("Your lifestyle appears optimal! 🎉")

with col2:
    st.header("📘 About Cognitive Scores")
    st.markdown("""
    A cognitive score estimates your brain's performance in areas like:
    
    - Memory and recall
    - Focus and attention
    - Processing speed
    - Problem-solving
    
    ### Factors That Influence Scores:
    - **Sleep**: Impacts memory and restoration.
    - **Stress**: Chronic stress reduces focus.
    - **Diet & Caffeine**: Fuels or hinders mental clarity.
    - **Exercise**: Supports brain plasticity.
    - **Screen Time**: Impacts attention and sleep.
    """)

    if has_sample_data and 'Cognitive_Score' in sample_data.columns:
        st.subheader("Sample Distribution")
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.histplot(sample_data['Cognitive_Score'], kde=True, ax=ax)
        ax.set_xlabel('Cognitive Score')
        ax.set_ylabel('Frequency')
        st.pyplot(fig)

# Footer
st.markdown("""
---
#### 📋 Instructions:
1. Fill in your details on the sidebar.
2. Click **Predict Cognitive Score**.
3. View your score, interpretation, and suggestions.

> *Note: This tool is for educational purposes. Please consult a healthcare provider for clinical assessments.*
""")
