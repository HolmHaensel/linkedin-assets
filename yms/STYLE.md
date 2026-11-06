# YMS Post-Style "Höhenlinien" (v4)

Gilt ab 02.11.2026. Bilder entstehen als Claude-Design-Canvas (`.dc.html` je Post-Ordner) und werden mit `tools/export_yms_design.py` als Bild exportiert. Eigene Illustrationen als flache Vektorformen, feine Höhenlinien als Motiv, sehr große Raleway 900 mit bewussten Zeilenumbrüchen. Farben und Textregeln wie unten.

## Basis: Style "Seite" (v3)

Gilt ab 02.11.2026 und ersetzt "Der Kreis". Vorbild ist Holms GoHighLevel-Landingpage. Renderer: `tools/render_yms_v3.py`. Beispiel: `yms/posts/2026-11-03-probestunde/`.

## Visuell
- Hintergründe im Wechsel: #f0f4f5, #ffffff, dunkel #0e161c. Text #162932, Fließtext #57666b.
- Teal #4db8b0 (auf Hell #3a9e97) für Eyebrow, Highlight und Grafiken. Rot #e05252 nur für den CTA-Button.
- Raleway 800 in normaler Schreibweise, Eyebrow in Lato Versalien. Karten mit feiner Linie und runden Ecken.
- Holm ist sichtbar: Porträt im Kreis (`tools/brand/holm-portrait.jpg`) auf der Vorstellungs-Slide und klein im Footer jeder Slide.
- Grafiken, wenn sie Inhalt klarer machen: Abläufe (`timeline`), Kosten (`grid`).

## Text
- Die Marke heißt immer YOGA MACHT STARK, durchgehend in Großbuchstaben. Nie anders schreiben.
- Schwerpunkt B2B: Business Yoga für HR, BGM und Geschäftsführung. Haupt-CTA: kostenlose Probestunde.
- Persönlich, kompetent, freundlich, nicht reißerisch. Ich-Form. Benefit zuerst, Feature als Beleg, kein Fachjargon, nur Belegbares.
- Die App ist noch nicht fertig: keine Funktionstests, Messungen, Re-Tests oder App-Funktionen bewerben.
- Referenz, die genannt werden darf: Gewandhaus Leipzig. HealthBioCare nie öffentlich nennen.
- Preise und Rechenwege offen zeigen. Förderung nur mit Bedingungen nennen, Heilversprechen nie.

## Google Business und Pinterest
Beide bekommen immer eine eigene Version und einen eigenen Metricool-Entwurf, nie das 4:5-Carousel. Google Business: ein Bild. Pinterest: Einzel-Pin oder Carousel-Pin mit 2 bis 5 Bildern im selben Format (2:3 oder 1:1), kein Video, Business-Konto nötig. Carousel-Pin in Metricool wird noch getestet.
- Google Business: 1200 x 900 (4:3), Typ `publication`, Text bis 1500 Zeichen, lokal formuliert, ohne Hashtags, voller Link.
- Pinterest: 1000 x 1500 (2:3), Titel bis 100 Zeichen, Beschreibung bis 500 Zeichen, Suchbegriffe im Titel, alles Wichtige auf einem Bild, pinLink auf die passende Seite. Board 684547280800331892 (aus bestehenden Posts).

## Grafiken zum Verständnis (Pflicht, gilt ab 06.11.2026)
Jeder Post entsteht in Claude Design und bekommt Grafiken, die den Inhalt erklären. Übungen werden immer gezeigt, nicht nur beschrieben: Leser müssen ohne Vorwissen sehen, wie die Übung aussieht (Figur auf dem Stuhl, Schritte nummeriert, Richtung als Pfeil, Atem als Kurve). Vorlage: `yms/posts/2026-11-07-drei-minuten-design/`.
