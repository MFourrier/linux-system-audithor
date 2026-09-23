""" Linux System Audit Tool 
Script Python CLI : utilisateurs avec sudo, ports ouverts, 
services actifs, fichiers SUID, dernières connexions SSH ,
crontabs actives. Output JSON + terminal coloré. 
"""
import argparse
import crontabs_actives
import derniers_ssh
import ports_ouverts
import services_actifs
import suid
import utilisateurs_sudo



parser=argparse.ArgumentParser(prog="Auditeur de system linux")
subparser=parser.add_subparsers(dest="commande")
cron=subparser.add_parser("cron",help="Lister les element de la crontab de l'utilisateur en cours")
cron.set_defaults(func=crontabs_actives.get_crontabs_actives)
service=subparser.add_parser("service",help="Lister les differents services actifs")
service.set_defaults(func=services_actifs.get_active_services)
ssh=subparser.add_parser("ssh",help="Lister les dernières connexions SSH")
ssh.set_defaults(func=derniers_ssh.get_last_ssh)
port=subparser.add_parser("open-port",help="Lister les ports ouverts")
port.set_defaults(func=ports_ouverts.get_open_ports)
args=parser.parse_args()
if args.commande == "cron" :
    for crontab in args.func()["data"] :
        print(crontab["data"])
else :
    print(args.func()["data"])