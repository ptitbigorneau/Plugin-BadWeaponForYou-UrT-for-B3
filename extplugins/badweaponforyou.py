# BadWeaponForYou Plugin b3 for Urban Terror

__author__  = 'PtitBigorneau www.ptitbigorneau.fr'
__version__ = '1.5.2'

import b3, threading, thread, re
import b3.events
import b3.plugin

def lgear(sgear):

    if sgear=="none":
        rgear="A"
        nsgear="None"
    if sgear=="beretta":
        rgear="F"
        nsgear="Beretta 92G"
    if sgear=="de":
        rgear="G"
        nsgear="Desert Eagle" 
    if sgear=="f":
        rgear="glock"
        nsgear="Glock 18"
    if sgear=="spas":
        rgear="H"
        nsgear="SPAS-12"
    if sgear=="mp5":
        rgear="I"
        nsgear="MP5K"
    if sgear=="ump":
        rgear="J" 
        nsgear="UMP45"                
    if sgear=="hk":
        rgear="K"
        nsgear="HK69"
    if sgear=="lr300":
        rgear="L"
        nsgear="LR300ML"                
    if sgear=="g36":
        rgear="M"
        nsgear="G36"
    if sgear=="psg1":
        rgear="N"
        nsgear="PSG-1"
    if sgear=="sr8":
        rgear="Z"
        nsgear="SR-8"
    if sgear=="ak":
        rgear="a"
        nsgear="AK-103"
    if sgear=="negev":
        rgear="c"
        nsgear="Negev"
    if sgear=="m4":
        rgear="e"
        nsgear="M4A1"
    if sgear=="he":
        rgear="O"
        nsgear="HE Grenade"
    if sgear=="flash":
        rgear="P"
        nsgear="Flash Grenade"
    if sgear=="smoke":
        rgear="Q"
        nsgear="HE Smoke"
    if sgear=="kevlar":
        rgear="R"
        nsgear="Kevlar Vest"
    if sgear=="helmet":
        rgear="W"
        nsgear="Kevlar Helmet"
    if sgear=="silencer":
        rgear="U"
        nsgear="Silencer"
    if sgear=="laser":
        rgear="V"
        nsgear="Laser Sight"
    if sgear=="medkit":
        rgear="T"
        nsgear="MedKit"
    if sgear=="tac":
        rgear="S"
        nsgear="TacGoggles"
    if sgear=="xtra":
        rgear="X"
        nsgear="Extra Ammo"
    if sgear=="colt":
        rgear="g"
        nsgear="Colt1911"
    if sgear=="mac11":
        rgear="h"
        nsgear="Ingram Mac11"

    return rgear, nsgear

