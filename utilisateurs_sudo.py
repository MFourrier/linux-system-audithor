import subprocess
#parser /etc/group pour reccuperer les membres du groupe sudo
import grp
def get_sudo_users() :
    sudo_users=[]
    try :
        info= grp.getgrnam("sudo")
    except Exception as e :
        return { "succes": False , "data" : str(e) }
    else : 
         for membre in info.gr_mem :
             sudo_users.append(membre)
    return { "succes": True , "data" : sudo_users }