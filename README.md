# ADTool

Petit développement d'un scraper web ayant pour but d'automatiser la documentation en allant chercher directement sur les sites des conférences les résultats de recherches par mots-clés (prenez un café en attendant :) )

Actuellement, l'outil permet de faire des recherches sur NDSS, Usenix, IEEE ACM et IEEE SP.

## Prérequis

Le code étant en python, les bibliothèques json, urllib, selenium et time sont nécessaires au fonctionnement de l'outil.

## Utilisation

Afin de paramétrer les recherches, il faudra éditer le fichier "conf.json". Dans ce json, on pourra voir plusieurs champs à modifier si souhaité:

* **site_to_search** : correspond aux sites sur lesquels vous souhaitez faire votre recherche. Pour l'instant, l'outil supporte les valeurs "Usenix", "NDSS", "IEEE_ACM" et "IEEE_SP". Il faudra disposer ces valeurs dans une liste (ex : ["Usenix","IEEE_ACM"] entraînera une recherche sur les sites de Usenix et d'IEEE ACM).
* **word_to_search** : correspond à une liste de mots à rechercher. Vous pouvez mettre plusieurs mots dans un seul élément de la liste, et dans ce cas, les recherches s'effectueront avec un ET logique (forçant les deux mots à être indexés par la recherche.) (ex : ["malware", "static analysis"] entraînera une recherche des articles indexés par le mot-clé "Malware" et des articles indexés par les mots-clés "static" et "analysis" simultanément.)
* **limit_date** : correspond à la limite basse de parution des articles qui seront considérés (ex : 2016 indique que le programme essayera de limiter les articles plus vieux que 2016 (i.e. Ce n'est pas toujours possible, de temps en temps en particulier pour Usenix des articles plus vieux peuvent être ajoutés pour des raisons de différence entre la date de parution du papier sur la librairie et sa date de rédaction)).
* **limit_IEEE_page** : IEEE possédant une très grande base de données, il n'est pas rare d'obtenir plus de 600 résultats lors de la recherche par mots-clés. Afin de limiter la taille des résultats (étant déjà très importante), nous proposons une limite dans le nombre de pages explorées sur IEEE (les résultats sont triés par pertinence donc plus il y a de pages vérifiées, moins les résultats seront pertinents en général). Ainsi, la limite n'est jamais atteinte, donc une limite de 4 engendrera une exploration de 3 pages.
* **history_file** : ADT possède un historique, ainsi en mettant le nom d'un fichier au format .txt situé dans le même répertoire lors de l'exécution que le programme, il enregistrera les résultats et stockera les titres. Une fois des titres stockés, l'outil comparera les titres d'articles trouvés dans de futures recherches dans le but d'éviter de devoir réanalyser des articles déjà vus. Si vous ne souhaitez pas utiliser l'option de l'historique, vous pouvez utiliser la valeur "None" (ex : "History_malware.txt" utilisera le fichier History_malware.txt pour vérifier et enregistrer les prochains résultats).

Pour lancer le script, un simple : `python3 ADTool.py`

## Sortie

Les résultats vont dans result.txt sous le format d'un CSV utilisant le séparateur "µ". Si vous souhaitez les visualiser, nous pouvons vous conseiller de les importer dans Excel ou Google Sheet en modifiant le séparateur CSV par défaut.

J'espère que l'outil vous sera utile ! N'hésitez pas à me faire des retours ou des axes d'amélioration ! :)

