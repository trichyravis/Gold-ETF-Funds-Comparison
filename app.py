
"""
Gold Fund Comparison Dashboard — LIVE NAV Feed
The Mountain Path Academy | Prof. V. Ravichandran
═══════════════════════════════════════
Live data via mfapi.in | 7 Indian Gold Funds/ETFs
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import requests
import json

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

    /* ── Fix contrast across all Streamlit elements ── */
    .stApp, .stApp p, .stApp span, .stApp label, .stApp div {{
        color: {TEXT} !important;
        -webkit-text-fill-color: {TEXT} !important;
    }}
    [data-testid="stMetricValue"] {{
        color: {GOLD} !important; -webkit-text-fill-color: {GOLD} !important;
        font-family: 'Playfair Display', serif !important;
    }}
    [data-testid="stMetricLabel"] {{
        color: {LIGHT_BLUE} !important; -webkit-text-fill-color: {LIGHT_BLUE} !important;
        font-size: 0.78rem !important;
    }}
    [data-testid="stMetricDelta"] {{
        font-family: 'JetBrains Mono', monospace !important;
    }}

    /* ── Dataframe/table contrast fix ── */
    .stDataFrame, .stDataFrame div, .stDataFrame span, .stDataFrame td, .stDataFrame th,
    [data-testid="stDataFrame"] div, [data-testid="stDataFrame"] span {{
        color: {TEXT} !important; -webkit-text-fill-color: {TEXT} !important;
    }}
    [data-testid="stDataFrame"] [role="gridcell"] {{
        color: {TEXT} !important; -webkit-text-fill-color: {TEXT} !important;
        background-color: {CARD_BG} !important;
    }}
    [data-testid="stDataFrame"] [role="columnheader"] {{
        color: {GOLD} !important; -webkit-text-fill-color: {GOLD} !important;
        background-color: {BLUE} !important;
    }}
    [data-testid="stDataFrame"] {{
        border: 1px solid rgba(255,215,0,0.15); border-radius: 10px;
    }}

    /* ── Selectbox, radio, multiselect contrast fix ── */
    .stSelectbox label, .stRadio label, .stMultiSelect label, .stSlider label,
    .stNumberInput label, .stTextInput label {{
        color: {LIGHT_BLUE} !important; -webkit-text-fill-color: {LIGHT_BLUE} !important;
        font-weight: 600 !important;
    }}
    .stSelectbox div[data-baseweb="select"] span,
    .stMultiSelect div[data-baseweb="select"] span {{
        color: {TEXT} !important; -webkit-text-fill-color: {TEXT} !important;
    }}

    /* ── DROPDOWN MENU — nuclear override for BaseWeb popover ── */
    ul[role="listbox"] {{
        background-color: #0f1d2f !important;
    }}
    ul[role="listbox"] li {{
        color: {TEXT} !important;
        -webkit-text-fill-color: {TEXT} !important;
        background-color: #0f1d2f !important;
    }}
    ul[role="listbox"] li:hover {{
        background-color: rgba(255,215,0,0.15) !important;
        color: {GOLD} !important;
        -webkit-text-fill-color: {GOLD} !important;
    }}
    ul[role="listbox"] li[aria-selected="true"] {{
        background-color: rgba(255,215,0,0.10) !important;
        color: {GOLD} !important;
        -webkit-text-fill-color: {GOLD} !important;
    }}
    /* Catch-all for any nested spans/divs inside dropdown options */
    ul[role="listbox"] li *,
    div[data-baseweb="popover"] * {{
        color: inherit !important;
        -webkit-text-fill-color: inherit !important;
    }}
    div[data-baseweb="popover"] {{
        background-color: #0f1d2f !important;
        border: 1px solid rgba(255,215,0,0.2) !important;
    }}

    /* Selected value inside the selectbox input area */
    div[data-baseweb="select"] > div {{
        background-color: rgba(0,51,102,0.5) !important;
        border-color: rgba(255,215,0,0.3) !important;
    }}
    div[data-baseweb="select"] > div > div {{
        color: {TEXT} !important;
        -webkit-text-fill-color: {TEXT} !important;
    }}
    /* Multiselect tags */
    span[data-baseweb="tag"] {{
        background-color: rgba(255,215,0,0.15) !important;
        color: {GOLD} !important;
        -webkit-text-fill-color: {GOLD} !important;
    }}
    /* Input text in search within selectbox */
    div[data-baseweb="select"] input {{
        color: {TEXT} !important;
        -webkit-text-fill-color: {TEXT} !important;
    }}
    .stRadio div[role="radiogroup"] label span {{
        color: {TEXT} !important; -webkit-text-fill-color: {TEXT} !important;
    }}

    /* ── Button contrast ── */
    .stButton > button {{
        color: {BLUE} !important; -webkit-text-fill-color: {BLUE} !important;
        background-color: {GOLD} !important;
        border: none !important; font-weight: 700 !important;
    }}
    .stButton > button:hover {{
        background-color: #ffe44d !important;
    }}
</style>
""")

