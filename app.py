
import streamlit as st
import pandas as pd
import numpy as np
import random
import plotly.express as px
from datetime import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="TOPSIS Dashboard", page_icon="✈️", layout="wide")

st.title("Multi-Criteria Decision Making Tool")
st.write("Interactive multi-criteria analysis using the TOPSIS method to rank simulated aircraft performance.")
st.markdown("---")

# --- FIX Pandas Styler rendering limit for large DataFrames ---
pd.set_option("styler.render.max_elements", 5_000_000)

# --- GENERAL INPUTS ---
st.header("Simulation Parameters")

col1, col2, col3, col4 = st.columns(4)
with col1:
    n_alternatives = st.number_input("Number of aircraft cases", min_value=2, max_value=1000000, value=50)
with col2:
    top_n = st.number_input("Top alternatives to display", min_value=1, max_value=n_alternatives, value=10)
with col3:
    electrif = st.selectbox("Electrification - Unfunctionnal ", ["None", "Hybrid", "Full Electric"])
with col4:
    tech_orient = st.radio("Technical orientation - Unfunctional", ["Conservative", "Aggressive", "Innovative"])

st.markdown("---")

# --- CRITERIA ---
inputs = [
    "Aircraft Cruise Speed (knots)",
    "Total Energy Required (MJ)",
    "Direct operating cost plus interest ($/mile)",
    "Required yield per revenue passenger mile ($/mile)",
    "Acquisition price with spares ($M)",
    "Trip Fuel (kg)"
]

st.header("Criteria Weights")

# --- TWO COLUMNS: input weights + pie chart ---
col_inputs, col_chart = st.columns([3, 2])

with col_inputs:
    weights = {}
    for inp in inputs:
        weights[inp] = st.number_input(
            f"Weight: {inp}",
            min_value=0.0,
            max_value=1.0,
            value= 1/len(inputs),
            key=f"weight_{inp}"
        )

    total_weight = sum(weights.values())

    if total_weight < 0.999:
        st.error(f"⚠️ The total of all weights is inferior to 1 , whereas it should be equal to 1. Current total = {total_weight:.2f}")
    elif total_weight > 1.001:
        st.error(f"⚠️ The sum of all weights is greater than 1, whereas it should be equal to 1[]. Current total = {total_weight:.2f}")
    else:
        st.success("✅ The sum of weights equals 1.")

with col_chart:
    if 0.999 <= total_weight <= 1.001:
        st.markdown("<h3 style='text-align: center;'>Weight Distribution</h3>", unsafe_allow_html=True)

        weights_df = pd.DataFrame({
            "Criteria": list(weights.keys()),
            "Weight": list(weights.values())
        }).sort_values(by="Weight", ascending=False)

        fig = px.pie(
            weights_df,
            names="Criteria",
            values="Weight",
            hole=0.55,
            color_discrete_sequence=px.colors.sequential.Tealgrn_r
        )

        fig.update_traces(
            textinfo="percent",
            textposition="inside",
            insidetextfont=dict(size=15, color="white"),
            hovertemplate="<b>%{label}</b><br>Weight: %{value:.2f} (%{percent})<extra></extra>",
            pull=[0.05 if w == weights_df["Weight"].max() else 0 for w in weights_df["Weight"]],
        )

        fig.update_layout(
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.25,
                xanchor="center",
                x=0.5,
                font=dict(size=13, color="white"),
                bgcolor="rgba(0,0,0,0)"
            ),
            margin=dict(t=20, b=50, l=0, r=0),
            height=400,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Adjust the weights to make the total equal to 1 before displaying the chart.")

# --- DEFINE OPTIMIZATION TYPE (MAX/MIN) ---
optimization = {
    "Aircraft Cruise Speed (knots)": "max",
    "Total Energy Required (MJ)": "min",
    "Direct operating cost plus interest ($/mile)": "min",
    "Required yield per revenue passenger mile ($/mile)": "min",
    "Acquisition price with spares ($M)": "min",
    "Trip Fuel (kg)": "min"
}

st.markdown("---")

