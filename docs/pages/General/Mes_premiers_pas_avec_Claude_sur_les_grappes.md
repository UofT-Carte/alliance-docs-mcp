---
title: "Mes premiers pas avec Claude sur les grappes"
url: "https://docs.alliancecan.ca/wiki/Mes_premiers_pas_avec_Claude_sur_les_grappes"
category: "General"
last_modified: "2026-09-05T00:03:49Z"
page_id: 34830
display_title: "Mes premiers pas avec Claude sur les grappes"
---

Claude Code est un agent de codage en ligne de commande développé par Anthropic. Il peut notamment lire et expliquer du code, modifier des fichiers, exécuter des commandes shell, préparer des scripts SLURM, analyser des journaux et soutenir le débogage.

Cette page décrit l’installation et l’utilisation de Claude Code dans le contexte des grappes de l’Alliance. Pour les principes généraux applicables à tous les agents IA : emplacement d’exécution, SLURM, sécurité, données, permissions et MFA, voir Utiliser les agents IA.

Terminologie : le terme « Claude » désigne ici Claude Code ou un environnement qui s’appuie sur Claude Code. Une interface comme « Claude Science » peut encapsuler Claude Code, mais son mécanisme de connexion SSH ou d’authentification peut différer.

== Avant de commencer ==

Avant d’utiliser Claude sur une grappe :

* déterminer où le client Claude sera exécuté;
* éviter une utilisation prolongée sur un nœud de connexion;
* utiliser SLURM pour les charges de calcul;
* vérifier la politique applicable aux données du projet;
* vérifier que la connectivité réseau requise est disponible;
* conserver un contrôle humain sur les commandes et modifications proposées.

Pour une utilisation interactive sur la grappe, une allocation SLURM constitue l’architecture technique privilégiée lorsque les politiques locales et la connectivité le permettent.

== Installation de Claude Code ==

Avant d’installer Claude, vérifier si l’exécutable est déjà disponible :

which claude
claude --version

=== Installation native ===

La documentation Anthropic recommande une installation native sur Linux. Dans un environnement où le téléchargement externe est autorisé :

curl -fsSL https://claude.ai/install.sh | bash

Le lanceur est généralement installé dans l’espace utilisateur. Au besoin, ajouter le répertoire correspondant au PATH :

export PATH="$HOME/.local/bin:$PATH"
claude --version
claude doctor

À vérifier localement : les politiques de réseau sortant et d’installation de logiciels peuvent varier entre systèmes. Ne pas utiliser sudo pour contourner les permissions d’une grappe partagée.

=== Installation avec npm ===

Une installation avec npm est également possible. Vérifier d’abord les versions disponibles :

node --version
npm --version

Puis installer le paquet dans un espace utilisateur approprié :

npm install -g @anthropic-ai/claude-code
claude --version

Ne pas utiliser sudo npm install -g sur une grappe partagée.

=== Vérification de l’installation ===

Les commandes suivantes permettent de vérifier l’installation :

claude --version
claude doctor

claude doctor fournit des diagnostics en lecture seule sur l’installation et la configuration.

== Authentification et connectivité réseau ==

Claude Code doit être authentifié auprès du service de modèle configuré. Selon le contexte, l’authentification peut passer par un compte Claude autorisé, la Console/API Anthropic ou un fournisseur d’infrastructure pris en charge par l’organisation.

Lors du premier lancement :

claude

le client ouvre normalement le flux de connexion approprié.

Claude Code nécessite également une connectivité réseau vers le service configuré. Il est donc possible que l’exécutable fonctionne dans un environnement mais que la session échoue dans un autre si les règles de réseau sortant diffèrent.

Secrets : ne jamais placer une clé API, un mot de passe, une clé SSH privée ou un code MFA dans un fichier partagé, un script SLURM, un dépôt Git ou un ticket de soutien.

== Exécution interactive avec SLURM ==

Demander d’abord une allocation :

salloc \
  --account= \
  --time=01:00:00 \
  --cpus-per-task=2 \
  --mem=4G

Ouvrir ensuite un shell dans l’allocation :

srun --pty bash

Vérifier l’environnement :

hostname
echo "$SLURM_JOB_ID"
echo "$SLURM_CPUS_PER_TASK"

Puis se placer dans le répertoire de projet et lancer Claude :

cd /path/to/project
claude

