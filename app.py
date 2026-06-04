"""
Tea.ai — V1 Consumer Insights Workspace
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(page_title="Tea.ai", page_icon="🍵", layout="wide",
                   initial_sidebar_state="expanded")

NAVY   = "#0B2A4A"; NAVY_SOFT = "#13355A"
SAGE   = "#7A9E7E"; SAGE_DEEP  = "#5E8463"
GOLD   = "#C8A86B"; GOLD_DEEP  = "#A8884B"
BG     = "#FAFAF8"; CARD       = "#FFFFFF"
INK    = "#1F2937"; SOFT       = "#6B7280"; FAINT = "#9AA1AC"
BORDER = "#E5E7EB"; BORDER_SOFT = "#EEF0F2"
OK_BG  = "#EDF3EE"; WARN_BG    = "#F7F1E3"
RED    = "#B45454"

DATA_PATH = Path(__file__).parent / "data" / "tea_verbatims_mock.csv"

# ─── GLOBAL CSS ──────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
/* ── Reset & base ── */
*, *::before, *::after {{ box-sizing: border-box; }}
html, body, [data-testid="stAppViewContainer"] {{
  height: 100vh; max-height: 100vh; overflow: hidden;
  font-family: 'Inter', 'Segoe UI', sans-serif;
  background: {BG}; color: {INK};
  -webkit-font-smoothing: antialiased;
}}
[data-testid="stAppViewContainer"] > .main {{
  height: 100vh; overflow: hidden; padding: 0;
}}
.main .block-container {{
  padding: 0 !important; max-width: 100% !important;
  height: 100vh; overflow: hidden;
}}
.stApp {{ background: {BG}; }}
#MainMenu, footer, header {{ visibility: hidden; }}

/* ── Sidebar (fixed, no scroll) ── */
section[data-testid="stSidebar"] {{
  background: {CARD};
  border-right: 1px solid {BORDER};
  height: 100vh;
  overflow: hidden !important;
}}
section[data-testid="stSidebar"] > div {{
  height: 100vh;
  overflow: hidden !important;
  display: flex;
  flex-direction: column;
}}
section[data-testid="stSidebar"] .block-container {{
  padding: 0 1rem 1rem !important;
  flex: 1;
  overflow: hidden !important;
  display: flex;
  flex-direction: column;
}}

/* ── Brand ── */
.brand {{
  display: flex; align-items: center; gap: 11px;
  padding: 1.2rem 0 0.2rem;
}}
.brand-mark {{
  width: 36px; height: 36px; border-radius: 9px; flex-shrink: 0;
  background: linear-gradient(135deg, {NAVY}, {NAVY_SOFT});
  color: #fff; font-weight: 800; font-size: 16px;
  display: flex; align-items: center; justify-content: center;
}}
.brand-name {{ font-weight: 700; font-size: 18px; color: {NAVY}; letter-spacing: -.3px; }}
.brand-name span {{ color: {GOLD_DEEP}; }}
.brand-sub {{ font-size: 11px; color: {SOFT}; margin-top: -2px; }}

/* ── About card ── */
.about-card {{
  background: {BG}; border: 1px solid {BORDER}; border-radius: 10px;
  padding: 12px 14px; margin: 10px 0 6px;
}}
.about-label {{
  font-size: 10px; font-weight: 700; letter-spacing: .6px; text-transform: uppercase;
  color: {GOLD_DEEP}; margin-bottom: 6px;
}}
.about-row {{ font-size: 11.5px; color: {INK}; line-height: 1.5; margin-bottom: 4px; }}
.about-row b {{ color: {NAVY}; }}

/* ── Nav section label ── */
.nav-section-label {{
  font-size: 10px; font-weight: 700; letter-spacing: .6px; text-transform: uppercase;
  color: {FAINT}; margin: 14px 0 6px 2px;
}}

/* ── Nav buttons (hide Streamlit radio, inject custom) ── */
div[data-testid="stSidebar"] div[role="radiogroup"] {{
  display: flex; flex-direction: column; gap: 6px;
}}
div[data-testid="stSidebar"] div[role="radiogroup"] > label {{
  display: flex !important;
  align-items: center;
  width: 100%;
  min-height: 42px;
  padding: 10px 14px !important;
  border-radius: 9px !important;
  border: 1px solid {BORDER} !important;
  background: {CARD} !important;
  cursor: pointer !important;
  font-size: 13.5px !important;
  font-weight: 600 !important;
  color: {INK} !important;
  transition: all .15s ease !important;
  margin: 0 !important;
}}
div[data-testid="stSidebar"] div[role="radiogroup"] > label:hover {{
  border-color: {NAVY} !important;
  background: #F0F4F8 !important;
  color: {NAVY} !important;
}}
div[data-testid="stSidebar"] div[role="radiogroup"] > label[data-baseweb="radio"] > div:first-child {{
  display: none !important;
}}
div[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) {{
  background: {NAVY} !important;
  border-color: {NAVY} !important;
  color: #fff !important;
  box-shadow: 0 2px 8px rgba(11,42,74,.25) !important;
}}
div[data-testid="stSidebar"] div[role="radiogroup"] input {{ display: none !important; }}
div[data-testid="stSidebar"] div[role="radiogroup"] p {{
  font-size: 13.5px !important;
  font-weight: 600 !important;
  margin: 0 !important;
  line-height: 1 !important;
}}

/* ── Main content area scrollable ── */
[data-testid="stMainBlockContainer"] {{
  height: 100vh;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 16px 22px 10px !important;
}}

/* ── Tighten default Streamlit element gaps ── */
div[data-testid="stPlotlyChart"] {{ margin-bottom: 0 !important; padding-bottom: 0 !important; }}
.stElementContainer {{ margin-bottom: 0 !important; }}
[data-testid="stVerticalBlock"] {{ gap: 0.4rem !important; }}

/* ── Page headers ── */
.page-header {{
  margin-bottom: 12px;
  padding-bottom: 10px;
  border-bottom: 1px solid {BORDER_SOFT};
}}
.page-title {{
  font-size: 22px; font-weight: 800; color: {NAVY}; letter-spacing: -.5px; margin-bottom: 2px;
}}
.page-sub {{ font-size: 12.5px; color: {SOFT}; }}

/* ── Generic card ── */
.card {{
  background: {CARD}; border: 1px solid {BORDER}; border-radius: 12px;
  padding: 12px 16px;
  box-shadow: 0 1px 2px rgba(11,42,74,.04), 0 4px 16px rgba(11,42,74,.05);
  margin-bottom: 10px;
}}
.card-title {{ font-size: 13px; font-weight: 700; color: {NAVY}; margin-bottom: 2px; }}
.card-sub {{ font-size: 11px; color: {SOFT}; margin-bottom: 8px; }}

/* ── KPI cards ── */
.kpi-row {{ display: flex; gap: 10px; margin-bottom: 12px; }}
.kpi-card {{
  flex: 1; background: {CARD}; border: 1px solid {BORDER}; border-radius: 12px;
  padding: 11px 14px;
  box-shadow: 0 1px 2px rgba(11,42,74,.04), 0 4px 16px rgba(11,42,74,.05);
}}
.kpi-label {{ font-size: 10px; font-weight: 700; letter-spacing: .5px; text-transform: uppercase; color: {SOFT}; margin-bottom: 4px; }}
.kpi-value {{ font-size: 22px; font-weight: 800; color: {NAVY}; letter-spacing: -.8px; line-height: 1; }}
.kpi-sub {{ font-size: 10.5px; color: {SOFT}; margin-top: 3px; }}
.kpi-delta {{ font-size: 10.5px; font-weight: 700; margin-top: 3px; }}
.delta-neg {{ color: {RED}; }}
.delta-pos {{ color: {SAGE_DEEP}; }}
.kpi-accent {{ border-top: 3px solid {NAVY}; }}
.kpi-accent-sage {{ border-top: 3px solid {SAGE_DEEP}; }}
.kpi-accent-gold {{ border-top: 3px solid {GOLD_DEEP}; }}
.kpi-accent-red {{ border-top: 3px solid {RED}; }}

/* ── Insight badge ── */
.insight-badge {{
  display: inline-flex; align-items: center; gap: 6px;
  font-size: 11px; font-weight: 700; padding: 4px 10px;
  border-radius: 20px; margin-right: 6px; margin-bottom: 4px;
}}
.badge-navy {{ background: #EAF0F6; color: {NAVY}; }}
.badge-sage {{ background: {OK_BG}; color: {SAGE_DEEP}; }}
.badge-gold {{ background: {WARN_BG}; color: {GOLD_DEEP}; }}
.badge-red {{ background: #FDECEA; color: {RED}; }}

/* ── Summary box ── */
.summary-box {{
  background: linear-gradient(180deg, #fff, {BG});
  border: 1px solid {BORDER}; border-left: 4px solid {SAGE};
  border-radius: 10px; padding: 12px 14px;
}}
.summary-box p {{ font-size: 13px; line-height: 1.55; color: {INK}; margin-bottom: 6px; }}
.summary-box strong {{ color: {NAVY}; }}

/* ── AI panel ── */
.prompt-chip {{ background:{NAVY};color:#fff;border-radius:10px;padding:10px 14px;
  font-size:13.5px;font-weight:600;display:inline-block; }}
.resp-card {{ background:{CARD};border:1px solid {BORDER};border-radius:12px;padding:18px 20px;
  box-shadow:0 1px 2px rgba(11,42,74,.04),0 4px 16px rgba(11,42,74,.05); }}
.resp-card h4 {{ color:{NAVY};font-size:15px;margin:2px 0 10px; }}
.resp-card p {{ font-size:13.5px;line-height:1.62;color:{INK};margin-bottom:10px; }}
.resp-card strong {{ color:{NAVY}; }}
.src-chip {{ display:inline-block;font-size:9.5px;font-weight:700;padding:1px 6px;border-radius:5px;
  margin-right:5px;background:#EAF0F6;color:{NAVY};vertical-align:middle; }}

/* ── Stray Streamlit padding cleanup ── */
div[data-testid="column"] > div {{ padding: 0 !important; }}
.stSelectbox label {{ font-size: 12px !important; font-weight: 600 !important; color: {SOFT} !important; }}
.stTextInput label {{ font-size: 12px !important; font-weight: 600 !important; color: {SOFT} !important; }}
.stSelectbox > div > div {{
  border-radius: 9px !important; border-color: {BORDER} !important;
  font-size: 13px !important;
}}
.stTextInput > div > div > input {{
  border-radius: 9px !important; border-color: {BORDER} !important; font-size: 13px !important;
}}

/* ── Data table container ── */
.table-outer {{
  height: calc(100vh - 300px);
  min-height: 300px;
  overflow: hidden;
  border: 1px solid {BORDER};
  border-radius: 10px;
}}
[data-testid="stDataFrame"] {{
  border-radius: 10px;
  overflow: hidden;
}}
[data-testid="stDataFrame"] iframe {{ border-radius: 10px; }}

/* ── Streamlit buttons ── */
.stButton > button {{
  background: {NAVY} !important; color: #fff !important;
  border: none !important; border-radius: 9px !important;
  font-weight: 600 !important; font-size: 13px !important;
  padding: 9px 18px !important; transition: all .15s ease !important;
}}
.stButton > button:hover {{
  background: {NAVY_SOFT} !important; color: #fff !important;
}}

/* ── Chart container ── */
.chart-wrap {{
  background: {CARD}; border: 1px solid {BORDER}; border-radius: 12px;
  padding: 4px 4px 0;
  box-shadow: 0 1px 2px rgba(11,42,74,.04), 0 4px 16px rgba(11,42,74,.05);
}}
</style>
""", unsafe_allow_html=True)