# ── Header ──
st.html(f"""
<div style="background:rgba(0,51,102,0.92); border-bottom:3px solid {GOLD}; border-radius:12px 12px 0 0; padding:18px 28px; margin-bottom:8px; user-select:none;">
    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
        <div>
            <span style="font-family:'Playfair Display',serif; color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-size:1.4rem; font-weight:700;">⛰ Indian Gold Fund Comparison Dashboard</span><br>
            <span style="font-family:'Source Sans Pro',sans-serif; color:{LIGHT_BLUE}; -webkit-text-fill-color:{LIGHT_BLUE}; font-size:0.84rem;">
                Live NAV via mfapi.in &nbsp;|&nbsp; 7 Funds &nbsp;|&nbsp; Returns &nbsp;|&nbsp; Risk Metrics &nbsp;|&nbsp; Sortable
            </span>
        </div>
        <div style="text-align:right;">
            <span style="font-family:'Source Sans Pro',sans-serif; color:{MUTED}; -webkit-text-fill-color:{MUTED}; font-size:0.7rem;">Prof. V. Ravichandran · NMIMS · BITS Pilani · RV University · GIM</span>
        </div>
    </div>
</div>
""")

# ══════════════════════════════════════════════════════════
#  LIVE DATA FETCH FROM mfapi.in
# ══════════════════════════════════════════════════════════

# AMFI Scheme Codes (Direct Growth Plans)
SCHEME_CODES = {
    "ICICI Prudential Gold ETF FoF": 120823,
    "ICICI Prudential Gold ETF": 120826,
    "HDFC Gold Fund (FoF)": 119800,
    "SBI Gold Fund": 120179,
    "Nippon India Gold Savings Fund": 118185,
    "Invesco India Gold ETF FoF": 120390,
    "Aditya Birla SL Gold Fund": 119527,
}

# Static metadata (not available from mfapi.in)
FUND_META = {
    "ICICI Prudential Gold ETF FoF": {"type": "FoF", "amc": "ICICI Prudential", "expense": 0.10, "exit_load": "1% if < 15 days", "min_sip": "100", "min_lump": "100", "launch": "Jan 2013"},
    "ICICI Prudential Gold ETF": {"type": "ETF", "amc": "ICICI Prudential", "expense": 0.50, "exit_load": "Nil (exchange)", "min_sip": "N/A (Demat)", "min_lump": "N/A (Demat)", "launch": "Aug 2010"},
    "HDFC Gold Fund (FoF)": {"type": "FoF", "amc": "HDFC", "expense": 0.20, "exit_load": "1% if < 15 days", "min_sip": "100", "min_lump": "100", "launch": "Nov 2011"},
    "SBI Gold Fund": {"type": "FoF", "amc": "SBI", "expense": 0.25, "exit_load": "1% if < 15 days", "min_sip": "500", "min_lump": "5,000", "launch": "Sep 2011"},
    "Nippon India Gold Savings Fund": {"type": "FoF", "amc": "Nippon India", "expense": 0.13, "exit_load": "1% if < 15 days", "min_sip": "100", "min_lump": "100", "launch": "Mar 2011"},
    "Invesco India Gold ETF FoF": {"type": "FoF", "amc": "Invesco", "expense": 0.10, "exit_load": "1% if < 15 days", "min_sip": "100", "min_lump": "1,000", "launch": "Mar 2012"},
    "Aditya Birla SL Gold Fund": {"type": "FoF", "amc": "Aditya Birla SL", "expense": 0.20, "exit_load": "1% if < 15 days", "min_sip": "100", "min_lump": "100", "launch": "Mar 2012"},
}

