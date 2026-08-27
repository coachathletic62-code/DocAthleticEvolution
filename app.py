# =========================================================================
# DOC ATHLETIC EVOLUTION - WEB-MASTER (Version 18.76 + Matrix-Upgrade)
# Architektur: 3-Stufig | Engine: Login, Kader, Diagnostik & Matrix-Druck
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
    
    .stSelectbox > div > div, .stTextInput > div > div > input, .stNumberInput > div > div > input {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    .stButton>button {
        background-color: #1f2833; color: #66fcf1;
        border: 2px solid #45a29e; border-radius: 8px;
        width: 100%; font-weight: bold;
    }
    .stDownloadButton > button {
        background-color: #1f2833 !important;
        color: #ffffff !important;
        font-weight: 900 !important;
        font-size: 15px !important;
        border: 3px solid #66fcf1 !important;
        border-radius: 8px !important;
        width: 100% !important;
        padding: 12px !important;
    }
    .steuermatrix {
        background-color: #111111; border: 2px solid #333333;
        border-radius: 5px; padding: 15px; margin-bottom: 20px;
    }
    .philosophie-box {
        background-color: #0b0c10; border-left: 4px solid #66fcf1;
        padding: 12px; margin-top: 10px; margin-bottom: 15px; font-size: 13px; color: #c5c6c7;
    }
    .druck-block {
        background-color: #ffffff; color: #000000; border: 2px solid #45a29e;
        border-radius: 8px; padding: 25px; margin-top: 20px; margin-bottom: 20px;
        font-family: Arial, sans-serif;
    }
    .druck-block h2, .druck-block h3, .druck-block h4, .druck-block p, .druck-block li, .druck-block th, .druck-block td, .druck-block strong {
        color: #000000 !important;
    }
    .footer-box {
        text-align: center; border: 2px solid #66fcf1; border-radius: 10px;
        padding: 25px; margin-top: 40px; margin-bottom: 20px; background-color: #0b0c10;
    }
</style>
""", unsafe_allow_html=True)

GAST_CODE = "gast2026"
TRAINER_CODE = "DocAthletic#2026!"

if 'auth_modus' not in st.session_state:
    st.session_state.auth_modus = None

if st.session_state.auth_modus is None:
    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    with col_l2:
        try:
            st.image("logo.png", use_container_width=True)
        except:
            st.markdown("<h2 style='text-align: center; color: #66fcf1;'>DOC ATHLETIC</h2>", unsafe_allow_html=True)
            
    st.markdown("<p style='text-align: center; color: #c5c6c7; margin-top: 20px;'>Bitte individuellen Zugriffscode eingeben</p>", unsafe_allow_html=True)
    
    col_p1, col_p2, col_p3 = st.columns([1, 2, 1])
    with col_p2:
        eingabe_code = st.text_input("Zugriffscode", type="password")
        if st.button("ZUGRIFF BESTÄTIGEN"):
            if eingabe_code == TRAINER_CODE:
                st.session_state.auth_modus = "trainer"
                st.rerun()
            elif eingabe_code == GAST_CODE:
                st.session_state.auth_modus = "gast"
                st.rerun()
            else:
                st.error("Ungültiger Code. Bitte prüfen.")
    st.stop()

if 'navigations_status' not in st.session_state:
    st.session_state.navigations_status = 'Start'

if 'kader_db' not in st.session_state:
    st.session_state.kader_db = {
        "Mathilda Karnik": {"alter": 14, "groesse": 1.57, "profil": "Fussball_U15_w", "fasertyp": "Gazelle", "reife": "Spätentwickler (Retardiert)", "sbe": "SR 3", "t_60": 8.20},
        "Sari Saeland": {"alter": 19, "groesse": 1.65, "profil": "Fussball_U19_w", "fasertyp": "Gazelle", "reife": "Normalentwickler", "sbe": "SR 2", "t_60": 8.00},
        "Ronja Borchmeyer": {"alter": 20, "groesse": 1.68, "profil": "Fussball_U23_w", "fasertyp": "Kraft", "reife": "Normalentwickler", "sbe": "SR 2", "t_60": 8.10},
        "Svenja Poock": {"alter": 20, "groesse": 1.68, "profil": "Fussball_U23_w", "fasertyp": "Kraft", "reife": "Normalentwickler", "sbe": "SR 2", "t_60": 8.30},
        "Nora Giannori": {"alter": 22, "groesse": 1.70, "profil": "Fussball_U23_w", "fasertyp": "Ausdauer", "reife": "Normalentwickler", "sbe": "SR 2", "t_60": 8.40},
        "Mieke Schiemann": {"alter": 24, "groesse": 1.72, "profil": "Fussball_U23_w", "fasertyp": "Ausdauer", "reife": "Normalentwickler", "sbe": "SR 2", "t_60": 8.50},
        "Christoffer Danders": {"alter": 19, "groesse": 1.78, "profil": "Fussball_U19_m", "fasertyp": "Schnelligkeit (Sprint)", "reife": "Normalentwickler", "sbe": "SR 1", "t_60": 7.60},
        "Matthias Mattusch": {"alter": 14, "groesse": 1.70, "profil": "Fussball_U15_m", "fasertyp": "Schnelligkeit (Sprint)", "reife": "Normalentwickler", "sbe": "SR 2", "t_60": 7.30},
        "Fred Lohmann": {"alter": 19, "groesse": 1.82, "profil": "Leichtathletik_U17_m", "fasertyp": "Schnelligkeit (Sprint)", "reife": "Normalentwickler", "sbe": "SR 1", "t_60": 7.00},
        "Franziska Nimmich": {"alter": 13, "groesse": 1.71, "profil": "Leichtathletik_U14", "fasertyp": "Schnelligkeit (Sprint)", "reife": "Frühentwickler (Akzeleriert)", "sbe": "SR 1", "t_60": 7.90}
    }

if 'ist_protokoll' not in st.session_state:
    st.session_state.ist_protokoll = {}

if 'te_anpassungen' not in st.session_state:
    st.session_state.te_anpassungen = {}

def navigiere(ziel):
    st.session_state.navigations_status = ziel

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
    "Leichtathletik_U14": {"sets": 4, "start_m": 15.0, "step_m": 2.0, "sbe_ziel": "SR 2-3"},
    "Leichtathletik_U15": {"sets": 4, "start_m": 18.0, "step_m": 2.5, "sbe_ziel": "SR 2"},
    "Leichtathletik_U17_m": {"sets": 5, "start_m": 25.0, "step_m": 3.5, "sbe_ziel": "SR 1-2"},
    "Leichtathletik_U17_w": {"sets": 5, "start_m": 22.0, "step_m": 3.0, "sbe_ziel": "SR 1-2"},
    "Skispringen_U20": {"sets": 5, "start_m": 22.0, "step_m": 3.0, "sbe_ziel": "SR 1"},
    "Hochleistung_m": {"sets": 6, "start_m": 30.0, "step_m": 3.0, "sbe_ziel": "SR 0"},
    "Hochleistung_w": {"sets": 6, "start_m": 28.0, "step_m": 3.0, "sbe_ziel": "SR 0"}
}

if st.session_state.auth_modus == "gast":
    st.sidebar.warning("🔒 GAST-MODUS (Nur Leserechte)")

if st.session_state.navigations_status == 'Start':
    st.markdown("<h1 style='text-align: center; color: #66fcf1 !important; margin-top: 50px;'>DOC ATHLETIC EVOLUTION</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        try:
            st.image("logo.png", use_container_width=True)
        except:
            st.markdown("<div style='text-align: center; border: 1px solid #ea580c; padding: 20px;'>[logo.png] konnte auf GitHub nicht gefunden werden.</div>", unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        st.button("SYSTEM INITIALISIEREN >>", on_click=navigiere, args=('Uebersicht',))

elif st.session_state.navigations_status == 'Uebersicht':
    st.title("Systemübersicht & Athleten-Datenbank")
    st.markdown("## Komplex-Training im Nachwuchs bis Hochleistungssport")
    st.markdown("---")
    
    uebersicht_datei = None
    for datei in os.listdir("."):
        if datei.lower() in ["übersicht.png", "übersicht.jpg", "uebersicht.png", "uebersicht.jpg"]:
            uebersicht_datei = datei
            break
            
    if uebersicht_datei:
        st.image(uebersicht_datei, use_container_width=True)
    else:
        st.markdown("<div style='text-align: center; border: 1px dashed #45a29e; padding: 50px;'><strong>[Übersicht.png] wurde im Verzeichnis nicht gefunden.</strong></div>", unsafe_allow_html=True)
        
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.button("<< ZURÜCK", on_click=navigiere, args=('Start',))
    with col2:
        st.button("OPERATIVES MENÜ STARTEN >>", on_click=navigiere, args=('Operativ',))

elif st.session_state.navigations_status == 'Operativ':
    col_top1, col_top2 = st.columns([1, 4])
    with col_top1:
        st.button("<< ÜBERSICHT", on_click=navigiere, args=('Uebersicht',))
    with col_top2:
        st.markdown("## 🏃‍♂️ Operative Trainingssteuerung")
    
    st.markdown("<div class='steuermatrix'>", unsafe_allow_html=True)
    st.markdown("### ⚙️ Biometrische Live-Steuerung & Kader-Verwaltung")
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        modus = st.selectbox("Steuerungs-Ebene", ["Einzelathlet / Einzelathletin", "Gruppe / Team"])
        if modus == "Einzelathlet / Einzelathletin":
            ziel = st.selectbox("Ziel (Name)", list(st.session_state.kader_db.keys()))
            aktuelle_daten = st.session_state.kader_db[ziel]
            profil_soll = aktuelle_daten["profil"]
        else:
            ziel = st.selectbox("Ziel (Kader)", list(abc_parameter.keys()))
            profil_soll = ziel
            aktuelle_daten = {"alter": 18, "groesse": 1.70, "fasertyp": "Schnelligkeit (Sprint)", "reife": "Normalentwickler", "sbe": abc_parameter[ziel]["sbe_ziel"], "t_60": 8.00}
            
    with c2:
        alter = st.number_input("Alter (Jahre)", min_value=10, max_value=40, value=int(aktuelle_daten["alter"]), disabled=(st.session_state.auth_modus == "gast"))
        groesse = st.number_input("Körpergröße (m)", min_value=1.30, max_value=2.15, value=float(aktuelle_daten["groesse"]), step=0.01, disabled=(st.session_state.auth_modus == "gast"))

    with c3:
        ft_liste = ["Ausdauer", "Kraft", "Sprungkraft", "Gazelle", "Schnelligkeit (Sprint)"]
        reife_liste = ["Spätentwickler (Retardiert)", "Normalentwickler", "Frühentwickler (Akzeleriert)"]
        
        ft_idx = ft_liste.index(aktuelle_daten["fasertyp"]) if aktuelle_daten["fasertyp"] in ft_liste else 4
        ft = st.selectbox("Fasertyp", ft_liste, index=ft_idx, disabled=(st.session_state.auth_modus == "gast"))
        
        reife_val = aktuelle_daten["reife"]
        r_idx = 0 if "Spät" in reife_val else 2 if "Früh" in reife_val else 1
        reife = st.selectbox("Entwicklungsstatus", reife_liste, index=r_idx, disabled=(st.session_state.auth_modus == "gast"))
            
    with c4:
        te_auswahl_liste = [f"TE {i}" for i in range(1, 3)] if st.session_state.auth_modus == "gast" else [f"TE {i}" for i in range(1, 15)]
        te_wahl = st.selectbox("Trainingseinheit (TE)", te_auswahl_liste)
        sbe_ziel = st.text_input("SBE (Reserve)", value=aktuelle_daten["sbe"], disabled=(st.session_state.auth_modus == "gast"))
        
    diag_col1, diag_col2 = st.columns(2)
    with diag_col1:
        t_60 = st.number_input("60m-Referenz (s)", min_value=6.0, max_value=15.0, value=float(aktuelle_daten.get("t_60", 8.00)), step=0.01, disabled=(st.session_state.auth_modus == "gast"))
    
    auto_150 = round(t_60 * 2.375, 2)
    with diag_col2:
        t_150 = st.number_input("150m-Referenz (s)", min_value=15.0, max_value=30.0, value=float(aktuelle_daten.get("t_150", auto_150)), step=0.01, disabled=(st.session_state.auth_modus == "gast"))

    st.markdown("</div>", unsafe_allow_html=True)

    calc_100 = round(t_60 * 1.615, 2)
    calc_200 = round(t_60 * 3.265, 2)
    vorgaben = abc_parameter.get(profil_soll, {"sets": 4, "start_m": 16.0, "step_m": 2.0})
    abc_sets = vorgaben["sets"]
    
    woche_num = int(te_wahl.replace("TE ", ""))
    raw_dist = (vorgaben["start_m"] + ((woche_num - 1) * vorgaben["step_m"])) * 1.09
    abc_dist = round(raw_dist * 2) / 2

    # --- NEU: Dynamische Hardware-Lasten für die Tabellenmatrix ---
    athleten_alter = int(alter)
    gewichtsstange = "2 Kg" if athleten_alter < 16 else "2-3 Kg"
    pb_leicht = "2 Kg" if athleten_alter < 16 else "4 Kg"
    pb_schwer = "3-4 Kg" if athleten_alter < 16 else "4-6 Kg"
    sj_last = "5-8 Kg" if ft in ["Gazelle", "Ausdauer"] and athleten_alter < 18 else "8-12 Kg"
    stl_vorgabe = "2x 100m u. 3x 60m"
    stl_intensitat = "bis 70% u. 80% Vmax"

    # DER NEUE SAUBERE BLOCK-DRUCKMODUS (Exaktes Doc-Athletic Format)
    st.markdown("---")
    st.subheader(f"📄 Offizielles Trainingsprotokoll & Druckansicht: {ziel} ({te_wahl})")
    st.markdown("Klicke unten auf den Block und nutze **Strg + P** für einen sauberen Papierausdruck.")

    html_matrix = f"""
    <div class="druck-block">
        <h2 style="color: #000000 !important; border-bottom: 2px solid #000000; padding-bottom: 5px; margin-top: 0;">DOC ATHLETIC TRAININGSMATRIX</h2>
        <p><strong>Athlet / Kader:</strong> {ziel} &nbsp;&nbsp;|&nbsp;&nbsp; <strong>Einheit:</strong> {te_wahl} &nbsp;&nbsp;|&nbsp;&nbsp; <strong>Fasertyp:</strong> {ft} &nbsp;&nbsp;|&nbsp;&nbsp; <strong>SBE-Ziel:</strong> {sbe_ziel}</p>
        <hr style="border: 1px solid #000;">
        <table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 13px;">
            <thead>
                <tr style="background-color: #e5e7eb; border-bottom: 2px solid #000;">
                    <th style="padding: 6px; border: 1px solid #000;">Block / Spezifisches Trainingsmittel</th>
                    <th style="padding: 6px; border: 1px solid #000; text-align: center;">Sätze</th>
                    <th style="padding: 6px; border: 1px solid #000;">Wdh. / Exakte Strecke</th>
                    <th style="padding: 6px; border: 1px solid #000;">Intensität / Zusatzlast</th>
                    <th style="padding: 6px; border: 1px solid #000; text-align: center;">Pause</th>
                    <th style="padding: 6px; border: 1px solid #000; text-align: center; width: 70px;">SBE (Ist)</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td style="padding: 6px; border: 1px solid #000;"><strong>Block 1: Allg. Erwärmung</strong></td>
                    <td style="padding: 6px; border: 1px solid #000; text-align: center;">1</td>
                    <td style="padding: 6px; border: 1px solid #000;">400 m</td>
                    <td style="padding: 6px; border: 1px solid #000;">Mobilisation</td>
                    <td style="padding: 6px; border: 1px solid #000; text-align: center;">-</td>
                    <td style="padding: 6px; border: 1px solid #000;"></td>
                </tr>
                <tr>
                    <td style="padding: 6px; border: 1px solid #000;">Spez. Erwärmung (STL locker/freq.)</td>
                    <td style="padding: 6px; border: 1px solid #000; text-align: center;">5</td>
                    <td style="padding: 6px; border: 1px solid #000;">{stl_vorgabe}</td>
                    <td style="padding: 6px; border: 1px solid #000;">{stl_intensitat}</td>
                    <td style="padding: 6px; border: 1px solid #000; text-align: center;">Trinkp.</td>
                    <td style="padding: 6px; border: 1px solid #000;"></td>
                </tr>
                <tr>
                    <td style="padding: 6px; border: 1px solid #000; background-color: #f9fafb;" colspan="6"><strong>Block 2: Neuromuskuläre Innervation</strong></td>
                </tr>
                <tr>
                    <td style="padding: 6px; border: 1px solid #000;">Kniehebelauf & Anfersen</td>
                    <td style="padding: 6px; border: 1px solid #000; text-align: center;">2</td>
                    <td style="padding: 6px; border: 1px solid #000;">{abc_dist:.1f} m hin/zurück</td>
                    <td style="padding: 6px; border: 1px solid #000;">>80% ({gewichtsstange})</td>
                    <td style="padding: 6px; border: 1px solid #000; text-align: center;">2s</td>
                    <td style="padding: 6px; border: 1px solid #000;"></td>
                </tr>
                <tr>
                    <td style="padding: 6px; border: 1px solid #000;">Seitliche Nachstellschritte & Überkrl.</td>
                    <td style="padding: 6px; border: 1px solid #000; text-align: center;">2</td>
                    <td style="padding: 6px; border: 1px solid #000;">{abc_dist:.1f} m hin/zurück</td>
                    <td style="padding: 6px; border: 1px solid #000;">>80% ({gewichtsstange})</td>
                    <td style="padding: 6px; border: 1px solid #000; text-align: center;">2s</td>
                    <td style="padding: 6px; border: 1px solid #000;"></td>
                </tr>
                <tr>
                    <td style="padding: 6px; border: 1px solid #000; background-color: #f9fafb;" colspan="6"><strong>Block 3: Kompl. Kraftfähigkeiten</strong></td>
                </tr>
                <tr>
                    <td style="padding: 6px; border: 1px solid #000;">Shuttle-Beschleunigung</td>
                    <td style="padding: 6px; border: 1px solid #000; text-align: center;">4</td>
                    <td style="padding: 6px; border: 1px solid #000;">40 m</td>
                    <td style="padding: 6px; border: 1px solid #000;">>85% Vmax</td>
                    <td style="padding: 6px; border: 1px solid #000; text-align: center;">10s</td>
                    <td style="padding: 6px; border: 1px solid #000;"></td>
                </tr>
                <tr>
                    <td style="padding: 6px; border: 1px solid #000;">Squat-Stoß-Jumps</td>
                    <td style="padding: 6px; border: 1px solid #000; text-align: center;">4</td>
                    <td style="padding: 6px; border: 1px solid #000;">10-12 Wdh.</td>
                    <td style="padding: 6px; border: 1px solid #000;">{pb_schwer} Bar</td>
                    <td style="padding: 6px; border: 1px solid #000; text-align: center;">1 min</td>
                    <td style="padding: 6px; border: 1px solid #000;"></td>
                </tr>
                <tr>
                    <td style="padding: 6px; border: 1px solid #000;">Technik Squat Jumps (11°)</td>
                    <td style="padding: 6px; border: 1px solid #000; text-align: center;">3</td>
                    <td style="padding: 6px; border: 1px solid #000;">10-12 Wdh.</td>
                    <td style="padding: 6px; border: 1px solid #000;">{sj_last} Speed Jumper</td>
                    <td style="padding: 6px; border: 1px solid #000; text-align: center;">90s</td>
                    <td style="padding: 6px; border: 1px solid #000;"></td>
                </tr>
                <tr>
                    <td style="padding: 6px; border: 1px solid #000; background-color: #f9fafb;" colspan="6"><strong>Block 4: Tempoläufe</strong></td>
                </tr>
                <tr>
                    <td style="padding: 6px; border: 1px solid #000;">Spezifischer Umfang</td>
                    <td style="padding: 6px; border: 1px solid #000; text-align: center;">{abc_sets}</td>
                    <td style="padding: 6px; border: 1px solid #000;">100 m</td>
                    <td style="padding: 6px; border: 1px solid #000;">80% (Basis {calc_100}s)</td>
                    <td style="padding: 6px; border: 1px solid #000; text-align: center;">Gehp.</td>
                    <td style="padding: 6px; border: 1px solid #000;"></td>
                </tr>
                <tr>
                    <td style="padding: 6px; border: 1px solid #000; background-color: #f9fafb;" colspan="6"><strong>Block 5: Ischiocrurale Sicherung</strong></td>
                </tr>
                <tr>
                    <td style="padding: 6px; border: 1px solid #000;">Ausfallschritt-Jumps</td>
                    <td style="padding: 6px; border: 1px solid #000; text-align: center;">2</td>
                    <td style="padding: 6px; border: 1px solid #000;">12 m</td>
                    <td style="padding: 6px; border: 1px solid #000;">2x {pb_leicht} Kettlebell</td>
                    <td style="padding: 6px; border: 1px solid #000; text-align: center;">45s</td>
                    <td style="padding: 6px; border: 1px solid #000;"></td>
                </tr>
                <tr>
                    <td style="padding: 6px; border: 1px solid #000;">Leg Speed Curler</td>
                    <td style="padding: 6px; border: 1px solid #000; text-align: center;">3</td>
                    <td style="padding: 6px; border: 1px solid #000;">24 Wdh.</td>
                    <td style="padding: 6px; border: 1px solid #000;">Körpergewicht</td>
                    <td style="padding: 6px; border: 1px solid #000; text-align: center;">60s</td>
                    <td style="padding: 6px; border: 1px solid #000;"></td>
                </tr>
                <tr>
                    <td style="padding: 6px; border: 1px solid #000; background-color: #d1d5db;" colspan="6"><strong>Block 6: Abwärmen & Regeneration</strong></td>
                </tr>
                <tr>
                    <td style="padding: 6px; border: 1px solid #000;">Auslaufen (Shuttle)</td>
                    <td style="padding: 6px; border: 1px solid #000; text-align: center;">1</td>
                    <td style="padding: 6px; border: 1px solid #000;">300m</td>
                    <td style="padding: 6px; border: 1px solid #000;">Sehr locker</td>
                    <td style="padding: 6px; border: 1px solid #000; text-align: center;">-</td>
                    <td style="padding: 6px; border: 1px solid #000;"></td>
                </tr>
                <tr>
                    <td style="padding: 6px; border: 1px solid #000;">Statische Dehnung (Tonus)</td>
                    <td style="padding: 6px; border: 1px solid #000; text-align: center;">1</td>
                    <td style="padding: 6px; border: 1px solid #000;">Individuell</td>
                    <td style="padding: 6px; border: 1px solid #000;">-</td>
                    <td style="padding: 6px; border: 1px solid #000; text-align: center;">-</td>
                    <td style="padding: 6px; border: 1px solid #000;"></td>
                </tr>
            </tbody>
        </table>
        <br>
        <p style="text-align: center; font-size: 11px; margin-bottom: 0;"><em>Doc Athletic Train Smart Philosophie — Aufgeben gilt nicht!</em></p>
    </div>
    """
    
    st.markdown(html_matrix, unsafe_allow_html=True)

    # FINALES ABSCHLUSS-FOTO
    st.markdown("---")
    col_f1, col_f2, col_f3 = st.columns([1, 2, 1])
    with col_f2:
        st.markdown("""
        <div class="footer-box">
            <h2 style="color: #66fcf1 !important; margin-bottom: 10px; font-family: Arial, sans-serif;">Aufgeben gilt nicht!</h2>
            <p style="color: #ffffff; font-size: 14px; letter-spacing: 1px;">DOC ATHLETIC EVOLUTION</p>
        </div>
        """, unsafe_allow_html=True)
        try:
            st.image("Foto.jpg", use_container_width=True)
        except:
            st.markdown("<div style='text-align: center; color: #66fcf1; padding: 10px;'>[Foto.jpg] wird im Hauptverzeichnis gesucht.</div>", unsafe_allow_html=True)
