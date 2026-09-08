import subprocess
import pwd
#reccuperer les contabs actives de l'utilisateur qui lance avec crontab -l
#crontab=subprocess.run(["crontab","-l"], capture_output=True, text=True)
#print(crontab.stdout)
def get_crontabs_actives() :
    try :
        users = pwd.getpwall() #reccuperer les infirmations sur tous les utilisateures su system
    except Exception as e : #cas ou la reccuperation echoue
        return { "succes": False , "data" : f"Erreur dans la reccuperation des utilisateurs du systeme : {e}" }
    comptes=[]
    crontabs=[]
    for user in users :
        if (user.pw_uid <= 0  or user.pw_uid >= 1000 )and (user.pw_uid != 65534) and  (user.pw_shell  not in ("/usr/sbin/nologin" , "/bin/false")) :
            comptes.append(user.pw_name) #reccuperer les utilisateurs humains et root ( en excluant les utilisatuers du system et noblody(65534))
    for compte in comptes :
        try:    #parcourrir les comptes pour reccuperer  leurs crontab
            cron=subprocess.run(["crontab","-u",compte,"-l"], capture_output=True,text=True)
        except Exception as e :
            crontabs.append({ "utilisateur" : compte ,"succes": False , "data" : f" Erreur dans la reccuperation de la crontab de {compte} : {e}" })
            
        else : 
            if cron.returncode == 0 :
                crontabs.append({ "utilisateur" : compte ,"succes": True , "data" : f" ---------------La crontab de {compte}-------------------- " +cron.stdout })
    if len(crontabs) != 0 : #renvoyer les resultats touours sous forme de liste de dicts pour uniformiser le format de retour
        return { "succes": True , "data" : crontabs }
    else : 
        return { "succes": True , "data" : [{"utilisateur": "" , "succes": True , "data": "Aucune crontab active pour les utilisateurs du systeme" }]}
    