# Fallback static data (used if API is unavailable)
FALLBACK_DATA = {
    "ICICI Prudential Gold ETF FoF": {"nav": 48.14, "1y": 69.9, "3y": 34.0, "5y": 25.3, "std": 14.8, "sharpe": 2.98, "aum": 6535, "max_dd": -14.2, "max_dd_date": "Mar 2021"},
    "ICICI Prudential Gold ETF": {"nav": 126.67, "1y": 63.3, "3y": 33.6, "5y": 24.9, "std": 14.5, "sharpe": 2.85, "aum": 25942, "max_dd": -13.8, "max_dd_date": "Mar 2021"},
    "HDFC Gold Fund (FoF)": {"nav": 45.52, "1y": 68.9, "3y": 33.7, "5y": 25.2, "std": 14.9, "sharpe": 3.01, "aum": 11766, "max_dd": -14.5, "max_dd_date": "Mar 2021"},
    "SBI Gold Fund": {"nav": 24.85, "1y": 69.1, "3y": 34.0, "5y": 25.1, "std": 14.7, "sharpe": 2.95, "aum": 14998, "max_dd": -14.0, "max_dd_date": "Mar 2021"},
    "Nippon India Gold Savings Fund": {"nav": 56.66, "1y": 58.6, "3y": 32.1, "5y": 24.3, "std": 15.1, "sharpe": 2.78, "aum": 7223, "max_dd": -15.3, "max_dd_date": "Mar 2021"},
    "Invesco India Gold ETF FoF": {"nav": 23.45, "1y": 67.1, "3y": 33.3, "5y": 24.7, "std": 14.6, "sharpe": 2.92, "aum": 1420, "max_dd": -14.1, "max_dd_date": "Mar 2021"},
    "Aditya Birla SL Gold Fund": {"nav": 22.98, "1y": 69.5, "3y": 34.0, "5y": 25.5, "std": 14.8, "sharpe": 3.02, "aum": 1782, "max_dd": -14.4, "max_dd_date": "Mar 2021"},
}


@st.cache_data(ttl=3600)  # Cache for 1 hour
def fetch_nav_data(scheme_code, fund_name):
    """Fetch NAV history from mfapi.in and compute returns + risk metrics."""
    try:
        resp = requests.get(f"https://api.mfapi.in/mf/{scheme_code}", timeout=10)
        resp.raise_for_status()
        raw = resp.json()
        navs = raw.get("data", [])
        if not navs or len(navs) < 30:
            return None

        # Parse NAV history
        records = []
        for entry in navs:
            try:
                dt = datetime.strptime(entry["date"], "%d-%m-%Y")
                nav_val = float(entry["nav"])
                records.append({"date": dt, "nav": nav_val})
            except (ValueError, KeyError):
                continue

        df = pd.DataFrame(records).sort_values("date").reset_index(drop=True)
        latest_nav = df.iloc[-1]["nav"]
        latest_date = df.iloc[-1]["date"]

        # Compute returns
        def cagr(start_nav, end_nav, years):
            if start_nav <= 0 or years <= 0:
                return None
            return ((end_nav / start_nav) ** (1 / years) - 1) * 100

        def find_nav_near(target_date):
            mask = df["date"] <= target_date
            if mask.any():
                return df.loc[mask, "nav"].iloc[-1]
            return None

        nav_1y = find_nav_near(latest_date - timedelta(days=365))
        nav_3y = find_nav_near(latest_date - timedelta(days=365 * 3))
        nav_5y = find_nav_near(latest_date - timedelta(days=365 * 5))

        ret_1y = ((latest_nav / nav_1y) - 1) * 100 if nav_1y else None
        ret_3y = cagr(nav_3y, latest_nav, 3) if nav_3y else None
        ret_5y = cagr(nav_5y, latest_nav, 5) if nav_5y else None

        # Risk metrics (annualised from daily returns, last 3 years)
        df_3y = df[df["date"] >= latest_date - timedelta(days=365 * 3)].copy()
        if len(df_3y) > 60:
            df_3y["ret"] = df_3y["nav"].pct_change()
            daily_std = df_3y["ret"].std()
            ann_std = daily_std * np.sqrt(252) * 100  # annualised %
            ann_ret = (ret_3y if ret_3y else 0)
            rf_rate = 6.0  # approximate Indian risk-free rate
            sharpe = (ann_ret - rf_rate) / ann_std if ann_std > 0 else 0
        else:
            ann_std, sharpe = None, None

        # Max Drawdown (full history)
        df["peak"] = df["nav"].cummax()
        df["drawdown"] = (df["nav"] - df["peak"]) / df["peak"] * 100  # negative %
        max_dd = df["drawdown"].min()  # most negative value
        max_dd_date = df.loc[df["drawdown"].idxmin(), "date"]

        # Drawdown series for plotting (last 5 years)
        df_dd = df[df["date"] >= latest_date - timedelta(days=365 * 5)][["date", "drawdown"]].copy()

        return {
            "nav": round(latest_nav, 2),
            "nav_date": latest_date.strftime("%d-%b-%Y"),
            "1y": round(ret_1y, 1) if ret_1y else None,
            "3y": round(ret_3y, 1) if ret_3y else None,
            "5y": round(ret_5y, 1) if ret_5y else None,
            "std": round(ann_std, 1) if ann_std else None,
            "sharpe": round(sharpe, 2) if sharpe else None,
            "max_dd": round(max_dd, 2),
            "max_dd_date": max_dd_date.strftime("%b %Y"),
            "dd_series": df_dd,
            "live": True,
        }
    except Exception:
        return None


