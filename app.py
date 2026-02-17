import streamlit as st
import pandas as pd

# ────────────────────────────────────────────────
# FUNCTIONS
# ────────────────────────────────────────────────


def calculate_bmr(weight, height_cm, age, gender):
    if gender == "male":
        return (10 * weight) + (6.25 * height_cm) - (5 * age) + 5
    else:
        return (10 * weight) + (6.25 * height_cm) - (5 * age) - 161


def get_activity_factor(level):
    return {1: 1.2, 2: 1.375, 3: 1.55, 4: 1.725, 5: 1.9}.get(level, 1.2)


def get_goal_settings(goal, intensity, weight, tdee, gender):
    protein_base = weight * (2.2 if gender == "male" else 2.0)

    if goal == "Fat Loss":
        deficits = {1: 0.15, 2: 0.22, 3: 0.28}
        fat_pct = {1: 25, 2: 22, 3: 20}
        return -tdee * deficits[intensity], protein_base + (
            intensity - 1) * 10, fat_pct[intensity]

    if goal == "Bulk":
        return tdee * 0.15, protein_base, 27

    if goal == "Maintenance":
        return 0, protein_base, 25

    if goal == "Recomp":
        return 0, protein_base + 15, 25

    return 0, protein_base, 25


def calculate_macros(calories, protein_g, fat_pct):
    protein_cal = protein_g * 4
    fat_cal = calories * (fat_pct / 100)
    fat_g = fat_cal / 9
    carbs_cal = calories - (protein_cal + fat_cal)
    carbs_g = carbs_cal / 4
    return round(protein_g), round(fat_g), round(carbs_g)


# ────────────────────────────────────────────────
# STREAMLIT APP
# ────────────────────────────────────────────────

st.set_page_config(page_title="Advanced Diet & Macro Planner", layout="wide")

st.title("Advanced Diet & Macro Planner")
st.caption("BMR • TDEE • Goal-Based Macros")

with st.form("diet_form"):

    st.subheader("Body Information")
    st.divider()

    col1, col2 = st.columns(2)

with st.form("diet_form"):
    col1, col2 = st.columns(2)

    with col1:
        weight = st.number_input("Weight (kg)", 30.0, 200.0, 70.0)
        height_ft = st.number_input("Height (feet)", 4, 7, 5)
        height_in = st.number_input("Height (inches)", 0, 11, 10)
        age = st.number_input("Age", 15, 80, 30)

with col2:
    st.markdown("### Lifestyle & Goal")

    gender = st.selectbox("Gender", ["male", "female"])

    with col2:
        gender = st.selectbox("Gender", ["male", "female"])

        activity = st.selectbox(
            "Activity Level", [1, 2, 3, 4, 5],
            format_func=lambda x: [
                "Sedentary", "Lightly Active", "Moderately Active",
                "Very Active", "Extra Active"
            ][x - 1])
        goal = st.selectbox("Goal",
                            ["Fat Loss", "Bulk", "Maintenance", "Recomp"])


st.divider()
st.subheader("Goal Intensity")

    intensity = 1
    if goal == "Fat Loss":
        intensity = st.selectbox(
            "Fat Loss Intensity", [1, 2, 3],
            format_func=lambda x: ["Mild", "Moderate", "Aggressive"][x - 1])

    submit = st.form_submit_button("Generate Plan", use_container_width=True)

if submit:
    if submit:

    st.divider()
    st.header("Your Personalized Plan")
    
    height_cm = height_ft * 30.48 + height_in * 2.54
    bmr = calculate_bmr(weight, height_cm, age, gender)
    tdee = bmr * get_activity_factor(activity)

    cal_adj, protein, fat_pct = get_goal_settings(goal, intensity, weight,
                                                  tdee, gender)
    final_cal = tdee + cal_adj
    protein_g, fat_g, carbs_g = calculate_macros(final_cal, protein, fat_pct)

    st.subheader("Results")
    st.write(f"**BMR:** {round(bmr)} kcal")
    st.write(f"**TDEE:** {round(tdee)} kcal")
    st.write(f"**Target Calories:** {round(final_cal)} kcal")

    st.subheader("Daily Macros")
    st.write(f"Protein: {protein_g} g")
    st.write(f"Fats: {fat_g} g")
    st.write(f"Carbs: {carbs_g} g")

    st.success("Plan generated successfully")

