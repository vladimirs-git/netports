"""unittest helpers"""

# ============================ CISCO IOS =============================
# show run | include interface
SHOW_RUN__IOS = """
interface FastEthernet0
interface GigabitEthernet1/0/1
interface Port-channel1
interface TenGigabitEthernet1/1/1
interface Tunnel1
interface Vlan1
"""

# show lldp neighbors
SHOW_LLDP_NEIGHBORS__IOS = """
Device ID           Local Intf     Hold-time  Capability      Port ID
cnx                 Gi2/0/47       120        B,R             Ethernet1/16
hpc                 Gi1/0/2        120        B               47
"""

# show interfaces summary
SHOW_INTERFACES_SUMMARY__IOS = """
  Interface                   IHQ       IQD       OHQ       OQD      RXBS      RXPS      TXBS    
-------------------------------------------------------------------------------------------------
  Vlan1                         0         0         0         0         0         0         0    
  FastEthernet0                 0         0         0         0         0         0         0    
  GigabitEthernet1/1/1          0         0         0         0         0         0         0    
  Te1/1/1                       0         0         0         0         0         0         0    
  Port-channel1                 0         0         0         0         0         0         0    
"""


# ============================ CISCO NXOS ============================
# show run | include interface
SHOW_RUN__NXOS = """
interface Ethernet1/1
interface Ethernet1/1.100
interface Tunnel1
interface Vlan1
interface loopback0
interface mgmt0
interface port-channel1
interface port-channel1.100
"""
# show interface brief
SHOW_INTERFACE_BRIEF_NXOS = """
mgmt0  --            up     10.0.0.1                              1000     1500    
Eth1/1       307     eth  trunk  down    Link not connected       auto(D)  --
Po100        1       eth  trunk  up      none                     a-40G(D) lacp
Vlan1  --            down   Administratively down  
"""

# show lldp neighbors
SHOW_LLDP_NEIGHBORS__NXOS = """
Device ID            Local Intf      Hold-time  Capability  Port ID
cnx                  Eth1/41         120        BR          Ethernet1/1
cnx                  Eth1/42         120        B           Eth1/1
cnx                  mgmt0           120        BR          Eth1/1 
enc                  Eth1/3          120        S           eth0
fpr                  Eth1/52         120        R           Eth1/1
h3c                  Eth1/2          121        BR          GigabitEthernet1/0/1
hpc                  mgmt0           120        B           16
ios                  Eth1/36         120        B           Te1/0/1
ios                  Eth1/39         120        BR          Te1/1.100
ios                  Eth1/41         120        R           Gi0/0/1 
ixr                  Eth2/44         120        R           TenGigE0/0/0/1
ixr                  Eth8/1          120        R           HundredGigE0/0/0/1
pan                  Eth1/37         120        OR          ethernet1/1
"""


# ========================== CISCO ASR 9000 ==========================

# show run | include interface
SHOW_RUN__ASR = """
interface Bundle-Ether1
interface Bundle-Ether1.100
interface Loopback1
interface tunnel-ip1
interface MgmtEth0/RSP0/CPU0/0
interface GigabitEthernet0/0/0/1
interface TenGigE0/0/0/1
interface TenGigE0/0/0/1.100
interface HundredGigE0/0/0/1
"""

# show lldp neighbors
SHOW_LLDP_NEIGHBORS__ASR = """
Device ID       Local Intf                      Hold-time  Capability      Port ID
ixr             TenGigE0/0/0/1                  120        R               TenGigE0/0/0/1
cnx             HundredGigE0/0/0/1              120        B,R             Ethernet1/1
"""

# show interfaces brief
SHOW_INTERFACES_BRIEF__ASR = """
               Intf       Intf        LineP              Encap  MTU        BW
               Name       State       State               Type (byte)    (Kbps)
--------------------------------------------------------------------------------
                BE1          up          up               ARPA  1514   40000000
            BE1.100          up          up             802.1Q  1518   40000000
                Lo1          up          up           Loopback  1500          0
                Nu0          up          up               Null  1500          0
                ti1          up          up          TUNNEL_IP  1500        100
    Mg0/RSP0/CPU0/0          up          up               ARPA  1514    1000000
          Gi0/0/0/1          up          up               ARPA  1514    1000000
          Hu0/0/0/1          up          up               ARPA  1514  100000000
          Te0/0/0/1          up          up               ARPA  1514   10000000
      Te0/0/0/1.100          up          up             802.1Q  1518   10000000
"""


# ============================ HP COMWARE ============================

# display current-configuration | include interface
SHOW_RUN__H3C = """
interface Bridge-Aggregation1
interface NULL0
interface Vlan-interface1
interface GigabitEthernet1/0/1
interface Ten-GigabitEthernet1/0/1
"""

# display interface brief
DISPLAY_INTERFACE_BRIEF__H3C = """
Interface            Link Protocol Primary IP      Description                
InLoop0              UP   UP(s)    --              
NULL0                UP   UP(s)    --              
Vlan1                UP   UP       10.0.0.1        Switch MGMT

Interface            Link Speed   Duplex Type PVID Description                
BAGG1                UP   2G(a)   F(a)   T    1    description
GE1/0/1              UP   1G(a)   F(a)   T    1    description
XGE1/0/1             ADM  auto    A      A    1    description
"""