# ── Fetch all funds ──
data_source = "live"
fund_rows = []
nav_date = "N/A"
dd_series_map = {}  # store drawdown time series per fund

with st.spinner("Fetching live NAV data from mfapi.in..."):
    for name, code in SCHEME_CODES.items():
        result = fetch_nav_data(code, name)
        meta = FUND_META[name]
        fallback = FALLBACK_DATA[name]

        if result and result.get("live"):
            row = {
                "Fund Name": name,
                "Type": meta["type"],
                "AMC": meta["amc"],
                "NAV (Rs.)": result["nav"],
                "1Y Return (%)": result["1y"] if result["1y"] else fallback["1y"],
                "3Y CAGR (%)": result["3y"] if result["3y"] else fallback["3y"],
                "5Y CAGR (%)": result["5y"] if result["5y"] else fallback["5y"],
                "Std Dev (%)": result["std"] if result["std"] else fallback["std"],
                "Sharpe Ratio": result["sharpe"] if result["sharpe"] else fallback["sharpe"],
                "Max Drawdown (%)": result.get("max_dd", fallback["max_dd"]),
                "Max DD Date": result.get("max_dd_date", fallback["max_dd_date"]),
                "Expense Ratio (%)": meta["expense"],
                "AUM (Rs. Cr)": fallback["aum"],
                "Exit Load": meta["exit_load"],
                "Min SIP (Rs.)": meta["min_sip"],
                "Min Lumpsum (Rs.)": meta["min_lump"],
            }
            nav_date = result.get("nav_date", nav_date)
            if result.get("dd_series") is not None and len(result["dd_series"]) > 0:
                dd_series_map[name] = result["dd_series"]
        else:
            data_source = "static"
            row = {
                "Fund Name": name,
                "Type": meta["type"],
                "AMC": meta["amc"],
                "NAV (Rs.)": fallback["nav"],
                "1Y Return (%)": fallback["1y"],
                "3Y CAGR (%)": fallback["3y"],
                "5Y CAGR (%)": fallback["5y"],
                "Std Dev (%)": fallback["std"],
                "Sharpe Ratio": fallback["sharpe"],
                "Max Drawdown (%)": fallback["max_dd"],
                "Max DD Date": fallback["max_dd_date"],
                "Expense Ratio (%)": meta["expense"],
                "AUM (Rs. Cr)": fallback["aum"],
                "Exit Load": meta["exit_load"],
                "Min SIP (Rs.)": meta["min_sip"],
                "Min Lumpsum (Rs.)": meta["min_lump"],
            }
        fund_rows.append(row)

funds = pd.DataFrame(fund_rows)

