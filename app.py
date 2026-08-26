# =========================================================================
# DOC ATHLETIC EVOLUTION - MASTER-ARCHITEKTUR (STREAMLIT v18.29)
# Integration: Visuelles Layout (Logo), Diagnostik (v18.28) & Komplett-Zyklus (v18.25)
# =========================================================================
import streamlit as st
import pandas as pd
import json
import os
import re

# 1. GRUNDEINSTELLUNGEN & DESIGN (Schwarzer Untergrund)
st.set_page_config(page_title="Doc Athletic Evolution", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    .stApp {
        background-color: #000000;
        color: #ffffff;
    }
    .stButton>button {
        background-color: #1f2833;
        color: #66fcf1;
        border: 2px solid #45a29e;
        border-radius: 8px;
        width: 100%;
        font-weight: bold;
    }
    h1, h2, h3, h4, h5, h6, p, div, span, label {
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# 2. SYSTEM-ZUSTAND (NAVIGATION)
if 'navigations_status' not in st.session_state:
    st.session_state.navigations_status = 'Start'

def navigiere(ziel):
    st.session_state.navigations_status = ziel

# 3. KADER-DATENBANK & PARAMETER
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

# 4. HILFSFUNKTIONEN FÜR LAST & PROTOKOLL (Logik 18.25)
def berechne_biologische_last(basis_last_str, is_grosse_uebung, reife):
    zahlen = re.findall(r'\d+', basis_last_str)
    if not zahlen: return basis_last_str
    val = float(zahlen[0]) if len(zahlen) == 1 else (float(zahlen[0]) + float(zahlen[1])) / 2.0
    if reife == "Spätentwickler":
        faktor = 0.70 if is_grosse_uebung else 0.80
        val = val * faktor
        return f"{val:.1f} kg (-30%)" if is_grosse_uebung else f"{val:.1f} kg (-20%)"
    elif reife == "Frühentwickler":
        val = val * 1.15
        return f"{val:.1f} kg (+15%)"
    return basis_last_str

def ermittle_spezifische_last(profil, athlet_name, reife):
    if athlet_name == "Aimie": basis = "14 kg"
    elif "U11" in profil: basis = "1 kg"
    elif "U13" in profil: basis = "3 kg"
    elif "U15_w" in profil: basis = "4 kg"
    elif "U15_m" in profil: basis = "5 kg"
    elif "U17_w" in profil: basis = "6 kg"
    elif "U17_m" in profil: basis = "11 kg"
    else: basis = "14 kg"
    return berechne_biologische_last(basis, True, reife)

def ermittle_stangen_gewicht(profil, reife):
    if "U11" in profil or "U13" in profil: basis = "1.5 kg"
    elif "U15" in profil: basis = "2.0 kg"
    elif "U17" in profil or "U19" in profil: basis = "3.0 kg"
    else: basis = "3.5 kg"
    return berechne_biologische_last(basis, False, reife)

# =========================================================================
# EBENE 1: STARTBILDSCHIRM (Mit Bild-Integration)
# =========================================================================
if st.session_state.navigations_status == 'Start':
    
    # Suchroutine nach der originalen Bilddatei
    bild_datei = None
    for datei in os.listdir("."):
        if datei.lower().endswith(('.png', '.jpg', '.jpeg')):
            bild_datei = datei
            break
            
    if bild_datei:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(bild_datei, use_container_width=True)
    else:
        st.markdown("<p style='text-align: center; color: #ea580c;'>⚠️ Hinweis: Logo/Ellipsen-Datei (.png/.jpg) befindet sich noch nicht im Ordner.</p>", unsafe_allow_html=True)
        
    st.markdown("<h1 style='text-align: center; color: #66fcf1 !important;'>DOC ATHLETIC EVOLUTION</h1>", unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.button("SYSTEM INITIALISIEREN >>", on_click=navigiere, args=('Uebersicht',))

# =========================================================================
# EBENE 2: SYSTEMÜBERSICHT
# =========================================================================
elif st.session_state.navigations_status == 'Uebersicht':
    st.title("Systemübersicht")
    st.markdown("---")
    st.markdown("### Modul-Status:")
    st.write("✅ **Visuelle Architektur:** Geladen (Original Logo & Schwarzer Untergrund)")
    st.write("✅ **Biometrische Datenbank:** Verbunden")
    st.write("✅ **Diagnostik-Prozessor:** Polynomische Regression (v18.28) aktiv")
    st.write("✅ **Makrozyklus-Generator:** Vollständige 14-Wochen-Logik (v18.25) aktiv")
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.button("<< ZURÜCK", on_click=navigiere, args=('Start',))
    with col2:
        st.button("OPERATIVES MENÜ STARTEN >>", on_click=navigiere, args=('Operativ',))

# =========================================================================
# EBENE 3: OPERATIVES MENÜ (Diagnostik & Voller 14-Wochen Makrozyklus)
# =========================================================================
elif st.session_state.navigations_status == 'Operativ':
    st.button("<< ZUR ÜBERSICHT", on_click=navigiere, args=('Uebersicht',))
    st.title("🏃‍♂️ Operative Trainingssteuerung")
    st.markdown("---")

    # SEITENLEISTE (STEUERUNG)
    st.sidebar.header("⚙️ Biometrische Live-Steuerung")
    ziel = st.sidebar.selectbox("Athlet/in wählen", list(kader.keys()) + list(abc_parameter.keys()))
    
    if ziel in kader:
        profil = kader[ziel]["profil"]
        ft = st.sidebar.selectbox("Fasertyp", ["Ausdauer", "Kraft", "Sprungkraft", "Gazelle", "Schnelligkeit (Sprint)"], index=["Ausdauer", "Kraft", "Sprungkraft", "Gazelle", "Schnelligkeit (Sprint)"].index(kader[ziel]["fasertyp"]))
        reife = st.sidebar.selectbox("Reife-Status", ["Spätentwickler", "Normalentwickler", "Frühentwickler"], index=["Spätentwickler", "Normalentwickler", "Frühentwickler"].index(kader[ziel]["reife"]))
    else:
        profil = ziel
        ft = st.sidebar.selectbox("Fasertyp", ["Ausdauer", "Kraft", "Sprungkraft", "Gazelle", "Schnelligkeit (Sprint)"])
        reife = st.sidebar.selectbox("Reife-Status", ["Spätentwickler", "Normalentwickler", "Frühentwickler"])
    
    te_wahl = st.sidebar.selectbox("Trainingseinheit (TE)", ["Alle TEs (1-14)"] + [f"TE {i}" for i in range(1, 15)])
    vorgaben = abc_parameter.get(profil, {"sets": 4, "start_m": 16.0, "step_m": 2.0, "sbe_ziel": "SR 2"})
    sbe_ziel = st.sidebar.text_input("SBE (Saubere Reserve)", vorgaben["sbe_ziel"])

    # DIAGNOSTIK-MODUL (v18.28)
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

    # VOLLSTÄNDIGER TRAININGSPLAN (Logik v18.25)
    st.subheader(f"📋 Operatives Trainingsprotokoll: {ziel}")
    
    basis_last = ermittle_spezifische_last(profil, ziel, reife)
    stangen_gewicht = ermittle_stangen_gewicht(profil, reife)
    is_skisprung = "Skispringen" in profil
    abc_sets = vorgaben["sets"]
    
    te_liste = range(1, 15) if "Alle" in te_wahl else [int(te_wahl.replace("TE ", ""))]
    protokoll = []

    for woche in te_liste:
        abc_dist = vorgaben["start_m"] + ((woche - 1) * vorgaben["step_m"])
        
        # Fasertyp-Anpassungen
        if ft == "Ausdauer":
            abc_dist *= 1.20
            erw_text, sprint_text, sprint_satz, ausdauer_satz = "Erweiterte Shuttle-Aktivierung", "Erhalt-Sprints & aerobe Kapazität", "6 x 30m (Kurze 60s Pause)", "5 x 150m (Tempolauf 70% / 90s)"
            f_notiz = "ST-Dominanz: Erhalt Aerob, Fokus Laktattoleranz"
        elif ft == "Schnelligkeit (Sprint)":
            abc_dist *= 0.90
            erw_text, sprint_text, sprint_satz, ausdauer_satz = "ZNS-Aktivierung & Frequenz-Drills (Gepard)", "Max. Beschleunigung & Peak-Power", "6 x 30m in Spikes (Vollständige 180s Gehpause)", "2 x 100m (Tempolauf 80% / 180s)"
            f_notiz = "Typ 2X/2XX Dominanz: Max. RFD, strenge Laktat-Vermeidung"
        elif ft in ["Sprungkraft", "Gazelle"]:
            erw_text, sprint_text, sprint_satz, ausdauer_satz = "Reaktiv-Aktivierung & Elastizität", "Fliegender Sprint & Sprung-Kombination", "5 x 40m (120s Pause)", "4 x 100m (Tempolauf 75% / 120s)"
            f_notiz = "Elastische Speicherfähigkeit & kurzer DVZ"
        else: # Kraft
            abc_dist *= 0.95
            erw_text, sprint_text, sprint_satz, ausdauer_satz = "Kraft-Mobilisation & Mechanische Spannung", "Beschleunigung gegen Zusatzwiderstand", "4 x 40m (+ Last / 150s Pause)", "4 x 100m (Tempolauf 70% / 150s)"
            f_notiz = "Typ 2A Dominanz: Maximale mechanische Last"

        stange_last = stangen_gewicht if woche <= 6 else "0 kg"
        stange_notiz = f"Zwingend: Stange über Kopf | {f_notiz}" if woche <= 6 else f"Ohne Zusatzlast | {f_notiz}"

        reife_hinweis = " [SCHUTZ: -30% Last]" if reife == "Spätentwickler" else " [AKZELEBRIERT]" if reife == "Frühentwickler" else ""

        # Standard-Block
        protokoll.append({"TE": f"TE {woche}", "Phase": "Erwärmung", "Trainingsmittel": erw_text, "Sätze/Wdh": "1 x 800m", "Soll-Last": "0 kg", "SBE": sbe_ziel, "Notiz": f"Intensität: Moderat{reife_hinweis}"})
        protokoll.append({"TE": f"TE {woche}", "Phase": "Speed Drills", "Trainingsmittel": sprint_text, "Sätze/Wdh": sprint_satz, "Soll-Last": stange_last, "SBE": sbe_ziel, "Notiz": stange_notiz})
        protokoll.append({"TE": f"TE {woche}", "Phase": "Lauf-ABC", "Trainingsmittel": "Kniehebe, Anfersen, Streckbeinlauf", "Sätze/Wdh": f"{abc_sets} x {abc_dist:.1f} m", "Soll-Last": stange_last, "SBE": sbe_ziel, "Notiz": "Technik-Fokus"})

        if is_skisprung:
            if woche <= 4:
                protokoll.append({"TE": f"TE {woche}", "Phase": "Spezifische Hardware", "Trainingsmittel": "Speed Master / Speed Jumper", "Sätze/Wdh": "3 x 8 Jumps", "Soll-Last": "+ 10% KG", "SBE": sbe_ziel, "Notiz": "Fokus: Max. RFD, kurzer DVZ"})
                protokoll.append({"TE": f"TE {woche}", "Phase": "Biomechanik", "Trainingsmittel": "One Leg Jumper (Asymmetrie)", "Sätze/Wdh": "3 x 10 L / 10 R", "Soll-Last": "0 kg", "SBE": sbe_ziel, "Notiz": "Symmetrie Toleranz < 2%"})
            elif woche == 14:
                protokoll.append({"TE": f"TE {woche}", "Phase": "DIAGNOSTIK", "Trainingsmittel": "Leistungs- und Verhaltenskontrolle", "Sätze/Wdh": "Maximal-Test (1RM)", "Soll-Last": "Soll-Werte", "SBE": "SR 0", "Notiz": "Telemark-Tiefsprünge auswerten"})
            else:
                protokoll.append({"TE": f"TE {woche}", "Phase": "Vorermüdung", "Trainingsmittel": "MFT-Board / Slackline", "Sätze/Wdh": "10-15 Min.", "Soll-Last": "0 kg", "SBE": sbe_ziel, "Notiz": "Koordinative Pre-Fatigue"})
        else:
            if woche in [1, 2]:
                protokoll.append({"TE": f"TE {woche}", "Phase": "Sprints", "Trainingsmittel": sprint_text, "Sätze/Wdh": sprint_satz, "Soll-Last": "0 kg", "SBE": sbe_ziel, "Notiz": "Ausführung sauber halten"})
                protokoll.append({"TE": f"TE {woche}", "Phase": "Ausdauer / TL", "Trainingsmittel": "Tempolauf-Pyramide", "Sätze/Wdh": ausdauer_satz, "Soll-Last": "0 kg", "SBE": sbe_ziel, "Notiz": "Pausensteuerung nach Fasertyp"})
                protokoll.append({"TE": f"TE {woche}", "Phase": "Zirkel / Athletik", "Trainingsmittel": "Squat-Stoß-Jumps & Einwurfcrunch", "Sätze/Wdh": "3 x 12 Wdh.", "Soll-Last": basis_last, "SBE": sbe_ziel, "Notiz": f"Umkehrphase steuern{reife_hinweis}"})
                protokoll.append({"TE": f"TE {woche}", "Phase": "Beinachse & Prävention", "Trainingsmittel": "Ausfallschritt-Gehen & LSC", "Sätze/Wdh": "2x20m / 3x20 Wdh.", "Soll-Last": "0 kg / Mod.", "SBE": sbe_ziel, "Notiz": "Fokus Achsenstabilität"})
            elif woche in [3, 4]:
                protokoll.append({"TE": f"TE {woche}", "Phase": "Sprints", "Trainingsmittel": sprint_text, "Sätze/Wdh": sprint_satz, "Soll-Last": "0 kg", "SBE": sbe_ziel, "Notiz": "Gehpause einhalten"})
                protokoll.append({"TE": f"TE {woche}", "Phase": "Ausdauer / TL", "Trainingsmittel": "Tempoläufe (Intervall)", "Sätze/Wdh": ausdauer_satz, "Soll-Last": "0 kg", "SBE": sbe_ziel, "Notiz": "Laktatmanagement"})
                protokoll.append({"TE": f"TE {woche}", "Phase": "Zirkel / Athletik", "Trainingsmittel": "TRX-Zug & Standstoßen", "Sätze/Wdh": "3 x 12 Wdh.", "Soll-Last": f"KG / {basis_last}", "SBE": sbe_ziel, "Notiz": "Explosiv"})
                protokoll.append({"TE": f"TE {woche}", "Phase": "Beinachse & Prävention", "Trainingsmittel": "Einbeinsprünge & LSC", "Sätze/Wdh": "3x20m / 3x22 Wdh.", "Soll-Last": "0 kg / Mod.", "SBE": sbe_ziel, "Notiz": "Isoliert L/R"})
            elif woche in [5, 6, 7]:
                protokoll.append({"TE": f"TE {woche}", "Phase": "Sprints", "Trainingsmittel": sprint_text, "Sätze/Wdh": sprint_satz, "Soll-Last": "0 kg", "SBE": sbe_ziel, "Notiz": "Max. Frequenz"})
                protokoll.append({"TE": f"TE {woche}", "Phase": "Ausdauer / TL", "Trainingsmittel": "Tempoläufe (Erweiterte Serie)", "Sätze/Wdh": ausdauer_satz, "Soll-Last": "0 kg", "SBE": sbe_ziel, "Notiz": "Stoffwechselaktivierung"})
                protokoll.append({"TE": f"TE {woche}", "Phase": "Zirkel / Athletik", "Trainingsmittel": "Front-Squat Jumps & Cheerleading", "Sätze/Wdh": "3 x 12 Wdh.", "Soll-Last": basis_last, "SBE": sbe_ziel, "Notiz": f"Transformation{reife_hinweis}"})
            elif woche in [8, 9]:
                protokoll.append({"TE": f"TE {woche}", "Phase": "Sprints", "Trainingsmittel": "Sprint in Spikes (Start)", "Sätze/Wdh": sprint_satz, "Soll-Last": "0 kg", "SBE": sbe_ziel, "Notiz": "Explosive Phase"})
                protokoll.append({"TE": f"TE {woche}", "Phase": "Ausdauer / TL", "Trainingsmittel": "Tempoläufe (Pyramide)", "Sätze/Wdh": ausdauer_satz, "Soll-Last": "0 kg", "SBE": sbe_ziel, "Notiz": "Pausen sukzessive verkürzen"})
                protokoll.append({"TE": f"TE {woche}", "Phase": "Zirkel / Athletik", "Trainingsmittel": "Anreiß-Sprünge & Einwurfcrunch", "Sätze/Wdh": "3 x 10 Wdh.", "Soll-Last": basis_last, "SBE": sbe_ziel, "Notiz": "Max. ZNS Rekrutierung"})
            elif woche in [10, 11]:
                protokoll.append({"TE": f"TE {woche}", "Phase": "Sprints (Peak)", "Trainingsmittel": "Max. Sprint (100%)", "Sätze/Wdh": sprint_satz, "Soll-Last": "0 kg", "SBE": "SR 1-0", "Notiz": "ZNS Peak"})
                protokoll.append({"TE": f"TE {woche}", "Phase": "Ausdauer / TL", "Trainingsmittel": "Tempoläufe (Intensiv)", "Sätze/Wdh": ausdauer_satz, "Soll-Last": "0 kg", "SBE": "SR 1-0", "Notiz": "Kurze Pausen"})
                protokoll.append({"TE": f"TE {woche}", "Phase": "Zirkel / Athletik", "Trainingsmittel": "Front-Squat Jumps (Max. Speed)", "Sätze/Wdh": "2 x 8 Wdh.", "Soll-Last": basis_last, "SBE": "SR 1-0", "Notiz": "Volumenreduktion, ZL erhöht"})
            elif woche in [12, 13]:
                protokoll.append({"TE": f"TE {woche}", "Phase": "Wettkampf-Tapering", "Trainingsmittel": "Max. Sprint (100%)", "Sätze/Wdh": "4x20m + 2x30m", "Soll-Last": "0 kg", "SBE": "SR 0", "Notiz": "Absolute Dominanz"})
                protokoll.append({"TE": f"TE {woche}", "Phase": "Ausdauer / TL", "Trainingsmittel": "Tempoläufe (Taper)", "Sätze/Wdh": ausdauer_satz, "Soll-Last": "0 kg", "SBE": "SR 0", "Notiz": "Regeneration"})
                protokoll.append({"TE": f"TE {woche}", "Phase": "Zirkel / Athletik", "Trainingsmittel": "Burpees-Master & Anreiß-Sprünge", "Sätze/Wdh": "2 x 8 Wdh.", "Soll-Last": basis_last, "SBE": "SR 0", "Notiz": "Submax. Frequenz"})
            elif woche == 14:
                protokoll.append({"TE": f"TE {woche}", "Phase": "DIAGNOSTIK", "Trainingsmittel": "Leistungs- und Verhaltenskontrolle", "Sätze/Wdh": "300m Parcours", "Soll-Last": "Soll-Werte", "SBE": "SR 0", "Notiz": "TEST-EINHEIT: Werte für nächste Periode ermitteln!"})

        if woche != 14:
            protokoll.append({"TE": f"TE {woche}", "Phase": "Cool-down 1", "Trainingsmittel": "Statische Dehnung", "Sätze/Wdh": "---", "Soll-Last": "0 kg", "SBE": "SR 1", "Notiz": "Zuerst: Muskulatur auf Länge bringen"})
            protokoll.append({"TE": f"TE {woche}", "Phase": "Cool-down 2", "Trainingsmittel": "Lockeres Auslaufen", "Sätze/Wdh": "400 - 800m", "Soll-Last": "0 kg", "SBE": "SR 1", "Notiz": "Stoffwechselabbau / Regeneration"})

    st.dataframe(pd.DataFrame(protokoll), use_container_width=True, hide_index=True)
