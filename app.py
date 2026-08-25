import streamlit as st

# Seitenkonfiguration
st.set_page_config(
    page_title="Doc Athletic Evolution",
    page_icon="⚡",
    layout="wide"
)

st.title("Doc Athletic Evolution — Operative Trainingssteuerung")
st.markdown("---")

# Sektion 1: Athleten- und Typisierungsprofil
st.header("1. Athletenprofil & Biologische Typisierung")
col1, col2, col3 = st.columns(3)

with col1:
    athlet_name = st.text_input("Name des Athleten", "Ronja Borchmeyer")
    geschlecht = st.selectbox("Geschlecht", ["Weiblich", "Männlich"])

with col2:
    altersklasse = st.selectbox(
        "Altersklasse / Kader",
        ["U11", "U13", "U15", "U17", "U20", "U23 / Profibereich"]
    )
    biologischer_typ = st.selectbox(
        "Biologischer Reifungsstatus",
        ["Retardiert (Spätentwickler)", "Normal", "Akzeleriert (Frühentwickler)"]
    )

with col3:
    motorig_typ = st.selectbox(
        "Motorischer Bewegungstyp",
        ["Gepard (Sprint- / Explosivkraft-Fokus)", "Gazelle (Ausdauer- / Elastizitäts-Fokus)", "Allrounder"]
    )

st.markdown("---")

# Sektion 2: Trainingskomplexe & Steuerung
st.header("2. Trainingskomplexe & Belastungsparameter")
col_komp1, col_komp2 = st.columns(2)

with col_komp1:
    trainingskomplex = st.selectbox(
        "Wählen Sie den Trainingskomplex",
        [
            "Schnelligkeits-Komplexe (Sprint / Speed Drills)",
            "Neuromuskulärer Komplex (Ansteuerung / Maximalkraft)",
            "Koordinations-Komplex (Technik / Agilität)",
            "Abtöfostölen-Komplex / Spezifische Integration",
            "Rezidivations-Komplex / Prävention"
        ]
    )
    
    uebung = st.selectbox(
        "Spezifisches Trainingsmittel",
        [
            "Front Squat Jumps (Zusatzlast & Peak Power)",
            "One Leg Jumper (Unilaterale Reaktivkraft)",
            "Koordinative Kraft / Kettenintegration",
            "Explosivkraft / Speed Master Olympia",
            "Lauf-ABC & Speed Drills (Kniehebelauf, Anferslauf)"
        ]
    )

with col_komp2:
    saetze = st.number_input("Sätze", min_value=1, max_value=10, value=4)
    wiederholungen = st.number_input("Wiederholungen / Distanz", min_value=1, max_value=100, value=6)
    zusatzlast = st.slider("Zusatzlast / Intensität (%)", 0, 100, 80)
    pause = st.text_input("Pausenlänge", "3 Minuten (vollständige ATP-Resynthese)")

st.markdown("---")

# Sektion 3: Doc Athletic Train Smart Bewertungskriterien (Post-Workout / Status)
st.header("3. Doc Athletic Train Smart — Objektive Bewertungskriterien")
col_bew1, col_bew2, col_bew3, col_bew4 = st.columns(4)

with col_bew1:
    neuro_status = st.selectbox(
        "Neuromuskulärer Status",
        ["Optimale Ansteuerung", "Moderate Latenz", "Ermüdung / Defizit"]
    )

with col_bew2:
    musk_status = st.selectbox(
        "Muskulärer Status",
        ["Morphologie / Hypertrophie", "Kraft / Leistung", "Kraftausdauer"]
    )

with col_bew3:
    rpe_wert = st.slider("Beanspruchungsempfinden (RPE)", 1, 10, 5)

with col_bew4:
    biol_integrität = st.selectbox(
        "Biomechanische Stabilität",
        ["Integrität gewahrt", "Ketteninstabilität", "Kompensation sichtbar"]
    )

st.markdown("---")

# Auswertung und Dokumentation
if st.button("Trainingseinheit final dokumentieren & exportieren", type="primary"):
    st.success(
        f"Datensatz für **{athlet_name}** ({altersklasse}, Typ: **{motorig_typ}**, Reifung: **{biologischer_typ}**) "
        f"erfolgreich erfasst! Komplex: {trainingskomplex} | Übung: {uebung} | RPE: {rpe_wert}"
    )