# ── Data source indicator ──
if data_source == "live":
    st.html(f"""<div style="font-family:'JetBrains Mono',monospace; font-size:0.72rem; color:{GREEN}; -webkit-text-fill-color:{GREEN}; margin:4px 0 10px; user-select:none;">
        🟢 LIVE DATA — NAVs fetched from mfapi.in (AMFI) as of {nav_date} &nbsp;|&nbsp; Returns & risk metrics computed from NAV history &nbsp;|&nbsp; Refreshes hourly
    </div>""")
else:
    st.html(f"""<div style="font-family:'JetBrains Mono',monospace; font-size:0.72rem; color:{HULL_AMBER}; -webkit-text-fill-color:{HULL_AMBER}; margin:4px 0 10px; user-select:none;">
        🟡 STATIC DATA — mfapi.in unavailable; showing cached data (Apr 2026). Deploy on Streamlit Cloud for live feed.
    </div>""")

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
    sort_by = st.selectbox("Sort by", ["1Y Return (%)", "3Y CAGR (%)", "5Y CAGR (%)", "Sharpe Ratio", "Max Drawdown (%)", "Expense Ratio (%)", "AUM (Rs. Cr)", "Std Dev (%)"])
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
                "Max Drawdown (%)", "Max DD Date", "Exit Load", "Min SIP (Rs.)", "Min Lumpsum (Rs.)"]
st.dataframe(filtered[display_cols], use_container_width=True, hide_index=True, height=320)

# ══════════════════════════════════════════════════════════
#  CHARTS
# ══════════════════════════════════════════════════════════
st.html(f"""<div style="font-family:'Playfair Display',serif; color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-size:1.1rem; margin:18px 0 6px; user-select:none;">📈 Visual Comparisons</div>""")

ch1, ch2 = st.columns(2)

with ch1:
    fig1 = go.Figure(layout=base_layout("Returns: 1Y vs 3Y vs 5Y CAGR", "", "Return (%)", height=420))
    for col, color, name in [("1Y Return (%)", GOLD, "1-Year"), ("3Y CAGR (%)", LIGHT_BLUE, "3-Year CAGR"), ("5Y CAGR (%)", GREEN, "5-Year CAGR")]:
        fig1.add_trace(go.Bar(
            y=filtered["Fund Name"].str[:20], x=filtered[col], orientation='h',
            name=name, marker_color=color, opacity=0.85,
            text=filtered[col].apply(lambda v: f"{v}%"), textposition="outside",
            textfont=dict(color=TEXT, size=10)))
    fig1.update_layout(barmode='group', yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig1, use_container_width=True)

with ch2:
    fig2 = go.Figure(layout=base_layout("Risk-Return Profile (3Y CAGR vs Std Dev)", "Standard Deviation (%)", "3Y CAGR (%)", height=420))
    fig2.add_trace(go.Scatter(
        x=filtered["Std Dev (%)"], y=filtered["3Y CAGR (%)"],
        mode="markers+text", text=filtered["Fund Name"].str[:15],
        textposition="top center", textfont=dict(color=TEXT, size=10),
        marker=dict(size=filtered["AUM (Rs. Cr)"].apply(lambda v: max(12, min(40, v / 500))),
                    color=filtered["Sharpe Ratio"], colorscale=[[0, RED], [0.5, HULL_AMBER], [1, GREEN]],
                    showscale=True, colorbar=dict(title="Sharpe", tickfont=dict(color=MUTED)),
                    line=dict(color=GOLD, width=1.5)),
        hovertemplate="<b>%{text}</b><br>Std Dev: %{x:.1f}%<br>3Y CAGR: %{y:.1f}%<extra></extra>"))
    st.plotly_chart(fig2, use_container_width=True)

ch3, ch4 = st.columns(2)

with ch3:
    sorted_er = filtered.sort_values("Expense Ratio (%)")
    fig3 = go.Figure(layout=base_layout("Expense Ratio Comparison", "", "Expense Ratio (%)", height=360))
    colors_er = [GREEN if v <= 0.15 else (HULL_AMBER if v <= 0.25 else RED) for v in sorted_er["Expense Ratio (%)"]]
    fig3.add_trace(go.Bar(y=sorted_er["Fund Name"].str[:20], x=sorted_er["Expense Ratio (%)"], orientation='h',
        marker_color=colors_er, text=sorted_er["Expense Ratio (%)"].apply(lambda v: f"{v}%"),
        textposition="outside", textfont=dict(color=TEXT, size=11)))
    fig3.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig3, use_container_width=True)

