% TP2 - Business Rules

% Le 18 mai 2026
aujourdhui(20260518).

% Clients
% client(ID_Client, Email, DateNaissance).
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

% panier_abandonne(ID_Panier, ID_Client, NumJour).
panier_abandonne(1, 1, 20260517).
panier_abandonne(11, 5, 20260516).
panier_abandonne(13, 8, 20260102).

% dernier_achat(ID_Client, JourDernierAchat).
dernier_achat(3, 20260416).
dernier_achat(1, 20260423).
dernier_achat(13, 20260118).
dernier_achat(7, 20251123).

% achat(ID_Client, NomProduit, JourAchat, Montant).
achat(1, 'ordinateur portable', 20260110, 310).
achat(1, 'ordinateur portable', 20260115, 280).
achat(2, 'smartphone', 20250717, 650).
achat(3, 'appareil photo', 20250907, 250).
achat(4, 'enceinte bluetooth', 20250910, 80).
achat(5, 'téléviseur 4K', 20260404, 350).
achat(6, 'console de jeux', 20260404, 890).
achat(7, 'aspirateur robot', 20260223, 450).
achat(8, 'montre connectée', 20260309, 110).
achat(9, 'casque audio', 20251211, 120).
achat(9, 'casque audio', 20251127, 110).
achat(10, 'imprimante', 20251207, 220).

% produit_complementaire(Produit, ProduitComplementaire).
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

% consulte(ID_Client, NomProduit, JourConsultation).
consulte(1, 'appareil photo', 20250907).
consulte(1, 'enceinte bluetooth', 20250910).
consulte(1, 'imprimante', 20251207).
consulte(10, 'ordinateur portable', 20260110).
consulte(10, 'smartphone', 20250717).
consulte(3, 'aspirateur robot', 20260223).
consulte(3, 'console de jeux', 20260319).
consulte(3, 'console de jeux', 20260319).
consulte(3, 'console de jeux', 20260318).
consulte(3, 'console de jeux', 20260320).
consulte(3, 'console de jeux', 20260319).
consulte(3, 'téléviseur 4K', 20260123).
consulte(4, 'montre connectée', 20260309).
consulte(5, 'casque audio', 20251127).

% stock(NbElements, NomProduit).
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

categorie('appareil photo').
categorie('aspirateur robot').
categorie('casque audio').
categorie('console de jeux').
categorie('enceinte bluetooth').
categorie('montre connectée').
categorie('ordinateur portable').
categorie('smartphone').
categorie('téléviseur 4K').


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

% Convertit une date longue 20260518 en date courte 260518.
% Si la date est deja courte, elle ne change pas.
date_courte(Date, DateCourte) :-
    Date > 1000000,
    DateCourte is Date mod 1000000.

date_courte(Date, Date) :-
    Date =< 1000000.

aujourdhui_court(JourCourt) :-
    aujourdhui(JourComplet),
    date_courte(JourComplet, JourCourt).

% Regle metier 1 :
% envoyer un email de relance aux clients qui ont abandonne leur panier dans les 24 heures.
relance_panier_abandonne(Email) :-
    aujourdhui_court(Aujourdhui),
    panier_abandonne(_, IDClient, JourAbandon),
    date_courte(JourAbandon, JourAbandonCourt),
    Difference is Aujourdhui - JourAbandonCourt,
    Difference >= 0,
    Difference =< 1,
    client(IDClient, Email, _).

emails_relance_panier(Emails) :-
    findall(Email, relance_panier_abandonne(Email), Emails).

% Tests a lancer dans SWI-Prolog :
% ?- relance_panier_abandonne(Email).
% Email = 'clientA@fri.com'.
%
% ?- emails_relance_panier(Emails).
% Emails = ['clientA@fri.com'].
