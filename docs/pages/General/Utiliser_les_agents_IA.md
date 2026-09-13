---
title: "Utiliser les agents IA"
url: "https://docs.alliancecan.ca/wiki/Utiliser_les_agents_IA"
category: "General"
last_modified: "2026-09-04T23:50:10Z"
page_id: 34833
display_title: "Utiliser les agents IA"
---

Les agents d’intelligence artificielle (IA) peuvent aider à lire et expliquer du code, modifier des fichiers, exécuter des commandes, préparer des scripts de soumission, analyser des journaux et soutenir le débogage. Sur une infrastructure de calcul partagé, leur utilisation demande toutefois de distinguer clairement le processus agentique, les ressources de calcul et le service de modèle utilisé. ==
Cette page présente des principes techniques généraux pour l’utilisation d’agents IA sur les grappes de l’Alliance. Elle ne constitue pas une approbation institutionnelle d’un produit ou d’un fournisseur particulier.

Important : À ce jour, l’Alliance n’a pas formulé de recommandation générale pour ou contre l’utilisation d’agents IA sur ses grappes. Le sujet est encore à l’étude. Les positions propres à un site ou à un partenaire régional doivent être distinguées des politiques générales de l’Alliance.

== Comprendre où s’exécute un agent IA ==

Il faut distinguer au moins deux composants :

* le client agentique, qui s’exécute dans l’environnement où l’agent est lancé;
* le modèle de langage, qui peut être fourni localement ou par un service externe, selon la configuration utilisée.

Un agent lancé avec le compte d’un utilisateur agit généralement avec les permissions accordées à ce compte. Il peut donc, selon son mode d’autorisation, lire des fichiers, exécuter des commandes ou préparer du contexte destiné au modèle.

Si l’agent est lancé sur un nœud de connexion, son processus s’exécute sur ce nœud. S’il est lancé dans une allocation interactive SLURM, son processus s’exécute sur le nœud de calcul alloué. Cette distinction est importante pour respecter les bonnes pratiques de calcul haute performance.

== Où exécuter un agent IA? ==

Emplacement                                   	Usage recommandé                                                                     	Remarques
Poste local ou machine virtuelle              	Souvent l’option la plus simple pour héberger l’agent.                               	L’agent fonctionne hors de la grappe et l’utilisateur se connecte ensuite aux ressources selon les mécanismes SSH, MFA et SLURM autorisés.
Nœud de connexion                             	À limiter aux opérations très légères.                                               	Une utilisation prolongée ou des commandes agentiques coûteuses ne conviennent pas à un nœud de connexion.
Nœud de calcul dans une allocation interactive	Adapté au développement, aux petits tests, à la validation et au débogage interactif.	L’utilisation reste soumise aux politiques locales et à la connectivité réseau disponible sur les nœuds de calcul.
Tâche batch SLURM                             	Méthode standard pour les calculs reproductibles, longs ou coûteux.                  	L’agent peut aider à préparer ou analyser la tâche, mais le calcul est géré par SLURM.
Nœud d’automatisation                         	Dépend du site.                                                                      	À Calcul Québec, ces nœuds sont destinés à des plateformes déterministes entièrement contrôlées par l’utilisateur; un agent IA ne correspond pas à cette définition.

== Utilisation avec SLURM ==

Les charges de calcul intensives doivent être exécutées sur les nœuds de calcul au moyen du planificateur. Voir Exécuter des tâches et Qu’est-ce qu’un ordonnanceur?.

Pour une utilisation interactive, demander d’abord une allocation, par exemple :

salloc \
  --account= \
  --time=01:00:00 \
  --cpus-per-task=2 \
  --mem=4G

Puis ouvrir un shell dans l’allocation :

srun --pty bash

Vérifier ensuite que la session se trouve bien dans une allocation :

hostname
echo "$SLURM_JOB_ID"
echo "$SLURM_CPUS_PER_TASK"

Pour les expériences longues ou reproductibles, privilégier une tâche batch avec sbatch. L’agent peut aider à préparer le script, mais chaque directive #SBATCH devrait être vérifiée par l’utilisateur avant la soumission.

Fin de session : quitter l’agent et le shell interactif lorsqu’ils ne sont plus nécessaires, puis vérifier qu’aucune allocation inutile ne reste active avec :

squeue -u "$USER"

== Sécurité, confidentialité et protection des données ==

=== Données sensibles ===

Les ressources de calcul général de l’Alliance ne sont pas appropriées pour le stockage de données sensibles. Avant d’utiliser un agent IA, consulter Protection des données, vie privée et confidentialité ainsi que les exigences de votre établissement et de votre projet.

L’utilisation d’un agent IA ne change pas la classification ni les obligations applicables aux données.

=== Permissions entre utilisateurs ===

Un agent lancé par un autre utilisateur ne contourne pas automatiquement les permissions du système de fichiers. Les contrôles Unix habituels continuent de s’appliquer.

La question est différente lorsqu’un utilisateur lance lui-même un agent : l’agent peut alors accéder aux ressources que le compte peut lire ou modifier, dans la mesure permise par son mode d’autorisation.