with ch4:
    sorted_aum = filtered.sort_values("AUM (Rs. Cr)", ascending=False)
    fig4 = go.Figure(layout=base_layout("AUM Comparison (Rs. Cr)", "", "AUM (Rs. Cr)", height=360))
    fig4.add_trace(go.Bar(y=sorted_aum["Fund Name"].str[:20], x=sorted_aum["AUM (Rs. Cr)"], orientation='h',
        marker_color=MID_BLUE, text=sorted_aum["AUM (Rs. Cr)"].apply(lambda v: f"₹{v:,}"),
        textposition="outside", textfont=dict(color=TEXT, size=10)))
    fig4.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig4, use_container_width=True)

# ── Risk metrics ──
st.html(f"""<div style="font-family:'Playfair Display',serif; color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-size:1.1rem; margin:18px 0 6px; user-select:none;">⚖ Risk Metrics Deep Dive</div>""")

rc1, rc2 = st.columns(2)
with rc1:
    sorted_sharpe = filtered.sort_values("Sharpe Ratio", ascending=False)
    fig5 = go.Figure(layout=base_layout("Sharpe Ratio (Higher = Better)", "", "Sharpe Ratio", height=360))
    colors_sh = [GREEN if v >= 3.0 else (HULL_AMBER if v >= 2.9 else LIGHT_BLUE) for v in sorted_sharpe["Sharpe Ratio"]]
    fig5.add_trace(go.Bar(y=sorted_sharpe["Fund Name"].str[:20], x=sorted_sharpe["Sharpe Ratio"], orientation='h',
        marker_color=colors_sh, text=sorted_sharpe["Sharpe Ratio"].apply(lambda v: f"{v:.2f}"),
        textposition="outside", textfont=dict(color=TEXT, size=11)))
    fig5.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig5, use_container_width=True)

with rc2:
    sorted_sd = filtered.sort_values("Std Dev (%)")
    fig6 = go.Figure(layout=base_layout("Standard Deviation (Lower = Less Volatile)", "", "Std Dev (%)", height=360))
    colors_sd = [GREEN if v <= 14.6 else (HULL_AMBER if v <= 14.9 else RED) for v in sorted_sd["Std Dev (%)"]]
    fig6.add_trace(go.Bar(y=sorted_sd["Fund Name"].str[:20], x=sorted_sd["Std Dev (%)"], orientation='h',
        marker_color=colors_sd, text=sorted_sd["Std Dev (%)"].apply(lambda v: f"{v:.1f}%"),
        textposition="outside", textfont=dict(color=TEXT, size=11)))
    fig6.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig6, use_container_width=True)

# ══════════════════════════════════════════════════════════
#  MAX DRAWDOWN ANALYSIS
# ══════════════════════════════════════════════════════════
st.html(f"""<div style="font-family:'Playfair Display',serif; color:{GOLD}; -webkit-text-fill-color:{GOLD}; font-size:1.1rem; margin:18px 0 6px; user-select:none;">📉 Maximum Drawdown Analysis</div>""")

st.html(f"""<div style="font-family:'Source Sans Pro',sans-serif; color:{MUTED}; -webkit-text-fill-color:{MUTED}; font-size:0.84rem; margin-bottom:12px; user-select:none;">
    Max Drawdown = largest peak-to-trough decline (%). Measures the worst loss an investor would have experienced. Lower (closer to 0%) is better.
</div>""")

# Bar chart: Max Drawdown comparison
sorted_dd = filtered.sort_values("Max Drawdown (%)", ascending=False)  # least negative first = best
fig_dd = go.Figure(layout=base_layout("Max Drawdown by Fund (Closer to 0% = Better)", "", "Max Drawdown (%)", height=380))
colors_dd = [GREEN if v >= -13.0 else (HULL_AMBER if v >= -14.5 else RED) for v in sorted_dd["Max Drawdown (%)"]]
fig_dd.add_trace(go.Bar(
    y=sorted_dd["Fund Name"].str[:20],
    x=sorted_dd["Max Drawdown (%)"],
    orientation='h',
    marker_color=colors_dd,
    text=sorted_dd.apply(lambda r: f"{r['Max Drawdown (%)']:.1f}% ({r['Max DD Date']})", axis=1),
    textposition="outside",
    textfont=dict(color=TEXT, size=10),
))
fig_dd.update_layout(yaxis=dict(autorange="reversed"))
fig_dd.update_xaxes(range=[min(sorted_dd["Max Drawdown (%)"]) - 3, 0])
st.plotly_chart(fig_dd, use_container_width=True)

