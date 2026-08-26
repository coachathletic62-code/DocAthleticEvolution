# =========================================================================
# DOC ATHLETIC EVOLUTION - WEB-ARCHITEKTUR (Master-Synthese)
# Integration: Visuelle Navigation, Diagnostik (v18.28) & Makrozyklus (v18.25)
# =========================================================================
import streamlit as st
import pandas as pd

# 1. GRUNDEINSTELLUNGEN & DESIGN
st.set_page_config(page_title="Doc Athletic Evolution", layout="wide")

st.markdown("""
<style>
    .stApp {
        background-color: #0b0c10;
        color: #c5c6c7;
    }
    h1, h2, h3, h4, h5, h6, p, div, span, label {
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
    }
    .ellipse {
        width: 300px;
        height: 150px;
        background: transparent;
        border: 4px solid #66fcf1;
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 28px;
        font-weight: bold;
        color: #66fcf1;
        box-shadow: 0 0 20px #45a29e;
    }
</style>
""", unsafe_allow_html=True)

# 2. SYSTEM-ZUSTAND (NAVIGATION)
if 'navigations_status' not in st.session_state:
    st.session_state.navigations_status = 'Start'

def navigiere(ziel):
    st.session_state.navigations_status = ziel

# 3. KADER-DATENBANK
kader = {
    "Matilda Karnik": {"alter": 14, "profil": "Fussball_U15_w", "fasertyp": "Schnelligkeit (Sprint)", "reife": "Normalentwickler"},
    "Ronja Borchmeyer": {"alter": 15, "profil": "Fussball_U17_w", "fasertyp": "Sprungkraft", "reife": "Normalentwickler"},
    "Aimie": {"alter": 16, "profil": "Fussball_U17_w", "fasertyp": "Kraft", "reife": "Frühentwickler"}
}

