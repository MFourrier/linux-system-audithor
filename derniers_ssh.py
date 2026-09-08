import subprocess 
#utiliser journalctl pour reccuperer les dernieres connexions ssh
#les resultats sont retournes sous forme de dictionnaires pour faciliter la conversion en json
def get_last_ssh() :
    try :
        ssh=subprocess.run(["journalctl", "-u", "ssh"] ,capture_output=True , text=True )
        resultat=subprocess.run (["grep", "-Ei", "Failed|Accepted"], capture_output=True , text=True , input=ssh.stdout)
    except Exception as e : 
        return { "succes": False , "data" : str(e) }
    else : 
        if resultat.returncode == 0 :
            return { "succes": True , "data" :resultat.stdout }
        else: 
            return { "succes": False , "data" :resultat.stderr }
        
    