# Drawdown timeline charts (only if live data with dd_series is available)
if dd_series_map:
    st.html(f"""<div style="font-family:'Source Sans Pro',sans-serif; color:{LIGHT_BLUE}; -webkit-text-fill-color:{LIGHT_BLUE}; font-size:0.95rem; font-weight:600; margin:14px 0 8px; user-select:none;">
        Drawdown Over Time (Last 5 Years) — From Live NAV History
    </div>""")

    # Overlay chart: all funds on one drawdown timeline
    fig_dd_overlay = go.Figure(layout=base_layout(
        "Drawdown Timeline — All Funds Overlaid", "Date", "Drawdown (%)", height=450))

    dd_colors = [GOLD, LIGHT_BLUE, GREEN, RED, HULL_AMBER, MID_BLUE, "#FF69B4"]
    for idx, (fund_name, dd_df) in enumerate(dd_series_map.items()):
        if fund_name in fund_filter:
            fig_dd_overlay.add_trace(go.Scatter(
                x=dd_df["date"], y=dd_df["drawdown"],
                mode="lines", name=fund_name[:20],
                line=dict(color=dd_colors[idx % len(dd_colors)], width=1.8),
                fill="tozeroy",
                fillcolor=f"rgba({int(dd_colors[idx % len(dd_colors)].lstrip('#')[0:2], 16)},{int(dd_colors[idx % len(dd_colors)].lstrip('#')[2:4], 16)},{int(dd_colors[idx % len(dd_colors)].lstrip('#')[4:6], 16)},0.05)",
                hovertemplate=f"<b>{fund_name[:20]}</b><br>Date: %{{x|%b %Y}}<br>Drawdown: %{{y:.1f}}%<extra></extra>",
            ))

    fig_dd_overlay.add_shape(type="line", x0=0, x1=1, xref="paper", y0=0, y1=0,
                             line=dict(color=MUTED, width=0.5, dash="dot"))
    fig_dd_overlay.update_yaxes(ticksuffix="%")
    st.plotly_chart(fig_dd_overlay, use_container_width=True)

    # Individual fund drawdown charts (2 per row)
    st.html(f"""<div style="font-family:'Source Sans Pro',sans-serif; color:{LIGHT_BLUE}; -webkit-text-fill-color:{LIGHT_BLUE}; font-size:0.95rem; font-weight:600; margin:14px 0 8px; user-select:none;">
        Individual Fund Drawdown Profiles
    </div>""")

    selected_dd_funds = [f for f in fund_filter if f in dd_series_map]
    for i in range(0, len(selected_dd_funds), 2):
        cols = st.columns(2)
        for j, col in enumerate(cols):
            if i + j < len(selected_dd_funds):
                fname = selected_dd_funds[i + j]
                dd_df = dd_series_map[fname]
                with col:
                    fig_ind = go.Figure(layout=base_layout(
                        fname[:25], "", "Drawdown (%)", height=280))
                    fig_ind.add_trace(go.Scatter(
                        x=dd_df["date"], y=dd_df["drawdown"],
                        mode="lines", line=dict(color=RED, width=1.5),
                        fill="tozeroy", fillcolor="rgba(220,53,69,0.12)",
                        hovertemplate="Date: %{x|%b %Y}<br>Drawdown: %{y:.1f}%<extra></extra>",
                        showlegend=False,
                    ))
                    # Mark the max drawdown point
                    min_idx = dd_df["drawdown"].idxmin()
                    fig_ind.add_trace(go.Scatter(
                        x=[dd_df.loc[min_idx, "date"]],
                        y=[dd_df.loc[min_idx, "drawdown"]],
                        mode="markers+text",
                        marker=dict(color=GOLD, size=10, symbol="diamond", line=dict(color=RED, width=2)),
                        text=[f"{dd_df.loc[min_idx, 'drawdown']:.1f}%"],
                        textposition="top center",
                        textfont=dict(color=GOLD, size=11),
                        showlegend=False,
                        hovertemplate=f"Max DD: {dd_df.loc[min_idx, 'drawdown']:.1f}%<br>Date: %{{x|%d %b %Y}}<extra></extra>",
                    ))
                    fig_ind.add_shape(type="line", x0=0, x1=1, xref="paper", y0=0, y1=0,
                                     line=dict(color=MUTED, width=0.5, dash="dot"))
                    fig_ind.update_yaxes(ticksuffix="%")
                    fig_ind.update_layout(margin=dict(l=45, r=15, t=40, b=35))
                    st.plotly_chart(fig_ind, use_container_width=True)
