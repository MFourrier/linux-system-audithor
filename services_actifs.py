import subprocess
#utiliser systemctl pour interagir avec le system et demander les services actifs
def get_active_services():
    try :
        actifs=subprocess.run (["systemctl",  "list-units", "--type=service", "--state=active", "--no-pager"], capture_output=True , text=True)
    except Exception as e : #cas ou la commande ne peut pas etre lancee
       return  { "succes": False , "data" :str(e)  }
    else :
        if actifs.returncode == 0 :
            return  { "succes": True , "data" : actifs.stdout } #la commande a fonctionné et on retourne le resultat
        else :
            return { "succes": False , "data" : actifs.stderr } #la commande a rencontre ue erreur et on retourne le message d'erreur