Distinction importante : « un autre utilisateur ne peut pas lire mes fichiers » et « mon propre agent peut accéder à des fichiers que mon compte peut lire » sont deux questions différentes.

=== Données transmises à un service externe ===

Si le modèle est fourni par un service externe, certains éléments de contexte nécessaires au traitement peuvent quitter l’infrastructure locale, selon la configuration de l’outil.

Avant toute utilisation :

* ne pas fournir de secrets, mots de passe, clés privées, jetons ou codes MFA dans un prompt;
* limiter l’agent au répertoire de projet nécessaire;
* éviter d’exposer des fichiers sans lien avec la tâche;
* examiner les permissions demandées et les commandes proposées;
* vérifier les politiques du fournisseur, de l’établissement et du projet;
* ne pas utiliser l’agent avec des données dont les conditions d’utilisation externe ne sont pas clairement établies.

== Permissions et contrôle humain ==

L’utilisateur reste responsable des commandes, modifications et calculs qu’il autorise.

Une configuration prudente devrait notamment imposer les principes suivants :

# expliquer les actions prévues avant leur exécution;
# ne pas lancer de calculs intensifs sur les nœuds de connexion;
# utiliser SLURM pour les charges de calcul;
# demander une confirmation avant de modifier des fichiers;
# demander une confirmation avant d’installer des logiciels;
# demander une confirmation avant de soumettre ou d’annuler des tâches;
# ne jamais supprimer des données sans approbation explicite;
# ne pas parcourir des répertoires sans lien avec le projet;
# ne jamais afficher ou modifier des identifiants ou secrets;
# résumer les actions réalisées.

== SSH, clés publiques et authentification multifacteur ==

Les clés SSH et l’authentification multifacteur peuvent correspondre à des étapes distinctes de l’authentification. Une clé publique acceptée ne signifie pas que l’étape MFA doit être contournée ou désactivée.

Voir SSH, Clés SSH, Authentification multifacteur et Automatisation dans le contexte de l’authentification multifacteur.

Lorsqu’un agent ou une application encapsule une connexion SSH, il faut vérifier que l’outil sait gérer une session interactive et le défi MFA. Si une connexion SSH classique fonctionne mais que l’intégration de l’application échoue, le problème peut provenir de la manière dont cette application gère l’interaction SSH ou le terminal.

Pour diagnostiquer la connexion depuis le même environnement que l’agent :

ssh -v @.alliancecan.ca

Ne jamais joindre une clé privée, un mot de passe, un code MFA ou un jeton d’API à un ticket de soutien.

== Nœuds d’automatisation ==

Les règles applicables aux nœuds d’automatisation peuvent varier selon le site.

À Calcul Québec, la position communiquée est que ces nœuds doivent être utilisés par des plateformes déterministes et entièrement contrôlées par l’utilisateur. Un agent IA n’est pas considéré comme répondant à cette définition. Un déploiement persistant d’un agent sur ce type de nœud n’est donc pas approprié à Calcul Québec.

Les architectures à privilégier sont plutôt :

* un poste local ou une VM qui héberge l’agent, avec connexion à la grappe par les mécanismes supportés;
* une allocation interactive SLURM pour les essais interactifs sur un nœud de calcul, lorsque les politiques et la connectivité le permettent;
* des tâches batch SLURM pour les calculs reproductibles ou coûteux.

== Bonnes pratiques ==

* Ne pas utiliser les nœuds de connexion pour des calculs ou une activité agentique intensive.
* Utiliser SLURM pour les travaux CPU ou GPU.
* Limiter l’agent au répertoire de projet nécessaire.
* Conserver un contrôle humain sur les modifications, installations, suppressions et soumissions de tâches.
* Ne jamais fournir de secrets à l’agent ou dans un ticket de soutien.
* Vérifier les règles applicables aux données avant d’utiliser un modèle ou un service externe.
* Valider indépendamment le code, les résultats scientifiques et les ressources SLURM suggérées par l’agent.
* Documenter les versions des outils, bibliothèques et environnements pour assurer la reproductibilité.
* Fermer les allocations interactives lorsqu’elles ne sont plus nécessaires.

== Informations à fournir dans un ticket de soutien ==

Lorsque vous signalez un problème lié à un agent IA, fournir si possible :

* le nom de la grappe;
* l’emplacement où l’agent est exécuté : poste local, VM, nœud de connexion ou nœud de calcul;
* le système d’exploitation et la version de l’outil;
* la méthode de connexion SSH utilisée;
* la présence ou non d’une allocation SLURM;
* le message d’erreur exact, sans secret;
* la sortie pertinente d’un diagnostic en lecture seule;
* la différence observée entre une connexion SSH classique et la connexion initiée par l’agent, le cas échéant.

== Voir aussi ==

* Exécuter des tâches
* Bonnes pratiques pour la soumission de tâches
* Protection des données, vie privée et confidentialité
* Authentification multifacteur
* Automatisation dans le contexte de l’authentification multifacteur
* SSH
* Claude sur les grappes de l’Alliance