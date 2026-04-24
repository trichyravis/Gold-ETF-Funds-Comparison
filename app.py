
"""
═══════════════════════════════════════════════════════════════
Gold Fund Comparison Dashboard — LIVE NAV Feed (Enhanced)
The Mountain Path Academy | Prof. V. Ravichandran
═══════════════════════════════════════════════════════════════
Live data via mfapi.in | 7 Indian Gold Funds/ETFs
NAV Timeline Charts: 1W / 1M / 3M / 6M / 1Y / 3Y / 5Y
Today's NAV • Returns • Risk Metrics • Max Drawdown Analysis
"""

import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import requests

st.set_page_config(
    page_title="Gold Fund Dashboard — The Mountain Path Academy",
    page_icon="⛰",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ════════════════════════════════════════════════════════
# MOUNTAIN PATH PALETTE
# ════════════════════════════════════════════════════════
GOLD = "#FFD700"; BLUE = "#003366"; MID_BLUE = "#004d80"; CARD_BG = "#112240"
TEXT = "#e6f1ff"; MUTED = "#8892b0"; GREEN = "#28a745"; RED = "#dc3545"
LIGHT_BLUE = "#ADD8E6"; BG_DARK = "#1a2332"; HULL_AMBER = "#f0c040"; PLOT_BG = "#0a1628"

st.html(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Source+Sans+Pro:wght@300;400;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    .stApp {{ background: linear-gradient(135deg, {BG_DARK}, #243447, #2a3f5f); }}
    #MainMenu, header, footer {{visibility: hidden;}}
    .block-container {{ padding-top: 1.5rem; max-width: 1200px; }}

    .stApp, .stApp p, .stApp span, .stApp label, .stApp div {{
        color: {TEXT} !important; -webkit-text-fill-color: {TEXT} !important;
    }}
    [data-testid="stMetricValue"] {{
        color: {GOLD} !important; -webkit-text-fill-color: {GOLD} !important;
        font-family: 'Playfair Display', serif !important;
    }}
    [data-testid="stMetricLabel"] {{
        color: {LIGHT_BLUE} !important; -webkit-text-fill-color: {LIGHT_BLUE} !important;
        font-size: 0.78rem !important;
    }}
    [data-testid="stMetricDelta"] {{ font-family: 'JetBrains Mono', monospace !important; }}

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
    [data-testid="stDataFrame"] {{ border: 1px solid rgba(255,215,0,0.15); border-radius: 10px; }}

    .stSelectbox label, .stRadio label, .stMultiSelect label, .stSlider label,
    .stNumberInput label, .stTextInput label {{
        color: {LIGHT_BLUE} !important; -webkit-text-fill-color: {LIGHT_BLUE} !important;
        font-weight: 600 !important;
    }}
    .stSelectbox div[data-baseweb="select"] span,
    .stMultiSelect div[data-baseweb="select"] span {{
        color: {TEXT} !important; -webkit-text-fill-color: {TEXT} !important;
    }}

    ul[role="listbox"] {{ background-color: #0f1d2f !important; }}
    ul[role="listbox"] li {{
        color: {TEXT} !important; -webkit-text-fill-color: {TEXT} !important;
        background-color: #0f1d2f !important;
    }}
    ul[role="listbox"] li:hover {{
        background-color: rgba(255,215,0,0.15) !important;
        color: {GOLD} !important; -webkit-text-fill-color: {GOLD} !important;
    }}
    ul[role="listbox"] li[aria-selected="true"] {{
        background-color: rgba(255,215,0,0.10) !important;
        color: {GOLD} !important; -webkit-text-fill-color: {GOLD} !important;
    }}
    ul[role="listbox"] li *, div[data-baseweb="popover"] * {{
        color: inherit !important; -webkit-text-fill-color: inherit !important;
    }}
    div[data-baseweb="popover"] {{
        background-color: #0f1d2f !important; border: 1px solid rgba(255,215,0,0.2) !important;
    }}
    div[data-baseweb="select"] > div {{
        background-color: rgba(0,51,102,0.5) !important; border-color: rgba(255,215,0,0.3) !important;
    }}
    div[data-baseweb="select"] > div > div {{
        color: {TEXT} !important; -webkit-text-fill-color: {TEXT} !important;
    }}
    span[data-baseweb="tag"] {{
        background-color: rgba(255,215,0,0.15) !important;
        color: {GOLD} !important; -webkit-text-fill-color: {GOLD} !important;
    }}
    div[data-baseweb="select"] input {{
        color: {TEXT} !important; -webkit-text-fill-color: {TEXT} !important;
    }}
    .stRadio div[role="radiogroup"] label span {{
        color: {TEXT} !important; -webkit-text-fill-color: {TEXT} !important;
    }}

    .stButton > button {{
        color: {BLUE} !important; -webkit-text-fill-color: {BLUE} !important;
        background-color: {GOLD} !important; border: none !important; font-weight: 700 !important;
    }}
    .stButton > button:hover {{ background-color: #ffe44d !important; }}

    /* Tab styling */
    div.stTabs [data-baseweb="tab-list"] button {{
        color: {MUTED} !important; -webkit-text-fill-color: {MUTED} !important;
        font-family: 'Source Sans Pro', sans-serif !important;
    }}
    div.stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {{
        color: {GOLD} !important; -webkit-text-fill-color: {GOLD} !important;
        border-bottom: 2px solid {GOLD} !important;
    }}
</style>
""")

# ── Header ──
st.html(f"""
<div style="background:rgba(0,51,102,0.92); border-bottom:3px solid {GOLD}; border-radius:12px 12px 0 0;
            padding:18px 28px; margin-bottom:8px; user-select:none;">
    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
        <div>
            <span style="font-family:'Playfair Display',serif; color:{GOLD}; -webkit-text-fill-color:{GOLD};
                         font-size:1.4rem; font-weight:700;">⛰ Indian Gold Fund Comparison Dashboard</span><br>
            <span style="font-family:'Source Sans Pro',sans-serif; color:{LIGHT_BLUE}; -webkit-text-fill-color:{LIGHT_BLUE};
                         font-size:0.84rem;">
                Live NAV via mfapi.in &nbsp;|&nbsp; 7 Funds &nbsp;|&nbsp; NAV Timelines &nbsp;|&nbsp;
                Returns &nbsp;|&nbsp; Risk Metrics &nbsp;|&nbsp; Drawdown Analysis
            </span>
        </div>
        <div style="text-align:right;">
            <span style="font-family:'Source Sans Pro',sans-serif; color:{MUTED}; -webkit-text-fill-color:{MUTED};
                         font-size:0.7rem;">
                Prof. V. Ravichandran · NMIMS · BITS Pilani · RV University · GIM
            </span>
        </div>
    </div>
</div>
""")

# ════════════════════════════════════════════════════════
# FUND METADATA
# ════════════════════════════════════════════════════════
SCHEME_CODES = {
    "ICICI Prudential Gold ETF FoF": 120823,
    "ICICI Prudential Gold ETF": 120826,
    "HDFC Gold Fund (FoF)": 119800,
    "SBI Gold Fund": 120179,
    "Nippon India Gold Savings Fund": 118185,
    "Invesco India Gold ETF FoF": 120390,
    "Aditya Birla SL Gold Fund": 119527,
}

FUND_META = {
    "ICICI Prudential Gold ETF FoF": {"type":"FoF","amc":"ICICI Prudential","expense":0.10,"exit_load":"1% if < 15 days","min_sip":"100","min_lump":"100","launch":"Jan 2013"},
    "ICICI Prudential Gold ETF": {"type":"ETF","amc":"ICICI Prudential","expense":0.50,"exit_load":"Nil (exchange)","min_sip":"N/A (Demat)","min_lump":"N/A (Demat)","launch":"Aug 2010"},
    "HDFC Gold Fund (FoF)": {"type":"FoF","amc":"HDFC","expense":0.20,"exit_load":"1% if < 15 days","min_sip":"100","min_lump":"100","launch":"Nov 2011"},
    "SBI Gold Fund": {"type":"FoF","amc":"SBI","expense":0.25,"exit_load":"1% if < 15 days","min_sip":"500","min_lump":"5,000","launch":"Sep 2011"},
    "Nippon India Gold Savings Fund": {"type":"FoF","amc":"Nippon India","expense":0.13,"exit_load":"1% if < 15 days","min_sip":"100","min_lump":"100","launch":"Mar 2011"},
    "Invesco India Gold ETF FoF": {"type":"FoF","amc":"Invesco","expense":0.10,"exit_load":"1% if < 15 days","min_sip":"100","min_lump":"1,000","launch":"Mar 2012"},
    "Aditya Birla SL Gold Fund": {"type":"FoF","amc":"Aditya Birla SL","expense":0.20,"exit_load":"1% if < 15 days","min_sip":"100","min_lump":"100","launch":"Mar 2012"},
}

FUND_COLORS = {
    "ICICI Prudential Gold ETF FoF": GOLD,
    "ICICI Prudential Gold ETF": "#FF6B6B",
    "HDFC Gold Fund (FoF)": LIGHT_BLUE,
    "SBI Gold Fund": GREEN,
    "Nippon India Gold Savings Fund": HULL_AMBER,
    "Invesco India Gold ETF FoF": "#FF69B4",
    "Aditya Birla SL Gold Fund": "#00CED1",
}

FALLBACK_DATA = {
    "ICICI Prudential Gold ETF FoF": {"nav":48.14,"1y":69.9,"3y":34.0,"5y":25.3,"std":14.8,"sharpe":2.98,"aum":6535,"max_dd":-14.2,"max_dd_date":"Mar 2021"},
    "ICICI Prudential Gold ETF": {"nav":126.67,"1y":63.3,"3y":33.6,"5y":24.9,"std":14.5,"sharpe":2.85,"aum":25942,"max_dd":-13.8,"max_dd_date":"Mar 2021"},
    "HDFC Gold Fund (FoF)": {"nav":45.52,"1y":68.9,"3y":33.7,"5y":25.2,"std":14.9,"sharpe":3.01,"aum":11766,"max_dd":-14.5,"max_dd_date":"Mar 2021"},
    "SBI Gold Fund": {"nav":24.85,"1y":69.1,"3y":34.0,"5y":25.1,"std":14.7,"sharpe":2.95,"aum":14998,"max_dd":-14.0,"max_dd_date":"Mar 2021"},
    "Nippon India Gold Savings Fund": {"nav":56.66,"1y":58.6,"3y":32.1,"5y":24.3,"std":15.1,"sharpe":2.78,"aum":7223,"max_dd":-15.3,"max_dd_date":"Mar 2021"},
    "Invesco India Gold ETF FoF": {"nav":23.45,"1y":67.1,"3y":33.3,"5y":24.7,"std":14.6,"sharpe":2.92,"aum":1420,"max_dd":-14.1,"max_dd_date":"Mar 2021"},
    "Aditya Birla SL Gold Fund": {"nav":22.98,"1y":69.5,"3y":34.0,"5y":25.5,"std":14.8,"sharpe":3.02,"aum":1782,"max_dd":-14.4,"max_dd_date":"Mar 2021"},
}

# ════════════════════════════════════════════════════════
# PLOTLY LAYOUT HELPER
# ════════════════════════════════════════════════════════
def base_layout(title="", xaxis_title="", yaxis_title="", height=420):
    return go.Layout(
        title=dict(text=title, font=dict(family="Playfair Display, serif", size=17, color=GOLD), x=0.01, y=0.97),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor=PLOT_BG,
        font=dict(family="Source Sans Pro, sans-serif", color=TEXT), height=height,
        margin=dict(l=55, r=25, t=50, b=55),
        xaxis=dict(title=dict(text=xaxis_title, font=dict(color=LIGHT_BLUE, size=13)),
                   gridcolor="rgba(255,255,255,0.05)", tickfont=dict(color=MUTED, size=11)),
        yaxis=dict(title=dict(text=yaxis_title, font=dict(color=LIGHT_BLUE, size=13)),
                   gridcolor="rgba(255,255,255,0.05)", tickfont=dict(color=MUTED, size=11)),
        hoverlabel=dict(bgcolor=CARD_BG, font_size=12, font_family="JetBrains Mono", bordercolor=GOLD),
        legend=dict(bgcolor="rgba(17,34,64,0.85)", bordercolor="rgba(255,215,0,0.2)",
                    borderwidth=1, font=dict(size=10, color=TEXT)),
    )

# ════════════════════════════════════════════════════════
# DATA FETCHING — FULL NAV HISTORY
# ════════════════════════════════════════════════════════
@st.cache_data(ttl=3600)
def fetch_full_nav_history(scheme_code, fund_name):
    """Fetch complete NAV history from mfapi.in. Returns a DataFrame with date, nav columns."""
    try:
        resp = requests.get(f"https://api.mfapi.in/mf/{scheme_code}", timeout=15)
        resp.raise_for_status()
        raw = resp.json()
        navs = raw.get("data", [])
        if not navs or len(navs) < 30:
            return None

        records = []
        for entry in navs:
            try:
                dt = datetime.strptime(entry["date"], "%d-%m-%Y")
                nav_val = float(entry["nav"])
                records.append({"date": dt, "nav": nav_val})
            except (ValueError, KeyError):
                continue

        df = pd.DataFrame(records)
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date").drop_duplicates(subset="date").reset_index(drop=True)
        return df
    except Exception:
        return None


def compute_metrics(df):
    """Compute returns, risk metrics, and drawdown from NAV DataFrame."""
    if df is None or len(df) < 30:
        return None

    latest_nav = df.iloc[-1]["nav"]
    latest_date = pd.Timestamp(df.iloc[-1]["date"])

    def find_nav_near(target_date):
        mask = df["date"] <= target_date
        return df.loc[mask, "nav"].iloc[-1] if mask.any() else None

    def cagr(start_nav, end_nav, years):
        if start_nav and start_nav > 0 and years > 0:
            return ((end_nav / start_nav) ** (1 / years) - 1) * 100
        return None

    # Period returns
    periods = {
        "1W": 7, "1M": 30, "3M": 90, "6M": 182, "1Y": 365, "3Y": 365*3, "5Y": 365*5
    }
    returns = {}
    for label, days in periods.items():
        nav_past = find_nav_near(latest_date - timedelta(days=days))
        if nav_past and nav_past > 0:
            if days <= 365:
                returns[label] = round(((latest_nav / nav_past) - 1) * 100, 2)
            else:
                years = days / 365
                returns[label] = round(cagr(nav_past, latest_nav, years), 2) if cagr(nav_past, latest_nav, years) else None
        else:
            returns[label] = None

    # Day change
    if len(df) >= 2:
        prev_nav = df.iloc[-2]["nav"]
        day_change = round(latest_nav - prev_nav, 2)
        day_change_pct = round((latest_nav / prev_nav - 1) * 100, 2) if prev_nav > 0 else 0
    else:
        day_change, day_change_pct = 0, 0

    # Risk metrics (3Y)
    df_3y = df[df["date"] >= latest_date - timedelta(days=365*3)].copy()
    ann_std, sharpe = None, None
    if len(df_3y) > 60:
        df_3y["ret"] = df_3y["nav"].pct_change()
        daily_std = df_3y["ret"].std()
        ann_std = round(daily_std * np.sqrt(252) * 100, 1)
        ann_ret = returns.get("3Y", 0) or 0
        rf_rate = 6.0
        sharpe = round((ann_ret - rf_rate) / ann_std, 2) if ann_std > 0 else 0

    # Max Drawdown
    df_dd = df.copy()
    df_dd["peak"] = df_dd["nav"].cummax()
    df_dd["drawdown"] = (df_dd["nav"] - df_dd["peak"]) / df_dd["peak"] * 100
    max_dd = round(df_dd["drawdown"].min(), 2)
    max_dd_idx = df_dd["drawdown"].idxmin()
    max_dd_date = df_dd.loc[max_dd_idx, "date"].strftime("%b %Y")

    # Drawdown series (5Y)
    dd_5y = df_dd[df_dd["date"] >= latest_date - timedelta(days=365*5)][["date", "drawdown"]].copy()

    return {
        "nav": round(latest_nav, 2),
        "nav_date": latest_date.strftime("%d-%b-%Y"),
        "day_change": day_change,
        "day_change_pct": day_change_pct,
        "returns": returns,
        "std": ann_std,
        "sharpe": sharpe,
        "max_dd": max_dd,
        "max_dd_date": max_dd_date,
        "dd_series": dd_5y,
        "live": True,
    }


# ── Fetch all funds ──
all_nav_histories = {}
all_metrics = {}
data_source = "live"
nav_date_global = "N/A"

with st.spinner("Fetching live NAV data from mfapi.in..."):
    for name, code in SCHEME_CODES.items():
        nav_df = fetch_full_nav_history(code, name)
        if nav_df is not None and len(nav_df) > 30:
            all_nav_histories[name] = nav_df
            metrics = compute_metrics(nav_df)
            if metrics:
                all_metrics[name] = metrics
                nav_date_global = metrics["nav_date"]
            else:
                all_metrics[name] = None
        else:
            all_nav_histories[name] = None
            all_metrics[name] = None
            data_source = "static"

# Build summary DataFrame
fund_rows = []
for name in SCHEME_CODES:
    meta = FUND_META[name]
    fb = FALLBACK_DATA[name]
    m = all_metrics.get(name)

    if m and m.get("live"):
        row = {
            "Fund Name": name, "Type": meta["type"], "AMC": meta["amc"],
            "NAV (₹)": m["nav"],
            "Day Chg (₹)": m["day_change"], "Day Chg (%)": m["day_change_pct"],
            "1W (%)": m["returns"].get("1W"), "1M (%)": m["returns"].get("1M"),
            "3M (%)": m["returns"].get("3M"), "6M (%)": m["returns"].get("6M"),
            "1Y (%)": m["returns"].get("1Y"),
            "3Y CAGR (%)": m["returns"].get("3Y"), "5Y CAGR (%)": m["returns"].get("5Y"),
            "Std Dev (%)": m["std"] if m["std"] else fb["std"],
            "Sharpe Ratio": m["sharpe"] if m["sharpe"] else fb["sharpe"],
            "Max DD (%)": m["max_dd"], "Max DD Date": m["max_dd_date"],
            "Expense (%)": meta["expense"], "AUM (₹ Cr)": fb["aum"],
            "Exit Load": meta["exit_load"], "Min SIP": meta["min_sip"], "Min Lump": meta["min_lump"],
        }
    else:
        data_source = "static"
        row = {
            "Fund Name": name, "Type": meta["type"], "AMC": meta["amc"],
            "NAV (₹)": fb["nav"],
            "Day Chg (₹)": 0, "Day Chg (%)": 0,
            "1W (%)": None, "1M (%)": None, "3M (%)": None, "6M (%)": None,
            "1Y (%)": fb["1y"],
            "3Y CAGR (%)": fb["3y"], "5Y CAGR (%)": fb["5y"],
            "Std Dev (%)": fb["std"], "Sharpe Ratio": fb["sharpe"],
            "Max DD (%)": fb["max_dd"], "Max DD Date": fb["max_dd_date"],
            "Expense (%)": meta["expense"], "AUM (₹ Cr)": fb["aum"],
            "Exit Load": meta["exit_load"], "Min SIP": meta["min_sip"], "Min Lump": meta["min_lump"],
        }
    fund_rows.append(row)

funds = pd.DataFrame(fund_rows)

# ── Data source indicator ──
if data_source == "live":
    st.html(f"""<div style="font-family:'JetBrains Mono',monospace; font-size:0.72rem; color:{GREEN};
        -webkit-text-fill-color:{GREEN}; margin:4px 0 10px; user-select:none;">
        🟢 LIVE DATA — NAVs fetched from mfapi.in (AMFI) as of {nav_date_global} &nbsp;|&nbsp;
        Returns & risk metrics computed from NAV history &nbsp;|&nbsp; Refreshes hourly
    </div>""")
else:
    st.html(f"""<div style="font-family:'JetBrains Mono',monospace; font-size:0.72rem; color:{HULL_AMBER};
        -webkit-text-fill-color:{HULL_AMBER}; margin:4px 0 10px; user-select:none;">
        🟡 STATIC DATA — mfapi.in unavailable; showing cached data. Deploy on Streamlit Cloud for live feed.
    </div>""")


# ════════════════════════════════════════════════════════
# TODAY'S NAV — CARD ROW
# ════════════════════════════════════════════════════════
st.html(f"""<div style="font-family:'Playfair Display',serif; color:{GOLD}; -webkit-text-fill-color:{GOLD};
    font-size:1.15rem; margin:12px 0 8px; user-select:none;">💰 Today's NAV — All Funds</div>""")

nav_cards_html = '<div style="display:flex; flex-wrap:wrap; gap:10px; margin-bottom:16px;">'
for _, row in funds.iterrows():
    chg = row["Day Chg (₹)"]
    chg_pct = row["Day Chg (%)"]
    chg_color = GREEN if chg >= 0 else RED
    arrow = "▲" if chg >= 0 else "▼"
    nav_cards_html += f"""
    <div style="background:{CARD_BG}; border:1px solid rgba(255,215,0,0.15); border-radius:10px;
                padding:14px 18px; min-width:155px; flex:1; user-select:none;">
        <div style="font-family:'Source Sans Pro',sans-serif; color:{LIGHT_BLUE}; -webkit-text-fill-color:{LIGHT_BLUE};
                    font-size:0.72rem; font-weight:600; margin-bottom:4px; white-space:nowrap; overflow:hidden;
                    text-overflow:ellipsis;">{row['Fund Name'][:22]}</div>
        <div style="font-family:'Playfair Display',serif; color:{GOLD}; -webkit-text-fill-color:{GOLD};
                    font-size:1.4rem; font-weight:700;">₹{row['NAV (₹)']:.2f}</div>
        <div style="font-family:'JetBrains Mono',monospace; color:{chg_color}; -webkit-text-fill-color:{chg_color};
                    font-size:0.78rem; margin-top:2px;">
            {arrow} ₹{abs(chg):.2f} ({chg_pct:+.2f}%)
        </div>
        <div style="font-family:'Source Sans Pro',sans-serif; color:{MUTED}; -webkit-text-fill-color:{MUTED};
                    font-size:0.62rem; margin-top:3px;">{row['Type']} · {row['AMC'][:12]}</div>
    </div>"""
nav_cards_html += '</div>'
st.html(nav_cards_html)

# ════════════════════════════════════════════════════════
# TOP METRICS
# ════════════════════════════════════════════════════════
best_1y = funds.loc[funds["1Y (%)"].idxmax()]
best_sharpe = funds.loc[funds["Sharpe Ratio"].idxmax()]
lowest_er = funds.loc[funds["Expense (%)"].idxmin()]
largest_aum = funds.loc[funds["AUM (₹ Cr)"].idxmax()]

m1, m2, m3, m4 = st.columns(4)
m1.metric("Best 1Y Return", f"{best_1y['1Y (%)']}%", best_1y['Fund Name'][:22])
m2.metric("Best Sharpe Ratio", f"{best_sharpe['Sharpe Ratio']}", best_sharpe['Fund Name'][:22])
m3.metric("Lowest Expense", f"{lowest_er['Expense (%)']}%", lowest_er['Fund Name'][:22])
m4.metric("Largest AUM", f"₹{largest_aum['AUM (₹ Cr)']:,} Cr", largest_aum['Fund Name'][:22])

# ════════════════════════════════════════════════════════
# FILTERS
# ════════════════════════════════════════════════════════
st.html(f"""<div style="font-family:'Playfair Display',serif; color:{GOLD}; -webkit-text-fill-color:{GOLD};
    font-size:1.1rem; margin:16px 0 6px; user-select:none;">🔍 Filter & Sort</div>""")

fc1, fc2, fc3 = st.columns(3)
with fc1:
    sort_by = st.selectbox("Sort by", ["1Y (%)","3Y CAGR (%)","5Y CAGR (%)","Sharpe Ratio",
                                        "Max DD (%)","Expense (%)","AUM (₹ Cr)","Std Dev (%)"])
with fc2:
    sort_order = st.radio("Order", ["Descending","Ascending"], horizontal=True)
with fc3:
    fund_filter = st.multiselect("Select Funds", funds["Fund Name"].tolist(), default=funds["Fund Name"].tolist())

ascending = sort_order == "Ascending"
filtered = funds[funds["Fund Name"].isin(fund_filter)].sort_values(sort_by, ascending=ascending).reset_index(drop=True)

# ════════════════════════════════════════════════════════
# MAIN TABS
# ════════════════════════════════════════════════════════
main_tabs = st.tabs(["📊 Comparison Table","📈 NAV Timelines","📉 Returns Charts",
                      "⚖ Risk Metrics","📉 Drawdown Analysis"])

# ─── TAB 1: COMPARISON TABLE ────────────────────────────
with main_tabs[0]:
    st.html(f"""<div style="font-family:'Playfair Display',serif; color:{GOLD}; -webkit-text-fill-color:{GOLD};
        font-size:1.1rem; margin:8px 0 6px; user-select:none;">📊 Fund Comparison Table</div>""")

    display_cols = ["Fund Name","Type","NAV (₹)","Day Chg (₹)","Day Chg (%)",
                    "1W (%)","1M (%)","3M (%)","6M (%)","1Y (%)",
                    "3Y CAGR (%)","5Y CAGR (%)","Std Dev (%)","Sharpe Ratio",
                    "Max DD (%)","Expense (%)","AUM (₹ Cr)","Exit Load","Min SIP"]
    st.dataframe(filtered[display_cols], use_container_width=True, hide_index=True, height=340)

    # Multi-period returns heatmap-style table
    st.html(f"""<div style="font-family:'Playfair Display',serif; color:{GOLD}; -webkit-text-fill-color:{GOLD};
        font-size:1.05rem; margin:18px 0 6px; user-select:none;">📅 Multi-Period Returns at a Glance</div>""")

    ret_cols = ["Fund Name","1W (%)","1M (%)","3M (%)","6M (%)","1Y (%)","3Y CAGR (%)","5Y CAGR (%)"]
    st.dataframe(filtered[ret_cols], use_container_width=True, hide_index=True, height=300)


# ─── TAB 2: NAV TIMELINES ───────────────────────────────
with main_tabs[1]:
    st.html(f"""<div style="font-family:'Playfair Display',serif; color:{GOLD}; -webkit-text-fill-color:{GOLD};
        font-size:1.1rem; margin:8px 0 4px; user-select:none;">📈 NAV Price Charts</div>""")

    has_live = any(all_nav_histories.get(f) is not None for f in fund_filter)

    if has_live:
        # Period selector
        period_map = {"1 Week":7, "1 Month":30, "3 Months":90, "6 Months":182,
                      "1 Year":365, "3 Years":365*3, "5 Years":365*5, "All Time":None}

        pc1, pc2 = st.columns([3, 1])
        with pc1:
            selected_period = st.selectbox("Select Period", list(period_map.keys()), index=4)
        with pc2:
            chart_type = st.radio("Chart Style", ["Absolute NAV","Normalised (₹100)"], horizontal=True)

        lookback_days = period_map[selected_period]

        # Use a GLOBAL cutoff date (most recent NAV date across all funds)
        global_latest = datetime(2020, 1, 1)
        for fn in fund_filter:
            ndf = all_nav_histories.get(fn)
            if ndf is not None and len(ndf) > 0:
                fund_latest = pd.Timestamp(ndf.iloc[-1]["date"]).to_pydatetime()
                if fund_latest > global_latest:
                    global_latest = fund_latest

        if lookback_days:
            global_cutoff = global_latest - timedelta(days=lookback_days)
        else:
            global_cutoff = None

        # ── OVERLAY CHART: All selected funds on one plot ──
        fig_nav = go.Figure(layout=base_layout(
            f"NAV Movement — {selected_period}", "Date",
            "NAV (₹)" if chart_type=="Absolute NAV" else "Value (₹100 base)", 480))

        for fund_name in fund_filter:
            nav_df = all_nav_histories.get(fund_name)
            if nav_df is None or len(nav_df) < 10:
                continue

            # Ensure date column is datetime
            if not pd.api.types.is_datetime64_any_dtype(nav_df["date"]):
                nav_df = nav_df.copy()
                nav_df["date"] = pd.to_datetime(nav_df["date"])

            # Filter to selected period using GLOBAL cutoff
            if global_cutoff:
                plot_df = nav_df[nav_df["date"] >= pd.Timestamp(global_cutoff)].copy()
            else:
                plot_df = nav_df.copy()

            if len(plot_df) < 2:
                continue

            if chart_type == "Normalised (₹100)":
                base_nav = plot_df.iloc[0]["nav"]
                if base_nav > 0:
                    plot_df["nav_plot"] = (plot_df["nav"] / base_nav) * 100
                else:
                    continue
                y_col = "nav_plot"
            else:
                y_col = "nav"

            color = FUND_COLORS.get(fund_name, MUTED)
            fig_nav.add_trace(go.Scatter(
                x=plot_df["date"], y=plot_df[y_col], mode="lines",
                name=fund_name[:22], line=dict(color=color, width=2),
                hovertemplate=f"<b>{fund_name[:20]}</b><br>Date: %{{x|%d %b %Y}}<br>NAV: ₹%{{y:.2f}}<extra></extra>"
            ))

        st.plotly_chart(fig_nav, use_container_width=True)

        # ── INDIVIDUAL FUND NAV CHARTS (2 per row) ──
        st.html(f"""<div style="font-family:'Source Sans Pro',sans-serif; color:{LIGHT_BLUE};
            -webkit-text-fill-color:{LIGHT_BLUE}; font-size:0.95rem; font-weight:600;
            margin:14px 0 8px; user-select:none;">Individual Fund NAV Charts — {selected_period}</div>""")

        active_funds = [f for f in fund_filter if all_nav_histories.get(f) is not None]
        for i in range(0, len(active_funds), 2):
            cols = st.columns(2)
            for j, col in enumerate(cols):
                if i + j < len(active_funds):
                    fname = active_funds[i + j]
                    nav_df = all_nav_histories[fname]

                    if not pd.api.types.is_datetime64_any_dtype(nav_df["date"]):
                        nav_df = nav_df.copy()
                        nav_df["date"] = pd.to_datetime(nav_df["date"])

                    if global_cutoff:
                        pdf = nav_df[nav_df["date"] >= pd.Timestamp(global_cutoff)].copy()
                    else:
                        pdf = nav_df.copy()

                    if len(pdf) < 2:
                        continue

                    start_nav = pdf.iloc[0]["nav"]
                    end_nav = pdf.iloc[-1]["nav"]
                    period_ret = ((end_nav / start_nav) - 1) * 100
                    line_color = GREEN if period_ret >= 0 else RED
                    fill_color = "rgba(40,167,69,0.10)" if period_ret >= 0 else "rgba(220,53,69,0.10)"

                    with col:
                        fig_ind = go.Figure(layout=base_layout(
                            f"{fname[:25]} — {period_ret:+.1f}%", "", "NAV (₹)", 280))
                        fig_ind.add_trace(go.Scatter(
                            x=pdf["date"], y=pdf["nav"], mode="lines",
                            line=dict(color=line_color, width=2),
                            fill="tozeroy", fillcolor=fill_color, showlegend=False,
                            hovertemplate="Date: %{x|%d %b %Y}<br>NAV: ₹%{y:.2f}<extra></extra>",
                        ))
                        # Mark start and end
                        fig_ind.add_trace(go.Scatter(
                            x=[pdf.iloc[0]["date"], pdf.iloc[-1]["date"]],
                            y=[start_nav, end_nav], mode="markers+text",
                            marker=dict(color=GOLD, size=8, line=dict(color=line_color, width=2)),
                            text=[f"₹{start_nav:.2f}", f"₹{end_nav:.2f}"],
                            textposition=["bottom center","top center"],
                            textfont=dict(color=GOLD, size=10), showlegend=False,
                        ))
                        fig_ind.update_layout(margin=dict(l=45, r=15, t=40, b=35))
                        st.plotly_chart(fig_ind, use_container_width=True)
    else:
        st.html(f"""<div style="font-family:'Source Sans Pro',sans-serif; color:{MUTED};
            -webkit-text-fill-color:{MUTED}; font-size:0.85rem; margin:12px 0; user-select:none;">
            ℹ NAV timeline charts require live data from mfapi.in. Deploy on Streamlit Cloud for interactive NAV charts.
        </div>""")


# ─── TAB 3: RETURNS CHARTS ──────────────────────────────
with main_tabs[2]:
    ch1, ch2 = st.columns(2)
    with ch1:
        fig1 = go.Figure(layout=base_layout("Returns: 1Y vs 3Y vs 5Y CAGR","","Return (%)", 420))
        for col, color, name in [("1Y (%)",GOLD,"1-Year"),("3Y CAGR (%)",LIGHT_BLUE,"3-Year CAGR"),("5Y CAGR (%)",GREEN,"5-Year CAGR")]:
            fig1.add_trace(go.Bar(
                y=filtered["Fund Name"].str[:20], x=filtered[col], orientation='h',
                name=name, marker_color=color, opacity=0.85,
                text=filtered[col].apply(lambda v: f"{v}%" if pd.notna(v) else "N/A"),
                textposition="outside", textfont=dict(color=TEXT, size=10)))
        fig1.update_layout(barmode='group', yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig1, use_container_width=True)

    with ch2:
        fig2 = go.Figure(layout=base_layout("Risk-Return Profile (3Y CAGR vs Std Dev)","Standard Deviation (%)","3Y CAGR (%)", 420))
        fig2.add_trace(go.Scatter(
            x=filtered["Std Dev (%)"], y=filtered["3Y CAGR (%)"],
            mode="markers+text", text=filtered["Fund Name"].str[:15],
            textposition="top center", textfont=dict(color=TEXT, size=10),
            marker=dict(size=filtered["AUM (₹ Cr)"].apply(lambda v: max(12,min(40,v/500))),
                        color=filtered["Sharpe Ratio"], colorscale=[[0,RED],[0.5,HULL_AMBER],[1,GREEN]],
                        showscale=True, colorbar=dict(title="Sharpe", tickfont=dict(color=MUTED)),
                        line=dict(color=GOLD, width=1.5)),
            hovertemplate="<b>%{text}</b><br>Std Dev: %{x:.1f}%<br>3Y CAGR: %{y:.1f}%<extra></extra>"))
        st.plotly_chart(fig2, use_container_width=True)

    ch3, ch4 = st.columns(2)
    with ch3:
        sorted_er = filtered.sort_values("Expense (%)")
        fig3 = go.Figure(layout=base_layout("Expense Ratio Comparison","","Expense Ratio (%)", 360))
        colors_er = [GREEN if v<=0.15 else (HULL_AMBER if v<=0.25 else RED) for v in sorted_er["Expense (%)"]]
        fig3.add_trace(go.Bar(y=sorted_er["Fund Name"].str[:20], x=sorted_er["Expense (%)"], orientation='h',
            marker_color=colors_er, text=sorted_er["Expense (%)"].apply(lambda v: f"{v}%"),
            textposition="outside", textfont=dict(color=TEXT, size=11)))
        fig3.update_layout(yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig3, use_container_width=True)

    with ch4:
        sorted_aum = filtered.sort_values("AUM (₹ Cr)", ascending=False)
        fig4 = go.Figure(layout=base_layout("AUM Comparison (₹ Cr)","","AUM (₹ Cr)", 360))
        fig4.add_trace(go.Bar(y=sorted_aum["Fund Name"].str[:20], x=sorted_aum["AUM (₹ Cr)"], orientation='h',
            marker_color=MID_BLUE, text=sorted_aum["AUM (₹ Cr)"].apply(lambda v: f"₹{v:,}"),
            textposition="outside", textfont=dict(color=TEXT, size=10)))
        fig4.update_layout(yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig4, use_container_width=True)


# ─── TAB 4: RISK METRICS ────────────────────────────────
with main_tabs[3]:
    rc1, rc2 = st.columns(2)
    with rc1:
        sorted_sh = filtered.sort_values("Sharpe Ratio", ascending=False)
        fig5 = go.Figure(layout=base_layout("Sharpe Ratio (Higher = Better)","","Sharpe Ratio", 360))
        colors_sh = [GREEN if v>=3.0 else (HULL_AMBER if v>=2.9 else LIGHT_BLUE) for v in sorted_sh["Sharpe Ratio"]]
        fig5.add_trace(go.Bar(y=sorted_sh["Fund Name"].str[:20], x=sorted_sh["Sharpe Ratio"], orientation='h',
            marker_color=colors_sh, text=sorted_sh["Sharpe Ratio"].apply(lambda v: f"{v:.2f}"),
            textposition="outside", textfont=dict(color=TEXT, size=11)))
        fig5.update_layout(yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig5, use_container_width=True)

    with rc2:
        sorted_sd = filtered.sort_values("Std Dev (%)")
        fig6 = go.Figure(layout=base_layout("Standard Deviation (Lower = Less Volatile)","","Std Dev (%)", 360))
        colors_sd = [GREEN if v<=14.6 else (HULL_AMBER if v<=14.9 else RED) for v in sorted_sd["Std Dev (%)"]]
        fig6.add_trace(go.Bar(y=sorted_sd["Fund Name"].str[:20], x=sorted_sd["Std Dev (%)"], orientation='h',
            marker_color=colors_sd, text=sorted_sd["Std Dev (%)"].apply(lambda v: f"{v:.1f}%"),
            textposition="outside", textfont=dict(color=TEXT, size=11)))
        fig6.update_layout(yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig6, use_container_width=True)


# ─── TAB 5: DRAWDOWN ANALYSIS ───────────────────────────
with main_tabs[4]:
    st.html(f"""<div style="font-family:'Playfair Display',serif; color:{GOLD}; -webkit-text-fill-color:{GOLD};
        font-size:1.1rem; margin:8px 0 6px; user-select:none;">📉 Maximum Drawdown Analysis</div>""")

    st.html(f"""<div style="font-family:'Source Sans Pro',sans-serif; color:{MUTED}; -webkit-text-fill-color:{MUTED};
        font-size:0.84rem; margin-bottom:12px; user-select:none;">
        Max Drawdown = largest peak-to-trough decline (%). Measures the worst loss an investor would have experienced.
        Lower (closer to 0%) is better.
    </div>""")

    sorted_dd = filtered.sort_values("Max DD (%)", ascending=False)
    fig_dd = go.Figure(layout=base_layout("Max Drawdown by Fund (Closer to 0% = Better)","","Max Drawdown (%)", 380))
    colors_dd = [GREEN if v>=-13.0 else (HULL_AMBER if v>=-14.5 else RED) for v in sorted_dd["Max DD (%)"]]
    fig_dd.add_trace(go.Bar(
        y=sorted_dd["Fund Name"].str[:20], x=sorted_dd["Max DD (%)"], orientation='h',
        marker_color=colors_dd,
        text=sorted_dd.apply(lambda r: f"{r['Max DD (%)']:.1f}% ({r['Max DD Date']})", axis=1),
        textposition="outside", textfont=dict(color=TEXT, size=10)))
    fig_dd.update_layout(yaxis=dict(autorange="reversed"))
    fig_dd.update_xaxes(range=[min(sorted_dd["Max DD (%)"]) - 3, 0])
    st.plotly_chart(fig_dd, use_container_width=True)

    # Drawdown timeline overlay
    dd_funds = {f: all_metrics[f] for f in fund_filter if all_metrics.get(f) and all_metrics[f].get("dd_series") is not None}

    if dd_funds:
        st.html(f"""<div style="font-family:'Source Sans Pro',sans-serif; color:{LIGHT_BLUE};
            -webkit-text-fill-color:{LIGHT_BLUE}; font-size:0.95rem; font-weight:600;
            margin:14px 0 8px; user-select:none;">Drawdown Over Time (Last 5 Years)</div>""")

        fig_ddov = go.Figure(layout=base_layout("Drawdown Timeline — All Funds","Date","Drawdown (%)", 450))
        for idx, (fname, m) in enumerate(dd_funds.items()):
            dd_df = m["dd_series"]
            color = FUND_COLORS.get(fname, MUTED)
            fig_ddov.add_trace(go.Scatter(
                x=dd_df["date"], y=dd_df["drawdown"], mode="lines",
                name=fname[:20], line=dict(color=color, width=1.8),
                fill="tozeroy",
                fillcolor=f"rgba({int(color.lstrip('#')[0:2],16)},{int(color.lstrip('#')[2:4],16)},{int(color.lstrip('#')[4:6],16)},0.05)",
                hovertemplate=f"<b>{fname[:20]}</b><br>%{{x|%b %Y}}<br>DD: %{{y:.1f}}%<extra></extra>"))
        fig_ddov.add_shape(type="line", x0=0, x1=1, xref="paper", y0=0, y1=0,
                           line=dict(color=MUTED, width=0.5, dash="dot"))
        fig_ddov.update_yaxes(ticksuffix="%")
        st.plotly_chart(fig_ddov, use_container_width=True)

        # Individual drawdowns
        st.html(f"""<div style="font-family:'Source Sans Pro',sans-serif; color:{LIGHT_BLUE};
            -webkit-text-fill-color:{LIGHT_BLUE}; font-size:0.95rem; font-weight:600;
            margin:14px 0 8px; user-select:none;">Individual Fund Drawdown Profiles</div>""")

        dd_list = list(dd_funds.keys())
        for i in range(0, len(dd_list), 2):
            cols = st.columns(2)
            for j, col in enumerate(cols):
                if i+j < len(dd_list):
                    fn = dd_list[i+j]
                    dd_df = dd_funds[fn]["dd_series"]
                    with col:
                        fig_i = go.Figure(layout=base_layout(fn[:25],"","Drawdown (%)", 280))
                        fig_i.add_trace(go.Scatter(
                            x=dd_df["date"], y=dd_df["drawdown"], mode="lines",
                            line=dict(color=RED, width=1.5), fill="tozeroy",
                            fillcolor="rgba(220,53,69,0.12)", showlegend=False,
                            hovertemplate="Date: %{x|%b %Y}<br>DD: %{y:.1f}%<extra></extra>"))
                        min_idx = dd_df["drawdown"].idxmin()
                        fig_i.add_trace(go.Scatter(
                            x=[dd_df.loc[min_idx,"date"]], y=[dd_df.loc[min_idx,"drawdown"]],
                            mode="markers+text",
                            marker=dict(color=GOLD, size=10, symbol="diamond", line=dict(color=RED, width=2)),
                            text=[f"{dd_df.loc[min_idx,'drawdown']:.1f}%"],
                            textposition="top center", textfont=dict(color=GOLD, size=11), showlegend=False))
                        fig_i.add_shape(type="line", x0=0, x1=1, xref="paper", y0=0, y1=0,
                                        line=dict(color=MUTED, width=0.5, dash="dot"))
                        fig_i.update_yaxes(ticksuffix="%")
                        fig_i.update_layout(margin=dict(l=45, r=15, t=40, b=35))
                        st.plotly_chart(fig_i, use_container_width=True)


# ════════════════════════════════════════════════════════
# EDUCATIONAL NOTES & DISCLAIMER
# ════════════════════════════════════════════════════════
st.html(f"""
<div style="background:rgba(240,192,64,0.07); border:1px solid rgba(240,192,64,0.28); border-radius:9px;
            padding:16px 20px; margin:18px 0; user-select:none;">
    <div style="font-family:'Source Sans Pro',sans-serif; font-size:0.65rem; text-transform:uppercase;
                letter-spacing:1.8px; color:{MUTED}; -webkit-text-fill-color:{MUTED}; margin-bottom:7px;">
        Key Insights for Investors</div>
    <div style="font-family:'Source Sans Pro',sans-serif; font-size:0.86rem; line-height:1.7;
                color:{HULL_AMBER}; -webkit-text-fill-color:{HULL_AMBER};">
        <b>🔄 Live Data:</b> NAVs are fetched from mfapi.in (AMFI source). Returns and risk metrics are computed
        from actual NAV history — not static snapshots. Data refreshes hourly.<br><br>
        <b>📈 NAV Timelines:</b> Charts show absolute NAV or normalised (₹100 base) performance across 1W, 1M, 3M,
        6M, 1Y, 3Y, 5Y, and All Time. Normalised view eliminates NAV-level bias and reveals true relative performance.<br><br>
        <b>ETF vs FoF:</b> Gold ETFs trade on exchanges (Demat needed, lower expense). FoFs invest in ETFs (no Demat, SIP available, slightly higher total expense).<br><br>
        <b>Expense Ratio:</b> Over 10+ years, even 0.1% difference compounds significantly. ICICI FoF and Invesco FoF lead at 0.10%.<br><br>
        <b>Sharpe Ratio:</b> Risk-adjusted return = (Fund Return − Risk-Free Rate) / Std Dev. Above 3.0 is excellent.<br><br>
        <b>📉 Max Drawdown:</b> Worst peak-to-trough decline in NAV history. Tells you the maximum loss if you bought at the peak and sold at the trough.
    </div>
</div>
""")

st.html(f"""
<div style="background:rgba(220,53,69,0.06); border:1px solid rgba(220,53,69,0.2); border-left:4px solid {RED};
            border-radius:0 9px 9px 0; padding:14px 20px; margin:10px 0; user-select:none;">
    <div style="font-family:'Source Sans Pro',sans-serif; font-size:0.78rem; font-weight:700;
                color:{RED}; -webkit-text-fill-color:{RED}; margin-bottom:5px;">⚠ Disclaimer</div>
    <div style="font-family:'Source Sans Pro',sans-serif; font-size:0.82rem; line-height:1.5;
                color:{TEXT}; -webkit-text-fill-color:{TEXT};">
        Mutual fund investments are subject to market risks. Read all scheme-related documents carefully.
        Past performance is not indicative of future results. NAV data sourced from mfapi.in (AMFI).
        This dashboard is for <b>educational purposes only</b> and does not constitute investment advice.
    </div>
</div>
""")

# ── Footer ──
st.html(f"""<div style="text-align:center; padding:28px 20px 10px; margin-top:20px;
    border-top:1px solid rgba(255,215,0,0.12); user-select:none;">
    <div style="font-family:'Playfair Display',serif; color:{GOLD}; -webkit-text-fill-color:{GOLD};
                font-size:1rem; margin-bottom:6px;">⛰ The Mountain Path Academy</div>
    <div style="font-family:'Source Sans Pro',sans-serif; color:{MUTED}; -webkit-text-fill-color:{MUTED};
                font-size:0.74rem; margin-bottom:4px;">
        Prof. V. Ravichandran — Visiting Faculty @ NMIMS Bangalore, BITS Pilani, RV University Bangalore,
        Goa Institute of Management</div>
    <div style="font-family:'Source Sans Pro',sans-serif; font-size:0.76rem;">
        <a href="https://themountainpathacademy.com" target="_blank"
           style="color:{GOLD}; -webkit-text-fill-color:{GOLD}; text-decoration:none;">themountainpathacademy.com</a> ·
        <a href="https://www.linkedin.com/in/trichyravis" target="_blank"
           style="color:{GOLD}; -webkit-text-fill-color:{GOLD}; text-decoration:none;">LinkedIn</a> ·
        <a href="https://github.com/trichyravis" target="_blank"
           style="color:{GOLD}; -webkit-text-fill-color:{GOLD}; text-decoration:none;">GitHub</a>
    </div>
</div>""")
