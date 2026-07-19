# FACADIER.SARL — L'art de la pose

## Installation

```bash
pip install -r requirements.txt
```

## Fichiers à conserver ensemble

```
app.py
assets/
  logo_facadier.jpg   <- le logo doit rester dans ce sous-dossier, à côté de app.py
requirements.txt
```

## Lancement

```bash
streamlit run app.py
```

L'application s'ouvre sur `http://localhost:8501`.

## Contenu

Un seul fichier `app.py` contenant les 7 modules demandés :

1. **Location de nacelles** (activité prioritaire) — dashboard temps réel, planning/disponibilité (heatmap 14 jours), réservations, contrats & bons de sortie, tarification éditable, suivi matériel & retours.
2. **Chantiers façades** — devis (aluminium, verre, marbre, placage), suivi kanban par étape (Devis → Commande → Fabrication → Pose → Livré), timeline détaillée par chantier.
3. **Calcul de structure** — dimensionnement panneau (pression de vent simplifiée), vérification des charges, recommandations d'ancrages par type de support, checklist de conformité.
4. **Facturation & gestion clients** — génération de factures, suivi des statuts, fiches clients détaillées.
5. **Dossiers clients (GED)** — dépôt de documents, historique chronologique, devis/contrats regroupés par client.
6. **Comptabilité** — recettes/dépenses/marges sur 12 mois, répartition par activité, détail mensuel.
7. **Automatisation** — règles déclencheur → action activables/désactivables, création de nouvelles règles, canaux de notification.

## Données

Les données sont générées en mémoire (`st.session_state`) à des fins de démonstration. Pour brancher une vraie base de données (PostgreSQL, Airtable, etc.), remplacer les DataFrames dans `init_data()` par des requêtes à votre source de données — le reste de l'interface reste inchangé.

## Identité visuelle

- Typographies : Space Grotesk (titres) + Inter (texte) + JetBrains Mono (données chiffrées).
- Palette : navy structurel (#0F2A44), orange sécurité nacelle (#FF7A29), teal verrier (#14A0A0), crème marbre (#F6F4EF).
- Icônes : SVG vectoriels dessinés sur mesure (aucun emoji) + icônes Bootstrap Icons pour la navigation.
- Motif signature : trame "mur-rideau" (mullions) en fond du bandeau d'en-tête, écho direct au métier de la façade.
