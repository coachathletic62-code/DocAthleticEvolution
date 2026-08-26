# =========================================================================
# DOC ATHLETIC EVOLUTION - STREAMLIT WEB-MASTER (Synthese v18.30)
# Visuelles Web-Design (Schwarz/Ellipsen) + Backend-Logik (v18.26) + Diagnostik (v18.28)
# =========================================================================
import streamlit as st
import pandas as pd
import math

# 1. VISUELLE ARCHITEKTUR & GRUNDEINSTELLUNGEN
st.set_page_config(page_title="Doc Athletic Evolution", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    .stApp {
        background-color: #0b0c10;
        color: #c5c6c7;
    }
    h1, h2, h3, h4, h5, h6, p, div, span, label, th, td {
        color: #c5c6c7 !important;
    }
    .stButton>button {
        background-color: #1f2833;
        color: #66fcf1;
        border: 2px solid #45a29e;
        border-radius: 8px;
        width: 100%;
        font-weight: bold;
    }
    .ellipse-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 350px;
        margin-top: 50px;
    }
    .ellipse {
        width: 400px;
        height: 200px;
        background: transparent;
        border: 4px solid #66fcf1;
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 36px;
        font-weight: bold;
        color: #66fcf1;
        box-shadow: 0 0 25px #45a29e;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
</style>
""", unsafe_allow_html=True)

# 2. SYSTEM-NAVIGATION (3-Stufig)
if 'navigations_status' not in st.session_state:
    st.session_state.navigations_status = 'Start'

def navigiere(ziel):
    st.session_state.navigations_status = ziel

# 3. KADER-DATENBANK & PARAMETER (Aus Version 18.26)
kader = {
    "Matilda Karnik": {"alter": 14, "profil": "Fussball_U15_w", "fasertyp": "Schnelligkeit (Sprint)", "reife": "Normalentwickler"},
    "Ronja Borchmeyer": {"alter": 15, "profil": "Fussball_U17_w", "fasertyp": "Sprungkraft", "reife": "Normalentwickler"},
    "Aimie": {"alter": 16, "profil": "Fussball_U17_w", "fasertyp": "Kraft", "reife": "Frühentwickler"}
}

abc_parameter = {
    "Fussball_U11": {"sets": 3, "start_m": 12.0, "step_m": 2.0, "sbe_ziel": "SR 3"},
    "Fussball_U13": {"sets": 4, "start_m": 15.0, "step_m": 2.5, "sbe_ziel": "SR 2-3"},
    "Fussball_U15_m": {"sets": 4, "start_m": 18.0, "step_m": 2.5, "sbe_ziel": "SR 2"},
    "Fussball_U15_w": {"sets": 4, "start_m": 16.0, "step_m": 2.0, "sbe_ziel": "SR 2"},
    "Fussball_U17_m": {"sets": 5, "start_m": 22.0, "step_m": 3.0, "sbe_ziel": "SR 1-2"},
    "Fussball_U17_w": {"sets": 5, "start_m": 20.0, "step_m": 2.5, "sbe_ziel": "SR 1-2"},
    "Fussball_U19_m": {"sets": 5, "start_m": 25.0, "step_m": 3.0, "sbe_ziel": "SR 1"},
    "Fussball_U19_w": {"sets": 5, "start_m": 22.0, "step_m": 2.5, "sbe_ziel": "SR 1"},
    "Fussball_U23_m": {"sets": 6, "start_m": 28.0, "step_m": 3.0, "sbe_ziel": "SR 1-0"},
    "Fussball_U23_w": {"sets": 6, "start_m": 25.0, "step_m": 2.5, "sbe_ziel": "SR 1-0"},
    "Basketball_U17_m": {"sets": 5, "start_m": 20.0, "step_m": 3.0, "sbe_ziel": "SR 2"},
    "Basketball_U17_w": {"sets": 5, "start_m": 18.0, "step_m": 2.5, "sbe_ziel": "SR 2"},
    "Leichtathletik_U17_m": {"sets": 5, "start_m": 25.0, "step_m": 3.5, "sbe_ziel": "SR 1-2"},
    "Leichtathletik_U17_w": {"sets": 5, "start_m": 22.0, "step_m": 3.0, "sbe_ziel": "SR 1-2"},
    "Skispringen_U20": {"sets": 5, "start_m": 22.0, "step_m": 3.0, "sbe_ziel": "SR 1"}
}

def ermittle_basis_50m(profil, ft, reife):
    if "U11" in profil: basis = 7.7 if "_m" in profil else 8.2
    elif "U13" in profil: basis = 7.1 if "_m" in profil else 7.6
    elif "U15_m" in profil: basis = 6.2
    elif "U15_w" in profil: basis = 7.0
    elif "U17_m" in profil: basis = 5.8
    elif "U17_w" in profil: basis = 6.8
    elif "U19_m" in profil or "U23_m" in profil: basis = 5.5
    elif "U19_w" in profil or "U23_w" in profil: basis = 6.6
    elif "Basketball" in profil: basis = 6.0 if "_m" in profil else 6.6
    elif "Leichtathletik" in profil: basis = 5.6 if "_m" in profil else 6.3
    else: basis = 6.6

    if ft == "Schnelligkeit (Sprint)": basis -= 0.2
    elif ft in ["Sprungkraft", "Gazelle"]: basis -= 0.1
    elif ft == "Kraft": basis += 0.1
    elif ft == "Ausdauer": basis += 0.3

    if reife == "Spätentwickler": basis += 0.4
    elif reife == "Frühentwickler": basis -= 0.3
    return round(basis, 2)

# =========================================================================
# EBENE 1: STARTBILDSCHIRM (Mit CSS-Ellipsen Logo)
# =========================================================================
if st.session_state.navigations_status == 'Start':
    st.markdown("<h1 style='text-align: center; color: #66fcf1 !important; margin-top: 20px;'>DOC ATHLETIC EVOLUTION</h1>", unsafe_allow_html=True)
    st.markdown("<div class='ellipse-container'><div class='ellipse'>Train Smart</div></div>", unsafe_allow_html=True)
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.button("SYSTEM INITIALISIEREN >>", on_click=navigiere, args=('Uebersicht',))

# =========================================================================
# EBENE 2: SYSTEMÜBERSICHT
# =========================================================================
elif st.session_state.navigations_status == 'Uebersicht':
    st.title("Systemübersicht & Status")
    st.markdown("---")
    st.markdown("### Modul-Checkliste:")
    st.write("✅ **Visuelle Architektur:** Geladen (Schwarzer Untergrund & CSS-Ellipsen aktiv)")
    st.write("✅ **Biometrische Datenbank:** Verbunden")
    st.write("✅ **Diagnostik-Prozessor:** Polynomische Regression (v18.28) aktiv")
    st.write("✅ **Makrozyklus-Generator:** Vollständige 14-Wochen-Logik (v18.26) aktiv")
    st.write("✅ **Tempotabellen:** Biometrisch gekoppelt")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.button("<< ZURÜCK", on_click=navigiere, args=('Start',))
    with col2:
        st.button("OPERATIVES MENÜ STARTEN >>", on_click=navigiere, args=('Operativ',))

# =========================================================================
# EBENE 3: OPERATIVES MENÜ
# =========================================================================
elif st.session_state.navigations_status == 'Operativ':
    st.button("<< ZUR ÜBERSICHT", on_click=navigiere, args=('Uebersicht',))
    st.title("🏃‍♂️ Operative Trainingssteuerung")
    st.markdown("---")

    # SEITENLEISTE
    st.sidebar.header("⚙️ Biometrische Live-Steuerung")
    ziel = st.sidebar.selectbox("Athlet/in wählen", list(kader.keys()) + list(abc_parameter.keys()))
    
    if ziel in kader:
        profil = kader[ziel]["profil"]
        ft_liste = ["Ausdauer", "Kraft", "Sprungkraft", "Gazelle", "Schnelligkeit (Sprint)"]
        ft = st.sidebar.selectbox("Fasertyp", ft_liste, index=ft_liste.index(kader[ziel]["fasertyp"]))
        reife_liste = ["Spätentwickler", "Normalentwickler", "Frühentwickler"]
        reife = st.sidebar.selectbox("Reife-Status", reife_liste, index=reife_liste.index(kader[ziel]["reife"]))
    else:
        profil = ziel
        ft = st.sidebar.selectbox("Fasertyp", ["Ausdauer", "Kraft", "Sprungkraft", "Gazelle", "Schnelligkeit (Sprint)"])
        reife = st.sidebar.selectbox("Reife-Status", ["Spätentwickler", "Normalentwickler", "Frühentwickler"])
    
    te_wahl = st.sidebar.selectbox("Trainingseinheit (TE)", ["Alle TEs (1-14)"] + [f"TE {i}" for i in range(1, 15)])
    vorgaben = abc_parameter.get(profil, {"sets": 4, "start_m": 16.0, "step_m": 2.0, "sbe_ziel": "SR 2"})
    sbe_ziel = st.sidebar.text_input("SBE (Saubere Reserve)", vorgaben["sbe_ziel"])

    basis_50m = ermittle_basis_50m(profil, ft, reife)

    # DIAGNOSTIK (v18.28)
    st.subheader("🔬 Diagnostik-Modul (Polynomische Regression)")
    komp_100 = 0.975 if "_m" in profil else 1.0  
    komp_200 = 0.968 if "_m" in profil else 1.0  
    komp_300 = 0.963 if "_m" in profil else 1.0  
    if "_m" in profil: st.info("⚡ Männliche Enzym-Kompensation aktiv.")
        
    diag_col1, diag_col2 = st.columns(2)
    with diag_col1:
        t_60 = st.number_input("60m-Referenz (s)", min_value=6.0, max_value=15.0, value=8.13, step=0.01)
        if t_60 > 0:
            prog_100 = (7.3829 - (0.4319 * t_60) + (0.1394 * (t_60**2))) * komp_100
            prog_200 = (13.7955 - (0.7205 * t_60) + (0.2806 * (t_60**2))) * komp_200
            st.write(f"➡️ Prognose 100m: **{prog_100:.2f} s** | 200m: **{prog_200:.2f} s**")
    with diag_col2:
        t_150 = st.number_input("150m-Referenz (s)", min_value=15.0, max_value=30.0, value=17.80, step=0.01)
        if t_150 > 0:
            p_100 = (-2.4964 + (0.9996 * t_150) - (0.0103 * (t_150**2))) * komp_100
            p_200 = (12.5421 - (0.0950 * t_150) + (0.0413 * (t_150**2))) * komp_200
            p_300 = (-7.8060 + (2.6981 * t_150) - (0.0031 * (t_150**2))) * komp_300
            st.write(f"➡️ Prognose 100m: **{p_100:.2f} s** | 200m: **{p_200:.2f} s** | 300m: **{p_300:.2f} s**")

    st.markdown("---")

    # TEMPOTABELLEN (Logik aus v18.26)
    st.subheader(f"⏱ Tempotabellen (Biometrisch gekoppelt: {basis_50m}s)")
    def format_time(seconds):
        if seconds >= 60:
            m = int(seconds // 60)
            s = seconds % 60
            return f"{m}:{s:04.1f} min"
        return f"{seconds:.1f} s"

    tempo_data = []
    for dist_m in [50, 100, 150, 200]:
        base_s = basis_50m * (dist_m / 50.0)
        row = {"Distanz": f"{dist_m}m", "100%": format_time(base_s), "95%": format_time(base_s/0.95), "90%": format_time(base_s/0.90), "80%": format_time(base_s/0.80), "70%": format_time(base_s/0.70)}
        tempo_data.append(row)
    st.table(tempo_data)

    st.markdown("---")

    # TRAININGSPLAN GENERIERUNG (Logik v18.26)
    st.subheader(f"📋 Operatives Trainingsprotokoll: {ziel}")
    
    # Lastberechnung
    def calc_last(base_str, is_gross):
        if reife == "Spätentwickler":
            return f"Reduziert (-30%)" if is_gross else f"Reduziert (-20%)"
        elif reife == "Frühentwickler":
            return f"Erhöht (+15%)"
        return base_str

    if ziel == "Aimie": basis_last = "12-16 kg"
    elif "U11" in profil: basis_last = "0-1 kg"
    elif "U13" in profil: basis_last = "2-3 kg"
    elif "U15_w" in profil: basis_last = "3-5 kg"
    elif "U15_m" in profil: basis_last = "4-6 kg"
    elif "U17_w" in profil: basis_last = "5-8 kg"
    else: basis_last = "10-12 kg"
    basis_last = calc_last(basis_last, True)

    if "U11" in profil or "U13" in profil: stangen_gewicht = "1.5 kg"
    elif "U15" in profil: stangen_gewicht = "2.0 kg"
    else: stangen_gewicht = "3.0 kg"
    stangen_gewicht = calc_last(stangen_gewicht, False)

    is_skisprung = "Skispringen" in profil
    abc_sets = vorgaben["sets"]
    
    te_liste = range(1, 15) if "Alle" in te_wahl else [int(te_wahl.replace("TE ", ""))]
    protokoll = []

    for woche in te_liste:
        abc_dist = vorgaben["start_m"] + ((woche - 1) * vorgaben["step_m"])
        
        if ft == "Ausdauer":
            abc_dist *= 1.20
            erw_text, sprint_text, sprint_satz, ausdauer_satz = "Erweiterte Shuttle-Aktivierung", "Erhalt-Sprints", "6 x 30m (60s Pause)", "5 x 150m (70% / 90s Pause)"
            f_notiz = "ST-Dominanz: Laktattoleranz"
        elif ft == "Schnelligkeit (Sprint)":
            abc_dist *= 0.90
            erw_text, sprint_text, sprint_satz, ausdauer_satz = "ZNS-Aktivierung (Gepard)", "Max. Beschleunigung", "6 x 30m (180s Pause)", "2 x 100m (80% / 180s Pause)"
            f_notiz = "Typ 2X/2XX Dominanz: Max. RFD"
        elif ft in ["Sprungkraft", "Gazelle"]:
            erw_text, sprint_text, sprint_satz, ausdauer_satz = "Reaktiv-Aktivierung", "Fliegender Sprint", "5 x 40m (120s Pause)", "4 x 100m (75% / 120s Pause)"
            f_notiz = "Elastische Speicherfähigkeit"
        else:
            abc_dist *= 0.95
            erw_text, sprint_text, sprint_satz, ausdauer_satz = "Kraft-Mobilisation", "Beschleunigung gegen Last", "4 x 40m (150s Pause)", "4 x 100m (70% / 150s Pause)"
            f_notiz = "Typ 2A Dominanz: Mech. Last"

        stange_last = stangen_gewicht if woche <= 6 else "0 kg"
        stange_notiz = f"Stange über Kopf | {f_notiz}" if woche <= 6 else f"Ohne Zusatzlast | {f_notiz}"

        # Standard-Blöcke
        protokoll.append({"TE": f"TE {woche}", "Phase": "Erwärmung", "Trainingsmittel": erw_text, "Sätze/Wdh": "1 x 800m", "Soll-Last": "0 kg", "SBE": sbe_ziel, "Notiz": "Intensität: Moderat"})
        protokoll.append({"TE": f"TE {woche}", "Phase": "Speed Drills", "Trainingsmittel": sprint_text, "Sätze/Wdh": sprint_satz, "Soll-Last": stange_last, "SBE": sbe_ziel, "Notiz": stange_notiz})
        protokoll.append({"TE": f"TE {woche}", "Phase": "Lauf-ABC", "Trainingsmittel": "Kniehebe, Anfersen", "Sätze/Wdh": f"{abc_sets} x {abc_dist:.1f} m", "Soll-Last": stange_last, "SBE": sbe_ziel, "Notiz": "Technik-Fokus"})

        if is_skisprung:
            if woche <= 4:
                protokoll.append({"TE": f"TE {woche}", "Phase": "Spezifisch", "Trainingsmittel": "Speed Master", "Sätze/Wdh": "3 x 8 Jumps", "Soll-Last": "+ 10% KG", "SBE": sbe_ziel, "Notiz": "Fokus: Max. RFD"})
            elif woche == 14:
                protokoll.append({"TE": f"TE {woche}", "Phase": "DIAGNOSTIK", "Trainingsmittel": "Maximal-Test (1RM)", "Sätze/Wdh": "1RM", "Soll-Last": "Max", "SBE": "SR 0", "Notiz": "Telemark-Tiefsprünge"})
        else:
            if woche in [1, 2]:
                protokoll.append({"TE": f"TE {woche}", "Phase": "Ausdauer", "Trainingsmittel": "Tempoläufe (70%)", "Sätze/Wdh": ausdauer_satz, "Soll-Last": "0 kg", "SBE": sbe_ziel, "Notiz": "120-180s Gehpause"})
                protokoll.append({"TE": f"TE {woche}", "Phase": "Zirkel", "Trainingsmittel": "Squat-Stoß-Jumps", "Sätze/Wdh": "3 x 12 Wdh.", "Soll-Last": basis_last, "SBE": sbe_ziel, "Notiz": "Fokus saubere Umkehrphase"})
            elif woche in [3, 4]:
                protokoll.append({"TE": f"TE {woche}", "Phase": "Ausdauer", "Trainingsmittel": "Tempoläufe (75%)", "Sätze/Wdh": ausdauer_satz, "Soll-Last": "0 kg", "SBE": sbe_ziel, "Notiz": "120-180s Gehpause"})
                protokoll.append({"TE": f"TE {woche}", "Phase": "Zirkel", "Trainingsmittel": "TRX-Zug & Standstoßen", "Sätze/Wdh": "3 x 12 Wdh.", "Soll-Last": basis_last, "SBE": sbe_ziel, "Notiz": "Explosiv"})
            elif woche in [5, 6, 7]:
                protokoll.append({"TE": f"TE {woche}", "Phase": "Ausdauer", "Trainingsmittel": "Tempoläufe (75%)", "Sätze/Wdh": ausdauer_satz, "Soll-Last": "0 kg", "SBE": sbe_ziel, "Notiz": "Stoffwechselaktivierung"})
                protokoll.append({"TE": f"TE {woche}", "Phase": "Zirkel", "Trainingsmittel": "Front-Squat Jumps", "Sätze/Wdh": "3 x 12 Wdh.", "Soll-Last": basis_last, "SBE": sbe_ziel, "Notiz": "Transformation"})
            elif woche in [10, 11]:
                protokoll.append({"TE": f"TE {woche}", "Phase": "Zirkel", "Trainingsmittel": "Front-Squat Jumps (Speed)", "Sätze/Wdh": "2 x 8 Wdh.", "Soll-Last": basis_last, "SBE": "SR 1-0", "Notiz": "Volumenreduktion, ZL erhöht"})
            elif woche == 14:
                protokoll.append({"TE": f"TE {woche}", "Phase": "DIAGNOSTIK", "Trainingsmittel": "300m Parcours", "Sätze/Wdh": "Soll-Werte", "Soll-Last": "0 kg", "SBE": "SR 0", "Notiz": "Werte für nächste Periode"})

    st.dataframe(pd.DataFrame(protokoll), use_container_width=True, hide_index=True)
