# Host Discovery
Durante la fase di host discovery non si è interessati alla scoperta dei servizi esposti ma esclusivamente agli host attivi all'interno dell'organizzazione.

#### Comandi generici
Il comando di base per effettuare host discovery è il seguente
```bash
nmap -sn CIDR/IP 
```
**Ricorda** l'opzione sn svolge un ruolo fondamentale poiché informa nmap di non effettuare il probing delle porte.
Con tale configurazione nmap effettuerà un ARP scan all'interno della propria subnet e un ping scan per tutti i possibili host non appartenenti alla propria subnet.

Gli IP da scansionare possono essere specificati in varie forme. Sicuramente una delle migliori è quella di utilizzare una lista contente gli IP da scansionare
```bash
nmap -sn -iL list.txt
```

Nel caso si dovesse escludere un host dalle scansioni ricorda che puoi utilizzare il flag `--exclude` o `--exludefile`

Per specificare gli indirizzi IPv6 ricorda di utilizzare l'opzione `-6`

#### Reverse LookUp -sL
La reverse lookup può essere utilizzata come una prima tecnica per individuare host attivi.  Infatti, se l'amministratore dell'organizzazzione ha assegnato un nome dominio ad un determinato indirizzo IP è presumibile che quest'ultimo venga utilizzato. 
```bash
nmap -sL -PN CIDR
```

**Ricorda** il flag `-PN` è utilizzato per disabilitare il ping scan. Tale scansione verrà eseguita in seguito.

