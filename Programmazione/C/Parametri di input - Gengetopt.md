
## Come funziona Gengetopt

Si crea un file di configurazione .ggo in cui si dichiarano:
- il nome delle opzioni
- il tipo (stringa, intero, flag, ecc.)
- se sono obbligatorie o opzionali
- eventuali valori di default
- una breve descrizione

Esempio:

```
version "0.1"
package "Terminal-Collector"
purpose "Capture terminal I/O through a PTY and store it for analysis."

# Options
option  "capture"           c
        "Identifier for the capture session"
        string
        default = "capture"
        optional

option  "verbose"           v
        "Increase program verbosity"
        flag
        off

option  "network"           n
        "Enable network capture"
        flag
        off
        
option  "count"             c 
        "Numero di iterazioni" 
        int 
        default="10"
```

Da questo file Gengetopt genera automaticamente due file (cmdline.c e cmdline.h) che implementano un parser completo.

## Per generare il parser:

```bash
gengetopt --input=collector.ggo --output-dir=lib
```
`gengetopt <opzioni> <file.ggo>`

Il comando produce due file:

- `cmdline.c`
- `cmdline.h`    

che contengono il codice completo per il parsing degli argomenti.


## Utilizzo nel programma C

```C
struct gengetopt_args_info tool_input;

if (cmdline_parser(argc, argv, &tool_input) != 0) {
	perror("[ERROR] Failed to parse input");
	exit(1);
}

setVerbose(tool_input.verbose_flag);
verbose("Verbose flag activated");
verbose("Network flag: %d\n", tool_input.network_flag);
verbose("Output string: %s\n", tool_input.output_arg);
```

Gengetopt gestisce automaticamente:

- `--help`
- `--version    
- errori di sintassi
- messaggi di usage
- validazione dei parametri richiesti

### Link
https://bikulov.org/blog/2013/10/26/command-line-arguments-in-c-and-c-with-gengetopt/
https://stackoverflow.com/questions/9642732/parsing-command-line-arguments-in-c
https://www.gnu.org/software/gengetopt/gengetopt.html