# ─── DATA LAYER ──────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)

df = load_data()
ALL_MARKETS = ["UK", "US", "CA"]
TEA_TYPES   = sorted(df["tea_type"].unique().tolist())

def scope(market):
    if market == "All Markets":
        return df
    return df[df["market"] == market]


# ─── MOCK AI ENGINE ───────────────────────────────────────────────────────────
def generate_ai_response(question, market):
    q = question.lower()
    d = scope(market)
    mkt_label = market if market != "All Markets" else "all markets"

    chart = None
    if any(w in q for w in ["theme","barrier","reject","why","reason","taste"]):
        counts = d["theme"].value_counts().head(6)
        chart = ("bar", {"labels": counts.index.tolist(), "values": counts.values.tolist(),
                         "title": f"Top rejection themes — {mkt_label}"})
    elif any(w in q for w in ["persona","who","segment","audience"]):
        counts = d["persona"].value_counts()
        chart = ("bar", {"labels": counts.index.tolist(), "values": counts.values.tolist(),
                         "title": f"Persona distribution — {mkt_label}"})
    elif any(w in q for w in ["sentiment","feel","positive","negative"]):
        counts = d["sentiment"].value_counts()
        chart = ("bar", {"labels": counts.index.tolist(), "values": counts.values.tolist(),
                         "title": f"Sentiment split — {mkt_label}"})
    elif any(w in q for w in ["trend","over time","region","market","country"]):
        mc = d.groupby("market").size().reset_index(name="count")
        chart = ("bar", {"labels": mc["market"].tolist(), "values": mc["count"].tolist(),
                         "title": f"Responses by market — {mkt_label}"})

    top_theme     = d["theme"].value_counts().idxmax()
    top_theme_pct = round(d["theme"].value_counts(normalize=True).max() * 100)
    top_persona   = d["persona"].value_counts().idxmax()
    neg_pct       = round((d["sentiment"] == "Negative").mean() * 100)

    text = (
        f"<p><span class='src-chip'>V1</span> Across {mkt_label}, "
        f"<strong>{top_theme.lower()}</strong> is the leading barrier, appearing in "
        f"<strong>{top_theme_pct}%</strong> of responses. Overall sentiment is "
        f"<strong>{neg_pct}% negative</strong>, consistent with rejection-reason data.</p>"
        f"<p>The most prominent consumer group is the <strong>{top_persona}</strong>, "
        f"suggesting messaging and product cues should be tuned to that mindset.</p>"
        f"<p>This is an illustrative mock answer generated from the dataset. "
        f"Once connected to the live model, this section will return full natural-language "
        f"analysis grounded in the selected market's verbatims.</p>"
    )
    return {"text": text, "chart": chart}


