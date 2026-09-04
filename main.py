# ============================================================================
# DOC ATHLETIC EVOLUTION - FUSSBALL & LEICHTATHLETIK (Version 23.8)
# Update: Power Bags als Von-Bis-Korridor (bis 17 kg) & 12-15 Wdh. Front Squat Jumps
# ============================================================================

import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Doc Athletic Evolution 23.8", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
.stApp { background-color: #000000; color: #ffffff; }
h1, h2, h3, h4, h5, h6, p, label { color: #ffffff !important; }
button[title="View fullscreen"] { display: none !important; }

/* Eingabefelder */
.stSelectbox > div > div, .stTextInput > div > div > input, .stNumberInput > div > div > input {
    background-color: #ffffff !important;
    color: #000000 !important;
}

/* Buttons */
.stButton>button {
    background-color: #1f2833; color: #66fcf1;
    border: 2px solid #45a29e; border-radius: 8px;
    width: 100%; font-weight: bold;
}
div.stDownloadButton > button {
    background-color: #66fcf1 !important;
    border: 2px solid #45a29e !important;
    border-radius: 8px !important;
    width: 100% !important;
    padding: 12px !important;
}
div.stDownloadButton > button *,
div.stDownloadButton > button p,
div.stDownloadButton > button span {
    color: #000000 !important;
    font-weight: 900 !important;
    font-size: 15px !important;
}

/* Peppiges High-Performance Steuerungs-Panel */
.steuermatrix {
    background: linear-gradient(145deg, #10161d, #07090c);
    border: 2px solid #66fcf1;
    box-shadow: 0 0 25px rgba(102, 252, 241, 0.25);
    border-radius: 12px;
    padding: 25px;
    margin-bottom: 25px;
}

/* Zentrierte und vergrößerte Sportarten-Wahl */
div[role="radiogroup"] {
    justify-content: center !important;
    gap: 30px !important;
    margin: 15px 0 !important;
}
div[role="radiogroup"] label {
    background-color: #1f2833 !important;
    padding: 12px 28px !important;
    border-radius: 10px !important;
    border: 2px solid #45a29e !important;
    cursor: pointer !important;
    transition: all 0.25s ease-in-out !important;
}
div[role="radiogroup"] label:hover {
    border-color: #66fcf1 !important;
    box-shadow: 0 0 15px rgba(102, 252, 241, 0.4) !important;
}
div[role="radiogroup"] label p {
    font-size: 22px !important;
    font-weight: 900 !important;
    color: #ffffff !important;
    letter-spacing: 0.5px !important;
}

.badge-fussball { 
    background-color: #2ecc71; color: #000000; padding: 8px 18px;
    border-radius: 6px; font-weight: 900; font-size: 16px; display: inline-block;
    box-shadow: 0 0 10px rgba(46, 204, 113, 0.4);
}
.badge-leichtathletik { 
    background-color: #e74c3c; color: #ffffff; padding: 8px 18px;
    border-radius: 6px; font-weight: 900; font-size: 16px; display: inline-block;
    box-shadow: 0 0 10px rgba(231, 76, 60, 0.4);
}

.footer-box {
    text-align: center; border: 2px solid #66fcf1; border-radius: 10px;
    padding: 25px; margin-top: 40px; margin-bottom: 20px; background-color: #0b0c10;
}

@media print {
    @page { size: landscape; margin: 10mm; }
    body { background-color: #ffffff !important; color: #000000 !important; }
    .stApp, .steuermatrix, .footer-box { background-color: #ffffff !important; color: #000000 !important; border: none !important; }
    h1, h2, h3, h4, h5, h6, p, label, span { color: #000000 !important; }
    .stButton, .stDownloadButton, [data-testid="stSidebar"], .stRadio { display: none !important; }
    .druck-block { background-color: #ffffff !important; color: #000000 !important; border: none !important; }
}
</style>
""", unsafe_allow_html=True)

def lade_bild(dateinamen_liste, use_col=False):
    for name in dateinamen_liste:
        if os.path.exists(name):
            if use_col:
                st.image(name, use_container_width=True)
            return True
    return False

GAST_CODE = "gast2026"
TRAINER_CODE = "DocAthletic#2026!"

if 'auth_modus' not in st.session_state:
    st.session_state.auth_modus = None

if st.session_state.auth_modus is None:
    col_11, col_12, col_13 = st.columns([1, 2, 1])
    with col_12:
        lade_bild(["logo.png", "logo.png.png", "logo"], use_col=True)
        st.markdown("<p style='text-align: center; color: #c5c6c7; margin-top: 20px;'>Bitte Zugriffscode eingeben (Fußball & Leichtathletik)</p>", unsafe_allow_html=True)
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
    st.stop()

if 'navigations_status' not in st.session_state:
    st.session_state.navigations_status = 'Start'

if 'kader_db' not in st.session_state:
    st.session_state.kader_db = {
        "Fussball": {
            "Mathilda Karnik": {"alter": 14, "groesse": 1.57, "gewicht": 46.0, "profil": "Fussball_U15_w", "fasertyp": "Gazelle", "reife": "Spätentwickler (Retardiert)", "sbe": "SR 3", "t_60": 8.90, "t_150": 21.14},
            "Sari Saeland": {"alter": 19, "groesse": 1.58, "gewicht": 52.0, "profil": "Fussball_U20_w", "fasertyp": "Gazelle", "reife": "Normalentwickler", "sbe": "SR 2", "t_60": 8.00},
            "Ronja Borchmeyer": {"alter": 20, "groesse": 1.70, "gewicht": 62.0, "profil": "Fussball_U23_w", "fasertyp": "Kraft", "reife": "Normalentwickler", "sbe": "SR 2", "t_60": 8.10},
            "Svenja Poock": {"alter": 20, "groesse": 1.78, "gewicht": 67.0, "profil": "Fussball_U23_w", "fasertyp": "Kraft", "reife": "Normalentwickler", "sbe": "SR 2", "t_60": 8.30},
            "Nora Giannori": {"alter": 22, "groesse": 1.77, "gewicht": 65.0, "profil": "Fussball_U23_w", "fasertyp": "Ausdauer", "reife": "Normalentwickler", "sbe": "SR 2", "t_60": 8.40},
            "Mieke Schiemann": {"alter": 24, "groesse": 1.78, "gewicht": 66.0, "profil": "Fussball_MASTER_w", "fasertyp": "Ausdauer", "reife": "Normalentwickler", "sbe": "SR 2", "t_60": 8.50},
            "Christoffer Danders": {"alter": 19, "groesse": 1.78, "gewicht": 74.0, "profil": "Fussball_U20_m", "fasertyp": "Schnelligkeit (Sprint)", "reife": "Normalentwickler", "sbe": "SR 1", "t_60": 7.60}
        },
        "Leichtathletik": {
            "Sprint Talent U17": {"alter": 16, "groesse": 1.75, "gewicht": 68.0, "profil": "Leichtathletik_U17_m", "fasertyp": "Schnelligkeit (Sprint)", "reife": "Normalentwickler", "sbe": "SR 1", "t_60": 7.30},
            "Nachwuchs Talent U13": {"alter": 12, "groesse": 1.52, "gewicht": 42.0, "profil": "Leichtathletik_U13", "fasertyp": "Sprungkraft", "reife": "Normalentwickler", "sbe": "SR 2", "t_60": 8.40}
        }
    }

def navigiere(ziel):
    st.session_state.navigations_status = ziel

abc_parameter = {
    "Fussball_U11": {"sets": 3, "start_m": 12.0, "step_m": 2.0, "sbe_ziel": "SR 3"},
    "Fussball_U13": {"sets": 4, "start_m": 15.0, "step_m": 2.5, "sbe_ziel": "SR 2-3"},
    "Fussball_U15_m": {"sets": 4, "start_m": 18.0, "step_m": 2.5, "sbe_ziel": "SR 2"},
    "Fussball_U15_w": {"sets": 4, "start_m": 15.0, "step_m": 2.5, "sbe_ziel": "SR 2"},
    "Fussball_U17_m": {"sets": 5, "start_m": 22.0, "step_m": 3.0, "sbe_ziel": "SR 1-2"},
    "Fussball_U17_w": {"sets": 5, "start_m": 20.0, "step_m": 2.5, "sbe_ziel": "SR 1-2"},
    "Fussball_U20_m": {"sets": 5, "start_m": 25.0, "step_m": 3.0, "sbe_ziel": "SR 1"},
    "Fussball_U20_w": {"sets": 5, "start_m": 22.0, "step_m": 2.5, "sbe_ziel": "SR 1"},
    "Fussball_U23_m": {"sets": 6, "start_m": 28.0, "step_m": 3.0, "sbe_ziel": "SR 1-0"},
    "Fussball_U23_w": {"sets": 6, "start_m": 25.0, "step_m": 2.5, "sbe_ziel": "SR 1-0"},
    "Fussball_MASTER_m": {"sets": 6, "start_m": 30.0, "step_m": 3.0, "sbe_ziel": "SR 0"},
    "Fussball_MASTER_w": {"sets": 6, "start_m": 28.0, "step_m": 3.0, "sbe_ziel": "SR 0"},
    "Leichtathletik_U11": {"sets": 3, "start_m": 12.0, "step_m": 2.0, "sbe_ziel": "SR 3"},
    "Leichtathletik_U13": {"sets": 4, "start_m": 15.0, "step_m": 2.0, "sbe_ziel": "SR 2-3"},
    "Leichtathletik_U15": {"sets": 4, "start_m": 18.0, "step_m": 2.5, "sbe_ziel": "SR 2"},
    "Leichtathletik_U17_m": {"sets": 5, "start_m": 25.0, "step_m": 3.5, "sbe_ziel": "SR 1-2"},
    "Leichtathletik_U17_w": {"sets": 5, "start_m": 22.0, "step_m": 3.0, "sbe_ziel": "SR 1-2"},
    "Leichtathletik_U20_m": {"sets": 6, "start_m": 28.0, "step_m": 3.0, "sbe_ziel": "SR 1"},
    "Leichtathletik_U20_w": {"sets": 6, "start_m": 26.0, "step_m": 3.0, "sbe_ziel": "SR 1"},
    "Leichtathletik_U23_m": {"sets": 6, "start_m": 30.0, "step_m": 3.0, "sbe_ziel": "SR 0"},
    "Leichtathletik_U23_w": {"sets": 6, "start_m": 28.0, "step_m": 3.0, "sbe_ziel": "SR 0"},
    "Leichtathletik_MASTER_m": {"sets": 6, "start_m": 30.0, "step_m": 3.0, "sbe_ziel": "SR 0"},
    "Leichtathletik_MASTER_w": {"sets": 6, "start_m": 28.0, "step_m": 3.0, "sbe_ziel": "SR 0"}
}

HARDWARE_GRIFFBAELLE = [3, 5, 7, 9]
HARDWARE_HEXBAR = [30, 35, 40, 45, 50, 55, 60, 65, 70]

def snap_to_hardware(wert, hardware_liste, konservativ=True):
    passende = [h for h in hardware_liste if (h <= wert if konservativ else h >= wert)]
    if passende:
        return max(passende) if konservativ else min(passende)
    return min(hardware_liste)

if st.session_state.auth_modus == "gast":
    st.sidebar.warning("GAST-MODUS (Nur Leserechte)")

if st.session_state.navigations_status == 'Start':
    st.markdown("<h1 style='text-align: center; color: #66fcf1 !important; margin-top: 30px;'>DOC ATHLETIC EVOLUTION 23.8</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #c5c6c7; font-size: 16px;'>Fußball & Leichtathletik Edition (12-15 Wdh. Front Squat & Power Bag Korridore)</p>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        lade_bild(["logo.png", "logo.png.png", "logo"], use_col=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.button("SYSTEM INITIALISIEREN >>", on_click=navigiere, args=('Uebersicht',))

elif st.session_state.navigations_status == 'Uebersicht':
    st.title("Systemübersicht & Athleten-Datenbank")
    st.markdown("## Komplex-Training im Nachwuchs bis Hochleistungssport (Fußball & Leichtathletik)")
    st.markdown("---")
    bild_geladen = lade_bild(["übersicht.png", "uebersicht.png", "uebersicht.png.png"], use_col=True)
    if not bild_geladen:
        st.markdown("<div style='text-align: center; border: 1px dashed #45a29e; padding: 30px;'><strong>[übersicht.png / uebersicht.png] im Verzeichnis hinterlegen.</strong></div>", unsafe_allow_html=True)
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
        st.markdown("## Operative Trainingssteuerung")

    st.markdown("<div class='steuermatrix'>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #66fcf1 !important; font-size: 26px; font-weight: 900; letter-spacing: 1.5px; text-transform: uppercase; margin-top: 0; margin-bottom: 5px;'>Biometrische Live-Steuerung & Disziplin-Wahl</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #a0aab2; font-size: 14px; margin-bottom: 15px;'>Fokussierte Trainingsansteuerung nach Doc Athletic Train Smart Philosophie</p>", unsafe_allow_html=True)
    
    sport_kategorie = st.radio("Sportart wählen", ["⚽ Fußball", "🏃 Leichtathletik"], horizontal=True, label_visibility="collapsed")
    
    if "Fußball" in sport_kategorie:
        aktive_kategorie = "Fussball"
        aktive_sport_schluessel = [k for k in abc_parameter.keys() if "Fussball" in k]
        st.markdown("<div style='text-align: center; margin-top: 10px;'><span class='badge-fussball'>⚽ Modul: Fußball aktiv (Kernsportart)</span></div>", unsafe_allow_html=True)
    else:
        aktive_kategorie = "Leichtathletik"
        aktive_sport_schluessel = [k for k in abc_parameter.keys() if "Leichtathletik" in k]
        st.markdown("<div style='text-align: center; margin-top: 10px;'><span class='badge-leichtathletik'>🏃 Modul: Leichtathletik aktiv (Peripher)</span></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    aktive_athleten_db = st.session_state.kader_db[aktive_kategorie]

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        modus = st.selectbox("Steuerungs-Ebene", ["Einzelathlet / Einzelathletin", "Gruppe / Team (Kader)"])
        if modus == "Einzelathlet / Einzelathletin":
            if len(aktive_athleten_db) > 0:
                ziel = st.selectbox("Ziel (Name)", list(aktive_athleten_db.keys()))
                aktuelle_daten = aktive_athleten_db[ziel]
                profil_soll = aktuelle_daten["profil"]
            else:
                ziel = "Neuer Athlet"
                aktuelle_daten = {"alter": 16, "groesse": 1.75, "gewicht": 65.0, "profil": aktive_sport_schluessel[0], "fasertyp": "Schnelligkeit (Sprint)", "reife": "Normalentwickler", "sbe": "SR 2", "t_60": 7.80}
                profil_soll = aktive_sport_schluessel[0]
        else:
            ziel = st.selectbox("Ziel (Kader / Profil)", aktive_sport_schluessel)
            profil_soll = ziel
            aktuelle_daten = {"alter": 16, "groesse": 1.75, "gewicht": 65.0, "fasertyp": "Schnelligkeit (Sprint)", "reife": "Normalentwickler", "sbe": abc_parameter[ziel]["sbe_ziel"], "t_60": 7.80}

    with c2:
        alter = st.number_input("Alter (Jahre)", min_value=10, max_value=40, value=int(aktuelle_daten["alter"]), disabled=(st.session_state.auth_modus == "gast"))
        geschlecht_wahl = st.selectbox("Geschlecht (Hormoneller Status)", ["Männlich", "Weiblich"], index=1 if "w" in profil_soll or "Weiblich" in str(aktuelle_daten.get("profil","")) else 0)

    with c3:
        groesse = st.number_input("Körpergröße (m)", min_value=1.30, max_value=2.15, value=float(aktuelle_daten.get("groesse", 1.70)), step=0.01, disabled=(st.session_state.auth_modus == "gast"))
        gewicht = st.number_input("Körpergewicht (kg)", min_value=30.0, max_value=140.0, value=float(aktuelle_daten.get("gewicht", 55.0)), step=0.5, disabled=(st.session_state.auth_modus == "gast"))

    with c4:
        ft_liste = ["Ausdauer", "Kraft", "Sprungkraft", "Gazelle", "Schnelligkeit (Sprint)"]
        reife_liste = ["Spätentwickler (Retardiert)", "Normalentwickler", "Frühentwickler (Akzeleriert)"]
        ft_idx = ft_liste.index(aktuelle_daten["fasertyp"]) if aktuelle_daten["fasertyp"] in ft_liste else 4
        ft = st.selectbox("Fasertyp", ft_liste, index=ft_idx, disabled=(st.session_state.auth_modus == "gast"))
        reife_val = aktuelle_daten["reife"]
        r_idx = 0 if "Spät" in reife_val else 2 if "Früh" in reife_val else 1
        reife = st.selectbox("Entwicklungsstatus", reife_liste, index=r_idx, disabled=(st.session_state.auth_modus == "gast"))

    c_opt1, c_opt2 = st.columns(2)
    with c_opt1:
        te_wahl = st.selectbox("Trainingseinheit (TE)", [f"TE {i}" for i in range(1, 15)] + ["Alle TEs (1-14)"])
    with c_opt2:
        jump_modus = st.selectbox("Komplex-Sprungmodus", ["Jumps (Vorfuß am Boden / Dreifachstreckung)", "Sprünge (Flugphase > 3-5 cm / Reaktiv)"])

    sbe_ziel = st.text_input("SBE (Reserve)", value=aktuelle_daten["sbe"], disabled=(st.session_state.auth_modus == "gast"))

    if modus == "Gruppe / Team (Kader)":
        base_prof = profil_soll.rsplit('_', 1)[0] if ('_m' in profil_soll or '_w' in profil_soll) else profil_soll
        suffix = "_w" if geschlecht_wahl == "Weiblich" else "_m"
        if f"{base_prof}{suffix}" in abc_parameter:
            profil_soll = f"{base_prof}{suffix}"

    diag_col1, diag_col2 = st.columns(2)
    with diag_col1:
        t_60 = st.number_input("60m-Referenz (s)", min_value=6.0, max_value=15.0, value=float(aktuelle_daten.get("t_60", 7.80)), step=0.01, disabled=(st.session_state.auth_modus == "gast"))
    with diag_col2:
        auto_150 = round(t_60 * 2.375, 2)
        t_150 = st.number_input("150m-Referenz (s)", min_value=15.0, max_value=30.0, value=float(aktuelle_daten.get("t_150", auto_150) if "t_150" in aktuelle_daten else auto_150), step=0.01, disabled=(st.session_state.auth_modus == "gast"))

    if modus == "Einzelathlet / Einzelathletin" and st.session_state.auth_modus == "trainer":
        neuer_name = st.text_input("Neuen Athleten-Namen eingeben (zum Anlegen):", value="")
        if st.button("Athleten-Profil in Sektion speichern"):
            ziel_name = neuer_name if neuer_name else ziel
            st.session_state.kader_db[aktive_kategorie][ziel_name] = {
                "alter": int(alter), "groesse": float(groesse), "gewicht": float(gewicht), "profil": profil_soll,
                "fasertyp": ft, "reife": reife, "sbe": sbe_ziel, "t_60": float(t_60), "t_150": float(t_150)
            }
            st.success(f"Profil für {ziel_name} ({gewicht} kg) erfolgreich gesichert.")
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    reife_intern = "Spätentwickler" if "Spät" in reife else "Frühentwickler" if "Früh" in reife else "Normalentwickler"

    st.subheader("Diagnostik-Modul (Polynomische Regression)")
    calc_100 = round(t_60 * 1.615, 2)
    calc_200 = round(t_60 * 3.265, 2)

    res_col1, res_col2 = st.columns(2)
    with res_col1:
        st.markdown("#### Aktuelle Ist-Korrelation")
        st.write(f"60m: **{t_60:.2f} s** | 100m: **{calc_100:.2f} s** | 150m: **{t_150:.2f} s** | 200m: **{calc_200:.2f} s**")
    with res_col2:
        st.markdown("#### 12-Monats-Entwicklungsprognose")
        prog_faktor = 0.97 if reife == "Frühentwickler (Akzeleriert)" else 0.98
        p_100 = calc_100 * prog_faktor
        p_200 = calc_200 * prog_faktor
        st.write(f"Prognose 100m: **{p_100:.2f} s** | 200m: **{p_200:.2f} s**")

    st.markdown("---")
    st.subheader("Tempotabellen (Echte Live-Korrelation mit 75m-Zwischenwert)")

    def format_time(seconds):
        if seconds >= 60:
            m = int(seconds // 60)
            s = seconds % 60
            return f"{m}:{s:04.1f} min"
        return f"{seconds:.1f} s"

    tempo_data = []
    for dist_m in [50, 75, 100, 150, 200]:
        if dist_m == 50:
            base_s = calc_100 / 1.93
        elif dist_m == 75:
            base_s = calc_100 * 0.775
        elif dist_m == 100:
            base_s = calc_100
        elif dist_m == 150:
            base_s = t_150
        elif dist_m == 200:
            base_s = calc_200

        row = {
            "Distanz": f"{dist_m}m",
            "100%": format_time(base_s),
            "95%": format_time(base_s / 0.95),
            "90%": format_time(base_s / 0.90),
            "80%": format_time(base_s / 0.80),
            "70%": format_time(base_s / 0.70)
        }
        tempo_data.append(row)

    st.table(pd.DataFrame(tempo_data).set_index("Distanz"))

    st.markdown("---")
    st.subheader(f"Detaillierter Trainingsplan & Doc-Athletic-Farbkodierung: {ziel}")

    vorgaben = abc_parameter.get(profil_soll, {"sets": 4, "start_m": 15.0, "step_m": 2.5})
    te_liste = range(1, 15) if "Alle" in te_wahl else [int(te_wahl.replace("TE ", ""))]

    # ========================================================================
    # POWER BAGS: REALISTISCHE VON-BIS-KORRIDORE (BIS 17 KG) & 12-15 WDH.
    # ========================================================================
    if int(alter) <= 13:
        bag_text = "Power Bag 5-8 kg"
        bag_wdh = "10-12 Wdh."
    elif int(alter) <= 15:
        if ft == "Gazelle" or reife_intern == "Spätentwickler":
            bag_text = "Power Bag 8-10 kg"
        else:
            bag_text = "Power Bag 10-13 kg"
        bag_wdh = "12-15 Wdh."
    elif int(alter) <= 17:
        if ft == "Gazelle":
            bag_text = "Power Bag 10-13 kg"
        else:
            bag_text = "Power Bag 12-15 kg"
        bag_wdh = "12-15 Wdh."
    else:
        if gewicht < 70 or ft == "Gazelle":
            bag_text = "Power Bag 12-16 kg"
        else:
            bag_text = "Power Bag 15-17 kg"
        bag_wdh = "12-15 Wdh."

    # Griffbälle für Umsatz/Crunch
    if int(alter) <= 13:
        gb_last_kg = 3
    elif int(alter) <= 15:
        gb_last_kg = 5 if ft in ["Kraft", "Schnelligkeit (Sprint)"] else 3
    elif int(alter) <= 17:
        gb_last_kg = 7 if ft == "Kraft" else 5
    else:
        gb_last_kg = 9 if ft == "Kraft" and gewicht >= 75 else 7

    # Hex Bar (8-12 Wdh. beibehalten)
    ist_jumps = "Jumps" in jump_modus
    if int(alter) <= 13:
        hex_text = "Hex Bar nicht freigegeben (Körpergewicht)"
    elif int(alter) <= 15:
        hex_kg = 30 if ft == "Kraft" else 25
        hex_text = f"Kettlebell-Paar {hex_kg} kg (Bodenkontakt)"
    elif int(alter) <= 17:
        ziel_hex = gewicht * (0.55 if ist_jumps else 0.45)
        if ft == "Gazelle": ziel_hex *= 0.90
        hex_kg = snap_to_hardware(ziel_hex, HARDWARE_HEXBAR, konservativ=True)
        hex_kg = min(hex_kg, 45 if ist_jumps else 35)
        hex_text = f"Hex Bar {hex_kg} kg ({'Jumps' if ist_jumps else 'Sprünge'})"
    else:
        ziel_hex = gewicht * (0.75 if ist_jumps else 0.60)
        if ft == "Gazelle": ziel_hex *= 0.90
        hex_kg = snap_to_hardware(ziel_hex, HARDWARE_HEXBAR, konservativ=True)
        hex_kg = min(hex_kg, 60 if ist_jumps else 50)
        hex_text = f"Hex Bar {hex_kg} kg ({'Jumps' if ist_jumps else 'Sprünge'})"

    # Hürden-Tiefsprünge
    if int(alter) <= 13:
        tief_hoehe = "30-38 cm"
        tief_kh = "ohne ZL"
    elif int(alter) <= 15:
        tief_hoehe = "38-45 cm"
        tief_kh = "ohne ZL bis 2x 1 kg KH"
    elif int(alter) <= 17:
        tief_hoehe = "45 cm (Abstand 4,5 Fuß)"
        tief_kh = "2x 1 kg bis 2x 2 kg KH (Spitze 2x 3 kg)"
    else:
        tief_hoehe = "45-55 cm (Abstand 4-5 Fuß)"
        tief_kh = "2x 2 kg bis 2x 4 kg KH"

    html_matrices = ""

    for woche in te_liste:
        abc_dist = vorgaben["start_m"] + ((woche - 1) * vorgaben["step_m"])

        if int(alter) <= 13:
            abc_last_str = "1,5-2,0 kg Power Bar über Kopf"
        elif int(alter) <= 15:
            abc_last_str = "2,0 kg Power Bar über Kopf" if ft == "Gazelle" else "2,0-3,0 kg Power Bar über Kopf"
        elif int(alter) <= 17:
            if woche in [1, 2]:
                abc_last_str = "Ohne Stange (Fokus Bahnung/Frequenz)"
            else:
                abc_last_str = "2,0-3,0 kg Power Bar über Kopf" if gewicht < 70 else "3,0-4,0 kg Power Bar über Kopf"
        else:
            abc_last_str = "2,0-3,0 kg Power Bar über Kopf" if gewicht < 70 else "3,0-4,0 kg Power Bar über Kopf"

        pause_komplex = "45-60s" if geschlecht_wahl == "Weiblich" else "90s" if int(alter) <= 15 else "90-120s"

        if int(alter) <= 15:
            if woche in [1, 2]:
                tl_pos = "nach_komplex"
                tl_text = "6 x 100m TL (75-80%)"
                tl_pause = "50m Gehpause"
            elif woche in [3, 4]:
                tl_pos = "nach_komplex"
                tl_text = "4 x 150m + 2 x 100m TL (> 75%)"
                tl_pause = "50m Gehpause"
            elif woche in [5, 6]:
                tl_pos = "nach_komplex"
                tl_text = "2 x 300m + 2 x 200m + 2 x 150m TL (Absteigend)"
                tl_pause = "100m Gehpause"
            elif woche == 7:
                tl_pos = "nach_komplex"
                tl_text = "2 x 400m + 2 x 300m + 2 x 200m TL (Absteigend)"
                tl_pause = "100m Gehpause"
            elif woche in [8, 9, 10]:
                tl_pos = "vor_komplex"
                tl_text = "2 x 600m (Basis 60%) + 2 x 400m + 3 x 200m (GLA vorab)"
                tl_pause = "100m Gehpause (200m bei 50m GP)"
            elif woche == 11:
                tl_pos = "vor_komplex"
                tl_text = "3 x 600m TL (Richtwert 1:40 min) + 4 x 150m Speed"
                tl_pause = "100m Gehpause"
            elif woche == 12:
                tl_pos = "nach_komplex"
                tl_text = "Speed-Shuttle auf Kunstrasen: 4 x 55m Doppel-Shuttle + Antritte"
                tl_pause = "Staffelpause"
            elif woche == 13:
                tl_pos = "marathon"
                tl_text = "Athletik & Lauf-Marathon: 3 Runden à 400m TL (50%) + Parcours"
                tl_pause = "Im Kettenablauf"
            else:
                tl_pos = "nach_komplex"
                tl_text = "Abschlusstest: 60m Zeit + 250m Zeit + 600m Zeit (Maximal)"
                tl_pause = "Volle Erholung"

        elif int(alter) <= 17:
            if woche in [1, 2]:
                tl_pos = "nach_komplex"
                tl_text = "6 x 100m Technik TL (80%) [Lauf-ABC ohne Stange]"
                tl_pause = "50m Gehpause"
            elif woche in [3, 4]:
                tl_pos = "nach_komplex"
                tl_text = "2 x 300m + 2 x 200m + 2 x 150m TL (Absteigend)"
                tl_pause = "100m Gehpause"
            elif woche in [5, 6]:
                tl_pos = "nach_komplex"
                tl_text = "1 x 500m + 1 x 400m + 2 x 300m + 2 x 200m (Absteigend 70-80%)"
                tl_pause = "100m Gehpause"
            elif woche == 7:
                tl_pos = "nach_komplex"
                tl_text = "2 x 550m + 2 x 350m TL (Kaskade > 65%)"
                tl_pause = "100m Gehpause"
            elif woche in [8, 9, 10]:
                tl_pos = "vor_komplex"
                tl_text = "GLA vorab: 600m, 600m, 500m, 500m (je 100m GP) vor Stationen"
                tl_pause = "100m Gehpause"
            elif woche == 11:
                tl_pos = "vor_komplex"
                tl_text = "GLA vorab: 1 x 700m Kappe + 2 x 500m + 3 x 150m Speed"
                tl_pause = "100m Gehpause"
            elif woche == 12:
                tl_pos = "nach_komplex"
                tl_text = "Witterungs-Speed: 12 x 40m Doppel-Shuttle mit 3 kg ZL"
                tl_pause = "5s Wende / Staffelpause"
            elif woche == 13:
                tl_pos = "marathon"
                tl_text = "Athletik- & Lauf-Marathon: 3x 400m Schleifen-Shuttle + Parcours"
                tl_pause = "Im Kettenablauf"
            else:
                tl_pos = "nach_komplex"
                tl_text = "Saison-Peak: 60m Sprint + 250m + 600m Test auf Zeit"
                tl_pause = "Volle Erholung"

        else:
            if woche in [1, 2]:
                tl_pos = "nach_komplex"
                tl_text = "6 x 100m Technik Sprintlauf (> 85%) direkt nach Station 1"
                tl_pause = "50-100m Gehpause"
            elif woche in [3, 4]:
                tl_pos = "nach_komplex"
                tl_text = "Direct-PAP: 2x 150m Sprint (>85%) + 1x 350m (>70%) + 1x 550m (70%)"
                tl_pause = "100m Gehpause"
            elif woche in [5, 6]:
                tl_pos = "nach_komplex"
                tl_text = "Absteigende Kaskade: 600m (60%) + 500m (70%) + 400m (70%) + 300m (80%)"
                tl_pause = "100m langsame Gehpause"
            elif woche == 7:
                tl_pos = "nach_komplex"
                tl_text = "KZA Kaskade: 2x 450m + 2x 550m (> 60%) + 100m Gehpause"
                tl_pause = "100m Gehpause"
            elif woche in [8, 9, 10]:
                tl_pos = "vor_komplex"
                tl_text = "GLA vorab: 800m (unter 3:15 min) + 600m, 600m (unter 2:30 min) + 500m vor Stationen"
                tl_pause = "100m Gehpause"
            elif woche == 11:
                tl_pos = "vor_komplex"
                tl_text = "GLA vorab: 800m Basis + 600m, 600m + 500m, 500m (je 100m GP)"
                tl_pause = "100m Gehpause"
            elif woche == 12:
                tl_pos = "nach_komplex"
                tl_text = "Staffel-Ausdauer Kunstrasen: 4x 220m (80%) + 5x 220m (90%)"
                tl_pause = "Staffelpause"
            elif woche == 13:
                tl_pos = "marathon"
                tl_text = "Athletik- & Lauf-Marathon: 3x 400m TL (>50%) + Tartan-Halbmond Parcours"
                tl_pause = "Im Kettenablauf"
            else:
                tl_pos = "nach_komplex"
                tl_text = "Abschlusstest: 60m Sprint + 250m Sprint + 600m Test auf Zeit"
                tl_pause = "Volle Erholung"

        phase_label = "Phase 1: PAP-Komplextraining" if woche <= 7 else "Phase 2: Laktazide Vorab-Ermüdung" if woche <= 11 else "Phase 3: Marathon & Zuspitzung"
        
        row_gla_vorab = ""
        if tl_pos == "vor_komplex":
            row_gla_vorab = f'<tr style="background-color: #FCE4D6;"><td style="padding: 6px 8px; border: 1px solid #D9D9D9; font-weight: bold; color: #C00000;">Block 1: GLA Vorab</td><td style="padding: 6px 8px; border: 1px solid #D9D9D9; font-weight: bold;">{tl_text}</td><td style="padding: 6px 8px; border: 1px solid #D9D9D9; text-align: center;">Serie</td><td style="padding: 6px 8px; border: 1px solid #D9D9D9;">Kaskade vor Kraft</td><td style="padding: 6px 8px; border: 1px solid #D9D9D9;">–</td><td style="padding: 6px 8px; border: 1px solid #D9D9D9;">60-70% Vmax</td><td style="padding: 6px 8px; border: 1px solid #D9D9D9; text-align: center;">{tl_pause}</td></tr>'

        row_tl_transfer = ""
        if tl_pos in ["nach_komplex", "marathon"]:
            row_tl_transfer = f'<tr style="background-color: #FCE4D6;"><td style="padding: 6px 8px; border: 1px solid #D9D9D9; font-weight: bold;">Block 2: Laktat/Lauf</td><td style="padding: 6px 8px; border: 1px solid #D9D9D9;">{tl_text}</td><td style="padding: 6px 8px; border: 1px solid #D9D9D9;">Variabel</td><td style="padding: 6px 8px; border: 1px solid #D9D9D9;">Direct-Transfer</td><td style="padding: 6px 8px; border: 1px solid #D9D9D9;">–</td><td style="padding: 6px 8px; border: 1px solid #D9D9D9;">55-85% Vmax</td><td style="padding: 6px 8px; border: 1px solid #D9D9D9; text-align: center;">{tl_pause}</td></tr>'

        html_matrix = f'''<meta charset="utf-8">
<div class="druck-block" style="background-color: #111111; color: #ffffff; border: 2px solid #45a29e; border-radius: 8px; padding: 20px; margin-top: 20px; font-family: Arial, sans-serif;">
<div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #66fcf1; padding-bottom: 5px;">
<h3 style="margin: 0; color: #66fcf1 !important;">TRAININGSMATRIX - EINHEIT: TE {woche}</h3>
<span style="color: #ffb703; font-weight: bold; font-size: 14px;">{phase_label}</span>
</div>
<p style="color: #ffffff !important; font-size: 14px; margin-top: 8px;"><strong>Athlet:</strong> {ziel} ({gewicht} kg) | <strong>Modus:</strong> {jump_modus} | <strong>Lauf-ABC Last:</strong> {abc_last_str}</p>
<table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 13px; color: #000000; border: 1px solid #7F7F7F;">
<thead>
<tr style="background-color: #1F4E78; color: #FFFFFF; font-weight: bold;">
<th style="padding: 8px; border: 1px solid #7F7F7F; width: 16%;">Block / Phase</th>
<th style="padding: 8px; border: 1px solid #7F7F7F; width: 26%;">Trainingsmittel / Übung</th>
<th style="padding: 8px; border: 1px solid #7F7F7F; width: 7%; text-align: center;">Sätze</th>
<th style="padding: 8px; border: 1px solid #7F7F7F; width: 17%;">Wdh. / Distanz</th>
<th style="padding: 8px; border: 1px solid #7F7F7F; width: 16%;">Hardware / Zusatzlast</th>
<th style="padding: 8px; border: 1px solid #7F7F7F; width: 10%;">Intensität</th>
<th style="padding: 8px; border: 1px solid #7F7F7F; width: 8%; text-align: center;">Pause</th>
</tr>
</thead>
<tbody>
<tr style="background-color: #FFF2CC;">
<td style="padding: 6px 8px; border: 1px solid #D9D9D9; font-weight: bold;">Erwärmung</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9;">800m Stadionrunde (Pacing & Aktivierung)</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9; text-align: center;">1</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9;">800m (unter 3:15 min)</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9;">–</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9;">Zügig</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9; text-align: center;">Trinkp.</td>
</tr>
<tr style="background-color: #DDEBF7;">
<td style="padding: 6px 8px; border: 1px solid #D9D9D9; font-weight: bold;">Block 1: ABC</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9;">Kniehebelauf & Anfersen / Streckbein</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9; text-align: center;">2</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9;">{abc_dist:.1f}m hin / STL zurück</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9; font-weight: bold;">{abc_last_str}</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9;">>80% frequent</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9; text-align: center;">2s</td>
</tr>
{row_gla_vorab}
<tr style="background-color: #BDD7EE;">
<td style="padding: 6px 8px; border: 1px solid #D9D9D9; font-weight: bold;">Komplex: Hürden</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9; font-weight: bold;">Hürden-Tiefsprünge (Reaktiv / DVZ)</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9; text-align: center;">3</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9;">8-12 Hürden ({tief_hoehe})</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9;">{tief_kh}</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9;">Maximal explosiv</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9; text-align: center;">3 Min. SP</td>
</tr>
<tr style="background-color: #FCE4D6;">
<td style="padding: 6px 8px; border: 1px solid #D9D9D9; font-weight: bold;">Komplex: Hex Bar</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9; font-weight: bold;">Kreuzhebe-Streckung (Hex Bar / KB)</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9; text-align: center;">3-4</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9;">8-12 Wdh.</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9; font-weight: bold;">{hex_text}</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9;">Maximal</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9; text-align: center;">{pause_komplex}</td>
</tr>
<tr style="background-color: #FCE4D6;">
<td style="padding: 6px 8px; border: 1px solid #D9D9D9; font-weight: bold;">Komplex: Bags</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9;">Front Squat Jumps / Anreiß-Sprünge</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9; text-align: center;">3</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9; font-weight: bold;">{bag_wdh}</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9; font-weight: bold;">{bag_text}</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9;">Explosiv</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9; text-align: center;">90s</td>
</tr>
<tr style="background-color: #FCE4D6;">
<td style="padding: 6px 8px; border: 1px solid #D9D9D9; font-weight: bold;">Komplex: Bälle</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9;">Umsatz / Ausstoß-Jumps & Crunches</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9; text-align: center;">3</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9;">12-15 Wdh.</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9;">Griffball {gb_last_kg} kg</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9;">Max. Schnellkraft</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9; text-align: center;">60s</td>
</tr>
{row_tl_transfer}
<tr style="background-color: #E2EFDA;">
<td style="padding: 6px 8px; border: 1px solid #D9D9D9; font-weight: bold;">Block 3: Rumpf/TRX</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9;">Zug im Schrägliegehang am TRX / Barren</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9;">3</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9;">12-15 Wdh.</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9;">Körpergewicht</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9;">Submaximal</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9; text-align: center;">60s</td>
</tr>
<tr style="background-color: #F2F2F2;">
<td style="padding: 6px 8px; border: 1px solid #D9D9D9; font-weight: bold;">Cool-Down</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9;">Auslaufen & Statische Tonus-Regulation</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9; text-align: center;">1</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9;">300-400 m</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9;">–</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9;">Sehr locker</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9; text-align: center;">–</td>
</tr>
</tbody>
</table>
</div>'''
        html_matrices += html_matrix

    st.markdown(html_matrices, unsafe_allow_html=True)
    st.markdown("---")

    st.download_button(
        label="💾 Trainingsplan als HTML direkt im Download-Ordner speichern",
        data=html_matrices,
        file_name=f"Doc_Athletic_Trainingsplan_{ziel.replace(' ', '_')}.html",
        mime="text/html; charset=utf-8"
    )

    col_f1, col_f2, col_f3 = st.columns([1, 2, 1])
    with col_f2:
        st.markdown("""<div style="text-align: center; border: 2px solid #45a29e; border-radius: 8px; padding: 15px; background-color: #111111;">
<h2 style="color: #66fcf1 !important; margin-bottom: 5px; font-family: Arial, sans-serif;">Aufgeben gilt nicht!</h2>
<p style="color: #ffb703 !important; font-size: 16px; font-weight: bold; margin: 8px 0;">>>Das, was du fühlst, ist nicht das, was du kannst.<<</p>
<p style="color: #ffffff !important; font-size: 13px; letter-spacing: 1px; margin-top: 5px;">DOC ATHLETIC EVOLUTION 23.8</p>
</div>""", unsafe_allow_html=True)
        lade_bild(["Foto.jpg", "Foto.JPG", "foto.jpg", "foto.JPG", "Foto.jpeg", "foto.jpeg", "Foto.png", "foto.png"], use_col=True)
