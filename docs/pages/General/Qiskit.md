---
title: "Qiskit"
url: "https://docs.alliancecan.ca/wiki/Qiskit"
category: "General"
last_modified: "2026-05-25T19:46:51Z"
page_id: 25819
display_title: "Qiskit"
---

Qiskit est une bibliothèque de programmation quantique à code source ouvert développée en Python par IBM. Comme PennyLane et Snowflurry, elle permet de construire, simuler et exécuter des circuits quantiques.

== Installation ==
1. Chargez les dépendances de Qiskit.

2. Créez et activez un environnement virtuel Python.

3. Installez une version spécifique de Qiskit.
X.Y.Z  qiskit_aerX.Y.Z}}
où X.Y.Z représente le numéro de la version, par exemple 1.4.0. Pour installer la plus récente version disponible sur nos grappes, n'indiquez pas de version. Ici, nous n'avons importé que qiskit et qiskit_aer. Vous pouvez ajouter d'autres logiciels Qiskit en fonction de vos besoins en suivant la structure qiskit_package==X.Y.Z où qiskit_package représente le logiciel voulu, par exemple qiskit-finance. Les wheels présentement disponibles sont listés sur la page Wheels Python.

4. Validez l’installation de Qiskit.

5. Gelez l'environnement et les dépendances.

==Exécuter Qiskit sur une grappe==

Vous pouvez ensuite soumettre votre tâche à l'ordonnanceur.
== Utiliser Qiskit avec MonarQ ==

Il est possible d’utiliser directement MonarQ avec Qiskit via le plugiciel qiskit-calculquebec. Ce plugiciel permet de développer et d'exécuter des circuits Qiskit sur l’infrastructure de Calcul Québec.

=== Installation des dépendances ===

* Étape 1 : Installer les dépendances

* Note : qiskit-calculquebec installe automatiquement Qiskit.

=== Initialisation du backend MonarQ et exécution du circuit ===

* Étape 2 : Configurer vos identifiants et le backend
** Créez un client avec vos identifiants. Votre jeton est disponible via le portail Thunderhead.
** Le host est https://monarq.calculquebec.ca.
** Initialisez ensuite le backend MonarQ.

* Étape 3 : Transpiler et exécuter le circuit

=== Notes ===

* La transpilation est nécessaire pour adapter le circuit à la connectivité et aux portes natives de MonarQ.
* Le nombre de shots peut être ajusté selon les besoins (maximum : 1024).
* L’utilisation de SamplerV2 est recommandée pour l’exécution de circuits avec mesures.

Ensuite, nous définissons le circuit. Nous appliquons une porte Hadamard afin de créer un état de superposition sur le premier qubit et nous appliquons ensuite une porte CNOT pour intriquer le premier et le deuxième qubit.
    circuit = QuantumCircuit(2)
    circuit.h(0)
    circuit.cx(0,1)
    circuit.measure_all()

Nous précisons le simulateur que nous voulons utiliser. AerSimulator étant le simulateur par défaut. Nous obtenons le dénombrement des états finaux des qubits après 1000 mesures.
    simulator = AerSimulator()
    result = simulator.run(circuit, shots=1000).result()
    counts = result.get_counts()
    print(counts)
    {'00': 489, '11': 535}
Nous affichons un histogramme des résultats avec la commande
    plot_histogram(counts)

-->