def render_chart(chart):
    if not chart:
        return
    kind, p = chart
    colors = [NAVY, SAGE_DEEP, GOLD_DEEP, SAGE, GOLD, FAINT, "#9AA1AC"]
    if kind == "bar":
        vals = p["values"]
        labs = p["labels"]
        # horizontal if labels are long text
        if any(len(str(l)) > 8 for l in labs):
            fig = go.Figure(go.Bar(
                x=vals[::-1], y=labs[::-1], orientation="h",
                marker_color=NAVY,
                marker_line_width=0,
                text=[f"{v:,}" for v in vals[::-1]],
                textposition="auto",
                textfont=dict(size=11, color="#fff")))
            fig.update_layout(
                title=dict(text=p["title"], font=dict(color=NAVY, size=13, family="Inter")),
                height=280, margin=dict(l=8, r=8, t=44, b=8),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter", color=INK, size=11),
                yaxis=dict(tickfont=dict(size=11)),
                xaxis=dict(gridcolor=BORDER_SOFT, gridwidth=1))
        else:
            bar_colors = colors[:len(vals)]
            fig = go.Figure(go.Bar(
                x=labs, y=vals,
                marker_color=bar_colors,
                marker_line_width=0,
                text=[f"{v:,}" for v in vals],
                textposition="auto",
                textfont=dict(size=11, color="#fff")))
            fig.update_layout(
                title=dict(text=p["title"], font=dict(color=NAVY, size=13, family="Inter")),
                height=260, margin=dict(l=8, r=8, t=44, b=8),
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter", color=INK, size=11),
                yaxis=dict(gridcolor=BORDER_SOFT, gridwidth=1))
        st.plotly_chart(fig, use_container_width=True)
    elif kind == "pie":
        fig = go.Figure(go.Pie(
            labels=p["labels"], values=p["values"], hole=.52,
            marker=dict(colors=colors[:len(p["values"])]),
            textfont=dict(size=11)))
        fig.update_layout(
            title=dict(text=p["title"], font=dict(color=NAVY, size=13, family="Inter")),
            height=280, margin=dict(l=8, r=8, t=44, b=8),
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color=INK, size=11),
            legend=dict(font=dict(size=10)))
        st.plotly_chart(fig, use_container_width=True)


# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div class="brand">
      <div class="brand-mark">T</div>
      <div>
        <div class="brand-name">Tea<span>.</span>ai</div>
        <div class="brand-sub">Consumer Insights Workspace</div>
      </div>
    </div>""", unsafe_allow_html=True)

    n_resp = len(df)
    st.markdown(f"""
    <div class="about-card">
      <div class="about-label">About the Data</div>
      <div class="about-row">Open-ended consumer responses on tea rejection and preference,
      enriched with themes, sentiment, and personas.</div>
      <div class="about-row"><b>Source:</b> International consumer barrier survey</div>
      <div class="about-row"><b>Markets:</b> UK, US, Canada</div>
      <div class="about-row"><b>Tea categories:</b> {len(TEA_TYPES)}</div>
      <div class="about-row"><b>Responses:</b> {n_resp:,}</div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="nav-section-label">Navigate</div>', unsafe_allow_html=True)
    view = st.radio("nav", ["Executive Overview", "Data Preview", "Ask AI"],
                    index=2, label_visibility="collapsed")


# ─── VIEW: ASK AI ─────────────────────────────────────────────────────────────
def view_ask_ai():
    st.markdown("""
    <div class="page-header">
      <div class="page-title">Ask AI</div>
      <div class="page-sub">Ask questions about the consumer-insight dataset.
      Answers are scoped to the market you select.</div>
    </div>""", unsafe_allow_html=True)

    if "chat" not in st.session_state:
        st.session_state.chat = None

    c1, c2 = st.columns([1, 2.4])
    with c1:
        st.selectbox("Market", ["All Markets"] + ALL_MARKETS, index=0, key="ask_market")
    with c2:
        if st.session_state.chat:
            st.markdown("&nbsp;", unsafe_allow_html=True)
            st.markdown(f'<div style="text-align:right"><span class="prompt-chip">'
                        f'{st.session_state.chat["q"]}</span></div>', unsafe_allow_html=True)

    if st.session_state.chat:
        r = st.session_state.chat["resp"]
        st.markdown(f'<div class="resp-card"><h4>Tea.ai response</h4>{r["text"]}</div>',
                    unsafe_allow_html=True)
        if r["chart"]:
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            with st.container():
                render_chart(r["chart"])
    else:
        st.markdown(f"""
          <div class="resp-card" style="text-align:center;padding:46px 24px;color:{SOFT}">
            <div style="font-size:24px;margin-bottom:8px">🍵</div>
            <div style="font-weight:600;color:{SOFT};font-size:15px;margin-bottom:5px">Ask Tea.ai anything</div>
            <div style="font-size:13px">Try "Why do consumers reject green tea?" or "Who are the main personas?"</div>
          </div>""", unsafe_allow_html=True)

    q = st.chat_input("Ask queries here…")
    if q:
        resp = generate_ai_response(q, st.session_state.ask_market)
        st.session_state.chat = {"q": q, "resp": resp}
        st.rerun()


