# projekt-inzynierski

Notebooki z poszczególnymi algorytmami znajdują się folderze `notebooks`. 
W celu poprawnego uruchomienia kodu naley mieć zainstalowany interpreter języka `Python 3.8.0`.
Następnie należy zainstalować wszystkie wymagane biblioteki z pliku `requirements.txt` używając następującej komendy:

```
pip install -r requirements.txt
```

Następnie należy zainstalować kilka dodatków z biblioteki `nltk`. W celu można uruchomić interaktywny intrpreter języka Python oraz wykonać następujący kod:

```
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('punkt')
```

W celu wizualizacji architektury sieci neuronowych należy zainstalować program `graphviz` https://graphviz.org/download/.

Niektóre notebooki wymagają pobrania wcześniej wytrenowanych modeli. Można je pobrać ze strony http://vectors.nlpl.eu/repository/ . Pierwszy z modeli jest wytrenowany na korpusie `English CoNLL17 corpus` z rozmiarem wektrów `100` oraz numerem ID `40`. Drugi został wytrenowane na korpusie `Polish CoNLL17` z rozmiarem wektorów `100` oraz numerem ID `62`. Oba pobrane archiwa `.zip` należy rozpakować w folderze `pretrained_models` katalogu roboczego
