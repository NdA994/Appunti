Si verifica quando un utente riesce a ottenere informazioni contenute all'interno di un database, accessibile tramite una web application, la quale è responsabile dell'esecuzione delle query per visualizzare il contenuto.

Un primo sintomo della presenza di questa vulnerabilità è il comportamento insolito della web application quando viene inserito il simbolo ' all'interno di uno dei possibili input forniti dall'utente.

### Superfice di attacco
La superficie di attacco per la seguente vulnerabilità risulta essere:
- Query presente all'interno dell'URL in una richiesta GET (o in una POST).
- Parametri forniti nel body della richiesta dell'utente in una richiesta post.

#### Ottenere dati dal Database
Per ottenere dati dal database e sfruttare una vulnerabilità di SQL Injection, è necessario effettuare una richiesta che permetti di eludere la logica con cui è implementata la web application. Ad esempio, consideriamo una richiesta GET come la seguente:

```
`https://insecure-website.com/products?<input_tag>=<input>`
```
Questa viene tradotta nella seguente query SQL:

```
`SELECT * FROM products WHERE <input_tag> = '<input>' AND released = 1`
```
Se un utente malintenzionato fornisce il seguente input `'+OR+1=1--` la query risultante diventa: 
```
`SELECT * FROM products WHERE <input_tag> = '<input>' OR 1=1--' AND released = 1`
```
permettendoci di ottenere tutte le informazioni contenute all'interno della tabella products utilizzata come esempio.