# ─── VIEW: DATA PREVIEW ───────────────────────────────────────────────────────
def view_data_preview():
    st.markdown("""
    <div class="page-header">
      <div class="page-title">Data Preview</div>
      <div class="page-sub">Inspect the raw consumer verbatims behind every AI answer.
      Filter, search, and verify.</div>
    </div>""", unsafe_allow_html=True)

    f1, f2, f3 = st.columns([1, 1.4, 1.6])
    with f1:
        m = st.selectbox("Market", ["All Markets"] + ALL_MARKETS, key="dp_market")
    with f2:
        t = st.selectbox("Tea type", ["All Tea Types"] + TEA_TYPES, key="dp_tea")
    with f3:
        s = st.text_input("Search verbatim", placeholder="words or phrases…", key="dp_search")

    d = df.copy()
    if m != "All Markets":  d = d[d["market"] == m]
    if t != "All Tea Types": d = d[d["tea_type"] == t]
    if s.strip():            d = d[d["verbatim"].str.contains(s.strip(), case=False, na=False)]

    st.markdown(
        f"<div style='font-size:12px;color:{SOFT};margin:8px 0 10px'>"
        f"Showing <b>{len(d):,}</b> of {len(df):,} responses</div>",
        unsafe_allow_html=True)

    show = d[["tea_type","market","response_no","verbatim","theme","sentiment","persona"]].rename(
        columns={"tea_type":"Tea Type","market":"Market","response_no":"#",
                 "verbatim":"Response Verbatim","theme":"Theme",
                 "sentiment":"Sentiment","persona":"Persona"})

    # table fills remaining height; headers are sticky via Streamlit's built-in
    tbl_height = 420
    st.dataframe(show, use_container_width=True, height=tbl_height,
                 hide_index=True,
                 column_config={
                     "#": st.column_config.NumberColumn(width="small"),
                     "Market": st.column_config.TextColumn(width="small"),
                     "Tea Type": st.column_config.TextColumn(width="medium"),
                     "Theme": st.column_config.TextColumn(width="medium"),
                     "Sentiment": st.column_config.TextColumn(width="small"),
                     "Persona": st.column_config.TextColumn(width="medium"),
                     "Response Verbatim": st.column_config.TextColumn(width="large"),
                 })