Quitter Claude et l’allocation lorsqu’ils ne sont plus nécessaires. Vérifier les tâches actives avec :

squeue -u "$USER"

== Exemple de test sur Narval ==

L’exemple suivant illustre un test contrôlé. Il peut être adapté à une autre grappe.

=== Structure du projet ===

claude_science_test/
├── config/
├── logs/
├── results/
├── scripts/
├── src/
├── environment.sh
├── REPORT.md
└── TUTORIAL.md

=== Explorer le projet sans modification ===

Exemple de prompt :

Read the current project.
Explain the directory structure.
Do not modify any file.

=== Créer un petit programme Python ===

Exemple de prompt :

Create a Python program called hello_cluster.py.

The program should:
- print the hostname
- print the current date
- print the Python version

Explain the code before creating it.

Exemple de programme :

import platform
import socket
from datetime import datetime

print("Hostname:", socket.gethostname())
print("Date:", datetime.now())
print("Python:", platform.python_version())

=== Préparer un script SLURM ===

Exemple de prompt :

Create a Slurm script to execute hello_cluster.py.

Requirements:
- 1 CPU
- 1 GB RAM
- execution time: 5 minutes
- save logs in logs/

Explain the script before creating it.

Exemple de script :

#!/bin/bash
#SBATCH --job-name=claude_hello
#SBATCH --account=
#SBATCH --time=00:05:00
#SBATCH --cpus-per-task=1
#SBATCH --mem=1G
#SBATCH --output=logs/%x-%j.out
#SBATCH --error=logs/%x-%j.err

module load python
python src/hello_cluster.py

=== Soumettre et suivre la tâche ===

Après vérification humaine du script :

sbatch scripts/run_hello.sh
squeue -u "$USER"
sacct -j  --format=JobID,JobName,State,Elapsed,AllocCPUS,ReqMem,MaxRSS,ExitCode

=== Analyser les résultats ===

Exemple de prompt :

Read the newest Slurm output.
Explain whether the execution succeeded.
Identify errors, if any.
Do not modify any files.

Principe : Claude peut accélérer le développement et l’analyse, mais ne remplace pas la validation scientifique, la revue du code ni la compréhension des ressources demandées.

== Claude et les tâches batch ==

Pour une expérience longue, reproductible ou coûteuse, le rôle de Claude devrait rester centré sur la préparation, la revue et l’analyse. L’exécution scientifique reste gérée par SLURM.

# Demander à Claude de lire le programme et d’estimer les ressources nécessaires.
# Faire générer un script SLURM et vérifier chaque directive #SBATCH.
# Soumettre la tâche avec sbatch après validation humaine.
# Utiliser squeue et sacct pour suivre l’exécution.
# Demander à Claude d’analyser les journaux et les résultats, puis valider scientifiquement la conclusion.

== Limiter l’accès de Claude au projet ==

Avant de lancer Claude, vérifier les permissions du répertoire :

ls -ld /path/to/project
ls -l /path/to/project

Se placer ensuite dans le répertoire minimal nécessaire :

cd /project//mon_projet
claude

Dans son mode manuel, Claude Code utilise un modèle de permissions où les opérations d’écriture et de nombreuses commandes demandent l’approbation de l’utilisateur. L’utilisateur reste responsable de la sécurité des commandes et du code qu’il approuve.

== Claude Science, SSH et Duo MFA ==

Un cas de soutien a montré une situation où SSH fonctionnait normalement depuis un terminal avec une clé publique, alors qu’une connexion initiée par Claude Science vers une ressource de l’Alliance ne présentait pas correctement l’étape Duo MFA.

Pour diagnostiquer ce type de problème, exécuter le test depuis le même environnement que Claude Science :

ssh -v @narval.alliancecan.ca

Vérifier ensuite :

* si Claude Science utilise un client SSH intégré ou la commande ssh du système;
* le système d’exploitation et la version de Claude;
* si la connexion attend indéfiniment ou se termine immédiatement;
* la partie pertinente de la sortie ssh -v, sans partager de secrets.

Si le SSH classique fonctionne mais que l’intégration de l’application ne présente pas le défi Duo, le problème est probablement lié à la manière dont l’application gère la session SSH interactive ou le terminal, plutôt qu’au compte Alliance lui-même.

Une clé SSH publique et Duo MFA répondent à des étapes d’authentification distinctes. Il ne faut pas tenter de contourner Duo.

