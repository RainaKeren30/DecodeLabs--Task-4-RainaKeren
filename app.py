import sys, os
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
import plotly.graph_objects as go
import pandas as pd

from data.roles_skills import ROLES_DATA, EXPERIENCE_MULTIPLIERS
from utils.nlp_engine import (
    parse_skills_input,
    weighted_match_score,
    compute_readiness_score,
    generate_learning_roadmap,
    estimate_timeline,
    radar_chart_data,
)
from utils.report import generate_text_report

st.set_page_config(
    page_title="SkillSync AI",
    layout="wide",
    initial_sidebar_state="collapsed",
)

C = {
    "primary":     "#102B53",
    "secondary":   "#50698D",
    "accent":      "#CEB5D4",
    "interactive": "#4E7AB1",
    "soft":        "#7D9FC0",
    "success":     "#2d7a4f",
    "error":       "#d45a30",
}

if "page"       not in st.session_state: st.session_state.page       = "home"
if "results"    not in st.session_state: st.session_state.results    = None
if "errors"     not in st.session_state: st.session_state.errors     = {}
if "submitted"  not in st.session_state: st.session_state.submitted  = False

TEXT  = "#ffffff"
TSUB  = "rgba(255,255,255,0.62)"
CARD  = "rgba(255,255,255,0.09)"
CBORD = "rgba(255,255,255,0.16)"
BG    = "linear-gradient(145deg,#102B53 0%,#1A3D6B 22%,#2356A0 46%,#6B90B8 70%,#CEB5D4 100%)"

# ─── CSS ──────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Inter:wght@300;400;500;600;700&display=swap');

#MainMenu,footer,header{{visibility:hidden;}}
[data-testid="stToolbar"]{{display:none;}}
[data-testid="collapsedControl"]{{display:none;}}
[data-testid="stSidebar"]{{display:none;}}
.block-container{{padding:0!important;max-width:100%!important;}}
[data-testid="stAppViewContainer"]{{background:{BG};min-height:100vh;}}
[data-testid="stAppViewBlockContainer"]{{padding:0!important;}}

*{{font-family:'Inter',sans-serif;box-sizing:border-box;}}
h1,h2,h3{{font-family:'Playfair Display',serif;}}

::-webkit-scrollbar{{width:5px;}}
::-webkit-scrollbar-track{{background:transparent;}}
::-webkit-scrollbar-thumb{{background:rgba(206,181,212,0.3);border-radius:3px;}}

