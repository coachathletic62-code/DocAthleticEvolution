# =========================================================================
# DOC ATHLETIC EVOLUTION - WEB-MASTER (Version 18.97)
# Architektur: Finale exakte Dateinamens-Zuordnung für GitHub-Videos
# =========================================================================
import streamlit as st
import pandas as pd
import os

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
    .philosophie-box {
        background-color: #0b0c10; border-left: 4px solid #66fcf1;
        padding: 12px; margin-top: 10px; margin-bottom: 15px; font-size: 13px; color: #c5c6c7;
    }
    .video-grid {
        background-color: #111111; border: 2px solid #45a29e; border-radius: 8px;
        padding: 15px; margin-bottom: 15px;
    }
    .footer-box {
        text-align: center; border: 2px solid #66fcf1; border-radius: 10px;
        padding: 25px; margin-top: 40px; margin-bottom: 20px; background-color: #0b0c10;
    }
</style>
""", unsafe_allow_html=True)

GAST_CODE = "gast2026"
TRAINER_CODE = "DocAthletic#2026!"

if 'auth_modus' not in st.session_state:
    st.session_state.auth_modus = None

if 'navigations_status' not in st.session_state:
    st.session_state.navigations_status = 'Start'

if st.session_state.auth_modus is None:
    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    with col_l2:
        try:
            st.image("logo.png", use_container_width=True)
        except:
            st.markdown("<h2 style='text-align: center; color: #66fcf1;'>DOC ATHLETIC</h2>", unsafe_allow_html=True)
            
    st.markdown("<p style='text-align: center; color: #c5c6c7; margin-top: 20px;'>Bitte individuellen Zugriffscode eingeben</p>", unsafe_allow_html=True)
    
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

# Kader-Datenbank mit Mathildas echten Ist-Daten (60m: 8.90s auf Asphalt)
if 'kader_db' not in st.session_state:
    st.session_state.kader_db = {
        "Mathilda Karnik": {"alter": 14, "groesse": 1.57, "profil": "Fussball_U15_w", "fasertyp": "Gazelle", "reife": "Spätentwickler (Retardiert)", "sbe": "SR 3", "t_60": 8.90, "t_150": 21.14},
        "Sari Saeland": {"alter": 19, "groesse": 1.58, "profil": "Fussball_U19_w", "fasertyp": "Gazelle", "reife": "Normalentwickler", "sbe": "SR 2", "t_60": 8.00},
        "Ronja Borchmeyer": {"alter": 20, "groesse": 1.70, "profil": "Fussball_U23_w", "fasertyp": "Kraft", "reife": "Normalentwickler", "sbe": "SR 2", "t_60": 8.10},
        "Svenja Poock": {"alter": 20, "groesse": 1.78, "profil": "Fussball_U23_w", "fasertyp": "Kraft", "reife": "Normalentwickler", "sbe": "SR 2", "t_60": 8.30},
        "Nora Giannori": {"alter": 22, "groesse": 1.77, "profil": "Fussball_U23_w", "fasertyp": "Ausdauer", "reife": "Normalentwickler", "sbe": "SR 2", "t_60": 8.40},
        "Mieke Schiemann": {"alter": 24, "groesse": 1.78, "profil": "Fussball_U23_w", "fasertyp": "Ausdauer", "reife": "Normalentwickler", "sbe": "SR 2", "t_60": 8.50},
        "Christoffer Danders": {"alter": 19, "groesse": 1.78, "profil": "Fussball_U19_m", "fasertyp": "Schnelligkeit (Sprint)", "reife": "Normalentwickler", "sbe": "SR 1", "t_60": 7.60},
        "Matthias Mattusch": {"alter": 14, "groesse": 1.70, "profil": "Fussball_U15_m", "fasertyp": "Schnelligkeit (Sprint)", "reife": "Normalentwickler", "sbe": "SR 2", "t_60": 7.30},
        "Fred Lohmann": {"alter": 19, "groesse": 1.82, "profil": "Leichtathletik_U17_m", "fasertyp": "Schnelligkeit (Sprint)", "reife": "Normalentwickler", "sbe": "SR 1", "t_60": 7.00},
        "Franziska Nimmich": {"alter": 13, "groesse": 1.71, "profil": "Leichtathletik_U14", "fasertyp": "Schnelligkeit (Sprint)", "reife": "Frühentwickler (Akzeleriert)", "sbe": "SR 1", "t_60": 7.90}
    }

if 'ist_protokoll' not in st.session_state:
    st.session_state.ist_protokoll = {}
if 'te_anpassungen' not in st.session_state:
    st.session_state.te_anpassungen = {}
if 'folgemakro_speicher' not in st.session_state:
    st.session_state.folgemakro_speicher = {}

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
    "Fussball_U20_m": {"sets": 5, "start_m": 26.0, "step_m": 3.0, "sbe_ziel": "SR 1"},
    "Fussball_U20_w": {"sets": 5, "start_m": 23.0, "step_m": 2.5, "sbe_ziel": "SR 1"},
    "Fussball_U23_m": {"sets": 6, "start_m": 28.0, "step_m": 3.0, "sbe_ziel": "SR 1-0"},
    "Fussball_U23_w": {"sets": 6, "start_m": 25.0, "step_m": 2.5, "sbe_ziel": "SR 1-0"},
    "Hochleistung_m": {"sets": 6, "start_m": 30.0, "step_m": 3.0, "sbe_ziel": "SR 0"},
    "Hochleistung_w": {"sets": 6, "start_m": 28.0, "step_m": 3.0, "sbe_ziel": "SR 0"}
}

if st.session_state.auth_modus == "gast":
    st.sidebar.warning("🔒 GAST-MODUS (Nur Leserechte, beschränkt auf TE 1 & TE 2)")

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

elif st.session_state.navigations_status == 'Uebersicht':
    st.title("Systemübersicht & Athleten-Datenbank")
    st.markdown("## Komplex-Training im Nachwuchs bis Hochleistungssport (Flagship Variante Premium Plus)")
    st.markdown("---")
    
    uebersicht_datei = None
    for datei in os.listdir("."):
        if datei.lower() in ["übersicht.png", "übersicht.jpg", "uebersicht.png", "uebersicht.jpg"]:
            uebersicht_datei = datei
            break
            
    if uebersicht_datei:
        st.image(uebersicht_datei, use_container_width=True)
    else:
        st.markdown("<div style='text-align: center; border: 1px dashed #45a29e; padding: 30px;'><strong>[Übersicht.png] Bilddatei im Verzeichnis hinterlegen.</strong></div>", unsafe_allow_html=True)
        
    st.markdown("---")
    st.subheader("🎬 Leistungs-Videobibliothek (Exakte Dateinamens-Zuordnung)")
    
    c_v1, c_v2 = st.columns(2)
    
    with c_v1:
        st.markdown("""
        <div class="video-grid">
            <h4 style="color: #66fcf1 !important; margin-top: 0;">1. Front Squat Jumps</h4>
        """, unsafe_allow_html=True)
        if os.path.exists("Front_Squad_Jumps.mp4"):
            st.video("Front_Squad_Jumps.mp4")
        else:
            st.warning("[Front_Squad_Jumps.mp4] nicht im Verzeichnis gefunden.")
        st.markdown("""
            <p><strong>Beanspruchte Muskeln:</strong> Quadriceps femoris, Gluteus maximus, Core/Rumpfstabilisatoren.</p>
            <p><em>Hinweis:</em> Bis U15 m/w ausschließlich Powerbags (5 bis 16 kg) statt freier Langhanteln.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="video-grid">
            <h4 style="color: #66fcf1 !important; margin-top: 0;">2. One Leg Jumper</h4>
        """, unsafe_allow_html=True)
        if os.path.exists("One_Leg_Jumper.mp4"):
            st.video("One_Leg_Jumper.mp4")
        else:
            st.warning("[One_Leg_Jumper.mp4] nicht im Verzeichnis gefunden.")
        st.markdown("""
            <p><strong>Beanspruchte Muskeln:</strong> Einbeinige Streckerkette (Triceps surae, Quadrizeps, Gluteus medius/maximus).</p>
            <p><em>Zweck:</em> Seitensymmetrische Entwicklung der relevanten Muskelgruppen. Koordinative Kraft als Zug-Umsatz-Druck-Variante gegenüber freiem Hantel-Umsatz-Stoß.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="video-grid">
            <h4 style="color: #66fcf1 !important; margin-top: 0;">3. Plyo-Hürden</h4>
        """, unsafe_allow_html=True)
        if os.path.exists("Plyo_Huerd..mp4"):
            st.video("Plyo_Huerd..mp4")
        else:
            st.warning("[Plyo_Huerd..mp4] nicht im Verzeichnis gefunden.")
        st.markdown("""
            <p><strong>Beanspruchte Muskeln:</strong> Reaktiv muskuläre Ketten und intermuskuläre Koordination.</p>
            <p><em>Zweck:</em> Schulung der neuromuskulären Ansteuerung und Frequenzoptimierung.</p>
        </div>
        """, unsafe_allow_html=True)

    with c_v2:
        st.markdown("""
        <div class="video-grid">
            <h4 style="color: #66fcf1 !important; margin-top: 0;">4. Speedmaster</h4>
        """, unsafe_allow_html=True)
        if os.path.exists("SPEED_MASTER.mp4"):
            st.video("SPEED_MASTER.mp4")
        else:
            st.warning("[SPEED_MASTER.mp4] nicht im Verzeichnis gefunden.")
        st.markdown("""
            <p><strong>Beanspruchte Muskeln:</strong> Gesamte kinetische Leistungskette unter Maximallast.</p>
            <p><em>Zweck:</em> Hochleistungs-Spezifische Maximalkraft- und Beschleunigungsentwicklung im Profibereich.</p>
        </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="video-grid">
            <h4 style="color: #66fcf1 !important; margin-top: 0;">5. Zugumsatzstoß</h4>
        """, unsafe_allow_html=True)
        if os.path.exists("Zug_Ums._Stoß.mp4"):
            st.video("Zug_Ums._Stoß.mp4")
        else:
            st.warning("[Zug_Ums._Stoß.mp4] nicht im Verzeichnis gefunden.")
        st.markdown("""
            <p><strong>Beanspruchte Muskeln:</strong> Komplette Streckerkette, Rumpf- und Schultergürtelstabilisatoren.</p>
            <p><em>Zweck:</em> Maximale explosive Kraftübertragung und koordinatives Zusammenspiel im Beschleunigungsverlauf.</p>
        </div>
        </div>
        """, unsafe_allow_html=True)

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
            aktuelle_daten = {"alter": 18, "groesse": 1.70, "fasertyp": "Schnelligkeit (Sprint)", "reife": "Normalentwickler", "sbe": abc_parameter[ziel]["sbe_ziel"], "t_60": 8.00}
            
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
        te_auswahl_liste = [f"TE {i}" for i in range(1, 3)] if st.session_state.auth_modus == "gast" else [f"TE {i}" for i in range(1, 15)] + ["Alle TEs (1-14)"]
        te_wahl = st.selectbox("Trainingseinheit (TE)", te_auswahl_liste)
        sbe_ziel = st.text_input("SBE (Reserve)", value=aktuelle_daten["sbe"], disabled=(st.session_state.auth_modus == "gast"))
        
    diag_col1, diag_col2 = st.columns(2)
    with diag_col1:
        t_60 = st.number_input("60m-Referenz (s)", min_value=6.0, max_value=15.0, value=float(aktuelle_daten.get("t_60", 8.00)), step=0.01, disabled=(st.session_state.auth_modus == "gast"))
    
    auto_150 = round(t_60 * 2.375, 2)
    with diag_col2:
        t_150 = st.number_input("150m-Referenz (s)", min_value=15.0, max_value=30.0, value=float(aktuelle_daten.get("t_150", auto_150)), step=0.01, disabled=(st.session_state.auth_modus == "gast"))
    
    if modus == "Einzelathlet / Einzelathletin" and st.session_state.auth_modus == "trainer":
        col_bs1, col_bs2 = st.columns(2)
        with col_bs1:
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
                st.success(f"Profil, Größe ({groesse}m) und Bestzeiten für {ziel} permanent verankert.")
        with col_bs2:
            if len(st.session_state.kader_db) > 1:
                if st.button(f"🗑️ Athlet {ziel} aus Kader löschen"):
                    del st.session_state.kader_db[ziel]
                    st.success(f"Athlet {ziel} wurde aus der Datenbank entfernt.")
                    st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    reife_intern = "Spätentwickler" if "Spät" in reife else "Frühentwickler" if "Früh" in reife else "Normalentwickler"
    st.subheader("🔬 Diagnostik-Modul (Polynomische Regression)")
    st.markdown("""
    <div class='philosophie-box'>
    <strong>Doc Athletic Arbeitsphilosophie ("der andere Weg"):</strong> Die dargestellten Prognosewerte für den 12-Monats-Entwicklungszeitraum basieren ausnahmslos auf der konsequenten Durchführung der Trainingsplanung, Einhaltung aller ernährungsphysiologischen Vorgaben sowie der obligatorischen Beanspruchungsparameter (Neuromuskulärer Status, Morphologie, SBE/RPE als objektiver Datenpunkt, biomechanische Kettenstabilität).
    </div>
    """, unsafe_allow_html=True)
    if "_w" in profil_soll: st.info("⚡ Weibliche Enzym-Kompensation & Individuelle Kurven-Kalibrierung ist aktiv.")
    elif "_m" in profil_soll: st.info("⚡ Männliche Enzym-Kompensation & Laktat-Rechtsverschiebung ist aktiv.")
        
    res_col1, res_col2 = st.columns(2)
    calc_100 = round(t_60 * 1.615, 2)
    calc_200 = round(t_60 * 3.265, 2)
    with res_col1:
        st.markdown("#### 📌 Aktuelle Ist-Korrelation (Referenzbasis)")
        st.write(f"➡️ 60m: **{t_60:.2f} s** | 100m: **{calc_100:.2f} s** | 150m: **{t_150:.2f} s** | 200m: **{calc_200:.2f} s**")
    with res_col2:
        st.markdown("#### 🎯 12-Monats-Entwicklungsprognose")
        prog_faktor = 0.97 if reife == "Frühentwickler (Akzeleriert)" else 0.98
        p_100 = calc_100 * prog_faktor
        p_200 = calc_200 * prog_faktor
        p_300 = p_200 * 1.48
        st.write(f"➡️ Prognose 100m: **{p_100:.2f} s** | 200m: **{p_200:.2f} s** | 300m: **{p_300:.2f} s**")
    st.markdown("---")
    
    st.subheader(f"⏱ Tempotabellen (Echte Live-Korrelation)")
    def format_time(seconds):
        if seconds >= 60:
            m = int(seconds // 60)
            s = seconds % 60
            return f"{m}:{s:04.1f} min"
        return f"{seconds:.1f} s"
    
    tempo_data = []
    for dist_m in [50, 100, 150, 200]:
        if dist_m == 50:
            base_s = calc_100 / 1.93
        elif dist_m == 100:
            base_s = calc_100
        elif dist_m == 150:
            base_s = t_150
        elif dist_m == 200:
            base_s = calc_200
        
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
    
    if te_wahl != "Alle TEs (1-14)":
        st.subheader(f"📋 Soll/Ist-Abgleich, Utensilien-Logistik & Makrozyklus-Adaption: {ziel} ({te_wahl})")
    else:
        st.subheader(f"📋 Vollständiger Makrozyklus & Adaptive Ist-Rückkopplung: {ziel}")
        
    def get_power_bar_last(p_soll, reife_i):
        if "U11" in p_soll: base = "Powerbag 5-8 kg"
        elif "U13" in p_soll: base = "Powerbag 8-12 kg"
        elif "U15_w" in p_soll: base = "Powerbag 10-14 kg"
        elif "U15_m" in p_soll: base = "Powerbag 12-16 kg"
        elif "U17" in p_soll or "U19" in p_soll: base = "Power Bars (5-8 kg)"
        else: base = "Power Bars / Hanteln (8-12 kg)"
            
        if reife_i == "Spätentwickler": return f"{base} (Reduziert)"
        elif reife_i == "Frühentwickler": return f"{base} (Erhöht)"
        return base

    basis_last = get_power_bar_last(profil_soll, reife_intern)
    stangen_gewicht = "Powerbag 5 kg" if "U11" in profil_soll else "Powerbag 10 kg" if "U15" in profil_soll else "Stange 3 kg"
    if reife_intern == "Spätentwickler": stangen_gewicht += " (Reduziert)"
    
    vorgaben = abc_parameter.get(profil_soll, {"sets": 4, "start_m": 15.0, "step_m": 2.5})
    abc_sets = vorgaben["sets"]
    
    te_liste = range(1, 3) if st.session_state.auth_modus == "gast" and "Alle" not in te_wahl else (range(1, 15) if "Alle" in te_wahl else [int(te_wahl.replace("TE ", ""))])
    protokoll = []
    
    for woche in te_liste:
        abc_dist = vorgaben["start_m"] + ((woche - 1) * vorgaben["step_m"])
        stange_last = stangen_gewicht if woche <= 6 else "0 kg"
        curler_wdh = 20 + (woche - 1) * 1
        jumps_wdh = 10 + (woche - 1) * 1
        
        if int(alter) <= 16:
            tl_distanz = 75 + (woche - 1) * 10
            if tl_distanz > 150: tl_distanz = 150
        else:
            tl_distanz = 75 + (woche - 1) * 25
            if tl_distanz > 200: tl_distanz = 200
            
        tl_saetze = 4 if int(alter) <= 14 else 5
        
        te_key = f"{ziel}_TE_{woche}_inhalt"
        standard_inhalt = f"Neuromuskuläre Innervation (Lauf-ABC & Speed Drills - Adaptiv)"
        aktiver_inhalt = st.session_state.te_anpassungen.get(te_key, standard_inhalt)
        key_ist = f"{ziel}_TE_{woche}_ist"
        ist_wert = st.text_input(f"TE {woche} - Tatsächlich durchgeführt", value=st.session_state.ist_protokoll.get(key_ist, f"TE {woche} planmäßig durchgeführt"), key=key_ist, disabled=(st.session_state.auth_modus == "gast"))
        st.session_state.ist_protokoll[key_ist] = ist_wert
        
        protokoll.append({
            "TE": f"TE {woche}", "Block": "Block 1", 
            "Inhalt / Trainingsmittel": "Allg. & Spez. Erwärmung: Adaptives Shuttle einlaufen, STL-Läufe", 
            "Benötigte Utensilien": "Hütchen, Markierungsschienen", 
            "Soll (Geplant)": "1 x 400m + STL", "Tatsächlich Ist": ist_wert
        })
        protokoll.append({
            "TE": f"TE {woche}", "Block": "Block 2", 
            "Inhalt / Trainingsmittel": aktiver_inhalt, 
            "Benötigte Utensilien": f"Gewichtsstangen ({stange_last})", 
            "Soll (Geplant)": f"{abc_sets} x {abc_dist:.1f} m (Progression +2.5m)", "Tatsächlich Ist": ist_wert
        })
        protokoll.append({
            "TE": f"TE {woche}", "Block": "Block 3", 
            "Inhalt / Trainingsmittel": "Reaktiv-Komplex (Systemwechsel A1/A2: Shuttle, Squat-Jumps & Speed Jumper GZ Entlastung)", 
            "Benötigte Utensilien": f"Speed Jumper (GZ Entlastung), {basis_last}, 55er Hürtenset", 
            "Soll (Geplant)": f"4 Durchgänge / {jumps_wdh} Wdh. (GZ Entlastung steigend)", "Tatsächlich Ist": ist_wert
        })
        protokoll.append({
            "TE": f"TE {woche}", "Block": "Block 4", 
            "Inhalt / Trainingsmittel": "Spezifischer Laufumfang (Tempoläufe nach adaptierter Tempotabelle)", 
            "Benötigte Utensilien": "Messband / Stoppuhr", 
            "Soll (Geplant)": f"{tl_saetze} x {tl_distanz}m TL ({calc_100}s Basis)", "Tatsächlich Ist": ist_wert
        })
        protokoll.append({
            "TE": f"TE {woche}", "Block": "Block 5", 
            "Inhalt / Trainingsmittel": "Unilaterale Belastung & Ischiocrurale Sicherung", 
            "Benötigte Utensilien": "Leg Speed Curler, Kettlebells (2-4 kg)", 
            "Soll (Geplant)": f"3 x {curler_wdh} Wdh. L/R", "Tatsächlich Ist": ist_wert
        })
        protokoll.append({
            "TE": f"TE {woche}", "Block": "Block 6", 
            "Inhalt / Trainingsmittel": "Rumpf- & Oberkörper-Athletik", 
            "Benötigte Utensilien": "Griffbälle (5-7 kg), TRX-Bänder", 
            "Soll (Geplant)": "3 Durchgänge", "Tatsächlich Ist": ist_wert
        })
        
    df_proto = pd.DataFrame(protokoll)
    st.markdown("### ⚙️ Operativer 3-Schritte Protokoll-Workflow")
    
    if st.session_state.auth_modus == "trainer":
        with st.expander("✏️ 1. Soll/Ist-Protokoll & TE-Inhalte überarbeiten", expanded=True):
            col_ed1, col_ed2 = st.columns(2)
            with col_ed1:
                ed_te_num = st.selectbox("Trainingseinheit wählen", [f"TE {i}" for i in range(1, 15)], key="ed_te_box")
            with col_ed2:
                neuer_inhalt = st.text_input("Inhalt / Disziplin anpassen (z.B. 60m Test / Lauf-ABC)", value=aktiver_inhalt, key="ed_inhalt_input")
                
            if st.button("💾 TE-Inhalt permanent aktualisieren"):
                st.session_state.te_anpassungen[f"{ziel}_{ed_te_num}_inhalt"] = neuer_inhalt
                st.success(f"{ed_te_num} erfolgreich aktualisiert.")
                st.rerun()
    else:
        st.info("ℹ️ Gast-Modus aktiv: Bearbeitung von TE-Inhalten nur für lizenzierte Trainer freigeschaltet.")
        
    col_w2, col_w3 = st.columns(2)
    with col_w2:
        st.markdown("**2. Protokoll herunterladen**")
        csv_data = df_proto.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 CSV HERUNTERLADEN",
            data=csv_data,
            file_name=f"Doc_Athletic_Protokoll_{ziel.replace(' ', '_')}.csv",
            mime="text/csv",
            key="download_btn_safe"
        )
        
    with col_w3:
        st.markdown("**3. Folgematrix übertragen**")
        if st.session_state.auth_modus == "trainer":
            if st.button("🚀 Ist-Werte für nächsten Makrozyklus sichern"):
                st.session_state.folgemakro_speicher[ziel] = "übernommen"
                st.success(f"Ist-Daten für {ziel} mit adaptiver Progression für den nächsten Makrozyklus verankert.")
        else:
            st.button("🚀 Ist-Werte für nächsten Makrozyklus sichern", disabled=True)
            st.caption("Nur für lizenzierte Trainer verfügbar.")

    # -------------------------------------------------------------------------
    # DIE 16px DRUCKMATRIX-RENDERLOGIK
    # -------------------------------------------------------------------------
    html_matrices = ""
    for woche in te_liste:
        abc_dist = vorgaben["start_m"] + ((woche - 1) * vorgaben["step_m"])
        stange_last = stangen_gewicht if woche <= 6 else "0 kg"
        curler_wdh = 20 + (woche - 1) * 1
        jumps_wdh = 10 + (woche - 1) * 1
        
        if int(alter) <= 16:
            tl_distanz = 75 + (woche - 1) * 10
            if tl_distanz > 150: tl_distanz = 150
        else:
            tl_distanz = 75 + (woche - 1) * 25
            if tl_distanz > 200: tl_distanz = 200
            
        tl_saetze = 4 if int(alter) <= 14 else 5
        
        html_matrices += f"""
        <div class="druck-block" style="background-color: #ffffff; color: #000000; border: 2px solid #45a29e; border-radius: 8px; padding: 25px; margin-top: 20px; font-family: Arial, sans-serif;">
            <h2 style="border-bottom: 2px solid #000; padding-bottom: 5px; margin-top: 0; color: #000000 !important;">DOC ATHLETIC TRAININGSMATRIX</h2>
            <p style="color: #000000 !important; font-size: 16px;"><strong>Athlet:</strong> {ziel} | <strong>Einheit:</strong> TE {woche} | <strong>Fasertyp:</strong> {ft} | <strong>SBE-Ziel:</strong> {sbe_ziel}</p>
            <table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 16px; color: #000000 !important;">
                <tr style="background-color: #e5e7eb; border-bottom: 2px solid #000;">
                    <th style="padding: 8px; border: 1px solid #000; color: #000000 !important;">Block / Trainingsmittel</th>
                    <th style="padding: 8px; border: 1px solid #000; color: #000000 !important; text-align: center;">Sätze</th>
                    <th style="padding: 8px; border: 1px solid #000; color: #000000 !important;">Strecke/Wdh.</th>
                    <th style="padding: 8px; border: 1px solid #000; color: #000000 !important;">Intensität/Last</th>
                    <th style="padding: 8px; border: 1px solid #000; color: #000000 !important; text-align: center;">Pause</th>
                    <th style="padding: 8px; border: 1px solid #000; color: #000000 !important;">SBE(Ist)</th>
                </tr>
                <tr><td style="padding: 8px; border: 1px solid #000; color: #000000 !important;"><strong>Block 1: Allg. Erwärmung</strong></td><td style="padding: 8px; border: 1px solid #000; color: #000000 !important; text-align: center;">1</td><td style="padding: 8px; border: 1px solid #000; color: #000000 !important;">400m</td><td style="padding: 8px; border: 1px solid #000; color: #000000 !important;">Mobilisation</td><td style="padding: 8px; border: 1px solid #000; color: #000000 !important; text-align: center;">-</td><td style="padding: 8px; border: 1px solid #000; color: #000000 !important;"></td></tr>
                <tr><td style="padding: 8px; border: 1px solid #000; color: #000000 !important;">Spez. Erw. (STL locker/freq.)</td><td style="padding: 8px; border: 1px solid #000; color: #000000 !important; text-align: center;">5</td><td style="padding: 8px; border: 1px solid #000; color: #000000 !important;">2x100m u 3x60m</td><td style="padding: 8px; border: 1px solid #000; color: #000000 !important;">bis 80% Vmax</td><td style="padding: 8px; border: 1px solid #000; color: #000000 !important; text-align: center;">Trinkp.</td><td style="padding: 8px; border: 1px solid #000; color: #000000 !important;"></td></tr>
                <tr><td colspan="6" style="padding: 8px; border: 1px solid #000; background-color: #f9fafb; color: #000000 !important;"><strong>Block 2: Neuromuskuläre Innervation</strong></td></tr>
                <tr><td style="padding: 8px; border: 1px solid #000; color: #000000 !important;">Kniehebelauf & Anfersen</td><td style="padding: 8px; border: 1px solid #000; color: #000000 !important; text-align: center;">2</td><td style="padding: 8px; border: 1px solid #000; color: #000000 !important;">{abc_dist:.1f}m hin/zurück</td><td style="padding: 8px; border: 1px solid #000; color: #000000 !important;">>80% ({stange_last})</td><td style="padding: 8px; border: 1px solid #000; color: #000000 !important; text-align: center;">2s</td><td style="padding: 8px; border: 1px solid #000; color: #000000 !important;"></td></tr>
                <tr><td style="padding: 8px; border: 1px solid #000; color: #000000 !important;">Nachstellschritte & Überkrl.</td><td style="padding: 8px; border: 1px solid #000; color: #000000 !important; text-align: center;">2</td><td style="padding: 8px; border: 1px solid #000; color: #000000 !important;">{abc_dist:.1f}m hin/zurück</td><td style="padding: 8px; border: 1px solid #000; color: #000000 !important;">>80% ({stange_last})</td><td style="padding: 8px; border: 1px solid #000; color: #000000 !important; text-align: center;">2s</td><td style="padding: 8px; border: 1px solid #000; color: #000000 !important;"></td></tr>
                <tr><td colspan="6" style="padding: 8px; border: 1px solid #000; background-color: #f9fafb; color: #000000 !important;"><strong>Block 3: Kompl. Kraftfähigkeiten</strong></td></tr>
                <tr><td style="padding: 8px; border: 1px solid #000; color: #000000 !important;">Squat-Stoß-Jumps</td><td style="padding: 8px; border: 1px solid #000; color: #000000 !important; text-align: center;">4</td><td style="padding: 8px; border: 1px solid #000; color: #000000 !important;">{jumps_wdh} Wdh.</td><td style="padding: 8px; border: 1px solid #000; color: #000000 !important;">{basis_last}</td><td style="padding: 8px; border: 1px solid #000; color: #000000 !important; text-align: center;">1 min</td><td style="padding: 8px; border: 1px solid #000; color: #000000 !important;"></td></tr>
                <tr><td style="padding: 8px; border: 1px solid #000; color: #000000 !important;">Technik Squat Jumps (11°) & Speed Jumper GZ Entlastung</td><td style="padding: 8px; border: 1px solid #000; color: #000000 !important; text-align: center;">3</td><td style="padding: 8px; border: 1px solid #000; color: #000000 !important;">{jumps_wdh} Wdh.</td><td style="padding: 8px; border: 1px solid #000; color: #000000 !important;">Speed Jumper (GZ Entlastung)</td><td style="padding: 8px; border: 1px solid #000; color: #000000 !important; text-align: center;">90s</td><td style="padding: 8px; border: 1px solid #000; color: #000000 !important;"></td></tr>
                <tr><td colspan="6" style="padding: 8px; border: 1px solid #000; background-color: #f9fafb; color: #000000 !important;"><strong>Block 4: Tempoläufe</strong></td></tr>
                <tr><td style="padding: 8px; border: 1px solid #000; color: #000000 !important;">Spezifischer Umfang</td><td style="padding: 8px; border: 1px solid #000; color: #000000 !important; text-align: center;">{tl_saetze}</td><td style="padding: 8px; border: 1px solid #000; color: #000000 !important;">{tl_distanz}m TL</td><td style="padding: 8px; border: 1px solid #000; color: #000000 !important;">80% Vmax (Basis {calc_100:.2f}s)</td><td style="padding: 8px; border: 1px solid #000; color: #000000 !important; text-align: center;">Gehp.</td><td style="padding: 8px; border: 1px solid #000; color: #000000 !important;"></td></tr>
                <tr><td colspan="6" style="padding: 8px; border: 1px solid #000; background-color: #f9fafb; color: #000000 !important;"><strong>Block 5: Ischiocrurale Sicherung</strong></td></tr>
                <tr><td style="padding: 8px; border: 1px solid #000; color: #000000 !important;">Leg Speed Curler</td><td style="padding: 8px; border: 1px solid #000; color: #000000 !important; text-align: center;">3</td><td style="padding: 8px; border: 1px solid #000; color: #000000 !important;">{curler_wdh} Wdh.</td><td style="padding: 8px; border: 1px solid #000; color: #000000 !important;">Körpergewicht</td><td style="padding: 8px; border: 1px solid #000; color: #000000 !important; text-align: center;">60s</td><td style="padding: 8px; border: 1px solid #000; color: #000000 !important;"></td></tr>
                <tr><td colspan="6" style="padding: 8px; border: 1px solid #000; background-color: #d1d5db; color: #000000 !important;"><strong>Block 6: Abwärmen & Regeneration</strong></td></tr>
                <tr><td style="padding: 8px; border: 1px solid #000; color: #000000 !important;">Auslaufen (Shuttle)</td><td style="padding: 8px; border: 1px solid #000; color: #000000 !important; text-align: center;">1</td><td style="padding: 8px; border: 1px solid #000; color: #000000 !important;">300m</td><td style="padding: 8px; border: 1px solid #000; color: #000000 !important;">Sehr locker</td><td style="padding: 8px; border: 1px solid #000; color: #000000 !important; text-align: center;">-</td><td style="padding: 8px; border: 1px solid #000; color: #000000 !important;"></td></tr>
                <tr><td style="padding: 8px; border: 1px solid #000; color: #000000 !important;">Statische Dehnung (Tonus)</td><td style="padding: 8px; border: 1px solid #000; color: #000000 !important; text-align: center;">1</td><td style="padding: 8px; border: 1px solid #000; color: #000000 !important;">Individuell</td><td style="padding: 8px; border: 1px solid #000; color: #000000 !important;">-</td><td style="padding: 8px; border: 1px solid #000; color: #000000 !important; text-align: center;">-</td><td style="padding: 8px; border: 1px solid #000; color: #000000 !important;"></td></tr>
            </table>
            <br>
            <p style="text-align: center; font-size: 14px; margin-bottom: 0; color: #000000 !important;"><em>Doc Athletic Train Smart Philosophie — Aufgeben gilt nicht!</em></p>
        </div>
        """
        
    st.markdown(html_matrices, unsafe_allow_html=True)

    # FINALES ABSCHLUSS-FOTO "Foto.jpg" MIT LEITSPRUCH
    st.markdown("---")
    col_f1, col_f2, col_f3 = st.columns([1, 2, 1])
    with col_f2:
        st.markdown("""
        <div class="footer-box">
            <h2 style="color: #66fcf1 !important; margin-bottom: 10px; font-family: Arial, sans-serif;">Aufgeben gilt nicht!</h2>
            <p style="color: #ffffff; font-size: 14px; letter-spacing: 1px;">DOC ATHLETIC EVOLUTION</p>
        </div>
        """, unsafe_allow_html=True)
        try:
            st.image("Foto.jpg", use_container_width=True)
        except:
            st.markdown("<div style='text-align: center; color: #66fcf1; padding: 10px;'>[Foto.jpg] wird im Hauptverzeichnis gesucht.</div>", unsafe_allow_html=True)
