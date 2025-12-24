
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
- `--version`  
- errori di sintassi
- messaggi di usage
- validazione dei parametri richiesti

### Link
https://bikulov.org/blog/2013/10/26/command-line-arguments-in-c-and-c-with-gengetopt/
https://stackoverflow.com/questions/9642732/parsing-command-line-arguments-in-c
https://www.gnu.org/software/gengetopt/gengetopt.html

## Implementazione verbose
È buona pratica prevedere un _verbose flag_ per fornire all’utente informazioni di debug aggiuntive, utili durante lo sviluppo e l’analisi di eventuali malfunzionamenti, senza impattare il comportamento normale dell’applicazione.  Il meccanismo può essere implementato tramite una semplice variabile globale controllata da funzioni di abilitazione e stampa condizionale.

**File header (`.h`)**

```C
/**
* @brief Enable or disable verbose output.
*
* @param enabled true to enable verbose logging, false to disable it.
*/

void setVerbose(int enabled);

/**
* @brief Print a message only when verbose mode is enabled.
*
* @param msg Null-terminated message to print.
* @return The number of bytes printed when verbose mode is enabled,
* or 0 when verbose mode is disabled.
*/

int verbose(const char * restrict format, ...);
```

**File sorgente (`.c`)**

```C
int verbose_flag = 0;

void setVerbose(int enabled) {
	verbose_flag = enabled;
}

int verbose (const char * restrict format, ...) {
	if (!verbose_flag) {
		return 0;
	}

	va_list args;
	va_start(args, format);
	int ret = vprintf(format, args);
	va_end(args);
	
	return ret;
}
```

### Link
https://stackoverflow.com/questions/36095915/implementing-verbose-in-c