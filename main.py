import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

np.random.seed(42)
years = np.arange(2000, 2025)
temp_changes = np.random.uniform(0.5, 1.5, len(years))
gmsl_changes = temp_changes * 3 + np.random.normal(0, 0.2, len(years))
antectica_loss = temp_changes * -2.5 + np.random.normal(0, 0.2, len(years))
groenlanda_loss = temp_changes * -3.2 + np.random.normal(0, 0.2, len(years))

df = pd.DataFrame({
    'Year': years,
    'Temperature Change (C)': temp_changes,
    'GMSL Change (mm)': gmsl_changes,
    'Antarctica Mass Loss (Gt)': antectica_loss,
    'Greenland Mass Loss (Gt)': groenlanda_loss
})

st.sidebar.title("Navigatie")
page = st.sidebar.radio("Alege pagina:", ("Home", "Vizualizare Grafice", "Simulare Predicție"))

if page == "Home":
    st.title("Topirea Ghetarilor in functie de schimbarea de temperatura la nivel global")
    st.write("""
        Aceasta mini-aplicatie permite:
        - Vizualizarea corelatiilor intre temperatura si topirea ghetarilor.
        - Simularea impactului unei cresteri de temperatura asupra nivelului marilor si masei de gheata.
    """)

elif page == "Vizualizare Grafice":
    st.title("Vizualizare Grafice")

    st.subheader("Matricea Corelațiilor")
    corr = df.drop('Year', axis=1).corr()
    fig, ax = plt.subplots(figsize=(8,6))
    sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig)

    st.subheader("Temperature vs GMSL")
    fig2, ax2 = plt.subplots()
    sns.scatterplot(x='Temperature Change (C)', y='GMSL Change (mm)', data=df, ax=ax2)
    st.pyplot(fig2)

    st.subheader("Temperature vs Antarctica Mass Loss")
    fig3, ax3 = plt.subplots()
    sns.scatterplot(x='Temperature Change (C)', y='Antarctica Mass Loss (Gt)', data=df, ax=ax3)
    st.pyplot(fig3)

    st.subheader("Temperature vs Greenland Mass Loss")
    fig4, ax4 = plt.subplots()
    sns.scatterplot(x='Temperature Change (C)', y='Greenland Mass Loss (Gt)', data=df, ax=ax4)
    st.pyplot(fig4)


elif page == "Simulare Predicție":
    st.title("Simulare Impact Creștere Temperatură")

    st.subheader("Setează parametrii pentru simulare:")

    year_input = st.number_input(
        "Alege anul pentru care vrei simularea:",
        min_value=2025,
        max_value=2100,
        value=2050,
        step=1
    )

    current_gmsl = st.number_input(
        "Nivelul actual al mării (mm):",
        min_value=0.0,
        max_value=5000.0,
        value=0.0,
        step=1.0
    )

    temp_input = st.slider(
        "Selectează creșterea temperaturii globale (°C):",
        min_value=0.0,
        max_value=5.0,
        value=1.0,
        step=0.1
    )

    df = pd.read_csv('C:\\Users\\Daria\\Desktop\\mini_app\\metrics_results.csv')

    slope_gmsl = df[df['Variable'] == 'GMSL_mm']['Slope'].values[0]
    slope_antarctica = df[df['Variable'] == 'AntarcticaMass_Gt']['Slope'].values[0]
    slope_greenland = df[df['Variable'] == 'GreenlandMass_Gt']['Slope'].values[0]
    intercept_gmsl = 0
    intercept_antarctica = 0
    intercept_greenland = 0

    if st.button("Prezice Impactul"):
        predicted_gmsl = current_gmsl + slope_gmsl * temp_input
        predicted_antarctica = slope_antarctica * temp_input
        predicted_greenland = slope_greenland * temp_input

        st.success(f"\U0001F4C5 În anul {year_input}, nivelul mării ar putea ajunge la {predicted_gmsl:.2f} mm")
        st.error(f"\U0001F30A Pierdere masa gheata Antarctica: {predicted_antarctica:.2f} Gt")
        st.error(f"\U0001F30A Pierdere masa gheata Groenlanda: {predicted_greenland:.2f} Gt")