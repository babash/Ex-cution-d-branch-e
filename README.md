# 🚦 Système d'exploitation humain

**L'ordonnancement des processus, joué en classe : les élèves deviennent des processus, le tableau devient le processeur.** Pour la terminale NSI.

> Tes élèves deviennent des processus. Chacun·e reçoit une fiche avec un PID, une priorité et quelques instructions : prendre un feutre, colorier des cases d'une grille, reposer le feutre. Tu joues l'ordonnanceur : tu appelles les processus au tableau, un par un. Chaque élève n'y exécute qu'une ligne, la coche si elle a réussi, puis retourne dans la file des prêts ; si le feutre est déjà pris, direction la file des bloqués. Ligne après ligne, un dessin apparaît sur la grille… jusqu'à la troisième activité, où **tout se fige : c'est l'interblocage**.

## 👉 [Préparer la séance : babash.github.io/Babash-NSI-SNT/nsi-terminale/fichiers/os-humain/diaporama.html](https://babash.github.io/Babash-NSI-SNT/nsi-terminale/fichiers/os-humain/diaporama.html)

**Gratuit · sans compte · sans ordinateur · rien n'est enregistré**

Système d'exploitation humain fait partie des [Ressources NSI et SNT](https://babash.github.io/Babash-NSI-SNT/), rubrique [NSI Terminale](https://babash.github.io/Babash-NSI-SNT/nsi-terminale/).

---

## Une séance en quatre étapes

1. **Tu** prépares le matériel et la salle : les fiches processus de l'activité, imprimées ([activité 1](https://babash.github.io/Babash-NSI-SNT/nsi-terminale/fichiers/os-humain/fiches-activite-1.pdf), [activité 2](https://babash.github.io/Babash-NSI-SNT/nsi-terminale/fichiers/os-humain/fiches-activite-2.pdf), [activité 3](https://babash.github.io/Babash-NSI-SNT/nsi-terminale/fichiers/os-humain/fiches-activite-3.pdf) : deux fiches par page A4) ; une table avec 4 feutres, rouge, bleu, vert et noir ; au tableau, une grille de 8 × 8 cases numérotées de 1 à 64 ([modèle](Grille/grille.png)). La salle a trois zones : la file des prêts à gauche, le processeur au tableau, la file des bloqués à droite. Les processus finis retournent à leur bureau.
2. **Tu** projettes le [diaporama](https://babash.github.io/Babash-NSI-SNT/nsi-terminale/fichiers/os-humain/diaporama.html) : les objectifs, le rôle de chacun·e, le protocole d'exécution, les instructions et les zones de la classe. Les élèves qui jouent les processus reçoivent leur fiche : 6 pour les activités 1 et 2, 4 pour l'activité 3.
3. **Les élèves exécutent leur fiche** : tu appelles un processus de la file des prêts. Au tableau, l'élève exécute **une seule ligne** (c'est le quantum), coche la case si l'action a réussi, puis retourne dans la file des prêts. Si `PRENDRE` échoue, rien n'est coché, et l'élève va dans la file des bloqués.
4. **Tu fais le bilan** après chaque activité : la question de rétro-analyse du diaporama, puis la notion de cours.

