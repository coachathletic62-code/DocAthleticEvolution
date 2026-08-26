# =========================================================================
# DOC ATHLETIC EVOLUTION - WEB-MASTER (Version 18.41)
# Architektur: 3-Stufig | Engine: Vollständige Athleten-Profilbindung (Fasertyp, Reife, SBE, Referenzzeiten)
# =========================================================================
import streamlit as st
import pandas as pd
import os

# 1. VISUELLE ARCHITEKTUR & GRUNDEINSTELLUNGEN
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
    .druck-btn {
        background-color: #ea580c; color: #ffffff; border: none; padding: 12px 20px;
        font-size: 16px; font-weight: bold; border-radius: 8px; cursor: pointer;
        width: 100%; margin-top: 15px; margin-bottom: 15px; text-transform: uppercase;
    }
    .druck-btn:hover { background-color: #c2410c; }
    
    .steuermatrix {
        background-color: #111111; border: 2px solid #333333;
        border-radius: 5px; padding: 15px; margin-bottom: 20px;
    }
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

    @media print {
        .stButton, .stSelectbox, .stTextInput, .stNumberInput, .druck-btn, header, footer { display: none !important; }
        .stApp { background-color: white !important; }
        h1, h2, h3, h4, h5, h6, p, td { color: black !important; }
        .druck-tabelle th { background-color: #dddddd !important; color: black !important; border: 1px solid black; }
        .druck-tabelle td { border: 1px solid black; }
        .steuermatrix { border: none; padding: 0; }
    }
</style>
""", unsafe_allow_html=True)

# 2. SYSTEM-NAVIGATION & INITIALISIERUNG KADER-DB (Inkl. exakter biologischer Profile)
if 'navigations_status' not in st.session_state:
    st.session_state.navigations_status = 'Start'

if 'kader_db' not in st.session_state:
    st.session_state.kader_db = {
        "Mathilda Karnik": {"alter": 14, "groesse": 1.57, "profil": "Fussball_U15_w", "fasertyp": "Gazelle", "reife": "Spätentwickler (Retardiert)", "sbe": "SR 3", "t_60": 8.20, "t_150": 19.50},
        "Sari Saeland": {"alter": 19, "groesse": 1.65, "profil": "Fussball_U19_w", "fasertyp": "Gazelle", "reife": "Normalentwickler", "sbe": "SR 2", "t_60": 8.00, "t_150": 19.00},
        "Ronja Borchmeyer": {"alter": 20, "groesse": 1.68, "profil": "Fussball_U23_w", "fasertyp": "Kraft", "reife": "Normalentwickler", "sbe": "SR 2", "t_60": 8.10, "t_150": 19.20},
        "Svenja Poock": {"alter": 20, "groesse": 1.68, "profil": "Fussball_U23_w", "fasertyp": "Kraft", "reife": "Normalentwickler", "sbe": "SR 2", "t_60": 8.30, "t_150": 19.80},
        "Nora Giannori": {"alter": 22, "groesse": 1.70, "profil": "Fussball_U23_w", "fasertyp": "Ausdauer", "reife": "Normalentwickler", "sbe": "SR 2", "t_60": 8.40, "t_150": 20.00},
        "Mieke Schiemann": {"alter": 24, "groesse": 1.72, "profil": "Fussball_U23_w", "fasertyp": "Ausdauer", "reife": "Normalentwickler", "sbe": "SR 2", "t_60": 8.50, "t_150": 20.20}
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
    "Basketball_U17_m": {"sets": 5, "start_m": 20.0, "step_m": 3.0, "sbe_ziel": "SR 2"},
    "Basketball_U17_w": {"sets": 5, "start_m": 18.0, "step_m": 2.5, "sbe_ziel": "SR 2"},
    "Leichtathletik_U17_m": {"sets": 5, "start_m": 25.0, "step_m": 3.5, "sbe_ziel": "SR 1-2"},
    "Leichtathletik_U17_w": {"sets": 5, "start_m": 22.0, "step_m": 3.0, "sbe_ziel": "SR 1-2"},
    "Skispringen_U20": {"sets": 5, "start_m": 22.0, "step_m": 3.0, "sbe_ziel": "SR 1"},
    "Hochleistung_m": {"sets": 6, "start_m": 30.0, "step_m": 3.0, "sbe_ziel": "SR 0"},
    "Hochleistung_w": {"sets": 6, "start_m": 28.0, "step_m": 3.0, "sbe_ziel": "SR 0"}
}

# =========================================================================
# EBENE 1: STARTBILDSCHIRM
# =========================================================================
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

# =========================================================================
# EBENE 2: SYSTEMÜBERSICHT
# =========================================================================
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

# =========================================================================
# EBENE 3: OPERATIVE MASKE
# =========================================================================
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
            aktuelle_daten = {"alter": 18, "groesse": 1.70, "fasertyp": "Schnelligkeit (Sprint)", "reife": "Normalentwickler", "sbe": abc_parameter[ziel]["sbe_ziel"], "t_60": 8.00, "t_150": 19.00}
            
    with c2:
        alter = st.number_input("Alter (Jahre)", min_value=10, max_value=40, value=int(aktuelle_daten["alter"]))
        groesse = st.number_input("Körpergröße (m)", min_value=1.30, max_value=2.15, value=float(aktuelle_daten["groesse"]), step=0.01)

    with c3:
        ft_liste = ["Ausdauer", "Kraft", "Sprungkraft", "Gazelle", "Schnelligkeit (Sprint)"]
        reife_liste = ["Spätentwickler (Retardiert)", "Normalentwickler", "Frühentwickler (Akzeleriert)"]
        
        ft_idx = ft_liste.index(aktuelle_daten["fasertyp"]) if aktuelle_daten["fasertyp"] in ft_liste else 4
        ft = st.selectbox("Fasertyp", ft_liste, index=ft_idx)
        
        reife_val = aktuelle_daten["reife"]
        r_idx = 0 if "Spät" in reife_val else 2 if "Früh" in reife_val else 1
        reife = st.selectbox("Entwicklungsstatus", reife_liste, index=r_idx)
            
    with c4:
        te_wahl = st.selectbox("Trainingseinheit (TE)", ["Alle TEs (1-14)"] + [f"TE {i}" for i in range(1, 15)])
        sbe_ziel = st.text_input("SBE (Reserve)", value=aktuelle_daten["sbe"])
        
    # DIAGNOSTIK REFERENZZEITEN (Eingebunden in den Speicher-Zyklus)
    diag_col1, diag_col2 = st.columns(2)
    with diag_col1:
        t_60 = st.number_input("60m-Referenz (s)", min_value=6.0, max_value=15.0, value=float(aktuelle_daten.get("t_60", 7.99)), step=0.01)
    with diag_col2:
        t_150 = st.number_input("150m-Referenz (s)", min_value=15.0, max_value=30.0, value=float(aktuelle_daten.get("t_150", 19.50)), step=0.01)

    if modus == "Einzelathlet / Einzelathletin":
        if st.button("💾 Athleten-Profil & Bestzeiten permanent speichern"):
            st.session_state.kader_db[ziel] = {
                "alter": int(alter),
                "groesse": float(groesse),
                "profil": profil_soll,
                "fasertyp": ft,
                "reife": reife,
                "sbe": sbe_ziel,
                "t_60": float(t_60),
                "t_150": float(t_150)
            }
            st.success(f"Profil und Referenzwerte für {ziel} erfolgreich permanent verankert.")

    st.markdown("</div>", unsafe_allow_html=True)

    with st.expander("➕ Neuen Athleten / Neue Athletin in Kader aufnehmen"):
        neu_name = st.text_input("Vollständiger Name")
        nc1, nc2, nc3 = st.columns(3)
        with nc1:
            neu_alter = st.number_input("Alter", min_value=10, max_value=40, value=18, key="n_alt")
            neu_groesse = st.number_input("Größe (m)", min_value=1.30, max_value=2.15, value=1.70, step=0.01, key="n_gro")
        with nc2:
            neu_profil = st.selectbox("Zuordnungs-Profil", list(abc_parameter.keys()), key="n_pro")
            neu_ft = st.selectbox("Fasertyp", ["Ausdauer", "Kraft", "Sprungkraft", "Gazelle", "Schnelligkeit (Sprint)"], key="n_ft")
        with nc3:
            neu_reife = st.selectbox("Entwicklungsstatus", ["Spätentwickler (Retardiert)", "Normalentwickler", "Frühentwickler (Akzeleriert)"], key="n_rei")
            neu_sbe = st.text_input("Standard SBE", value="SR 2", key="n_sbe")
            
        if st.button("Athlet anlegen & in Datenbank verankern"):
            if neu_name.strip():
                st.session_state.kader_db[neu_name.strip()] = {
                    "alter": int(neu_alter),
                    "groesse": float(neu_groesse),
                    "profil": neu_profil,
                    "fasertyp": neu_ft,
                    "reife": neu_reife,
                    "sbe": neu_sbe,
                    "t_60": 8.00,
                    "t_150": 19.50
                }
                st.success(f"Athletin {neu_name.strip()} erfolgreich angelegt.")
                st.rerun()
            else:
                st.error("Bitte einen gültigen Namen eingeben.")

    reife_intern = "Spätentwickler" if "Spät" in reife else "Frühentwickler" if "Früh" in reife else "Normalentwickler"

    # DIAGNOSTIK-MODUL AUSFÜHRUNG
    st.subheader("🔬 Diagnostik-Modul (Polynomische Regression)")
    if "_w" in profil_soll: st.info("⚡ Weibliche Enzym-Kompensation & Individuelle Kurven-Kalibrierung ist aktiv.")
        
    res_col1, res_col2 = st.columns(2)
    with res_col1:
        if t_60 > 0:
            if "_w" in profil_soll:
                prog_100 = 12.61 + ((t_60 - 7.99) * 2.55)
                prog_200 = 27.00 + ((t_60 - 7.99) * 5.0)
            else:
                prog_100 = (7.3829 - (0.4319 * t_60) + (0.1394 * (t_60**2)))
                prog_200 = (13.7955 - (0.7205 * t_60) + (0.2806 * (t_60**2)))
            st.write(f"➡️ Prognose 100m: **{prog_100:.2f} s** | 200m: **{prog_200:.2f} s**")
            
    with res_col2:
        if t_150 > 0:
            if "_w" in profil_soll:
                p_100 = (-2.4964 + (0.9996 * t_150) - (0.0103 * (t_150**2))) * 0.98 
                p_200 = (12.5421 - (0.0950 * t_150) + (0.0413 * (t_150**2))) * 1.045
                p_300 = (-7.8060 + (2.6981 * t_150) - (0.0031 * (t_150**2))) * 1.060
            else:
                p_100 = (-2.4964 + (0.9996 * t_150) - (0.0103 * (t_150**2))) 
                p_200 = (12.5421 - (0.0950 * t_150) + (0.0413 * (t_150**2))) 
                p_300 = (-7.8060 + (2.6981 * t_150) - (0.0031 * (t_150**2)))
            st.write(f"➡️ Prognose 100m: **{p_100:.2f} s** | 200m: **{p_200:.2f} s** | 300m: **{p_300:.2f} s**")

    st.markdown("---")

    # TEMPOTABELLEN (Absolut synchronisiert)
    st.subheader(f"⏱ Tempotabellen (Exakt gekoppelt an Live-Prognose)")
    def format_time(seconds):
        if seconds >= 60:
            m = int(seconds // 60)
            s = seconds % 60
            return f"{m}:{s:04.1f} min"
        return f"{seconds:.1f} s"

    tempo_data = []
    for dist_m in [50, 100, 150, 200]:
        if dist_m == 50:
            base_s = prog_100 / 1.93
        elif dist_m == 100:
            base_s = prog_100
        elif dist_m == 150:
            base_s = t_150  # Direkte Koppelung an die gespeicherte/eingetragene 150m-Referenz
        elif dist_m == 200:
            base_s = prog_200
        
        row = {
            "Distanz": f"{dist_m}m", 
            "100%": format_time(base_s), 
            "95%": format_time(base_s/0.95), 
            "90%": format_time(base_s/0.90), 
            "80%": format_time(base_s/0.80), 
            "70%": format_time(base_s/0.70)
        }
        tempo_data.append(row)
    
    st.table(pd.DataFrame(tempo_data).set_index("Distanz"))

    st.markdown("---")

    # DRUCK-BUTTON
    st.markdown('<button onclick="window.print()" class="druck-btn">🖨️ Trainingsprotokoll drucken</button>', unsafe_allow_html=True)

    # TRAININGSPLAN GENERIERUNG
    if te_wahl != "Alle TEs (1-14)":
        st.subheader(f"📋 Operatives Trainingsprotokoll: {ziel} ({te_wahl})")
    else:
        st.subheader(f"📋 Operativer 14-Wochen Makrozyklus: {ziel}")
        
    def calc_last(base_str, is_gross):
        if reife_intern == "Spätentwickler":
            return f"Reduziert (-30%)" if is_gross else f"Reduziert (-20%)"
        elif reife_intern == "Frühentwickler":
            return f"Erhöht (+15%)"
        return base_str

    basis_last = "12-16 kg" if ziel == "Aimie" else "0-1 kg" if "U11" in profil_soll else "2-3 kg" if "U13" in profil_soll else "3-5 kg" if "U15_w" in profil_soll else "4-6 kg" if "U15_m" in profil_soll else "5-8 kg" if "U17_w" in profil_soll else "10-12 kg"
    basis_last = calc_last(basis_last, True)

    stangen_gewicht = "1.5 kg" if "U11" in profil_soll or "U13" in profil_soll else "2.0 kg" if "U15" in profil_soll else "3.0 kg"
    stangen_gewicht = calc_last(stangen_gewicht, False)

    is_skisprung = "Skispringen" in profil_soll
    vorgaben = abc_parameter.get(profil_soll, {"sets": 4, "start_m": 16.0, "step_m": 2.0})
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

    # HTML Rendering
    df_proto = pd.DataFrame(protokoll)
    html_tabelle = df_proto.to_html(index=False, classes="druck-tabelle")
    st.markdown(html_tabelle, unsafe_allow_html=True)
