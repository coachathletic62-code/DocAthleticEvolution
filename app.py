# =========================================================================
# DOC ATHLETIC EVOLUTION - WEB-MASTER (Version 18.78)
# Architektur: 3-Stufig | Engine: Login, Kader, Diagnostik & Voll-Matrix-Druck
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
    .steuermatrix {
        background-color: #111111; border: 2px solid #333333;
        border-radius: 5px; padding: 15px; margin-bottom: 20px;
    }
    .druck-block {
        background-color: #ffffff; color: #000000; border: 2px solid #45a29e;
        border-radius: 8px; padding: 25px; margin-top: 20px; margin-bottom: 20px;
        font-family: Arial, sans-serif;
    }
    .druck-block h2, .druck-block p, .druck-block td, .druck-block th {
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
    "Leichtathletik_U14": {"sets": 4, "start_m": 15.0, "step_m": 2.0, "sbe_ziel": "SR 2-3"}
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
            pass
    st.markdown("<br><br>", unsafe_allow_html=True)
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        st.button("SYSTEM INITIALISIEREN >>", on_click=navigiere, args=('Uebersicht',))

elif st.session_state.navigations_status == 'Uebersicht':
    st.title("Systemübersicht & Athleten-Datenbank")
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
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        modus = st.selectbox("Steuerungs-Ebene", ["Einzelathlet / Einzelathletin", "Gruppe / Team"])
        ziel = st.selectbox("Ziel (Name)", list(st.session_state.kader_db.keys()))
        aktuelle_daten = st.session_state.kader_db[ziel]
        profil_soll = aktuelle_daten["profil"]
            
    with c2:
        alter = st.number_input("Alter (Jahre)", min_value=10, max_value=40, value=int(aktuelle_daten["alter"]))
        groesse = st.number_input("Körpergröße (m)", min_value=1.30, max_value=2.15, value=float(aktuelle_daten["groesse"]), step=0.01)

    with c3:
        ft_liste = ["Ausdauer", "Kraft", "Sprungkraft", "Gazelle", "Schnelligkeit (Sprint)"]
        reife_liste = ["Spätentwickler (Retardiert)", "Normalentwickler", "Frühentwickler (Akzeleriert)"]
        ft_idx = ft_liste.index(aktuelle_daten["fasertyp"]) if aktuelle_daten["fasertyp"] in ft_liste else 4
        ft = st.selectbox("Fasertyp", ft_liste, index=ft_idx)
        r_idx = 0 if "Spät" in aktuelle_daten["reife"] else 2 if "Früh" in aktuelle_daten["reife"] else 1
        reife = st.selectbox("Entwicklungsstatus", reife_liste, index=r_idx)
            
    with c4:
        te_auswahl_liste = [f"TE {i}" for i in range(1, 15)]
        te_wahl = st.selectbox("Trainingseinheit (TE)", te_auswahl_liste)
        sbe_ziel = st.text_input("SBE (Reserve)", value=aktuelle_daten["sbe"])
        
    diag_col1, diag_col2 = st.columns(2)
    with diag_col1:
        t_60 = st.number_input("60m-Referenz (s)", value=float(aktuelle_daten.get("t_60", 8.00)), step=0.01)
    auto_150 = round(t_60 * 2.375, 2)
    with diag_col2:
        t_150 = st.number_input("150m-Referenz (s)", value=float(aktuelle_daten.get("t_150", auto_150)), step=0.01)

    st.markdown("</div>", unsafe_allow_html=True)

    calc_100 = round(t_60 * 1.615, 2)
    vorgaben = abc_parameter.get(profil_soll, {"sets": 4, "start_m": 16.0, "step_m": 2.0})
    abc_sets = vorgaben["sets"]
    woche_num = int(te_wahl.replace("TE ", ""))
    raw_dist = (vorgaben["start_m"] + ((woche_num - 1) * vorgaben["step_m"])) * 1.09
    abc_dist = round(raw_dist * 2) / 2

    athleten_alter = int(aktuelle_daten["alter"])
    gewichtsstange = "2 Kg" if athleten_alter < 16 else "2-3 Kg"
    power_bar_leicht = "2 Kg" if athleten_alter < 16 else "4 Kg"
    power_bar_schwer = "3-4 Kg" if athleten_alter < 16 else "4-6 Kg"
    speed_jumper_last = "5-8 Kg" if ft in ["Gazelle", "Ausdauer"] and athleten_alter < 18 else "8-12 Kg"
    stl_vorgabe = "2x 100m u. 3x 60m"
    stl_intensitat = "70% u. 80% Vmax"

    st.markdown("---")
    st.markdown(f"""
    <div class="druck-block">
        <h2 style="border-bottom: 2px solid #000000; padding-bottom: 5px; margin-top: 0;">DOC ATHLETIC TRAININGSMATRIX</h2>
        <p><strong>Athlet:</strong> {ziel} &nbsp;&nbsp;|&nbsp;&nbsp; <strong>Einheit:</strong> {te_wahl} &nbsp;&nbsp;|&nbsp;&nbsp; <strong>Fasertyp:</strong> {ft} &nbsp;&nbsp;|&nbsp;&nbsp; <strong>SBE-Ziel:</strong> {sbe_ziel}</p>
        <table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 13px;">
            <thead>
                <tr style="background-color: #e5e7eb; border-bottom: 2px solid #000000;">
                    <th style="padding: 6px; border: 1px solid #000;">Block / Spezifisches Trainingsmittel</th>
                    <th style="padding: 6px; border: 1px solid #000; text-align: center;">Sätze</th>
                    <th style="padding: 6px; border: 1px solid #000;">Wdh. / Strecke</th>
                    <th style="padding: 6px; border: 1px solid #000;">Intensität / Last</th>
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
                    <td style="padding: 6px; border: 1px solid #000;">{abc_dist:.1f} m hin / {abc_dist:.1f} m zurück</td>
                    <td style="padding: 6px; border: 1px solid #000;">>80% ({gewichtsstange})</td>
                    <td style="padding: 6px; border: 1px solid #000; text-align: center;">2s</td>
                    <td style="padding: 6px; border: 1px solid #000;"></td>
                </tr>
                <tr>
                    <td style="padding: 6px; border: 1px solid #000;">Seitliche Nachstellschritte & Überkrl.</td>
                    <td style="padding: 6px; border: 1px solid #000; text-align: center;">2</td>
                    <td style="padding: 6px; border: 1px solid #000;">{abc_dist:.1f} m hin / {abc_dist:.1f} m zurück</td>
                    <td style="padding: 6px; border: 1px solid #000;">>80% ({gewichtsstange})</td>
                    <td style="padding: 6px; border: 1px solid #000; text-align: center;">2s</td>
                    <td style="padding: 6px; border: 1px solid #000;"></td>
                </tr>
                <tr>
                    <td style="padding: 6px; border: 1px solid #000;">Hopserlauf & Streckbeinlauf</td>
                    <td style="padding: 6px; border: 1px solid #000; text-align: center;">2</td>
                    <td style="padding: 6px; border: 1px solid #000;">{abc_dist:.1f} m / {abc_dist:.1f} m zurück</td>
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
                    <td style="padding: 6px; border: 1px solid #000;">10 - 12 Wdh.</td>
                    <td style="padding: 6px; border: 1px solid #000;">{power_bar_schwer} Bar</td>
                    <td style="padding: 6px; border: 1px solid #000; text-align: center;">1 min</td>
                    <td style="padding: 6px; border: 1px solid #000;"></td>
                </tr>
                <tr>
                    <td style="padding: 6px; border: 1px solid #000;">Technik Squat Jumps (11°)</td>
                    <td style="padding: 6px; border: 1px solid #000; text-align: center;">3</td>
                    <td style="padding: 6px; border: 1px solid #000;">10 - 12 Wdh.</td>
                    <td style="padding: 6px; border: 1px solid #000;">{speed_jumper_last} Speed Jumper</td>
                    <td style="padding: 6px; border: 1px solid #000; text-align: center;">90s</td>
                    <td style="padding: 6px; border: 1px solid #000;"></td>
                </tr>
                <tr>
                    <td style="padding: 6px; border: 1px solid #000;"><strong>Block 4: Tempoläufe</strong></td>
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
                    <td style="padding: 6px; border: 1px solid #000;">2x {power_bar_leicht} Kett.</td>
                    <td style="padding: 6px; border: 1px solid #000; text-align: center;">45s</td>
                    <td style="padding: 6px; border: 1px solid #000;"></td>
                </tr>
                <tr>
                    <td style="padding: 6px; border: 1px solid #000;">Leg Speed Curler</td>
                    <td style="padding: 6px; border: 1px solid #000; text-align: center;">3</td>
                    <td style="padding: 6px; border: 1px solid #000;">20-24 Wdh.</td>
                    <td style="padding: 6px; border: 1px solid #000;">Körpergewicht</td>
                    <td style="padding: 6px; border: 1px solid #000; text-align: center;">60s</td>
                    <td style="padding: 6px; border: 1px solid #000;"></td>
                </tr>
            </tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)
