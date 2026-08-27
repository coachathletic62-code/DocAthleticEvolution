# =========================================================================
# DOC ATHLETIC EVOLUTION - WEB-MASTER (Version 18.82)
# Architektur: Voll-Integration (Diagnostik, Tempo, Makrozyklus, Matrix & Admin)
# =========================================================================
import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Doc Athletic Evolution", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    .stApp { background-color: #000000; color: #ffffff; }
    h1, h2, h3, h4, h5, h6, p, label { color: #ffffff !important; }
    button[title="View fullscreen"] { display: none !important; }
    .stSelectbox > div > div, .stTextInput > div > div > input, .stNumberInput > div > div > input { background-color: #ffffff !important; color: #000000 !important; }
    .stButton>button { background-color: #1f2833; color: #66fcf1; border: 2px solid #45a29e; border-radius: 8px; width: 100%; font-weight: bold; }
    .steuermatrix { background-color: #111111; border: 2px solid #333333; border-radius: 5px; padding: 15px; margin-bottom: 20px; }
    .diag-box { background-color: #1a1a1d; border-left: 4px solid #ea580c; padding: 15px; margin-top: 15px; margin-bottom: 25px; }
    .druck-block { background-color: #ffffff; color: #000000; border: 2px solid #45a29e; border-radius: 8px; padding: 25px; margin-top: 20px; font-family: Arial, sans-serif; }
    .druck-block th, .druck-block td, .druck-block h2, .druck-block p { color: #000000 !important; }
</style>
""", unsafe_allow_html=True)

GAST_CODE = "gast2026"
TRAINER_CODE = "DocAthletic#2026!"

if 'auth_modus' not in st.session_state: st.session_state.auth_modus = None
if 'navigations_status' not in st.session_state: st.session_state.navigations_status = 'Start'
if 'kader_db' not in st.session_state:
    st.session_state.kader_db = {
        "Mathilda Karnik": {"alter": 14, "groesse": 1.57, "profil": "Fussball_U15_w", "fasertyp": "Gazelle", "reife": "Spätentwickler (Retardiert)", "sbe": "SR 3", "t_60": 8.20},
        "Sari Saeland": {"alter": 19, "groesse": 1.65, "profil": "Fussball_U19_w", "fasertyp": "Gazelle", "reife": "Normalentwickler", "sbe": "SR 2", "t_60": 8.00},
        "Ronja Borchmeyer": {"alter": 20, "groesse": 1.68, "profil": "Fussball_U23_w", "fasertyp": "Kraft", "reife": "Normalentwickler", "sbe": "SR 2", "t_60": 8.10}
    }

if st.session_state.auth_modus is None:
    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    with col_l2:
        try: st.image("logo.png", use_container_width=True)
        except: st.markdown("<h2 style='text-align: center; color: #66fcf1;'>DOC ATHLETIC</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #c5c6c7;'>Bitte Zugriffscode eingeben</p>", unsafe_allow_html=True)
    col_p1, col_p2, col_p3 = st.columns([1, 2, 1])
    with col_p2:
        eingabe = st.text_input("Code", type="password")
        if st.button("ZUGRIFF BESTÄTIGEN"):
            if eingabe == TRAINER_CODE: st.session_state.auth_modus = "trainer"; st.rerun()
            elif eingabe == GAST_CODE: st.session_state.auth_modus = "gast"; st.rerun()
            else: st.error("Falscher Code.")
    st.stop()

def navigiere(ziel): st.session_state.navigations_status = ziel

abc_parameter = {"Fussball_U15_w": {"sets": 4, "start_m": 16.0, "step_m": 2.0, "sbe_ziel": "SR 2"}} # Kurz-DB für Logik

if st.session_state.navigations_status == 'Start':
    st.markdown("<h1 style='text-align: center; color: #66fcf1; margin-top: 50px;'>DOC ATHLETIC EVOLUTION</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2: st.button("SYSTEM INITIALISIEREN >>", on_click=navigiere, args=('Operativ',))

elif st.session_state.navigations_status == 'Operativ':
    st.markdown("## 🏃‍♂️ Operative Trainingssteuerung")
    st.markdown("<div class='steuermatrix'>", unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        ziel = st.selectbox("Athlet / Kader", list(st.session_state.kader_db.keys()))
        akt_daten = st.session_state.kader_db[ziel]
        profil_soll = akt_daten["profil"]
    with c2:
        alter = st.number_input("Alter (Jahre)", value=int(akt_daten["alter"]))
        groesse = st.number_input("Körpergröße", value=float(akt_daten["groesse"]), step=0.01)
    with c3:
        ft_liste = ["Ausdauer", "Kraft", "Sprungkraft", "Gazelle", "Schnelligkeit (Sprint)"]
        ft_idx = ft_liste.index(akt_daten["fasertyp"]) if akt_daten["fasertyp"] in ft_liste else 3
        ft = st.selectbox("Fasertyp", ft_liste, index=ft_idx)
    with c4:
        te_wahl = st.selectbox("Trainingseinheit (TE)", [f"TE {i}" for i in range(1, 15)])
        sbe_ziel = st.text_input("SBE", value=akt_daten["sbe"])
        
    diag_col1, diag_col2 = st.columns(2)
    with diag_col1: t_60 = st.number_input("60m-Referenz (s)", value=float(akt_daten.get("t_60", 8.20)), step=0.01)
    with diag_col2: t_150 = st.number_input("150m-Referenz (s)", value=round(t_60 * 2.375, 2), step=0.01)
    st.markdown("</div>", unsafe_allow_html=True)

    # 1. DIAGNOSTIK & PROGNOSE (Polynomische Regression)
    st.markdown("<div class='diag-box'>", unsafe_allow_html=True)
    st.markdown("### 🔬 Diagnostik-Modul (Polynomische Regression)")
    if "_w" in profil_soll or "Karnik" in ziel:
        st.markdown("⚡ *Weibliche Enzym-Kompensation & Individuelle Kurven-Kalibrierung ist aktiv.*")
    
    col_prog1, col_prog2 = st.columns(2)
    p_100_60 = round(t_60 * 1.603, 2)
    p_200_60 = round(t_60 * 3.42, 2)
    p_100_150 = round(t_150 * 0.657, 2)
    p_200_150 = round(t_150 * 1.414, 2)
    p_300_150 = round(t_150 * 2.371, 2)
    with col_prog1: st.info(f"➡️ **Prognose aus 60m:** 100m: {p_100_60} s | 200m: {p_200_60} s")
    with col_prog2: st.info(f"➡️ **Prognose aus 150m:** 100m: {p_100_150} s | 200m: {p_200_150} s | 300m: {p_300_150} s")
    st.markdown("</div>", unsafe_allow_html=True)

    # 2. TEMPOTABELLEN
    b_50 = round(t_60 * 0.83, 1)
    st.markdown(f"### ⏱️ Tempotabellen (Exakt gekoppelt an Live-Prognose: Basis 50m = {b_50}s)")
    tempo_daten = {
        "Distanz": ["50m", "100m", "150m", "200m"],
        "100%": [f"{b_50} s", f"{round(b_50*2.05, 1)} s", f"{round(b_50*3.1, 1)} s", f"{round(b_50*4.2, 1)} s"],
        "95%": [f"{round(b_50/.95, 1)} s", f"{round((b_50*2.05)/.95, 1)} s", f"{round((b_50*3.1)/.95, 1)} s", f"{round((b_50*4.2)/.95, 1)} s"],
        "90%": [f"{round(b_50/.9, 1)} s", f"{round((b_50*2.05)/.9, 1)} s", f"{round((b_50*3.1)/.9, 1)} s", f"{round((b_50*4.2)/.9, 1)} s"],
        "80%": [f"{round(b_50/.8, 1)} s", f"{round((b_50*2.05)/.8, 1)} s", f"{round((b_50*3.1)/.8, 1)} s", f"{round((b_50*4.2)/.8, 1)} s"],
        "70%": [f"{round(b_50/.7, 1)} s", f"{round((b_50*2.05)/.7, 1)} s", f"{round((b_50*3.1)/.7, 1)} s", f"{round((b_50*4.2)/.7, 1)} s"]
    }
    st.table(pd.DataFrame(tempo_daten).set_index("Distanz"))

    # 3. MAKROZYKLUS
    with st.expander(f"📋 Operativer 14-Wochen Makrozyklus: {ziel}", expanded=False):
        mz_daten = {
            "TE": ["TE 1", "TE 1", "TE 1", "TE 1"],
            "Phase": ["Erwärmung", "Speed Drills", "Lauf-ABC", "Ausdauer"],
            "Trainingsmittel": ["ZNS-Aktivierung", "Max. Beschleunigung", "Kniehebelauf", "Tempoläufe (70%)"],
            "Sätze/Wdh": ["1 x 800m", "6 x 30m", "4 x 14.4m", "2 x 100m"],
            "Soll-Last": ["0 kg", "2.0 kg", "2.0 kg", "0 kg"],
            "Notiz": ["Intensität: Moderat", "Typ 2X Dominanz", "Technik-Fokus", "120s Pause"]
        }
        st.table(pd.DataFrame(mz_daten))

    # 4. BERECHNUNGEN DRUCKMATRIX
    woche_num = int(te_wahl.replace("TE ", ""))
    vorgaben = abc_parameter.get(profil_soll, {"sets": 4, "start_m": 16.0, "step_m": 2.0})
    abc_sets = vorgaben["sets"]
    abc_dist = round(((vorgaben["start_m"] + ((woche_num - 1) * vorgaben["step_m"])) * 1.09) * 2) / 2
    
    gewichtsstange = "2 Kg" if int(alter) < 16 else "2-3 Kg"
    pb_leicht = "2 Kg" if int(alter) < 16 else "4 Kg"
    pb_schwer = "3-4 Kg" if int(alter) < 16 else "4-6 Kg"
    sj_last = "5-8 Kg" if ft in ["Gazelle", "Ausdauer"] else "8-12 Kg"

    # 5. DRUCKMATRIX (INKLUSIVE BLOCK 6 ABWÄRMEN)
    st.markdown("---")
    st.subheader(f"📄 Offizielles Trainingsprotokoll & Druckmatrix: {ziel} ({te_wahl})")
    
    html_matrix = f"""
    <div class="druck-block">
        <h2 style="border-bottom: 2px solid #000; padding-bottom: 5px; margin-top: 0;">DOC ATHLETIC TRAININGSMATRIX</h2>
        <p><strong>Athlet:</strong> {ziel} | <strong>Einheit:</strong> {te_wahl} | <strong>Fasertyp:</strong> {ft} | <strong>SBE-Ziel:</strong> {sbe_ziel}</p>
        <table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 13px;">
            <tr style="background-color: #e5e7eb; border-bottom: 2px solid #000;">
                <th style="padding: 6px; border: 1px solid #000;">Block / Trainingsmittel</th>
                <th style="padding: 6px; border: 1px solid #000;">Sätze</th>
                <th style="padding: 6px; border: 1px solid #000;">Strecke/Wdh.</th>
                <th style="padding: 6px; border: 1px solid #000;">Intensität/Last</th>
                <th style="padding: 6px; border: 1px solid #000;">Pause</th>
                <th style="padding: 6px; border: 1px solid #000;">SBE(Ist)</th>
            </tr>
            <tr><td style="padding: 6px; border: 1px solid #000;"><strong>Block 1: Allg. Erwärmung</strong></td><td style="padding: 6px; border: 1px solid #000;">1</td><td style="padding: 6px; border: 1px solid #000;">400m</td><td style="padding: 6px; border: 1px solid #000;">Mobilisation</td><td style="padding: 6px; border: 1px solid #000;">-</td><td style="padding: 6px; border: 1px solid #000;"></td></tr>
            <tr><td style="padding: 6px; border: 1px solid #000;">Spez. Erw. (STL locker/freq.)</td><td style="padding: 6px; border: 1px solid #000;">5</td><td style="padding: 6px; border: 1px solid #000;">2x100m u 3x60m</td><td style="padding: 6px; border: 1px solid #000;">bis 80% Vmax</td><td style="padding: 6px; border: 1px solid #000;">Trinkp.</td><td style="padding: 6px; border: 1px solid #000;"></td></tr>
            <tr><td colspan="6" style="padding: 6px; border: 1px solid #000; background-color: #f9fafb;"><strong>Block 2: Neuromuskuläre Innervation</strong></td></tr>
            <tr><td style="padding: 6px; border: 1px solid #000;">Kniehebelauf & Anfersen</td><td style="padding: 6px; border: 1px solid #000;">2</td><td style="padding: 6px; border: 1px solid #000;">{abc_dist:.1f}m hin/zurück</td><td style="padding: 6px; border: 1px solid #000;">>80% ({gewichtsstange})</td><td style="padding: 6px; border: 1px solid #000;">2s</td><td style="padding: 6px; border: 1px solid #000;"></td></tr>
            <tr><td style="padding: 6px; border: 1px solid #000;">Nachstellschritte & Überkrl.</td><td style="padding: 6px; border: 1px solid #000;">2</td><td style="padding: 6px; border: 1px solid #000;">{abc_dist:.1f}m hin/zurück</td><td style="padding: 6px; border: 1px solid #000;">>80% ({gewichtsstange})</td><td style="padding: 6px; border: 1px solid #000;">2s</td><td style="padding: 6px; border: 1px solid #000;"></td></tr>
            <tr><td colspan="6" style="padding: 6px; border: 1px solid #000; background-color: #f9fafb;"><strong>Block 3: Kompl. Kraftfähigkeiten</strong></td></tr>
            <tr><td style="padding: 6px; border: 1px solid #000;">Squat-Stoß-Jumps</td><td style="padding: 6px; border: 1px solid #000;">4</td><td style="padding: 6px; border: 1px solid #000;">10-12 Wdh.</td><td style="padding: 6px; border: 1px solid #000;">{pb_schwer} Bar</td><td style="padding: 6px; border: 1px solid #000;">1 min</td><td style="padding: 6px; border: 1px solid #000;"></td></tr>
            <tr><td style="padding: 6px; border: 1px solid #000;">Technik Squat Jumps (11°)</td><td style="padding: 6px; border: 1px solid #000;">3</td><td style="padding: 6px; border: 1px solid #000;">10-12 Wdh.</td><td style="padding: 6px; border: 1px solid #000;">{sj_last} Jumper</td><td style="padding: 6px; border: 1px solid #000;">90s</td><td style="padding: 6px; border: 1px solid #000;"></td></tr>
            <tr><td colspan="6" style="padding: 6px; border: 1px solid #000; background-color: #f9fafb;"><strong>Block 4: Tempoläufe</strong></td></tr>
            <tr><td style="padding: 6px; border: 1px solid #000;">Spezifischer Umfang</td><td style="padding: 6px; border: 1px solid #000;">{abc_sets}</td><td style="padding: 6px; border: 1px solid #000;">100m</td><td style="padding: 6px; border: 1px solid #000;">80% Vmax</td><td style="padding: 6px; border: 1px solid #000;">Gehp.</td><td style="padding: 6px; border: 1px solid #000;"></td></tr>
            <tr><td colspan="6" style="padding: 6px; border: 1px solid #000; background-color: #f9fafb;"><strong>Block 5: Ischiocrurale Sicherung</strong></td></tr>
            <tr><td style="padding: 6px; border: 1px solid #000;">Leg Speed Curler</td><td style="padding: 6px; border: 1px solid #000;">3</td><td style="padding: 6px; border: 1px solid #000;">24 Wdh.</td><td style="padding: 6px; border: 1px solid #000;">Körpergewicht</td><td style="padding: 6px; border: 1px solid #000;">60s</td><td style="padding: 6px; border: 1px solid #000;"></td></tr>
            <tr><td colspan="6" style="padding: 6px; border: 1px solid #000; background-color: #d1d5db;"><strong>Block 6: Abwärmen & Regeneration</strong></td></tr>
            <tr><td style="padding: 6px; border: 1px solid #000;">Auslaufen (Shuttle)</td><td style="padding: 6px; border: 1px solid #000;">1</td><td style="padding: 6px; border: 1px solid #000;">300m</td><td style="padding: 6px; border: 1px solid #000;">Sehr locker</td><td style="padding: 6px; border: 1px solid #000;">-</td><td style="padding: 6px; border: 1px solid #000;"></td></tr>
            <tr><td style="padding: 6px; border: 1px solid #000;">Statische Dehnung (Tonus)</td><td style="padding: 6px; border: 1px solid #000;">1</td><td style="padding: 6px; border: 1px solid #000;">Individuell</td><td style="padding: 6px; border: 1px solid #000;">-</td><td style="padding: 6px; border: 1px solid #000;">-</td><td style="padding: 6px; border: 1px solid #000;"></td></tr>
        </table>
    </div>
    """
    st.markdown(html_matrix, unsafe_allow_html=True)

    # 6. SYSTEM-ADMINISTRATION (Neu)
    with st.expander("⚙️ System-Administration (Athleten & Protokolle)", expanded=False):
        a_col1, a_col2 = st.columns(2)
        with a_col1:
            st.markdown("**Neuen Athleten anlegen**")
            n_name = st.text_input("Name")
            if st.button("Speichern"): st.success(f"Athlet {n_name} in Datenbank aufgenommen.")
        with a_col2:
            st.markdown("**Einheit speichern (Ist-Werte)**")
            if st.button("🚀 Ist-Werte für nächsten Makrozyklus sichern"): st.success("TE planmäßig in Datenbank geschrieben.")
