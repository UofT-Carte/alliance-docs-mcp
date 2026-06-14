---
title: "Metrix/en-ca"
url: "https://docs.alliancecan.ca/wiki/Metrix/en-ca"
category: "General"
last_modified: "2026-06-05T16:12:04Z"
page_id: 33374
display_title: "Metrix/en-ca"
---

= Aperçu =

Le portail Metrix est un site web destiné aux usagers de l'Alliance. Il exploite les informations collectées sur les nœuds de calcul et les serveurs de gestion pour générer, de manière interactive, des données permettant aux usagers de suivre en temps réel leur utilisation des ressources (CPU, GPU, mémoire, système de fichiers).

Rorqual	https://metrix.rorqual.alliancecan.ca
Narval 	http://metrix.narval.alliancecan.ca
Nibi   	https://portal.nibi.sharcnet.ca
tamIA  	https://portail.tamia.ecpia.ca
Vulcan 	http://metrix.vulcan.alliancecan.ca

Performance des système de fichiers

On retrouve ici les graphiques de bandes passantes et d'opérations sur les métadonnées, accompagnés des options de visualisation suivantes: dernière semaine, dernier jour et dernière heure.

Nœuds de connexion

Les statistiques d’utilisation des CPU, de la mémoire, de la charge système et du réseau sont présentées dans cet onglet, avec les options de visualisation suivantes : dernière semaine, dernier jour et dernière heure.

Ordonnancement

Cet onglet présente des statistiques sur les cœurs et les GPU alloués de la grappe, avec les options de visualisation suivantes : dernière semaine, dernier jour et dernière heure.

Logiciels scientifiques

Les logiciels les plus utilisés avec les cœurs CPU et les GPU sont présentés sous forme de graphiques.

Nœuds de transfert de données

Les statistiques de bande passante des nœuds de transfert de données sont présentées dans cet onglet.

= Sommaire utilisateur =
Sous l'onglet sommaire utilisateur, vous trouverez vos quotas des différents systèmes de fichiers, suivis de vos 10 dernières tâches. Vous pouvez en sélectionner une par son numéro et accéder à la page détaillée. De plus, en cliquant sur (Plus de détails), vous serez redirigé directement vers l'onglet Statistiques des tâches, où vous allez retrouver toutes vos tâches.

= Statistiques des tâches =
Le premier bloc affiche votre utilisation actuelle (Cœur CPU, mémoire et GPUs). Ces statistiques représentent la moyenne des ressources utilisées par l’ensemble des tâches en cours d’exécution. Vous pouvez comparer facilement les ressources qui vous sont allouées à celles que vous utilisez réellement.

Vous avez ensuite accès à une moyenne des derniers jours, présentée sous forme de graphique.

Vous avez ensuite une représentation de votre activité sur les systèmes de fichiers. À gauche, le graphique montre le nombre de commandes d’écriture sur disque que vous avez effectuées. (input/output operations per second (IOPS)) À droite, vous voyez la quantité de données transférées vers les serveurs sur une période donnée. (Bande passante)

La section suivante présente l’ensemble des tâches que vous avez déjà lancées, qui sont actuellement en cours d’exécution ou en attente. En haut à gauche, vous pouvez filtrer les tâches par statut (OOM, completed, running, etc.). En haut à droite, vous pouvez effectuer une recherche par numéro de tâche (Job ID) ou par nom. Enfin, en bas à droite, une option vous permet de naviguer rapidement entre les pages en effectuant des sauts multiples.

== Page d'une tâche CPU ==
Vous avez en haut le nom de la tâche, son numéro et votre nom d'utilisateur ainsi que le statut. Les détails de votre script de soumission s'affichent en cliquant sur Voir le script de la tâche. Si la tâche a été lancée en mode interactif, le script de soumission ne sera pas disponible.

Le répertoire de travail et la commande de soumission sont accessibles en cliquant sur Voir la commande de soumission.

La prochaine section est dédiée aux informations de l'ordonnanceur. Vous pouvez accéder à la page de suivi de votre compte CPU en cliquant sur le numéro de votre compte.

Dans la section Ressources vous pouvez obtenir un aperçu initial de l'utilisation des ressources de votre tâche en comparant les colonnes Alloués et Utilisés pour les différents paramètres listés.

Le graphique CPU vous permet de visualiser, dans le temps, des cœurs CPUs que vous avez demandés. À droite, vous pouvez sélectionner/désélectionner les différents cœurs selon vos besoins. Notez que pour des tâches très courtes, ce graphique n'est pas disponible.

Le graphique Mémoire vous permet de visualiser, dans le temps, l'utilisation de la mémoire que vous avez demandée.

