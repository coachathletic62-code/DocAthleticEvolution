# =========================================================================
# DOC ATHLETIC EVOLUTION - WEB-VERSION (Streamlit)
# Version 18.28: Inkl. Diagnostik-Modul & geschlechtsspezifischer Enzym-Kompensation
# =========================================================================

import streamlit as st
import json
import os

st.set_page_config(page_title="Doc Athletic Evolution", layout="wide")

st.title("🏃‍♂️ Doc Athletic Evolution - Komplex-Training Steuerung (v18.28)")
st.markdown("---")

KADER_DATEI = "kader_daten.json"
if os.path.exists(KADER_DATEI):
    try:
        with open(KADER_DATEI, "r", encoding="utf-8") as f:
            kader = json.load(f)
    except:
        kader = {}
else:
    kader = {}

# Verbindliche Festlegung der Athleten-Parameter
kader["Matilda Karnik"] = {"alter": 14, "groesse": 1.57, "profil": "Fussball_U15_w", "fasertyp": "Schnelligkeit (Sprint)", "reife": "Retardiert"}
kader["Ronja Borchmeyer"] = {"alter": 15, "groesse": 1.68, "profil": "Fussball_U17_w", "fasertyp": "Sprungkraft", "reife": "Normal"}
kader["Aimie"] = {"alter": 16, "groesse": 1.70, "profil": "Fussball_U17_w", "fasertyp": "Kraft", "reife": "Akzeleriert"}

mannschafts_profile = [
    "Fussball_U11", "Fussball_U13", "Fussball_U15_m", "Fussball_U15_w", 
    "Fussball_U17_m", "Fussball_U17_w", "Fussball_U19_m", "Fussball_U19_w", 
    "Fussball_U23_m", "Fussball_U23_w", 
    "Basketball_U17_m", "Basketball_U17_w", 
    "Leichtathletik_U17_m", "Leichtathletik_U17_w", 
    "Skispringen_U20"
]

fasertypen_liste = ["Ausdauer", "Kraft", "Sprungkraft", "Gazelle", "Schnelligkeit (Sprint)"]
entwicklungs_liste = ["Retardiert", "Normal", "Akzeleriert"]

st.sidebar.header("⚙️ Biometrische Live-Steuerung")
modus = st.sidebar.radio("Steuerungs-Ebene", ["Einzelathlet / Einzelathletin", "Mannschaft / Kader"])

if modus == "Einzelathlet / Einzelathletin":
    ziel = st.sidebar.selectbox("Athlet/in wählen", list(kader.keys()))
    dat = kader[ziel]
    profil = dat["profil"]
    
    ft_wert = dat.get("fasertyp", "Schnelligkeit (Sprint)")
    ft_index = fasertypen_liste.index(ft_wert) if ft_wert in fasertypen_liste else 0
    ft = st.sidebar.selectbox("Fasertyp", fasertypen_liste, index=ft_index)
    
    reife_wert = dat.get("reife", "Normal")
    if reife_wert not in entwicklungs_liste:
        reife_wert = "Normal"
    reife = st.sidebar.selectbox("Reife-Status", entwicklungs_liste, index=entwicklungs_liste.index(reife_wert))
else:
    ziel = st.sidebar.selectbox("Kader / Mannschaft", mannschafts_profile)
    profil = ziel
    ft = st.sidebar.selectbox("Fasertyp", fasertypen_liste)
    reife = st.sidebar.selectbox("Reife-Status", entwicklungs_liste)

te_wahl = st.sidebar.selectbox("Trainingseinheit (TE)", ["Alle TEs (1-14)"] + [f"TE {i}" for i in range(1, 15)])
sbe_wahl = st.sidebar.text_input("SBE (Saubere Reserve)", "SR 2")

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
    elif ft == "Sprungkraft" or ft == "Gazelle": basis -= 0.1
    elif ft == "Kraft": basis += 0.1
    elif ft == "Ausdauer": basis += 0.3

    if reife == "Retardiert": basis += 0.4
    elif reife == "Akzeleriert": basis -= 0.3

    return round(basis, 2)

basis_50m = ermittle_basis_50m(profil, ft, reife)

col1, col2, col3 = st.columns(3)
col1.metric("Aktives Profil", profil)
col2.metric("Fasertyp", ft)
col3.metric("Biometrischer 50m-Benchmark", f"{basis_50m} s")

st.markdown("---")

# =========================================================================
# DIAGNOSTIK-MODUL (Polynomische Regression + Männliche Enzym-Kompensation)
# =========================================================================
st.subheader("🔬 Diagnostik-Modul: Polynomische Sprint-Prognostik")

# Dynamischer Korrekturfaktor für männliche Profile
komp_100 = 0.975 if "_m" in profil else 1.0  # -2.5%
komp_200 = 0.968 if "_m" in profil else 1.0  # -3.2%
komp_300 = 0.963 if "_m" in profil else 1.0  # -3.7%

if "_m" in profil:
    st.info("⚡ Männliche Enzym-Kompensation (Rechtsverschiebung Laktatkurve) ist aktiv.")

diag_col1, diag_col2 = st.columns(2)

