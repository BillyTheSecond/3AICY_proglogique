
# TP Business Rules

Les business rules, ou règles métier, sont des directives qui définissent ou contraignent certaines actions dans une organisation. Elles sont essentielles pour assurer la cohérence, la conformité et l'efficacité des processus métiers.

## Exemples

Exemples de règles métier pour les ressources humaines :

- "Les employés doivent soumettre leurs demandes de congé au moins deux semaines à l'avance."
- "Les heures supplémentaires doivent être approuvées par le responsable hiérarchique avant d'être effectuées."

Il y a plusieurs façons d'implémenter des règles métier :

- directement par une écriture ad hoc dans un code ;
- en utilisant des systèmes de gestion des règles métier (BRMS) comme Drools.

Exemple de règle Drools :

```drools
rule "Reorder Stock"
  when
       $item : StockItem(quantity < reorderLevel)
  then
       System.out.println("Reorder needed for: " + $item.getProductName());
end
```

## Sujet : Business Rules Pour Le Business

On s'intéresse aux règles métier pour un site d'achat en ligne.
On simplifie la notion de date en la notant selon le format donné dans les faits.

Définir les règles Prolog pour les règles métier suivantes.

Vous donnerez :

- les faits ;
- les règles ;
- les tests que vous avez effectués.

Vous pouvez rendre un fichier texte de préférence, ou un fichier `swinb`.

## Faits De Base

```prolog
% Le 18 mai 2026
aujourdhui(20260518).

% Clients
% predicat(ID_Client, email, numeroJourAnniversaire(1 = 1er janvier, 365 = 31 décembre))
client(1, 'clientA@fri.com', 20060123).
client(2, 'clientB@fri.com', 20060328).
client(3, 'clientC@rouge.com', 20160426).
client(4, 'clientD@rouge.com', 19480526).
client(5, 'clientE@wanadou.com', 19550427).
client(6, 'clientF@wanadou.com', 19680426).
client(7, 'clientG@ahoel.com', 19720518).
client(8, 'clientH@ahoel.com', 19841011).
client(9, 'clientI@jaimail.com', 19980528).
client(10, 'clientJ@jaimail.com', 20080720).
```

## Rappel Prolog

```prolog
Dif is 8 - 3. % Affecte la différence 5 à la variable Dif.
Dif =:= 2.   % Vérifie si la valeur de Dif vaut 2.
A =< B.      % A <= B.
A >= B.      % A >= B.
```

## Règles Métier

### 1. Relance Après Abandon De Panier

> Envoyer un email de relance aux clients qui ont abandonné leur panier d'achat dans les 24 heures.

Vous indiquerez la liste des adresses emails.

Quelques faits :

```prolog
% panier_abandonne(ID_Panier, ID_Client, NumJour).
panier_abandonne(1, 1, 260517).
panier_abandonne(11, 5, 260516).
panier_abandonne(13, 8, 260102).
```

### 2. Relance Pour Les Clients Inactifs

> Envoyer un email promotionnel aux clients qui n'ont pas effectué d'achat depuis 30 jours.

Quelques faits :

```prolog
% dernier_achat(ID_Client, JourDernierAchat).
dernier_achat(3, 260416).
dernier_achat(1, 260423).
dernier_achat(13, 260118).
dernier_achat(7, 251123).
```

### 3. Relance Pour Les Anniversaires

> Envoyer un email avec une offre spéciale aux clients une semaine avant leur anniversaire.

### 4. Relance Pour Les Produits Complémentaires

> Envoyer un email suggérant des produits complémentaires aux clients qui ont acheté un produit spécifique.

Quelques faits :