Potrebbe essere utile da utilizzare come opzione `--dns-server` nel caso volessimo utilizzare un server DNS specifico e non quello impostato sulla macchina (utile quando ci troviamo all'interno della rete aziendale e vogliamo effettuare la reverse lookup sugli indirizzi ip privati).

####  TCP SYN Ping -PS < porte >
Per individuare un host attivo possiamo inviare un datagramma TCP contentente una porta qualsiasi. Nel caso l'host sia attivo ci dovrebbe fornire un ACK se la porta è utilizzata oppure un RST nel caso la porta non sia utilizzata

Risposta | Descrizione
------------ | ------------
SYN | Host attivo e la porta è utilizzata 
RESET | Host attivo e la porta non è utilizzata
Indeterminato | Host non attivo oppure il Firewall ci blocca

```bash
nmap -PS -PN CIDR
```

**Ricorda** il firewall può alterare l'esito di questa scansione dato che potrebbe non far raggiungere il datagramma alla destinazione. Io consiglio di scagliere sei porte come riportata nella tabella.

Porte | Descrizione
------------ | ------------
1-1023 | Porte Well-Know. (scegli porte di uso comune, per es. 80)
1024–49151 | Registed port. (2 a caso)
49152–65535 | Dynamic port. Porte utilizzate dal client per aprire connessioni con il server. (2 a caso)

Questo perchè in presenza di un firewall vuoi forzare la risposta di un ACK da parte dell'host oppure sperare che quelle porte non siano bloccate dal firewall.

#### TCP Ack Ping -PA < porte >
In presenza di un firewall non statefull potrebbe essere utile effettuare un TCP ACK scan piuttosto che un TCP SYN scan. Ciò perché il firewall non blocchera i nostri ACK poiché non verifica o meno se abbiamo già aperto una sessione. Per quanto riguarda le porte si consiglia di utilizzare la configurazione spiegata sopra.

#### UDP Ping -PU < porte >
Si può effettuare l'attività di host discovery inviando un datagramma UDP ad un host specifico (il datagramma avrà payload nullo a meno che non si utilizzi il flag `--data-lenght`). Con questo tipo di scan si cerca di forzare la risposta da parte della macchina vittima di un messaggio ICMP port unreachable. La ricezione di altri tipi di pacchetti ICMP può indicare che ci si trovi in presenza di un host down o unreachable. Nel caso invece il datagramma incontra una porta aperta probabilmente l'host deciderà di ignorare il messaggio e non fornire alcun tipo di risposta. Per questo motivo si consiglia di **utilizzare due porte che difficilmente vengono utilizzare dalla macchina vittima** (ad es. 31338) **e due porte che presumibilmente possano essere utilizzate dalla macchina vittima** (53, 161)
Questo ci consente di ridurre la probabilità che i nostri messaggi vengano bloccati dal Firewall. 

#### ICMP Ping Scan (-PE, -PP, -PM)
Nel caso l'invio di messaggi di ICMP di tipo 0 (echo reply) sia bloccato potrebbe essere utile provare a forzare la risposta dell'host remoto con altri tipi di messaggi ICMP

Scan | Tipo di scansione
------------ | ------------
-PE o -sP | Ping Scan
-PP | Timestamp Request
-PM | Netmask Request

####  IP Protocol Ping (-PO < protocol list >)
Vengono inviati pacchetti IP con il campo IP protocol specificato all'interno dell'header IP. Nel caso non vanga specificato alcun protocol number di default verranno inviati pacchetti multipli aventi IP protocol ICMP (number 1), IGMP (protocol 2) e IP-in-IP (protocol 4). I pacchetti non avranno payload a meno che non venga specificato con il flag `--data-lenght`. Con questo metodo di scan si cerca di forzare un host a rispondere con lo stesso protocollo inviato oppure con un messaggio ICMP protocol unreachable (ovvero che il protocollo non è supportato dall'host). 


#### ARP Scan (-PR) 
Molto affidabile, purtroppo può essere utilizzato esclusivamente se ci si trova nella stessa network da scansionare.

#### Flag Utili
`-PN` non effettua il probing per verificare se l'host è attivo o meno attraverso un ping scan. In questa fase è utile inserirlo poiché siamo noi che specifichiamo che tipo di scansione fare e non risulta necessario verificare che l'host risulti essere attivo.

`-n` non effettua il reverse lookup dell'indirizzo specificato. Spesso è utile inserirlo poiché questa operazione è stata effettuata preliminarmente.

`-v` permette di ottenere informazioni aggiuntive per quanto riguarda la scansione. Potrebbe essere utile anche per rilevare la presenza di Firewall che droppano i pacchetti che inviamo.

# Port Scanning	
Durante la fase di Port Scanning si è interessati ad individuare tutte le porte in ascolto su una determinata macchina. 

### Tipi di porte
-	**open** Una applicazione sulla suddetta porta è attiva e accetta datagrammi TCP o UDP.
-	**closed** Sulla porta non vi è nessuna applicazione in ascolto.
-	**filtered** Non si riesce a determinare se la porta è chiusa o meno poiché politiche di filtraggio dei pacchetti prevengono la raggiungibilità della porta.
-	**unfiltered** La porta è raggiungibile ma Nmap non è in grado di comprendere se c'è una applicazione in ascolto o meno.
-	**open | filtered** Nmap non è in grado di determinare se la porta è in ascolto o meno. Capita quando lo stato di porta aperta è determinato da una assenza di risposta.
-	**closed | filtered** Nmap non è in grado di determinare se la porta è filtrata oppure non vi è nessuna applicazione in ascolto. 

#### TCP SYN Stealth (-sS) 
Scan estremamente veloce ed estramente adatto in constesti in cui le attività di scanning non sono ostacolate. Questo perché prova ad aprire una connessione TCP attraverso l'invio di un SYN. Nel caso di ricezione di un ACK Nmap invia un RST al fine di evitare il completamento dell'handshake.

Risposta | Porta
------------ | ------------
TCP SYN/ACK response | open
TCP RST | closed
No Response | filtered
ICMP unreachable error | filtered

La problematica di questo tipo di scansione è quando siamo in presenza di un firewall che droppa le nostre richieste SYN su determinate porte. Questo tipo di approccio rallenta estremamente le scansioni effettuate a casua degli elevati timeout che il comportamento del firewall causa. 

#### TCP Connect (-sT)
Funziona allo stesso tipo del SYN Scan ma al posto di terminare subito la connessione completa l'handshake inviando un messaggio di ACK. Se si può utilizzare il SYN Scan quest'ultimo deve essere preferito dato che impiega la metà del tempo. 

Risposta | Porta
------------ | ------------
TCP SYN/ACK response | open
TCP RST | closed
No Response | filtered
ICMP unreachable error | filtered

#### UDP Scan 
Lo UDP Scan è generalmente più lento rispetto a quello su TCP. 
**Ricorda** non sottovalutare comunque questa fase poiché molte vulnerabilità potrebbero essere presenti su servizi che utilizzano a livello trasporto UDP e nel caso non venisse eseguita quest'ultime non sarebbero trovate.
 
Risposta | Porta
------------ | ------------
Qualsiasi datagramma UDP provenitente dall'host *(inusuale)* | open
Nessuna risposta anche in presenza di ritrasmissioni | open | filtered
ICMP port unreachable | closed
Altri messaggi di tipo ICMP | filtered

La principale sfida nell'individuazione delle porte UDP è che generalmente le applicazioni non forniscono alcun tipo di risposta se stimolate dato che probabilmente quest'ultime scarteranno il datagramma essendo vuoto. Si potrebbe pensare che questo sia un problema risolvibile poiché le porte negli altri stati rispondono ma purtroppo in genere i firewall droppano i suddetti pacchetti di risposta. Inoltre, molti host limitano il rate di invio di pacchetti ICMP.

**NOTA IMPORTANTE** Per distinguere una porta *open* da una *open | filter* si potrebbe pensare di utilizzare il flag `-sV`. Questo perché l'applicazione potrebbe scartare datagrammi che considera invalidi e non fornire risposta. Con il flag `-sV` Nmap utilizza datagrammi ben formati.

**FLAG UTILI** 
`-version-intesity 0` Tale opzione informa Nmap di provare esclusivamente i servizi più probabili verso una determinata porta. 

#### TCP FIN, XMAS e NULL Scan (-sF, -sX, -sN)

#### TCP Window (-sW)

#### TCP Maimon (-sM)

#### TCP Idle (-sI < zombie host >)

#### IP portcol (-sO)

#### TCP FTP bounce (-b < FTP bounce proxy >)

#### Flag utili
`-PN` In questo genere di attività in genere non si è interessati a verificare che l'host sia attivo poiché questa procedura è già stata eseguita nella fase di Host Discovery

`-n` Generalemente durante la fase di Host Discovery si è già effettuato il reverse lookup dei nomi dominio e quindi risulterebbe un inutile spreco di tempo (questa opzione è compresa nel `-PN`)

`-6` Si richiede ad Nmap l'utilizzo del protocollo IPv6