Le graphique Process and threads vous permet d'observer différents paramètres liés aux processus et aux fils d'exécution. Idéalement, pour une tâche multifils (multithreading), l'addition du paramètre Running threads et Sleeping threads ne devrait pas dépasser de 2 fois le nombre de cœurs demandé. Cela dit, il est tout à fait normal d'avoir quelques processus en mode dormant (Sleeping threads) pour certain type de programmes (java, Matlab, logiciels commercial ou programmes complexes). Vous avez aussi en paramètre les applications du programme exécutées au fil du temps.

Les graphiques suivants représentent l'utilisation du système de fichier pour la tâche en cours et non du nœud au complet. À gauche, une représentation du nombre d’opérations d’entrée/sortie par seconde (IOPS) est affichée. À droite, le graphique illustre le débit de transfert de données entre la tâche et le système de fichiers au fil du temps. Ce graphique permet d’identifier les périodes d’activité intense ou de faible utilisation du système de fichiers.

Pour les statistiques des ressources du nœud au complet, sachez quelles peuvent être imprécises si le nœud est partagé entre plusieurs utilisateurs. Le graphique de gauche, illustre l'évolution de la bande passante utilisée par la tâche au fil du temps, en lien avec les logiciels, les licences, etc. Le graphique de droite représente l’évolution de la bande passante réseau utilisée par une tâche ou un ensemble de tâches via le réseau Infiniband, au fil du temps. On peut y observer les périodes de transfert massif de données (ex. : lecture/écriture sur un système de fichiers (Lustre), communication MPI entre nœuds).

Le graphique de gauche illustre l’évolution du nombre d’opérations d’entrée/sortie par seconde (IOPS) effectuées sur le disque local au fil du temps. Celui de droite montre l’évolution de la bande passante utilisée sur le disque local au fil du temps, c’est-à-dire la quantité de données lues ou écrites par seconde.

Représentation graphique de l’utilisation de l’espace disque local.

Représentation graphique de la puissance utilisée.

== Page d'une tâche CPU (vecteur de tâches, job array)==

La page d'une tâche CPU dans un vecteur de tâches est identique à celle d'une tâche CPU régulière, à l'exception de la section Other jobs in the array. Le tableau liste les autres numéros de tâches faisant partie du même vecteur de tâches, ainsi que des informations sur leur statut, leur nom, leur heure de début et leur heure de fin.

== Page d'une tâche GPU  ==

En haut de page, vous avez le nom de la tâche, son numéro et votre nom d'utilisateur ainsi que le statut. Les détails de votre script de soumission s'affichent en cliquant sur Voir le script de la tâche. Si vous avez lancé une tâche interactive, le script de soumission n'est pas disponible.

Le répertoire et la commande de soumission sont accessibles en cliquant sur Voir la commande de soumission.

La section suivante est réservée aux informations de l'ordonnanceur. Vous pouvez accéder à la page de votre compte GPU en cliquant sur le numéro de votre compte.

Dans la section Ressources vous pouvez obtenir un premier aperçu de l'utilisation des ressources de votre tâche en comparant les colonnes Alloués et Utilisés pour les différents paramètres listés.

Le graphique CPU vous permet de visualiser l'utilisation des cœurs CPUs demandés au fil du temps. À droite, vous pouvez sélectionner/désélectionner les différents cœurs selon vos besoins. Notez que pour des tâches très courtes, ce graphique n'est pas disponible.

Le graphique Mémoire vous permet de visualiser l'utilisation dans le temps de la mémoire que vous avez demandée pour les CPU.

Le graphique Process and threads vous permet d'observer différents paramètres liés aux processus et aux fils d'exécution.

Les graphiques suivants représentent l'utilisation du système de fichier pour la tâche en cours et non du nœud au complet. À gauche, une représentation du nombre d’opérations d’entrée/sortie par seconde (IOPS) est affichée. À droite, le graphique illustre le débit de transfert de données entre la tâche et le système de fichiers au fil du temps. Ce graphique permet d’identifier les périodes d’activité intense ou de faible utilisation du système de fichiers.

Le graphique GPU représente votre utilisation des GPU. Le paramètre Streaming Multiprocessors (SM) active indique le pourcentage de temps pendant lequel le GPU exécute un warp (un groupe de threads consécutifs) dans la dernière fenêtre d’échantillonnage. Cette valeur devrait idéalement se situer autour de 80 %. Pour le SM occupancy (défini comme le rapport entre le nombre de warps affectés à un SM et le nombre maximal de warps qu’un SM peut gérer), une valeur autour de 50 % est généralement attendue. Concernant le paramètre Tensor, la valeur devrait être la plus élevée possible. Idéalement, votre code devrait exploiter cette partie du GPU, optimisée pour les multiplications et convolutions de matrices multidimensionnelles. Enfin, pour les opérations en virgule flottante (Floating Point) FP64, FP32 et FP16, vous devriez observer une activité significative sur un seul de ces types, selon la précision utilisée par votre code.

