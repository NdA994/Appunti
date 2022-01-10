# Comandi utili Linux

Trovare file con bit suid
```bash
find / -perm -u=s -type f 2>/dev/null
```

---------------------------------------

Verificare quali comandi possono essere eseguiti come un'altro utente
```bash
sudo -l
```
**Ricorda** dall'output di questo comando devi osservare due cose 
- presenza di comandi che possono essere lanciati come root e che non richiedono la passord (*no passwd*)
- presenza della variabile secure_path. Viene utilizzata come PATH in presenza di comandi lanciati con  `sudo`

---------------------------------------

