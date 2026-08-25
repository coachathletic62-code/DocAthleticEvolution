import streamlit as st

# Seitenkonfiguration
st.set_page_config(
    page_title="Doc Athletic Evolution",
    page_icon="⚡",
    layout="centered"
)

# Logo einbinden
try:
    st.image("logo.png", use_container_width=True)
except Exception:
    st.warning("Logo logo.png konnte nicht geladen werden.")

st.title("Doc Athletic Evolution")
st.subheader("Trainingssteuerung / Nachwuchs- bis Hochleistungssport")
st.markdown("---")

# Zustandsverwaltung für die Navigation (Startseite -> Programm)
if 'page' not in st.session_state:
    st.session_state.page = 'start'

if st.session_state.page == 'start':
    st.markdown("### System-Initialisierung")
    st.write("Die Plattform basiert auf der Doc Athletic Train Smart Philosophie.")
    
    if st.button("Programm starten", type="primary"):
        st.session_state.page = 'app'
        st.rerun()

elif st.session_state.page == 'app':
    if st.button("Zurück zur Startseite"):
        st.session_state.page = 'start'
        st.rerun()
        
    st.markdown("---")
    st.header("Operative Trainingssteuerung (v18.28)")
    
    # Bewertungskriterien mit angepasster internationaler Nomenklatur
    rpe = st.slider("SBE / RPE (Subjektives Beanspruchungsempfinden)", 1, 10, 5)
    neuro = st.selectbox("Neuromuskulärer Status", ["Optimale Ansteuerung", "Moderate Latenz", "Neuromuskuläre Ermüdung"])
    morpho = st.selectbox("Muskulärer Status", ["Hypertrophie-Fokus", "Kraftausdauer", "Maximalstärke"])
    
    if st.button("Daten berechnen und dokumentieren"):
        st.success(f"Datensatz erfasst. SBE/RPE: {rpe} | Status: {neuro} / {morpho}")
