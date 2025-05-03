# BGPTool V1.9

  - The bgptool tool was developed in the languages python3, dialog and netmiko automation module with the objective of facilitating the day-to-day network operation where it is possible to perform massive network traffic switching for secondary and primary links by manipulating the BGP routing protocol with the creation of prefix filters by neighborhood.

* Tool Frontend:

  - Frontend has the dialog that has the characteristic of providing user-friendly options.

Frontend Example:

--

 * Structure of commands sent in automation for reflectors:

        - STATIC ROUTE-MAP STRUCTURE THAT SHOULD BE CREATED IN THE PREFIX REFLECTORS

            route-map DENY-ALL deny 10
            description AUTOMACAO - BGPTOOL

        - COMUTA FOR SECONDARY LINK

          router bgp 65000
            address-family vpnv4
            neighbor 10.2.1.3 route-map DENY-ALL in
            neighbor 10.2.1.3 route-map DENY-ALL out
            neighbor 10.2.1.15 route-map DENY-ALL in
            neighbor 10.2.1.15 route-map DENY-ALL out

        - RETURNING TO PRIMARY LINK

            router bgp 65000
            address-family vpnv4
            no neighbor 10.2.1.3 route-map DENY-ALL in
            no neighbor 10.2.1.3 route-map DENY-ALL out
            no neighbor 10.2.1.15 route-map DENY-ALL in
            no neighbor 10.2.1.15 route-map DENY-ALL out


* By filtering the prefixes in the specific session as shown above, it is possible to manipulate and instruct the network to prefer the desired path.

* Netmiko Automation Module:

  - The Automation Module today has the python3 and netmiko language that does all the work being the execution component for the frontend.

* mod_peers module:

  - The Peer Module is designed to group BGP neighborhood addresses and relate them to your network domain and reflectors.

Requirements:

    - python3.9
    - pythondialog==3.5.3
    - dialog
    - netmiko==4.4.0
    - paramiko==3.4.0

TODO:

  - Identify the state of BGP sessions on reflectors before automation.


* Configuration of the MobaXterm terminal to automate tool opening.

* In the SSH session include the following line in Advanced SSH Settings/Execute command:

        cd /bgptool && source .bashrc && python3 bgptool.py