[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea{{
    background:rgba(255,255,255,0.1)!important;
    border:1px solid rgba(255,255,255,0.22)!important;
    border-radius:10px!important;
    color:#fff!important;
    font-family:'Inter',sans-serif!important;
    font-size:13px!important;
    transition:border-color .2s,box-shadow .2s!important;
}}
[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus{{
    border-color:rgba(206,181,212,0.7)!important;
    box-shadow:0 0 0 3px rgba(206,181,212,0.15)!important;
}}
[data-testid="stTextInput"] input::placeholder,
[data-testid="stTextArea"] textarea::placeholder{{color:rgba(255,255,255,0.32)!important;}}
[data-testid="stTextInput"] label,
[data-testid="stTextArea"] label,
[data-testid="stSelectbox"] label,
div[data-testid="stMarkdownContainer"] p{{color:#fff!important;}}

div[data-baseweb="select"]>div{{
    background:rgba(255,255,255,0.1)!important;
    border:1px solid rgba(255,255,255,0.22)!important;
    border-radius:10px!important;
    color:#fff!important;
    transition:border-color .2s!important;
}}
div[data-baseweb="select"]>div:focus-within{{
    border-color:rgba(206,181,212,0.7)!important;
    box-shadow:0 0 0 3px rgba(206,181,212,0.15)!important;
}}
li[role="option"]{{color:#102B53!important;background:#fff!important;}}

[data-testid="stButton"]>button{{
    font-family:'Inter',sans-serif!important;
    font-weight:600!important;
    border-radius:10px!important;
    transition:all .22s ease!important;
    color:#fff!important;
    border:0.5px solid rgba(255,255,255,0.28)!important;
    background:rgba(255,255,255,0.1)!important;
}}
[data-testid="stButton"]>button:hover{{
    background:rgba(255,255,255,0.18)!important;
    transform:translateY(-1px)!important;
    box-shadow:0 8px 24px rgba(16,43,83,0.4)!important;
}}
[data-testid="stButton"]>button:active{{transform:translateY(0)!important;}}

[data-testid="stDownloadButton"]>button{{
    background:linear-gradient(135deg,#102B53,#4E7AB1)!important;
    color:#fff!important;border:none!important;
    border-radius:10px!important;font-weight:600!important;
    font-family:'Inter',sans-serif!important;
    padding:0.65rem 1.5rem!important;
    transition:all .22s!important;
}}
[data-testid="stDownloadButton"]>button:hover{{
    transform:translateY(-2px)!important;
    box-shadow:0 10px 28px rgba(16,43,83,0.5)!important;
}}

[data-testid="column"]{{padding:0.2rem!important;}}
[data-testid="stPlotlyChart"]{{border-radius:14px!important;overflow:hidden;}}

.err-input-border div[data-baseweb="select"]>div{{
    border-color:rgba(212,90,48,0.8)!important;
    box-shadow:0 0 0 3px rgba(212,90,48,0.18)!important;
}}
</style>
""", unsafe_allow_html=True)

# ─── 3D Transition JS (injected once) ─────────────────────────────────────────
st.markdown("""
<style>
.page-wrap{
    perspective:1200px;
    transform-style:preserve-3d;
}
.slide-in{
    animation:slideIn3D .52s cubic-bezier(.77,0,.175,1) both;
}
.slide-out{
    animation:slideOut3D .52s cubic-bezier(.77,0,.175,1) both;
}
@keyframes slideIn3D{
    from{opacity:0;transform:rotateY(-18deg) translateX(60px) scale(0.96);}
    to{opacity:1;transform:rotateY(0deg) translateX(0) scale(1);}
}
@keyframes slideOut3D{
    from{opacity:1;transform:rotateY(0deg) translateX(0) scale(1);}
    to{opacity:0;transform:rotateY(18deg) translateX(-60px) scale(0.96);}
}
@keyframes fadeUp{
    from{opacity:0;transform:translateY(10px);}
    to{opacity:1;transform:translateY(0);}
}
@keyframes errShake{
    0%,100%{transform:translateX(0);}
    20%{transform:translateX(-6px);}
    40%{transform:translateX(6px);}
    60%{transform:translateX(-4px);}
    80%{transform:translateX(4px);}
}
@keyframes countUp{
    from{opacity:0;transform:translateY(8px);}
    to{opacity:1;transform:translateY(0);}
}
.fade-up{animation:fadeUp .4s ease both;}
.err-shake{animation:errShake .38s ease;}
.count-anim{animation:countUp .35s ease both;}

.metric-card{
    background:rgba(255,255,255,0.09);
    border:0.5px solid rgba(255,255,255,0.16);
    border-radius:14px;
    padding:13px 15px;
    backdrop-filter:blur(12px);
    transition:transform .2s,background .2s;
}
.metric-card:hover{
    transform:translateY(-2px);
    background:rgba(255,255,255,0.13);
}
.metric-lbl{
    font-size:10px;font-weight:700;letter-spacing:.12em;
    text-transform:uppercase;color:rgba(255,255,255,0.5);margin-bottom:3px;
}
.metric-val{
    font-family:'Playfair Display',serif;
    font-size:26px;font-weight:700;line-height:1;margin-bottom:2px;
}
.metric-sub{font-size:11px;color:rgba(255,255,255,0.48);}

.glass-card{
    background:rgba(255,255,255,0.09);
    border:0.5px solid rgba(255,255,255,0.16);
    border-radius:16px;padding:14px 17px;
    backdrop-filter:blur(14px);
    transition:border-color .2s;
}
.glass-card:focus-within{border-color:rgba(206,181,212,0.5);}

.section-label{
    font-size:10px;font-weight:700;letter-spacing:.14em;
    text-transform:uppercase;color:rgba(255,255,255,0.5);margin-bottom:4px;
}
.section-title{
    font-family:'Playfair Display',serif;
    font-size:14.5px;color:#fff;font-weight:600;margin-bottom:10px;
}
.field-label{
    font-size:11.5px;color:rgba(255,255,255,0.62);
    font-weight:500;margin-bottom:3px;margin-top:8px;
    display:flex;align-items:center;gap:4px;
}
.required-star{color:#f5a97f;font-size:13px;}

.err-msg{
    font-size:11px;color:#f5a97f;margin-top:3px;
    font-weight:600;display:flex;align-items:center;gap:5px;
}
.err-banner{
    background:rgba(212,90,48,0.15);
    border:0.5px solid rgba(212,90,48,0.5);
    border-radius:11px;padding:11px 15px;
    display:flex;align-items:center;gap:10px;
    animation:fadeUp .3s ease;
    margin-bottom:10px;
}
.err-banner-txt{color:#f5a97f;font-weight:600;font-size:12.5px;}

.skill-row{
    display:flex;align-items:center;justify-content:space-between;
    padding:8px 11px;border-radius:0 9px 9px 0;
    margin-bottom:5px;transition:transform .15s;
}
.skill-row:hover{transform:translateX(3px);}
.skill-name{font-size:12.5px;font-weight:500;color:#fff;}
.priority-pill{
    font-size:9px;font-weight:700;letter-spacing:.07em;
    text-transform:uppercase;padding:2px 8px;
    border-radius:20px;color:#fff;flex-shrink:0;margin-left:7px;
}

.bar-row{margin-bottom:7px;}
.bar-label-row{display:flex;justify-content:space-between;font-size:11px;margin-bottom:3px;}
.bar-track{background:rgba(255,255,255,0.08);border-radius:4px;height:6px;overflow:hidden;}
.bar-fill{height:6px;border-radius:4px;transition:width .7s cubic-bezier(.22,1,.36,1);}

.roadmap-card{
    background:rgba(255,255,255,0.08);
    border:0.5px solid rgba(255,255,255,0.13);
    border-radius:12px;padding:12px 14px;
    border-left-width:3px;border-left-style:solid;
    margin-bottom:8px;
    transition:transform .2s,background .2s;
    animation:fadeUp .4s ease both;
}
.roadmap-card:hover{transform:translateY(-2px);background:rgba(255,255,255,0.12);}
.roadmap-skill{
    font-family:'Playfair Display',serif;
    font-size:13.5px;color:#fff;font-weight:600;
}
.roadmap-res{font-size:11px;color:rgba(255,255,255,0.56);line-height:1.5;margin:4px 0;}
.roadmap-dur{font-size:11px;color:rgba(255,255,255,0.48);}
.roadmap-dur strong{color:#fff;font-weight:600;}

.analyst-box{
    border-radius:13px;padding:15px 18px;
    margin-bottom:12px;transition:all .4s;
    animation:fadeUp .5s ease both;
}
.analyst-lbl{
    font-size:9.5px;font-weight:700;letter-spacing:.14em;
    text-transform:uppercase;margin-bottom:7px;
}
.analyst-p{font-size:12.5px;line-height:1.78;margin-bottom:7px;}

.nav-bar{
    display:flex;align-items:center;justify-content:space-between;
    padding:11px 24px;
    background:rgba(16,43,83,0.55);
    border-bottom:0.5px solid rgba(255,255,255,0.1);
    backdrop-filter:blur(16px);
}
.nav-brand{
    font-size:11px;font-weight:700;letter-spacing:.16em;
    text-transform:uppercase;color:#CEB5D4;
}
</style>
""", unsafe_allow_html=True)


# ─── Helpers ──────────────────────────────────────────────────────────────────
def glass_card(html, pad="14px 17px", mb="10px", extra=""):
    st.markdown(f"""
    <div class="glass-card fade-up" style="padding:{pad};margin-bottom:{mb};{extra}">
        {html}
    </div>""", unsafe_allow_html=True)

def metric_card(label, value, sub, color):
    st.markdown(f"""
    <div class="metric-card fade-up">
        <div class="metric-lbl">{label}</div>
        <div class="metric-val count-anim" style="color:{color};">{value}</div>
        <div class="metric-sub">{sub}</div>
    </div>""", unsafe_allow_html=True)

def plotly_base():
    return dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#fff"),
        margin=dict(l=18,r=18,t=24,b=18)
    )

def error_banner(msg):
    st.markdown(f"""
    <div class="err-banner err-shake">
        <span style="font-size:18px;color:#f5a97f;">⚠</span>
        <span class="err-banner-txt">{msg}</span>
    </div>""", unsafe_allow_html=True)

def field_err(msg):
    st.markdown(f"""
    <div class="err-msg">
        <span>⚠</span><span>{msg}</span>
    </div>""", unsafe_allow_html=True)

def describe_gap(ms, rLabel, strengths, missing, role, experience, timeline, role_data):
    weights = role_data.get("weights", {})
    if ms >= 80:
        opener = f"Your profile aligns strongly with the {role} role. You cover most of what hiring teams actively screen for, putting you in a competitive position immediately."
    elif ms >= 60:
        opener = f"You have a meaningful foundation for {role}. Several high-value skills are already in place — targeted effort on the remaining gaps will move you into job-ready range."
    elif ms >= 40:
        opener = f"You are at an early-to-mid stage for {role}. The gap is real but bridgeable — prioritizing the highest-weight missing skills will have the greatest impact on your readiness."
    else:
        opener = f"The {role} role requires a broad technical foundation. Your current skills cover a smaller portion of that requirement — this is a longer runway but achievable with structured effort."

    st_note = ""
    if strengths:
        top = ", ".join(s.title() for s in strengths[:3])
        st_note = f"Your strongest assets — {top} — are genuinely high-value in this role and give you a real starting point beyond surface familiarity."

    if missing:
        crit = ", ".join(s.title() for s in missing[:3])
        gap_note = f"The most critical gaps are {crit}. These carry the highest weight in {role} requirements and appear consistently across job postings. Closing these first delivers outsized improvement to your match score."
    else:
        gap_note = "No major skill gaps detected — your profile is well-aligned with this role."

    exp_short = experience.split("(")[0].strip()
    tl_note = f"Based on your experience level ({exp_short}) and gaps identified, a realistic timeline is {timeline} at 8–10 hours of study per week. Prioritize Critical and High items in the roadmap before anything else."

    stance = "strong" if ms >= 80 else "progressing" if ms >= 60 else "early" if ms >= 40 else "foundational"
    return {"opener": opener, "st_note": st_note, "gap_note": gap_note, "tl_note": tl_note, "stance": stance}


# ════════════════════════════════════════════════════════════════════════════════
# HOME PAGE
# ════════════════════════════════════════════════════════════════════════════════
def render_home():
    st.markdown(f"""
    <div class="nav-bar">
        <div class="nav-brand">SkillSync AI</div>
    </div>
    <div class="page-wrap">
    <div class="slide-in" style="padding:46px 26px 30px;text-align:center;max-width:780px;margin:0 auto;">
        <p style="font-size:10px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:#CEB5D4;margin-bottom:12px;">
            Career Intelligence Platform
        </p>
        <h1 style="font-family:'Playfair Display',serif;font-size:clamp(2.1rem,5vw,3.6rem);
                   font-weight:700;color:#fff;line-height:1.17;margin-bottom:13px;
                   text-shadow:0 2px 20px rgba(16,43,83,0.5);">
            Know exactly where<br>you stand — and<br>where to go next.
        </h1>
        <p style="font-size:14px;color:rgba(255,255,255,0.68);line-height:1.82;
                  max-width:460px;margin:0 auto 28px;">
            SkillSync AI maps your skills against any target role, identifies what matters,
            and delivers a clear path to close the gap — powered by NLP.
        </p>
    </div>
    </div>""", unsafe_allow_html=True)

    b1, b2, b3 = st.columns([2.5, 1.4, 2.5])
    with b2:
        if st.button("Analyze My Skills", key="go_an", use_container_width=True):
            st.session_state.page = "analyzer"
            st.session_state.errors = {}
            st.session_state.submitted = False
            st.rerun()
    st.markdown("""
    <style>
    section[data-testid="stVerticalBlock"] > div:nth-child(2) [data-testid="stButton"]>button{
        background:linear-gradient(135deg,rgba(255,255,255,0.18),rgba(255,255,255,0.06))!important;
        border:0.5px solid rgba(255,255,255,0.38)!important;
        color:#fff!important;padding:0.88rem 0.4rem!important;
        font-size:14.5px!important;
        box-shadow:0 8px 28px rgba(16,43,83,0.38)!important;
    }
    </style>""", unsafe_allow_html=True)

    st.markdown("<div style='padding:0 24px;max-width:1100px;margin:0 auto;'>", unsafe_allow_html=True)
    fc = st.columns(4, gap="small")
    feats = [
        ("NLP Engine",       "TF-IDF and cosine similarity score your alignment with real role requirements."),
        ("Weighted Scoring", "Importance-weighted match reflecting what roles genuinely prioritize."),
        ("Gap Roadmap",      "Prioritized learning paths with curated resources and realistic timelines."),
        ("Visual Dashboard", "Radar charts, progress bars, and a downloadable report in one clean view."),
    ]
    for col, (title, desc) in zip(fc, feats):
        with col:
            st.markdown(f"""
            <div class="glass-card fade-up" style="padding:13px;">
                <p style="font-size:9px;font-weight:700;letter-spacing:.13em;text-transform:uppercase;
                          color:#CEB5D4;margin-bottom:5px;">Feature</p>
                <h3 style="font-family:'Playfair Display',serif;font-size:13.5px;color:#fff;
                           font-weight:600;margin-bottom:4px;">{title}</h3>
                <p style="font-size:11.5px;color:rgba(255,255,255,0.58);line-height:1.58;margin:0;">{desc}</p>
            </div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div style="display:flex;justify-content:center;gap:44px;flex-wrap:wrap;
                padding:28px 24px 44px;text-align:center;">
        {''.join(f'<div class="fade-up"><p style="font-family:Playfair Display,serif;font-size:26px;font-weight:700;color:#CEB5D4;margin:0;">{s}</p><p style="font-size:10px;text-transform:uppercase;letter-spacing:.1em;color:rgba(255,255,255,0.48);margin:2px 0 0;">{l}</p></div>'
                 for s,l in [("8+","Target Roles"),("100+","Skills Mapped"),("5 sec","Analysis Time")])}
    </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════════
# ANALYZER PAGE
# ════════════════════════════════════════════════════════════════════════════════
def render_analyzer():
    errors = st.session_state.errors

    # Nav
    nc1, nc2, nc3 = st.columns([1, 6, 1])
    with nc1:
        st.markdown("<div style='padding-top:10px;'>", unsafe_allow_html=True)
        if st.button("← Home", key="bk"):
            st.session_state.page = "home"
            st.session_state.results = None
            st.session_state.errors = {}
            st.session_state.submitted = False
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    with nc2:
        st.markdown("""
        <div class="nav-bar" style="border-bottom:none;background:transparent;justify-content:center;">
            <div class="nav-brand">SkillSync AI</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class="page-wrap slide-in" style="padding:0 24px 6px;max-width:1200px;margin:0 auto;">
        <p style="font-size:10px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;
                  color:#CEB5D4;margin:0 0 3px;">Skill Gap Analyzer</p>
        <h1 style="font-family:'Playfair Display',serif;font-size:22px;color:#fff;margin:0;">
            Map your skills. Close the gaps.
        </h1>
    </div>""", unsafe_allow_html=True)

    st.markdown("<div style='padding:10px 24px 0;max-width:1200px;margin:0 auto;'>", unsafe_allow_html=True)

    # ── Global error banner ───────────────────────────────────────────────────
    if errors and st.session_state.submitted:
        missing_labels = []
        if errors.get("name"):      missing_labels.append("Name")
        if errors.get("role"):      missing_labels.append("Target Role")
        if errors.get("exp"):       missing_labels.append("Experience Level")
        if errors.get("skills"):    missing_labels.append("Current Skills")
        error_banner(f"Please fill in the following required fields: {', '.join(missing_labels)}.")

    col_a, col_b = st.columns([2, 3], gap="large")

    # ── Left panel ────────────────────────────────────────────────────────────
    with col_a:
        name_err  = errors.get("name",  False) and st.session_state.submitted
        role_err  = errors.get("role",  False) and st.session_state.submitted
        exp_err   = errors.get("exp",   False) and st.session_state.submitted

        st.markdown(f"""
        <div class="glass-card fade-up" style="padding:14px 16px 8px;margin-bottom:6px;">
            <div class="section-label">Your Information</div>
            <h3 style="font-family:'Playfair Display',serif;font-size:14px;color:#fff;margin:0 0 2px;">Tell us about yourself</h3>
        </div>""", unsafe_allow_html=True)

        # Name field
        st.markdown(f"""
        <div class="field-label">
            Full Name <span class="required-star">*</span>
        </div>""", unsafe_allow_html=True)
        name = st.text_input(
            "Name", placeholder="e.g. Alex Morgan",
            label_visibility="collapsed", key="inp_name"
        )
        if name_err:
            field_err("Name is required.")
        st.markdown(f"""
        <style>[data-testid="stTextInput"]:has(input[value=""]) input{{border-color:{'rgba(212,90,48,0.7)' if name_err else 'rgba(255,255,255,0.22)'}!important;}}</style>
        """, unsafe_allow_html=True)

        # Role field
        st.markdown(f"""
        <div class="field-label" style="margin-top:10px;">
            Target Role <span class="required-star">*</span>
        </div>""", unsafe_allow_html=True)
        role_opts = ["— Select a role —"] + list(ROLES_DATA.keys())
        role_idx  = st.session_state.get("role_idx", 0)
        target_role = st.selectbox(
            "Target Role", role_opts,
            index=0, label_visibility="collapsed", key="inp_role"
        )
        if role_err or (target_role == "— Select a role —" and st.session_state.submitted):
            field_err("Please select a target role.")

        # Experience field
        st.markdown(f"""
        <div class="field-label" style="margin-top:10px;">
            Experience Level <span class="required-star">*</span>
        </div>""", unsafe_allow_html=True)
        exp_opts = ["— Select level —"] + list(EXPERIENCE_MULTIPLIERS.keys())
        experience = st.selectbox(
            "Experience Level", exp_opts,
            index=0, label_visibility="collapsed", key="inp_exp"
        )
        if exp_err or (experience == "— Select level —" and st.session_state.submitted):
            field_err("Please select your experience level.")

    # ── Right panel ───────────────────────────────────────────────────────────
    with col_b:
        skills_err = errors.get("skills", False) and st.session_state.submitted

        st.markdown(f"""
        <div class="glass-card fade-up" style="padding:14px 16px 8px;margin-bottom:6px;">
            <div class="section-label">Skills Assessment</div>
            <h3 style="font-family:'Playfair Display',serif;font-size:14px;color:#fff;margin:0 0 4px;">Your current skills</h3>
            <p style="font-size:11.5px;color:rgba(255,255,255,0.56);line-height:1.6;margin:0;">
                Enter skills separated by commas or new lines. Technologies, frameworks, and tools all count.
            </p>
        </div>""", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="field-label">
            Current Skills <span class="required-star">*</span>
        </div>""", unsafe_allow_html=True)
        skills_raw = st.text_area(
            "Skills", height=170,
            placeholder="e.g.\npython, machine learning, sql, pandas,\nnumpy, git, docker, statistics",
            label_visibility="collapsed", key="inp_skills"
        )
        if skills_err:
            field_err("Please enter at least one skill.")

        ex1, ex2, ex3 = st.columns(3)
        EXAMPLES = {
            "Data Scientist":       "python, sql, pandas, numpy, matplotlib, statistics, jupyter, git, scikit-learn",
            "ML Engineer":          "python, tensorflow, docker, git, flask, sql, numpy, machine learning, fastapi",
            "DevOps Engineer":      "linux, docker, aws, git, bash, ci/cd, networking, monitoring, kubernetes",
        }
        for col, (ex_role, ex_skills) in zip([ex1, ex2, ex3], EXAMPLES.items()):
            with col:
                if st.button(f"Try {ex_role.split()[0]}", key=f"ex_{ex_role}", use_container_width=True):
                    st.session_state["_prefill"] = ex_skills
                    st.rerun()

    if "_prefill" in st.session_state:
        skills_raw = st.session_state.pop("_prefill")

    st.markdown("</div>", unsafe_allow_html=True)

    # ── Analyze button ────────────────────────────────────────────────────────
    rb1, rb2, rb3 = st.columns([3, 1.8, 3])
    with rb2:
        st.markdown("<div style='padding:14px 0 6px;'>", unsafe_allow_html=True)
        run = st.button("Run Analysis", key="run_btn", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <style>
    div[data-testid="column"]:nth-of-type(5) [data-testid="stButton"]>button{
        background:linear-gradient(135deg,#102B53,#4E7AB1)!important;
        color:#fff!important;border:none!important;
        padding:0.85rem 0.4rem!important;font-size:14px!important;
        box-shadow:0 8px 26px rgba(16,43,83,0.45)!important;
    }
    </style>""", unsafe_allow_html=True)

    if run:
        st.session_state.submitted = True
        new_errors = {}

        if not name or not name.strip():
            new_errors["name"] = True
        if not target_role or target_role == "— Select a role —":
            new_errors["role"] = True
        if not experience or experience == "— Select level —":
            new_errors["exp"] = True

        parsed_skills = parse_skills_input(skills_raw) if skills_raw and skills_raw.strip() else []
        if not parsed_skills:
            new_errors["skills"] = True

        st.session_state.errors = new_errors

        if new_errors:
            st.rerun()
        else:
            st.session_state.errors = {}
            with st.spinner("Analyzing your profile..."):
                exp_mult  = EXPERIENCE_MULTIPLIERS[experience]
                role_data = ROLES_DATA[target_role]
                scores    = weighted_match_score(parsed_skills, role_data, exp_mult)
                readiness = compute_readiness_score(scores["match_score"], exp_mult)
                roadmap   = generate_learning_roadmap(scores["missing_skills"], role_data)
                timeline  = estimate_timeline(roadmap)
                radar     = radar_chart_data(parsed_skills, role_data["required_skills"], role_data.get("weights", {}))
                gap_desc  = describe_gap(
                    scores["match_score"], readiness["label"],
                    scores["strengths"], scores["missing_skills"],
                    target_role, experience, timeline, role_data
                )
                st.session_state.results = dict(
                    name=name, role=target_role, experience=experience,
                    user_skills=parsed_skills, scores=scores, readiness=readiness,
                    roadmap=roadmap, timeline=timeline, radar=radar,
                    role_data=role_data, gap_desc=gap_desc,
                )
            st.rerun()

    if st.session_state.results:
        render_results(st.session_state.results)


# ════════════════════════════════════════════════════════════════════════════════
# RESULTS
# ════════════════════════════════════════════════════════════════════════════════
def render_results(r):
    scores   = r["scores"]
    readiness= r["readiness"]
    radar    = r["radar"]
    roadmap  = r["roadmap"]
    gap_desc = r["gap_desc"]

    st.markdown(f"""
    <div class="page-wrap slide-in" style="padding:18px 24px 4px;max-width:1200px;margin:0 auto;">
        <hr style="border:none;border-top:0.5px solid rgba(255,255,255,0.12);margin-bottom:16px;">
        <p style="font-size:10px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;
                  color:#CEB5D4;margin:0 0 3px;">Analysis Complete</p>
        <h2 style="font-family:'Playfair Display',serif;font-size:20px;color:#fff;margin:0;">
            Results — {r['role']}
        </h2>
    </div>""", unsafe_allow_html=True)

    st.markdown("<div style='padding:10px 24px 0;max-width:1200px;margin:0 auto;'>", unsafe_allow_html=True)

    # ── Score cards ───────────────────────────────────────────────────────────
    mc1, mc2, mc3, mc4 = st.columns(4, gap="small")
    cards = [
        ("Match Score",    f"{scores['match_score']}%", "Skill alignment",     C["interactive"]),
        ("Readiness",      f"{readiness['score']}%",    readiness["label"],     readiness["color"]),
        ("Skills Matched", f"{len(scores['matched_skills'])} / {len(r['role_data']['required_skills'])}", "Of required",  "#fff"),
        ("Timeline",       r["timeline"],               "To reach job-ready",  "#CEB5D4"),
    ]
    for col, (lbl, val, sub, col_c) in zip([mc1, mc2, mc3, mc4], cards):
        with col:
            metric_card(lbl, val, sub, col_c)

    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

    # ── Analyst Note ──────────────────────────────────────────────────────────
    stance_styles = {
        "strong":      ("rgba(20,60,38,0.88)", "rgba(45,122,79,0.5)", "#a3e4b7"),
        "progressing": ("rgba(18,38,78,0.88)", "rgba(78,122,177,0.5)", "#b8d4f5"),
        "early":       ("rgba(50,28,72,0.88)", "rgba(120,85,160,0.5)", "#d4b8f0"),
        "foundational":("rgba(55,26,14,0.88)", "rgba(180,88,40,0.5)",  "#f5c4a3"),
    }
    bg_s, bord_s, txt_s = stance_styles.get(gap_desc["stance"], stance_styles["early"])
    st.markdown(f"""
    <div class="analyst-box" style="background:{bg_s};border:0.5px solid {bord_s};">
        <div class="analyst-lbl" style="color:{bord_s};">Analyst Note</div>
        <p class="analyst-p" style="color:{txt_s};font-weight:500;">{gap_desc['opener']}</p>
        {'<p class="analyst-p" style="color:'+txt_s+';opacity:.9;">'+gap_desc['st_note']+'</p>' if gap_desc['st_note'] else ''}
        <p class="analyst-p" style="color:{txt_s};opacity:.88;">{gap_desc['gap_note']}</p>
        <p class="analyst-p" style="color:{txt_s};opacity:.75;border-top:0.5px solid {bord_s};padding-top:7px;margin-bottom:0;">{gap_desc['tl_note']}</p>
    </div>""", unsafe_allow_html=True)

    # ── Gauge + Coverage bars ──────────────────────────────────────────────────
    ch1, ch2 = st.columns(2, gap="large")
    with ch1:
        ms = scores["match_score"]
        gc = C["success"] if ms >= 70 else C["interactive"] if ms >= 45 else C["accent"]
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=ms,
            number={"suffix": "%", "font": {"size": 42, "family": "Playfair Display", "color": "#fff"}},
            gauge={
                "axis": {"range": [0, 100], "tickfont": {"color": "rgba(255,255,255,0.45)", "size": 9},
                         "gridcolor": "rgba(255,255,255,0.1)"},
                "bar":  {"color": gc, "thickness": 0.26},
                "bgcolor": "rgba(0,0,0,0)", "borderwidth": 0,
                "steps": [
                    {"range": [0,  40],  "color": "rgba(206,181,212,0.1)"},
                    {"range": [40, 70],  "color": "rgba(78,122,177,0.1)"},
                    {"range": [70, 100], "color": "rgba(45,122,79,0.08)"},
                ],
                "threshold": {"line": {"color": "#CEB5D4", "width": 2}, "thickness": 0.75, "value": ms},
            },
            title={"text": "Match Score", "font": {"family": "Inter", "size": 11, "color": "rgba(255,255,255,0.5)"}},
            domain={"x": [0.08, 0.92], "y": [0.05, 0.95]},
        ))
        fig.update_layout(**plotly_base(), height=260)
        st.markdown(f'<div class="glass-card fade-up" style="padding:6px;">', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with ch2:
        weights  = r["role_data"].get("weights", {})
        user_set = set(r["user_skills"])
        bars = []
        for s in r["role_data"]["required_skills"][:10]:
            has = s in user_set
            bars.append({"s": s, "pct": (weights.get(s,5)*10) if has else 0, "has": has})

        bar_html = ""
        for b in bars:
            col_c = "#4E7AB1" if b["has"] else "#CEB5D4"
            lbl2  = "Matched" if b["has"] else "Gap"
            bar_html += f"""
            <div class="bar-row">
                <div class="bar-label-row">
                    <span style="color:#fff;font-weight:500;font-size:11px;">{b['s'].title()}</span>
                    <span style="font-size:10px;color:{col_c};">{lbl2}</span>
                </div>
                <div class="bar-track">
                    <div class="bar-fill" style="width:{b['pct']}%;background:{col_c};"></div>
                </div>
            </div>"""

        st.markdown(f"""
        <div class="glass-card fade-up" style="padding:14px;">
            <p style="font-size:10px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;
                      color:rgba(255,255,255,0.5);margin-bottom:4px;">Skill Coverage</p>
            <h3 style="font-family:'Playfair Display',serif;font-size:13.5px;color:#fff;margin-bottom:10px;">
                Role skills — matched vs gaps
            </h3>
            {bar_html}
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

    # ── Radar chart ───────────────────────────────────────────────────────────
    cats = list(radar.keys())
    vals = list(radar.values())
    if len(cats) >= 3:
        fig2 = go.Figure()
        fig2.add_trace(go.Scatterpolar(
            r=vals+[vals[0]], theta=cats+[cats[0]], fill="toself",
            fillcolor="rgba(78,122,177,0.2)",
            line=dict(color=C["interactive"], width=2), name="Your Profile",
        ))
        fig2.add_trace(go.Scatterpolar(
            r=[100]*(len(cats)+1), theta=cats+[cats[0]], fill="toself",
            fillcolor="rgba(206,181,212,0.06)",
            line=dict(color=C["accent"], width=1, dash="dot"), name="Target",
        ))
        fig2.update_layout(
            **plotly_base(), height=280,
            polar=dict(
                bgcolor="rgba(0,0,0,0)",
                radialaxis=dict(visible=True, range=[0,100],
                                tickfont=dict(color="rgba(255,255,255,0.45)",size=9),
                                gridcolor="rgba(255,255,255,0.12)"),
                angularaxis=dict(tickfont=dict(color="#fff",size=10),
                                 gridcolor="rgba(255,255,255,0.1)"),
            ),
            showlegend=True,
            legend=dict(font=dict(color="rgba(255,255,255,0.55)",size=10),
                       orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
        )
        st.markdown('<div class="glass-card fade-up" style="padding:6px;">', unsafe_allow_html=True)
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

    # ── Strengths + Gaps ──────────────────────────────────────────────────────
    sg1, sg2 = st.columns(2, gap="large")
    with sg1:
        items = ""
        for s in scores["strengths"]:
            items += f'<div class="skill-row" style="background:rgba(78,122,177,0.15);border-left:3px solid #4E7AB1;"><span class="skill-name">{s.title()}</span></div>'
        if not items:
            items = '<p style="color:rgba(255,255,255,0.45);font-size:12px;">No matched skills yet.</p>'
        st.markdown(f"""
        <div class="glass-card fade-up">
            <div class="section-label">Existing Strengths</div>
            <h3 class="section-title">What you already bring</h3>
            {items}
        </div>""", unsafe_allow_html=True)

    with sg2:
        items2 = ""
        for i, s in enumerate(scores["missing_skills"][:8]):
            p = "Critical" if i < 3 else "High" if i < 6 else "Medium"
            pc = "#4E7AB1" if i < 3 else "#7D9FC0" if i < 6 else "#CEB5D4"
            items2 += f'<div class="skill-row" style="background:rgba(206,181,212,0.08);border-left:3px solid {pc};"><span class="skill-name">{s.title()}</span><span class="priority-pill" style="background:{pc};">{p}</span></div>'
        if not items2:
            items2 = '<p style="color:rgba(255,255,255,0.45);font-size:12px;">No significant gaps — strong profile.</p>'
        st.markdown(f"""
        <div class="glass-card fade-up">
            <div class="section-label">Skill Gaps</div>
            <h3 class="section-title">Priority to acquire</h3>
            {items2}
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

    # ── Roadmap ───────────────────────────────────────────────────────────────
    priority_order = {"Critical": 1, "High": 2, "Medium": 3, "Low": 4}
    sorted_rm = sorted(roadmap, key=lambda x: priority_order.get(x["priority"], 5))

    st.markdown(f"""
    <div class="glass-card fade-up" style="padding:14px 18px 10px;margin-bottom:10px;">
        <div class="section-label">Personalized Roadmap</div>
        <h2 style="font-family:'Playfair Display',serif;font-size:18px;color:#fff;margin:0 0 3px;">
            Your learning path to {r['role']}
        </h2>
        <p style="font-size:12px;color:rgba(255,255,255,0.56);margin:0;">
            Ranked by impact on role fit. Total commitment: <strong style="color:#fff;">{r['timeline']}</strong> at 8–10 hrs/week.
        </p>
    </div>""", unsafe_allow_html=True)

    p_colors = {"Critical": "#4E7AB1", "High": "#7D9FC0", "Medium": "#CEB5D4", "Low": "#50698D"}
    rd1, rd2 = st.columns(2, gap="medium")
    for i, item in enumerate(sorted_rm):
        col = rd1 if i % 2 == 0 else rd2
        pc  = p_colors.get(item["priority"], "#7D9FC0")
        with col:
            st.markdown(f"""
            <div class="roadmap-card" style="border-left-color:{pc};">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:5px;">
                    <div class="roadmap-skill">{item['skill']}</div>
                    <span class="priority-pill" style="background:{pc};">{item['priority']}</span>
                </div>
                <div class="roadmap-res">{item['resource']}</div>
                <div class="roadmap-dur">Duration: <strong>{item['duration']}</strong></div>
            </div>""", unsafe_allow_html=True)

    # ── Download ──────────────────────────────────────────────────────────────
    report_text = generate_text_report(
        name=r["name"], role=r["role"], experience=r["experience"],
        match_score=scores["match_score"], readiness=readiness,
        strengths=scores["strengths"], missing_skills=scores["missing_skills"],
        roadmap=roadmap, timeline=r["timeline"],
    )
    dl1, dl2, dl3 = st.columns([3, 1.8, 3])
    with dl2:
        st.markdown("<div style='padding:12px 0;'>", unsafe_allow_html=True)
        st.download_button(
            "⬇ Download Report", data=report_text,
            file_name=f"SkillSync_{r['role'].replace(' ','_')}.txt",
            mime="text/plain", use_container_width=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div style='height:3rem;'></div>", unsafe_allow_html=True)


# ── Router ────────────────────────────────────────────────────────────────────
if st.session_state.page == "home":
    render_home()
else:
    render_analyzer()
