# -*- coding: utf-8 -*-
"""
FACADIER.SARL — L'art de la pose
Plateforme de gestion intégrée : pose de façades (aluminium, verre, marbre, placage)
& location de nacelles élévatrices
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta, date
from streamlit_option_menu import option_menu
from pathlib import Path
import base64
import random

# ============================================================================
# LOGO — chargement du logo officiel (dossier assets/, à côté de ce fichier)
# ============================================================================
LOGO_PATH = Path(__file__).parent / "assets" / "logo_facadier.jpg"

@st.cache_data
def get_logo_base64():
    if LOGO_PATH.exists():
        return base64.b64encode(LOGO_PATH.read_bytes()).decode()
    return None

LOGO_B64 = get_logo_base64()

# ============================================================================
# CONFIGURATION GÉNÉRALE
# ============================================================================
st.set_page_config(
    page_title="FACADIER.SARL",
    page_icon="⬛",
    layout="wide",
    initial_sidebar_state="expanded",
)

random.seed(42)
np.random.seed(42)

# ============================================================================
# ICÔNES — SVG vectoriels dessinés à la main (aucun emoji), style trait fin
# cohérent avec l'univers du bâtiment / façade / levage
# ============================================================================
ICON_STROKE = 1.7

def icon(name, size=22, color="currentColor"):
    paths = {
        "nacelle": f'''
            <rect x="2" y="19" width="20" height="2.4" rx="1"/>
            <rect x="9" y="15" width="6" height="4.2" rx="0.6"/>
            <line x1="12" y1="15" x2="12" y2="7"/>
            <line x1="9.3" y1="10.5" x2="14.7" y2="10.5"/>
            <rect x="6.4" y="3.4" width="11.2" height="4.4" rx="0.8"/>
            <line x1="7.6" y1="3.4" x2="7.6" y2="7.8"/>
            <line x1="10.2" y1="3.4" x2="10.2" y2="7.8"/>
            <line x1="12.8" y1="3.4" x2="12.8" y2="7.8"/>
            <line x1="15.4" y1="3.4" x2="15.4" y2="7.8"/>
        ''',
        "facade": f'''
            <rect x="3" y="4" width="18" height="17" rx="0.6"/>
            <line x1="3" y1="9" x2="21" y2="9"/>
            <line x1="3" y1="14" x2="21" y2="14"/>
            <line x1="8" y1="4" x2="8" y2="21"/>
            <line x1="13" y1="4" x2="13" y2="21"/>
            <line x1="18" y1="4" x2="18" y2="21"/>
        ''',
        "glass": f'''
            <rect x="4" y="3" width="16" height="18" rx="0.8"/>
            <line x1="6.5" y1="18.5" x2="14" y2="5.5"/>
            <line x1="10" y1="18.5" x2="17.5" y2="5.5"/>
        ''',
        "aluminum": f'''
            <line x1="3" y1="6" x2="21" y2="6"/>
            <line x1="3" y1="12" x2="21" y2="12"/>
            <line x1="3" y1="18" x2="21" y2="18"/>
            <rect x="3" y="4.6" width="18" height="2.8" rx="0.5"/>
            <rect x="3" y="10.6" width="18" height="2.8" rx="0.5"/>
            <rect x="3" y="16.6" width="18" height="2.8" rx="0.5"/>
        ''',
        "marble": f'''
            <rect x="3" y="4" width="18" height="16" rx="1"/>
            <path d="M4 9 Q9 7 12 9.5 T20 9"/>
            <path d="M3.5 14 Q8 12.5 12.5 15 T20.5 13.5"/>
        ''',
        "cladding": f'''
            <rect x="3" y="14" width="8.4" height="6.6" rx="0.5"/>
            <rect x="12.4" y="14" width="8.4" height="6.6" rx="0.5"/>
            <rect x="3" y="6.4" width="8.4" height="6.6" rx="0.5"/>
            <rect x="12.4" y="6.4" width="8.4" height="6.6" rx="0.5"/>
        ''',
        "calculator": f'''
            <rect x="5" y="2.5" width="14" height="19" rx="1.4"/>
            <line x1="7.4" y1="6" x2="16.6" y2="6"/>
            <circle cx="7.7" cy="10.4" r="0.9" fill="{color}" stroke="none"/>
            <circle cx="12" cy="10.4" r="0.9" fill="{color}" stroke="none"/>
            <circle cx="16.3" cy="10.4" r="0.9" fill="{color}" stroke="none"/>
            <circle cx="7.7" cy="14.2" r="0.9" fill="{color}" stroke="none"/>
            <circle cx="12" cy="14.2" r="0.9" fill="{color}" stroke="none"/>
            <circle cx="16.3" cy="14.2" r="0.9" fill="{color}" stroke="none"/>
            <circle cx="7.7" cy="18" r="0.9" fill="{color}" stroke="none"/>
            <circle cx="12" cy="18" r="0.9" fill="{color}" stroke="none"/>
            <circle cx="16.3" cy="18" r="0.9" fill="{color}" stroke="none"/>
        ''',
        "invoice": f'''
            <path d="M6 2.5h9l3 3v16H6z"/>
            <path d="M15 2.5v3h3"/>
            <line x1="8.4" y1="10.5" x2="15.6" y2="10.5"/>
            <line x1="8.4" y1="13.6" x2="15.6" y2="13.6"/>
            <line x1="8.4" y1="16.7" x2="13" y2="16.7"/>
        ''',
        "folder": f'''
            <path d="M3 6.4a1 1 0 0 1 1-1h5l2 2.2h9a1 1 0 0 1 1 1v9.4a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1z"/>
        ''',
        "chart": f'''
            <line x1="3" y1="21" x2="21" y2="21"/>
            <rect x="5" y="12.5" width="3.6" height="8.2" rx="0.4"/>
            <rect x="10.2" y="7.5" width="3.6" height="13.2" rx="0.4"/>
            <rect x="15.4" y="15.5" width="3.6" height="5.2" rx="0.4"/>
        ''',
        "gear": f'''
            <circle cx="12" cy="12" r="3.1"/>
            <path d="M12 3.2v2.4M12 18.4v2.4M20.8 12h-2.4M5.6 12H3.2M18 6l-1.7 1.7M7.7 16.3L6 18M18 18l-1.7-1.7M7.7 7.7L6 6"/>
        ''',
        "client": f'''
            <circle cx="12" cy="8" r="3.6"/>
            <path d="M4.5 20.5c1-4 4-6 7.5-6s6.5 2 7.5 6"/>
        ''',
        "check": f'''
            <circle cx="12" cy="12" r="9.2"/>
            <path d="M7.6 12.4l3 3 6-6.4"/>
        ''',
        "alert": f'''
            <path d="M12 3.4 21.3 20H2.7z"/>
            <line x1="12" y1="9.6" x2="12" y2="14.2"/>
            <circle cx="12" cy="17" r="0.15" fill="{color}" stroke="{color}" stroke-width="1.6"/>
        ''',
        "calendar": f'''
            <rect x="3" y="4.6" width="18" height="16" rx="1.2"/>
            <line x1="3" y1="9.4" x2="21" y2="9.4"/>
            <line x1="7.4" y1="2.4" x2="7.4" y2="6.6"/>
            <line x1="16.6" y1="2.4" x2="16.6" y2="6.6"/>
        ''',
        "truck": f'''
            <rect x="2" y="8" width="12" height="9" rx="0.8"/>
            <path d="M14 11h4.4L21 14.6V17h-7z"/>
            <circle cx="6.5" cy="18.4" r="1.7"/>
            <circle cx="17.5" cy="18.4" r="1.7"/>
        ''',
        "wrench": f'''
            <path d="M14.5 6.5a4 4 0 0 1-5.4 5.4L4 17l3 3 5.1-5.1a4 4 0 0 1 5.4-5.4l-2.6 2.6-2-2z"/>
        ''',
        "pin": f'''
            <path d="M12 21.5s7-6.6 7-11.8a7 7 0 0 0-14 0c0 5.2 7 11.8 7 11.8z"/>
            <circle cx="12" cy="9.6" r="2.4"/>
        ''',
        "clock": f'''
            <circle cx="12" cy="12" r="9.2"/>
            <path d="M12 6.8V12l3.6 2.1"/>
        ''',
        "coin": f'''
            <circle cx="12" cy="12" r="9.2"/>
            <path d="M9.6 8.8c0-1 1-1.8 2.4-1.8s2.4.8 2.4 1.8-1 1.4-2.4 1.8-2.4.9-2.4 1.9 1 1.8 2.4 1.8 2.4-.8 2.4-1.8"/>
        ''',
        "trend": f'''
            <polyline points="3,17 9,10.5 13,14 21,5"/>
            <polyline points="15,5 21,5 21,11"/>
        ''',
        "doc": f'''
            <path d="M6 2.5h8l4 4v15H6z"/>
            <path d="M14 2.5v4h4"/>
            <line x1="8.4" y1="12" x2="15.6" y2="12"/>
            <line x1="8.4" y1="15.4" x2="15.6" y2="15.4"/>
        ''',
        "automation": f'''
            <circle cx="7" cy="7" r="2.6"/>
            <circle cx="17" cy="17" r="2.6"/>
            <path d="M9.4 8.4 15 15.6"/>
            <path d="M7 9.6v5a2 2 0 0 0 2 2h1"/>
        ''',
        "bolt": f'''
            <polygon points="13,2 4,14 11,14 10,22 20,9 13,9"/>
        ''',
        "shield": f'''
            <path d="M12 2.5 20 6v6c0 5-3.4 8.4-8 9.5-4.6-1.1-8-4.5-8-9.5V6z"/>
            <path d="M8.6 12.2l2.4 2.4 4.4-5"/>
        ''',
        "box": f'''
            <path d="M3 7.5 12 3l9 4.5-9 4.5-9-4.5z"/>
            <path d="M3 7.5v9L12 21l9-4.5v-9"/>
            <line x1="12" y1="12" x2="12" y2="21"/>
        ''',
    }
    inner = paths.get(name, paths["box"])
    return f'''<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none"
        stroke="{color}" stroke-width="{ICON_STROKE}" stroke-linecap="round"
        stroke-linejoin="round" xmlns="http://www.w3.org/2000/svg">{inner}</svg>'''

# ============================================================================
# THÈME — CSS injecté (identité visuelle "structure & chantier")
# Palette : navy structurel, orange sécurité nacelle, teal verrier, crème marbre
# Typo : Space Grotesk (display / architecturale) + Inter (lecture) + JetBrains Mono (données)
# ============================================================================
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;600&display=swap');

:root{
    --navy:#152B6B;
    --navy-dk:#0A1440;
    --steel:#5B6B7C;
    --steel-lt:#D8E0E8;
    --orange:#2E5BFF;
    --orange-dk:#1B3FCC;
    --teal:#1FBEB0;
    --cream:#EEF2FA;
    --white:#FFFFFF;
    --ink:#101820;
    --ok:#1E9E6B;
    --warn:#E0A000;
    --danger:#D7443E;
    --radius:14px;
}

html, body, [class*="css"]  { font-family:'Inter', sans-serif; }
.stApp { background: var(--cream); }

h1,h2,h3,h4, .display-font { font-family:'Space Grotesk', sans-serif !important; letter-spacing:-0.01em; }

/* ---- Bandeau structure (motif "mur-rideau") en fond du header ---- */
.mullion-band{
    position:relative;
    background:
        repeating-linear-gradient(115deg, rgba(255,255,255,0.05) 0 2px, transparent 2px 46px),
        linear-gradient(120deg, var(--navy-dk) 0%, var(--navy) 55%, #123554 100%);
    border-radius: 18px;
    padding: 28px 34px;
    margin-bottom: 22px;
    box-shadow: 0 10px 30px rgba(8,24,38,0.28);
    overflow:hidden;
}
.mullion-band::after{
    content:"";
    position:absolute; top:0; right:-10%; width:55%; height:100%;
    background: repeating-linear-gradient(90deg, rgba(255,122,41,0.07) 0 3px, transparent 3px 34px);
    pointer-events:none;
}
.brand-row{ display:flex; align-items:center; gap:14px; position:relative; z-index:2;}
.brand-mark{
    width:46px; height:46px; border-radius:12px;
    background: linear-gradient(145deg, var(--orange), var(--orange-dk));
    display:flex; align-items:center; justify-content:center;
    box-shadow: 0 6px 14px rgba(255,122,41,0.35);
    color:white; flex-shrink:0;
}
.brand-title{ color:white; font-size:1.55rem; font-weight:700; margin:0; line-height:1.15;}
.brand-sub{ color:#AFC2D6; font-size:0.86rem; margin:2px 0 0 0; font-weight:400; letter-spacing:0.01em;}
.eyebrow{
    text-transform:uppercase; letter-spacing:0.14em; font-size:0.68rem; font-weight:600;
    color:var(--orange); margin-bottom:4px; display:block;
}

/* ---- Cartes KPI ---- */
.kpi-card{
    background:var(--white); border-radius:var(--radius);
    padding:18px 20px; box-shadow: 0 2px 14px rgba(15,42,68,0.07);
    border-left:4px solid var(--accent, var(--orange));
    height:100%; position:relative; transition:transform .15s ease, box-shadow .15s ease;
}
.kpi-card:hover{ transform:translateY(-2px); box-shadow:0 8px 22px rgba(15,42,68,0.12); }
.kpi-top{ display:flex; align-items:center; justify-content:space-between; margin-bottom:10px;}
.kpi-icon{
    width:38px; height:38px; border-radius:10px; display:flex; align-items:center; justify-content:center;
    background: var(--accent-soft, #FFEEE1); color:var(--accent, var(--orange));
}
.kpi-label{ font-size:0.72rem; text-transform:uppercase; letter-spacing:0.08em; color:var(--steel); font-weight:600;}
.kpi-value{ font-family:'Space Grotesk',sans-serif; font-size:1.85rem; font-weight:700; color:var(--ink); line-height:1.1;}
.kpi-delta{ font-size:0.78rem; font-weight:600; margin-top:4px; font-family:'JetBrains Mono',monospace;}
.kpi-delta.up{ color:var(--ok); } .kpi-delta.down{ color:var(--danger); } .kpi-delta.flat{ color:var(--steel); }

/* ---- Badges de statut ---- */
.badge{
    display:inline-flex; align-items:center; gap:6px; padding:4px 11px; border-radius:20px;
    font-size:0.74rem; font-weight:600; font-family:'Inter',sans-serif; white-space:nowrap;
}
.badge-dot{ width:7px; height:7px; border-radius:50%; }
.b-green{ background:#E4F5EC; color:#177A50; } .b-green .badge-dot{ background:#1E9E6B;}
.b-orange{ background:#FFEEE1; color:#B85200; } .b-orange .badge-dot{ background:#FF7A29;}
.b-red{ background:#FBE7E6; color:#A62A25; } .b-red .badge-dot{ background:#D7443E;}
.b-blue{ background:#E7F1FB; color:#1D5C93; } .b-blue .badge-dot{ background:#2C82C9;}
.b-grey{ background:#EAEDF0; color:#4B5A68; } .b-grey .badge-dot{ background:#5B6B7C;}

/* ---- Cartes contenu / section ---- */
.section-card{
    background:var(--white); border-radius:var(--radius); padding:22px 24px;
    box-shadow:0 2px 14px rgba(15,42,68,0.06); margin-bottom:18px;
}
.section-title{ display:flex; align-items:center; gap:10px; margin-bottom:14px; }
.section-title .ic{ color:var(--orange); display:flex; }
.section-title h4{ margin:0; font-size:1.05rem; color:var(--ink); }

/* ---- Kanban ---- */
.kanban-col{ background:#EFF2F5; border-radius:12px; padding:12px; min-height:140px;}
.kanban-col h5{ font-size:0.78rem; text-transform:uppercase; letter-spacing:0.06em; color:var(--steel); margin-bottom:10px;}
.kanban-card{
    background:white; border-radius:10px; padding:12px 13px; margin-bottom:9px;
    box-shadow:0 1px 6px rgba(15,42,68,0.08); border-top:3px solid var(--orange);
    font-size:0.85rem;
}
.kanban-card b{ font-family:'Space Grotesk',sans-serif; font-size:0.92rem;}
.kanban-meta{ color:var(--steel); font-size:0.75rem; margin-top:4px;}

/* ---- Timeline ---- */
.tl-item{ display:flex; gap:14px; margin-bottom:2px;}
.tl-dot-wrap{ display:flex; flex-direction:column; align-items:center; }
.tl-dot{ width:16px; height:16px; border-radius:50%; background:var(--orange); border:3px solid #FFE1C7; flex-shrink:0;}
.tl-dot.done{ background:var(--ok); border-color:#CFEFDD;}
.tl-dot.todo{ background:var(--steel-lt); border-color:#F0F2F4;}
.tl-line{ width:2px; flex:1; background:var(--steel-lt); margin:3px 0;}
.tl-content{ padding-bottom:20px;}
.tl-content b{ font-family:'Space Grotesk',sans-serif;}
.tl-content p{ color:var(--steel); font-size:0.83rem; margin:2px 0 0 0;}

/* ---- Chip autonome : fond clair garanti + texte bleu foncé, quel que soit le fond parent ---- */
.chip{
    background:#FFFFFF !important; border-radius:11px; padding:12px 14px;
    box-shadow:0 2px 8px rgba(10,20,60,0.18);
}
.chip *{ color:var(--navy) !important; }
.chip .chip-value{ font-family:'JetBrains Mono',monospace; font-weight:700; color:var(--orange) !important; }

/* ---- Divers ---- */
.mono{ font-family:'JetBrains Mono',monospace; }
hr.soft{ border:none; border-top:1px solid #E4E8EC; margin:14px 0;}
.tag-chip{
    display:inline-block; padding:3px 10px; border-radius:8px; background:#EFF2F5; color:var(--navy);
    font-size:0.72rem; font-weight:600; margin-right:6px;
}
[data-testid="stMetricValue"]{ font-family:'Space Grotesk',sans-serif; }
.stButton>button{
    border-radius:9px; font-weight:600; border:1px solid rgba(15,42,68,0.12);
}
.stButton>button[kind="primary"]{ background:var(--orange); border:none; }
.stButton>button[kind="primary"]:hover{ background:var(--orange-dk); }
[data-testid="stSidebar"],
[data-testid="stSidebarContent"],
[data-testid="stSidebarUserContent"],
section[data-testid="stSidebar"] > div{
    background: linear-gradient(180deg, var(--navy-dk), var(--navy)) !important;
}
/* Texte par défaut clair dans la sidebar (fond sombre garanti ci-dessus) */
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span:not(.chip *),
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] div:not(.chip):not(.chip *){ color:#E9EFF4; }
/* Les chips restent autonomes : fond clair + texte bleu foncé, non affectés par la règle ci-dessus */
[data-testid="stSidebar"] .chip, [data-testid="stSidebar"] .chip *{ color:var(--navy) !important; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ============================================================================
# COMPOSANTS RÉUTILISABLES
# ============================================================================
ACCENTS = {
    "orange": ("#2E5BFF", "#E7EDFF"),   # accent principal — bleu de marque (nom conservé pour compatibilité du code)
    "teal": ("#1FBEB0", "#E1F7F4"),
    "navy": ("#152B6B", "#E9EBF8"),
    "ok": ("#1E9E6B", "#E4F5EC"),
    "danger": ("#D7443E", "#FBE7E6"),
}

def kpi_card(icon_name, label, value, delta=None, delta_dir="flat", accent="orange"):
    a, a_soft = ACCENTS.get(accent, ACCENTS["orange"])
    delta_html = ""
    if delta:
        arrow = {"up": "▲", "down": "▼", "flat": "▬"}[delta_dir]
        delta_html = f'<div class="kpi-delta {delta_dir}">{arrow} {delta}</div>'
    st.markdown(f'''
        <div class="kpi-card" style="--accent:{a}; --accent-soft:{a_soft};">
            <div class="kpi-top">
                <span class="kpi-label">{label}</span>
                <div class="kpi-icon">{icon(icon_name, 19, a)}</div>
            </div>
            <div class="kpi-value">{value}</div>
            {delta_html}
        </div>
    ''', unsafe_allow_html=True)

def badge(text, kind="grey"):
    cls = {"ok": "b-green", "warn": "b-orange", "danger": "b-red", "info": "b-blue", "grey": "b-grey"}[kind]
    return f'<span class="badge {cls}"><span class="badge-dot"></span>{text}</span>'

def section_header(icon_name, title):
    st.markdown(f'''
        <div class="section-title">
            <span class="ic">{icon(icon_name, 22)}</span>
            <h4>{title}</h4>
        </div>
    ''', unsafe_allow_html=True)

def page_header(icon_name, eyebrow, title, subtitle):
    st.markdown(f'''
        <div class="mullion-band">
            <div class="brand-row">
                <div class="brand-mark">{icon(icon_name, 24, "#FFFFFF")}</div>
                <div>
                    <span class="eyebrow">{eyebrow}</span>
                    <p class="brand-title">{title}</p>
                    <p class="brand-sub">{subtitle}</p>
                </div>
            </div>
        </div>
    ''', unsafe_allow_html=True)

STATUT_MAP_NACELLE = {"Disponible": "ok", "Louée": "warn", "Maintenance": "danger"}
STATUT_MAP_RESA = {"Confirmée": "ok", "En attente": "warn", "Terminée": "info", "Annulée": "danger"}
STATUT_MAP_DEVIS = {"Accepté": "ok", "Envoyé": "info", "Brouillon": "grey", "Refusé": "danger"}
STATUT_MAP_FACTURE = {"Payée": "ok", "En attente": "warn", "En retard": "danger"}

# ============================================================================
# DONNÉES DE DÉMONSTRATION (simulateur de base de données via session_state)
# ============================================================================
def init_data():
    if "init" in st.session_state:
        return
    st.session_state.init = True

    modeles = [
        ("N-101", "Ciseaux électrique", "Ciseaux", 10, 230),
        ("N-102", "Ciseaux électrique", "Ciseaux", 8, 230),
        ("N-203", "Télescopique diesel", "Télescopique", 18, 300),
        ("N-204", "Télescopique diesel", "Télescopique", 22, 350),
        ("N-305", "Articulée électrique", "Articulée", 16, 230),
        ("N-306", "Articulée diesel", "Articulée", 20, 250),
        ("N-407", "Araignée compacte", "Araignée", 14, 200),
        ("N-408", "Araignée compacte", "Araignée", 17, 200),
        ("N-509", "Ciseaux diesel tout-terrain", "Ciseaux", 12, 450),
        ("N-510", "Télescopique diesel", "Télescopique", 26, 350),
    ]
    statuts = ["Disponible", "Louée", "Maintenance"]
    localisations = ["Dépôt Nord", "Dépôt Sud", "Chantier Liffré", "Chantier Cesson", "Dépôt Central"]
    rows = []
    for ref, modele, typ, h, cap in modeles:
        st_ = random.choices(statuts, weights=[0.55, 0.35, 0.10])[0]
        retour = (date.today() + timedelta(days=random.randint(-2, 12))) if st_ == "Louée" else None
        rows.append({
            "ID": ref, "Modèle": modele, "Type": typ, "Hauteur (m)": h, "Capacité (kg)": cap,
            "Statut": st_, "Localisation": random.choice(localisations),
            "Prochain retour": retour.strftime("%d/%m/%Y") if retour else "—",
            "_retard": (retour is not None and retour < date.today()),
        })
    st.session_state.nacelles = pd.DataFrame(rows)

    clients_noms = ["Bâti Ouest SARL", "Groupe Armor Construction", "Cabinet Verrier & Fils",
                    "Promobat Bretagne", "SCI Les Terrasses", "Atlantique Façades",
                    "Marbrerie du Ponant", "Ker Bâtiment", "Ville de Rennes — Services Techniques",
                    "Immo Perspective"]
    types_c = ["Entreprise", "Promoteur", "Entreprise", "Promoteur", "Particulier",
               "Entreprise", "Entreprise", "Entreprise", "Collectivité", "Promoteur"]
    villes = ["Rennes", "Nantes", "Vannes", "Saint-Malo", "Lorient", "Brest", "Quimper", "Redon", "Rennes", "Nantes"]
    clist = []
    for i, (n, t, v) in enumerate(zip(clients_noms, types_c, villes)):
        clist.append({
            "ID": f"CL-{100+i}", "Nom": n, "Type": t, "Ville": v,
            "Contact": f"{['Marie','Julien','Sophie','Thomas','Claire','Nicolas'][i%6]} {['Le Roux','Morel','Guichard','Fabre','Riou','Berthier'][i%6]}",
            "Téléphone": f"02 {random.randint(10,99)} {random.randint(10,99)} {random.randint(10,99)} {random.randint(10,99)}",
            "Email": n.lower().replace(" ", "").replace("&", "et")[:14] + "@client.fr",
            "CA cumulé (€)": random.randint(8000, 240000),
            "Client depuis": random.randint(2016, 2025),
        })
    st.session_state.clients = pd.DataFrame(clist)

    resa_rows = []
    for i in range(9):
        n = st.session_state.nacelles.sample(1).iloc[0]
        deb = date.today() - timedelta(days=random.randint(-3, 20))
        fin = deb + timedelta(days=random.randint(2, 15))
        resa_rows.append({
            "ID": f"RES-{500+i}",
            "Client": random.choice(clients_noms),
            "Nacelle": n["ID"] + " · " + n["Modèle"],
            "Début": deb.strftime("%d/%m/%Y"),
            "Fin": fin.strftime("%d/%m/%Y"),
            "Statut": random.choices(["Confirmée", "En attente", "Terminée", "Annulée"], weights=[0.45,0.2,0.3,0.05])[0],
            "Montant (€)": random.randint(600, 5200),
        })
    st.session_state.reservations = pd.DataFrame(resa_rows)

    types_facade = ["Aluminium", "Verre", "Marbre", "Placage"]
    etapes = ["Devis", "Commande", "Fabrication", "Pose", "Livré"]
    proj_rows = []
    for i in range(8):
        etape = random.choice(etapes)
        avc = {"Devis": 10, "Commande": 28, "Fabrication": 55, "Pose": 80, "Livré": 100}[etape]
        deb = date.today() - timedelta(days=random.randint(10, 90))
        proj_rows.append({
            "ID": f"CH-{300+i}",
            "Client": random.choice(clients_noms),
            "Type de façade": random.choice(types_facade),
            "Étape": etape, "Avancement": avc,
            "Début": deb.strftime("%d/%m/%Y"),
            "Livraison prévue": (deb + timedelta(days=random.randint(60, 150))).strftime("%d/%m/%Y"),
            "Responsable": random.choice(["Y. Le Gall", "A. Duprat", "M. Sénéchal", "K. Robic"]),
            "Surface (m²)": random.randint(80, 900),
        })
    st.session_state.projets = pd.DataFrame(proj_rows)

    devis_rows = []
    for i in range(10):
        surf = random.randint(40, 700)
        typ = random.choice(types_facade)
        prix_m2 = {"Aluminium": 320, "Verre": 410, "Marbre": 560, "Placage": 260}[typ]
        montant = surf * prix_m2
        devis_rows.append({
            "ID": f"DV-{700+i}",
            "Client": random.choice(clients_noms),
            "Type de façade": typ, "Surface (m²)": surf,
            "Montant HT (€)": montant,
            "Statut": random.choices(["Accepté", "Envoyé", "Brouillon", "Refusé"], weights=[0.4,0.3,0.2,0.1])[0],
            "Date": (date.today() - timedelta(days=random.randint(1, 120))).strftime("%d/%m/%Y"),
        })
    st.session_state.devis = pd.DataFrame(devis_rows)

    fact_rows = []
    for i in range(10):
        montant_ht = random.randint(4000, 95000)
        tva = round(montant_ht * 0.20)
        fact_rows.append({
            "ID": f"FA-{900+i}",
            "Client": random.choice(clients_noms),
            "Montant HT (€)": montant_ht, "TVA (€)": tva, "Montant TTC (€)": montant_ht + tva,
            "Statut": random.choices(["Payée", "En attente", "En retard"], weights=[0.55, 0.3, 0.15])[0],
            "Émission": (date.today() - timedelta(days=random.randint(5, 100))).strftime("%d/%m/%Y"),
            "Échéance": (date.today() + timedelta(days=random.randint(-20, 40))).strftime("%d/%m/%Y"),
        })
    st.session_state.factures = pd.DataFrame(fact_rows)

    doc_types = ["Devis", "Contrat", "Facture", "Plan technique", "Photo chantier"]
    doc_rows = []
    for i in range(14):
        doc_rows.append({
            "Client": random.choice(clients_noms),
            "Document": f"{random.choice(doc_types)}_{random.randint(100,999)}.pdf",
            "Type": random.choice(doc_types),
            "Ajouté le": (date.today() - timedelta(days=random.randint(1, 200))).strftime("%d/%m/%Y"),
        })
    st.session_state.documents = pd.DataFrame(doc_rows)

    trans_rows = []
    mois = pd.date_range(end=date.today(), periods=12, freq="MS")
    for m in mois:
        recette = random.randint(38000, 92000)
        depense = random.randint(24000, 60000)
        trans_rows.append({"Mois": m.strftime("%b %Y"), "Recettes (€)": recette, "Dépenses (€)": depense,
                            "Marge (€)": recette - depense})
    st.session_state.compta = pd.DataFrame(trans_rows)

    st.session_state.automations = pd.DataFrame([
        {"Règle": "Alerte retard de retour nacelle", "Déclencheur": "Date de retour dépassée de 24h",
         "Action": "Notification SMS + email à l'agence", "Actif": True},
        {"Règle": "Relance devis sans réponse", "Déclencheur": "Devis « Envoyé » depuis 7 jours",
         "Action": "Email de relance automatique au client", "Actif": True},
        {"Règle": "Alerte facture en retard", "Déclencheur": "Échéance dépassée", "Action": "Relance + blocage nouvelle réservation",
         "Actif": True},
        {"Règle": "Rappel maintenance nacelle", "Déclencheur": "500h d'utilisation atteintes", "Action": "Création d'un ordre de maintenance",
         "Actif": False},
        {"Règle": "Confirmation de réservation", "Déclencheur": "Nouvelle réservation validée", "Action": "Envoi bon de sortie au client",
         "Actif": True},
        {"Règle": "Alerte fin de chantier proche", "Déclencheur": "J-5 avant livraison prévue", "Action": "Notification au chef de chantier",
         "Actif": True},
    ])

init_data()

# ============================================================================
# NAVIGATION LATÉRALE
# ============================================================================
with st.sidebar:
    if LOGO_B64:
        st.markdown(f'''
            <div style="background:white;border-radius:14px;padding:12px 14px;margin-bottom:14px;
                box-shadow:0 4px 14px rgba(10,20,60,0.25);">
                <img src="data:image/jpeg;base64,{LOGO_B64}" style="width:100%;display:block;border-radius:4px;">
            </div>
            <div style="text-align:center;margin-bottom:16px;">
                <span style="font-size:0.7rem;color:#AEC0E8;letter-spacing:0.14em;text-transform:uppercase;">Gestion intégrée</span>
            </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown(f'''
            <div style="display:flex;align-items:center;gap:10px;padding:6px 4px 18px 4px;">
                <div style="width:38px;height:38px;border-radius:10px;background:linear-gradient(145deg,#2E5BFF,#1B3FCC);
                    display:flex;align-items:center;justify-content:center;">{icon("nacelle", 20, "#fff")}</div>
                <div>
                    <div style="font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:1.15rem;color:white;">FACADIER.SARL</div>
                    <div style="font-size:0.68rem;color:#9FB4C7;letter-spacing:0.06em;">L'ART DE LA POSE</div>
                </div>
            </div>
        ''', unsafe_allow_html=True)

    selected = option_menu(
        menu_title=None,
        options=[
            "Vue d'ensemble",
            "Location de nacelles",
            "Chantiers façades",
            "Calcul de structure",
            "Facturation & clients",
            "Dossiers clients (GED)",
            "Comptabilité",
            "Automatisation",
        ],
        icons=["speedometer2", "truck-front", "buildings", "rulers", "receipt-cutoff",
               "folder2-open", "graph-up-arrow", "cpu"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0", "background-color": "transparent"},
            "icon": {"color": "#2E5BFF", "font-size": "16px"},
            "nav-link": {"font-size": "13.5px", "text-align": "left", "margin": "3px 0", "border-radius": "9px",
                         "padding": "10px 12px", "color": "#D7E2EC"},
            "nav-link-selected": {"background-color": "#E7EDFF", "color": "#152B6B", "font-weight": "600",
                                   "border-left": "3px solid #2E5BFF"},
        }
    )

    st.markdown("<hr class='soft' style='border-color:rgba(255,255,255,0.12);'>", unsafe_allow_html=True)
    st.markdown('<span style="color:#9FB4C7;font-size:0.72rem;">ACTIVITÉ PRIORITAIRE</span>', unsafe_allow_html=True)
    dispo = (st.session_state.nacelles["Statut"] == "Disponible").sum()
    total_n = len(st.session_state.nacelles)
    st.markdown(f'''
        <div class="chip" style="margin-top:8px;">
            <div style="display:flex;justify-content:space-between;font-size:0.85rem;">
                <span>Nacelles disponibles</span><span class="chip-value">{dispo}/{total_n}</span>
            </div>
        </div>
    ''', unsafe_allow_html=True)

# ============================================================================
# PAGE — VUE D'ENSEMBLE
# ============================================================================
if selected == "Vue d'ensemble":
    page_header("nacelle", "Tableau de bord général", "Bonjour, voici l'activité du jour",
                "Location de nacelles élévatrices & pose de façades aluminium, verre, marbre et placage")

    c1, c2, c3, c4 = st.columns(4)
    with c1: kpi_card("truck", "Nacelles disponibles", f"{dispo}/{total_n}", "3 retours attendus sous 48h", "up", "orange")
    with c2: kpi_card("facade", "Chantiers en cours", f"{(st.session_state.projets['Étape']!='Livré').sum()}", "+2 vs mois dernier", "up", "teal")
    with c3: kpi_card("coin", "CA du mois", "68 400 €", "+8,4 %", "up", "ok")
    with c4:
        retard = (st.session_state.factures["Statut"] == "En retard").sum()
        kpi_card("alert", "Factures en retard", f"{retard}", "à relancer", "down", "danger")

    st.write("")
    colA, colB = st.columns([1.35, 1])
    with colA:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        section_header("chart", "Recettes vs dépenses — 12 derniers mois")
        df = st.session_state.compta
        fig = go.Figure()
        fig.add_bar(x=df["Mois"], y=df["Recettes (€)"], name="Recettes", marker_color="#2E5BFF")
        fig.add_bar(x=df["Mois"], y=df["Dépenses (€)"], name="Dépenses", marker_color="#152B6B")
        fig.add_trace(go.Scatter(x=df["Mois"], y=df["Marge (€)"], name="Marge", mode="lines+markers",
                                  line=dict(color="#1FBEB0", width=3)))
        fig.update_layout(barmode="group", height=340, margin=dict(l=10, r=10, t=10, b=10),
                           plot_bgcolor="white", paper_bgcolor="white",
                           legend=dict(orientation="h", yanchor="bottom", y=1.02),
                           font=dict(family="Inter"))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with colB:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        section_header("facade", "Répartition des chantiers par matériau")
        rep = st.session_state.projets["Type de façade"].value_counts().reset_index()
        rep.columns = ["Type", "Nombre"]
        fig2 = px.pie(rep, names="Type", values="Nombre", hole=0.55,
                       color_discrete_sequence=["#2E5BFF", "#1FBEB0", "#152B6B", "#B8C4CE"])
        fig2.update_traces(textinfo="percent+label")
        fig2.update_layout(height=340, margin=dict(l=10, r=10, t=10, b=10), showlegend=False,
                            font=dict(family="Inter"))
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    section_header("alert", "Alertes prioritaires")
    alertes = []
    for _, r in st.session_state.nacelles[st.session_state.nacelles["_retard"]].iterrows():
        alertes.append(("danger", f"Retour en retard — {r['ID']} ({r['Modèle']}), attendu le {r['Prochain retour']}"))
    for _, r in st.session_state.factures[st.session_state.factures["Statut"] == "En retard"].iterrows():
        alertes.append(("warn", f"Facture {r['ID']} en retard — {r['Client']} — {r['Montant TTC (€)']:,} € TTC".replace(",", " ")))
    if not alertes:
        st.info("Aucune alerte active. Tout est sous contrôle.")
    for kind, txt in alertes[:6]:
        st.markdown(f'{badge("URGENT" if kind=="danger" else "À TRAITER", kind)}&nbsp;&nbsp;{txt}', unsafe_allow_html=True)
        st.markdown("<hr class='soft'>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# PAGE — LOCATION DE NACELLES (ACTIVITÉ PRIORITAIRE)
# ============================================================================
elif selected == "Location de nacelles":
    page_header("nacelle", "Activité prioritaire", "Location de nacelles élévatrices",
                "Disponibilité en temps réel, réservations, contrats, tarification et suivi du parc")

    tabs = st.tabs(["Tableau de bord", "Planning & disponibilité", "Réservations", "Contrats & bons de sortie",
                    "Tarification", "Suivi matériel & retours"])

    # --- Tableau de bord
    with tabs[0]:
        c1, c2, c3, c4 = st.columns(4)
        with c1: kpi_card("truck", "Disponibles", str(dispo), None, "flat", "ok")
        with c2: kpi_card("clock", "En location", str((st.session_state.nacelles['Statut']=='Louée').sum()), None, "flat", "orange")
        with c3: kpi_card("wrench", "En maintenance", str((st.session_state.nacelles['Statut']=='Maintenance').sum()), None, "flat", "danger")
        with c4: kpi_card("calendar", "Réservations actives", str((st.session_state.reservations['Statut']=='Confirmée').sum()), None, "flat", "teal")

        st.write("")
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        section_header("nacelle", "État du parc en temps réel")
        df = st.session_state.nacelles.drop(columns=["_retard"]).copy()
        def _fmt_statut(v):
            k = STATUT_MAP_NACELLE[v]
            return badge(v, k)
        for _, r in df.iterrows():
            c = st.columns([1, 2.4, 1.6, 1, 1, 1.4, 1.4])
            c[0].markdown(f"**{r['ID']}**")
            c[1].write(r["Modèle"])
            c[2].markdown(f'<span class="tag-chip">{r["Type"]}</span>', unsafe_allow_html=True)
            c[3].markdown(f'<span class="mono">{r["Hauteur (m)"]} m</span>', unsafe_allow_html=True)
            c[4].markdown(f'<span class="mono">{r["Capacité (kg)"]} kg</span>', unsafe_allow_html=True)
            c[5].markdown(_fmt_statut(r["Statut"]), unsafe_allow_html=True)
            c[6].write(r["Localisation"])
        st.markdown('</div>', unsafe_allow_html=True)

    # --- Planning
    with tabs[1]:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        section_header("calendar", "Planning d'occupation — 14 prochains jours")
        days = pd.date_range(date.today(), periods=14)
        heat = []
        for _, n in st.session_state.nacelles.iterrows():
            row = []
            for d in days:
                if n["Statut"] == "Maintenance":
                    row.append(2)
                elif n["Statut"] == "Louée" and random.random() > 0.35:
                    row.append(1)
                else:
                    row.append(0)
            heat.append(row)
        fig = go.Figure(data=go.Heatmap(
            z=heat, x=[d.strftime("%d/%m") for d in days], y=st.session_state.nacelles["ID"],
            colorscale=[[0, "#E4F5EC"], [0.5, "#FFDCB8"], [1, "#F6C6C4"]],
            showscale=False, xgap=3, ygap=3))
        fig.update_layout(height=420, margin=dict(l=10, r=10, t=10, b=10), font=dict(family="Inter"))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(f'{badge("Disponible","ok")} &nbsp; {badge("Loué / réservé","warn")} &nbsp; {badge("Maintenance","danger")}', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- Réservations
    with tabs[2]:
        colL, colR = st.columns([1, 1.5])
        with colL:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            section_header("calendar", "Nouvelle réservation")
            with st.form("form_resa"):
                client = st.selectbox("Client", st.session_state.clients["Nom"])
                nacelle_dispo = st.session_state.nacelles[st.session_state.nacelles["Statut"] == "Disponible"]
                choix_nacelle = st.selectbox("Nacelle", nacelle_dispo["ID"] + " · " + nacelle_dispo["Modèle"]
                                              if len(nacelle_dispo) else ["Aucune disponible"])
                d1, d2 = st.columns(2)
                deb = d1.date_input("Date de début", date.today())
                fin = d2.date_input("Date de fin", date.today() + timedelta(days=5))
                montant = st.number_input("Montant estimé (€)", min_value=0, value=1200, step=50)
                submit = st.form_submit_button("Créer la réservation", type="primary", use_container_width=True)
                if submit:
                    new = pd.DataFrame([{
                        "ID": f"RES-{500+len(st.session_state.reservations)}", "Client": client,
                        "Nacelle": choix_nacelle, "Début": deb.strftime("%d/%m/%Y"), "Fin": fin.strftime("%d/%m/%Y"),
                        "Statut": "Confirmée", "Montant (€)": montant,
                    }])
                    st.session_state.reservations = pd.concat([new, st.session_state.reservations], ignore_index=True)
                    st.success(f"Réservation créée pour {client}.")
            st.markdown('</div>', unsafe_allow_html=True)
        with colR:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            section_header("truck", "Réservations en cours")
            for _, r in st.session_state.reservations.iterrows():
                c = st.columns([1.1, 1.8, 1.7, 1.3, 1.3])
                c[0].markdown(f"**{r['ID']}**")
                c[1].write(r["Client"])
                c[2].write(r["Nacelle"])
                c[3].markdown(f'<span class="mono">{r["Début"]} → {r["Fin"]}</span>', unsafe_allow_html=True)
                c[4].markdown(badge(r["Statut"], STATUT_MAP_RESA[r["Statut"]]), unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # --- Contrats & bons de sortie
    with tabs[3]:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        section_header("invoice", "Génération d'un bon de sortie / contrat de location")
        c1, c2 = st.columns([1, 1.3])
        with c1:
            resa_id = st.selectbox("Réservation concernée", st.session_state.reservations["ID"])
            r = st.session_state.reservations[st.session_state.reservations["ID"] == resa_id].iloc[0]
            st.write("")
            st.checkbox("Contrôle visuel effectué", value=True)
            st.checkbox("Niveau carburant / batterie vérifié", value=True)
            st.checkbox("Équipements de sécurité remis (EPI, harnais)", value=True)
            gen = st.button("Générer le document", type="primary", use_container_width=True)
        with c2:
            if gen or True:
                st.markdown(f'''
                    <div style="border:1.5px dashed var(--steel-lt); border-radius:12px; padding:20px 22px; background:#FBFCFD;">
                        <div class="eyebrow">Bon de sortie — {r['ID']}</div>
                        <p class="display-font" style="font-size:1.2rem; font-weight:700; margin:2px 0 14px 0;">FACADIER.SARL — Location de nacelles</p>
                        <table class="mono" style="width:100%; font-size:0.85rem; line-height:1.9;">
                            <tr><td style="color:var(--steel);">Client</td><td style="text-align:right;">{r['Client']}</td></tr>
                            <tr><td style="color:var(--steel);">Matériel</td><td style="text-align:right;">{r['Nacelle']}</td></tr>
                            <tr><td style="color:var(--steel);">Période</td><td style="text-align:right;">{r['Début']} → {r['Fin']}</td></tr>
                            <tr><td style="color:var(--steel);">Montant</td><td style="text-align:right;">{r['Montant (€)']} € HT</td></tr>
                            <tr><td style="color:var(--steel);">Statut</td><td style="text-align:right;">{r['Statut']}</td></tr>
                        </table>
                        <hr class="soft">
                        <p style="font-size:0.78rem; color:var(--steel);">Signature client et responsable dépôt requises à la remise du matériel.</p>
                    </div>
                ''', unsafe_allow_html=True)
                doc_txt = (f"BON DE SORTIE — {r['ID']}\nClient: {r['Client']}\nMatériel: {r['Nacelle']}\n"
                           f"Période: {r['Début']} au {r['Fin']}\nMontant: {r['Montant (€)']} EUR HT\nStatut: {r['Statut']}\n")
                st.download_button("Télécharger le bon de sortie (.txt)", doc_txt, file_name=f"bon_sortie_{r['ID']}.txt",
                                    use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- Tarification
    with tabs[4]:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        section_header("coin", "Grille tarifaire")
        tarifs = pd.DataFrame([
            {"Type": "Ciseaux électrique", "Jour": 85, "Semaine": 340, "Mois": 980},
            {"Type": "Télescopique diesel", "Jour": 165, "Semaine": 690, "Mois": 1980},
            {"Type": "Articulée électrique", "Jour": 140, "Semaine": 590, "Mois": 1690},
            {"Type": "Araignée compacte", "Jour": 130, "Semaine": 540, "Mois": 1540},
        ])
        edited = st.data_editor(tarifs, use_container_width=True, hide_index=True,
                                 column_config={
                                     "Jour": st.column_config.NumberColumn("Tarif jour (€)"),
                                     "Semaine": st.column_config.NumberColumn("Tarif semaine (€)"),
                                     "Mois": st.column_config.NumberColumn("Tarif mois (€)"),
                                 })
        st.caption("Grille modifiable — les tarifs s'appliquent automatiquement aux nouvelles réservations.")
        st.markdown('</div>', unsafe_allow_html=True)

    # --- Suivi matériel & retours
    with tabs[5]:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        section_header("wrench", "Suivi du matériel et retours attendus")
        retours = st.session_state.nacelles[st.session_state.nacelles["Statut"] == "Louée"]
        for _, r in retours.iterrows():
            c = st.columns([1, 2.4, 1.6, 1.6, 1.4])
            c[0].markdown(f"**{r['ID']}**")
            c[1].write(r["Modèle"])
            c[2].write(r["Localisation"])
            c[3].markdown(f'<span class="mono">{r["Prochain retour"]}</span>', unsafe_allow_html=True)
            c[4].markdown(badge("Retard", "danger") if r["_retard"] else badge("Dans les temps", "ok"), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# PAGE — CHANTIERS FAÇADES
# ============================================================================
elif selected == "Chantiers façades":
    page_header("facade", "Pose de façades", "Chantiers façades — tous matériaux",
                "Aluminium, verre, marbre, placage — du devis à la livraison")

    tabs = st.tabs(["Devis", "Suivi des projets (Kanban)", "Étapes du chantier"])

    with tabs[0]:
        colL, colR = st.columns([1, 1.4])
        with colL:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            section_header("invoice", "Nouveau devis")
            with st.form("form_devis"):
                client = st.selectbox("Client", st.session_state.clients["Nom"])
                typ = st.selectbox("Type de façade", ["Aluminium", "Verre", "Marbre", "Placage"],
                                    format_func=lambda x: x)
                surf = st.number_input("Surface (m²)", min_value=1, value=120)
                prix_m2 = {"Aluminium": 320, "Verre": 410, "Marbre": 560, "Placage": 260}[typ]
                st.caption(f"Prix de référence : {prix_m2} €/m² ({typ})")
                montant = surf * prix_m2
                st.metric("Montant estimé HT", f"{montant:,} €".replace(",", " "))
                submit = st.form_submit_button("Enregistrer le devis", type="primary", use_container_width=True)
                if submit:
                    new = pd.DataFrame([{
                        "ID": f"DV-{700+len(st.session_state.devis)}", "Client": client, "Type de façade": typ,
                        "Surface (m²)": surf, "Montant HT (€)": montant, "Statut": "Brouillon",
                        "Date": date.today().strftime("%d/%m/%Y"),
                    }])
                    st.session_state.devis = pd.concat([new, st.session_state.devis], ignore_index=True)
                    st.success("Devis enregistré.")
            st.markdown('</div>', unsafe_allow_html=True)
        with colR:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            section_header("doc", "Devis récents")
            icon_type = {"Aluminium": "aluminum", "Verre": "glass", "Marbre": "marble", "Placage": "cladding"}
            for _, r in st.session_state.devis.iterrows():
                c = st.columns([0.5, 1.6, 1.3, 1, 1.1, 1.1])
                c[0].markdown(icon(icon_type[r["Type de façade"]], 20, "#2E5BFF"), unsafe_allow_html=True)
                c[1].write(r["Client"])
                c[2].write(r["Type de façade"])
                c[3].markdown(f'<span class="mono">{r["Surface (m²)"]} m²</span>', unsafe_allow_html=True)
                c[4].markdown(f'<span class="mono">{r["Montant HT (€)"]:,} €</span>'.replace(",", " "), unsafe_allow_html=True)
                c[5].markdown(badge(r["Statut"], STATUT_MAP_DEVIS[r["Statut"]]), unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    with tabs[1]:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        section_header("facade", "Suivi des projets par étape")
        etapes = ["Devis", "Commande", "Fabrication", "Pose", "Livré"]
        cols = st.columns(len(etapes))
        for col, et in zip(cols, etapes):
            with col:
                st.markdown(f'<div class="kanban-col"><h5>{et}</h5>', unsafe_allow_html=True)
                sub = st.session_state.projets[st.session_state.projets["Étape"] == et]
                for _, p in sub.iterrows():
                    st.markdown(f'''
                        <div class="kanban-card">
                            <b>{p['ID']}</b><br>{p['Client']}
                            <div class="kanban-meta">{p['Type de façade']} · {p['Surface (m²)']} m²</div>
                            <div class="kanban-meta">Livraison : {p['Livraison prévue']}</div>
                        </div>
                    ''', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tabs[2]:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        section_header("calendar", "Détail des étapes d'un chantier")
        proj_id = st.selectbox("Sélectionner un chantier", st.session_state.projets["ID"] + " — " + st.session_state.projets["Client"])
        sel = proj_id.split(" — ")[0]
        p = st.session_state.projets[st.session_state.projets["ID"] == sel].iloc[0]
        etapes = ["Devis", "Commande", "Fabrication", "Pose", "Livré"]
        idx_actuel = etapes.index(p["Étape"])
        st.progress(p["Avancement"] / 100, text=f"Avancement global : {p['Avancement']}%")
        st.write("")
        for i, et in enumerate(etapes):
            state = "done" if i < idx_actuel else ("todo" if i > idx_actuel else "")
            dotclass = "done" if i < idx_actuel else ("todo" if i > idx_actuel else "")
            is_line = i < len(etapes) - 1
            st.markdown(f'''
                <div class="tl-item">
                    <div class="tl-dot-wrap">
                        <div class="tl-dot {dotclass}"></div>
                        {'<div class="tl-line"></div>' if is_line else ''}
                    </div>
                    <div class="tl-content">
                        <b>{et}</b>
                        <p>{"Terminé" if i < idx_actuel else ("En cours" if i == idx_actuel else "À venir")} — Responsable : {p['Responsable']}</p>
                    </div>
                </div>
            ''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# PAGE — CALCUL DE STRUCTURE
# ============================================================================
elif selected == "Calcul de structure":
    page_header("calculator", "Bureau d'études", "Calcul de structure",
                "Dimensionnement, charges, ancrages et contrôle de conformité (usage indicatif — à valider par un BE)")

    tabs = st.tabs(["Dimensionnement", "Vérification des charges", "Ancrages", "Contrôle de conformité"])

    with tabs[0]:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        section_header("aluminum", "Dimensionnement d'un panneau de façade")
        c1, c2 = st.columns(2)
        with c1:
            largeur = st.number_input("Largeur du panneau (m)", 0.3, 6.0, 1.5, 0.1)
            hauteur_p = st.number_input("Hauteur du panneau (m)", 0.3, 6.0, 2.8, 0.1)
            materiau = st.selectbox("Matériau", ["Aluminium", "Verre feuilleté", "Marbre", "Panneau composite (placage)"])
            epaisseur = st.slider("Épaisseur (mm)", 4, 40, 10)
        with c2:
            vent_ref = st.slider("Vitesse de vent de référence (m/s)", 20, 55, 26)
            zone = st.selectbox("Zone de vent (Eurocode 1)", ["Zone 1", "Zone 2", "Zone 3", "Zone 4"])
            hauteur_batiment = st.number_input("Hauteur du bâtiment (m)", 3, 250, 24)
        pression = 0.5 * 1.225 * (vent_ref ** 2) / 1000  # kN/m² simplifié
        coeff_zone = {"Zone 1": 1.0, "Zone 2": 1.15, "Zone 3": 1.3, "Zone 4": 1.5}[zone]
        coeff_hauteur = 1 + (hauteur_batiment / 100)
        pression_calc = round(pression * coeff_zone * coeff_hauteur, 2)
        surface_panneau = round(largeur * hauteur_p, 2)
        charge_totale = round(pression_calc * surface_panneau, 2)
        st.write("")
        m1, m2, m3 = st.columns(3)
        with m1: kpi_card("chart", "Pression de vent estimée", f"{pression_calc} kN/m²", None, "flat", "teal")
        with m2: kpi_card("facade", "Surface du panneau", f"{surface_panneau} m²", None, "flat", "orange")
        with m3: kpi_card("bolt", "Charge totale estimée", f"{charge_totale} kN", None, "flat", "navy")
        st.caption("⚠ Calcul simplifié à visée indicative — le dimensionnement définitif doit être validé par un bureau d'études structure selon les Eurocodes en vigueur (EN 1991-1-4, DTU 33.1, etc.)")
        st.markdown('</div>', unsafe_allow_html=True)

    with tabs[1]:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        section_header("chart", "Vérification des charges admissibles")
        charge_admissible = st.number_input("Charge admissible du système (kN/m²)", 0.5, 10.0, 2.4, 0.1)
        charge_calculee = st.number_input("Charge calculée (kN/m²)", 0.1, 10.0, 1.8, 0.1)
        ratio = charge_calculee / charge_admissible
        fig = go.Figure(go.Bar(
            x=["Charge admissible", "Charge calculée"], y=[charge_admissible, charge_calculee],
            marker_color=["#1FBEB0", "#2E5BFF" if ratio <= 1 else "#D7443E"], width=[0.5, 0.5]))
        fig.update_layout(height=320, margin=dict(l=10, r=10, t=10, b=10), font=dict(family="Inter"))
        st.plotly_chart(fig, use_container_width=True)
        if ratio <= 0.8:
            st.markdown(badge("Conforme — marge confortable", "ok"), unsafe_allow_html=True)
        elif ratio <= 1:
            st.markdown(badge("Conforme — marge réduite", "warn"), unsafe_allow_html=True)
        else:
            st.markdown(badge("Non conforme — dépassement", "danger"), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tabs[2]:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        section_header("wrench", "Recommandation d'ancrages")
        support = st.selectbox("Type de support", ["Béton banché", "Maçonnerie creuse", "Ossature métallique", "Ossature bois"])
        reco = {
            "Béton banché": [("Cheville chimique HILTI HIT-RE 500", "12–16 mm", "≥ 8 kN"),
                              ("Ancrage mécanique à expansion", "10–14 mm", "≥ 6 kN")],
            "Maçonnerie creuse": [("Cheville chimique à tamis", "10–12 mm", "≥ 4 kN"),
                                   ("Cheville nylon renforcée", "8–10 mm", "≥ 2,5 kN")],
            "Ossature métallique": [("Vis autoperceuse inox A2", "6,3 mm", "≥ 5 kN"),
                                     ("Boulon HR classe 8.8", "10–12 mm", "≥ 9 kN")],
            "Ossature bois": [("Vis à bois structurelle", "8 mm", "≥ 3,5 kN"),
                               ("Boulon traversant + rondelle large", "10 mm", "≥ 4,5 kN")],
        }[support]
        df_reco = pd.DataFrame(reco, columns=["Ancrage recommandé", "Diamètre", "Résistance min. requise"])
        st.dataframe(df_reco, use_container_width=True, hide_index=True)
        st.caption("Recommandations génériques — se référer à la fiche technique du fabricant et à l'avis technique CSTB du système.")
        st.markdown('</div>', unsafe_allow_html=True)

    with tabs[3]:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        section_header("check", "Checklist de contrôle de conformité")
        items = [
            "Note de calcul de structure validée par le BE",
            "Conformité DTU 33.1 (façades rideaux) respectée",
            "Résistance au vent vérifiée (Eurocode 1 — EN 1991-1-4)",
            "Ancrages conformes à l'avis technique du système",
            "Étanchéité à l'air et à l'eau contrôlée",
            "Essais AEV (Air / Eau / Vent) réalisés ou planifiés",
            "Plan de calepinage validé par le client",
            "Autorisation de voirie / échafaudage obtenue",
        ]
        done = 0
        for it in items:
            c = st.checkbox(it, key=f"conf_{it}")
            if c: done += 1
        st.progress(done / len(items), text=f"Conformité : {done}/{len(items)} points validés")
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# PAGE — FACTURATION & GESTION CLIENTS
# ============================================================================
elif selected == "Facturation & clients":
    page_header("invoice", "Gestion commerciale", "Facturation & gestion clients",
                "Génération et suivi des factures, fiches clients détaillées")

    tabs = st.tabs(["Factures", "Fiches clients"])

    with tabs[0]:
        f = st.session_state.factures
        c1, c2, c3 = st.columns(3)
        with c1: kpi_card("coin", "Total facturé TTC", f"{f['Montant TTC (€)'].sum():,} €".replace(",", " "), None, "flat", "orange")
        with c2:
            impaye = f[f["Statut"] != "Payée"]["Montant TTC (€)"].sum()
            kpi_card("alert", "Impayés", f"{impaye:,} €".replace(",", " "), None, "flat", "danger")
        with c3: kpi_card("check", "Factures payées", f"{(f['Statut']=='Payée').sum()}/{len(f)}", None, "flat", "ok")

        st.write("")
        colL, colR = st.columns([1, 1.6])
        with colL:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            section_header("invoice", "Générer une facture")
            with st.form("form_facture"):
                cl = st.selectbox("Client", st.session_state.clients["Nom"])
                montant_ht = st.number_input("Montant HT (€)", min_value=0, value=15000, step=500)
                tva = round(montant_ht * 0.20)
                st.metric("Montant TTC (TVA 20%)", f"{montant_ht + tva:,} €".replace(",", " "))
                sub = st.form_submit_button("Générer la facture", type="primary", use_container_width=True)
                if sub:
                    new = pd.DataFrame([{
                        "ID": f"FA-{900+len(st.session_state.factures)}", "Client": cl,
                        "Montant HT (€)": montant_ht, "TVA (€)": tva, "Montant TTC (€)": montant_ht + tva,
                        "Statut": "En attente", "Émission": date.today().strftime("%d/%m/%Y"),
                        "Échéance": (date.today() + timedelta(days=30)).strftime("%d/%m/%Y"),
                    }])
                    st.session_state.factures = pd.concat([new, st.session_state.factures], ignore_index=True)
                    st.success("Facture générée.")
            st.markdown('</div>', unsafe_allow_html=True)
        with colR:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            section_header("doc", "Suivi des factures")
            for _, r in st.session_state.factures.iterrows():
                c = st.columns([0.9, 1.7, 1.2, 1.2, 1.1])
                c[0].markdown(f"**{r['ID']}**")
                c[1].write(r["Client"])
                c[2].markdown(f'<span class="mono">{r["Montant TTC (€)"]:,} €</span>'.replace(",", " "), unsafe_allow_html=True)
                c[3].markdown(f'<span class="mono">éch. {r["Échéance"]}</span>', unsafe_allow_html=True)
                c[4].markdown(badge(r["Statut"], STATUT_MAP_FACTURE[r["Statut"]]), unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    with tabs[1]:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        section_header("client", "Fiches clients")
        choix = st.selectbox("Sélectionner un client", st.session_state.clients["Nom"])
        cl = st.session_state.clients[st.session_state.clients["Nom"] == choix].iloc[0]
        c1, c2, c3 = st.columns(3)
        with c1: kpi_card("client", "Type de client", cl["Type"], None, "flat", "navy")
        with c2: kpi_card("coin", "CA cumulé", f"{cl['CA cumulé (€)']:,} €".replace(",", " "), None, "flat", "orange")
        with c3: kpi_card("calendar", "Client depuis", str(cl["Client depuis"]), None, "flat", "teal")
        st.write("")
        d1, d2 = st.columns(2)
        d1.markdown(f"**Contact :** {cl['Contact']}  \n**Téléphone :** {cl['Téléphone']}  \n**Email :** {cl['Email']}")
        d2.markdown(f"**Ville :** {cl['Ville']}  \n**Identifiant :** {cl['ID']}")
        st.markdown("<hr class='soft'>", unsafe_allow_html=True)
        st.markdown("**Devis associés**")
        st.dataframe(st.session_state.devis[st.session_state.devis["Client"] == choix], use_container_width=True, hide_index=True)
        st.markdown("**Factures associées**")
        st.dataframe(st.session_state.factures[st.session_state.factures["Client"] == choix], use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# PAGE — DOSSIERS CLIENTS (GED)
# ============================================================================
elif selected == "Dossiers clients (GED)":
    page_header("folder", "Gestion électronique des documents", "Dossiers clients",
                "Documents, historique, devis et contrats regroupés par client")

    colL, colR = st.columns([1, 2])
    with colL:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        section_header("client", "Sélection du client")
        choix = st.selectbox("Client", st.session_state.clients["Nom"])
        up = st.file_uploader("Ajouter un document", type=["pdf", "png", "jpg", "docx", "xlsx"])
        if up is not None:
            new = pd.DataFrame([{"Client": choix, "Document": up.name, "Type": "Autre",
                                  "Ajouté le": date.today().strftime("%d/%m/%Y")}])
            st.session_state.documents = pd.concat([new, st.session_state.documents], ignore_index=True)
            st.success(f"Document « {up.name} » ajouté au dossier de {choix}.")
        st.markdown('</div>', unsafe_allow_html=True)

    with colR:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        section_header("folder", f"Dossier — {choix}")
        docs = st.session_state.documents[st.session_state.documents["Client"] == choix]
        type_icons = {"Devis": "invoice", "Contrat": "doc", "Facture": "invoice", "Plan technique": "aluminum",
                      "Photo chantier": "facade", "Autre": "doc"}
        if docs.empty:
            st.info("Aucun document pour ce client pour le moment.")
        for _, d in docs.iterrows():
            c = st.columns([0.5, 3, 1.2, 1.2])
            c[0].markdown(icon(type_icons.get(d["Type"], "doc"), 19, "#2E5BFF"), unsafe_allow_html=True)
            c[1].write(d["Document"])
            c[2].markdown(f'<span class="tag-chip">{d["Type"]}</span>', unsafe_allow_html=True)
            c[3].markdown(f'<span class="mono">{d["Ajouté le"]}</span>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        section_header("clock", "Historique du client")
        hist = []
        for _, d in st.session_state.devis[st.session_state.devis["Client"] == choix].iterrows():
            hist.append((d["Date"], f"Devis {d['ID']} — {d['Type de façade']} — {d['Montant HT (€)']:,} € HT".replace(",", " ")))
        for _, f in st.session_state.factures[st.session_state.factures["Client"] == choix].iterrows():
            hist.append((f["Émission"], f"Facture {f['ID']} — {f['Montant TTC (€)']:,} € TTC — {f['Statut']}".replace(",", " ")))
        hist.sort(key=lambda x: datetime.strptime(x[0], "%d/%m/%Y"), reverse=True)
        if not hist:
            st.info("Aucun historique disponible.")
        for dte, txt in hist:
            st.markdown(f'<span class="mono" style="color:var(--steel);">{dte}</span> &nbsp;—&nbsp; {txt}', unsafe_allow_html=True)
            st.markdown("<hr class='soft'>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# PAGE — COMPTABILITÉ
# ============================================================================
elif selected == "Comptabilité":
    page_header("chart", "Pilotage financier", "Comptabilité",
                "Tableau de bord, recettes / dépenses, marges")

    df = st.session_state.compta
    total_recettes = df["Recettes (€)"].sum()
    total_depenses = df["Dépenses (€)"].sum()
    marge_totale = df["Marge (€)"].sum()
    marge_pct = round(marge_totale / total_recettes * 100, 1)

    c1, c2, c3, c4 = st.columns(4)
    with c1: kpi_card("coin", "Recettes (12 mois)", f"{total_recettes:,} €".replace(",", " "), None, "flat", "orange")
    with c2: kpi_card("wrench", "Dépenses (12 mois)", f"{total_depenses:,} €".replace(",", " "), None, "flat", "navy")
    with c3: kpi_card("trend", "Marge nette", f"{marge_totale:,} €".replace(",", " "), f"{marge_pct}% de marge", "up", "ok")
    with c4: kpi_card("coin", "Trésorerie estimée", f"{int(marge_totale*0.8):,} €".replace(",", " "), None, "flat", "teal")

    st.write("")
    colA, colB = st.columns([1.4, 1])
    with colA:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        section_header("chart", "Évolution recettes / dépenses / marge")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df["Mois"], y=df["Recettes (€)"], name="Recettes", fill="tozeroy",
                                  line=dict(color="#2E5BFF")))
        fig.add_trace(go.Scatter(x=df["Mois"], y=df["Dépenses (€)"], name="Dépenses", fill="tozeroy",
                                  line=dict(color="#152B6B")))
        fig.add_trace(go.Scatter(x=df["Mois"], y=df["Marge (€)"], name="Marge", line=dict(color="#1FBEB0", width=3, dash="dot")))
        fig.update_layout(height=360, margin=dict(l=10, r=10, t=10, b=10), plot_bgcolor="white", paper_bgcolor="white",
                           legend=dict(orientation="h", yanchor="bottom", y=1.02), font=dict(family="Inter"))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with colB:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        section_header("chart", "Répartition par activité")
        rep = pd.DataFrame({"Activité": ["Location nacelles", "Pose façades"],
                             "CA (€)": [int(total_recettes*0.42), int(total_recettes*0.58)]})
        fig2 = px.pie(rep, names="Activité", values="CA (€)", hole=0.55,
                      color_discrete_sequence=["#2E5BFF", "#152B6B"])
        fig2.update_layout(height=360, margin=dict(l=10, r=10, t=10, b=10), font=dict(family="Inter"))
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    section_header("doc", "Détail mensuel")
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# PAGE — AUTOMATISATION
# ============================================================================
elif selected == "Automatisation":
    page_header("automation", "Gain de temps", "Automatisation",
                "Règles automatiques pour fiabiliser le suivi et libérer du temps aux équipes")

    c1, c2, c3 = st.columns(3)
    actifs = int(st.session_state.automations["Actif"].sum())
    with c1: kpi_card("automation", "Règles actives", f"{actifs}/{len(st.session_state.automations)}", None, "flat", "orange")
    with c2: kpi_card("bolt", "Actions déclenchées (30j)", "142", "+18 vs mois -1", "up", "teal")
    with c3: kpi_card("clock", "Temps estimé gagné / mois", "26 h", None, "flat", "ok")

    st.write("")
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    section_header("automation", "Règles d'automatisation")
    for i, row in st.session_state.automations.iterrows():
        c = st.columns([2.2, 2.6, 2.6, 1])
        c[0].markdown(f"**{row['Règle']}**")
        c[1].markdown(f'<span style="color:var(--steel);">Si :</span> {row["Déclencheur"]}', unsafe_allow_html=True)
        c[2].markdown(f'<span style="color:var(--steel);">Alors :</span> {row["Action"]}', unsafe_allow_html=True)
        new_val = c[3].toggle("Actif", value=bool(row["Actif"]), key=f"auto_{i}", label_visibility="collapsed")
        st.session_state.automations.at[i, "Actif"] = new_val
        st.markdown("<hr class='soft'>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    colL, colR = st.columns(2)
    with colL:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        section_header("gear", "Créer une nouvelle règle")
        with st.form("form_auto"):
            nom = st.text_input("Nom de la règle", placeholder="Ex. Alerte contrôle technique nacelle")
            decl = st.text_input("Déclencheur", placeholder="Ex. Date de contrôle technique dans 15 jours")
            action = st.text_input("Action", placeholder="Ex. Notification à l'agence + email au client")
            sub = st.form_submit_button("Créer la règle", type="primary", use_container_width=True)
            if sub and nom:
                new = pd.DataFrame([{"Règle": nom, "Déclencheur": decl, "Action": action, "Actif": True}])
                st.session_state.automations = pd.concat([st.session_state.automations, new], ignore_index=True)
                st.success("Règle créée avec succès.")
        st.markdown('</div>', unsafe_allow_html=True)
    with colR:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        section_header("shield", "Canaux de notification")
        st.checkbox("Email", value=True)
        st.checkbox("SMS", value=True)
        st.checkbox("Notification interne (application)", value=True)
        st.checkbox("WhatsApp Business", value=False)
        st.caption("Les notifications sont envoyées selon les règles actives ci-dessus.")
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# PIED DE PAGE
# ============================================================================
st.markdown("<hr class='soft'>", unsafe_allow_html=True)
st.markdown('''
    <div style="text-align:center; color:#8A97A3; font-size:0.78rem; padding:6px 0 18px 0;">
        FACADIER.SARL — L'art de la pose · Plateforme de gestion façades & nacelles élévatrices · Données de démonstration
    </div>
''', unsafe_allow_html=True)
