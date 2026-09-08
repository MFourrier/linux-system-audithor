import subprocess
#utiliser ss pour rccuperer les port ouverts visibles cote machine
def get_open_ports() :
    
    try :
        ports=subprocess.run([ "ss", "-tulnp" ], capture_output=True , text=True)
    except Exception as e : #cas ou la commande ne fonctionne pas
        return { "succes": False , "data" :str(e) }
    else :
        if ports.returncode == 0 :
            return  { "succes": True , "data" : ports.stdout }
        else :
            return { "succes": False , "data" : ports.stderr } #la commande a rencontre ue erreur et on retourne le message d'erreur