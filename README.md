# Pilotage d’un centre de contact 3-1-1 en 2025

Projet personnel de data analyse réalisé à partir de données publiques du centre de contact 3-1-1 de Vancouver.

L’objectif est de construire un tableau de bord Power BI permettant de suivre l’activité annuelle, d’analyser les volumes hebdomadaires et d’identifier les semaines à risque pour la planification.

## Livrables

- [Dashboard Power BI exporté en PDF](dashboard_pilotage_centre_contact_2025.pdf)
- [Note de synthèse du projet](note_synthese_pilotage_centre_contact_2025.pdf)
- Fichier Power BI : `pilotage_centre_contact_2025.pbix`
- Script Python de préparation des données : `01_preparation_donnees.py`
- Tables préparées pour Power BI au format CSV

## Outils utilisés

- Python / pandas
- Power BI
- DAX
- Analyse temporelle
- Indicateurs de pilotage

## Résultats principaux

En 2025, le centre de contact enregistre 358 295 appels présentés. Le taux d’abandon annuel est de 4,94 %, tandis que le niveau de service moyen atteint 80,28 %.

L’analyse hebdomadaire met en évidence une forte activité en début d’année. Les cinq semaines les plus chargées sont les semaines 5, 6, 3, 2 et 4.

La page d’aide à la décision identifie 23 semaines sous l’objectif de niveau de service fixé à 80 %, représentant 171 963 appels concernés.

## Compétences illustrées

Ce projet montre une démarche complète de traitement et de restitution de données opérationnelles :

- nettoyage et préparation des données avec Python/pandas ;
- création de tables adaptées à Power BI ;
- construction de mesures DAX ;
- analyse mensuelle et hebdomadaire ;
- identification de semaines à risque ;
- restitution synthétique orientée pilotage métier.

## Données

Les données utilisées proviennent du jeu de données public “3-1-1 contact centre metrics” relatif au centre de contact 3-1-1 de Vancouver.
