# Notepad++ Extension pour NVDA #

Cette extension améliore l'accessibilité de notepad++. Notepad++ est un éditeur de texte pour windows, et possède de nombreuses fonctionnalités. Pour en savoir plus à ce sujet aller sur <https://notepad-plus-plus.org/>

## Caractéristiques :

### Prise en charge des signets

Notepad++ permet de définir des signets dans votre texte.
Un signet vous permet de revenir rapidement vers un emplacement dans l’éditeur à n’importe quel moment.
Pour définir un signet, à partir de la ligne que vous souhaitez mettre en signet, appuyez sur contrôle+f2.
Puis, lorsque vous souhaitez revenir sur ce signet, appuyer sur f2 pour aller au signet suivant, ou maj+f2 pour revenir au Signet précédent.
Vous pouvez définir autant de signets que vous souhaitez.

### Annonce de longueur de ligne maximale

Notepad ++ a une règle qui peut être utilisée pour vérifier la longueur d'une ligne. Cependant, cette fonctionnalité n’est ni accessible ni significative pour les utilisateurs non-voyants, Par conséquent, cette extension dispose d'un indicateur de longueur de ligne audible qui émet un bip lorsqu'une ligne est plus longue que le nombre de caractères spécifié.

Pour activer cette fonctionnalité, tout d’abord activer Notepad++, puis allez dans le menu NVDA et activer Notepad++ dans le menu paramètres. Cocher la case "Activer l'indicateur de longueur de ligne" et modifiez le nombre maximal de caractères si nécessaire. Lorsque la fonctionnalité est activée, vous entendrez un bip lors du déplacement à travers des lignes trop longues ou des caractères dépassant la longueur maximale. Vous pouvez également appuyer sur NVDA+g pour aller jusqu’au premier caractère débordant sur la ligne active.

### Se déplacer au délimiteur symétrique

Dans Notepad++ vous pouvez vous déplacer au délimiteur symétrique d'un programme en appuyant sur contrôle+b. 
Pour se déplacer vous devez être dans un caractère de l'accolade à laquelle vous souhaitez correspondre.
Lorsque vous appuyez sur cette commande, NVDA lira la ligne sur laquelle vous avez atterri, et si la ligne se compose uniquement d'une accolade, il lira la ligne au-dessus et au-dessous de l'accolade afin d'avoir une idée du contexte.

### La saisie automatique

La fonctionnalité de la saisie automatique de Notepad++ n'est pas accessible par défaut. La saisie automatique a de nombreux problèmes, y compris qu'elle s'affiche dans une fenêtre flottante. Pour rendre cette fonctionnalité accessible, trois choses à faire. 

1. Lorsqu'une suggestion pour la saisie automatique s'affiche, un son comme un glissement est joué. Le son inverse est fait lorsque les suggestions disparaissent.
2. En appuyant sur les flèches bas/haut il lira le texte suggéré suivant/précédent. 
3. Le texte recommandé est verbalisé lorsque les suggestions apparaissent.

### Recherche Incrémentielle

L'une des caractéristiques les plus intéressantes de notepad++ est la possibilité d'utiliser la recherche incrémentielle. 
La recherche incrémentielle est un mode de recherche dans lequel vous recherchez une phrase-test en tapant dans le champ d'édition, et le document se déplace en vous montrant la recherche en temps réel.  
Pendant que vous tapez, le document se déplace pour afficher la ligne de texte avec la phrase la plus probable que vous recherchez. Il met également en évidence le texte qui correspond.
Le programme vous indique également combien de correspondances ont été détectées. Il y a des boutons pour se déplacer au correspondance suivante et précédente.
Au fur et à mesure que vous tapez, NVDA annoncera la ligne de texte que notepad ++ a détectée dans les résultats de la recherche. NVDA annonce également le nombre de correspondances, mais uniquement si le nombre de correspondances a changé. 
Lorsque vous avez trouvé la ligne de texte que vous voulez, il suffit d'appuyer sur Echap, et cette ligne de texte sera sur votre curseur.
Pour lancer cette boîte de dialogue, sélectionnez Recherche Incrémentielle dans le menu Recherche, ou appuyez sur alt+contrôle+i.

### Announcement des informations sur la ligne actuelle

Appuyer sur NVDA+maj+\ (barre oblique inverser) à tout moment il va annoncé ce qui suit:

* le numéro de ligne
* le numéro de colonne C'EST À DIRE. Jusqu'où vous êtes éloigné dans la ligne.
* la taille de la sélection, (nombre de caractères sélectionnés horizontalement, suivi d'un symbole |, suivi du nombre de caractères sélectionnés verticalement, ce qui ferait un rectangle.

### Prise en charge de la fonction de recherche précédente / suivante

Par défaut, si vous appuyez sur contrôle+f vous ouvrez la boîte de dialogue de recherche. 
Si vous tapez du texte ici et appuyez sur Entrée, le texte dans la fenêtre est sélectionné et le document est déplacé vers le résultat de recherche suivant. 
Dans Notepad++ Vous pouvez appuyer sur f3 ou maj+f3 pour répéter la recherche dans la direction vers l'avant ou vers l'arrière respectivement. 
NVDA lira à la fois la ligne courante et la sélection dans la ligne qui représente le texte trouvé.

### Aperçu de MarkDown ou Hypertext en tant que page Web 

Notepad++ Nativement, ne supporte pas MarkDown (*.md) avec par exemple la coloration de langage. 
Cependant, vous pouvez prévisualiser ce contenu comme un message consultable si vous appuyez sur NVDA+h (Échap pour fermer le message). 
Appuyez sur NVDA+maj+h pour l'ouvrir dans votre navigateur standard. 
Certaines extensions Markdown populaires telles que PHP Extra ou TOC sont prises en charge. 
Il fonctionne également avec (à partir d'une seule page) Html. 

Pour l'essayer, copiez le bloc suivant, collez-le dans un nouveau document Notepad ++ et appuyez sur NVDA+h :

<br>

    ---
    ## D'où cela a commencé...  
    > Il y a longtemps,  
    > dans un pays étranger.  
    ## Et où est-il allé ensuite  
    1. Première étape  
    2. Deuxième étape  
    ## Finalement, il est devenu  
    * non ordonné  
    * mais reste  
    * une liste  

<br>

## Raccourcis clavier Notepad++ non par défaut

Cette extension suppose que Notepad++ est utilisé avec les touches de raccourci par défaut. 
Si ce n'est pas le cas, S'il vous plaît, modifiez les touches de commandes de cette extension applicative pour refléter vos commandes Notepad++ selon les besoins dans la boîte de dialogue Gestes de commandes de NVDA.
Toutes les commandes de l'extension sont sous la section notepad++.