# =========================================================================
# EBENE 1: STARTBILDSCHIRM
# =========================================================================
if st.session_state.navigations_status == 'Start':
    st.markdown("<h1 style='text-align: center; color: #66fcf1 !important;'>DOC ATHLETIC EVOLUTION</h1>", unsafe_allow_html=True)
    st.markdown("<div class='ellipse-container'><div class='ellipse'>Train Smart</div></div>", unsafe_allow_html=True)
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
    st.write("✅ **Visuelle Architektur:** Geladen (Nacht-Modus aktiv)")
    st.write("✅ **Biometrische Datenbank:** Verbunden")
    st.write("✅ **Diagnostik-Prozessor:** Polynomische Regression & Enzym-Kompensation aktiv")
    st.write("✅ **Makrozyklus-Generator:** Logik v18.25 integriert")
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

    # SEITENLEISTE (STEUERUNG)
    st.sidebar.header("⚙️ Biometrische Live-Steuerung")
    ziel = st.sidebar.selectbox("Athlet/in wählen", list(kader.keys()) + ["Fussball_U19_m", "Skispringen_U20"])
    
    if ziel in kader:
        profil = kader[ziel]["profil"]
        ft = st.sidebar.selectbox("Fasertyp", ["Ausdauer", "Kraft", "Sprungkraft", "Gazelle", "Schnelligkeit (Sprint)"], index=["Ausdauer", "Kraft", "Sprungkraft", "Gazelle", "Schnelligkeit (Sprint)"].index(kader[ziel]["fasertyp"]))
        reife = st.sidebar.selectbox("Reife-Status", ["Spätentwickler", "Normalentwickler", "Frühentwickler"], index=["Spätentwickler", "Normalentwickler", "Frühentwickler"].index(kader[ziel]["reife"]))
    else:
        profil = ziel
        ft = st.sidebar.selectbox("Fasertyp", ["Ausdauer", "Kraft", "Sprungkraft", "Gazelle", "Schnelligkeit (Sprint)"])
        reife = st.sidebar.selectbox("Reife-Status", ["Spätentwickler", "Normalentwickler", "Frühentwickler"])
    
    te_wahl = st.sidebar.selectbox("Trainingseinheit (TE)", ["Alle TEs (1-14)"] + [f"TE {i}" for i in range(1, 15)])
    sbe_ziel = st.sidebar.text_input("SBE (Saubere Reserve)", "SR 2")

    # DIAGNOSTIK-MODUL (v18.28)
    st.subheader("🔬 Diagnostik-Modul (Polynomische Regression)")
    komp_100 = 0.975 if "_m" in profil else 1.0  
    komp_200 = 0.968 if "_m" in profil else 1.0  
    komp_300 = 0.963 if "_m" in profil else 1.0  
    
    if "_m" in profil:
        st.info("⚡ Männliche Enzym-Kompensation aktiv.")
        
    diag_col1, diag_col2 = st.columns(2)
    with diag_col1:
        t_60 = st.number_input("60m-Referenz (s)", value=8.13)
        prog_100 = (7.3829 - (0.4319 * t_60) + (0.1394 * (t_60**2))) * komp_100
        prog_200 = (13.7955 - (0.7205 * t_60) + (0.2806 * (t_60**2))) * komp_200
        st.write(f"➡️ Prognose 100m: **{prog_100:.2f} s** | 200m: **{prog_200:.2f} s**")
        
    with diag_col2:
        t_150 = st.number_input("150m-Referenz (s)", value=17.80)
        p_100 = (-2.4964 + (0.9996 * t_150) - (0.0103 * (t_150**2))) * komp_100
        p_200 = (12.5421 - (0.0950 * t_150) + (0.0413 * (t_150**2))) * komp_200
        p_300 = (-7.8060 + (2.6981 * t_150) - (0.0031 * (t_150**2))) * komp_300
        st.write(f"➡️ Prognose 100m: **{p_100:.2f} s** | 200m: **{p_200:.2f} s** | 300m: **{p_300:.2f} s**")

    st.markdown("---")

    # TRAININGSPROTOKOLL GENERIERUNG (v18.25 Logik)
    st.subheader(f"📋 Operatives Trainingsprotokoll: {ziel}")
    
    # Basisdaten festlegen
    abc_sets, abc_dist, step_m = 4, 16.0, 2.0
    basis_last = "4 kg" if "w" in profil else "11 kg"
    if ziel == "Aimie": basis_last = "14 kg"
    stange_last = "2.0 kg" if "w" in profil else "3.0 kg"
    is_skisprung = "Skispringen" in profil
    
    te_liste = range(1, 15) if "Alle" in te_wahl else [int(te_wahl.replace("TE ", ""))]
    protokoll = []

    for woche in te_liste:
        akt_dist = abc_dist + ((woche - 1) * step_m)
        if ft == "Ausdauer": akt_dist *= 1.20
        elif ft == "Schnelligkeit (Sprint)": akt_dist *= 0.90
        
        # Erwärmung & ABC
        protokoll.append({"TE": f"TE {woche}", "Phase": "Erwärmung", "Trainingsmittel": "Aktivierung", "Sätze x Wdh": "1 x 800m", "Last": "0 kg", "SBE": sbe_ziel, "Notiz": f"Fokus: {ft}"})
        protokoll.append({"TE": f"TE {woche}", "Phase": "Lauf-ABC", "Trainingsmittel": "Kniehebe, Anfersen", "Sätze x Wdh": f"{abc_sets} x {akt_dist:.1f} m", "Last": stange_last if woche <=6 else "0 kg", "SBE": sbe_ziel, "Notiz": f"Reife: {reife}"})
        
        if is_skisprung:
            if woche <= 4:
                protokoll.append({"TE": f"TE {woche}", "Phase": "Spezifisch", "Trainingsmittel": "Speed Master / Jumper", "Sätze x Wdh": "3 x 8 Jumps", "Last": "+ 10% KG", "SBE": sbe_ziel, "Notiz": "Fokus: Max. RFD"})
        else:
            if woche in [1, 2, 3, 4]:
                protokoll.append({"TE": f"TE {woche}", "Phase": "Sprints", "Trainingsmittel": "Max. Beschleunigung", "Sätze x Wdh": "6 x 30m", "Last": "0 kg", "SBE": sbe_ziel, "Notiz": "Saubere Ausführung"})
                protokoll.append({"TE": f"TE {woche}", "Phase": "Zirkel", "Trainingsmittel": "Squat-Stoß-Jumps", "Sätze x Wdh": "3 x 12 Wdh.", "Last": basis_last, "SBE": sbe_ziel, "Notiz": "Umkehrphase steuern"})
            elif woche in [5, 6, 7]:
                protokoll.append({"TE": f"TE {woche}", "Phase": "Sprints", "Trainingsmittel": "Sprints", "Sätze x Wdh": "5 x 40m", "Last": "0 kg", "SBE": sbe_ziel, "Notiz": "Max. Frequenz"})
                protokoll.append({"TE": f"TE {woche}", "Phase": "Zirkel", "Trainingsmittel": "Front-Squat Jumps", "Sätze x Wdh": "3 x 12 Wdh.", "Last": basis_last, "SBE": sbe_ziel, "Notiz": "Transformation"})
            elif woche in [10, 11]:
                protokoll.append({"TE": f"TE {woche}", "Phase": "Sprints (Peak)", "Trainingsmittel": "Max. Sprint", "Sätze x Wdh": "4 x 30m", "Last": "0 kg", "SBE": "SR 1-0", "Notiz": "ZNS Peak"})
            elif woche == 14:
                protokoll.append({"TE": f"TE {woche}", "Phase": "DIAGNOSTIK", "Trainingsmittel": "Parcours", "Sätze x Wdh": "Maximal-Test", "Last": "Soll-Werte", "SBE": "SR 0", "Notiz": "TEST-EINHEIT"})

    # Ausgabe als Tabelle
    df = pd.DataFrame(protokoll)
    st.dataframe(df, use_container_width=True, hide_index=True)
