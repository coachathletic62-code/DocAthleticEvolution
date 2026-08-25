import streamlit as st

# Seitenkonfiguration
st.set_page_config(
    page_title="Doc Athletic Evolution",
    page_icon="⚡",
    layout="centered"
)

# Zustandsverwaltung für die Navigation
if 'page' not in st.session_state:
    st.session_state.page = 'splash'

# -----------------------------------------------------------------
# STUFE 1: Splash-Screen (Schwarzer Hintergrund & Logo)
# -----------------------------------------------------------------
if st.session_state.page == 'splash':
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #000000;
            color: #ffffff;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    try:
        st.image("logo.png", use_container_width=True)
    except Exception:
        st.warning("Logo logo.png konnte nicht geladen werden.")
        
    st.markdown("<h1 style='text-align: center; color: white;'>Doc Athletic Evolution</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #aaaaaa;'>Trainingssteuerung / Nachwuchs- bis Hochleistungssport</h3>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("SYSTEM STARTEN", type="primary", use_container_width=True):
            st.session_state.page = 'overview'
            st.rerun()

# -----------------------------------------------------------------
# STUFE 2: System- und Makrozyklus-Übersicht (Komplexe & Altersklassen)
# -----------------------------------------------------------------
elif st.session_state.page == 'overview':
    st.title("Doc Athletic Evolution")
    st.subheader("System- und Makrozyklus-Übersicht")
    st.markdown("---")
    
    try:
        st.image("uebersicht.jpg", use_container_width=True)
    except Exception:
        st.warning("Bild uebersicht.jpg konnte nicht geladen werden.")
        
    st.markdown("### 📊 Trainingskomplexe & Leistungsstruktur")
    st.write("Die Plattform basiert ausnahmslos auf der Doc Athletic Train Smart Philosophie zur Steuerung der biologischen und mechanischen Systeme.")
    
    altersklasse = st.selectbox(
        "Zielgruppe / Altersklasse wählen:",
        ["U11", "U13", "U15", "U17", "U20", "U23 / Hochleistungssport"]
    )
    
    st.markdown("---")
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("← Zurück zum Logo"):
            st.session_state.page = 'splash'
            st.rerun()
    with col_b:
        if st.button("Zur Trainingsplanung & Dokumentation →", type="primary"):
            st.session_state.page = 'planning'
            st.rerun()

# -----------------------------------------------------------------
# STUFE 3: Trainingsplanung (Vorbereitung / Soll-Vorgabe)
# -----------------------------------------------------------------
elif st.session_state.page == 'planning':
    if st.button("← Zurück zur Übersicht"):
        st.session_state.page = 'overview'
        st.rerun()
        
    st.markdown("---")
    st.header("Trainingsplanung & Programm-Struktur")
    st.write("Vorbereitung der Trainingseinheit, Auswahl der Trainingsmittel und Tempotabellen.")
    
    st.info("Hier erfolgt die strukturierte Zuweisung der Übungen, Sätze, Wiederholungen und Zusatzlasten gemäß Excel-Vorgabe.")
    
    if st.button("Weiter zum Post-Workout Monitoring (RPE/SBE) →", type="primary"):
        st.session_state.page = 'monitoring'
        st.rerun()

# -----------------------------------------------------------------
# STUFE 4: Post-Workout Monitoring (Operative Erfassung / RPE)
# -----------------------------------------------------------------
elif st.session_state.page == 'monitoring':
    if st.button("← Zurück zur Trainingsplanung"):
        st.session_state.page = 'planning'
        st.rerun()
        
    st.markdown("---")
    st.header("Post-Workout Monitoring (Operative Erfassung)")
    st.write("Nachträgliche Bewertung und Dokumentation nach Abschluss der Belastung.")
    
    rpe = st.slider("SBE / RPE (Subjektives Beanspruchungsempfinden)", 1, 10, 5)
    neuro = st.selectbox("Neuromuskulärer Status", ["Optimale Ansteuerung", "Moderate Latenz", "Neuromuskuläre Ermüdung"])
    morpho = st.selectbox("Muskulärer Status", ["Hypertrophie-Fokus", "Kraftausdauer", "Maximalstärke"])
    
    if st.button("Datensatz abschließend speichern"):
        st.success(f"Trainingseinheit dokumentiert. SBE/RPE: {rpe} | Status: {neuro} / {morpho}")
