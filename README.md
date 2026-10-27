# netinv

[![tests](https://github.com/malolefoll/netinv/actions/workflows/tests.yml/badge.svg)](https://github.com/malolefoll/netinv/actions/workflows/tests.yml)
[![Licence MIT](https://img.shields.io/badge/licence-MIT-green.svg)](LICENSE)
[![Contributions bienvenues](https://img.shields.io/badge/contributions-bienvenues-brightgreen.svg)](CONTRIBUTING.md)

🇬🇧 [English below](#english)

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

## Contribuer

Les contributions sont les bienvenues, même petites ! Commence par le [guide de contribution](CONTRIBUTING.md) et les issues marquées [`good first issue`](https://github.com/malolefoll/netinv/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).

## Licence

[MIT](LICENSE) © Malo Le Foll

---

## English

**netinv** is a small local network inventory tool written in Python, with **no dependencies and no admin rights required**. It lists the devices on your network with their **IP address, hostname, MAC address, vendor, open ports and latency**, and exports a searchable HTML report (CSV and JSON too). Works on Windows, Linux and macOS, in English and French.

### Quick start

```bash
git clone https://github.com/malolefoll/netinv.git
cd netinv
export PYTHONPATH=app          # Windows: set PYTHONPATH=app
python -m netinv scan                         # scans your local /24
python -m netinv scan 192.168.1.0/24 -o report.html
python -m netinv scan --help
```

On Windows you can also just double-click `scanner-reseau.bat` (French interface).

### How it works

Hosts are found with the system `ping` and plain TCP connections (no raw packets, so no admin rights). MAC addresses come from the OS ARP table and are matched against `app/netinv/data/oui.txt`; hostnames come from reverse DNS.

### Contributing

Contributions are welcome, including small ones: adding MAC vendors, translating netinv into your language, or adding an export format. See [CONTRIBUTING.md](CONTRIBUTING.md) and the [`good first issue`](https://github.com/malolefoll/netinv/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22) list. Issues and pull requests can be written in English or French.

⚠️ Only scan networks you own or are authorized to scan.
