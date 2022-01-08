# Execute after read
Si presenta quando all'utente viene fornita una risposta di tipo 302 (per esempio perché non si ha acesso ad una particolare risorsa) ma il webserver continua l'esecuzione dello script server side. In queste condizioni l'output dello script server side viene mostrato all'interno del body della risposta. 

Un primo sintomo della presenza di questa vulnerabilità è la presenza di un payload non vuoto in presenza di una risposta HTTP di tipo 302. 
Invece per verificare la presenza di questa vulnerabilità ci basta effettuare utilizzare un tool che non segue la redirect fornita dal webserver. Ad es.

```bash
curl http://webserver
```

### PHP Improper redirect
Questo comportamento si ha in PHP quando non si inserisce un `die();` subito dopo del redirect all'interno del codice.