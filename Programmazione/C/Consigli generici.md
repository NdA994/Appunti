## Uso di `memcpy`
Per motivi di efficienza, è possibile utilizzare `memcpy` (preferibile a `strcpy` [source](https://stackoverflow.com/questions/610238/c-strcpy-evil)), sebbene si tratti di una funzione intrinsecamente insicura, ad esempio quando impiegata per copiare una stringa in un’altra. Tale approccio può essere adottato **esclusivamente** quando la dimensione della stringa è nota a tempo di compilazione. È inoltre consigliabile che il buffer di destinazione sia preventivamente allocato e che l’operazione sia accompagnata da una `static_assert`, al fine di ridurre il rischio di *buffer overflow*. **In aggiunta, è opportuno includere una _security note_ che motivi nel dettaglio questa scelta e ne espliciti le assunzioni di sicurezza.**

```C
/* ------------------------------------------------------------------
SECURITY NOTE: capture_name MUST be at least 8 bytes long
------------------------------------------------------------------- */

char capture_name[30] = "capture";

static_assert(sizeof(capture_name) >= sizeof("capture"), "capture_name buffer too small for default value");

...

memcpy(capture_name, "capture", sizeof("capture"));
```