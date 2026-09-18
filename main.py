# ============================================================================
# DOC ATHLETIC EVOLUTION - FUSSBALL & LEICHTATHLETIK (Version 23.8.2)
# Stand 18.09.2026: Wochensteuerung, Trainerregeln, geprüfte Speicherung, Demo-Modus
# ============================================================================

import streamlit as st
import pandas as pd
import os
import json
import sqlite3
import math
from pathlib import Path
from copy import deepcopy
from html import escape
import hashlib
import hmac
from contextlib import contextmanager, closing

st.set_page_config(page_title="Doc Athletic Evolution 23.8.2", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
.stApp { background-color: #000000; color: #ffffff; }
h1, h2, h3, h4, h5, h6, p, label { color: #ffffff !important; }
button[title="View fullscreen"] { display: none !important; }

/* Eingabefelder */
.stSelectbox > div > div, .stTextInput > div > div > input, .stNumberInput > div > div > input {
    background-color: #ffffff !important;
    color: #000000 !important;
}

/* Buttons */
.stButton>button {
    background-color: #1f2833; color: #66fcf1;
    border: 2px solid #45a29e; border-radius: 8px;
    width: 100%; font-weight: bold;
}
div.stDownloadButton > button {
    background-color: #66fcf1 !important;
    border: 2px solid #45a29e !important;
    border-radius: 8px !important;
    width: 100% !important;
    padding: 12px !important;
}
div.stDownloadButton > button *,
div.stDownloadButton > button p,
div.stDownloadButton > button span {
    color: #000000 !important;
    font-weight: 900 !important;
    font-size: 15px !important;
}

/* Peppiges High-Performance Steuerungs-Panel */
.steuermatrix {
    background: linear-gradient(145deg, #10161d, #07090c);
    border: 2px solid #66fcf1;
    box-shadow: 0 0 25px rgba(102, 252, 241, 0.25);
    border-radius: 12px;
    padding: 25px;
    margin-bottom: 25px;
}

/* Zentrierte und vergrößerte Sportarten-Wahl */
div[role="radiogroup"] {
    justify-content: center !important;
    gap: 30px !important;
    margin: 15px 0 !important;
}
div[role="radiogroup"] label {
    background-color: #1f2833 !important;
    padding: 12px 28px !important;
    border-radius: 10px !important;
    border: 2px solid #45a29e !important;
    cursor: pointer !important;
    transition: all 0.25s ease-in-out !important;
}
div[role="radiogroup"] label:hover {
    border-color: #66fcf1 !important;
    box-shadow: 0 0 15px rgba(102, 252, 241, 0.4) !important;
}
div[role="radiogroup"] label p {
    font-size: 22px !important;
    font-weight: 900 !important;
    color: #ffffff !important;
    letter-spacing: 0.5px !important;
}

.badge-fussball { 
    background-color: #2ecc71; color: #000000; padding: 8px 18px;
    border-radius: 6px; font-weight: 900; font-size: 16px; display: inline-block;
    box-shadow: 0 0 10px rgba(46, 204, 113, 0.4);
}
.badge-leichtathletik { 
    background-color: #e74c3c; color: #ffffff; padding: 8px 18px;
    border-radius: 6px; font-weight: 900; font-size: 16px; display: inline-block;
    box-shadow: 0 0 10px rgba(231, 76, 60, 0.4);
}

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

def setting(name):
    value = os.environ.get(name)
    if value is not None:
        return value
    try:
        return str(st.secrets.get(name, ""))
    except (FileNotFoundError, st.errors.StreamlitSecretNotFoundError):
        return ""

TRAINER_CODE = setting("DOC_ATHLETIC_TRAINER_CODE")
GAST_CODE = setting("DOC_ATHLETIC_GAST_CODE")
DATABASE_URL = setting("DOC_ATHLETIC_DATABASE_URL")
if TRAINER_CODE and GAST_CODE and TRAINER_CODE == GAST_CODE:
    st.error("Trainer- und Gastcode müssen unterschiedlich sein.")
    st.stop()

# SQLite writes are transactional; revisions prevent stale sessions overwriting data.
# The hosting platform must retain this directory. JSON downloads are portable backups.
DATA_DIR = Path(os.environ.get("DOC_ATHLETIC_DATA_DIR", str(Path(__file__).resolve().parent)))
DB_FILE = DATA_DIR / "doc_athletic.sqlite3"
KADER_DATEI = DATA_DIR / "kader_db.json"
VALID_PROFILES = {'Fussball_U13', 'Leichtathletik_MASTER_w', 'Fussball_U23_m', 'Fussball_U23_w', 'Fussball_MASTER_w', 'Fussball_U20_m', 'Leichtathletik_MASTER_m', 'Leichtathletik_U17_m', 'Fussball_U17_w', 'Fussball_U15_w', 'Leichtathletik_U11', 'Leichtathletik_U15', 'Leichtathletik_U17_w', 'Leichtathletik_U20_w', 'Fussball_U15_m', 'Fussball_U17_m', 'Fussball_U20_w', 'Leichtathletik_U23_w', 'Fussball_MASTER_m', 'Leichtathletik_U20_m', 'Leichtathletik_U13', 'Leichtathletik_U23_m', 'Fussball_U11'}
DEFAULT_KADER = {"Fussball": {}, "Leichtathletik": {}}


class StorageConflict(Exception):
    pass

TEMPO_DISTANCES = [50, 60, 75, 100, 150, 200] + list(range(250, 801, 50))
TEMPO_PERCENTAGES = [100, 95, 90, 85, 80, 75, 70, 65, 60, 55, 50]

def format_tempo_time(seconds):
    # Round once before splitting, so 59.96 seconds becomes 1:00.0.
    tenths = round(seconds * 10)
    if tenths >= 600:
        minutes, rest = divmod(tenths, 600)
        return f"{minutes}:{rest / 10:04.1f} min"
    return f"{tenths / 10:.1f} s"

def estimate_time(distance, anchors, extrapolate):
    points = sorted((int(d), float(t)) for d,t in anchors.items() if t > 0)
    if len(points) < 2:
        return None
    left = [p for p in points if p[0] < distance]
    right = [p for p in points if p[0] > distance]
    if left and right:
        (d1,t1),(d2,t2) = left[-1],right[0]
        source = "Richtwert zwischen Referenzen"
    elif extrapolate and left and distance > points[-1][0] and points[-1][0] >= 300 and distance <= min(800,2*points[-1][0]):
        (d1,t1),(d2,t2) = points[-2:]
        source = "Richtwert über längste Referenz hinaus"
    else:
        return None
    if t2 <= t1:
        return None
    exponent = math.log(t2/t1) / math.log(d2/d1)
    return t1 * (distance/d1)**exponent, source

def build_tempo_table(t60, t150, source150, references, test_distance, test_seconds, interpolate=True, extrapolate=False):
    calc100 = round(t60 * 1.615, 2)
    modeled = {50:calc100 / 1.93, 75:calc100 * .775, 100:calc100,
               150:t150, 200:round(t60 * 3.265,2)}
    anchors = {60:t60}
    if source150 != "berechnet":
        anchors[150] = t150
    if test_seconds > 0:
        anchors[test_distance] = test_seconds
    anchors.update({int(d):t for d,t in references.items() if t > 0})
    result = []
    for distance in TEMPO_DISTANCES:
        explicit = references.get(str(distance), 0)
        estimation = estimate_time(distance,anchors,extrapolate) if interpolate else None
        if explicit > 0:
            base, source = explicit, "Trainerreferenz"
        elif distance == test_distance and test_seconds > 0:
            base, source = test_seconds, "Referenz: Einzeltest"
        elif distance == 60:
            base, source = t60, "60-m-Referenz"
        elif distance == 150 and source150 != "berechnet":
            base, source = t150, "150-m-Referenz"
        elif estimation is not None:
            base,source = estimation
        elif distance in modeled:
            base,source = modeled[distance], "Richtwert aus Kurzsprint"
        else:
            base,source = None, "Längere Referenz ergänzen"
        row = {"Distanz":f"{distance}m", "Herkunft":source}
        for percent in TEMPO_PERCENTAGES:
            seconds = base / (percent / 100) if base is not None else None
            # Longer training runs use whole seconds; inputs retain their precision.
            if seconds is None:
                value = "—"
            elif distance >= 250:
                total = round(seconds)
                minutes, rest = divmod(total,60)
                value = f"{minutes}:{rest:02d} min" if minutes else f"{total} s"
            else:
                value = format_tempo_time(seconds)
            row[f"{percent}%"] = value
        result.append(row)
    return result

def validate_kader(kader):
    if not isinstance(kader, dict) or set(kader) != {"Fussball", "Leichtathletik"}:
        raise ValueError("Die Sicherung muss Fußball und Leichtathletik enthalten.")
    for sport, athletes in kader.items():
        if not isinstance(athletes, dict) or len(athletes) > 10000:
            raise ValueError("Ungültige Athletenliste.")
        for name, p in athletes.items():
            if not isinstance(name, str) or not name.strip() or len(name) > 120 or name != name.strip():
                raise ValueError("Ungültiger Athletenname.")
            if not isinstance(p, dict):
                raise ValueError("Ungültiges Athletenprofil.")
            for field, low, high in [("alter",10,40),("groesse",1.30,2.15),("gewicht",30,140),("t_60",6,15)]:
                value = p.get(field)
                if type(value) not in (int, float) or not math.isfinite(value) or not low <= value <= high:
                    raise ValueError(f"Ungültiger Wert im Feld {field}.")
            if int(p["alter"]) != p["alter"]:
                raise ValueError("Das Alter muss in ganzen Jahren angegeben sein.")
            if p.get("profil") not in VALID_PROFILES or not p["profil"].startswith(sport + "_"):
                raise ValueError("Trainingsprofil und Sportart passen nicht zusammen.")
            if p.get("fasertyp") not in ["Ausdauer", "Kraft", "Sprungkraft", "Gazelle", "Schnelligkeit (Sprint)"]:
                raise ValueError("Unbekannter Fasertyp.")
            if p.get("reife") not in ["Spätentwickler (Retardiert)", "Normalentwickler", "Frühentwickler (Akzeleriert)"]:
                raise ValueError("Unbekannter Entwicklungsstatus.")
            if not isinstance(p.get("sbe"), str) or len(p["sbe"]) > 120:
                raise ValueError("Ungültige SBE-Angabe.")
            if "geschlecht" in p and p["geschlecht"] not in ["Männlich", "Weiblich"]:
                raise ValueError("Ungültige Geschlechtsangabe.")
            if "t_150" in p:
                v = p["t_150"]
                if type(v) not in (int,float) or not math.isfinite(v) or not 0 < v <= 120:
                    raise ValueError("Ungültige 150-m-Zeit.")
            if "t_150_quelle" in p and p["t_150_quelle"] not in ["gemessen", "berechnet", "ungeklärt"]:
                raise ValueError("Ungültige Herkunft der 150-m-Zeit.")
            references = p.get("tempo_referenzen", {})
            if not isinstance(references, dict) or any(k not in {str(d) for d in [100,200,1500] + list(range(250,801,50))} for k in references):
                raise ValueError("Ungültige Streckenreferenzen für die Tempotabelle.")
            for seconds in references.values():
                if type(seconds) not in (int,float) or not math.isfinite(seconds) or not 0 <= seconds <= 1800:
                    raise ValueError("Testzeiten müssen zwischen 0 und 1800 Sekunden liegen; 0 bedeutet fehlend.")
            plan = p.get("planung", {})
            if not isinstance(plan, dict):
                raise ValueError("Ungültige Planung.")
            ranges = {"einheiten":(1,2), "startwoche":(1,52), "bag_start":(1,20),
                      "burpee_start":(1,30), "cheer_start":(0,30), "single_start":(0,30), "beid_start":(0,30),
                      "bag_last":(0,30), "test_distanz":(50,1500), "test_zeit":(0,900),
                      "test_prozent":(50,100)}
            for key, (low, high) in ranges.items():
                value = plan.get(key)
                if value is not None and (type(value) not in (int,float) or not math.isfinite(value) or not low <= value <= high):
                    raise ValueError(f"Ungültige Planung: {key}.")
                if value is not None and key not in ("bag_last", "test_zeit") and int(value) != value:
                    raise ValueError(f"Ganze Zahl erforderlich: {key}.")
            for key in ("progression", "kapazitaet20", "burpees_bestaetigt", "tempo_interpolation", "tempo_extrapolation"):
                if key in plan and type(plan[key]) is not bool:
                    raise ValueError(f"Ungültige Freigabe: {key}.")
            if "rolle" in plan and plan["rolle"] not in ["Automatisch nach Wochenrhythmus", "Haupttag", "Neuromuskulär / vor dem Spiel"]:
                raise ValueError("Unbekanntes Einheitsziel.")
    return deepcopy(kader)

class StorageError(Exception):
    pass

@contextmanager
def remote_connection():
    try:
        import psycopg
    except ImportError as exc:
        raise StorageError("Für die externe Datenbank fehlt psycopg. requirements.txt aktualisieren.") from exc
    try:
        with psycopg.connect(DATABASE_URL, connect_timeout=10) as con:
            yield con
    except psycopg.Error as exc:
        raise StorageError("Externe Datenbank nicht erreichbar oder nicht eingerichtet. Es wurde nicht lokal ersatzgespeichert.") from exc

def remote_load():
    with remote_connection() as con:
        con.execute("CREATE TABLE IF NOT EXISTS doc_athletic_state (id INTEGER PRIMARY KEY CHECK(id=1), revision BIGINT NOT NULL, payload TEXT NOT NULL)")
        con.execute("CREATE TABLE IF NOT EXISTS doc_athletic_history (revision BIGINT PRIMARY KEY, payload TEXT NOT NULL, saved_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP)")
        initial = json.dumps(validate_kader(DEFAULT_KADER), ensure_ascii=False)
        con.execute("INSERT INTO doc_athletic_state VALUES (1,0,%s) ON CONFLICT (id) DO NOTHING", (initial,))
        row = con.execute("SELECT payload,revision FROM doc_athletic_state WHERE id=1").fetchone()
        return validate_kader(json.loads(row[0])), row[1]

def remote_save(kader, expected_revision):
    payload = json.dumps(validate_kader(kader), ensure_ascii=False, allow_nan=False)
    with remote_connection() as con:
        old = con.execute("SELECT revision,payload FROM doc_athletic_state WHERE id=1 FOR UPDATE").fetchone()
        if old is None or old[0] != expected_revision:
            raise StorageConflict("Eine andere Sitzung hat inzwischen gespeichert. Bitte den gespeicherten Stand neu laden.")
        con.execute("INSERT INTO doc_athletic_history(revision,payload) VALUES (%s,%s) ON CONFLICT (revision) DO NOTHING", old)
        con.execute("UPDATE doc_athletic_state SET payload=%s,revision=revision+1 WHERE id=1", (payload,))
    return expected_revision + 1

def lade_kader_von_datei():
    if DATABASE_URL:
        return remote_load()
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with closing(sqlite3.connect(DB_FILE, timeout=10)) as con, con:
        con.execute("CREATE TABLE IF NOT EXISTS state (id INTEGER PRIMARY KEY CHECK(id=1), revision INTEGER NOT NULL, payload TEXT NOT NULL)")
        con.execute("CREATE TABLE IF NOT EXISTS history (revision INTEGER PRIMARY KEY, payload TEXT NOT NULL, saved_at TEXT DEFAULT CURRENT_TIMESTAMP)")
        con.execute("BEGIN IMMEDIATE")
        row = con.execute("SELECT payload, revision FROM state WHERE id=1").fetchone()
        if row is None:
            if KADER_DATEI.exists():
                with KADER_DATEI.open(encoding="utf-8") as f:
                    initial = validate_kader(json.load(f))
            else:
                initial = validate_kader(DEFAULT_KADER)
            payload = json.dumps(initial, ensure_ascii=False, allow_nan=False)
            con.execute("INSERT INTO state VALUES (1, 0, ?)", (payload,))
            row = (payload, 0)
        return validate_kader(json.loads(row[0])), row[1]

def speichere_kader_in_datei(kader, expected_revision):
    validated = validate_kader(kader)
    if DATABASE_URL:
        return remote_save(validated, expected_revision)
    payload = json.dumps(validated, ensure_ascii=False, allow_nan=False)
    with closing(sqlite3.connect(DB_FILE, timeout=10)) as con, con:
        con.execute("BEGIN IMMEDIATE")
        old = con.execute("SELECT revision, payload FROM state WHERE id=1").fetchone()
        if old is None or old[0] != expected_revision:
            raise StorageConflict("Eine andere Sitzung hat inzwischen gespeichert. Bitte den gespeicherten Stand neu laden und Änderungen erneut prüfen.")
        con.execute("INSERT OR IGNORE INTO history(revision,payload) VALUES (?,?)", old)
        con.execute("UPDATE state SET payload=?, revision=revision+1 WHERE id=1", (payload,))
    return expected_revision + 1

def warmup_text(band, te):
    if band == "U13":
        return "800 m ca. 3:40 min; Einstieg nach Trainerprüfung" if te >= 3 else "Einlaufen nach Trainerentscheidung; 800 m erst etwa ab TE 3"
    return {"U15":"800 m ca. 3:30 min", "U17":"800 m unter 3:15 min",
            "U20":"800 m unter 3:05 min", "U23":"800 m unter 2:55 min"}.get(band,
            "Einlaufen nach Trainerentscheidung; noch keine feste Zeit hinterlegt")

def weekly_reps(start, week, cap, approved):
    return min(start + (week - 1 if approved else 0), cap)

def unit_context(te, units_per_week, start_week, role):
    week = start_week + (te - 1) // units_per_week
    day = (te - 1) % units_per_week + 1
    short = role == "Neuromuskulär / vor dem Spiel" or (role == "Automatisch nach Wochenrhythmus" and units_per_week == 2 and day == 2)
    return week, day, short

def cheer_load(band, gender):
    if gender != "Weiblich":
        return "Last je Hand individuell festlegen"
    return {"U11":"1 kg je Hand", "U13":"2 kg je Hand", "U15":"3 kg je Hand",
            "U17":"4 kg je Hand", "U20":"4–6 kg je Hand"}.get(band, "Last je Hand individuell festlegen")

def exercise_row(exercise, sets, reps, load, note):
    cells = ["Ergänzung", exercise, str(sets), reps, load, note, "Trainerfestlegung"]
    return '<tr style="background:#e8f4f0">' + ''.join('<td style="padding:6px;border:1px solid #aaa">'+escape(v)+'</td>' for v in cells) + '</tr>'

def profile_age(profile):
    band = profile.split("_")[1]
    return {"U11":10,"U13":12,"U15":14,"U17":16,"U20":19,"U23":22,"MASTER":24}[band]

def widget_key(field, sport, mode, target):
    context = json.dumps([sport,mode,target,st.session_state.get("edit_epoch",0)], ensure_ascii=False)
    return field + "_" + hashlib.sha256(context.encode()).hexdigest()[:16]

def reload_saved():
    data, revision = lade_kader_von_datei()
    st.session_state.kader_db = data
    st.session_state.kader_revision = revision
    st.session_state.edit_epoch = st.session_state.get("edit_epoch",0) + 1


auth_fingerprint = hashlib.sha256(json.dumps([TRAINER_CODE,GAST_CODE,DATABASE_URL]).encode()).hexdigest()
if st.session_state.get("auth_fingerprint") != auth_fingerprint:
    st.session_state.clear()
    st.session_state.auth_fingerprint = auth_fingerprint

if not TRAINER_CODE:
    st.title("Doc Athletic Evolution 23.8.2")
    st.info("Trainerzugang einrichten: In den Streamlit-Einstellungen unter Secrets den Eintrag DOC_ATHLETIC_TRAINER_CODE mit einem eigenen Zugangscode speichern. Danach die App neu laden.")
    st.stop()
if DATABASE_URL:
    st.caption("Speicher: externe PostgreSQL-Datenbank")
else:
    st.warning("Speicher: lokale App-Datei. Auf Streamlit Cloud nicht dauerhaft garantiert. Nach der Arbeit unter Kader-Datensicherung ein Backup herunterladen; externe Datenbank noch einrichten.")

if 'auth_modus' not in st.session_state:
    st.session_state.auth_modus = None

if st.session_state.auth_modus is None:
    col_11, col_12, col_13 = st.columns([1, 2, 1])
    with col_12:
        lade_bild(["logo.png", "logo.png.png", "logo"], use_col=True)
        st.markdown("<p style='text-align: center; color: #c5c6c7; margin-top: 20px;'>Bitte Zugriffscode eingeben (Fußball & Leichtathletik)</p>", unsafe_allow_html=True)
        col_p1, col_p2, col_p3 = st.columns([1, 2, 1])
        with col_p2:
            eingabe_code = st.text_input("Zugriffscode", type="password")
            if st.button("ZUGRIFF BESTÄTIGEN"):
                if TRAINER_CODE and hmac.compare_digest(eingabe_code.encode(), TRAINER_CODE.encode()):
                    st.session_state.auth_modus = "trainer"
                    st.rerun()
                elif GAST_CODE and hmac.compare_digest(eingabe_code.encode(), GAST_CODE.encode()):
                    st.session_state.auth_modus = "gast"
                    st.rerun()
                else:
                    st.error("Ungültiger Code. Bitte prüfen.")
                st.stop()
    st.stop()

if 'navigations_status' not in st.session_state:
    st.session_state.navigations_status = 'Start'

if 'kader_db' not in st.session_state:
    try:
        reload_saved()
    except (OSError, sqlite3.Error, StorageError, ValueError) as exc:
        st.error(f"Athletendaten konnten nicht geladen werden: {exc}. Vorhandene Dateien bleiben erhalten.")
        st.stop()

if "save_notice" in st.session_state:
    st.success(st.session_state.pop("save_notice"))

def navigiere(ziel):
    st.session_state.navigations_status = ziel

if st.session_state.get('auth_modus') == 'trainer':
    st.sidebar.markdown('**Kader-Datensicherung**')
    st.sidebar.caption("Sicherung enthält die zuletzt gespeicherten Profile einschließlich Planungseinstellungen.")
    try:
        backup_data, _ = lade_kader_von_datei()
        st.sidebar.download_button('Kader sichern (Backup-Datei)',
            data=json.dumps(backup_data, ensure_ascii=False, indent=2),
            file_name='kader_db.json', mime='application/json')
    except (OSError, sqlite3.Error, StorageError, ValueError):
        st.sidebar.error("Die aktuelle Sicherung ist nicht verfügbar.")
    st.sidebar.caption("Neu laden verwirft noch nicht gespeicherte Eingaben.")
    if st.sidebar.button('Gespeicherten Stand neu laden'):
        try:
            reload_saved()
            st.rerun()
        except (OSError, sqlite3.Error, StorageError, ValueError) as exc:
            st.sidebar.error(str(exc))
    _upload = st.sidebar.file_uploader('Kader aus Backup laden', type=['json'])
    restore_confirm = st.sidebar.checkbox('Vorhandenen Kader durch die Sicherung ersetzen')
    if _upload is not None and st.sidebar.button('Backup jetzt wiederherstellen', disabled=not restore_confirm):
        try:
            if _upload.size > 5_000_000:
                raise ValueError("Die Sicherung ist zu groß.")
            restored = validate_kader(json.loads(_upload.getvalue()))
            rev = speichere_kader_in_datei(restored, st.session_state.kader_revision)
            st.session_state.kader_db = restored
            st.session_state.kader_revision = rev
            st.session_state.edit_epoch = st.session_state.get("edit_epoch",0) + 1
            st.session_state.save_notice = 'Kader wiederhergestellt und gespeichert.'
            st.rerun()
        except (OSError, sqlite3.Error, StorageError, ValueError, StorageConflict) as exc:
            st.sidebar.error(f"Wiederherstellung abgebrochen: {exc}")

abc_parameter = {
    "Fussball_U11": {"sets": 3, "start_m": 12.0, "step_m": 2.0, "sbe_ziel": "SR 3"},
    "Fussball_U13": {"sets": 4, "start_m": 15.0, "step_m": 2.5, "sbe_ziel": "SR 2-3"},
    "Fussball_U15_m": {"sets": 4, "start_m": 18.0, "step_m": 2.5, "sbe_ziel": "SR 2"},
    "Fussball_U15_w": {"sets": 4, "start_m": 15.0, "step_m": 2.5, "sbe_ziel": "SR 2"},
    "Fussball_U17_m": {"sets": 5, "start_m": 22.0, "step_m": 3.0, "sbe_ziel": "SR 1-2"},
    "Fussball_U17_w": {"sets": 5, "start_m": 20.0, "step_m": 2.5, "sbe_ziel": "SR 1-2"},
    "Fussball_U20_m": {"sets": 5, "start_m": 25.0, "step_m": 3.0, "sbe_ziel": "SR 1"},
    "Fussball_U20_w": {"sets": 5, "start_m": 22.0, "step_m": 2.5, "sbe_ziel": "SR 1"},
    "Fussball_U23_m": {"sets": 6, "start_m": 28.0, "step_m": 3.0, "sbe_ziel": "SR 1-0"},
    "Fussball_U23_w": {"sets": 6, "start_m": 25.0, "step_m": 2.5, "sbe_ziel": "SR 1-0"},
    "Fussball_MASTER_m": {"sets": 6, "start_m": 30.0, "step_m": 3.0, "sbe_ziel": "SR 0"},
    "Fussball_MASTER_w": {"sets": 6, "start_m": 28.0, "step_m": 3.0, "sbe_ziel": "SR 0"},
    "Leichtathletik_U11": {"sets": 3, "start_m": 12.0, "step_m": 2.0, "sbe_ziel": "SR 3"},
    "Leichtathletik_U13": {"sets": 4, "start_m": 15.0, "step_m": 2.0, "sbe_ziel": "SR 2-3"},
    "Leichtathletik_U15": {"sets": 4, "start_m": 18.0, "step_m": 2.5, "sbe_ziel": "SR 2"},
    "Leichtathletik_U17_m": {"sets": 5, "start_m": 25.0, "step_m": 3.5, "sbe_ziel": "SR 1-2"},
    "Leichtathletik_U17_w": {"sets": 5, "start_m": 22.0, "step_m": 3.0, "sbe_ziel": "SR 1-2"},
    "Leichtathletik_U20_m": {"sets": 6, "start_m": 28.0, "step_m": 3.0, "sbe_ziel": "SR 1"},
    "Leichtathletik_U20_w": {"sets": 6, "start_m": 26.0, "step_m": 3.0, "sbe_ziel": "SR 1"},
    "Leichtathletik_U23_m": {"sets": 6, "start_m": 30.0, "step_m": 3.0, "sbe_ziel": "SR 0"},
    "Leichtathletik_U23_w": {"sets": 6, "start_m": 28.0, "step_m": 3.0, "sbe_ziel": "SR 0"},
    "Leichtathletik_MASTER_m": {"sets": 6, "start_m": 30.0, "step_m": 3.0, "sbe_ziel": "SR 0"},
    "Leichtathletik_MASTER_w": {"sets": 6, "start_m": 28.0, "step_m": 3.0, "sbe_ziel": "SR 0"}
}

HARDWARE_GRIFFBAELLE = [3, 5, 7, 9]
HARDWARE_HEXBAR = [30, 35, 40, 45, 50, 55, 60, 65, 70]

def snap_to_hardware(wert, hardware_liste, konservativ=True):
    passende = [h for h in hardware_liste if (h <= wert if konservativ else h >= wert)]
    if passende:
        return max(passende) if konservativ else min(passende)
    return None

if st.sidebar.button("ABMELDEN"):
    st.session_state.clear()
    st.rerun()

if st.session_state.auth_modus == "gast":
    st.sidebar.warning("GAST-MODUS (Nur Leserechte)")

if st.session_state.navigations_status == 'Start':
    st.markdown("<h1 style='text-align: center; color: #66fcf1 !important; margin-top: 30px;'>DOC ATHLETIC EVOLUTION 23.8.2</h1><p style='text-align:center'>Tempotabellen bis 800 m</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #c5c6c7; font-size: 16px;'>Fußball & Leichtathletik · Individuelle Trainingsplanung</p>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        lade_bild(["logo.png", "logo.png.png", "logo"], use_col=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.button("SYSTEM INITIALISIEREN >>", on_click=navigiere, args=('Uebersicht',))

elif st.session_state.navigations_status == 'Uebersicht':
    st.title("Systemübersicht & Athleten-Datenbank")
    st.markdown("## Komplex-Training im Nachwuchs bis Hochleistungssport (Fußball & Leichtathletik)")
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
        st.markdown("## Operative Trainingssteuerung")

    st.markdown("<div class='steuermatrix'>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #66fcf1 !important; font-size: 26px; font-weight: 900; letter-spacing: 1.5px; text-transform: uppercase; margin-top: 0; margin-bottom: 5px;'>Biometrische Live-Steuerung & Disziplin-Wahl</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #a0aab2; font-size: 14px; margin-bottom: 15px;'>Fokussierte Trainingsansteuerung nach Doc Athletic Train Smart Philosophie</p>", unsafe_allow_html=True)
    
    sport_kategorie = st.radio("Sportart wählen", ["⚽ Fußball", "🏃 Leichtathletik"], horizontal=True, label_visibility="collapsed")
    
    if "Fußball" in sport_kategorie:
        aktive_kategorie = "Fussball"
        aktive_sport_schluessel = [k for k in abc_parameter.keys() if "Fussball" in k]
        st.markdown("<div style='text-align: center; margin-top: 10px;'><span class='badge-fussball'>⚽ Modul: Fußball aktiv (Kernsportart)</span></div>", unsafe_allow_html=True)
    else:
        aktive_kategorie = "Leichtathletik"
        aktive_sport_schluessel = [k for k in abc_parameter.keys() if "Leichtathletik" in k]
        st.markdown("<div style='text-align: center; margin-top: 10px;'><span class='badge-leichtathletik'>🏃 Modul: Leichtathletik aktiv (Peripher)</span></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    aktive_athleten_db = st.session_state.kader_db[aktive_kategorie]

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        modus = st.selectbox("Steuerungs-Ebene", ["Einzelathlet / Einzelathletin", "Gruppe / Team (Kader)"])
        if modus == "Einzelathlet / Einzelathletin":
            if len(aktive_athleten_db) > 0:
                ziel = st.selectbox("Ziel (Name)", list(aktive_athleten_db.keys()), key=f"athlet_{aktive_kategorie}")
                aktuelle_daten = aktive_athleten_db[ziel]
                profil_soll = aktuelle_daten["profil"]
            else:
                ziel = "Neuer Athlet"
                aktuelle_daten = {"alter": 10, "groesse": 1.50, "gewicht": 35.0, "profil": aktive_sport_schluessel[0], "fasertyp": "Schnelligkeit (Sprint)", "reife": "Normalentwickler", "sbe": "SR 2", "t_60": 7.80}
                profil_soll = aktive_sport_schluessel[0]
        else:
            ziel = st.selectbox("Ziel (Kader / Profil)", aktive_sport_schluessel, key=f"kader_{aktive_kategorie}")
            profil_soll = ziel
            aktuelle_daten = {"alter": profile_age(ziel), "groesse": 1.50 if profile_age(ziel) <= 12 else 1.75, "gewicht": 35.0 if profile_age(ziel) <= 12 else 65.0, "fasertyp": "Schnelligkeit (Sprint)", "reife": "Normalentwickler", "sbe": abc_parameter[ziel]["sbe_ziel"], "t_60": 7.80}

    key_for = lambda field: widget_key(field, aktive_kategorie, modus, ziel)

    with c2:
        alter = st.number_input("Alter (Jahre)", min_value=10, max_value=40, value=int(aktuelle_daten["alter"]), key=key_for("alter"), disabled=(st.session_state.auth_modus == "gast" or modus == "Gruppe / Team (Kader)"))
        geschlecht_wahl = st.selectbox("Geschlecht", ["Männlich", "Weiblich"], index=1 if aktuelle_daten.get("geschlecht", "Weiblich" if profil_soll.endswith("_w") else "Männlich") == "Weiblich" else 0, key=key_for("geschlecht"), disabled=(st.session_state.auth_modus == "gast"))

    with c3:
        groesse = st.number_input("Körpergröße (m)", min_value=1.30, max_value=2.15, value=float(aktuelle_daten.get("groesse", 1.70)), step=0.01, key=key_for("groesse"), disabled=(st.session_state.auth_modus == "gast"))
        gewicht = st.number_input("Körpergewicht (kg)", min_value=30.0, max_value=140.0, value=float(aktuelle_daten.get("gewicht", 55.0)), step=0.5, key=key_for("gewicht"), disabled=(st.session_state.auth_modus == "gast"))

    with c4:
        ft_liste = ["Ausdauer", "Kraft", "Sprungkraft", "Gazelle", "Schnelligkeit (Sprint)"]
        reife_liste = ["Spätentwickler (Retardiert)", "Normalentwickler", "Frühentwickler (Akzeleriert)"]
        ft_idx = ft_liste.index(aktuelle_daten["fasertyp"]) if aktuelle_daten["fasertyp"] in ft_liste else 4
        ft = st.selectbox("Fasertyp", ft_liste, index=ft_idx, key=key_for("fasertyp"), disabled=(st.session_state.auth_modus == "gast"))
        reife_val = aktuelle_daten["reife"]
        r_idx = 0 if "Spät" in reife_val else 2 if "Früh" in reife_val else 1
        reife = st.selectbox("Entwicklungsstatus", reife_liste, index=r_idx, key=key_for("reife"), disabled=(st.session_state.auth_modus == "gast"))

    c_opt1, c_opt2 = st.columns(2)
    with c_opt1:
        te_wahl = st.selectbox("Trainingseinheit (TE)", [f"TE {i}" for i in range(1, 15)] + ["Alle TEs (1-14)"])
    with c_opt2:
        jump_modus = st.selectbox("Komplex-Sprungmodus", ["Jumps (Vorfuß am Boden / Dreifachstreckung)", "Sprünge (Flugphase > 3-5 cm / Reaktiv)"])

    sbe_ziel = st.text_input("SBE (Reserve)", value=aktuelle_daten["sbe"], key=key_for("sbe"), disabled=(st.session_state.auth_modus == "gast"))

    if modus == "Einzelathlet / Einzelathletin":
        profil_soll = st.selectbox("Trainingsprofil / Altersklasse", aktive_sport_schluessel,
            index=aktive_sport_schluessel.index(profil_soll), key=key_for("profil"),
            disabled=(st.session_state.auth_modus == "gast"))
    else:
        st.caption("Gruppenmodus: Das Alter ist ein Referenzwert der gewählten Altersklasse; Körpermaße und Testzeiten sind Beispiele und müssen angepasst werden.")

    base_prof = profil_soll.rsplit('_', 1)[0] if ('_m' in profil_soll or '_w' in profil_soll) else profil_soll
    suffix = "_w" if geschlecht_wahl == "Weiblich" else "_m"
    if f"{base_prof}{suffix}" in abc_parameter:
        profil_soll = f"{base_prof}{suffix}"

    band = profil_soll.split("_")[1]
    # Load prescriptions use the selected category; actual age remains separate.
    plan_age = profile_age(profil_soll)
    if modus == "Einzelathlet / Einzelathletin" and abs(int(alter) - plan_age) > 1:
        st.warning("Alter und gewählte Trainingsklasse weichen ab. Die Trainingsklasse steuert den Plan; bitte prüfen.")
    saved_plan = aktuelle_daten.get("planung", {})
    guest = st.session_state.auth_modus == "gast"
    with st.expander("Wochenplanung und individuelle Vorgaben", expanded=True):
        st.caption("Trainerregeln vom 18.09.2026. Die zweite Einheit bei zwei TEs pro Woche ist im Automatikmodus neuromuskulär ausgerichtet. Einheitsziel bei Bedarf ändern.")
        pc1, pc2 = st.columns(2)
        with pc1:
            einheiten = st.number_input("Einheiten pro Woche", 1, 2, int(saved_plan.get("einheiten",2)), key=key_for("einheiten"), disabled=guest)
            startwoche = st.number_input("Startwoche für TE 1", 1, 52, int(saved_plan.get("startwoche",1)), key=key_for("startwoche"), disabled=guest)
            roles = ["Automatisch nach Wochenrhythmus", "Haupttag", "Neuromuskulär / vor dem Spiel"]
            role = st.selectbox("Einheitsziel", roles, index=roles.index(saved_plan.get("rolle",roles[0])), key=key_for("rolle"), disabled=guest)
            progression = st.checkbox("Wöchentliche Steigerung nach Belastungsprüfung freigegeben", value=saved_plan.get("progression",False), key=key_for("progression"), disabled=guest)
            bag_start = st.number_input("Powerbag: Startwiederholungen", 1, 20, int(saved_plan.get("bag_start",10)), key=key_for("bagstart"), disabled=guest)
            capacity = st.checkbox("Individuelles Kapazitätsziel bis 20 Wiederholungen", value=saved_plan.get("kapazitaet20",False), key=key_for("capacity"), disabled=guest)
            bag_override = st.number_input("Individuelle Powerbag-Last (kg; 0 = Korridor)", 0.0, 30.0, float(saved_plan.get("bag_last",0)), step=0.5, key=key_for("bagload"), disabled=guest)
        with pc2:
            burpee_start = st.number_input("Burpees: Startwiederholungen (vorläufig 8 w / 10 m)", 1, 30, int(saved_plan.get("burpee_start",8 if geschlecht_wahl=="Weiblich" else 10)), key=key_for("burpeestart_"+geschlecht_wahl), disabled=guest)
            burpees_ok = st.checkbox("Burpee-Startwert für diesen Athleten bestätigt", value=saved_plan.get("burpees_bestaetigt",False), key=key_for("burpeeok"), disabled=guest)
            cheer_start = st.number_input("Cheerleading: Start je Arm (0 = offen)", 0, 30, int(saved_plan.get("cheer_start",0)), key=key_for("cheerstart"), disabled=guest)
            single_start = st.number_input("Einbeiniger Curl: Start je Bein (0 = offen)", 0, 30, int(saved_plan.get("single_start",0)), key=key_for("singlestart"), disabled=guest)
            bilateral_start = st.number_input("Beidbeiniger Curl: Startwiederholungen (0 = offen)", 0, 30, int(saved_plan.get("beid_start",0)), key=key_for("bilatstart"), disabled=guest)
            st.caption("Cheerleading: beidbeinige Fußgelenksprünge, Arme wechselseitig vertikal, neutraler Griff. Last gilt je Kurzhantel. Powerbar-Angaben gelten für die gesamte Stange.")
        if bag_start > 15 and not capacity:
            st.warning("Für mehr als 15 Powerbag-Wiederholungen das individuelle Kapazitätsziel aktivieren. Aktuell begrenzt der Plan auf 15.")
        st.markdown("**Tempolauf aus einem Test derselben Distanz**")
        tc1, tc2, tc3 = st.columns(3)
        test_distance = tc1.number_input("Testdistanz (m)",50,1500,int(saved_plan.get("test_distanz",800)),key=key_for("testdist"),disabled=guest)
        test_seconds = tc2.number_input("Gemessene Testzeit (Sekunden; 0 = fehlt)",0.0,900.0,float(saved_plan.get("test_zeit",0)),step=0.1,key=key_for("testtime"),disabled=guest)
        test_percent = tc3.number_input("Zieltempo (% der Testgeschwindigkeit)",50,100,int(saved_plan.get("test_prozent",80)),key=key_for("testpercent"),disabled=guest)
        st.caption("Einlaufen und Tempolauf bleiben getrennt. Keine automatische Ableitung durch Abzug von 10–15 Sekunden; keine Umrechnung dieses Tests auf andere Distanzen.")
    plan_settings = {"einheiten":einheiten,"startwoche":startwoche,"rolle":role,"progression":progression,
        "bag_start":bag_start,"kapazitaet20":capacity,"bag_last":bag_override,"burpee_start":burpee_start,
        "burpees_bestaetigt":burpees_ok,"cheer_start":cheer_start,"single_start":single_start,"beid_start":bilateral_start,
        "test_distanz":test_distance,"test_zeit":test_seconds,"test_prozent":test_percent}

    diag_col1, diag_col2 = st.columns(2)
    with diag_col1:
        t_60 = st.number_input("60m-Referenz (s)", min_value=6.0, max_value=15.0, value=float(aktuelle_daten.get("t_60", 7.80)), step=0.01, key=key_for("t_60"), disabled=(st.session_state.auth_modus == "gast"))
    with diag_col2:
        auto_150 = round(t_60 * 2.375, 2)
        quellen = ["berechnet", "gemessen", "ungeklärt"]
        quelle_default = aktuelle_daten.get("t_150_quelle", "ungeklärt" if "t_150" in aktuelle_daten else "berechnet")
        quelle_150 = st.selectbox("Herkunft der 150-m-Zeit", quellen, index=quellen.index(quelle_default),
            key=key_for("quelle150"), disabled=(st.session_state.auth_modus == "gast"))
        if quelle_150 == "berechnet":
            t_150 = auto_150
            st.metric("150-m-Richtwert (berechnet)", f"{t_150:.2f} s")
        else:
            t_150 = st.number_input("150m-Referenz (s)", min_value=0.01, max_value=120.0,
                value=float(aktuelle_daten.get("t_150", auto_150)), step=0.01,
                key=key_for("t_150"), disabled=(st.session_state.auth_modus == "gast"))
            if quelle_150 == "ungeklärt":
                st.caption("Übernommener Wert: Bitte bestätigen, ob diese Zeit gemessen wurde.")

    with st.expander("Referenzzeiten und Tempotabelle bis 800 m", expanded=True):
        st.caption("Hier deine Referenzzeiten in Sekunden eintragen, z. B. 132 für 2:12 Minuten. Praktische Richtwerte sind möglich. 0 bedeutet: fehlt. Einlaufzeiten bleiben separat.")
        reference_columns = st.columns(3)
        saved_references = aktuelle_daten.get("tempo_referenzen", {})
        tempo_references = {}
        for index, distance in enumerate([100,200] + list(range(250,801,50)) + [1500]):
            with reference_columns[index % 3]:
                tempo_references[str(distance)] = st.number_input(
                    f"{distance} m: Referenzzeit (s; 0 = fehlt)", min_value=0.0, max_value=1800.0,
                    value=float(saved_references.get(str(distance),0)), step=0.1,
                    key=key_for(f"tempo_ref_{distance}"), disabled=guest)
        st.caption("Ein vorhandener Einzeltest aus der Wochenplanung wird für seine Strecke verwendet, solange hier keine eigene Streckenreferenz eingetragen ist. Die Zeiten werden mit dem Athletenprofil gespeichert.")
        tempo_interpolation = st.checkbox("Zwischenstrecken als individuelle Richtwerte berechnen", value=saved_plan.get("tempo_interpolation",True), key=key_for("tempo_interp"), disabled=guest)
        tempo_extrapolation = st.checkbox("Richtwerte über die längste Referenz hinaus zulassen (bis 800 m)", value=saved_plan.get("tempo_extrapolation",False), key=key_for("tempo_extra"), disabled=guest)
        st.caption("Für längere Strecken mindestens eine längere Referenz ergänzen, etwa 600 oder 800 m. Die Berechnung verbindet deine Zeiten abschnittsweise. Fortsetzungen benötigen eine Referenz ab 300 m und reichen höchstens bis zur doppelten Referenzstrecke. Es handelt sich um Planungsrichtwerte.")
    plan_settings.update({"tempo_interpolation":tempo_interpolation,"tempo_extrapolation":tempo_extrapolation})
    points = sorted((int(d),t) for d,t in tempo_references.items() if t > 0)
    if any(t2 <= t1 for (_,t1),(_,t2) in zip(points,points[1:])):
        st.warning("Bitte die Referenzzeiten prüfen: Eine längere Strecke hat eine gleich kurze oder kürzere Zeit. Für den betroffenen Bereich werden keine Richtwerte interpoliert.")

    if (test_seconds > 0 and tempo_references.get(str(test_distance),0) > 0
            and not math.isclose(tempo_references[str(test_distance)],test_seconds)):
        st.warning("Für dieselbe Strecke sind zwei Testzeiten eingetragen. Die Tempotabelle verwendet die Streckenreferenz aus ‚Testzeiten bis 800 m‘; der Einzeltest-Rechner verwendet seine eigene Eingabe. Bitte die Werte abgleichen.")

    if modus == "Einzelathlet / Einzelathletin" and st.session_state.auth_modus == "trainer":
        neuer_name = st.text_input("Neuen Athleten-Namen eingeben (zum Anlegen):", value="", key=key_for("neu")).strip()
        st.caption("Vor dem Athletenwechsel speichern. Ein neuer Name legt ein zusätzliches Profil mit den aktuellen Werten an.")
        if st.button("Athleten-Profil in Sektion speichern"):
            ziel_name = neuer_name if neuer_name else ziel
            try:
                if not aktive_athleten_db and not neuer_name:
                    raise ValueError("Bitte zuerst einen Athletennamen eingeben.")
                if neuer_name and neuer_name in st.session_state.kader_db[aktive_kategorie]:
                    raise ValueError("Dieser Name ist bereits vorhanden. Bitte das vorhandene Profil auswählen.")
                updated = deepcopy(st.session_state.kader_db)
                record = deepcopy(aktuelle_daten)
                record.update({"alter": int(alter), "groesse": float(groesse), "gewicht": float(gewicht), "profil": profil_soll,
                    "geschlecht": geschlecht_wahl, "fasertyp": ft, "reife": reife, "sbe": sbe_ziel,
                    "t_60": float(t_60), "t_150": float(t_150), "t_150_quelle": quelle_150, "planung":plan_settings, "tempo_referenzen":tempo_references})
                updated[aktive_kategorie][ziel_name] = record
                revision = speichere_kader_in_datei(updated, st.session_state.kader_revision)
                st.session_state.kader_db = updated
                st.session_state.kader_revision = revision
                st.session_state.save_notice = f"Profil {ziel_name} gespeichert."
                st.rerun()
            except (OSError, sqlite3.Error, StorageError, ValueError, StorageConflict) as exc:
                st.error(f"Nicht gespeichert: {exc}")

    st.markdown("</div>", unsafe_allow_html=True)

    reife_intern = "Spätentwickler" if "Spät" in reife else "Frühentwickler" if "Früh" in reife else "Normalentwickler"

    st.subheader("Testzeiten und berechnete Richtwerte")
    calc_100 = round(t_60 * 1.615, 2)
    calc_200 = round(t_60 * 3.265, 2)

    res_col1, res_col2 = st.columns(2)
    with res_col1:
        st.markdown("#### Eingaben und Modellwerte")
        st.write(f"60m: **{t_60:.2f} s** | 100m: **{calc_100:.2f} s** | 150m: **{t_150:.2f} s** | 200m: **{calc_200:.2f} s**")
    with res_col2:
        st.info("Die Übersicht zeigt die bisherigen Kurzsprint-Richtwerte. In der Tempotabelle haben deine eingetragenen Referenzzeiten Vorrang.")

    st.markdown("---")
    st.subheader("Tempotabellen 50–800 m")
    st.caption("100–50 % beziehen sich auf die mittlere Geschwindigkeit der jeweiligen Referenzleistung. Beispiel: 180 s bei 100 % ergeben 225 s bei 80 %. Das sind keine Anteile der maximalen momentanen Sprintgeschwindigkeit.")
    tempo_data = build_tempo_table(t_60,t_150,quelle_150,tempo_references,test_distance,test_seconds,tempo_interpolation,tempo_extrapolation)
    st.dataframe(pd.DataFrame(tempo_data), hide_index=True, width="stretch", height=670)
    if any(row["Herkunft"] == "Längere Referenz ergänzen" for row in tempo_data):
        st.info("Für die noch leeren Strecken eine längere Referenzzeit ergänzen oder die Fortsetzung der Richtwerte aktivieren. Deine eingetragenen Referenzen haben immer Vorrang.")

    st.markdown("---")
    st.subheader(f"Detaillierter Trainingsplan & Doc-Athletic-Farbkodierung: {ziel}")

    vorgaben = abc_parameter.get(profil_soll, {"sets": 4, "start_m": 15.0, "step_m": 2.5})
    te_liste = range(1, 15) if "Alle" in te_wahl else [int(te_wahl.replace("TE ", ""))]

    # ========================================================================
    # POWER BAGS: REALISTISCHE VON-BIS-KORRIDORE (BIS 17 KG) & 12-15 WDH.
    # ========================================================================
    if plan_age <= 13:
        bag_text = "Power Bag 5-8 kg"
        bag_wdh = "10-12 Wdh."
    elif plan_age <= 15:
        if ft == "Gazelle" or reife_intern == "Spätentwickler":
            bag_text = "Power Bag 8-10 kg"
        else:
            bag_text = "Power Bag 10-13 kg"
        bag_wdh = "12-15 Wdh."
    elif plan_age <= 17:
        if ft == "Gazelle":
            bag_text = "Power Bag 10-13 kg"
        else:
            bag_text = "Power Bag 12-15 kg"
        bag_wdh = "12-15 Wdh."
    else:
        if gewicht < 70 or ft == "Gazelle":
            bag_text = "Power Bag 12-16 kg"
        else:
            bag_text = "Power Bag 15-17 kg"
        bag_wdh = "12-15 Wdh."

    if band == "U11":
        bag_text = "Körpergewicht; keine Powerbag-Zusatzlast hinterlegt"
    elif band == "U13":
        bag_text = "Powerbag bis 5 kg nach Trainerfreigabe"
    elif band == "U15":
        bag_text = "Powerbag 8–12 kg" if geschlecht_wahl == "Weiblich" else "Powerbag 12–15 kg; bei Bedarf z. B. 10 kg"
    if bag_override > 0:
        bag_text = f"Powerbag {bag_override:g} kg (individuelle Trainerfestlegung)"

    # Griffbälle für Umsatz/Crunch
    if plan_age <= 13:
        gb_last_kg = 3
    elif plan_age <= 15:
        gb_last_kg = 5 if ft in ["Kraft", "Schnelligkeit (Sprint)"] else 3
    elif plan_age <= 17:
        gb_last_kg = 7 if ft == "Kraft" else 5
    else:
        gb_last_kg = 9 if ft == "Kraft" and gewicht >= 75 else 7

    # Hex Bar (8-12 Wdh. beibehalten)
    ist_jumps = "Jumps" in jump_modus
    if plan_age <= 13:
        hex_text = "Hex Bar nicht freigegeben (Körpergewicht)"
    elif plan_age <= 15:
        hex_kg = 30 if ft == "Kraft" else 25
        hex_text = f"Kettlebell-Paar {hex_kg} kg (Bodenkontakt)"
    elif plan_age <= 17:
        ziel_hex = gewicht * (0.55 if ist_jumps else 0.45)
        if ft == "Gazelle": ziel_hex *= 0.90
        hex_kg = snap_to_hardware(ziel_hex, HARDWARE_HEXBAR, konservativ=True)
        hex_kg = min(hex_kg, 45 if ist_jumps else 35) if hex_kg is not None else None
        hex_text = f"Hex Bar {hex_kg} kg ({'Jumps' if ist_jumps else 'Sprünge'})" if hex_kg is not None else "Keine passende Hex-Bar-Last: Trainerentscheidung erforderlich"
    else:
        ziel_hex = gewicht * (0.75 if ist_jumps else 0.60)
        if ft == "Gazelle": ziel_hex *= 0.90
        hex_kg = snap_to_hardware(ziel_hex, HARDWARE_HEXBAR, konservativ=True)
        hex_kg = min(hex_kg, 60 if ist_jumps else 50) if hex_kg is not None else None
        hex_text = f"Hex Bar {hex_kg} kg ({'Jumps' if ist_jumps else 'Sprünge'})" if hex_kg is not None else "Keine passende Hex-Bar-Last: Trainerentscheidung erforderlich"

    # Hürden-Tiefsprünge
    if plan_age <= 13:
        tief_hoehe = "30-38 cm"
        tief_kh = "ohne ZL"
    elif plan_age <= 15:
        tief_hoehe = "38-45 cm"
        tief_kh = "ohne ZL bis 2x 1 kg KH"
    elif plan_age <= 17:
        tief_hoehe = "45 cm (Abstand 4,5 Fuß)"
        tief_kh = "2x 1 kg bis 2x 2 kg KH (Spitze 2x 3 kg)"
    else:
        tief_hoehe = "45-55 cm (Abstand 4-5 Fuß)"
        tief_kh = "2x 2 kg bis 2x 4 kg KH"

    st.info("DOC-Athletik-Trainerplanung: vom Niederen zum Höheren, Links-rechts-Symmetrie und Anpassung an das Belastungsempfinden. Lasten, Umfänge und Einheitsziel vor der Anwendung individuell prüfen.")
    html_matrices = ""

    for te_num in te_liste:
        week, day, short_day = unit_context(te_num, einheiten, startwoche, role)
        # Existing 14-block sequence is keyed to TE, never to calendar week.
        woche = te_num
        abc_dist = vorgaben["start_m"] + ((week - 1 if progression else 0) * vorgaben["step_m"])
        warmup = warmup_text(band, te_num)
        bag_count = weekly_reps(bag_start, week, 20 if capacity else 15, progression)
        bag_wdh = "8–6–5 Wdh. (3 Sätze)" if short_day else f"{bag_count} Wdh. je Satz"
        day_label = "Neuromuskulär / vor dem Spiel" if short_day else "Haupttag"
        extra_rows = ""
        if short_day:
            extra_rows += exercise_row("Komplextransfer: Hürdensprünge / Hürden-Steigesprung / kurze Sprints", "Trainerwahl", "Kurz, technisch sauber", "Trainerfestlegung", "Neuromuskulärer Erinnerungsreiz")
        else:
            burpee_rep = str(weekly_reps(burpee_start,week,100,progression)) + " Wdh." if burpees_ok else "Startwert noch bestätigen"
            extra_rows += exercise_row("Burpees / Liegestützsprünge mit Strecksprung", "Trainerwahl", burpee_rep, "Powerbar 2–3 kg gesamt: ab U15 noch bestätigen" if plan_age >= 14 else "Zusatzlast noch individuell bestätigen", "+1 Wdh./Woche bei Freigabe")
            paired = weekly_reps(cheer_start,week,100,progression) if cheer_start else 0
            pair_text = f"{paired} links + {paired} rechts = {paired*2} gesamt" if paired else "Start je Seite noch festlegen"
            extra_rows += exercise_row("Cheerleading: beidbeinige Fußgelenksprünge, Arme wechselseitig", "Trainerwahl", pair_text, cheer_load(band,geschlecht_wahl), "+1 je Seite / Woche")
            paired = weekly_reps(single_start,week,100,progression) if single_start else 0
            pair_text = f"{paired} links + {paired} rechts = {paired*2} gesamt" if paired else "Start je Bein noch festlegen"
            extra_rows += exercise_row("Leg Speed Curler einbeinig", "Trainerwahl", pair_text, "Trainerfestlegung", "+1 je Bein / Woche")
            bilateral = str(weekly_reps(bilateral_start,week,100,progression)) + " Wdh." if bilateral_start else "Start noch festlegen"
            extra_rows += exercise_row("Leg Speed Curler beidbeinig", "Trainerwahl", bilateral, "Trainerfestlegung", "+1 gemeinsame Wdh./Woche")


        if plan_age <= 13:
            abc_last_str = "1,5-2,0 kg Power Bar über Kopf"
        elif plan_age <= 15:
            abc_last_str = "2,0 kg Power Bar über Kopf" if ft == "Gazelle" else "2,0-3,0 kg Power Bar über Kopf"
        elif plan_age <= 17:
            if woche in [1, 2]:
                abc_last_str = "Ohne Stange (Fokus Bahnung/Frequenz)"
            else:
                abc_last_str = "2,0-3,0 kg Power Bar über Kopf" if gewicht < 70 else "3,0-4,0 kg Power Bar über Kopf"
        else:
            abc_last_str = "2,0-3,0 kg Power Bar über Kopf" if gewicht < 70 else "3,0-4,0 kg Power Bar über Kopf"

        pause_komplex = "45-60s" if geschlecht_wahl == "Weiblich" else "90s" if plan_age <= 15 else "90-120s"

        if plan_age <= 15:
            if woche in [1, 2]:
                tl_pos = "nach_komplex"
                tl_text = "6 x 100m TL (75-80%)"
                tl_pause = "50m Gehpause"
            elif woche in [3, 4]:
                tl_pos = "nach_komplex"
                tl_text = "4 x 150m + 2 x 100m TL (> 75%)"
                tl_pause = "50m Gehpause"
            elif woche in [5, 6]:
                tl_pos = "nach_komplex"
                tl_text = "2 x 300m + 2 x 200m + 2 x 150m TL (Absteigend)"
                tl_pause = "100m Gehpause"
            elif woche == 7:
                tl_pos = "nach_komplex"
                tl_text = "2 x 400m + 2 x 300m + 2 x 200m TL (Absteigend)"
                tl_pause = "100m Gehpause"
            elif woche in [8, 9, 10]:
                tl_pos = "vor_komplex"
                tl_text = "2 x 600m (Basis 60%) + 2 x 400m + 3 x 200m (GLA vorab)"
                tl_pause = "100m Gehpause (200m bei 50m GP)"
            elif woche == 11:
                tl_pos = "vor_komplex"
                tl_text = "3 x 600m TL (Richtwert 1:40 min) + 4 x 150m Speed"
                tl_pause = "100m Gehpause"
            elif woche == 12:
                tl_pos = "nach_komplex"
                tl_text = "Speed-Shuttle auf Kunstrasen: 4 x 55m Doppel-Shuttle + Antritte"
                tl_pause = "Staffelpause"
            elif woche == 13:
                tl_pos = "marathon"
                tl_text = "Athletik & Lauf-Marathon: 3 Runden à 400m TL (50%) + Parcours"
                tl_pause = "Im Kettenablauf"
            else:
                tl_pos = "nach_komplex"
                tl_text = "Abschlusstest: 60m Zeit + 250m Zeit + 600m Zeit (Maximal)"
                tl_pause = "Volle Erholung"

        elif plan_age <= 17:
            if woche in [1, 2]:
                tl_pos = "nach_komplex"
                tl_text = "6 x 100m Technik TL (80%) [Lauf-ABC ohne Stange]"
                tl_pause = "50m Gehpause"
            elif woche in [3, 4]:
                tl_pos = "nach_komplex"
                tl_text = "2 x 300m + 2 x 200m + 2 x 150m TL (Absteigend)"
                tl_pause = "100m Gehpause"
            elif woche in [5, 6]:
                tl_pos = "nach_komplex"
                tl_text = "1 x 500m + 1 x 400m + 2 x 300m + 2 x 200m (Absteigend 70-80%)"
                tl_pause = "100m Gehpause"
            elif woche == 7:
                tl_pos = "nach_komplex"
                tl_text = "2 x 550m + 2 x 350m TL (Kaskade > 65%)"
                tl_pause = "100m Gehpause"
            elif woche in [8, 9, 10]:
                tl_pos = "vor_komplex"
                tl_text = "GLA vorab: 600m, 600m, 500m, 500m (je 100m GP) vor Stationen"
                tl_pause = "100m Gehpause"
            elif woche == 11:
                tl_pos = "vor_komplex"
                tl_text = "GLA vorab: 1 x 700m Kappe + 2 x 500m + 3 x 150m Speed"
                tl_pause = "100m Gehpause"
            elif woche == 12:
                tl_pos = "nach_komplex"
                tl_text = "Witterungs-Speed: 12 x 40m Doppel-Shuttle mit 3 kg ZL"
                tl_pause = "5s Wende / Staffelpause"
            elif woche == 13:
                tl_pos = "marathon"
                tl_text = "Athletik- & Lauf-Marathon: 3x 400m Schleifen-Shuttle + Parcours"
                tl_pause = "Im Kettenablauf"
            else:
                tl_pos = "nach_komplex"
                tl_text = "Saison-Peak: 60m Sprint + 250m + 600m Test auf Zeit"
                tl_pause = "Volle Erholung"

        else:
            if woche in [1, 2]:
                tl_pos = "nach_komplex"
                tl_text = "6 x 100m Technik Sprintlauf (> 85%) direkt nach Station 1"
                tl_pause = "50-100m Gehpause"
            elif woche in [3, 4]:
                tl_pos = "nach_komplex"
                tl_text = "Direct-PAP: 2x 150m Sprint (>85%) + 1x 350m (>70%) + 1x 550m (70%)"
                tl_pause = "100m Gehpause"
            elif woche in [5, 6]:
                tl_pos = "nach_komplex"
                tl_text = "Absteigende Kaskade: 600m (60%) + 500m (70%) + 400m (70%) + 300m (80%)"
                tl_pause = "100m langsame Gehpause"
            elif woche == 7:
                tl_pos = "nach_komplex"
                tl_text = "KZA Kaskade: 2x 450m + 2x 550m (> 60%) + 100m Gehpause"
                tl_pause = "100m Gehpause"
            elif woche in [8, 9, 10]:
                tl_pos = "vor_komplex"
                tl_text = "GLA vorab: 800m (unter 3:15 min) + 600m, 600m (unter 2:30 min) + 500m vor Stationen"
                tl_pause = "100m Gehpause"
            elif woche == 11:
                tl_pos = "vor_komplex"
                tl_text = "GLA vorab: 800m Basis + 600m, 600m + 500m, 500m (je 100m GP)"
                tl_pause = "100m Gehpause"
            elif woche == 12:
                tl_pos = "nach_komplex"
                tl_text = "Staffel-Ausdauer Kunstrasen: 4x 220m (80%) + 5x 220m (90%)"
                tl_pause = "Staffelpause"
            elif woche == 13:
                tl_pos = "marathon"
                tl_text = "Athletik- & Lauf-Marathon: 3x 400m TL (>50%) + Tartan-Halbmond Parcours"
                tl_pause = "Im Kettenablauf"
            else:
                tl_pos = "nach_komplex"
                tl_text = "Abschlusstest: 60m Sprint + 250m Sprint + 600m Test auf Zeit"
                tl_pause = "Volle Erholung"

        if short_day:
            tl_pos = "nach_komplex"
            tl_text = "Kurze Antritte / Sprints nach dem Komplex; Umfang individuell, kein laktazider Laufblock"
            tl_pause = "Erholung nach Trainerfestlegung"
        test_note = (f"Testauswertung (keine Laufvorgabe): {test_distance} m: {test_seconds / (test_percent / 100):.1f} s bei {test_percent}% der gemessenen Testgeschwindigkeit"
                     if test_seconds > 0 else "Tempolauf-Zielzeit: Test derselben Distanz noch eingeben")
        phase_label = "Phase 1: PAP-Komplextraining" if woche <= 7 else "Phase 2: Laktazide Vorab-Ermüdung" if woche <= 11 else "Phase 3: Marathon & Zuspitzung"
        
        if short_day:
            phase_label = "Neuromuskulärer Erinnerungsreiz"
        row_gla_vorab = ""
        if tl_pos == "vor_komplex":
            row_gla_vorab = f'<tr style="background-color: #FCE4D6;"><td style="padding: 6px 8px; border: 1px solid #D9D9D9; font-weight: bold; color: #C00000;">Block 1: GLA Vorab</td><td style="padding: 6px 8px; border: 1px solid #D9D9D9; font-weight: bold;">{tl_text}</td><td style="padding: 6px 8px; border: 1px solid #D9D9D9; text-align: center;">Serie</td><td style="padding: 6px 8px; border: 1px solid #D9D9D9;">Kaskade vor Kraft</td><td style="padding: 6px 8px; border: 1px solid #D9D9D9;">–</td><td style="padding: 6px 8px; border: 1px solid #D9D9D9;">60-70% Vmax</td><td style="padding: 6px 8px; border: 1px solid #D9D9D9; text-align: center;">{tl_pause}</td></tr>'

        row_tl_transfer = ""
        if tl_pos in ["nach_komplex", "marathon"]:
            row_tl_transfer = f'<tr style="background-color: #FCE4D6;"><td style="padding: 6px 8px; border: 1px solid #D9D9D9; font-weight: bold;">Block 2: Lauf / Transfer</td><td style="padding: 6px 8px; border: 1px solid #D9D9D9;">{tl_text}</td><td style="padding: 6px 8px; border: 1px solid #D9D9D9;">Variabel</td><td style="padding: 6px 8px; border: 1px solid #D9D9D9;">Direct-Transfer</td><td style="padding: 6px 8px; border: 1px solid #D9D9D9;">–</td><td style="padding: 6px 8px; border: 1px solid #D9D9D9;">{escape("Kurz und hochwertig" if short_day else "Individuelles Trainingsziel")}</td><td style="padding: 6px 8px; border: 1px solid #D9D9D9; text-align: center;">{tl_pause}</td></tr>'

        html_matrix = f'''<meta charset="utf-8">
<div class="druck-block" style="background-color: #111111; color: #ffffff; border: 2px solid #45a29e; border-radius: 8px; padding: 20px; margin-top: 20px; font-family: Arial, sans-serif;">
<div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #66fcf1; padding-bottom: 5px;">
<h3 style="margin: 0; color: #66fcf1 !important;">TRAININGSMATRIX - EINHEIT: TE {woche}</h3>
<span style="color: #ffb703; font-weight: bold; font-size: 14px;">{phase_label}</span>
</div>
<p style="color: #ffffff !important; font-size: 14px; margin-top: 8px;"><strong>Athlet:</strong> {escape(ziel)} ({gewicht} kg) | <strong>Woche:</strong> {week}, Einheit {day} | <strong>Ziel:</strong> {day_label} | <strong>Modus:</strong> {jump_modus} | <strong>Lauf-ABC Last:</strong> {abc_last_str}</p>
<p>{escape(test_note)}</p>
<table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 13px; color: #000000; border: 1px solid #7F7F7F;">
<thead>
<tr style="background-color: #1F4E78; color: #FFFFFF; font-weight: bold;">
<th style="padding: 8px; border: 1px solid #7F7F7F; width: 16%;">Block / Phase</th>
<th style="padding: 8px; border: 1px solid #7F7F7F; width: 26%;">Trainingsmittel / Übung</th>
<th style="padding: 8px; border: 1px solid #7F7F7F; width: 7%; text-align: center;">Sätze</th>
<th style="padding: 8px; border: 1px solid #7F7F7F; width: 17%;">Wdh. / Distanz</th>
<th style="padding: 8px; border: 1px solid #7F7F7F; width: 16%;">Hardware / Zusatzlast</th>
<th style="padding: 8px; border: 1px solid #7F7F7F; width: 10%;">Intensität</th>
<th style="padding: 8px; border: 1px solid #7F7F7F; width: 8%; text-align: center;">Pause</th>
</tr>
</thead>
<tbody>
<tr style="background-color: #FFF2CC;">
<td style="padding: 6px 8px; border: 1px solid #D9D9D9; font-weight: bold;">Erwärmung</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9;">Einlaufen / Aktivierung</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9; text-align: center;">1</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9;">{escape(warmup)}</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9;">–</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9;">Einlaufen</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9; text-align: center;">Trinkp.</td>
</tr>
<tr style="background-color: #DDEBF7;">
<td style="padding: 6px 8px; border: 1px solid #D9D9D9; font-weight: bold;">Block 1: ABC</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9;">Kniehebelauf & Anfersen / Streckbein</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9; text-align: center;">2</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9;">{abc_dist:.1f}m hin / STL zurück</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9; font-weight: bold;">{abc_last_str}</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9;">>80% frequent</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9; text-align: center;">2s</td>
</tr>
{row_gla_vorab}
<tr style="background-color: #BDD7EE;">
<td style="padding: 6px 8px; border: 1px solid #D9D9D9; font-weight: bold;">Komplex: Hürden</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9; font-weight: bold;">Hürden-Tiefsprünge (Reaktiv / DVZ)</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9; text-align: center;">3</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9;">{"Kurze Serie nach Trainerwahl" if short_day else "8–12 Hürden (Trainerbasis)"} ({tief_hoehe})</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9;">{tief_kh}</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9;">Maximal explosiv</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9; text-align: center;">3 Min. SP</td>
</tr>
<tr style="background-color: #FCE4D6;">
<td style="padding: 6px 8px; border: 1px solid #D9D9D9; font-weight: bold;">Komplex: Hex Bar</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9; font-weight: bold;">Kreuzhebe-Streckung (Hex Bar / KB)</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9; text-align: center;">{"3" if short_day else "3–4 (Trainerbasis)"}</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9;">{"8–6–5 Wdh." if short_day else "8–12 Wdh. (Trainerbasis)"}</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9; font-weight: bold;">{hex_text}</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9;">Maximal</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9; text-align: center;">{pause_komplex}</td>
</tr>
<tr style="background-color: #FCE4D6;">
<td style="padding: 6px 8px; border: 1px solid #D9D9D9; font-weight: bold;">Komplex: Bags</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9;">Front Squat Jumps / Anreiß-Sprünge</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9; text-align: center;">3</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9; font-weight: bold;">{bag_wdh}</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9; font-weight: bold;">{bag_text}</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9;">Explosiv</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9; text-align: center;">90s</td>
</tr>
<tr style="background-color: #FCE4D6;">
<td style="padding: 6px 8px; border: 1px solid #D9D9D9; font-weight: bold;">Komplex: Bälle</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9;">Umsatz / Ausstoß-Jumps & Crunches</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9; text-align: center;">3</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9;">{"5–8 Wdh." if short_day else "12–15 Wdh. (Trainerbasis)"}</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9;">Griffball {gb_last_kg} kg</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9;">Max. Schnellkraft</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9; text-align: center;">60s</td>
</tr>
{row_tl_transfer}
{extra_rows}
<tr style="background-color: #E2EFDA;">
<td style="padding: 6px 8px; border: 1px solid #D9D9D9; font-weight: bold;">Block 3: Rumpf/TRX</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9;">Zug im Schrägliegehang am TRX / Barren</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9;">3</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9;">{"5–8 Wdh." if short_day else "12–15 Wdh. (Trainerbasis)"}</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9;">Körpergewicht</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9;">Submaximal</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9; text-align: center;">60s</td>
</tr>
<tr style="background-color: #F2F2F2;">
<td style="padding: 6px 8px; border: 1px solid #D9D9D9; font-weight: bold;">Cool-Down</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9;">Auslaufen & Statische Tonus-Regulation</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9; text-align: center;">1</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9;">300-400 m</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9;">–</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9;">Sehr locker</td>
<td style="padding: 6px 8px; border: 1px solid #D9D9D9; text-align: center;">–</td>
</tr>
</tbody>
</table>
</div>'''
        html_matrices += html_matrix

    st.markdown(html_matrices, unsafe_allow_html=True)
    st.markdown("---")

    st.download_button(
        label="💾 Trainingsplan und Tempotabelle herunterladen",
        data="<!doctype html><html lang=\"de\"><head><meta charset=\"utf-8\"><title>Doc Athletic Trainingsplan</title><style>body{font-family:Arial,sans-serif}table{border-collapse:collapse}th,td{padding:6px;border:1px solid #aaa}@media print{@page{size:A4 landscape;margin:10mm}.druck-block{break-before:page}}</style></head><body>" + "<h1>Doc Athletic 23.8.2 · Trainingsentwurf</h1><p>Trainerplanung nach individuellen Referenzen und Belastungsverträglichkeit. Berechnete Richtwerte sind Orientierungshilfen.</p><h2>Tempotabelle 50–800 m</h2><p>Prozentwerte der mittleren Referenzgeschwindigkeit. Zwischenwerte und ausdrücklich aktivierte Fortsetzungen sind als Richtwerte gekennzeichnet. Einlaufzeiten bleiben separat.</p>" + pd.DataFrame(tempo_data).to_html(index=False, escape=True) + html_matrices + "</body></html>",
        file_name=f"Doc_Athletic_Trainingsplan_{ziel.replace(' ', '_')}.html",
        mime="text/html; charset=utf-8"
    )

    col_f1, col_f2, col_f3 = st.columns([1, 2, 1])
    with col_f2:
        st.markdown("""<div style="text-align: center; border: 2px solid #45a29e; border-radius: 8px; padding: 15px; background-color: #111111;">
<h2 style="color: #66fcf1 !important; margin-bottom: 5px; font-family: Arial, sans-serif;">Aufgeben gilt nicht!</h2>
<p style="color: #ffb703 !important; font-size: 16px; font-weight: bold; margin: 8px 0;">>>Das, was du fühlst, ist nicht das, was du kannst.<<</p>
<p style="color: #ffffff !important; font-size: 13px; letter-spacing: 1px; margin-top: 5px;">DOC ATHLETIC EVOLUTION 23.8.2</p>
</div>""", unsafe_allow_html=True)
        lade_bild(["Foto.jpg", "Foto.JPG", "foto.jpg", "foto.JPG", "Foto.jpeg", "foto.jpeg", "Foto.png", "foto.png"], use_col=True)
