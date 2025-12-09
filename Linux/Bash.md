# Bash 
Cose utili che scordo sempre

Varibile | Descrizione
------------ | ------------
$0 | Nome del BASH script
$1-9 | Primi nove argomenti passato allo script
$# | Numero di argomenti passati allo script
$@ | Tutti gli argomenti passati allo script
$? | Exit status dell'ultimo running process
\$$ | Process ID
$USER | Username di chi sta eseguendo lo script
$HOSTNAME | Hostname di chi ha lanciato lo script
$RANDOM | Random numeber
$LINENO | Current line all'interno dello script

## Blocchi strutturati
### Blocchi di selezione 
#### If than else block
```bash
if [ <some test> ]
then 
	<perform action>
elif [ <some test> ]
then 
	<perform action>
else
	<perform action>
fi
```
**RICORDA** che [ ] fanno riferimento al comando test ( *v. man [* )

### Cicli

#### For Loop
```bash
for var-name in <list> 
do 
	<perform action>
done
```

#### While Loops
```bash
while [ <some-test> ] 
do 
	<perform action>
done
```


## Prompt String
Varibile | Descrizione
------------ | ------------
PS0 | Il valore di questo parametro viene mostrato da una scell INTERATTIVA dopo la lettura di un comando e prima che quest'ultimo sia eseguito.
PS1 | Il valore di questo parametro viene mostrato allputente come primary prompt script. (ad se. nda@ubuntu:~$)
PS2 | Il valore di questo parametro viene mostrato quando si prova a lanciare un multiple-line command. 
PS3 | Il valore di questo valore è mostrato quando si è in attesa di un input utente
PS4 | è il prefisso della debugging trace line per gli script bash. (Uno script si lancia in modalità `bash -x <script.sh>`)