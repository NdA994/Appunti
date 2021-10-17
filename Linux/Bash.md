# Bash 
Cose utili che scordo sempre
## Cicli di iterazione
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