class BadweaponforyouPlugin(b3.plugin.Plugin):

    _adminPlugin = None
    _listplayersgear = []
    _bwfyminlevel = 60
    _glminlevel = 20
    _lbwfyminlevel = 20
    _mlbwfyminlevel = 1
    _protectlevel = 20
    _wgminlevel = 20

    def onStartup(self):

        self._adminPlugin = self.console.getPlugin('admin')
        
        if not self._adminPlugin:

            self.error('Could not find admin plugin')
            return False
        
        self._adminPlugin.registerCommand(self, 'bwfy',self._bwfyminlevel, self.cmd_bwfy)
        self._adminPlugin.registerCommand(self, 'listgear',self._glminlevel, self.cmd_listgear)
        self._adminPlugin.registerCommand(self, 'listbwfy',self._lbwfyminlevel, self.cmd_listbwfy)
        self._adminPlugin.registerCommand(self, 'mylistbwfy',self._mlbwfyminlevel, self.cmd_mylistbwfy)
        self._adminPlugin.registerCommand(self, 'whogear',self._wgminlevel, self.cmd_whogear)

        self.registerEvent(b3.events.EVT_CLIENT_GEAR_CHANGE)
        self.registerEvent(b3.events.EVT_CLIENT_NAME_CHANGE)
        self.registerEvent(b3.events.EVT_CLIENT_TEAM_CHANGE)
        self.registerEvent(b3.events.EVT_GAME_ROUND_START)
        self.registerEvent(b3.events.EVT_GAME_MAP_CHANGE)

        self.gamename = self.console.game.gameName

        if self.gamename == 'iourt41':

            self.gmessage = 'gear[beretta|de|spas|mp5|ump|hk|lr300|g36|psg1|sr8|ak|negev|he|smoke|kevlar|helmet|silencer|laser|medkit|tag|xtra]'

        if self.gamename == 'iourt42':

            self.gmessage = 'gear[beretta|de|glock|colt|spas|mp5|ump|mac11|hk|lr300|g36|psg1|sr8|ak|negev|he|flash|smoke|kevlar|helmet|silencer|laser|medkit|tag|xtra]'

    def onLoadConfig(self):

        try:
            self._bwfyminlevel = self.config.getint('settings', 'bwfyminlevel')
        except Exception, err:    
            self.warning("bwfyminlevel using default value. %s" % (err))

        try:
            self._glminlevel = self.config.getint('settings', 'glminlevel')
        except Exception, err: 
            self.warning("glminlevel using default value. %s" % (err))

        try:
            self._lbwfyminlevel = self.config.getint('settings', 'lbwfyminlevel')
        except Exception, err:
            self.warning("lbwfyminlevel using default value. %s" % (err))

        try:
            self._mlbwfyminlevel = self.config.getint('settings', 'mlbwfyminlevel')
        except Exception, err:
            self.warning("mlbwfyminlevel using default value. %s" % (err))
        try:
            self._protectlevel = self.config.getint('settings', 'protectlevel')
        except Exception, err:
            self.warning("protectlevel using default value. %s" % (err))

        try:
            self._wgminlevel = self.config.getint('settings', 'wgminlevel')        
        except Exception, err:
            self.warning("wgminlevel using default value. %s" % (err))

    def onEvent(self,  event):       
        
        if event.type == b3.events.EVT_GAME_MAP_CHANGE :
            
            self._listplayersgear = [] 
        
        if (event.type == b3.events.EVT_CLIENT_TEAM_CHANGE) or (event.type == b3.events.EVT_CLIENT_GEAR_CHANGE) or (event.type == b3.events.EVT_CLIENT_NAME_CHANGE):
                
                client = event.client
                fclient = client.guid
                
                for x in self._listplayersgear:
                    
                    if fclient in x:
                        elligne=x.split(' ')
                        babclientgear= elligne[1]
          
                        if babclientgear in client.gear:
                            if client.team in (2, 3):
                                self.console.write('forceteam %s %s' %(client.cid, 's'))
                                client.message('^3Weapon /gear prohibited for %s ^3: ^7-%s-'%(client.exactName, elligne[2]))
            
    def cmd_bwfy(self, data, client, cmd=None):
        """\
        <playername> <on or off> <gear> - prohibits or not a player from using an equipment
        """
        
        if data:
            input = self._adminPlugin.parseUserCmd(data)
        
        else:
            client.message('!bwfy <playername> <on or off> <gear>')
            return
        
        sclient = self._adminPlugin.findClientPrompt(input[0], client)
        
        if not sclient:
            return False
        
        if sclient.maxLevel >= self._protectlevel:
            client.message('^3Invalid Command on %s!' %(sclient.exactName))
            return False
        
        if not input[1]:
            client.message('!bwfy <playername> <on or off> <gear>')
            return False
        nespace= input[1].count(' ')
        
        if nespace==0:
            client.message('!bwfy <playername> <on or off> <gear>')
            return False        
        
        tdata = input[1].split(' ')
        onoff = tdata[0]
        sgear = tdata[1]    
        
        if (onoff=="on") or (onoff=="off"):
            
            if onoff=='on':
                sayonoff='^2authorized'
            if onoff=='off':
                sayonoff='^1prohibited'
        else:
            client.message('!bwfy <playername> <on or off> <gear>')
            return False
        
        if not sgear in ('beretta', 'de', 'glock', 'colt', 'mac11', 'spas', 'mp5', 'ump', 'hk', 'lr300', 'g36', 'psg1', 'sr8', 'ak', 'negev', 'm4', 'he', 'flash', 'smoke', 'kevlar', 'helmet', 'silencer', 'laser', 'medkit', 'tac', 'xtra'):
     
            client.message('!bwfy <playername> <on or off> <gear>')
            client.message('%s'%self.gmessage)
            return False
        
        if sclient:
        
            self._map=self.console.game.mapName
            
            rlgear = lgear(sgear)
            rgear = rlgear[0]
            ngear = rlgear[1]     
               
            self.console.say('^3For %s ^7-%s-^3 : %s'%(sclient.exactName, ngear, sayonoff))    
            sguid=sclient.guid
                            
            if onoff=="off":

                try:

                    if rgear in sclient.gear:
                        self.console.write('forceteam %s %s' %(sclient.cid, 's'))
                
                        sclient.message('^3%s %s %s'%(sclient.exactName, ngear, sayonoff))

                except:
                
                    sclient.message('^3%s %s %s'%(sclient.exactName, ngear, sayonoff))

                chaine = sguid + " " + rgear + " " + ngear

                for x in self._listplayersgear:
                    if chaine in x:
                        client.message('^3For %s ^7-%s-^3 is already %s'%(sclient.exactName, ngear , sayonoff))
                        return False

                self._listplayersgear.append('%s %s %s'%(sguid, rgear, ngear)) 
                                
            if onoff=="on":

                sclient.message('^3%s %s %s'%(sclient.exactName, ngear, sayonoff))
                chaineoff = sguid + " " + rgear + " " + ngear
                
                for x in self._listplayersgear:
                    if chaineoff in x:
                        self._listplayersgear.remove(x)
                
        else:
            return False

    def cmd_listgear(self, data, client, cmd=None):
        """\
        <playername> - list of weapons and equipments of the player
                """
        
        if data:
            input = self._adminPlugin.parseUserCmd(data)
        else:
            client.message('!listgear <playername>')
            return

        sclient = self._adminPlugin.findClientPrompt(input[0], client)

        if not sclient:
            return False
               
        if (sclient):
        
            a=0
            b=1
            
            for i in xrange(7):
                if sclient.gear[a:b]=="F":
                    saysgear='Beretta 92G'
                if sclient.gear[a:b]=="f":
                    saysgear='Glock 18'
                if sclient.gear[a:b]=="G":
                    saysgear='Desert Eagle'
                if sclient.gear[a:b]=="H":
                    saysgear='SPAS-12'
                if sclient.gear[a:b]=="I":
                    saysgear='MP5K'
                if sclient.gear[a:b]=="J":
                    saysgear='UMP45'
                if sclient.gear[a:b]=="K":
                    saysgear='HK69'
                if sclient.gear[a:b]=="L":
                    saysgear='LR300ML'
                if sclient.gear[a:b]=="M":
                    saysgear='G36'
                if sclient.gear[a:b]=="N":
                    saysgear='PSG-1'
                if sclient.gear[a:b]=="Z":
                    saysgear='SR-8'
                if sclient.gear[a:b]=="a":
                    saysgear='AK-103'
                if sclient.gear[a:b]=="c":
                    saysgear='Negev'
                if sclient.gear[a:b]=="e":
                    saysgear='M4A1'
                if sclient.gear[a:b]=="O":
                    saysgear='HE Grenade'
                if sclient.gear[a:b]=="P":
                    saysgear='Flash Grenade'
                if sclient.gear[a:b]=="Q":
                    saysgear='HE Smoke'
                if sclient.gear[a:b]=="R":
                    saysgear='Kevlar Vest'
                if sclient.gear[a:b]=="W":
                    saysgear='Kevlar Helmet'
                if sclient.gear[a:b]=="U":
                    saysgear='Silencer'
                if sclient.gear[a:b]=="V":
                    saysgear='Laser Sight'
                if sclient.gear[a:b]=="T":
                    saysgear='MedKit'
                if sclient.gear[a:b]=="S":
                    saysgear='TacGoggles'
                if sclient.gear[a:b]=="X":
                    saysgear='Extra Anno'
                if sclient.gear[a:b]=="g":
                    saysgear='Colt1911'
                if sclient.gear[a:b]=="h":
                    saysgear='Ingram Mac11'
                if sclient.gear[a:b]=="A":
                    saysgear=''
                if saysgear!='':
                    client.message('%s^3 weapon / gear : ^7-%s-' % (sclient.exactName, saysgear))            
                a=a+1
                b=b+1
                
        else:
            return False
    
    def cmd_listbwfy(self, data, client, cmd=None):
        """\
        <playername or all> - list prohibited of weapons and equipments of player 
                """

        if data:
            input = self._adminPlugin.parseUserCmd(data)
        
        else:
            client.message('!listbwfy <playername or all>')
            return
        
        if input[0]=="all":
            lclient="all"
        
        else:
            lclient = self._adminPlugin.findClientPrompt(input[0], client)                
        
        if not lclient:
            return False
               
        if (lclient):
            if lclient=="all":
                test=''

                for x in self._listplayersgear:
                    
                    egear=x.split(' ')
                    sguid = egear[0]
                    cursor = self.console.storage.query("""
                    SELECT *
                    FROM clients n
                    WHERE n.guid = '%s'       
                    """ % (sguid))
                    if cursor.rowcount != 0:
                        sr = cursor.getRow()
                        sdclient = sr['name']
                        cursor.close()
                    else:
                        cursor.close()
                    
                    client.message('^3Weapon /gear prohibited for ^2%s ^3: ^7-%s-'%(sdclient, egear[2]))
                    test="ok"

                if test=='':
                    client.message('^3No Players in Weapon /gear prohibited list')
            else:
                test=''
                fclient=lclient.guid

                for x in self._listplayersgear:
                    
                    if fclient in x:
                        egear=x.split(' ')
                        client.message('^3Weapon /gear prohibited for %s ^3: ^7-%s-'%(lclient.exactName, egear[2]))
                        test='ok'
                       
                if test=='': 
                    client.message('%s ^3is not in Weapon /gear prohibited list'%(lclient.exactName))                   
        else:
            return False
    
    def cmd_mylistbwfy(self, data, client, cmd=None):
        """\
        list of your weapons and equipments prohibited 
                """
        
        test=''
        fclient=client.guid

        for x in self._listplayersgear:
                    
            if fclient in x:
                egear=x.split(' ')
                client.message('^3Weapon /gear prohibited for %s ^3: ^7-%s-'%(client.exactName, egear[2]))
                test='ok'
                       
        if test=='': 
            client.message('%s ^3is not in Weapon /gear prohibited list'%(client.exactName))
    
    def cmd_whogear(self, data, client, cmd=None):
        """\
        <gear> - list of players who have the weapon or gear specify
                """
        
        if data:
            input = self._adminPlugin.parseUserCmd(data)
        
        else:
            client.message('!whogear <gear>')
            client.message('%s'%self.gmessage)
            return
        
        sgear = input[0]
        
        if not sgear in ('beretta', 'de', 'glock', 'colt', 'mac11', 'spas', 'mp5', 'ump', 'hk', 'lr300', 'g36', 'psg1', 'sr8', 'ak', 'negev', 'm4', 'he', 'flash', 'smoke', 'kevlar', 'helmet', 'silencer', 'laser', 'medkit', 'tac', 'xtra'):
     
            client.message('!whogear <gear>')
            client.message('%s'%self.gmessage)
            return False
               
        if (sgear):
        
            thread.start_new_thread(self.dowhogear, (client, sgear, cmd))
        
        else:
            return False

    def dowhogear(self, client, sgear, cmd):

        rlgear = lgear(sgear)
        rgear = rlgear[0]
        ngear = rlgear[1]  

        names = []
        
        for c in self.console.clients.getClientsByLevel():
        
            sclient = self._adminPlugin.findClientPrompt(c.name, client)
            
            if sclient.team==1:
                steam="^7Spectator"
            if sclient.team==2:
                steam="^1Red"
            if sclient.team==3:
                steam="^4Blue"

            if rgear in sclient.gear:
                client.message('%s ^7team : %s ^7has ^2%s'%(sclient.exactName, steam, ngear))

        return true
