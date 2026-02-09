import streamlit as st
import numpy as np
from scipy.optimize import fsolve

st.set_page_config(page_title="AASHTO 1993 Flexible Pavement", layout="centered")

st.title("AASHTO 1993 Flexible Pavement Design")
st.write("คำนวณความหนาผิวทางลาดยางตามมาตรฐาน AASHTO 1993")

# -------------------------
# INPUT SECTION
# -------------------------
st.header("1. Input Design Parameters")

W18 = st.number_input("Design ESALs (W18)", value=1_000_000.0)
ZR = st.number_input("Reliability (ZR)", value=-1.645)
So = st.number_input("Overall Standard Deviation (So)", value=0.45)
delta_PSI = st.number_input("ΔPSI", value=1.7)
Mr = st.number_input("Subgrade Resilient Modulus Mr (psi)", value=8000.0)

st.header("2. Layer Coefficients")

a1 = st.number_input("a1 (Asphalt Concrete)", value=0.44)
a2 = st.number_input("a2 (Base Course)", value=0.14)
a3 = st.number_input("a3 (Subbase)", value=0.11)

m2 = st.number_input("m2 (Drainage coefficient Base)", value=1.0)
m3 = st.number_input("m3 (Drainage coefficient Subbase)", value=1.0)

# -------------------------
# AASHTO EQUATION
# -------------------------
def aashto_equation(SN):
    term1 = ZR * So
    term2 = 9.36 * np.log10(SN + 1) - 0.20
    term3 = np.log10(delta_PSI / (4.2 - 1.5)) / (
        0.40 + (1094 / ((SN + 1) ** 5.19))
    )
    term4 = 2.32 * np.log10(Mr) - 8.07
    return term1 + term2 + term3 + term4 - np.log10(W18)

# -------------------------
# CALCULATION
# -------------------------
if st.button("Calculate Pavement Design"):

    SN_initial_guess = 3.0
    SN_solution = fsolve(aashto_equation, SN_initial_guess)
    SN = SN_solution[0]

    st.success(f"Required Structural Number (SN) = {SN:.3f}")

    # สมมุติแบ่งชั้นตัวอย่าง (สามารถปรับ logic ได้)
    D1 = 4  # inch (กำหนดขั้นต่ำ)
    SN_remaining = SN - (a1 * D1)

    if SN_remaining > 0:
        D2 = SN_remaining / (a2 * m2)
        D3 = 0
    else:
        D2 = 0
        D3 = 0

    st.subheader("Layer Thickness (inches)")
    st.write(f"Asphalt Concrete (D1) = {D1:.2f} in")
    st.write(f"Base Course (D2) = {D2:.2f} in")
    st.write(f"Subbase (D3) = {D3:.2f} in")

    st.subheader("Layer Thickness (cm)")
    st.write(f"Asphalt Concrete (D1) = {D1*2.54:.2f} cm")
    st.write(f"Base Course (D2) = {D2*2.54:.2f} cm")
    st.write(f"Subbase (D3) = {D3*2.54:.2f} cm")
