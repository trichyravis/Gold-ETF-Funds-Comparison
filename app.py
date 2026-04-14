"""
Gold Fund Comparison Dashboard
The Mountain Path Academy
Prof. V. Ravichandran
═══════════════════════════════════════
Interactive comparison of 7 Indian Gold Funds/ETFs
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

st.set_page_config(page_title="Gold Fund Dashboard — The Mountain Path Academy", page_icon="⛰", layout="wide", initial_sidebar_state="collapsed")

# Mountain Path Palette
GOLD = "#FFD700"; BLUE = "#003366"; MID_BLUE = "#004d80"; CARD_BG = "#112240"
TEXT = "#e6f1ff"; MUTED = "#8892b0"; GREEN = "#28a745"; RED = "#dc3545"
LIGHT_BLUE = "#ADD8E6"; BG_DARK = "#1a2332"; HULL_AMBER = "#f0c040"; PLOT_BG = "#0a1628"

st.html(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Source+Sans+Pro:wght@300;400;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    .stApp {{ background: linear-gradient(135deg, {BG_DARK}, #243447, #2a3f5f); }}
    #MainMenu, header, footer {{visibility: hidden;}}
    .block-container {{ padding-top: 1.5rem; max-width: 1200px; }}
    [data-testid="stMetricValue"] {{ color: {GOLD} !important; -webkit-text-fill-color: {GOLD} !important; font-family: 'Playfair Display', serif !important; }}
    [data-testid="stMetricLabel"] {{ color: {LIGHT_BLUE} !important; -webkit-text-fill-color: {LIGHT_BLUE} !important; font-size: 0.78rem !important; }}
    [data-testid="stMetricDelta"] {{ font-family: 'JetBrains Mono', monospace !important; }}
    div[data-testid="stDataFrame"] {{ border: 1px solid rgba(255,215,0,0.12); border-radius: 10px; }}
</style>
""")

# ── Header ──
st.html(f"""
<div style="background:rgba(0,51,102,0.92); border-bottom:3px solid {GOLD}; border-radius:12px 12px 0 0; padding:18px 28px; margin-bottom:8px; user-select:none;">
    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
        <div>
            <span style="font-family:'Playfair Display',serif; color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-size:1.4rem; font-weight:700;">⛰ Indian Gold Fund Comparison Dashboard</span><br>
            <span style="font-family:'Source Sans Pro',sans-serif; color:{LIGHT_BLUE}; -webkit-text-fill-color:{LIGHT_BLUE}; font-size:0.84rem;">
                7 Funds · NAV · Returns · Expense Ratios · AUM · Risk Metrics · Sortable Filters
            </span>
        </div>
        <div style="text-align:right;">
            <span style="font-family:'Source Sans Pro',sans-serif; color:{MUTED}; -webkit-text-fill-color:{MUTED}; font-size:0.7rem;">Prof. V. Ravichandran · NMIMS · BITS Pilani · RV University · GIM</span>
        </div>
    </div>
</div>
""")

# ══════════════════════════════════════════════════════════
#  FUND DATA (Direct Growth Plans — sourced Apr 2026)
# ══════════════════════════════════════════════════════════
funds = pd.DataFrame({
    "Fund Name": [
        "ICICI Prudential Gold ETF FoF",
        "ICICI Prudential Gold ETF",
        "HDFC Gold Fund (FoF)",
        "SBI Gold Fund",
        "Nippon India Gold Savings Fund",
        "Invesco India Gold ETF FoF",
        "Aditya Birla SL Gold Fund",
    ],
    "Type": ["FoF", "ETF", "FoF", "FoF", "FoF", "FoF", "FoF"],
    "AMC": ["ICICI Prudential", "ICICI Prudential", "HDFC", "SBI", "Nippon India", "Invesco", "Aditya Birla SL"],
    "NAV (Rs.)": [48.14, 126.67, 45.52, 24.85, 56.66, 23.45, 22.98],
    "AUM (Rs. Cr)": [6535, 25942, 11766, 14998, 7223, 1420, 1782],
    "Expense Ratio (%)": [0.10, 0.50, 0.20, 0.25, 0.13, 0.10, 0.20],
    "1Y Return (%)": [69.9, 63.3, 68.9, 69.1, 58.6, 67.1, 69.5],
    "3Y CAGR (%)": [34.0, 33.6, 33.7, 34.0, 32.1, 33.3, 34.0],
    "5Y CAGR (%)": [25.3, 24.9, 25.2, 25.1, 24.3, 24.7, 25.5],
    "Std Dev (%)": [14.8, 14.5, 14.9, 14.7, 15.1, 14.6, 14.8],
    "Sharpe Ratio": [2.98, 2.85, 3.01, 2.95, 2.78, 2.92, 3.02],
    "Exit Load": [
        "1% if < 15 days",
        "Nil (exchange traded)",
        "1% if < 15 days",
        "1% if < 15 days",
        "1% if < 15 days",
        "1% if < 15 days",
        "1% if < 15 days",
    ],
    "Min SIP (Rs.)": ["100", "N/A (Demat)", "100", "500", "100", "100", "100"],
    "Min Lumpsum (Rs.)": ["100", "N/A (Demat)", "100", "5,000", "100", "1,000", "100"],
    "Launch Date": ["Jan 2013", "Aug 2010", "Nov 2011", "Sep 2011", "Mar 2011", "Mar 2012", "Mar 2012"],
    "Benchmark": ["Domestic Gold Price"] * 7,
})

