# Spielwiese

Dieses Repository ist eure Sandbox zum Ausprobieren von Git und GitHub. Hier dürft ihr **alles** machen — committen, pushen, branchen, mergen, kaputt machen.

Wenn etwas schiefgeht, ist das **kein Drama**, sondern eine Lerngelegenheit.

---

## Struktur

```
.
├── README.md
├── persoenlich/
│   ├── leonie.md       # Eure pers\u00f6nlichen Spielwiesen
│   ├── jonas.md
│   ├── justin.md
│   └── george.md
└── gemeinsam/
    └── notizen.md      # Hier arbeiten alle gemeinsam
```

### Persönlicher Bereich

In `persoenlich/<euername>.md` dürft ihr machen, was ihr wollt. Hier kommt euch niemand in die Quere — perfekt zum Ausprobieren von Befehlen ohne Stress.

### Gemeinsamer Bereich

In `gemeinsam/notizen.md` schreiben alle gleichzeitig. Hier kann es zu Konflikten kommen — genau das soll auch passieren. Wer Konflikte üben will, kommt hier auf seine Kosten.

---

## Spielregeln

- **Persönliche Datei: euer Reich.** Probiert dort aus, was ihr wollt.
- **Gemeinsame Datei: kurz absprechen oder per Branch arbeiten.** So lernt ihr, wie man Konflikte verhindert — oder löst.
- **Niemand löscht die README absichtlich.** Versehentlich? Kein Problem, kann zurückgeholt werden.
- **Wenn nichts mehr geht: fragen.** Lieber 30 Sekunden fragen als 30 Minuten kämpfen.

---

## Übungsvorschläge zum Aufwärmen

Wenn ihr nicht wisst, was ihr ausprobieren sollt, hier ein paar Ideen:

- **Commit-Übung:** Eure persönliche Datei mit Inhalt füllen — Lieblingsmusik, Hobbys, was auch immer. Mehrere kleine Commits machen.
- **Branch-Übung:** Einen Branch `experiment/<euername>` anlegen, dort etwas ändern, wieder zurück nach `main` wechseln und beobachten, was passiert.
- **Konflikt provozieren:** Mit jemandem absprechen, beide die gleiche Zeile in `gemeinsam/notizen.md` ändern, beide versuchen zu pushen. Der zweite muss den Konflikt lösen.
- **Pull Request:** Einen Branch erstellen, dort eine Datei anlegen, pushen und einen Pull Request öffnen. Ein anderer reviewt und merged.
- **History erkunden:** Mit `git log --oneline --graph --all` sehen, was im Repo schon alles passiert ist.

---

## Klonen

```bash
git clone https://github.com/<USERNAME>/<REPONAME>.git
cd <REPONAME>
```

Die genaue URL findet ihr auf dieser Seite unter dem grünen **Code**-Button.

---

## Bei Fragen

Im Kurs einfach Bescheid geben.
