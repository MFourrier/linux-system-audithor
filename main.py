""" Linux System Audit Tool
Script Python CLI : utilisateurs avec sudo, ports ouverts,
services actifs, fichiers SUID, dernières connexions SSH,
crontabs actives. Output JSON + terminal coloré.
"""
import argparse
from colorama import init, Fore, Style
init(autoreset=True)
import json 

import crontabs_actives
import derniers_ssh
import ports_ouverts
import services_actifs
import suid
import utilisateurs_sudo


def afficher(resultat, entete=None):
    if entete:
        print(Style.BRIGHT + Fore.CYAN + entete)

    if not resultat["succes"]:
        print(Fore.RED + f"[ERREUR] {resultat['data']}")
        print()
        return

    data = resultat["data"]

    if isinstance(data, str):
        print(data if data.strip() else Fore.BLUE + "(aucun résultat)")

    elif isinstance(data, list):
        if not data:
            print(Fore.LIGHTBLACK_EX + "(aucun résultat)")
        else:
            for item in data:
                valeur = item.get("data", item) if isinstance(item, dict) else item
                print(Fore.GREEN + f"› {valeur}")

    else:
        print(data)

    #print()


parser = argparse.ArgumentParser(prog="Auditeur de system linux")
subparser = parser.add_subparsers(dest="commande")
jsoon = parser.add_argument("--json", help="Rediriger le resultat vers un fichier json" , metavar="Chemin_fichier")

cron = subparser.add_parser("cron", help="Lister les éléments de la crontab de l'utilisateur en cours")
cron.set_defaults(func=crontabs_actives.get_crontabs_actives)

service = subparser.add_parser("service", help="Lister les différents services actifs")
service.set_defaults(func=services_actifs.get_active_services)

ssh = subparser.add_parser("ssh", help="Lister les dernières connexions SSH")
ssh.set_defaults(func=derniers_ssh.get_last_ssh)

port = subparser.add_parser("open-port", help="Lister les ports ouverts")
port.set_defaults(func=ports_ouverts.get_open_ports)

user = subparser.add_parser("sudo-users", help="Lister les utilisateurs avec sudo")
user.set_defaults(func=utilisateurs_sudo.get_sudo_users)

s = subparser.add_parser("suid", help="Lister les fichiers SUID")
s.set_defaults(func=suid.get_suid_files)

all_cmd = subparser.add_parser("all", help="Exécuter toutes les commandes de l'audit")

args = parser.parse_args()

if args.commande == "all":
    audits = [
        ("-----cron-----", crontabs_actives.get_crontabs_actives),
        ("-----service-----", services_actifs.get_active_services),
        ("-----ssh-----", derniers_ssh.get_last_ssh),
        ("-----open-port-----", ports_ouverts.get_open_ports),
        ("-----sudo-users-----", utilisateurs_sudo.get_sudo_users),
        ("-----suid-----", suid.get_suid_files),
    ]
    if args.json :
        rapport= { nom.strip("-") : fonction() for nom , fonction in audits}
        with open (args.json ,"w", encoding="utf-8") as f :
            json.dump(rapport,f, indent=1 , ensure_ascii=False) 
        print(Fore.LIGHTGREEN_EX +  f"Rapport sauvegarde dans {args.json}")
    else :
        for entete, fonction in audits:
         afficher(fonction(), entete)

elif args.commande is None:
    print(Fore.RED + "Aucune commande n'a été spécifiée. Utilisez -h pour afficher l'aide.")

else:
    if args.json :
        with open (args.json , "w", encoding="utf-8") as f :
            json.dump({args.commande : args.func()} ,f ,  indent=1 , ensure_ascii=False)
        print(Fore.BLUE + f"Rapport sauvegarde dans {args.json}")
    else :
        afficher(args.func(),args.commande)