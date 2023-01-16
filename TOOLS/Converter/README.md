## Cosa può fare?

Legge file .bin o .nfc, ID amiibo direttamente o come elenco da un file .txt e lo restituisce come file .bin o .nfc.

Esegue la scansione ricorsiva delle cartelle, in cui emette i nuovi file nella stessa directory o un nuovo con la stessa struttura di cartelle.

Opzione per randomizzare l'UID e creare più output dello stesso file sorgente (per giochi come BOTW).

## Come farlo?

Eseguire lo script dal terminale, passando i seguenti argomenti:
`-m` richiesto: modalità da eseguire, bin2bin, bin2nfc, id2bin, id2nfc, nfc2bin o nfc2nfc. più file o stringhe possono essere analizzati contemporaneamente, separati da spazio.
`-i` richiesto: percorso, file o stringa da analizzare come input.
`-o` facoltativo: percorso o file in cui scrivere l'output.
`-r` opzionale: randomizza l'UID dell'output.
`-d` opzionale: numero di copie da scrivere (`-r` è impostato automaticamente durante l'esecuzione).
`-v` opzionale: visualizza più informazioni durante l'esecuzione, `-vv` per ulteriori informazioni.
`-h` visualizza il testo della guida.

**esempi:**
`python converter.py -m bin2nfc -i bin -o nfc` convertirà tutti i file .bin trovati nella cartella ./bin, li convertirà in .nfc e li memorizzerà in una cartella chiamata ./nfc
`python converter.py -m id2bin -i id.txt -d 3` prenderà tutti gli ID amiibo trovati in id.txt e creerà 3 nuovi file .bin (con UID casuale) per ogni ID trovato.

Quando inserisci l'ID amiibo, il nome del file può essere impostato aggiungendo il nome e un punto e virgola prima dell'ID. Come `Luigi:0x00010000...` o `Daisy:00130000037a..`, lo stesso vale per i file .txt, dove si applica anche un ID per riga. Se non viene aggiunto alcun nome, l'ID verrà utilizzato come nome file.

## Cosa richiede?

Python 3.8 o successivo

Hai bisogno delle librerie in `requirements.txt`, installale usando qualcosa come `pip install -r requirements.txt`

Per qualsiasi cosa tranne la pura conversione bin-to-nfc / nfc-to-bin, sono necessarie le chiavi di decrittazione corrette nella stessa cartella dello script, questi sono file comunemente chiamati `unfixed-info.bin` e `locked-secret.bin `. È anche possibile utilizzare una versione unita di questi file chiamata `key_retail.bin`. Questi file non sono forniti.

## Un piccolo avvertimento alla fine!

Conserva un backup dei tuoi file di origine, siano essi .bin o .nfc. Questo strumento può sovrascrivere i tuoi file. I file generati con un UID casuale funzionano al momento, ma potrebbero non funzionare in futuro.