# ── Plotly layout ──
def base_layout(title="", xaxis_title="", yaxis_title="", height=420):
    return go.Layout(
        title=dict(text=title, font=dict(family="Playfair Display, serif", size=17, color=GOLD), x=0.01, y=0.97),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor=PLOT_BG,
        font=dict(family="Source Sans Pro, sans-serif", color=TEXT), height=height,
        margin=dict(l=55, r=25, t=50, b=55),
        xaxis=dict(title=dict(text=xaxis_title, font=dict(color=LIGHT_BLUE, size=13)), gridcolor="rgba(255,255,255,0.05)", tickfont=dict(color=MUTED, size=11)),
        yaxis=dict(title=dict(text=yaxis_title, font=dict(color=LIGHT_BLUE, size=13)), gridcolor="rgba(255,255,255,0.05)", tickfont=dict(color=MUTED, size=11)),
        hoverlabel=dict(bgcolor=CARD_BG, font_size=12, font_family="JetBrains Mono", bordercolor=GOLD),
        legend=dict(bgcolor="rgba(17,34,64,0.85)", bordercolor="rgba(255,215,0,0.2)", borderwidth=1, font=dict(size=10, color=TEXT)),
    )

# ══════════════════════════════════════════════════════════
#  TOP METRICS
# ══════════════════════════════════════════════════════════
best_1y = funds.loc[funds["1Y Return (%)"].idxmax()]
best_sharpe = funds.loc[funds["Sharpe Ratio"].idxmax()]
lowest_er = funds.loc[funds["Expense Ratio (%)"].idxmin()]
largest_aum = funds.loc[funds["AUM (Rs. Cr)"].idxmax()]

m1, m2, m3, m4 = st.columns(4)
m1.metric("Best 1Y Return", f"{best_1y['1Y Return (%)']}%", best_1y['Fund Name'][:22])
m2.metric("Best Sharpe Ratio", f"{best_sharpe['Sharpe Ratio']}", best_sharpe['Fund Name'][:22])
m3.metric("Lowest Expense Ratio", f"{lowest_er['Expense Ratio (%)']}%", lowest_er['Fund Name'][:22])
m4.metric("Largest AUM", f"Rs. {largest_aum['AUM (Rs. Cr)']:,} Cr", largest_aum['Fund Name'][:22])

# ══════════════════════════════════════════════════════════
#  FILTERS
# ══════════════════════════════════════════════════════════
st.html(f"""<div style="font-family:'Playfair Display',serif; color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-size:1.1rem; margin:16px 0 6px; user-select:none;">🔍 Filter & Sort</div>""")

fc1, fc2, fc3 = st.columns(3)
with fc1:
    sort_by = st.selectbox("Sort by", ["1Y Return (%)", "3Y CAGR (%)", "5Y CAGR (%)", "Sharpe Ratio", "Expense Ratio (%)", "AUM (Rs. Cr)", "Std Dev (%)"])
with fc2:
    sort_order = st.radio("Order", ["Descending", "Ascending"], horizontal=True)
with fc3:
    fund_filter = st.multiselect("Select Funds", funds["Fund Name"].tolist(), default=funds["Fund Name"].tolist())

