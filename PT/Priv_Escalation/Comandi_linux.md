# Comandi utili Linux

Trovare file con bit suid
```bash
find / -perm -u=s -type f 2>/dev/null
```

Verificare quali comandi possono essere eseguiti come un'altro utente
```bash
sudo -l
```