== Nœuds d’automatisation de Calcul Québec ==

Calcul Québec a indiqué que ses nœuds d’automatisation sont destinés à des plateformes déterministes entièrement contrôlées par l’utilisateur. Claude, en tant qu’agent IA, ne répond pas à cette définition.

Il ne faut donc pas demander à héberger Claude comme service persistant sur un nœud d’automatisation de Calcul Québec.

Les options à privilégier sont :

* Claude sur un poste local ou une VM, avec connexion à la grappe par les mécanismes supportés;
* Claude dans une allocation interactive SLURM pour les essais interactifs lorsque cela est permis;
* SLURM batch pour les calculs reproductibles ou coûteux.

== Dépannage ==

Symptôme                                                              	Vérification                                                                     	Action
claude: command not found                                             	which claude et echo $PATH                                                       	Vérifier l’installation utilisateur et le répertoire ~/.local/bin.
Claude fonctionne dans un environnement mais pas dans un autre        	claude --version, claude doctor, variables d’environnement et connectivité réseau	Comparer le PATH, l’authentification et l’accès réseau.
Authentification impossible                                           	claude doctor                                                                    	Vérifier la méthode d’authentification; ne jamais publier les jetons.
Connexion SSH classique fonctionnelle mais échec depuis Claude Science	ssh -v depuis le même environnement                                              	Vérifier la gestion de la session interactive, du terminal et du défi MFA par l’application.
Une tâche générée demande trop de ressources                          	Relire les directives #SBATCH                                                    	Ajuster les ressources avant sbatch et valider les besoins du programme.

== Prompts de départ ==

Les exemples suivants peuvent servir pour des tests contrôlés.

=== Comprendre le projet ===

Read the project and explain:
1. the directory structure;
2. the main entry points;
3. the dependencies;
4. how the program is expected to run.
Do not modify files.

=== Créer un script SLURM ===

Review this program and propose a Slurm script for an Alliance cluster.
Explain every #SBATCH directive before creating the file.
Do not submit the job.

=== Analyser des journaux ===

Read the most recent Slurm output and error files.
Identify the likely cause of failure.
Propose diagnostic steps before proposing modifications.
Do not modify files.

=== Revue HPC ===

Review this workflow for HPC best practices.
Check CPU, memory, GPU, walltime, filesystem usage and Slurm directives.
Explain any issue you find.
Do not change files and do not submit jobs.

== Foire aux questions ==

=== Puis-je lancer Claude directement après une connexion SSH sur Narval? ===

Un test très léger peut être effectué pour vérifier l’installation. Pour une utilisation prolongée ou susceptible de lancer des commandes, demander une allocation SLURM et utiliser un nœud de calcul, sous réserve des politiques et de la connectivité du site.

=== Claude utilise-t-il les GPU de la grappe pour générer ses réponses? ===

Dans l’utilisation standard de Claude Code avec un service de modèle externe, la génération du modèle ne s’effectue pas sur les GPU de la grappe. Les GPU de la grappe sont utilisés par les programmes de l’utilisateur soumis via SLURM.

=== Une clé SSH publique remplace-t-elle Duo? ===

Non. Une clé SSH publique et MFA peuvent correspondre à des étapes distinctes. Il ne faut pas tenter de contourner Duo.

=== Puis-je installer Claude sur un nœud d’automatisation? ===

Pas sur les nœuds d’automatisation de Calcul Québec, selon la position communiquée par Calcul Québec.

=== L’Alliance recommande-t-elle officiellement Claude? ===

À ce jour, aucune recommandation générale pour ou contre l’utilisation d’agents IA n’a été établie. La présente page est un guide technique et non une approbation institutionnelle du produit.

=== Puis-je utiliser Claude avec des données sensibles? ===

Les ressources de calcul général de l’Alliance ne sont pas conçues pour le stockage de données sensibles. Consulter Protection des données, vie privée et confidentialité et les exigences de votre établissement avant toute utilisation.

== Voir aussi ==

* Agents IA sur les grappes de l’Alliance
* Exécuter des tâches
* Bonnes pratiques pour la soumission de tâches
* Protection des données, vie privée et confidentialité
* Authentification multifacteur
* Automatisation dans le contexte de l’authentification multifacteur
* SSH

== Références externes ==

* Anthropic — Claude Code
* Anthropic — sécurité de Claude Code