with diag_col1:
    st.markdown("**Prognose aus 60m-Referenz**")
    t_60 = st.number_input("Gemessene 60m-Zeit (in Sekunden)", min_value=6.0, max_value=15.0, value=8.13, step=0.01)
    if t_60 > 0:
        prog_100_from_60 = (7.3829 - (0.4319 * t_60) + (0.1394 * (t_60**2))) * komp_100
        prog_200_from_60 = (13.7955 - (0.7205 * t_60) + (0.2806 * (t_60**2))) * komp_200
        st.write(f"➡️ Erwartete 100m-Zeit: **{prog_100_from_60:.2f} s**")
        st.write(f"➡️ Erwartete 200m-Zeit: **{prog_200_from_60:.2f} s**")

with diag_col2:
    st.markdown("**Prognose aus 150m-Referenz**")
    t_150 = st.number_input("Gemessene 150m-Zeit (in Sekunden)", min_value=15.0, max_value=30.0, value=17.80, step=0.01)
    if t_150 > 0:
        prog_100_from_150 = (-2.4964 + (0.9996 * t_150) - (0.0103 * (t_150**2))) * komp_100
        prog_200_from_150 = (12.5421 - (0.0950 * t_150) + (0.0413 * (t_150**2))) * komp_200
        prog_300_from_150 = (-7.8060 + (2.6981 * t_150) - (0.0031 * (t_150**2))) * komp_300
        st.write(f"➡️ Erwartete 100m-Zeit: **{prog_100_from_150:.2f} s**")
        st.write(f"➡️ Erwartete 200m-Zeit: **{prog_200_from_150:.2f} s**")
        st.write(f"➡️ Erwartete 300m-Zeit: **{prog_300_from_150:.2f} s**")

st.markdown("---")
st.subheader("⏱ Dynamische Tempotabelle (Handstopp)")

def format_time(seconds):
    if seconds >= 60:
        m = int(seconds // 60)
        s = seconds % 60
        return f"{m}:{s:04.1f} min"
    return f"{seconds:.1f} s"

distanzen = [50, 100, 150, 200]
table_data = []
for dist_m in distanzen:
    if dist_m == 50: base_s = basis_50m
    elif dist_m == 100: base_s = basis_50m * 1.93
    elif dist_m == 150: base_s = basis_50m * 2.82
    else: base_s = basis_50m * 3.70
    
    row = {"Distanz": f"{dist_m}m"}
    for p in [100, 95, 90, 80, 70, 60]:
        row[f"{p}%"] = format_time(base_s / (p / 100))
    table_data.append(row)

st.table(table_data)

st.markdown("---")
st.subheader(f"📋 Operatives Trainingsprotokoll für: {ziel}")

abc_parameter = {
    "Fussball_U11": {"sets": 3, "start_m": 12.0, "step_m": 2.0},
    "Fussball_U13": {"sets": 4, "start_m": 15.0, "step_m": 2.5},
    "Fussball_U15_m": {"sets": 4, "start_m": 18.0, "step_m": 2.5},
    "Fussball_U15_w": {"sets": 4, "start_m": 16.0, "step_m": 2.0},
    "Fussball_U17_m": {"sets": 5, "start_m": 22.0, "step_m": 3.0},
    "Fussball_U17_w": {"sets": 5, "start_m": 20.0, "step_m": 2.5},
    "Fussball_U19_m": {"sets": 5, "start_m": 25.0, "step_m": 3.0},
    "Fussball_U19_w": {"sets": 5, "start_m": 22.0, "step_m": 2.5},
    "Fussball_U23_m": {"sets": 6, "start_m": 28.0, "step_m": 3.0},
    "Fussball_U23_w": {"sets": 6, "start_m": 25.0, "step_m": 2.5},
    "Basketball_U17_m": {"sets": 5, "start_m": 20.0, "step_m": 3.0},
    "Basketball_U17_w": {"sets": 5, "start_m": 18.0, "step_m": 2.5},
    "Leichtathletik_U17_m": {"sets": 5, "start_m": 25.0, "step_m": 3.5},
    "Leichtathletik_U17_w": {"sets": 5, "start_m": 22.0, "step_m": 3.0},
    "Skispringen_U20": {"sets": 5, "start_m": 22.0, "step_m": 3.0}
}

vorgaben = abc_parameter.get(profil, {"sets": 4, "start_m": 16.0, "step_m": 2.0})
abc_sets = vorgaben["sets"]

te_liste = range(1, 15) if "Alle" in te_wahl else [int(te_wahl.replace("TE ", ""))]

proto_rows = []
for woche in te_liste:
    abc_dist = vorgaben["start_m"] + ((woche - 1) * vorgaben["step_m"])
    if ft == "Ausdauer": abc_dist *= 1.20
    elif ft == "Schnelligkeit (Sprint)": abc_dist *= 0.90

    proto_rows.append({
        "TE": f"TE {woche}",
        "Phase": "Speed Drills & Lauf-ABC",
        "Wdh./Distanz": f"{abc_sets} x {abc_dist:.1f} m",
        "Zusatzlast": "Retardiert -30%" if reife == "Retardiert" else "Standard",
        "SBE": sbe_wahl,
        "Methodische Notiz": f"Fokus: {ft} | Reife: {reife}"
    })

st.table(proto_rows)