# --- RUN TOPSIS ANALYSIS ---
if st.button("🚀 Run TOPSIS Analysis"):
    # --- SIMULATED DATA ---
    data = {
        "Case": [f"Aircraft {i+1}" for i in range(n_alternatives)],
        "Aircraft Cruise Speed (knots)": [random.randint(210, 250) for _ in range(n_alternatives)],
        "Total Energy Required (MJ)": [round(random.uniform(3, 7), 3) for _ in range(n_alternatives)],
        "Direct operating cost plus interest ($/mile)": [round(random.uniform(6.4, 8.7), 3) for _ in range(n_alternatives)],
        "Required yield per revenue passenger mile ($/mile)": [round(random.uniform(1.35, 1.5), 3) for _ in range(n_alternatives)],
        "Acquisition price with spares ($M)": [round(random.uniform(220, 270), 3) for _ in range(n_alternatives)],
        "Trip Fuel (kg)": [random.randint(27032, 31032) for _ in range(n_alternatives)],
    }

    df = pd.DataFrame(data)

    st.subheader(f"Simulated Aircraft Data ({n_alternatives} alternatives)")
    st.dataframe(df, use_container_width=True, hide_index=True)

    # --- NORMALIZATION ---
    df_norm = df.copy()
    for inp in inputs:
        norm = np.linalg.norm(df[inp])
        df_norm[inp] = df[inp] / norm if norm != 0 else df[inp]

    # --- APPLY WEIGHTS ---
    df_weighted = df_norm.copy()
    for inp in inputs:
        df_weighted[inp] *= weights[inp]

    # --- IDEAL / ANTI-IDEAL SOLUTIONS ---
    ideal = {inp: df_weighted[inp].max() if optimization[inp] == "max" else df_weighted[inp].min() for inp in inputs}
    anti_ideal = {inp: df_weighted[inp].min() if optimization[inp] == "max" else df_weighted[inp].max() for inp in inputs}

    # --- DISTANCES & TOPSIS SCORES ---
    D_plus, D_minus = [], []
    for i in range(n_alternatives):
        d_plus = np.sqrt(sum((df_weighted.loc[i, inp] - ideal[inp]) ** 2 for inp in inputs))
        d_minus = np.sqrt(sum((df_weighted.loc[i, inp] - anti_ideal[inp]) ** 2 for inp in inputs))
        D_plus.append(d_plus)
        D_minus.append(d_minus)

    df["TOPSIS Score"] = [d_minus / (d_plus + d_minus) for d_plus, d_minus in zip(D_plus, D_minus)]

    df_sorted = df.sort_values(by="TOPSIS Score", ascending=False).reset_index(drop=True)
    topN = df_sorted.head(int(top_n))

    # --- HIGHLIGHT BEST ---
    def highlight_best_row(row):
        color = "background-color: #3CB371; color: white" if row.name == 0 else ""
        return [color] * len(row)

    st.markdown("---")
    st.subheader(f"TOPSIS Ranking (Top {int(top_n)} Aircraft)")
    st.dataframe(topN.style.apply(highlight_best_row, axis=1), use_container_width=True)

    # --- VISUALIZATION (ORDERED LEFT → RIGHT) ---
    st.markdown(f"### Top {int(top_n)} Aircraft - TOPSIS Scores")

    fig = px.bar(
        topN.sort_values(by="TOPSIS Score", ascending=False),
        x="Case",
        y="TOPSIS Score",
        text="TOPSIS Score",
        color="TOPSIS Score",
        color_continuous_scale=px.colors.sequential.Tealgrn,
    )

    fig.update_traces(
        texttemplate="%{text:.3f}",
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>TOPSIS Score: %{y:.4f}<extra></extra>"
    )

    fig.update_layout(
        xaxis=dict(categoryorder="array", categoryarray=topN["Case"]),
        yaxis_title="Score",
        xaxis_title="Aircraft Case",
        height=450,
        coloraxis_showscale=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white", size=13),
    )

    st.plotly_chart(fig, use_container_width=True)

    # --- BEST ALTERNATIVE ---
    best_alt = topN.iloc[0]["Case"]
    best_score = topN.iloc[0]["TOPSIS Score"]
    st.success(f"✅ **Best aircraft configuration:** {best_alt} — TOPSIS Score: {best_score:.4f}")

else:
    st.info("Click **🚀 Run TOPSIS Analysis** to generate simulated aircraft data and compute the ranking.")

st.markdown("---")
st.caption(f"Streamlit Prototype - last update {datetime.now().strftime('%d %B %Y - %H:%M')}")