ascending = sort_order == "Ascending"
filtered = funds[funds["Fund Name"].isin(fund_filter)].sort_values(sort_by, ascending=ascending).reset_index(drop=True)

# ══════════════════════════════════════════════════════════
#  MAIN TABLE
# ══════════════════════════════════════════════════════════
st.html(f"""<div style="font-family:'Playfair Display',serif; color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-size:1.1rem; margin:18px 0 6px; user-select:none;">📊 Fund Comparison Table</div>""")

display_cols = ["Fund Name", "Type", "NAV (Rs.)", "AUM (Rs. Cr)", "Expense Ratio (%)",
                "1Y Return (%)", "3Y CAGR (%)", "5Y CAGR (%)", "Std Dev (%)", "Sharpe Ratio",
                "Exit Load", "Min SIP (Rs.)", "Min Lumpsum (Rs.)"]
st.dataframe(filtered[display_cols], use_container_width=True, hide_index=True, height=320)

# ══════════════════════════════════════════════════════════
#  CHARTS
# ══════════════════════════════════════════════════════════
st.html(f"""<div style="font-family:'Playfair Display',serif; color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-size:1.1rem; margin:18px 0 6px; user-select:none;">📈 Visual Comparisons</div>""")

ch1, ch2 = st.columns(2)

# Chart 1: Returns comparison
with ch1:
    fig1 = go.Figure(layout=base_layout("Returns: 1Y vs 3Y vs 5Y CAGR", "", "Return (%)", height=420))
    for col, color, name in [("1Y Return (%)", GOLD, "1-Year"), ("3Y CAGR (%)", LIGHT_BLUE, "3-Year CAGR"), ("5Y CAGR (%)", GREEN, "5-Year CAGR")]:
        fig1.add_trace(go.Bar(
            y=filtered["Fund Name"].str[:20], x=filtered[col], orientation='h',
            name=name, marker_color=color, opacity=0.85,
            text=filtered[col].apply(lambda v: f"{v}%"), textposition="outside",
            textfont=dict(color=TEXT, size=10),
        ))
    fig1.update_layout(barmode='group', yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig1, use_container_width=True)

# Chart 2: Risk-Return scatter
with ch2:
    fig2 = go.Figure(layout=base_layout("Risk-Return Profile (3Y CAGR vs Std Dev)", "Standard Deviation (%)", "3Y CAGR (%)", height=420))
    fig2.add_trace(go.Scatter(
        x=filtered["Std Dev (%)"], y=filtered["3Y CAGR (%)"],
        mode="markers+text", text=filtered["Fund Name"].str[:15],
        textposition="top center", textfont=dict(color=TEXT, size=10),
        marker=dict(size=filtered["AUM (Rs. Cr)"].apply(lambda v: max(12, min(40, v/500))),
                    color=filtered["Sharpe Ratio"], colorscale=[[0, RED], [0.5, HULL_AMBER], [1, GREEN]],
                    showscale=True, colorbar=dict(title="Sharpe", tickfont=dict(color=MUTED)),
                    line=dict(color=GOLD, width=1.5)),
        hovertemplate="<b>%{text}</b><br>Std Dev: %{x:.1f}%<br>3Y CAGR: %{y:.1f}%<br>Sharpe: %{marker.color:.2f}<extra></extra>",
    ))
    st.plotly_chart(fig2, use_container_width=True)

ch3, ch4 = st.columns(2)

# Chart 3: Expense ratio comparison
with ch3:
    sorted_er = filtered.sort_values("Expense Ratio (%)")
    fig3 = go.Figure(layout=base_layout("Expense Ratio Comparison", "", "Expense Ratio (%)", height=360))
    colors_er = [GREEN if v <= 0.15 else (HULL_AMBER if v <= 0.25 else RED) for v in sorted_er["Expense Ratio (%)"]]
    fig3.add_trace(go.Bar(
        y=sorted_er["Fund Name"].str[:20], x=sorted_er["Expense Ratio (%)"], orientation='h',
        marker_color=colors_er, text=sorted_er["Expense Ratio (%)"].apply(lambda v: f"{v}%"),
        textposition="outside", textfont=dict(color=TEXT, size=11),
    ))
    fig3.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig3, use_container_width=True)

