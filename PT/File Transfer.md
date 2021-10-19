# File transfert 
## nc
Macchina su cui trasferire il file
```bash
nc -nlvp <PORT> > <FILE>
```
Macchina da cui prelevare il file
```bash
nc -nlvp <IP> <PORT> < <FILE>
```

## Socat 
Macchina su cui trasferire il file 
```bash
socat TCP4-LISTEN:<PORT>,fork file:<FILE>,create
```
Macchina da cui prelevare il file
```bash
socat TCP4:<IP>:<PORT> < <FILE>
```
 