# streamlit_app.py
import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path

# ===== Page Config =====
st.set_page_config(page_title="תמחור עובד", page_icon="💼")

# ===== Force RTL Styling =====
st.markdown("""
    <style>
    body, .stApp {
        direction: rtl;
        text-align: right;
        font-family: "Alef", sans-serif;
    }
    table {
        direction: rtl;
    }
    .css-1v3fvcr { direction: rtl; }
    </style>
""", unsafe_allow_html=True)

# ===== Title =====
st.title("💼 מחשבון תמחור עובד - נבנה על ידי עמית שטיין")

# ===== Reset History Button =====
path = Path("pricing_history.csv")
st.markdown("### ⚙️ ניהול נתונים")
if path.exists():
    if st.button("🗑️ אפס היסטוריה"):
        path.unlink()
        st.success("✅ ההיסטוריה אופסה בהצלחה!")

# ===== Inputs =====
with st.form("pricing_form"):
    col1, col2 = st.columns(2)
    with col1:
        employee_name = st.text_input("שם עובד/ת", "")
        role = st.text_input("תפקיד", "")
        currency = st.selectbox("מטבע", ["₪", "$", "€"], index=0)
        base_salary = st.number_input("שכר בסיס חודשי ברוטו", min_value=0.0, step=100.0, value=12000.0)
        bonus_monthly = st.number_input("בונוס חודשי ממוצע (אם יש)", min_value=0.0, step=100.0, value=0.0)
        travel = st.number_input("נסיעות/החזרי הוצאות", min_value=0.0, step=10.0, value=0.0)
    with col2:
        pension_pct = st.number_input("פנסיה + פיצויים (% מהשכר)", min_value=0.0, max_value=100.0, step=0.5, value=18.33)
        ni_pct = st.number_input("ביטוח לאומי/בריאות מעסיק (% מהשכר)", min_value=0.0, max_value=100.0, step=0.5, value=7.0)
        other_benefits = st.number_input("הטבות נוספות קבועות", min_value=0.0, step=50.0, value=0.0)
        overhead_pct = st.number_input("תקורה/הנהלה וכלליות (% עלות)", min_value=0.0, max_value=100.0, step=0.5, value=10.0)
        margin_pct = st.number_input("עמלת רווח (% עלות לאחר תקורה)", min_value=0.0, max_value=100.0, step=0.5, value=20.0)

    submitted = st.form_submit_button("חשב")

def pct(x): return x / 100.0

if submitted:
    # ===== Calculations =====
    salary_base_total = base_salary + bonus_monthly
    pension = salary_base_total * pct(pension_pct)
    ni = salary_base_total * pct(ni_pct)

    direct_cost = salary_base_total + pension + ni + travel + other_benefits
    overhead = direct_cost * pct(overhead_pct)
    cost_after_overhead = direct_cost + overhead
    profit = cost_after_overhead * pct(margin_pct)
    client_price = cost_after_overhead + profit

    # ===== Breakdown table =====
    rows = [
        ("שכר בסיס + בונוס", salary_base_total),
        (f"פנסיה+פיצויים ({pension_pct}%)", pension),
        (f"ביטוח לאומי/בריאות מעסיק ({ni_pct}%)", ni),
        ("נסיעות/החזרי הוצאות", travel),
        ("הטבות נוספות", other_benefits),
        ("סך עלות ישירה", direct_cost),
        (f"תקורה ({overhead_pct}%)", overhead),
        ("עלות לאחר תקורה", cost_after_overhead),
        (f"רווח ({margin_pct}%)", profit),
    ]
    df = pd.DataFrame(rows, columns=["רכיב", f"סכום ({currency})"])

    st.subheader("📊 פירוט לוגיקה")
    st.dataframe(df, use_container_width=True)

    st.subheader("💰 מחיר סופי ללקוח")
    st.metric(label=f"מחיר חודשי ({currency})", value=f"{client_price:,.0f}")

    # ===== Save history =====
    rec = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "employee_name": employee_name,
        "role": role,
        "currency": currency,
        "base_salary": base_salary,
        "bonus_monthly": bonus_monthly,
        "travel": travel,
        "pension_pct": pension_pct,
        "ni_pct": ni_pct,
        "other_benefits": other_benefits,
        "overhead_pct": overhead_pct,
        "margin_pct": margin_pct,
        "direct_cost": round(direct_cost, 2),
        "cost_after_overhead": round(cost_after_overhead, 2),
        "client_price": round(client_price, 2),
    }
    if path.exists():
        hist = pd.read_csv(path)
        hist = pd.concat([hist, pd.DataFrame([rec])], ignore_index=True)
    else:
        hist = pd.DataFrame([rec])
    hist.to_csv(path, index=False)
    st.success("✅ נשמר לקובץ pricing_history.csv")

    with st.expander("🕓 צפייה בהיסטוריית תמחורים"):
        st.dataframe(hist.tail(50), use_container_width=True)


