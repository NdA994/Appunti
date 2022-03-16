# Comandi utili
## checksec
```bash
apt install -y checksec
checksec --file==<locazione file>
```

## gdb
Lanciare gdb
```bash
gdb -q file-esseguibile
```

Inserire un breakpoint 
```gdb
break main
```

lanciare il programma che si sta debbugando (l'esecuzione procede fino il primo breakpoit)
```gdb
run
```

esegue la prossima istruzione macchina (next instruction)
```gdb
ni
```

esegue tutte le istruzioni prima di arrivare alla prima istruzione macchina
```gdb
stepi
```

dissassembla la funzione specificata
```gdb
dissas main
```

mosta il contenuto di tutti i registri del processore
```gdb
info registers
```

mosta il contenuto del registro specificato
```gdb
info register <registro>
```

analizzare il contenuto di memoria
```gdb
info register <registro>
```

mostrare il contenuto della memoria
```gdb
x/<numero di locazioni><format><size unit> <mem address>
```
I possibili formtati che possono essere utilizzati con il comando examinate sono:
-	**o** mostra il contenuto in base 8
-	**x** mostra il contenuto il esadecimale
-	**u** mostra il contenuto in base 10 unsigned
-	**t** mostra il contenuto in binario

I possibili size unit che possono essere utilizzati con il comando examinate sono_
-  **b** single byte
-  **h** halfword (2 byte)
-  **w** word (4 byte)
-  **g** giant o double word (8 byte)

Il comando examinate permette di accettare come parametro di ingresso i (instruction) per visualizzare la memoria come linguaggio dissasemblato.
```gdb
x/i $eip
```

mostrare il backtrace dello stack
```gdb
bt
```

stampare il valore o l'indirizzo di una variabile o il contenuro di una variabile deferenziata
```gdb
print var
print &var
print *var
```

stampare tutte le variabili presenti all'interno dei vari frame delle funzioni 
```gdb
bt full
```

## gcc
Oltre a compilare il sorgente inserisce dei metadati che possono essere informazioni utili durante la fase di debugging. Questo permette anche l'accesso al codice sorgente dell'eseguibile.
```bash
gdb -q file-sorgente
```

Specificare il file di output 
```bash
gdb -o file-esseguibile file-sorgente
```