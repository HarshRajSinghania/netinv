# netinv

Petit outil d'inventaire du réseau local, en Python, sans dépendance et sans droits administrateur.

Il liste les appareils de ton réseau avec leur **adresse IP, nom d'hôte, adresse MAC, fabricant, ports ouverts et latence**, puis génère un rapport HTML avec une barre de recherche (export CSV et JSON possibles aussi).

## Utilisation (Windows)

1. Installer Python 3.9 ou plus récent : `winget install Python.Python.3.12`
2. Télécharger ce dépôt (bouton **Code → Download ZIP**) et le décompresser
3. Double-cliquer sur **`scanner-reseau.bat`**
4. Appuyer sur Entrée pour scanner le réseau actuel, ou taper une plage (`192.168.1.0/24`, `192.168.1.10-50`)

Le rapport `inventaire-reseau.html` s'ouvre dans le navigateur.

## En ligne de commande (Windows, Linux, macOS)

```bash
# depuis le dossier du dépôt
export PYTHONPATH=app          # Windows : set PYTHONPATH=app
python -m netinv scan 192.168.1.0/24 --lang fr
python -m netinv scan -p 22,80,443,8006 -o inventaire.csv
python -m netinv scan --help
```

## Fonctionnement

- **Détection** : `ping` système et connexion TCP sur quelques ports courants (une connexion refusée prouve aussi que l'appareil est là).
- **Ports** : simple connexion TCP, pas de paquets bruts, donc pas besoin d'être admin.
- **MAC et fabricant** : lus dans la table ARP du système, puis comparés à `app/netinv/data/oui.txt`. Visibles uniquement pour les appareils du même sous-réseau.
- **Noms** : DNS inverse.

## ⚠️ Usage responsable

N'utilise cet outil que sur des réseaux qui t'appartiennent ou que tu es autorisé à scanner.

## Licence

[MIT](LICENSE) © Malo Le Foll