À gauche, vous avez un graphique indiquant la mémoire utilisée par le GPU. À droite, un graphique des cycles d'accès du GPU à la mémoire, représentant le pourcentage de cycles pendant lesquels l’interface mémoire de l’appareil est active pour envoyer ou recevoir des données.

Le graphique de puissance GPU affiche l’évolution de la consommation énergétique (en watts) du GPU au fil du temps.

This next graph shows the GPU bandwidth on the PCIe bus (or PCI Express, for Peripheral Component Interconnect Express).
thumb|900px|center

Pour les statistiques des ressources du nœud au complet, sachez quelles peuvent être imprécises si le nœud est partagé entre plusieurs utilisateurs. Le graphique de gauche, illustre l'évolution de la bande passante utilisée par la tâche au fil du temps, en lien avec les logiciels, les licences, etc. Le graphique de droite représente l’évolution de la bande passante réseau utilisée par une tâche ou un ensemble de tâches via le réseau Infiniband, au fil du temps. On peut y observer les périodes de transfert massif de données (ex. : lecture/écriture sur un système de fichiers (Lustre), communication MPI entre nœuds).

Le graphique de gauche illustre l’évolution du nombre d’opérations d’entrée/sortie par seconde (IOPS) effectuées sur le disque local au fil du temps. Celui de droite montre l’évolution de la bande passante utilisée sur le disque local au fil du temps, c’est-à-dire la quantité de données lues ou écrites par seconde.

Représentation graphique de l’utilisation de l’espace disque local.

Représentation graphique de la puissance utilisée.

= Statistiques d'un compte =

La section Statistique d'un compte regroupe l'utilisation de votre groupe dans deux sous-sections: CPU et GPU.

== Statistiques d'un compte CPU ==

Vous y trouverez la somme des demandes de votre groupe pour les cœurs CPU, ainsi que leur utilisation correspondante au cours des derniers mois. Vous pouvez également suivre l'évolution de votre priorité, qui varie en fonction de votre utilisation.

Ce graphique montre les applications les plus couramment utilisées.

Vous pouvez consulter ici l'utilisation des ressources par chacun des utilisateurs de votre groupe.

Ce graphique montre l’évolution dans le temps des cœurs CPU gaspillés par chaque utilisateur du groupe.

Vous pouvez consulter ici l’utilisation de la mémoire par chacun des utilisateurs de votre groupe.

Ce graphique représente la mémoire gaspillée par chaque utilisateur.

Vous avez ensuite une représentation de votre activité sur les systèmes de fichiers. À gauche, le graphique montre le nombre de commandes d’écriture sur disque que vous avez effectuées. (input/output operations per second (IOPS)) À droite, vous voyez la quantité de données transférées vers les serveurs sur une période donnée. (Bande passante)

Vous avez une liste des dernières tâches qui ont été effectuées pour l'ensemble du groupe.

== Statistiques d'un compte GPU ==

Vous retrouvez ici la somme des demandes GPUs de votre groupe, ainsi que l'utilisation correspondante au cours des derniers mois. Vous pouvez également suivre l’évolution de votre priorité, qui varie en fonction de votre utilisation.

Ce graphique représente les applications les plus couramment utilisées.

Vous pouvez consulter ici l’utilisation des ressources par chacun des utilisateurs de votre groupe.

Le graphique suivant représente, dans le temps, la quantité de GPU gaspillés par utilisateur.

Vous avez ensuite les cœurs CPUs alloués et utilisés dans vos tâches GPU.

Cette figure illustre ici le gaspillage des CPUs dans le cadre de vos tâches GPU.

Vous pouvez visualiser ici l'utilisation de la mémoire pour chaque utilisateur de votre groupe.

Ce graphique illustre la mémoire gaspillée par chaque utilisateur.

Vous avez ensuite une représentation de votre activité sur les systèmes de fichiers. À gauche, le graphique montre le nombre de commandes d’écriture sur disque que vous avez effectuées. (input/output operations per second (IOPS)) À droite, vous voyez la quantité de données transférées vers les serveurs sur une période donnée. (Bande passante)

Voici la liste des dernières tâches effectuées au niveau de votre groupe.

= Statistiques du cloud =

Le premier tableau « Vos instances » présente l'ensemble des machines virtuelles associées à un compte. La colonne « Saveur » fait référence au type de machine virtuelle. La colonne « UUID » correspond à un identifiant unique attribué à chaque machine virtuelle.

Ensuite, chaque machine virtuelle dispose de ses propres statistiques d'utilisation (Cœurs CPU, Mémoire, Bande passante disque, IOPS disque et Bande passante réseau) affichables pour le dernier mois, la dernière semaine, le dernier jour ou la dernière heure.