```prolog
% achat(ID_Client, nom_produit, JourAchat, Montant).
achat(1, 'ordinateur portable', 260110, 310).
achat(1, 'ordinateur portable', 260115, 280).
achat(2, 'smartphone', 250717, 650).
achat(3, 'appareil photo', 250907, 250).
achat(4, 'enceinte bluetooth', 250910, 80).
achat(5, 'téléviseur 4K', 260404, 350).
achat(6, 'console de jeux', 260404, 890).
achat(7, 'aspirateur robot', 260223, 450).
achat(8, 'montre connectée', 260309, 110).
achat(9, 'casque audio', 251211, 120).
achat(9, 'casque audio', 251127, 110).
achat(10, 'imprimante', 251207, 220).

% Exemples de produits complémentaires.
produit_complementaire('ordinateur portable', 'sacoche pour ordinateur').
produit_complementaire('ordinateur portable', 'souris sans fil').
produit_complementaire('smartphone', 'coque de protection').
produit_complementaire('smartphone', 'écouteurs sans fil').
produit_complementaire('appareil photo', 'trépied').
produit_complementaire('appareil photo', 'carte mémoire').
produit_complementaire('enceinte bluetooth', 'câble audio').
produit_complementaire('enceinte bluetooth', 'support mural').
produit_complementaire('téléviseur 4K', 'barre de son').
produit_complementaire('téléviseur 4K', 'support TV').
produit_complementaire('console de jeux', 'manette supplémentaire').
produit_complementaire('console de jeux', 'jeu vidéo').
produit_complementaire('aspirateur robot', 'filtres de rechange').
produit_complementaire('aspirateur robot', 'station de charge').
produit_complementaire('montre connectée', 'bracelet de rechange').
produit_complementaire('montre connectée', 'chargeur sans fil').
produit_complementaire('casque audio', 'étui de transport').
produit_complementaire('casque audio', 'câble jack').
produit_complementaire('imprimante', 'cartouches d\'encre').
produit_complementaire('imprimante', 'papier photo').
```

### 5. Relance Pour Les Avis Clients

> Envoyer un email demandant un avis aux clients une semaine après un achat.

### 6. Relance Pour Les Produits En Rupture De Stock

> Informer les clients par email lorsque des produits qu'ils ont consultés sont de nouveau en stock.

Quelques faits :

```prolog
% consulte(ID_Client, nom_produit, JourConsultation).
consulte(1, 'appareil photo', 250907).
consulte(1, 'enceinte bluetooth', 250910).
consulte(1, 'imprimante', 251207).
consulte(10, 'ordinateur portable', 260110).
consulte(10, 'smartphone', 250717).
consulte(3, 'aspirateur robot', 260223).
consulte(3, 'console de jeux', 260319).
consulte(3, 'console de jeux', 260319).
consulte(3, 'console de jeux', 260318).
consulte(3, 'console de jeux', 260320).
consulte(3, 'console de jeux', 260319).
consulte(3, 'téléviseur 4K', 260123).
consulte(4, 'montre connectée', 260309).
consulte(5, 'casque audio', 251127).

% stock(nb_elements, nom_produit).
stock(10, 'appareil photo').
stock(0, 'enceinte bluetooth').
stock(1, 'imprimante').
stock(10, 'ordinateur portable').
stock(10, 'smartphone').
stock(0, 'aspirateur robot').
stock(5, 'console de jeux').
stock(0, 'téléviseur 4K').
stock(0, 'montre connectée').
stock(50, 'casque audio').
```

### 7. Relance Basée Sur Le Comportement D'achat

> Envoyer un email personnalisé aux clients qui ont acheté des produits d'une certaine catégorie plus de deux fois en un mois, avec une recommandation de produits complémentaire.

Quelques faits :

```prolog
categorie('appareil photo').
categorie('aspirateur robot').
categorie('casque audio').
categorie('console de jeux').
categorie('enceinte bluetooth').
categorie('montre connectée').
categorie('ordinateur portable').
categorie('smartphone').
categorie('téléviseur 4K').
```

Astuce : regardez le comportement de cette ligne :

```prolog
categorie(M), findall(Categorie, achat(Email, M, Date), Dates).
```

### 8. Relance Basée Sur Le Score De Satisfaction

> Envoyer un email avec une offre spéciale aux clients ayant un score de satisfaction inférieur à 7/10 pour améliorer leur expérience.

Quelques faits :

```prolog
satisfaction(1, 6).
satisfaction(2, 8).
satisfaction(3, 9.5).
satisfaction(4, 9).
satisfaction(5, 7.5).
satisfaction(6, 7.75).
satisfaction(7, 5).
satisfaction(8, 6).
satisfaction(9, 6).
satisfaction(10, 7).
```

### 9. Relance Basée Sur L'historique De Navigation

> Envoyer un email avec des suggestions de produits aux clients qui ont consulté des pages spécifiques plus de deux fois sans acheter.

### 10. Relance Basée Sur Le Panier Moyen

> Envoyer un email avec une offre de fidélité aux clients dont le panier moyen dépasse 500 euros sur les trois derniers mois.
