---
title: "MonarQ/en-ca"
url: "https://docs.alliancecan.ca/wiki/MonarQ/en-ca"
category: "General"
last_modified: "2026-09-18T12:43:02Z"
page_id: 27460
display_title: "MonarQ"
---

Nœud de connexion : https://manager.anyonlabs.com

MonarQ est un  ordinateur quantique supraconducteur à 24 qubits développé à Montréal par Anyon Systèmes et situé à l'École de technologie supérieure. Pour plus d'informations sur les spécifications et les performances de MonarQ voir Spécifications techniques ci-dessous.

== Technical specifications ==

== Accéder à MonarQ ==

# Pour commencer le processus d'accès à MonarQ, remplir ce formulaire. Il doit être complété par le chercheur principal.
# Vous devez avoir un compte avec l'Alliance pour avoir accès à MonarQ.
# Rencontrez notre équipe pour discuter des spécificités de votre projet, des accès, et des détails de facturation.
# Recevoir l'accès au tableau de bord MonarQ et générer votre jeton d'accès.
# Pour démarrer, voir Premiers pas sur MonarQ ci-dessous.

Contactez notre équipe quantique à quantique@calculquebec.ca si vous avez des questions ou si vous souhaitez avoir une discussion plus générale avant de demander l'accès.

== Spécifications techniques ==

À l'instar des processeurs quantiques disponibles aujourd'hui, MonarQ fonctionne dans un environnement où le bruit reste un facteur significatif. Les métriques de performance, mises à jour à chaque calibration, sont accessibles via le portail Thunderhead. L'accès à ce portail nécessite une approbation d'accès à MonarQ.

On y retrouve, entre autres, les métriques suivantes :
* Processeur quantique de 24 qubits
* Porte un qubit avec fidélité de 99.8% et durée de 32ns
* Porte deux qubits avec fidélité de 96% et durée de 90ns
* Temps de cohérence de 4-10μs (en fonction de l'état)
* Profondeur maximale du circuit d'environ 350 pour des portes à un qubit et 115 pour des portes à deux qubits

== Logiciels de calcul quantique ==

Il existe plusieurs bibliothèques logicielles spécialisées pour faire du calcul quantique et pour développer des algorithmes quantiques. Ces bibliothèques permettent de construire des circuits qui sont exécutés sur des simulateurs qui imitent la performance et les résultats obtenus sur un ordinateur quantique tel que MonarQ. Elles peuvent être utilisées sur toutes les grappes de l’Alliance.

* PennyLane, bibliothèque de commandes en Python
* Snowflurry, bibliothèque de commandes en Julia
* Qiskit, bibliothèque de commandes en Python

Les portes logiques quantiques du processeur de MonarQ sont appelées par le biais d'une bibliothèque logicielle Snowflurry, écrit en Julia. Bien que MonarQ soit nativement compatible avec Snowflurry, il existe un plugiciel PennyLane-CalculQuébec développé par Calcul Québec permettant d'exécuter des circuits sur MonarQ tout en bénéficiant des fonctionnalités et de l'environnement de développement offerts par PennyLane.

== Premiers pas sur MonarQ ==
Prérequis : Assurez-vous d’avoir un accès à MonarQ ainsi que vos identifiants de connexion (username, API token). Pour toute question, écrivez à  quantique@calculquebec.ca.

* Étape 1 : Connectez-vous à Narval
** MonarQ est accessible depuis Narval, une grappe de Calcul Québec. L’accès à Narval se fait à partir du nœud de connexion narval.alliancecan.ca.
** Pour de l’aide concernant la connexion à Narval, consultez la page SSH.

* Étape 2 : Créez l’environnement
** Créez un environnement virtuel Python (3.11 ou ultérieur) pour utiliser PennyLane et le plugiciel PennyLane-CalculQuébec. Ces derniers sont déjà installés sur Narval et  vous aurez uniquement à importer les bibliothèques logicielles que vous souhaitez.

* Étape 3 : Configurez vos identifiants sur MonarQ et définissez MonarQ comme machine (device)
** Ouvrez un fichier Python .py et importez les dépendances nécessaires soit PennyLane et CalculQuebecClient dans l’exemple ci-dessous.
** Créez un client avec vos identifiants. Votre jeton est disponible à partir du portail Thunderhead. Le host est https://manager.anyonlabs.com
** Créez un device PennyLane avec votre client. Vous pouvez également mentionner le nombre de qubits (wires) à utiliser et le nombre d'échantillons ( shots).
** Pour de l’aide, consultez pennylane_calculquebec.

* Étape 4 : Créez votre circuit
** Dans le même fichier Python vous pouvez maintenant coder votre circuit quantique

* Étape 5 : Exécutez votre circuit depuis l'ordonnanceur
** La commande sbatch est utilisée pour soumettre une tâche sbatch.

$ sbatch simple_job.sh
Submitted batch job 123456

Avec un script Slurm ressemblant à ceci:

* Le résultat du circuit est écrit dans un fichier dont le nom commence par slurm-, suivi de l'ID de la tâche et du suffixe .out, par exemple slurm-123456.out.
* On retrouve dans ce fichier le résultat de notre circuit dans un dictionnaire {'000': 496, '001': 0, '010': 0, '011': 0, '100': 0, '101': 0, '110': 0, '111': 504}.
* Pour plus d’information sur comment soumettre des tâches sur Narval, voir Exécuter des tâches.

== Questions courantes ==
* Foire aux questions (FAQ)

==Autres outils ==
* Transpileur quantique

== Applications ==
MonarQ est adapté aux calculs nécessitant de petites quantités de qubits de haute fidélité, ce qui en fait un outil idéal pour le développement et le test d'algorithmes quantiques. D'autres applications possibles incluent la modélisation de petits systèmes quantiques; les tests de nouvelles méthodes et techniques de programmation quantique et de correction d'erreurs; et plus généralement, la recherche fondamentale en informatique quantique.

== Soutien technique ==
Si vous avez des questions sur nos services quantiques, écrivez à quantique@calculquebec.ca.
Les sessions sur l'informatique quantique et la programmation avec MonarQ sont listées ici.