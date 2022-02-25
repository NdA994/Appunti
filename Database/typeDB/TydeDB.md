# typeDB
## Concetti 
- **Schema** Lo schema è costituito da tipi e regole. In particolare, con tipi facciamo riferimento alle entità, relazioni e attributi.
- **Entity** sono oggetti distinguibili all'interno del tuo dominio.
- **Relation** stabiliscono le connessioni tra i diversi oggetti del dominio. Il contesto all'interno di una relazione viene assegnato attraverso i ruoli. 
   *RICORDA* che in typedb le relazioni non connettono solo entità ma possono collegare anche attributi e relazioni.
- **Attribute** sono globalmente univoci per tipo e valore e sono anche immutabile. Questo significa che ci può essere al massimo un attributo e che non può essere sostituito in-place. Questa caratteristica rende l'update di un determinato valore molto complesso dato che si deve riassegnare la proprietà.
- **Inheritance** un sottotipo erediterà le proprietà (come i ruoli svolti e gli attributi posseduti) dai loro tipi principali.
- **Rule** Permettono di inserire la logica deduttiva all'interno dello schema.

###