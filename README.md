# Linux System Auditor

Outil CLI en Python pour auditer rapidement un système Linux : utilisateurs sudo, ports ouverts, services actifs, fichiers SUID, dernières connexions SSH, crontabs actives. Projet du Mois 1 de ma roadmap SOC Analyst.

## Prérequis

- Python 3.8+
- Linux uniquement (utilise `pwd`, `grp`, et des commandes système comme `find`, `ss`, `systemctl`, `journalctl`, `crontab`)
- Dépendance externe : `colorama`

## Installation

```bash
git clone <url-du-repo>
cd linux-system-auditor
pip install -r requirements.txt
```

`requirements.txt` :
```
colorama
```

## Usage

### Sous-commandes disponibles

| Commande | Description |
|---|---|
| `cron` | Liste les crontabs actives des utilisateurs du système |
| `service` | Liste les services actifs (`systemctl`) |
| `ssh` | Liste les dernières connexions SSH (réussies et échouées) |
| `open-port` | Liste les ports ouverts (`ss -tulnp`) |
| `sudo-users` | Liste les membres du groupe sudo |
| `suid` | Liste les fichiers avec bit SUID actif |
| `all` | Exécute les 6 audits à la suite |

### Exemples

```bash
# Un audit isolé, affichage coloré dans le terminal
python main.py sudo-users

# Audit complet
python main.py all

# Audit complet, export JSON au lieu de l'affichage terminal
python main.py --json rapport.json all

# Un seul audit, export JSON
python main.py --json suid.json suid

# Sans sous-commande : affiche un message d'aide
python main.py
```

> ⚠️ `--json FICHIER` doit être placé **avant** la sous-commande : `python main.py --json out.json all`, pas l'inverse.

## Format de sortie

### Terminal (par défaut)

Chaque audit est affiché avec un entête, en couleur selon le statut :

```
-----sudo-users-----
› fourrier
```

Une erreur d'exécution (commande système indisponible, etc.) est affichée en rouge sous la forme `[ERREUR] ...`. Un résultat vide (ex. aucune connexion SSH enregistrée) affiche `(aucun résultat)` plutôt qu'un écran vide silencieux.

### JSON (`--json`)

```json
{
  "sudo-users": {
    "succes": true,
    "data": ["fourrier"]
  }
}
```

Chaque module retourne systématiquement `{"succes": bool, "data": ...}`. Le type de `data` varie selon le module : liste de dicts (`cron`), liste de strings (`sudo-users`), ou string brute multi-lignes (`service`, `open-port`, `suid`, `ssh`) — ce choix est assumé pour ce projet, voir Limitations.

## Architecture

```
main.py                 → argparse, dispatch, fonction afficher()
crontabs_actives.py     → get_crontabs_actives()
derniers_ssh.py         → get_last_ssh()
ports_ouverts.py        → get_open_ports()
services_actifs.py      → get_active_services()
suid.py                 → get_suid_files()
utilisateurs_sudo.py    → get_sudo_users()
```

Chaque module expose une fonction unique sans paramètre, retournant un dict `{"succes": bool, "data": ...}`. `main.py` associe chaque fonction à une sous-commande via `set_defaults(func=...)`, et la fonction `afficher()` adapte le rendu terminal selon le **type réel** du contenu de `data` (string, liste de dicts, liste de strings) plutôt que selon le nom de la commande.

## Limitations connues

- **`find` sans privilèges root** : le scan SUID (`suid`) rencontre généralement des dossiers protégés (`Permission denied`). Ce n'est pas traité comme une erreur bloquante — le résultat partiel est affiché avec une note. Pour un scan exhaustif, lancer en root.
- **Sorties non structurées** : `service`, `open-port`, `suid` et `ssh` retournent le `stdout` brut de la commande système (string multi-lignes), pas une liste structurée. Un export JSON de ces sections contient donc du texte avec des `\n` échappés plutôt que des éléments de liste individuels — assumé pour ce projet, pourrait être amélioré en V2.

## Tests manuels effectués

<!-- À compléter : tests sur les machines de camarades (lundi) -->

| Date | Machine / contexte | Commande testée | Résultat observé | OK ? |
|---|---|---|---|---|
| | Ma machine (Kali) | `all` | | |
| | Ma machine (Kali) | `suid` (non-root) | Permission denied géré, résultat partiel affiché | |
| | Ma machine (Kali) | `sudo-users` | | |
| | Ma machine (Kali) | `--json out.json all` | JSON valide (vérifié avec `python -m json.tool`) | |
| *(à ajouter lundi)* | Machine camarade 1 | | | |
| *(à ajouter lundi)* | Machine camarade 2 | | | |
| *(à ajouter lundi)* | Machine camarade 3 | | | |

## Auteur

Fourrier — Projet Mois 1, roadmap SOC Analyst (18 mois)