Tu veux d'abord comprendre l'activité seul·e ? Le [guide de l'activité](https://babash.github.io/Babash-NSI-SNT/nsi-terminale/fichiers/os-humain/guide.html) résume les règles, les activités et leurs débriefings.

## Ce que font les élèves

Chaque fiche porte en haut le PID et la priorité du processus, puis des instructions numérotées, chacune avec sa case à cocher. Il n'y a que trois instructions : `PRENDRE(Couleur)` pour récupérer un feutre s'il est libre, `DESSINER(Couleur, [Cases])` pour colorier toutes les cases de la liste en un seul passage, et `POSER(Couleur)` pour libérer le feutre.

```text
PID 0 · priorité 1 (haute) · quantum : 1 ligne par tour
1  [ ]  PRENDRE(NOIR)
2  [ ]  DESSINER(NOIR, [9, 11])
3  [ ]  DESSINER(NOIR, [18, 19])
4  [ ]  DESSINER(NOIR, [26])
5  [ ]  POSER(NOIR)
```

| Activité | Fiches | Ce qui change | La notion du bilan |
|---|---|---|---|
| 1. Le tourniquet (*round-robin*), sur un processeur | 6 | Chacun·e son tour : premier arrivé, premier servi | Les états d'un processus (prêt, élu, bloqué) ; programme et processus |
| 2. Les priorités | 6, de priorité 1 (haute) à 3 (basse) | L'ordonnanceur appelle toujours la priorité la plus haute | La famine, et le vieillissement pour l'éviter |
| 3. L'interblocage | 4 | Des fiches qui gardent un feutre en attendant le suivant | L'interblocage et ses 4 conditions (Coffman) |

Le diaporama et le guide prévoient deux activités de plus, sans fiches dans le dépôt : le multicœur, où l'ordonnanceur appelle 3 élèves en même temps au tableau.

## Pour quels usages

| Usage | Comment |
|---|---|
| **Le multicœur** (activités 4 et 5) | 3 élèves au tableau en même temps : d'abord sans conflit, puis en compétition pour les feutres. Le bilan oppose parallélisme et concurrence. |
| **D'autres variantes** | Le guide en propose trois : éloigner la zone de dessin, pour séparer processeur et mémoire (la latence) ; plusieurs élèves avec le même PID et des fiches différentes (les *threads*, ou fils d'exécution) ; faire passer d'abord l'élève qui a le moins de cases à cocher (*Shortest Job First*, le plus court d'abord). |
| **Tes propres fiches** | Un générateur fabrique des fiches à imprimer à partir d'un fichier d'instructions (voir « Pour aller plus loin »). |
| **Comparer les politiques** | Un simulateur d'ordonnancement, à ouvrir dans le navigateur, trace le chronogramme : tourniquet, priorités, plus court d'abord, premier arrivé, avec un ou plusieurs cœurs. |

## Pourquoi ça marche

- **On vit la notion avant de la nommer** : attendre son tour, rester bloqué·e faute de feutre, se retrouver figé·e ; le cours met ensuite des mots dessus.
- **Un objet pour chaque notion** : la fiche est le programme, l'élève le processus, la case cochée le compteur ordinal, le tableau le processeur, les feutres les ressources.
- **L'architecture de von Neumann révisée au passage** : l'élève qui décode sa fiche est l'unité de commande, l'action de dessiner l'UAL, la fiche la mémoire, les déplacements le bus.
- **Des questions avant la synthèse** : après chaque activité, une rétro-analyse ouverte (« Pourquoi le système est-il totalement figé ? Qui peut débloquer la situation ? »), puis la notion de cours.
- **Les limites dites franchement** : le tableau est une sortie, pas la mémoire où l'on calcule ; et une personne met 10 secondes là où un processeur met une nanoseconde.

## Pour aller plus loin

| Document | Contenu |
|---|---|
| [Diaporama](https://babash.github.io/Babash-NSI-SNT/nsi-terminale/fichiers/os-humain/diaporama.html) (`slide.html`) | À projeter : les objectifs, les rôles, le protocole, les 5 activités, leurs rétro-analyses et les notions de cours |
| [Guide de l'activité](https://babash.github.io/Babash-NSI-SNT/nsi-terminale/fichiers/os-humain/guide.html) (`specifications.txt`) | Les objectifs, le matériel, les règles, les activités et leurs débriefings, le lexique, les limites, les variantes |
| Fiches processus : [activité 1](https://babash.github.io/Babash-NSI-SNT/nsi-terminale/fichiers/os-humain/fiches-activite-1.pdf), [activité 2](https://babash.github.io/Babash-NSI-SNT/nsi-terminale/fichiers/os-humain/fiches-activite-2.pdf), [activité 3](https://babash.github.io/Babash-NSI-SNT/nsi-terminale/fichiers/os-humain/fiches-activite-3.pdf) | Les PDF à imprimer, A4 à l'italienne ; leurs instructions sont dans `Activites/` |
| [Grille](Grille/grille.png) | Le modèle de la grille de 64 cases numérotées |
| [Simulateur d'ordonnancement](A%20ranger/chronogramme_os.html) | Une page à télécharger et à ouvrir dans le navigateur |

### Fabriquer d'autres fiches

```sh
python3 "A ranger/generateur_fiches.py" Activites/A3_mono_interblocage/script1 -o fiches.html
```

Le fichier d'instructions donne, pour chaque fiche, `PID:` et `PRIORITE:` (1, 2 ou 3), puis une instruction par ligne ; `---` sépare deux fiches (exemple : `A ranger/exemple_instructions.txt`). La page produite s'imprime en PDF depuis le navigateur.

## Contact

Conçu par Babash - NSI Tani Malandi et Johanne Bakalara (enseignante de NSI à Bandrélé) pour les classes de NSI de terminale de l'académie de Mayotte.
Une question, une idée, un bug ? Les [issues GitHub](https://github.com/babash/Ex-cution-d-branch-e/issues) du dépôt. Toutes les ressources sont sur le site [Ressources NSI et SNT](https://babash.github.io/Babash-NSI-SNT/).

## Licence

- **Le code** (le générateur `A ranger/generateur_fiches.py` et le simulateur `A ranger/chronogramme_os.html`) est sous licence [MIT](LICENSE).
- **Les documents** (le diaporama `slide.html`, le guide `specifications.txt`, les fiches processus et leurs instructions, les pages de fiches de `A ranger/`, la grille et les images) sont sous licence [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/deed.fr).
- **[reveal.js](https://revealjs.com)**, de Hakim El Hattab (le moteur du diaporama) : licence MIT. **[Font Awesome Free](https://fontawesome.com)** (ses icônes) : licence CC BY 4.0. Le diaporama les charge en ligne : ils ne font pas partie du dépôt.

Tu peux les réutiliser et les modifier, y compris pour tes classes, en mentionnant Babash - NSI Tani Malandi, Johanne Bakalara et la licence ; un document modifié se partage sous la même licence. Si tu utilises l'IA pour les modifier, merci de le préciser.
