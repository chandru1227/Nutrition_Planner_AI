import streamlit as st
import pandas as pd
import joblib

# Load models
breakfast_model = joblib.load("diet_breakfast_model (2).joblib")
lunch_model = joblib.load("diet_lunch_model (1).joblib")
dinner_model = joblib.load("diet_dinner_model (1).joblib")

st.title("🍽️ AI Nutrition Planner")
st.markdown("Input your personal details and get meal recommendations tailored to your weight goal.")

# --- User Inputs ---
age = st.number_input("Age", min_value=10, max_value=100, value=25)
weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, value=70.0)
height = st.number_input("Height (cm)", min_value=100.0, max_value=250.0, value=170.0)
gender = st.selectbox("Gender", ["Male", "Female"])
activity = st.selectbox("Activity Level", ["Low", "Moderate", "High"])
diet_goal = st.selectbox("Diet Goal", ["Weight Loss", "Weight Gain"])

# --- Derived Features ---
bmi = weight / ((height / 100) ** 2)
weight_height_ratio = weight / height
bmr = 10 * weight + 6.25 * height - 5 * age + (5 if gender == "Male" else -161)

# --- DataFrame for Prediction ---
input_data = pd.DataFrame([{
    'Age': age,
    'Weight': weight,
    'Height': height,
    'Activity Level': activity,
    'Gender': gender,
    'Basic Metabolic Rate': bmr,
    'BMI': bmi,
    'WeightHeightRatio': weight_height_ratio,
    'Diet Goal': diet_goal
}])

# --- Predict Meals ---
if st.button("🔍 Recommend My Meals"):
    breakfast = breakfast_model.predict(input_data)[0]
    lunch = lunch_model.predict(input_data)[0]
    dinner = dinner_model.predict(input_data)[0]

    st.subheader("🍴 Predicted Meal Plan")
    st.success(f"🥣 **Breakfast**: {breakfast}")
    st.success(f"🍛 **Lunch**: {lunch}")
    st.success(f"🍽️ **Dinner**: {dinner}")