else:
    st.html(f"""<div style="font-family:'Source Sans Pro',sans-serif; color:{MUTED}; -webkit-text-fill-color:{MUTED}; font-size:0.82rem; margin:8px 0; user-select:none;">
        ℹ Drawdown timeline charts require live NAV data from mfapi.in. Deploy on Streamlit Cloud to see interactive drawdown timelines for each fund.
    </div>""")

# ══════════════════════════════════════════════════════════
#  EDUCATIONAL NOTES
# ══════════════════════════════════════════════════════════
st.html(f"""
<div style="background:rgba(240,192,64,0.07); border:1px solid rgba(240,192,64,0.28); border-radius:9px; padding:16px 20px; margin:18px 0; user-select:none;">
    <div style="font-family:'Source Sans Pro',sans-serif; font-size:0.65rem; text-transform:uppercase; letter-spacing:1.8px; color:{MUTED}; -webkit-text-fill-color:{MUTED}; margin-bottom:7px;">Key Insights for Investors</div>
    <div style="font-family:'Source Sans Pro',sans-serif; font-size:0.86rem; line-height:1.7; color:{HULL_AMBER}; -webkit-text-fill-color:{HULL_AMBER};">
        <b>🔄 Live Data:</b> NAVs are fetched from mfapi.in (AMFI source). Returns and risk metrics (Std Dev, Sharpe) are computed from actual NAV history — not static snapshots. Data refreshes hourly.<br><br>
        <b>ETF vs FoF:</b> Gold ETFs trade on exchanges and require a Demat account with lower expense ratios. FoFs invest in these ETFs, don't need Demat, offer SIP, but carry slightly higher total expense.<br><br>
        <b>Expense Ratio:</b> Over 10+ years, even 0.1% difference compounds significantly. ICICI FoF and Invesco FoF lead at 0.10%.<br><br>
        <b>Sharpe Ratio:</b> Risk-adjusted return = (Fund Return − Risk-Free Rate) / Std Dev. Above 3.0 is excellent for gold funds.<br><br>
        <b>Std Dev:</b> Annualised volatility from daily NAV returns. All gold funds cluster at 14.5–15.1% — gold is inherently volatile.<br><br>
        <b>📉 Max Drawdown:</b> The worst peak-to-trough decline in NAV history. Tells you the maximum loss you could have faced if you bought at the peak and sold at the trough. Most gold funds saw their worst drawdown during the 2021 gold correction. Lower (closer to 0%) is better.
    </div>
</div>
""")

st.html(f"""
<div style="background:rgba(220,53,69,0.06); border:1px solid rgba(220,53,69,0.2); border-left:4px solid {RED}; border-radius:0 9px 9px 0; padding:14px 20px; margin:10px 0; user-select:none;">
    <div style="font-family:'Source Sans Pro',sans-serif; font-size:0.78rem; font-weight:700; color:{RED}; -webkit-text-fill-color:{RED}; margin-bottom:5px;">⚠ Disclaimer</div>
    <div style="font-family:'Source Sans Pro',sans-serif; font-size:0.82rem; line-height:1.5; color:{TEXT}; -webkit-text-fill-color:{TEXT};">
        Mutual fund investments are subject to market risks. Read all scheme-related documents carefully. Past performance is not indicative of future results.
        NAV data sourced from mfapi.in (AMFI). AUM and expense ratios may lag by up to one month. This dashboard is for <b>educational purposes only</b> and does not constitute investment advice.
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
