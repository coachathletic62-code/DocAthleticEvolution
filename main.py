# ==============================================================================
# DOC ATHLETIC EVOLUTION - MULTI-SPORT MASTER EDITION (Version 22.8)
# Architektur: Vollständiger Quellcode mit strikter ZL-Logik ab U16
# ==============================================================================
import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Doc Athletic Evolution 22.8", layout="wide", initial_sidebar_state="collapsed")

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
.badge-fussball { background-color: #2ecc71; color: #000000; padding: 6px 12px; border-radius: 6px; font-weight: bold; font-size: 15px; display: inline-block; margin-top: 10px; }
.badge-leichtathletik { background-color: #e74c3c; color: #ffffff; padding: 6px 12px; border-radius: 6px; font-weight: bold; font-size: 15px; display: inline-block; margin-top: 10px; }
.badge-basketball { background-color: #3498db; color: #ffffff; padding: 6px 12px; border-radius: 6px; font-weight: bold; font-size: 15px; display: inline-block; margin-top: 10px; }
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
        st.markdown("<p style='text-align: center; color: #c5c6c7; margin-top: 20px;'>Bitte Zugriffscode eingeben</p>", unsafe_allow_html=True)
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
        "Fussball": {
            "Mathilda Karnik": {"alter": 14, "groesse": 1.57, "profil": "Fussball_U15_w", "fasertyp": "Gazelle", "reife": "Spätentwickler (Retardiert)", "sbe": "SR 3", "t_60": 8.90, "t_150": 21.14},
            "Sari Saeland": {"alter": 19, "groesse": 1.58, "profil": "Fussball_U19_w", "fasertyp": "Gazelle", "reife": "Normalentwickler", "sbe": "SR 2", "t_60": 8.00},
            "Ronja Borchmeyer": {"alter": 20, "groesse": 1.70, "profil": "Fussball_U23_w", "fasertyp": "Kraft", "reife": "Normalentwickler", "sbe": "SR 2", "t_60": 8.10},
            "Svenja Poock": {"alter": 20, "groesse": 1.78, "profil": "Fussball_U23_w", "fasertyp": "Kraft", "reife": "Normalentwickler", "sbe": "SR 2", "t_60": 8.30},
            "Nora Giannori": {"alter": 22, "groesse": 1.77, "profil": "Fussball_U23_w", "fasertyp": "Ausdauer", "reife": "Normalentwickler", "sbe": "SR 2", "t_60": 8.40},
            "Mieke Schiemann": {"alter": 24, "groesse": 1.78, "profil": "Fussball_U23_w", "fasertyp": "Ausdauer", "reife": "Normalentwickler", "sbe": "SR 2", "t_60": 8.50},
            "Christoffer Danders": {"alter": 19, "groesse": 1.78, "profil": "Fussball_U19_m", "fasertyp": "Schnelligkeit (Sprint)", "reife": "Normalentwickler", "sbe": "SR 1", "t_60": 7.60}
        },
        "Basketball": {
            "Basketball Talent U13": {"alter": 12, "groesse": 1.62, "profil": "Basketball_U13", "fasertyp": "Sprungkraft", "reife": "Normalentwickler", "sbe": "SR 2-3", "t_60": 7.80}
        },
        "Leichtathletik": {
            "Sprint Talent U17": {"alter": 16, "groesse": 1.75, "profil": "Hochleistung_m", "fasertyp": "Schnelligkeit (Sprint)", "reife": "Normalentwickler", "sbe": "SR 1", "t_60": 7.30}
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
    "Fussball_U19_m": {"sets": 5, "start_m": 25.0, "step_m": 3.0, "sbe_ziel": "SR 1"},
    "Fussball_U19_w": {"sets": 5, "start_m": 22.0, "step_m": 2.5, "sbe_ziel": "SR 1"},
    "Fussball_U23_m": {"sets": 6, "start_m": 28.0, "step_m": 3.0, "sbe_ziel": "SR 1-0"},
    "Fussball_U23_w": {"sets": 6, "start_m": 25.0, "step_m": 2.5, "sbe_ziel": "SR 1-0"},
    "Basketball_U11": {"sets": 3, "start_m": 15.0, "step_m": 2.5, "sbe_ziel": "SR 3"},
    "Basketball_U13": {"sets": 4, "start_m": 15.0, "step_m": 2.0, "sbe_ziel": "SR 2-3"},
    "Basketball_U15_m": {"sets": 4, "start_m": 20.0, "step_m": 2.5, "sbe_ziel": "SR 2"},
    "Basketball_U15_w": {"sets": 4, "start_m": 20.0, "step_m": 2.0, "sbe_ziel": "SR 2"},
    "Basketball_U17_m": {"sets": 5, "start_m": 22.0, "step_m": 3.0, "sbe_ziel": "SR 1-2"},
    "Basketball_U17_w": {"sets": 5, "start_m": 20.0, "step_m": 2.5, "sbe_ziel": "SR 1-2"},
    "Basketball_U19_m": {"sets": 5, "start_m": 25.0, "step_m": 3.0, "sbe_ziel": "SR 1"},
    "Basketball_U19_w": {"sets": 5, "start_m": 22.0, "step_m": 2.5, "sbe_ziel": "SR 1"},
    "Basketball_U23_m": {"sets": 6, "start_m": 28.0, "step_m": 3.0, "sbe_ziel": "SR 1-0"},
    "Basketball_U23_w": {"sets": 6, "start_m": 25.0, "step_m": 2.5, "sbe_ziel": "SR 1-0"},
    "Leichtathletik_U14": {"sets": 4, "start_m": 15.0, "step_m": 2.0, "sbe_ziel": "SR 2-3"},
    "Leichtathletik_U15": {"sets": 4, "start_m": 18.0, "step_m": 2.5, "sbe_ziel": "SR 2"},
    "Leichtathletik_U17_m": {"sets": 5, "start_m": 25.0, "step_m": 3.5, "sbe_ziel": "SR 1-2"},
    "Leichtathletik_U17_w": {"sets": 5, "start_m": 22.0, "step_m": 3.0, "sbe_ziel": "SR 1-2"},
    "Hochleistung_m": {"sets": 6, "start_m": 30.0, "step_m": 3.0, "sbe_ziel": "SR 0"},
    "Hochleistung_w": {"sets": 6, "start_m": 28.0, "step_m": 3.0, "sbe_ziel": "SR 0"}
}

def get_power_bar_last(p_soll, reife_i):
    if "U11" in p_soll:
        base = "Power Bar (3 kg)"
    elif "U13" in p_soll:
        base = "Power Bar (4 kg)"
    elif "U15_w" in p_soll:
        base = "Power Bar (4-6 kg)"
    elif "U15_m" in p_soll:
        base = "Power Bar (6-8 kg)"
    elif "U17" in p_soll or "U19" in p_soll:
        base = "Power Bars (8-10 kg)"
    else:
        base = "Power Bars / Langhantel (10-14 kg)"
    if reife_i == "Spätentwickler":
        return f"{base} (Reduziert)"
    elif reife_i == "Frühentwickler":
        return f"{base} (Erhöht)"
    return base

if st.session_state.auth_modus == "gast":
    st.sidebar.warning("GAST-MODUS (Nur Leserechte)")

if st.session_state.navigations_status == 'Start':
    st.markdown("<h1 style='text-align: center; color: #66fcf1 !important; margin-top: 30px;'>DOC ATHLETIC EVOLUTION 22.8</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #c5c6c7; font-size: 16px;'>Multi-Sport Master Edition (Mit hormoneller Geschlechter-Verknüpfung & strikter Last-Logik)</p>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        lade_bild(["logo.png", "logo.png.png", "logo"], use_col=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.button("SYSTEM INITIALISIEREN >>", on_click=navigiere, args=('Uebersicht',))

elif st.session_state.navigations_status == 'Uebersicht':
    st.title("Systemübersicht & Athleten-Datenbank")
    st.markdown("## Komplex-Training im Nachwuchs bis Hochleistungssport")
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
        st.markdown("## Operative Trainingssteuerung (Multi-Sport)")

    st.markdown("<div class='steuermatrix'>", unsafe_allow_html=True)
    st.markdown("### Biometrische Live-Steuerung & Disziplin-Wahl")
    sport_kategorie = st.radio("Sportart wählen", ["⚽ Fußball", "🏃 Leichtathletik", "🏀 Basketball"], horizontal=True, label_visibility="collapsed")

    if "⚽" in sport_kategorie:
        aktive_kategorie = "Fussball"
        aktive_sport_schluessel = [k for k in abc_parameter.keys() if "Fussball" in k]
        st.markdown("<span class='badge-fussball'>Modul: Fußball aktiv</span>", unsafe_allow_html=True)
    elif "🏃" in sport_kategorie:
        aktive_kategorie = "Leichtathletik"
        aktive_sport_schluessel = [k for k in abc_parameter.keys() if "Leichtathletik" in k or "Hochleistung" in k]
        st.markdown("<span class='badge-leichtathletik'>Modul: Leichtathletik aktiv</span>", unsafe_allow_html=True)
    else:
        aktive_kategorie = "Basketball"
        aktive_sport_schluessel = [k for k in abc_parameter.keys() if "Basketball" in k]
        st.markdown("<span class='badge-basketball'>Modul: Basketball aktiv</span>", unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
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
                aktuelle_daten = {"alter": 16, "groesse": 1.75, "profil": aktive_sport_schluessel[0], "fasertyp": "Schnelligkeit (Sprint)", "reife": "Normalentwickler", "sbe": "SR 2", "t_60": 7.80}
                profil_soll = aktive_sport_schluessel[0]
        else:
            ziel = st.selectbox("Ziel (Kader / Profil)", aktive_sport_schluessel)
            profil_soll = ziel
            aktuelle_daten = {"alter": 16, "groesse": 1.75, "fasertyp": "Schnelligkeit (Sprint)", "reife": "Normalentwickler", "sbe": abc_parameter[ziel]["sbe_ziel"], "t_60": 7.80}

    with c2:
        alter = st.number_input("Alter (Jahre)", min_value=10, max_value=40, value=int(aktuelle_daten["alter"]), disabled=(st.session_state.auth_modus == "gast"))
        # Hormonelle Geschlechter-Anwahl zur Verknüpfung
        geschlecht_wahl = st.selectbox("Geschlecht (Hormoneller Status)", ["Männlich", "Weiblich"], index=1 if "w" in profil_soll or "Weiblich" in str(aktuelle_daten.get("profil","")) else 0)

    with c3:
        groesse = st.number_input("Körpergröße (m)", min_value=1.30, max_value=2.15, value=float(aktuelle_daten["groesse"]), step=0.01, disabled=(st.session_state.auth_modus == "gast"))
        ft_liste = ["Ausdauer", "Kraft", "Sprungkraft", "Gazelle", "Schnelligkeit (Sprint)"]
        reife_liste = ["Spätentwickler (Retardiert)", "Normalentwickler", "Frühentwickler (Akzeleriert)"]
        ft_idx = ft_liste.index(aktuelle_daten["fasertyp"]) if aktuelle_daten["fasertyp"] in ft_liste else 4
        ft = st.selectbox("Fasertyp", ft_liste, index=ft_idx, disabled=(st.session_state.auth_modus == "gast"))

    with c4:
        reife_val = aktuelle_daten["reife"]
        r_idx = 0 if "Spät" in reife_val else 2 if "Früh" in reife_val else 1
        reife = st.selectbox("Entwicklungsstatus", reife_liste, index=r_idx, disabled=(st.session_state.auth_modus == "gast"))
        te_wahl = st.selectbox("Trainingseinheit (TE)", [f"TE {i}" for i in range(1, 15)] + ["Alle TEs (1-14)"])
        sbe_ziel = st.text_input("SBE (Reserve)", value=aktuelle_daten["sbe"], disabled=(st.session_state.auth_modus == "gast"))

    # Automatische Anpassung des Profil-Suffix (_m / _w) basierend auf der Geschlechter-Anwahl
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
        t_150 = st.number_input("150m-Referenz (s)", min_value=15.0, max_value=30.0, value=float(aktuelle_daten.get("150", auto_150) if "150" in aktuelle_daten else auto_150), step=0.01, disabled=(st.session_state.auth_modus == "gast"))

    if modus == "Einzelathlet / Einzelathletin" and st.session_state.auth_modus == "trainer":
        neuer_name = st.text_input("Neuen Athleten-Namen eingeben (zum Anlegen):", value="")
        if st.button("Athleten-Profil in Sektion speichern"):
            ziel_name = neuer_name if neuer_name else ziel
            st.session_state.kader_db[aktive_kategorie][ziel_name] = {
                "alter": int(alter), "groesse": float(groesse), "profil": profil_soll,
                "fasertyp": ft, "reife": reife, "sbe": sbe_ziel, "t_60": float(t_60), "t_150": float(t_150)
            }
            st.success(f"Profil für {ziel_name} in Sportart {aktive_kategorie} erfolgreich angelegt.")
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
    st.subheader(f"Tempotabellen (Echte Live-Korrelation mit 75m-Zwischenwert)")

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
    abc_last_str = "Gewichtsstangen (2 kg)"
    basis_last = get_power_bar_last(profil_soll, reife_intern)

    # Korrektur der Hardware-Last: GZ-Entlastung strikt nur noch bis U15 (<= 14 Jahre) bei retardierter Entwicklung.
    # Ab 15 Jahren (U16+) ausnahmslos "ZL individuell" für Speed Jumper und Squat Master.
    if int(alter) <= 14 and reife_intern == "Spätentwickler":
        block3_zusatz = "GZ Entlastung"
    else:
        block3_zusatz = "ZL individuell"

    for woche in te_liste:
        abc_dist = vorgaben["start_m"] + ((woche - 1) * vorgaben["step_m"])
        curler_wdh = 20 + (woche - 1) * 1
        jumps_wdh = 10 + (woche - 1) * 1

        # Hürden-Progression über 12 Einheiten
        if woche <= 4:
            hurden_text = "2 Serien à 4 Durchgänge (8 Hürden, Höhe 45 cm)"
        elif woche <= 8:
            hurden_text = "2 Serien à 5 Durchgänge (10 Hürden, Höhe 45 cm)"
        else:
            hurden_text = "4 Serien à 2 Durchgänge (8 Hürden, Höhe 55 cm)"

        tl_distanz = 75
        tl_saetze = 4

        html_matrix = f"""
        <div class="druck-block" style="background-color: #111111; color: #ffffff; border: 2px solid #45a29e; border-radius: 8px; padding: 20px; margin-top: 20px; font-family: Arial, sans-serif;">
            <h3 style="border-bottom: 2px solid #66fcf1; padding-bottom: 5px; margin-top: 0; color: #66fcf1 !important;">TRAININGSMATRIX - EINHEIT: TE {woche}</h3>
            <p style="color: #ffffff !important; font-size: 15px;"><strong>Athlet:</strong> {ziel} | <strong>Geschlecht:</strong> {geschlecht_wahl} | <strong>Fasertyp:</strong> {ft} | <strong>SBE-Ziel:</strong> {sbe_ziel}</p>
            <table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 13px; color: #000000; border: 1px solid #7F7F7F;">
              <thead>
                <tr style="background-color: #1F4E78; color: #FFFFFF; font-weight: bold;">
                  <th style="padding: 8px; border: 1px solid #7F7F7F; width: 15%;">Block / Phase</th>
                  <th style="padding: 8px; border: 1px solid #7F7F7F; width: 25%;">Trainingsmittel / Übung</th>
                  <th style="padding: 8px; border: 1px solid #7F7F7F; width: 8%; text-align: center;">Sätze</th>
                  <th style="padding: 8px; border: 1px solid #7F7F7F; width: 14%;">Wdh. / Distanz</th>
                  <th style="padding: 8px; border: 1px solid #7F7F7F; width: 13%;">Zusatzlast (ZL)</th>
                  <th style="padding: 8px; border: 1px solid #7F7F7F; width: 10%;">Intensität</th>
                  <th style="padding: 8px; border: 1px solid #7F7F7F; width: 7%; text-align: center;">Pause</th>
                  <th style="padding: 8px; border: 1px solid #7F7F7F; width: 8%;">SBE(Ist)</th>
                </tr>
              </thead>
              <tbody>
                <tr style="background-color: #FFF2CC;">
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9; font-weight: bold;">Vorbereitung</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9;">Shuttle-Einlaufen (Feldlinien)</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9; text-align: center;">1</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9;">400 m</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9;">–</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9;">Mobilisation</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9; text-align: center;">–</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9;"></td>
                </tr>
                <tr style="background-color: #FFF2CC;">
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9; font-weight: bold;">Vorbereitung</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9;">Spez. Erw. (STL locker/freq.)</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9; text-align: center;">5</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9;">2x100m u 3x60m</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9;">–</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9;">bis 80% Vmax</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9; text-align: center;">Trinkp.</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9;"></td>
                </tr>
                <tr style="background-color: #DDEBF7;">
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9; font-weight: bold;">Block 1: ABC</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9;">Kniehebelauf & Anfersen</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9; text-align: center;">2</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9;">{abc_dist:.1f}m hin/zurück</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9;">{abc_last_str}</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9;">>80% frequent</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9; text-align: center;">2s</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9;"></td>
                </tr>
                <tr style="background-color: #DDEBF7;">
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9; font-weight: bold;">Block 1: ABC</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9;">Nachstellschritte & Überkreuzlauf</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9; text-align: center;">2</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9;">{abc_dist:.1f}m hin/zurück</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9;">–</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9;">>80% dynamisch</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9; text-align: center;">2s</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9;"></td>
                </tr>
                <tr style="background-color: #BDD7EE;">
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9; font-weight: bold;">Block 1: Reiz</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9; font-weight: bold;">Hürdensteigesprünge (Progression)</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9; text-align: center; font-weight: bold;">Variabel</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9;">{hurden_text}</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9;">–</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9;">Maximal explosiv</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9; text-align: center;">3 Min.</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9;">Alpha-Motoneuronen & Koordination</td>
                </tr>
                <tr style="background-color: #FCE4D6;">
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9; font-weight: bold;">Block 2: Komplex</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9;">Squat-Stoß-Jumps</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9; text-align: center;">4</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9;">{jumps_wdh} Wdh.</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9;">{basis_last} (Technik)</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9;">Maximal</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9; text-align: center;">1 min</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9;"></td>
                </tr>
                <tr style="background-color: #FCE4D6;">
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9; font-weight: bold;">Block 2: Komplex</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9;">Speed Jumper / Squat Master</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9; text-align: center;">3</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9;">{jumps_wdh} Wdh.</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9;">{block3_zusatz}</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9;">Explosiv</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9; text-align: center;">90s</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9;"></td>
                </tr>
                <tr style="background-color: #FCE4D6;">
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9; font-weight: bold;">Block 2: Laktat</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9;">Spezifischer Tempolauf-Umfang</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9; text-align: center;">{tl_saetze}</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9;">{tl_distanz}m TL Shuttle</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9;">–</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9;">80% Vmax</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9; text-align: center;">30s Wende</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9;"></td>
                </tr>
                <tr style="background-color: #E2EFDA;">
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9; font-weight: bold;">Block 3: Kraft</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9; font-weight: bold;">Leg Speed Curler (Ischiocrurale Sicherung)</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9; text-align: center; font-weight: bold;">3</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9;">{curler_wdh} Wdh.</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9;">Körpergewicht</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9;">Submaximal</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9; text-align: center;">60s</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9;"></td>
                </tr>
                <tr style="background-color: #F2F2F2;">
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9; font-weight: bold;">Cool-Down</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9;">Auslaufen (Shuttle)</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9; text-align: center;">1</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9;">300m</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9;">–</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9;">Sehr locker</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9; text-align: center;">–</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9;"></td>
                </tr>
                <tr style="background-color: #F2F2F2;">
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9; font-weight: bold;">Cool-Down</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9;">Statische Dehnung (Tonus)</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9; text-align: center;">1</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9;">Individuell</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9;">–</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9;">Passiv</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9; text-align: center;">–</td>
                  <td style="padding: 6px 8px; border: 1px solid #D9D9D9;"></td>
                </tr>
              </tbody>
            </table>
        </div>
        """
        st.markdown(html_matrix, unsafe_allow_html=True)

    st.markdown("---")
    st.download_button(
    label="💾 Trainingsplan als HTML direkt im Download-Ordner speichern",
    data=html_matrix,
    file_name="Doc_Athletic_Trainingsplan.html",
    mime="text/html")

    col_f1, col_f2, col_f3 = st.columns([1, 2, 1])
    with col_f2:
        st.markdown("""<div style="text-align: center; border: 2px solid #45a29e; border-radius: 8px; padding: 15px; background-color: #111111;">
        <h2 style="color: #66fcf1 !important; margin-bottom: 5px; font-family: Arial, sans-serif;">Aufgeben gilt nicht!</h2>
        <p style="color: #ffb703 !important; font-size: 16px; font-weight: bold; margin: 8px 0;">»Das, was du fühlst, ist nicht das, was du kannst.«</p>
        <p style="color: #ffffff !important; font-size: 13px; letter-spacing: 1px; margin-top: 5px;">DOC ATHLETIC EVOLUTION - MULTISPORT</p>
    </div>""", unsafe_allow_html=True)
    lade_bild(["Foto.jpg", "Foto.JPG", "foto.jpg", "foto.JPG", "Foto.jpeg", "foto.jpeg", "Foto.png", "foto.png"], use_col=True)
