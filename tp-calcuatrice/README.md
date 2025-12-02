TP Calcuatrice
===============

Petit projet Java : une calculatrice CLI avec historique JSON.

Build
-----
Vous pouvez construire avec Maven :

```bash
mvn -f tp-calcuatrice/pom.xml package
```

Run
---
Interactive mode (default history file `history.json`):

```bash
java -cp tp-calcuatrice/target/classes;tp-calcuatrice/target/dependency/* calculator.Main
```

Non-interactive:

```bash
java -cp tp-calcuatrice/target/classes;tp-calcuatrice/target/dependency/* calculator.Main add 2 3
```

Exemples de commandes dans le mode interactif:
- `add 1 2`
- `sub 5 3`
- `mul 2 4`
- `div 10 2`
- `history` (affiche l'historique)
- `save` (force l'écriture de l'historique)

Notes
-----
Ce projet utilise Gson pour sérialiser l'historique en JSON (`history.json`).
