import crontabs_actives
import derniers_ssh
import ports_ouverts
import services_actifs
import suid
import utilisateurs_sudo





class PC ():
    def __init__(self,crantabs,ssh,ports,services,suid,usudo):
        self.crontabs=crantabs
        self.ssh=ssh
        self.ports=ports
        self.services=services
        self.suid=suid
        self.usudo=usudo

fourrier=PC(crontabs_actives.get_crontabs_actives(), derniers_ssh.get_last_ssh(), ports_ouverts.get_open_ports(), services_actifs.get_active_services(),
            suid.get_suid_files(), utilisateurs_sudo.get_sudo_users())
 
print (fourrier.usudo["data"])
    
    