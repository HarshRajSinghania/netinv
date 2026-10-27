# Contribuer à netinv

Merci de ton intérêt ! Toute contribution est bienvenue, même petite : une ligne dans la liste des fabricants, une traduction, une correction de faute ou un rapport de bug.

## Signaler un bug ou proposer une idée

Ouvre une [issue](../../issues) en indiquant :

- ton système (Windows, Linux, macOS) et ta version de Python ;
- la commande lancée et ce que tu attendais ;
- ce qui s'est passé (message d'erreur complet).

⚠️ **Ne colle jamais un rapport de scan réel** (IP, adresses MAC, noms d'hôtes de ton réseau). Remplace-les par des valeurs fictives, par exemple `192.168.1.x` ou `aa:bb:cc:dd:ee:ff`.

## Proposer une modification

1. Fais un *fork* du dépôt, puis crée une branche : `git checkout -b ma-modif`
2. Fais ta modification et teste-la (voir plus bas).
3. Ouvre une *pull request* qui explique ce que tu as changé et pourquoi.

Une pull request = un sujet. Plusieurs petites PR valent mieux qu'une grosse.

## Contributions faciles pour commencer

### Ajouter un fabricant (OUI)

Le fichier `app/netinv/data/oui.txt` associe le début d'une adresse MAC à un fabricant. Une ligne par entrée, **séparée par une tabulation** :

```
AA:BB:CC	Nom du fabricant
```

- Préfixe en majuscules, séparé par `:`.
- Vérifie le préfixe dans le registre officiel de l'IEEE : https://standards-oui.ieee.org/
- Garde le fichier trié par préfixe.

### Ajouter une langue

1. Copie `app/netinv/locales/en.json` vers `app/netinv/locales/<code>.json` (ex. `es.json`, `de.json`).
2. Traduis uniquement les valeurs, pas les clés, et garde les `{variables}` telles quelles.
3. Teste avec `--lang <code>`.

La langue apparaît automatiquement dans l'option `--lang`.

### Ajouter un format d'export

Dans `app/netinv/exporters.py`, écris une fonction `to_<nom>(hosts, t) -> str` puis ajoute-la au dictionnaire `EXPORTERS`.

## Règles du projet

- **Aucune dépendance externe** : uniquement la bibliothèque standard de Python.
- **Pas besoin d'être administrateur** : pas de paquets bruts ni de raw sockets.
- **Python 3.9 ou plus récent.**
- Tous les textes affichés passent par les fichiers de `locales/` : pas de texte en dur dans le code.
- Code lisible, fonctions courtes, docstrings en anglais.

## Tester ta modification

Depuis le dossier du dépôt :

```bash
export PYTHONPATH=app          # Windows : set PYTHONPATH=app
python -m netinv scan 127.0.0.1 --no-ping
python -m netinv scan --help
```

Puis scanne ton propre réseau et vérifie les exports (`-o test.html`, `-o test.csv`, `-o test.json`). Ces fichiers sont ignorés par git : ils ne partiront pas dans ta PR.

## Usage responsable

netinv ne doit être utilisé que sur des réseaux qui t'appartiennent ou que tu es autorisé à scanner. Les contributions qui servent à contourner des protections ou à rendre les scans furtifs ne seront pas acceptées.

## Licence

En contribuant, tu acceptes que ton code soit publié sous la [licence MIT](LICENSE) du projet.
