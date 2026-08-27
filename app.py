# Dynamische Belastungsparameter (Wissenschaftliche Steuerung nach Athletenprofil)
    athleten_alter = int(aktuelle_daten["alter"])
    
    # Lastberechnung Mechanische Systeme
    gewichtsstange = "2 Kg" if athleten_alter < 16 else "2-3 Kg"
    power_bar_leicht = "2 Kg" if athleten_alter < 16 else "4 Kg"
    power_bar_schwer = "3-4 Kg" if athleten_alter < 16 else "4-6 Kg"
    speed_jumper_last = "5-8 Kg" if ft in ["Gazelle", "Ausdauer"] and athleten_alter < 18 else "8-12 Kg"
    
    # Spezifische Laufparameter
    stl_vorgabe = "2x 100m u. 3x 60m"
    stl_intensitat = "70% u. 80% Vmax"

    st.markdown("---")
    st.subheader(f"📄 Offizielles Trainingsprotokoll & Druckmatrix: {ziel} ({te_wahl})")
    st.markdown("Zur Dokumentation auf dem Platz via **Strg + P** ausdrucken.")

    st.markdown(f"""
    <div class="druck-block">
        <h2 style="border-bottom: 2px solid #000000; padding-bottom: 5px; margin-top: 0;">DOC ATHLETIC TRAININGSMATRIX</h2>
        <p><strong>Athlet / Kader:</strong> {ziel} &nbsp;&nbsp;|&nbsp;&nbsp; <strong>Einheit:</strong> {te_wahl} &nbsp;&nbsp;|&nbsp;&nbsp; <strong>Fasertyp:</strong> {ft} &nbsp;&nbsp;|&nbsp;&nbsp; <strong>SBE-Ziel:</strong> {sbe_ziel}</p>
        <hr style="border: 1px solid #000;">
        
        <table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 13px;">
            <thead>
                <tr style="background-color: #e5e7eb; border-bottom: 2px solid #000000;">
                    <th style="padding: 6px; border: 1px solid #000;">Block / Spezifisches Trainingsmittel</th>
                    <th style="padding: 6px; border: 1px solid #000; text-align: center;">Sätze</th>
                    <th style="padding: 6px; border: 1px solid #000;">Wdh. / Exakte Strecke</th>
                    <th style="padding: 6px; border: 1px solid #000;">Intensität / Zusatzlast</th>
                    <th style="padding: 6px; border: 1px solid #000; text-align: center;">Pause</th>
                    <th style="padding: 6px; border: 1px solid #000; text-align: center; width: 70px;">SBE (Ist)</th>
                </tr>
            </thead>
            <tbody>
                <!-- Block 1 -->
                <tr>
                    <td style="padding: 6px; border: 1px solid #000;"><strong>Block 1: Allg. Erwärmung</strong> (Shuttle, über ganzen Fuß abrollen)</td>
                    <td style="padding: 6px; border: 1px solid #000; text-align: center;">1</td>
                    <td style="padding: 6px; border: 1px solid #000;">400 m</td>
                    <td style="padding: 6px; border: 1px solid #000;">Mobilisation</td>
                    <td style="padding: 6px; border: 1px solid #000; text-align: center;">-</td>
                    <td style="padding: 6px; border: 1px solid #000;"></td>
                </tr>
                <tr>
                    <td style="padding: 6px; border: 1px solid #000;">Spez. Erwärmung (Steigerungsläufe locker/frequentiert)</td>
                    <td style="padding: 6px; border: 1px solid #000; text-align: center;">5</td>
                    <td style="padding: 6px; border: 1px solid #000;">{stl_vorgabe}</td>
                    <td style="padding: 6px; border: 1px solid #000;">{stl_intensitat}</td>
                    <td style="padding: 6px; border: 1px solid #000; text-align: center;">Trinkp.</td>
                    <td style="padding: 6px; border: 1px solid #000;"></td>
                </tr>
                <!-- Block 2 -->
                <tr>
                    <td style="padding: 6px; border: 1px solid #000; background-color: #f9fafb;" colspan="6"><strong>Block 2: Neuromuskuläre & koord. Innervation</strong> (>80% Beschleunigung zurück)</td>
                </tr>
                <tr>
                    <td style="padding: 6px; border: 1px solid #000;">Kniehebelauf & Anfersen</td>
                    <td style="padding: 6px; border: 1px solid #000; text-align: center;">2</td>
                    <td style="padding: 6px; border: 1px solid #000;">{abc_dist:.1f} m hin / {abc_dist:.1f} m zurück</td>
                    <td style="padding: 6px; border: 1px solid #000;">>80% ({gewichtsstange} Gewichtsstange)</td>
                    <td style="padding: 6px; border: 1px solid #000; text-align: center;">2s Wende</td>
                    <td style="padding: 6px; border: 1px solid #000;"></td>
                </tr>
                <tr>
                    <td style="padding: 6px; border: 1px solid #000;">Seitliche Nachstellschritte & Überkreuzlauf</td>
                    <td style="padding: 6px; border: 1px solid #000; text-align: center;">2</td>
                    <td style="padding: 6px; border: 1px solid #000;">{abc_dist:.1f} m hin / {abc_dist:.1f} m zurück</td>
                    <td style="padding: 6px; border: 1px solid #000;">>80% ({gewichtsstange} Gewichtsstange)</td>
                    <td style="padding: 6px; border: 1px solid #000; text-align: center;">2s Wende</td>
                    <td style="padding: 6px; border: 1px solid #000;"></td>
                </tr>
                <tr>
                    <td style="padding: 6px; border: 1px solid #000;">Hopserlauf mittel & Streckbeinlauf</td>
                    <td style="padding: 6px; border: 1px solid #000; text-align: center;">2</td>
                    <td style="padding: 6px; border: 1px solid #000;">{abc_dist:.1f} m / {abc_dist:.1f} m zurück</td>
                    <td style="padding: 6px; border: 1px solid #000;">>80% ({gewichtsstange} Gewichtsstange)</td>
                    <td style="padding: 6px; border: 1px solid #000; text-align: center;">2s Wende</td>
                    <td style="padding: 6px; border: 1px solid #000;"></td>
                </tr>
                <!-- Block 3 -->
                <tr>
                    <td style="padding: 6px; border: 1px solid #000; background-color: #f9fafb;" colspan="6"><strong>Block 3: Kompl. Kraftfähigkeiten / Reaktiv-Komplex</strong></td>
                </tr>
                <tr>
                    <td style="padding: 6px; border: 1px solid #000;">Shuttle-Beschleunigung (Technik)</td>
                    <td style="padding: 6px; border: 1px solid #000; text-align: center;">4</td>
                    <td style="padding: 6px; border: 1px solid #000;">40 m</td>
                    <td style="padding: 6px; border: 1px solid #000;">>85% Vmax</td>
                    <td style="padding: 6px; border: 1px solid #000; text-align: center;">10s zw. Läufen</td>
                    <td style="padding: 6px; border: 1px solid #000;"></td>
                </tr>
                <tr>
                    <td style="padding: 6px; border: 1px solid #000;">Squat-Stoß-Jumps (im Systemwechsel)</td>
                    <td style="padding: 6px; border: 1px solid #000; text-align: center;">4</td>
                    <td style="padding: 6px; border: 1px solid #000;">10 - 12 Wdh.</td>
                    <td style="padding: 6px; border: 1px solid #000;">{power_bar_schwer} Power Bar</td>
                    <td style="padding: 6px; border: 1px solid #000; text-align: center;">1 min Pause</td>
                    <td style="padding: 6px; border: 1px solid #000;"></td>
                </tr>
                <tr>
                    <td style="padding: 6px; border: 1px solid #000;">Technik Squat Jumps (11° Neigung)</td>
                    <td style="padding: 6px; border: 1px solid #000; text-align: center;">3</td>
                    <td style="padding: 6px; border: 1px solid #000;">10 - 12 Wdh.</td>
                    <td style="padding: 6px; border: 1px solid #000;">{speed_jumper_last} Speed Jumper</td>
                    <td style="padding: 6px; border: 1px solid #000; text-align: center;">90s</td>
                    <td style="padding: 6px; border: 1px solid #000;"></td>
                </tr>
                <!-- Block 4 -->
                <tr>
                    <td style="padding: 6px; border: 1px solid #000;"><strong>Block 4: Tempoläufe (TL)</strong> (Spezifischer Umfang)</td>
                    <td style="padding: 6px; border: 1px solid #000; text-align: center;">{abc_sets}</td>
                    <td style="padding: 6px; border: 1px solid #000;">100 m</td>
                    <td style="padding: 6px; border: 1px solid #000;">80% Vmax (Basis {calc_100}s)</td>
                    <td style="padding: 6px; border: 1px solid #000; text-align: center;">Gehpause</td>
                    <td style="padding: 6px; border: 1px solid #000;"></td>
                </tr>
                <!-- Block 5 -->
                <tr>
                    <td style="padding: 6px; border: 1px solid #000; background-color: #f9fafb;" colspan="6"><strong>Block 5: Unilaterale Belastung & Ischiocrurale Sicherung</strong></td>
                </tr>
                <tr>
                    <td style="padding: 6px; border: 1px solid #000;">Ausfallschritt-Gehen/Jumps Shuttle</td>
                    <td style="padding: 6px; border: 1px solid #000; text-align: center;">2</td>
                    <td style="padding: 6px; border: 1px solid #000;">12 m</td>
                    <td style="padding: 6px; border: 1px solid #000;">2x {power_bar_leicht} Kettlebell</td>
                    <td style="padding: 6px; border: 1px solid #000; text-align: center;">45s</td>
                    <td style="padding: 6px; border: 1px solid #000;"></td>
                </tr>
                <tr>
                    <td style="padding: 6px; border: 1px solid #000;">Leg Speed Curler (Beidbeinig)</td>
                    <td style="padding: 6px; border: 1px solid #000; text-align: center;">3</td>
                    <td style="padding: 6px; border: 1px solid #000;">20-24 Wdh. (90% Ampl.)</td>
                    <td style="padding: 6px; border: 1px solid #000;">Körpergewicht</td>
                    <td style="padding: 6px; border: 1px solid #000; text-align: center;">60s</td>
                    <td style="padding: 6px; border: 1px solid #000;"></td>
                </tr>
            </tbody>
        </table>
        
        <br>
        <p style="text-align: center; font-size: 11px; margin-bottom: 0;"><em>Doc Athletic Train Smart Philosophie — Aufgeben gilt nicht!</em></p>
    </div>
    """, unsafe_allow_html=True)
