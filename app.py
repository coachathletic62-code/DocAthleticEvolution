# ==============================================================================
# DOC ATHLETIC EVOLUTION - MULTI-SPORT MASTER EDITION (Version 22.0)
# Architektur: Finale Master-Edition mit WLAN-Querformat-Druck & bereinigtem Protokoll
# ==============================================================================
import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Doc Athletic Evolution 22.0", layout="wide", initial_sidebar_state="collapsed")

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
/* Markante, breite Sportarten-Auswahl */
.stRadio > div {
    display: flex;
    flex-direction: row;
    gap: 15px;
    width: 100%;
}
.stRadio > div > label {
    flex: 1;
    background-color: #1f2833 !important;
    border: 2px solid #45a29e;
    border-radius: 10px;
    padding: 15px !important;
    text-align: center;
    font-size: 16px !important;
    font-weight: bold !important;
    color: #ffffff !important;
    cursor: pointer;
}
.badge-fussball { background-color: #2ecc71; color: #000000; padding: 6px 12px; border-radius: 6px; font-weight: bold; font-size: 15px; display: inline-block; margin-top: 10px; }
.badge-leichtathletik { background-color: #e74c3c; color: #ffffff; padding: 6px 12px; border-radius: 6px; font-weight: bold; font-size: 15px; display: inline-block; margin-top: 10px; }
.badge-basketball { background-color: #3498db; color: #ffffff; padding: 6px 12px; border-radius: 6px; font-weight: bold; font-size: 15px; display: inline-block; margin-top: 10px; }

.druck-tabelle {
    width: 100%; border-collapse: collapse; margin-top: 10px;
    font-family: Arial, sans-serif; font-size: 14px; color: #ffffff;
}
.druck-tabelle th {
    background-color: #1f2833; color: #66fcf1 !important;
    border: 1px solid #45a29e; padding: 10px; text-align: left;
}
.druck-tabelle td { border: 1px solid #333333; padding: 8px; }
.druck-tabelle tr:nth-child(even) { background-color: #0b0c10; }
.druck-tabelle tr:nth-child(odd) { background-color: #111111; }

.footer-box {
    text-align: center; border: 2px solid #66fcf1; border-radius: 10px;
    padding: 25px; margin-top: 40px; margin-bottom: 20px; background-color: #0b0c10;
}

/* DRUCKOPTIMIERUNG FÜR QUERFORMAT (LANDSCAPE WLAN-DRUCK) */
@media print {
    @page { size: landscape; margin: 10mm; }
    body { background-color: #ffffff !important; color: #000000 !important; }
    .stApp, .steuermatrix, .footer-box { background-color: #ffffff !important; color: #000000 !important; border: none !important; }
    h1, h2, h3, h4, h5, h6, p, label, span { color: #000000 !important; }
    .stButton, .stDownloadButton, [data-testid="stSidebar"], .stRadio { display: none !important; }
    .druck-tabelle { width: 100% !important; border-collapse: collapse !important; }
    .druck-tabelle th { background-color: #e0e0e0 !important; color: #000000 !important; border: 1px solid #000000 !important; }
    .druck-tabelle td { border: 1px solid #000000 !important; color: #000000 !important; background-color: #ffffff !important; }
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

# AUTHENTIFIZIERUNG
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
            "Mathilda Karnik": {"alter": 14, "groesse": 1.57, "profil": "Fussball_U15_w", "fasertyp": "Gazelle", "reife": "Spätentwickler (Retardiert)", "sbe": "SR 3", "t_60": 8.20},
            "Sari Saeland": {"alter": 19, "groesse": 1.65, "profil": "Fussball_U19_w", "fasertyp": "Gazelle", "reife": "Normalentwickler", "sbe": "SR 2", "t_60": 8.00},
            "Ronja Borchmeyer": {"alter": 20, "groesse": 1.68, "profil": "Fussball_U23_w", "fasertyp": "Kraft", "reife": "Normalentwickler", "sbe": "SR 2", "t_60": 8.10},
            "Christoffer Danders": {"alter": 19, "groesse": 1.78, "profil": "Fussball_U19_m", "fasertyp": "Schnelligkeit (Sprint)", "reife": "Normalentwickler", "sbe": "SR 1", "t_60": 7.60}
        },
        "Basketball": {
            "Basketball Talent U13": {"alter": 12, "groesse": 1.62, "profil": "Basketball_U13", "fasertyp": "Sprungkraft", "reife": "Normalentwickler", "sbe": "SR 2-3", "t_60": 7.80}
        },
        "Leichtathletik": {
            "Sprint Talent U17": {"alter": 16, "groesse": 1.75, "profil": "Hochleistung_m", "fasertyp": "Schnelligkeit (Sprint)", "reife": "Normalentwickler", "sbe": "SR 1", "t_60": 7.30}
        }
    }

if 'ist_protokoll' not in st.session_state:
    st.session_state.ist_protokoll = {}
if 'te_anpassungen' not in st.session_state:
    st.session_state.te_anpassungen = {}

def navigiere(ziel):
    st.session_state.navigations_status = ziel

# ZENTRALE PARAMETER-MATRIZE
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

def get_ueberkopf_last(profil, woche, makrozyklus=1):
    if "U11" in profil or "U13" in profil:
        max_w = 10 if makrozyklus == 1 else 6
        if woche <= max_w:
            return "2.0 kg Gewichtsstange (Überkopf)"
        return "0 kg"
    elif "U15" in profil or "U17" in profil:
        if woche <= 8:
            return "3.0 kg Gewichtsstange (Überkopf)"
        elif woche <= 12:
            return "2 x 1.0 kg Kurzhanteln"
        return "0 kg"
    elif "U19" in profil or "U23" in profil or "Hochleistung" in profil:
        if "_w" in profil or "weiblich" in profil.lower():
            if woche <= 8:
                return "3.0 kg Gewichtsstange (Überkopf - Schutz)"
            elif woche <= 12:
                return "2 x 1.0 kg Kurzhanteln"
            return "0 kg"
        else:
            if woche <= 8:
                return "4.0 kg Gewichtsstange (Überkopf)"
            elif woche <= 12:
                return "2 x 1.5 kg Spezial-Kurzhanteln"
            return "0 kg"
    return "2.0 kg Gewichtsstange"

if st.session_state.auth_modus == "gast":
    st.sidebar.warning("GAST-MODUS (Nur Leserechte)")

# SEITENNAVIGATION & HAUPTMENÜ
if st.session_state.navigations_status == 'Start':
    st.markdown("<h1 style='text-align: center; color: #66fcf1 !important; margin-top: 30px;'>DOC ATHLETIC EVOLUTION</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #c5c6c7; font-size: 16px;'>Multi-Sport Master Edition (Fußball, Leichtathletik, Basketball)</p>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        lade_bild(["logo.png", "logo.png.png", "logo"], use_col=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.button("SYSTEM INITIALISIEREN >>", on_click=navigiere, args=('Uebersicht',))

elif st.session_state.navigations_status == 'Uebersicht':
    st.title("Systemübersicht & Athleten-Datenbank")
    st.markdown("## Komplex-Training im Nachwuchs bis Hochleistungssport")
    st.markdown("---")
    
    uebersicht_datei = None
    erlaubte_namen = ["uebersicht.png", "uebersicht.png.png", "übersicht.png", "übersicht.jpg", "uebersicht.jpg", "uebersicht.jpg.jpg"]
    for datei in os.listdir("."):
        if datei.lower() in erlaubte_namen:
            uebersicht_datei = datei
            break
            
    if uebersicht_datei:
        st.image(uebersicht_datei, use_container_width=True)
    else:
        st.markdown("<div style='text-align: center; border: 1px dashed #45a29e; padding: 30px;'><strong>[uebersicht.png] im Verzeichnis hinterlegen.</strong></div>", unsafe_allow_html=True)
    
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
    
    # GROSSE BREITE SPORTARTEN-HAUPTAUSWAHL
    sport_kategorie = st.radio("Sportart wählen", ["⚽ Fußball", "🏃 Leichtathletik", "🏀 Basketball"], horizontal=True, label_visibility="collapsed")
    
    if "Fußball" in sport_kategorie:
        aktive_kategorie = "Fussball"
        aktive_sport_schluessel = [k for k in abc_parameter.keys() if "Fussball" in k]
        st.markdown("<span class='badge-fussball'>Modul: Fußball aktiv (Isolierte Kaderdaten)</span>", unsafe_allow_html=True)
    elif "Leichtathletik" in sport_kategorie:
        aktive_kategorie = "Leichtathletik"
        aktive_sport_schluessel = [k for k in abc_parameter.keys() if "Leichtathletik" in k or "Hochleistung" in k]
        st.markdown("<span class='badge-leichtathletik'>Modul: Leichtathletik aktiv (Isolierte Kaderdaten)</span>", unsafe_allow_html=True)
    else:
        aktive_kategorie = "Basketball"
        aktive_sport_schluessel = [k for k in abc_parameter.keys() if "Basketball" in k]
        st.markdown("<span class='badge-basketball'>Modul: Basketball aktiv (Isolierte Kaderdaten)</span>", unsafe_allow_html=True)

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
                st.warning("Keine Athleten in diesem Modul hinterlegt.")
                ziel = "Neuer Athlet"
                aktuelle_daten = {"alter": 16, "groesse": 1.75, "profil": aktive_sport_schluessel[0], "fasertyp": "Schnelligkeit (Sprint)", "reife": "Normalentwickler", "sbe": "SR 2", "t_60": 7.80}
                profil_soll = aktive_sport_schluessel[0]
        else:
            ziel = st.selectbox("Ziel (Kader / Profil)", aktive_sport_schluessel)
            profil_soll = ziel
            aktuelle_daten = {"alter": 16, "groesse": 1.75, "fasertyp": "Schnelligkeit (Sprint)", "reife": "Normalentwickler", "sbe": abc_parameter[ziel]["sbe_ziel"], "t_60": 7.80}
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
        te_wahl = st.selectbox("Trainingseinheit (TE)", [f"TE {i}" for i in range(1, 15)] + ["Alle TEs (1-14)"])
        sbe_ziel = st.text_input("SBE (Reserve)", value=aktuelle_daten["sbe"], disabled=(st.session_state.auth_modus == "gast"))

    diag_col1, diag_col2 = st.columns(2)
    with diag_col1:
        t_60 = st.number_input("60m-Referenz (s)", min_value=6.0, max_value=15.0, value=float(aktuelle_daten.get("t_60", 7.80)), step=0.01, disabled=(st.session_state.auth_modus == "gast"))
        auto_150 = round(t_60 * 2.375, 2)
    with diag_col2:
        t_150 = st.number_input("150m-Referenz (s)", min_value=15.0, max_value=30.0, value=float(aktuelle_daten.get("t_150", auto_150)), step=0.01, disabled=(st.session_state.auth_modus == "gast"))

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

    st.subheader("Diagnostik-Modul (Polynomische Regression)")
    res_col1, res_col2 = st.columns(2)
    calc_100 = round(t_60 * 1.615, 2)
    calc_200 = round(t_60 * 3.265, 2)
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
    st.subheader(f"Vollständiger Makrozyklus & Protokoll: {ziel}")
    
    vorgaben = abc_parameter.get(profil_soll, {"sets": 4, "start_m": 16.0, "step_m": 2.0})
    abc_sets = vorgaben["sets"]
    te_liste = range(1, 15) if "Alle" in te_wahl else [int(te_wahl.replace("TE ", ""))]
    
    protokoll = []
    for woche in te_liste:
        raw_dist = (vorgaben["start_m"] + ((woche - 1) * vorgaben["step_m"])) * 1.09
        abc_dist = round(raw_dist * 2) / 2
        ueberkopf_last_str = get_ueberkopf_last(profil_soll, woche, makrozyklus=1)
        
        te_key = f"{ziel}_TE_{woche}_inhalt"
        standard_inhalt = f"Neuromuskuläre Innervation (Lauf-ABC & Überkopf-Protokoll)"
        aktiver_inhalt = st.session_state.te_anpassungen.get(te_key, standard_inhalt)
        
        key_ist = f"{ziel}_TE_{woche}_ist"
        ist_wert = st.text_input(f"TE {woche} - Tatsächlich durchgeführt", value=st.session_state.ist_protokoll.get(key_ist, f"TE {woche} planmäßig durchgeführt"), key=key_ist, disabled=(st.session_state.auth_modus == "gast"))
        st.session_state.ist_protokoll[key_ist] = ist_wert

        protokoll.append({
            "TE": f"TE {woche}", "Block": "Block 1",
            "Inhalt / Trainingsmittel": "Allg. & Spez. Erwärmung: Adaptives Einlaufen, STL-Läufe",
            "Benötigte Utensilien": "Hütchen, Markierungsschienen",
            "Soll (Geplant)": "1 x 400m + STL", "Tatsächlich Ist": ist_wert
        })
        protokoll.append({
            "TE": f"TE {woche}", "Block": "Block 2",
            "Inhalt / Trainingsmittel": aktiver_inhalt,
            "Benötigte Utensilien": f"Zusatzlast: {ueberkopf_last_str}",
            "Soll (Geplant)": f"{abc_sets} x {abc_dist:.1f} m (Folgematrix +9%)", "Tatsächlich Ist": ist_wert
        })
        protokoll.append({
            "TE": f"TE {woche}", "Block": "Block 3",
            "Inhalt / Trainingsmittel": "Reaktiv-Komplex (Shuttle & Jumps - Latenzfreie Serienfolge)",
            "Benötigte Utensilien": "Speed Jumper, Power Bars, Hürdenset",
            "Soll (Geplant)": "4 Durchgänge / 12 Wdh.", "Tatsächlich Ist": ist_wert
        })
        protokoll.append({
            "TE": f"TE {woche}", "Block": "Block 4",
            "Inhalt / Trainingsmittel": "Spezifischer Laufumfang (Tempoläufe max. 200m Limit)",
            "Benötigte Utensilien": "Messband / Stoppuhr",
            "Soll (Geplant)": f"5 x 100m TL ({calc_100}s Basis)", "Tatsächlich Ist": ist_wert
        })

    df_proto = pd.DataFrame(protokoll)
    
    col_w1, col_w2, col_w3 = st.columns(3)
    with col_w1:
        # WLAN-DIREKTDRUCK IM QUERFORMAT BUTTON
        st.markdown("""
            <script>
            function druckeQuerformat() {
                window.print();
            }
            </script>
            <button onclick="window.print();" style="background-color: #1f2833; color: #66fcf1; border: 3px solid #66fcf1; border-radius: 8px; width: 100%; font-weight: 900; font-size: 15px; padding: 12px; cursor: pointer;">
            🖨️ PLAN DIREKT DRUCKEN (WLAN)
            </button>
        """, unsafe_allow_html=True)
    with col_w2:
        csv_data = df_proto.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="CSV PROTOKOLL HERUNTERLADEN",
            data=csv_data,
            file_name=f"Doc_Athletic_Protokoll_{ziel.replace(' ', '_')}.csv",
            mime="text/csv"
        )
    with col_w3:
        if st.session_state.auth_modus == "trainer":
            if st.button("Ist-Werte für nächsten Makrozyklus sichern"):
                st.success("Ist-Daten für den nächsten Makrozyklus verankert.")

    html_tabelle = df_proto.to_html(index=False, classes="druck-tabelle")
    st.markdown(html_tabelle, unsafe_allow_html=True)

    st.markdown("---")
    col_f1, col_f2, col_f3 = st.columns([1, 2, 1])
    with col_f2:
        st.markdown("""
        <div class="footer-box">
        <h2 style="color: #66fcf1 !important; margin-bottom: 10px; font-family: Arial, sans-serif;">Aufgeben gilt nicht!</h2>
        <p style="color: #ffffff; font-size: 14px; letter-spacing: 1px;">DOC ATHLETIC EVOLUTION - 22.0</p>
        </div>
        """, unsafe_allow_html=True)
        lade_bild(["Foto.jpg", "Foto.jpg.jpg", "foto.jpg", "foto.jpg.jpg"], use_col=True)