# Chart 4: AUM comparison
with ch4:
    sorted_aum = filtered.sort_values("AUM (Rs. Cr)", ascending=False)
    fig4 = go.Figure(layout=base_layout("AUM Comparison (Rs. Cr)", "", "AUM (Rs. Cr)", height=360))
    fig4.add_trace(go.Bar(
        y=sorted_aum["Fund Name"].str[:20], x=sorted_aum["AUM (Rs. Cr)"], orientation='h',
        marker_color=MID_BLUE, text=sorted_aum["AUM (Rs. Cr)"].apply(lambda v: f"₹{v:,}"),
        textposition="outside", textfont=dict(color=TEXT, size=10),
    ))
    fig4.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig4, use_container_width=True)

# Chart 5: Sharpe Ratio bar
st.html(f"""<div style="font-family:'Playfair Display',serif; color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-size:1.1rem; margin:18px 0 6px; user-select:none;">⚖ Risk Metrics Deep Dive</div>""")

rc1, rc2 = st.columns(2)
with rc1:
    sorted_sharpe = filtered.sort_values("Sharpe Ratio", ascending=False)
    fig5 = go.Figure(layout=base_layout("Sharpe Ratio (Higher = Better Risk-Adjusted Return)", "", "Sharpe Ratio", height=360))
    colors_sh = [GREEN if v >= 3.0 else (HULL_AMBER if v >= 2.9 else LIGHT_BLUE) for v in sorted_sharpe["Sharpe Ratio"]]
    fig5.add_trace(go.Bar(
        y=sorted_sharpe["Fund Name"].str[:20], x=sorted_sharpe["Sharpe Ratio"], orientation='h',
        marker_color=colors_sh, text=sorted_sharpe["Sharpe Ratio"].apply(lambda v: f"{v:.2f}"),
        textposition="outside", textfont=dict(color=TEXT, size=11),
    ))
    fig5.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig5, use_container_width=True)

with rc2:
    sorted_sd = filtered.sort_values("Std Dev (%)")
    fig6 = go.Figure(layout=base_layout("Standard Deviation (Lower = Less Volatile)", "", "Std Dev (%)", height=360))
    colors_sd = [GREEN if v <= 14.6 else (HULL_AMBER if v <= 14.9 else RED) for v in sorted_sd["Std Dev (%)"]]
    fig6.add_trace(go.Bar(
        y=sorted_sd["Fund Name"].str[:20], x=sorted_sd["Std Dev (%)"], orientation='h',
        marker_color=colors_sd, text=sorted_sd["Std Dev (%)"].apply(lambda v: f"{v:.1f}%"),
        textposition="outside", textfont=dict(color=TEXT, size=11),
    ))
    fig6.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig6, use_container_width=True)

# ══════════════════════════════════════════════════════════
#  FUND DETAILS
# ══════════════════════════════════════════════════════════
st.html(f"""<div style="font-family:'Playfair Display',serif; color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-size:1.1rem; margin:18px 0 6px; user-select:none;">📋 Fund Details & Key Notes</div>""")

