import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns

# Set page configuration
st.set_page_config(
    page_title="Cognitive Score Predictor",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define IT-themed color palette
primary_color = "#0078D7"  # Microsoft blue
secondary_color = "#106EBE"  # Darker blue
accent_color = "#2B88D8"  # Light blue
background_color = "#F5F5F5"  # Light gray
text_color = "#333333"  # Dark gray
success_color = "#107C10"  # Green
warning_color = "#D83B01"  # Orange

# Custom CSS for IT theme
st.markdown(f"""
<style>
    .main .block-container {{
        padding-top: 2rem;
        padding-bottom: 2rem;
    }}
    h1, h2, h3, h4, h5, h6 {{
        color: {primary_color};
    }}
    .stButton>button {{
        background-color: {primary_color};
        color: white;
    }}
    .stButton>button:hover {{
        background-color: {secondary_color};
    }}
    .stProgress .st-bo {{
        background-color: {accent_color};
    }}
    .sidebar .sidebar-content {{
        background-color: {background_color};
    }}
    .css-145kmo2 {{
        border: 2px solid {accent_color};
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 1rem;
    }}
</style>
""", unsafe_allow_html=True)

# App title and description
st.title("🧠 Cognitive Score Predictor")
st.markdown("""
This application predicts cognitive performance scores based on various lifestyle and health factors.
Enter your information below to get a prediction of your cognitive score.
""")

# Load a small sample of the dataset for reference
try:
    sample_data = pd.read_csv('/home/ubuntu/cognitive_app/data_subset.csv')
    has_sample_data = True
except:
    # If the file doesn't exist, create a simple reference dataset
    has_sample_data = False
    # Create a simple reference dataset with reasonable ranges
    sample_data = pd.DataFrame({
        'Age': [18, 59],
        'Sleep_Duration': [4.0, 10.0],
        'Stress_Level': [1, 10],
        'Daily_Screen_Time': [1.0, 12.0],
        'Caffeine_Intake': [0, 500],
        'Reaction_Time': [200.0, 600.0],
        'Memory_Test_Score': [40, 100]
    })

# Sidebar for inputs
st.sidebar.header("User Information")

# Create input fields
with st.sidebar:
    # Personal Information
    st.subheader("Personal Information")
    age = st.slider("Age", min_value=18, max_value=59, value=30, 
                   help="Age in years")
    
    gender = st.selectbox("Gender", options=["Male", "Female", "Other"], 
                         help="Gender")
    
    # Lifestyle Factors
    st.subheader("Lifestyle Factors")
    sleep_duration = st.slider("Sleep Duration (hours)", 
                              min_value=4.0, max_value=10.0, value=7.0, step=0.1,
                              help="Average sleep duration in hours per day")
    
    stress_level = st.slider("Stress Level", 
                            min_value=1, max_value=10, value=5,
                            help="Stress level on a scale of 1-10 (1: very low, 10: very high)")
    
    diet_type = st.selectbox("Diet Type", 
                            options=["Non-Vegetarian", "Vegetarian", "Vegan"],
                            help="Primary diet type")
    
    daily_screen_time = st.slider("Daily Screen Time (hours)", 
                                 min_value=1.0, max_value=12.0, value=6.0, step=0.1,
                                 help="Average screen time in hours per day")
    
    exercise_frequency = st.selectbox("Exercise Frequency", 
                                     options=["Low", "Medium", "High"],
                                     help="How often you exercise")
    
    caffeine_intake = st.slider("Caffeine Intake (mg)", 
                               min_value=0, max_value=500, value=150,
                               help="Daily caffeine intake in milligrams")
    
    # Cognitive Metrics
    st.subheader("Cognitive Metrics")
    reaction_time = st.slider("Reaction Time (ms)", 
                             min_value=200.0, max_value=600.0, value=350.0, step=0.1,
                             help="Reaction time in milliseconds (lower is better)")
    
    memory_test_score = st.slider("Memory Test Score", 
                                 min_value=40, max_value=100, value=70,
                                 help="Memory test score out of 100")

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.header("Prediction")
    
    # Create a prediction function (simplified model)
    def predict_cognitive_score(age, gender, sleep_duration, stress_level, diet_type, 
                               daily_screen_time, exercise_frequency, caffeine_intake,
                               reaction_time, memory_test_score):
        """
        A simplified prediction model based on general cognitive science principles.
        This is a placeholder for the actual trained model.
        """
        # Convert categorical variables to numeric
        gender_factor = {'Male': 0, 'Female': 0, 'Other': 0}
        diet_factor = {'Non-Vegetarian': 0, 'Vegetarian': 0.5, 'Vegan': 1}
        exercise_factor = {'Low': 0, 'Medium': 0.5, 'High': 1}
        
        # Normalize inputs (simplified)
        age_norm = 1 - ((age - 18) / (59 - 18))  # Younger is better for cognitive performance
        sleep_quality = 1 - abs(sleep_duration - 8) / 4  # Optimal sleep around 8 hours
        stress_impact = 1 - (stress_level / 10)  # Lower stress is better
        screen_impact = 1 - (daily_screen_time / 12)  # Less screen time is better
        caffeine_impact = 1 - (abs(caffeine_intake - 200) / 300)  # Moderate caffeine is optimal
        reaction_impact = 1 - ((reaction_time - 200) / 400)  # Faster reaction time is better
        memory_impact = memory_test_score / 100  # Higher memory score is better
        
        # Combine factors with weights
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
        
        # Scale to 0-100 range
        return max(0, min(100, score * 100))
    
    if st.button("Predict Cognitive Score", key="predict_button"):
        # Calculate prediction
        prediction = predict_cognitive_score(
            age, gender, sleep_duration, stress_level, diet_type,
            daily_screen_time, exercise_frequency, caffeine_intake,
            reaction_time, memory_test_score
        )
        
        # Display prediction with gauge chart
        st.subheader("Your Predicted Cognitive Score")
        
        # Create a gauge chart
        fig, ax = plt.subplots(figsize=(10, 5), subplot_kw={'projection': 'polar'})
        
        # Gauge settings
        gauge_min, gauge_max = 0, 100
        theta = np.linspace(np.pi/2, -np.pi/2, 100)
        
        # Background colors for gauge (green to red)
        cmap = plt.cm.RdYlGn_r
        norm = plt.Normalize(gauge_min, gauge_max)
        colors = cmap(norm(np.linspace(gauge_min, gauge_max, 100)))
        
        # Draw the gauge background
        ax.barh(0, 1, left=theta, height=0.1, color=colors)
        
        # Calculate the position for the needle
        needle_theta = np.pi/2 - prediction/gauge_max * np.pi
        
        # Draw the needle
        ax.plot([0, needle_theta], [0, 0.8], 'k-', lw=3)
        ax.plot([needle_theta], [0.8], 'ko', ms=10)
        
        # Set the limits and remove unnecessary elements
        ax.set_ylim(0, 1)
        ax.set_frame_on(False)
        ax.axes.get_yaxis().set_visible(False)
        
        # Add labels
        for i, score in enumerate([0, 25, 50, 75, 100]):
            angle = np.pi/2 - (score/gauge_max * np.pi)
            ax.text(angle, 0.85, f"{score}", ha='center', va='center', fontsize=12, fontweight='bold')
        
        # Add the score in the center
        ax.text(0, -0.2, f"{prediction:.1f}", ha='center', va='center', fontsize=30, fontweight='bold')
        ax.text(0, -0.35, "Cognitive Score", ha='center', va='center', fontsize=14)
        
        st.pyplot(fig)
        
        # Interpretation
        st.subheader("Interpretation")
        if prediction >= 80:
            st.success(f"Excellent cognitive performance score of {prediction:.1f}! Your lifestyle factors are supporting optimal brain function.")
        elif prediction >= 60:
            st.info(f"Good cognitive performance score of {prediction:.1f}. There's room for improvement in some lifestyle factors.")
        elif prediction >= 40:
            st.warning(f"Moderate cognitive performance score of {prediction:.1f}. Consider adjusting several lifestyle factors for better cognitive health.")
        else:
            st.error(f"Low cognitive performance score of {prediction:.1f}. Multiple lifestyle factors may be negatively impacting your cognitive function.")
        
        # Recommendations
        st.subheader("Recommendations for Improvement")
        recommendations = []
        
        if sleep_duration < 7 or sleep_duration > 9:
            recommendations.append("Aim for 7-9 hours of quality sleep per night.")
        
        if stress_level > 6:
            recommendations.append("Consider stress reduction techniques like meditation or mindfulness.")
        
        if daily_screen_time > 8:
            recommendations.append("Reduce screen time and take regular breaks from digital devices.")
        
        if exercise_frequency == "Low":
            recommendations.append("Increase physical activity - aim for at least 150 minutes of moderate exercise per week.")
        
        if caffeine_intake > 400:
            recommendations.append("Reduce caffeine intake to below 400mg per day.")
        
        if reaction_time > 450:
            recommendations.append("Practice brain training games to improve reaction time.")
        
        if memory_test_score < 60:
            recommendations.append("Engage in memory exercises and learning new skills to boost memory performance.")
        
        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                st.write(f"{i}. {rec}")
        else:
            st.write("Your current lifestyle is well-balanced for cognitive health. Keep it up!")

with col2:
    st.header("About Cognitive Scores")
    
    st.markdown("""
    ### What is a Cognitive Score?
    
    A cognitive score is a measure of your brain's performance across various domains including:
    
    - Memory and recall
    - Processing speed
    - Attention and focus
    - Problem-solving ability
    - Decision-making capacity
    
    ### Key Factors Affecting Cognitive Performance
    
    **Sleep Quality**: Sleep is essential for memory consolidation and cognitive function.
    
    **Stress Levels**: Chronic stress can impair attention, memory, and decision-making.
    
    **Physical Activity**: Regular exercise improves blood flow to the brain and promotes neuroplasticity.
    
    **Diet**: Nutrition plays a crucial role in brain health and cognitive performance.
    
    **Screen Time**: Excessive screen time may impact attention and sleep quality.
    
    **Caffeine**: Moderate caffeine consumption can enhance alertness, but excessive amounts may increase anxiety.
    """)
    
    # Display a sample distribution if data is available
    if has_sample_data and 'Cognitive_Score' in sample_data.columns:
        st.subheader("Sample Distribution of Cognitive Scores")
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.histplot(sample_data['Cognitive_Score'], kde=True, ax=ax)
        ax.set_xlabel('Cognitive Score')
        ax.set_ylabel('Frequency')
        st.pyplot(fig)

# Footer
st.markdown("""
---
### How to Use This Predictor

1. Enter your personal information and lifestyle factors in the sidebar
2. Click the "Predict Cognitive Score" button
3. Review your predicted score and recommendations
4. Make lifestyle adjustments to improve your cognitive performance

*Note: This is a simplified model for educational purposes. For medical advice, please consult healthcare professionals.*
""")
