"""
Validation Intelligence Platform - 1000 Companies
Dark editorial UI - correct column names from validation_final.py schema
"""

import streamlit as st
import sqlite3
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="Company Intelligence — Validation",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');
    * { font-family: 'DM Sans', sans-serif !important; }
    .stApp { background: #080b10; }
    .block-container { background: #0d1117; border-radius: 0px; padding: 2.5rem 3rem; border-left: 1px solid rgba(56,189,248,0.08); max-width: 1400px; }
    [data-testid="stSidebar"] { background: #080b10; border-right: 1px solid rgba(56,189,248,0.08); }
    [data-testid="stSidebar"] * { color: #94a3b8 !important; }
    h1 { font-family: 'Syne', sans-serif !important; font-weight: 800 !important; font-size: 3rem !important; color: #f1f5f9 !important; letter-spacing: -0.04em !important; }
    h2 { font-family: 'Syne', sans-serif !important; font-weight: 700 !important; font-size: 1.6rem !important; color: #e2e8f0 !important; margin-top: 2rem !important; }
    h3 { font-family: 'Syne', sans-serif !important; font-weight: 600 !important; color: #cbd5e1 !important; font-size: 1rem !important; text-transform: uppercase !important; letter-spacing: 0.05em !important; }
    p, .stMarkdown p { color: #94a3b8 !important; line-height: 1.7 !important; }
    div[data-testid="metric-container"] { background: #111827; border-radius: 16px; padding: 1.5rem; border: 1px solid rgba(56,189,248,0.1); transition: all 0.3s ease; }
    div[data-testid="metric-container"]:hover { border-color: rgba(56,189,248,0.3); transform: translateY(-3px); box-shadow: 0 8px 24px rgba(56,189,248,0.08); }
    [data-testid="stMetricValue"] { font-family: 'Syne', sans-serif !important; font-size: 2.6rem !important; font-weight: 800 !important; color: #38bdf8 !important; }
    [data-testid="stMetricLabel"] { font-size: 0.75rem !important; font-weight: 600 !important; text-transform: uppercase !important; letter-spacing: 0.1em !important; color: #64748b !important; }
    .stButton > button { background: transparent; color: #38bdf8 !important; border: 1.5px solid rgba(56,189,248,0.4); border-radius: 8px; padding: 0.6rem 1.8rem; font-weight: 600; font-size: 0.85rem; letter-spacing: 0.08em; text-transform: uppercase; transition: all 0.25s ease; }
    .stButton > button:hover { background: rgba(56,189,248,0.08); border-color: #38bdf8; }
    [data-testid="stSidebar"] .stRadio > label { background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.04); border-radius: 10px; padding: 0.75rem 1rem; margin: 0.3rem 0; transition: all 0.25s ease; cursor: pointer; }
    [data-testid="stSidebar"] .stRadio > label:hover { background: rgba(56,189,248,0.06); border-color: rgba(56,189,248,0.2); transform: translateX(4px); }
    .stSelectbox > div > div, .stTextInput > div > div > input { background: #111827 !important; border: 1.5px solid rgba(56,189,248,0.15) !important; border-radius: 10px !important; color: #e2e8f0 !important; }
    .stTabs [data-baseweb="tab-list"] { background: #111827; border-radius: 12px; padding: 0.4rem; gap: 6px; border: 1px solid rgba(56,189,248,0.08); }
    .stTabs [data-baseweb="tab"] { border-radius: 8px; padding: 0.6rem 1.5rem; font-weight: 600; font-size: 0.85rem; color: #64748b; background: transparent; border: none; transition: all 0.25s ease; }
    .stTabs [data-baseweb="tab"][aria-selected="true"] { background: rgba(56,189,248,0.12) !important; color: #38bdf8 !important; }
    [data-testid="stDataFrame"] { border-radius: 12px; border: 1px solid rgba(56,189,248,0.1); overflow: hidden; }
    hr { border: none; height: 1px; background: linear-gradient(90deg, transparent 0%, rgba(56,189,248,0.2) 50%, transparent 100%); margin: 2.5rem 0; }
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #080b10; }
    ::-webkit-scrollbar-thumb { background: #1e293b; border-radius: 6px; }
    ::-webkit-scrollbar-thumb:hover { background: #38bdf8; }
    .js-plotly-plot { border-radius: 16px !important; border: 1px solid rgba(56,189,248,0.08) !important; }
    footer { visibility: hidden; }
    #MainMenu { visibility: hidden; }
    .badge { display: inline-block; background: rgba(56,189,248,0.1); color: #38bdf8; border: 1px solid rgba(56,189,248,0.2); border-radius: 20px; padding: 0.2rem 0.8rem; font-size: 0.75rem; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 1rem; }
    .accent-line { width: 60px; height: 4px; background: linear-gradient(90deg, #38bdf8, #818cf8); border-radius: 2px; margin-bottom: 1.5rem; }
</style>
""", unsafe_allow_html=True)

# ── Database ──────────────────────────────────────────────────────────────────
DB_PATH = "validation_intelligence.db"

@st.cache_data
def load_data():
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql("SELECT * FROM companies WHERE claude_status='done'", conn)
        conn.close()
        return df
    except Exception as e:
        return pd.DataFrame()

def get_options(df, col):
    if col not in df.columns:
        return []
    vals = df[col].dropna().unique().tolist()
    return sorted([v for v in vals if v not in ['Unknown', '']])

# ── Load ──────────────────────────────────────────────────────────────────────
with st.spinner("Loading..."):
    df = load_data()

if df.empty:
    st.error(f"No data found. Make sure '{DB_PATH}' is in the same folder.")
    st.stop()

# ── Safe column access ────────────────────────────────────────────────────────
def safe_count(df, col, val='Yes'):
    return (df[col] == val).sum() if col in df.columns else 0

hei_count  = safe_count(df, 'claude_hei_found')
k12_count  = safe_count(df, 'claude_hei_k12')
he_count   = safe_count(df, 'claude_hei_higher_ed')
corp_count = safe_count(df, 'claude_hei_corporate')

# ── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.markdown(f"""
<div style='padding: 1rem 0 0.5rem 0;'>
    <div style='font-family: Syne, sans-serif; font-size: 1.1rem; font-weight: 800; color: #38bdf8;'>Company Intelligence</div>
    <div style='font-size: 0.75rem; color: #475569; font-weight: 500; letter-spacing: 0.08em; text-transform: uppercase; margin-top: 0.2rem;'>Validation Dataset</div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
page = st.sidebar.radio("Navigation", ["🏠 Overview","🔎 Company Explorer","🎓 HEI Intelligence","📊 Analytics","🎯 Divergence"])
st.sidebar.markdown("---")
st.sidebar.markdown(f"""
<div style='padding: 0.5rem 0;'>
    <div style='font-size: 0.7rem; color: #475569; text-transform: uppercase; letter-spacing: 0.1em; font-weight: 600; margin-bottom: 0.8rem;'>Dataset</div>
    <div style='display:flex;justify-content:space-between;margin-bottom:0.5rem;'><span style='color:#64748b;font-size:0.85rem;'>Companies</span><span style='color:#38bdf8;font-weight:600;'>{len(df)}</span></div>
    <div style='display:flex;justify-content:space-between;margin-bottom:0.5rem;'><span style='color:#64748b;font-size:0.85rem;'>HEI Found</span><span style='color:#34d399;font-weight:600;'>{hei_count}</span></div>
    <div style='display:flex;justify-content:space-between;margin-bottom:0.5rem;'><span style='color:#64748b;font-size:0.85rem;'>K-12</span><span style='color:#a78bfa;font-weight:600;'>{k12_count}</span></div>
    <div style='display:flex;justify-content:space-between;'><span style='color:#64748b;font-size:0.85rem;'>Higher Ed</span><span style='color:#f472b6;font-weight:600;'>{he_count}</span></div>
</div>
""", unsafe_allow_html=True)
st.sidebar.markdown("---")
st.sidebar.markdown("<div style='font-size:0.7rem;color:#334155;text-transform:uppercase;letter-spacing:0.08em;'>MS Business Analytics<br>Worcester Polytechnic Institute</div>", unsafe_allow_html=True)

# ── PAGE 1: OVERVIEW ──────────────────────────────────────────────────────────
if page == "🏠 Overview":
    st.markdown('<div class="badge">Validation Dataset · 1000 Companies</div>', unsafe_allow_html=True)
    st.markdown('<div class="accent-line"></div>', unsafe_allow_html=True)
    st.title("Company Intelligence")
    st.markdown("**Dual-model enrichment pipeline** — Claude Sonnet · GPT-4o · Web Scraping")
    st.markdown("---")

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1: st.metric("Companies", len(df))
    with col2: st.metric("HEI Partnerships", hei_count, delta=f"{hei_count/len(df)*100:.1f}%")
    with col3: st.metric("K-12 Partners", k12_count)
    with col4: st.metric("Higher Ed", he_count)
    with col5: st.metric("Corporate Training", corp_count)

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Top Industries")
        top_ind = df['claude_industry'].value_counts().head(10)
        fig = go.Figure(go.Bar(
            x=top_ind.values[::-1], y=top_ind.index[::-1], orientation='h',
            marker=dict(color=top_ind.values[::-1], colorscale=[[0,'#1e3a5f'],[1,'#38bdf8']], showscale=False),
            text=top_ind.values[::-1], textposition='outside', textfont=dict(color='#64748b')
        ))
        fig.update_layout(plot_bgcolor='#111827', paper_bgcolor='#111827',
            xaxis=dict(showgrid=False, color='#475569'), yaxis=dict(color='#94a3b8', tickfont=dict(size=11)),
            margin=dict(l=0, r=40, t=10, b=10), height=380)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### B2B vs B2C")
        if 'claude_b2b_b2c' in df.columns:
            b2b = df[df['claude_b2b_b2c']!='Unknown']['claude_b2b_b2c'].value_counts()
            fig = go.Figure(go.Pie(labels=b2b.index, values=b2b.values, hole=0.6,
                marker=dict(colors=['#38bdf8','#818cf8','#34d399','#f472b6']),
                textfont=dict(color='#e2e8f0', size=13)))
            fig.update_layout(plot_bgcolor='#111827', paper_bgcolor='#111827',
                legend=dict(font=dict(color='#94a3b8'), bgcolor='#111827'),
                margin=dict(l=0, r=0, t=10, b=10), height=380)
            st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### HEI Confidence")
        if 'claude_hei_confidence_label' in df.columns:
            conf = df['claude_hei_confidence_label'].value_counts()
            colors = {'Very High':'#34d399','High':'#38bdf8','Medium':'#818cf8','Low':'#f59e0b','Very Low':'#475569'}
            fig = go.Figure(go.Bar(x=conf.index, y=conf.values,
                marker_color=[colors.get(i,'#475569') for i in conf.index],
                text=conf.values, textposition='outside', textfont=dict(color='#64748b')))
            fig.update_layout(plot_bgcolor='#111827', paper_bgcolor='#111827',
                xaxis=dict(color='#475569'), yaxis=dict(showgrid=False, color='#475569'),
                margin=dict(l=0, r=0, t=10, b=10), height=280)
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### HEI Categories")
        fig = go.Figure(go.Bar(
            x=['K-12','Higher Ed','Corporate'], y=[k12_count, he_count, corp_count],
            marker_color=['#a78bfa','#f472b6','#34d399'],
            text=[k12_count, he_count, corp_count], textposition='outside', textfont=dict(color='#64748b')))
        fig.update_layout(plot_bgcolor='#111827', paper_bgcolor='#111827',
            xaxis=dict(color='#475569'), yaxis=dict(showgrid=False, color='#475569'),
            margin=dict(l=0, r=0, t=10, b=10), height=280)
        st.plotly_chart(fig, use_container_width=True)

    with col3:
        st.markdown("### Model Agreement")
        agree = df['confidence_level'].value_counts()
        fig = go.Figure(go.Pie(labels=agree.index, values=agree.values, hole=0.5,
            marker=dict(colors=['#34d399','#38bdf8','#475569']), textfont=dict(color='#e2e8f0')))
        fig.update_layout(plot_bgcolor='#111827', paper_bgcolor='#111827',
            legend=dict(font=dict(color='#94a3b8'), bgcolor='#111827'),
            margin=dict(l=0, r=0, t=10, b=10), height=280)
        st.plotly_chart(fig, use_container_width=True)

# ── PAGE 2: COMPANY EXPLORER ──────────────────────────────────────────────────
elif page == "🔎 Company Explorer":
    st.markdown('<div class="badge">Filter & Search</div>', unsafe_allow_html=True)
    st.markdown('<div class="accent-line"></div>', unsafe_allow_html=True)
    st.title("Company Explorer")
    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)
    with col1: search = st.text_input("🔍 Search company", placeholder="e.g. Coursera...")
    with col2:
        industries = ['All'] + get_options(df, 'claude_industry')
        sel_ind = st.selectbox("Industry", industries)
    with col3: sel_hei = st.selectbox("HEI Found", ['All','Yes','No'])
    with col4: sel_b2b = st.selectbox("B2B/B2C", ['All']+get_options(df,'claude_b2b_b2c'))

    col1, col2, col3 = st.columns(3)
    with col1: sel_k12 = st.selectbox("K-12", ['All','Yes','No'])
    with col2: sel_he = st.selectbox("Higher Ed", ['All','Yes','No'])
    with col3: sel_corp = st.selectbox("Corporate Training", ['All','Yes','No'])

    filtered = df.copy()
    if search: filtered = filtered[filtered['company_name'].str.contains(search, case=False, na=False)]
    if sel_ind != 'All': filtered = filtered[filtered['claude_industry']==sel_ind]
    if sel_hei != 'All': filtered = filtered[filtered['claude_hei_found']==sel_hei]
    if sel_b2b != 'All' and 'claude_b2b_b2c' in filtered.columns: filtered = filtered[filtered['claude_b2b_b2c']==sel_b2b]
    if sel_k12 != 'All' and 'claude_hei_k12' in filtered.columns: filtered = filtered[filtered['claude_hei_k12']==sel_k12]
    if sel_he != 'All' and 'claude_hei_higher_ed' in filtered.columns: filtered = filtered[filtered['claude_hei_higher_ed']==sel_he]
    if sel_corp != 'All' and 'claude_hei_corporate' in filtered.columns: filtered = filtered[filtered['claude_hei_corporate']==sel_corp]

    st.markdown(f"**{len(filtered)} companies** match your filters")
    st.markdown("---")

    display_cols = ['company_name','claude_industry','claude_location','claude_b2b_b2c',
                    'claude_funding_stage','claude_company_size','claude_hei_found',
                    'claude_hei_k12','claude_hei_higher_ed','claude_hei_corporate',
                    'claude_hei_confidence_label','claude_hei_institutions','confidence_level']
    existing = [c for c in display_cols if c in filtered.columns]
    display_df = filtered[existing].rename(columns={
        'company_name':'Company','claude_industry':'Industry','claude_location':'Location',
        'claude_b2b_b2c':'B2B/B2C','claude_funding_stage':'Funding','claude_company_size':'Size',
        'claude_hei_found':'HEI Found','claude_hei_k12':'K-12','claude_hei_higher_ed':'Higher Ed',
        'claude_hei_corporate':'Corporate','claude_hei_confidence_label':'Confidence',
        'claude_hei_institutions':'Institutions','confidence_level':'Agreement'
    })
    st.dataframe(display_df, use_container_width=True, height=600)
    st.markdown("---")
    st.download_button("⬇ Export CSV", data=filtered.to_csv(index=False), file_name="filtered_companies.csv", mime="text/csv")

# ── PAGE 3: HEI INTELLIGENCE ──────────────────────────────────────────────────
elif page == "🎓 HEI Intelligence":
    st.markdown('<div class="badge">Educational Partnership Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="accent-line"></div>', unsafe_allow_html=True)
    st.title("HEI Intelligence")
    st.markdown("---")

    hei_cols = [c for c in ['company_name','claude_industry','claude_location',
                'claude_hei_confidence','claude_hei_confidence_label',
                'claude_hei_institutions','scraped_hei_found'] if c in df.columns]

    tab1, tab2, tab3, tab4 = st.tabs(["🏫 All HEI","📚 K-12","🎓 Higher Education","💼 Corporate Training"])

    with tab1:
        hei_df = df[df['claude_hei_found']=='Yes'][hei_cols]
        if 'claude_hei_confidence' in hei_df.columns:
            hei_df = hei_df.sort_values('claude_hei_confidence', ascending=False)
        st.markdown(f"**{len(hei_df)} companies** with confirmed HEI partnerships")
        st.dataframe(hei_df, use_container_width=True, height=500)

    with tab2:
        if 'claude_hei_k12' in df.columns:
            k12_df = df[df['claude_hei_k12']=='Yes'][hei_cols]
            st.markdown(f"**{len(k12_df)} companies** serving K-12")
            st.dataframe(k12_df, use_container_width=True, height=500)

    with tab3:
        if 'claude_hei_higher_ed' in df.columns:
            he_df = df[df['claude_hei_higher_ed']=='Yes'][hei_cols]
            st.markdown(f"**{len(he_df)} companies** serving universities")
            st.dataframe(he_df, use_container_width=True, height=500)

    with tab4:
        if 'claude_hei_corporate' in df.columns:
            corp_df = df[df['claude_hei_corporate']=='Yes'][hei_cols]
            st.markdown(f"**{len(corp_df)} companies** serving corporate L&D")
            st.dataframe(corp_df, use_container_width=True, height=500)

# ── PAGE 4: ANALYTICS ─────────────────────────────────────────────────────────
elif page == "📊 Analytics":
    st.markdown('<div class="badge">Business Intelligence</div>', unsafe_allow_html=True)
    st.markdown('<div class="accent-line"></div>', unsafe_allow_html=True)
    st.title("Analytics")
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### HEI Penetration by Industry")
        ind_stats = df.groupby('claude_industry').agg(
            total=('company_name','count'),
            hei=('claude_hei_found', lambda x: (x=='Yes').sum())
        ).reset_index()
        ind_stats['rate'] = (ind_stats['hei']/ind_stats['total']*100).round(1)
        ind_stats = ind_stats[ind_stats['total']>=3].sort_values('rate', ascending=False).head(15)
        fig = go.Figure(go.Bar(
            y=ind_stats['claude_industry'][::-1], x=ind_stats['rate'][::-1], orientation='h',
            marker=dict(color=ind_stats['rate'][::-1], colorscale=[[0,'#1e3a5f'],[1,'#38bdf8']], showscale=False),
            text=[f"{r}%" for r in ind_stats['rate'][::-1]], textposition='outside', textfont=dict(color='#64748b')))
        fig.update_layout(plot_bgcolor='#111827', paper_bgcolor='#111827',
            xaxis=dict(showgrid=False, color='#475569'), yaxis=dict(color='#94a3b8', tickfont=dict(size=11)),
            margin=dict(l=0, r=60, t=10, b=10), height=500)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### Funding Stage Distribution")
        funding = df[df['claude_funding_stage']!='Unknown']['claude_funding_stage'].value_counts()
        fig = go.Figure(go.Bar(x=funding.index, y=funding.values,
            marker=dict(color=funding.values, colorscale=[[0,'#1e1b4b'],[1,'#818cf8']], showscale=False),
            text=funding.values, textposition='outside', textfont=dict(color='#64748b')))
        fig.update_layout(plot_bgcolor='#111827', paper_bgcolor='#111827',
            xaxis=dict(color='#475569'), yaxis=dict(showgrid=False, color='#475569'),
            margin=dict(l=0, r=0, t=10, b=10), height=500)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Geographic Distribution")
        def get_country(loc):
            if pd.isna(loc) or loc=='Unknown': return 'Unknown'
            parts = str(loc).split(',')
            return parts[-1].strip() if len(parts)>=2 else str(loc)
        df2 = df.copy()
        df2['country'] = df2['claude_location'].apply(get_country)
        geo = df2[df2['country']!='Unknown']['country'].value_counts().head(10)
        fig = go.Figure(go.Pie(labels=geo.index, values=geo.values, hole=0.5,
            marker=dict(colors=['#38bdf8','#818cf8','#34d399','#f472b6','#f59e0b','#06b6d4','#a78bfa','#fb7185','#4ade80','#fbbf24']),
            textfont=dict(color='#e2e8f0', size=12)))
        fig.update_layout(plot_bgcolor='#111827', paper_bgcolor='#111827',
            legend=dict(font=dict(color='#94a3b8'), bgcolor='#111827'),
            margin=dict(l=0, r=0, t=10, b=10), height=380)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### Company Size Distribution")
        size_order = ['1-10','11-50','51-200','201-500','500+']
        size_data = df[df['claude_company_size'].isin(size_order)]['claude_company_size'].value_counts().reindex(size_order).dropna()
        fig = go.Figure(go.Bar(x=size_data.index, y=size_data.values,
            marker=dict(color=size_data.values, colorscale=[[0,'#164e63'],[1,'#34d399']], showscale=False),
            text=size_data.values, textposition='outside', textfont=dict(color='#64748b')))
        fig.update_layout(plot_bgcolor='#111827', paper_bgcolor='#111827',
            xaxis=dict(color='#475569'), yaxis=dict(showgrid=False, color='#475569'),
            margin=dict(l=0, r=0, t=10, b=10), height=380)
        st.plotly_chart(fig, use_container_width=True)

# ── PAGE 5: DIVERGENCE ────────────────────────────────────────────────────────
elif page == "🎯 Divergence":
    st.markdown('<div class="badge">Outlier & Anomaly Detection</div>', unsafe_allow_html=True)
    st.markdown('<div class="accent-line"></div>', unsafe_allow_html=True)
    st.title("Divergence Analysis")
    st.markdown("---")

    def get_size_num(s):
        return {"1-10":5,"11-50":30,"51-200":125,"201-500":350,"500+":750}.get(s)
    def get_fund_num(s):
        return {"Bootstrapped":0,"Seed":1,"Series A":2,"Series B":3,"Series C":4,"Public":5}.get(s)

    df3 = df.copy()
    df3['size_num'] = df3['claude_company_size'].apply(get_size_num)
    df3['fund_num'] = df3['claude_funding_stage'].apply(get_fund_num)

    tab1, tab2, tab3 = st.tabs(["💰 Funding Anomalies","🎓 HEI Divergence","🗺️ Geographic Outliers"])

    with tab1:
        anomalies = []
        for _, row in df3.iterrows():
            s, f = row['size_num'], row['fund_num']
            if pd.isna(s) or pd.isna(f): continue
            if s<=30 and f>=3:
                anomalies.append({'Company':row['company_name'],'Industry':row['claude_industry'],'Size':row['claude_company_size'],'Funding':row['claude_funding_stage'],'Pattern':'🔴 Late-stage funding, small team'})
            elif s>=350 and f<=1:
                anomalies.append({'Company':row['company_name'],'Industry':row['claude_industry'],'Size':row['claude_company_size'],'Funding':row['claude_funding_stage'],'Pattern':'🟡 Large team, minimal funding'})
        if anomalies:
            adf = pd.DataFrame(anomalies)
            st.markdown(f"**{len(adf)} companies** with unusual patterns")
            st.dataframe(adf, use_container_width=True, height=500)
        else:
            st.info("No funding anomalies detected")

    with tab2:
        ind_hei = df3.groupby('claude_industry').apply(
            lambda x: (x['claude_hei_found']=='Yes').sum()/len(x)*100 if len(x)>0 else 0).to_dict()
        hei_div = []
        for _, row in df3.iterrows():
            ind = row['claude_industry']
            rate = ind_hei.get(ind, 0)
            has = row['claude_hei_found']=='Yes'
            if has and rate<20:
                hei_div.append({'Company':row['company_name'],'Industry':ind,'HEI Found':'Yes','Industry Avg':f"{rate:.0f}%",'Pattern':'🟢 HEI leader in non-traditional sector'})
            elif not has and rate>60:
                hei_div.append({'Company':row['company_name'],'Industry':ind,'HEI Found':'No','Industry Avg':f"{rate:.0f}%",'Pattern':'🔴 Missing partnerships common in sector'})
        if hei_div:
            hdf = pd.DataFrame(hei_div)
            st.markdown(f"**{len(hdf)} companies** with divergent HEI patterns")
            st.dataframe(hdf, use_container_width=True, height=500)
        else:
            st.info("No significant HEI divergence detected")

    with tab3:
        def get_country(loc):
            if pd.isna(loc) or loc=='Unknown': return 'Unknown'
            parts = str(loc).split(',')
            return parts[-1].strip() if len(parts)>=2 else str(loc)
        df3['country'] = df3['claude_location'].apply(get_country)
        geo_outliers = []
        for ind in df3['claude_industry'].value_counts().head(20).index:
            idf = df3[df3['claude_industry']==ind]
            if len(idf)<5: continue
            top = idf['country'].value_counts()
            if len(top)>0:
                pct = top.iloc[0]/len(idf)*100
                if pct>70:
                    geo_outliers.append({'Industry':ind,'Dominant Country':top.index[0],'Concentration':f"{pct:.0f}%",'Total Companies':len(idf)})
        if geo_outliers:
            gdf = pd.DataFrame(geo_outliers).sort_values('Concentration', ascending=False)
            st.markdown(f"**{len(gdf)} industries** with strong geographic concentration")
            st.dataframe(gdf, use_container_width=True, height=400)
        else:
            st.info("No geographic concentration found")