detail_data = pd.DataFrame({
    "Fund Name": funds["Fund Name"],
    "Type": ["Fund of Funds (invests in ICICI Gold ETF)", "Exchange Traded Fund (tracks physical gold)",
             "Fund of Funds (invests in HDFC Gold ETF)", "Fund of Funds (invests in SBI ETF Gold)",
             "Fund of Funds (invests in Nippon India ETF Gold BeES)", "Fund of Funds (invests in Invesco India Gold ETF)",
             "Fund of Funds (invests in Aditya Birla SL Gold ETF)"],
    "Launch Date": funds["Launch Date"],
    "Demat Required?": ["No", "Yes", "No", "No", "No", "No", "No"],
    "SIP Available?": ["Yes (Rs. 100)", "No", "Yes (Rs. 100)", "Yes (Rs. 500)", "Yes (Rs. 100)", "Yes (Rs. 100)", "Yes (Rs. 100)"],
    "Min Lumpsum": ["Rs. 100", "Via exchange", "Rs. 100", "Rs. 5,000", "Rs. 100", "Rs. 1,000", "Rs. 100"],
    "Tax (LTCG >24mo)": ["12.5% w/o indexation"] * 7,
    "Tax (STCG ≤24mo)": ["Slab rate"] * 7,
})
st.dataframe(detail_data, use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════
#  EDUCATIONAL NOTES
# ══════════════════════════════════════════════════════════
st.html(f"""
<div style="background:rgba(240,192,64,0.07); border:1px solid rgba(240,192,64,0.28); border-radius:9px; padding:16px 20px; margin:18px 0; user-select:none;">
    <div style="font-family:'Source Sans Pro',sans-serif; font-size:0.65rem; text-transform:uppercase; letter-spacing:1.8px; color:{MUTED}; -webkit-text-fill-color:{MUTED}; margin-bottom:7px;">Key Insights for Investors</div>
    <div style="font-family:'Source Sans Pro',sans-serif; font-size:0.86rem; line-height:1.7; color:{HULL_AMBER}; -webkit-text-fill-color:{HULL_AMBER};">
        <b>ETF vs FoF:</b> Gold ETFs (like ICICI Prudential Gold ETF) trade on exchanges, require a Demat account, and have lower expense ratios. FoFs invest in these ETFs, don't need Demat, offer SIP, but carry a slightly higher total expense.<br><br>
        <b>Expense Ratio matters:</b> Over 10+ years, even a 0.1% expense difference compounds significantly. ICICI FoF and Invesco FoF lead at 0.10%.<br><br>
        <b>Sharpe Ratio:</b> Measures risk-adjusted return. Above 3.0 is excellent for gold funds. Aditya Birla SL and HDFC lead here.<br><br>
        <b>Standard Deviation:</b> Measures volatility. All gold funds cluster at 14.5–15.1% — gold is inherently volatile as a commodity. Lower is better for risk-averse investors.<br><br>
        <b>AUM:</b> Larger AUM generally means better liquidity and lower tracking error. ICICI Gold ETF (Rs. 25,942 Cr) and SBI Gold Fund (Rs. 14,998 Cr) lead.<br><br>
        <b>Exit Load:</b> Most FoFs charge 1% if redeemed within 15 days. ETFs have no exit load but incur brokerage.
    </div>
</div>
""")

st.html(f"""
<div style="background:rgba(220,53,69,0.06); border:1px solid rgba(220,53,69,0.2); border-left:4px solid {RED}; border-radius:0 9px 9px 0; padding:14px 20px; margin:10px 0; user-select:none;">
    <div style="font-family:'Source Sans Pro',sans-serif; font-size:0.78rem; font-weight:700; color:{RED}; -webkit-text-fill-color:{RED}; margin-bottom:5px;">⚠ Disclaimer</div>
    <div style="font-family:'Source Sans Pro',sans-serif; font-size:0.82rem; line-height:1.5; color:{TEXT}; -webkit-text-fill-color:{TEXT};">
        Mutual fund investments are subject to market risks. Read all scheme-related documents carefully. Past performance is not indicative of future results.
        Data shown is illustrative and sourced from publicly available information as of April 2026. Verify current NAV and returns from the respective AMC websites before investing.
        This dashboard is for <b>educational purposes only</b> and does not constitute investment advice.
    </div>
</div>
""")

# ── Footer ──
st.html(f"""<div style="text-align:center; padding:28px 20px 10px; margin-top:20px; border-top:1px solid rgba(255,215,0,0.12); user-select:none;">
    <div style="font-family:'Playfair Display',serif; color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-size:1rem; margin-bottom:6px;">⛰ The Mountain Path Academy</div>
    <div style="font-family:'Source Sans Pro',sans-serif; color:{MUTED}; -webkit-text-fill-color:{MUTED}; font-size:0.74rem; margin-bottom:4px;">Prof. V. Ravichandran — Visiting Faculty @ NMIMS Bangalore, BITS Pilani, RV University Bangalore, Goa Institute of Management</div>
    <div style="font-family:'Source Sans Pro',sans-serif; font-size:0.76rem;">
        <a href="https://themountainpathacademy.com" target="_blank" style="color:{GOLD}; -webkit-text-fill-color:{GOLD}; text-decoration:none;">themountainpathacademy.com</a> ·
        <a href="https://www.linkedin.com/in/trichyravis" target="_blank" style="color:{GOLD}; -webkit-text-fill-color:{GOLD}; text-decoration:none;">LinkedIn</a> ·
        <a href="https://github.com/trichyravis" target="_blank" style="color:{GOLD}; -webkit-text-fill-color:{GOLD}; text-decoration:none;">GitHub</a>
    </div>
</div>""")
