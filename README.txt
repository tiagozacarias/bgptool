# BGPTool V1.9

- A ferramenta bgptool foi desenvolvida nas linguagens python3, dialog e modulo de automação netmiko com o objetivo de facilitar o dia a dia da operação de rede onde é possivel realizar comutação de tráfego de rede de forma massiva para links secundarios e primarios manipulando o protocolo de roteamento BGP com a criação de filtros de prefixos por vizinhança.

# Frontend da Ferramenta:

- Frontend conta com o dialog que possue a caracteristica de fornecer opções de forma amigáveis para o usuario.

## Exemplo do Frontend:

--

# Estrutura de comandos enviados na automação para refletores:

## ESTRUTURA ESTATICA DE ROUTE-MAP QUE DEVERÁ SER CRIADA NOS REFLETORES DE PREFIXOS

route-map DENY-ALL deny 10
 description AUTOMACAO - BGPTOOL

## COMUTA PARA LINK SECUNDARIO ##

router bgp 65000 
 address-family vpnv4
  neighbor 10.2.1.3 route-map DENY-ALL in
  neighbor 10.2.1.3 route-map DENY-ALL out
  neighbor 10.2.1.15 route-map DENY-ALL in
  neighbor 10.2.1.15 route-map DENY-ALL out

## RETORNANDO PARA LINK PRIMARIO ##

router bgp 65000
 address-family vpnv4
  no neighbor 10.2.1.3 route-map DENY-ALL in
  no neighbor 10.2.1.3 route-map DENY-ALL out
  no neighbor 10.2.1.15 route-map DENY-ALL in
  no neighbor 10.2.1.15 route-map DENY-ALL out


- Com a filtragem dos prefixos na sessão especifica conforme demostrado acima é possivel manipular e instruir a rede a preferir o caminho desejado.


# Modulo de automação netmiko:

- O Modulo de automaçao hoje conta com a linguagem python3 e netmiko que realiza todo o trabalho sendo o componente de execução para o frontend.

# Modulo de mod_peers:

- O Modulo de peers foi desenvolvido para agrupar os endereçamentos de vizinhança do BGP e relaciona-los com o seu dominio de rede e refletores.

# Requerimentos

- python3.9
- pythondialog==3.5.3
- dialog
- netmiko==4.4.0
- paramiko==3.4.0

# TODO

- Identificar o estado das sessões BGP nos refletores antes da automação.


# Configuração do terminal MobaXterm para automatizar a abertura da ferramenta.

- Na sessão SSH incluir a seguinte linha em Advanced SSH Settings/Execute command:

	cd /bgptool && source .bashrc && python3 bgptool.py