# ─── VIEW: EXECUTIVE OVERVIEW ─────────────────────────────────────────────────
def view_overview():
    st.markdown("""
    <div class="page-header">
      <div class="page-title">Executive Overview</div>
      <div class="page-sub">Leadership-level summary — who the consumers are,
      what drives rejection, and where the opportunities sit.</div>
    </div>""", unsafe_allow_html=True)

    # ── KPI cards ─────────────────────────────────────────────────
    total        = len(df)
    markets_n    = df["market"].nunique()
    neg_pct      = round((df["sentiment"] == "Negative").mean() * 100)
    top_barrier  = df["theme"].value_counts().idxmax()
    top_b_pct    = round(df["theme"].value_counts(normalize=True).max() * 100)
    top_persona  = df["persona"].value_counts().idxmax()
    tea_types_n  = df["tea_type"].nunique()

    st.markdown(f"""
    <div class="kpi-row">
      <div class="kpi-card kpi-accent">
        <div class="kpi-label">Total Responses</div>
        <div class="kpi-value">{total:,}</div>
        <div class="kpi-sub">{markets_n} markets · {tea_types_n} tea types</div>
      </div>
      <div class="kpi-card kpi-accent-red">
        <div class="kpi-label">Negative Sentiment</div>
        <div class="kpi-value">{neg_pct}%</div>
        <div class="kpi-sub delta-neg">Rejection-driven dataset</div>
      </div>
      <div class="kpi-card kpi-accent-gold">
        <div class="kpi-label">Top Barrier</div>
        <div class="kpi-value" style="font-size:15px;letter-spacing:-.2px">{top_barrier}</div>
        <div class="kpi-sub">{top_b_pct}% of responses</div>
      </div>
      <div class="kpi-card kpi-accent-sage">
        <div class="kpi-label">Dominant Persona</div>
        <div class="kpi-value" style="font-size:13px;letter-spacing:-.1px;line-height:1.2">{top_persona}</div>
        <div class="kpi-sub">Largest consumer segment</div>
      </div>
    </div>""", unsafe_allow_html=True)

    # ── Chart row 1: Themes + Sentiment + Market split ─────────────
    ch1, ch2, ch3 = st.columns(3)

    with ch1:
        tc = df["theme"].value_counts().head(7)
        colors_bar = [NAVY if i == 0 else SAGE_DEEP if i < 3 else FAINT
                      for i in range(len(tc))]
        fig = go.Figure(go.Bar(
            x=tc.values[::-1], y=tc.index.tolist()[::-1], orientation="h",
            marker_color=colors_bar[::-1], marker_line_width=0,
            text=[f"{v}" for v in tc.values[::-1]],
            textposition="auto",
            textfont=dict(size=10, color="#fff")))
        fig.update_layout(
            title=dict(text="Rejection Themes", font=dict(color=NAVY, size=13, family="Inter")),
            height=240, margin=dict(l=4, r=4, t=38, b=4),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", size=10, color=INK),
            xaxis=dict(gridcolor=BORDER_SOFT, gridwidth=1, tickfont=dict(size=9)),
            yaxis=dict(tickfont=dict(size=10)))
        st.plotly_chart(fig, use_container_width=True)

    with ch2:
        sc = df["sentiment"].value_counts()
        sent_colors = {
            "Negative": RED, "Neutral": GOLD_DEEP, "Positive": SAGE_DEEP
        }
        bar_colors = [sent_colors.get(l, FAINT) for l in sc.index]
        total_sent = sc.sum()
        pcts = [round(v / total_sent * 100) for v in sc.values]
        fig = go.Figure(go.Bar(
            x=sc.index.tolist(), y=sc.values.tolist(),
            marker_color=bar_colors, marker_line_width=0,
            text=[f"{p}%" for p in pcts],
            textposition="outside",
            textfont=dict(size=11, color=INK)))
        fig.update_layout(
            title=dict(text="Sentiment Distribution", font=dict(color=NAVY, size=13, family="Inter")),
            height=240, margin=dict(l=4, r=4, t=38, b=4),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", size=10, color=INK),
            yaxis=dict(gridcolor=BORDER_SOFT, gridwidth=1, tickfont=dict(size=9)),
            xaxis=dict(tickfont=dict(size=11)))
        st.plotly_chart(fig, use_container_width=True)

    with ch3:
        mc = df.groupby("market").size().reindex(ALL_MARKETS).fillna(0)
        fig = go.Figure(go.Bar(
            x=ALL_MARKETS, y=mc.values,
            marker_color=[NAVY, SAGE_DEEP, GOLD_DEEP],
            marker_line_width=0,
            text=[f"{int(v):,}" for v in mc.values],
            textposition="outside",
            textfont=dict(size=11, color=INK)))
        fig.update_layout(
            title=dict(text="Responses by Market", font=dict(color=NAVY, size=13, family="Inter")),
            height=240, margin=dict(l=4, r=4, t=38, b=4),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", size=10, color=INK),
            yaxis=dict(gridcolor=BORDER_SOFT, gridwidth=1, tickfont=dict(size=9)),
            xaxis=dict(tickfont=dict(size=13, color=INK)))
        st.plotly_chart(fig, use_container_width=True)

    # ── Chart row 2: Persona breakdown + Tea type volume ──────────
    ch4, ch5 = st.columns([1.1, 1])

    with ch4:
        pc = df["persona"].value_counts()
        persona_colors = [NAVY, SAGE_DEEP, GOLD_DEEP, SAGE, GOLD, FAINT][:len(pc)]
        total_p = pc.sum()
        pcts_p  = [round(v / total_p * 100) for v in pc.values]
        fig = go.Figure(go.Bar(
            x=pc.values[::-1], y=pc.index.tolist()[::-1], orientation="h",
            marker_color=persona_colors[::-1], marker_line_width=0,
            text=[f"{p}%" for p in pcts_p[::-1]],
            textposition="auto",
            textfont=dict(size=10, color="#fff")))
        fig.update_layout(
            title=dict(text="Consumer Persona Breakdown", font=dict(color=NAVY, size=13, family="Inter")),
            height=200, margin=dict(l=4, r=4, t=38, b=4),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", size=10, color=INK),
            xaxis=dict(gridcolor=BORDER_SOFT, gridwidth=1, tickfont=dict(size=9)),
            yaxis=dict(tickfont=dict(size=10)))
        st.plotly_chart(fig, use_container_width=True)

    with ch5:
        ttc = df["tea_type"].value_counts().head(8)
        fig = go.Figure(go.Bar(
            x=ttc.values[::-1], y=ttc.index.tolist()[::-1], orientation="h",
            marker_color=SAGE_DEEP, marker_line_width=0,
            text=ttc.values[::-1], textposition="auto",
            textfont=dict(size=10, color="#fff")))
        fig.update_layout(
            title=dict(text="Top Tea Categories by Volume", font=dict(color=NAVY, size=13, family="Inter")),
            height=200, margin=dict(l=4, r=4, t=38, b=4),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", size=10, color=INK),
            xaxis=dict(gridcolor=BORDER_SOFT, gridwidth=1, tickfont=dict(size=9)),
            yaxis=dict(tickfont=dict(size=10)))
        st.plotly_chart(fig, use_container_width=True)

    # ── Market summary panel ───────────────────────────────────────
    st.markdown('<div class="card"><div class="card-title">Market Summary</div>'
                '<div class="card-sub">Data-derived executive read for the selected cut</div>',
                unsafe_allow_html=True)
    ms1, ms2 = st.columns([1, 1.3])
    with ms1:
        sm  = st.selectbox("Market", ["All Markets"] + ALL_MARKETS, key="ov_sum_market")
        stt = st.selectbox("Tea type", ["All Tea Types"] + TEA_TYPES, key="ov_sum_tea")
    with ms2:
        d2 = scope(sm)
        if stt != "All Tea Types": d2 = d2[d2["tea_type"] == stt]
        if len(d2) == 0:
            st.info("No responses for this combination.")
        else:
            tt    = d2["theme"].value_counts().idxmax()
            tp    = d2["persona"].value_counts().idxmax()
            neg2  = round((d2["sentiment"] == "Negative").mean() * 100)
            pos2  = round((d2["sentiment"] == "Positive").mean() * 100)
            label = stt if stt != "All Tea Types" else "tea overall"
            mkt   = sm  if sm  != "All Markets"  else "across markets"
            st.markdown(f"""
            <div class="summary-box">
              <p><strong>{label}</strong> {mkt} faces its strongest barrier in
              <strong>{tt.lower()}</strong>, the most-cited rejection driver.</p>
              <p>Sentiment runs <strong>{neg2}% negative</strong> / {pos2}% positive,
              and the dominant consumer group is the <strong>{tp}</strong>.</p>
              <p>Growth potential is strongest where the barrier is education- or
              perception-led rather than fundamental — a candidate for targeted activation.</p>
            </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ─── ROUTER ───────────────────────────────────────────────────────────────────
if view == "Ask AI":
    view_ask_ai()
elif view == "Data Preview":
    view_data_preview()
else:
    view_overview()

