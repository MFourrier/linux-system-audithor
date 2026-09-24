import subprocess
#utiliser find pour retrouver les fichiers avec les bit de suid active
def get_suid_files() :
    try :
        files= subprocess.run([ "find", "/", "-type", "f", "-perm", "-u+s"], capture_output=True , text=True)
    except Exception as e :
        return { "succes": False , "data"  : str(e) }
    else :
        if files.returncode == 0 :
            return  { "succes": True , "data" :files.stdout }
        else :
            return { "succes": False , "data" : files.stderr } #la commande a rencontre ue erreur et on retourne le message d'erreur
       
        