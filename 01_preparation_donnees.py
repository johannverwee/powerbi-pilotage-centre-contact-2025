from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]

RAW_FILE = BASE_DIR / "data" / "raw" / "3-1-1-contact-centre-metrics.csv"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# Lecture du fichier brut
df = pd.read_csv(RAW_FILE, sep=";")

# Renommage en français
df = df.rename(
    columns={
        "Date": "date",
        "CallsOffered": "appels_presentes",
        "CallsHandled": "appels_traites",
        "CallsAbandoned": "appels_abandonnes",
        "AverageSpeedofAnswer": "delai_moyen_reponse_sec",
        "ServiceLevel": "niveau_service",
        "BI_ID": "id",
    }
)

# Conversion des types
df["date"] = pd.to_datetime(df["date"], errors="coerce")

colonnes_numeriques = [
    "appels_presentes",
    "appels_traites",
    "appels_abandonnes",
    "delai_moyen_reponse_sec",
    "niveau_service",
]

for col in colonnes_numeriques:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Variables temporelles
df["annee"] = df["date"].dt.year
df["mois"] = df["date"].dt.to_period("M").astype(str)
df["nom_mois"] = df["date"].dt.month_name(locale="fr_FR")
df["jour_semaine"] = df["date"].dt.day_name(locale="fr_FR")
df["numero_jour_semaine"] = df["date"].dt.weekday + 1
df["semaine_iso"] = df["date"].dt.isocalendar().week.astype(int)

# Indicateurs calculés
df["taux_abandon"] = df["appels_abandonnes"] / df["appels_presentes"]
df["taux_traitement"] = df["appels_traites"] / df["appels_presentes"]
df["niveau_service_pct"] = 100 * df["niveau_service"]

# On garde l'année complète 2025 pour le dashboard principal
df_2025 = df[df["annee"] == 2025].copy()

# Table journalière 2025
journalier_2025 = df_2025[
    [
        "date",
        "annee",
        "mois",
        "nom_mois",
        "jour_semaine",
        "numero_jour_semaine",
        "semaine_iso",
        "appels_presentes",
        "appels_traites",
        "appels_abandonnes",
        "delai_moyen_reponse_sec",
        "niveau_service",
        "niveau_service_pct",
        "taux_abandon",
        "taux_traitement",
    ]
].copy()

# Agrégation mensuelle
mensuel_2025 = (
    df_2025.groupby(["annee", "mois", "nom_mois"], as_index=False)
    .agg(
        appels_presentes=("appels_presentes", "sum"),
        appels_traites=("appels_traites", "sum"),
        appels_abandonnes=("appels_abandonnes", "sum"),
        delai_moyen_reponse_sec=("delai_moyen_reponse_sec", "mean"),
        niveau_service=("niveau_service", "mean"),
    )
)

mensuel_2025["taux_abandon"] = (
    mensuel_2025["appels_abandonnes"] / mensuel_2025["appels_presentes"]
)
mensuel_2025["taux_traitement"] = (
    mensuel_2025["appels_traites"] / mensuel_2025["appels_presentes"]
)
mensuel_2025["niveau_service_pct"] = 100 * mensuel_2025["niveau_service"]

# Agrégation par jour de semaine
jour_semaine_2025 = (
    df_2025.groupby(["numero_jour_semaine", "jour_semaine"], as_index=False)
    .agg(
        appels_presentes=("appels_presentes", "sum"),
        appels_traites=("appels_traites", "sum"),
        appels_abandonnes=("appels_abandonnes", "sum"),
        delai_moyen_reponse_sec=("delai_moyen_reponse_sec", "mean"),
        niveau_service=("niveau_service", "mean"),
    )
    .sort_values("numero_jour_semaine")
)

jour_semaine_2025["taux_abandon"] = (
    jour_semaine_2025["appels_abandonnes"] / jour_semaine_2025["appels_presentes"]
)
jour_semaine_2025["niveau_service_pct"] = 100 * jour_semaine_2025["niveau_service"]

# Synthèse annuelle 2025
total_appels_presentes = df_2025["appels_presentes"].sum()
total_appels_traites = df_2025["appels_traites"].sum()
total_appels_abandonnes = df_2025["appels_abandonnes"].sum()

synthese_2025 = pd.DataFrame(
    [
        {
            "annee": 2025,
            "appels_presentes": total_appels_presentes,
            "appels_traites": total_appels_traites,
            "appels_abandonnes": total_appels_abandonnes,
            "taux_abandon": total_appels_abandonnes / total_appels_presentes,
            "taux_traitement": total_appels_traites / total_appels_presentes,
            "delai_moyen_reponse_sec": df_2025["delai_moyen_reponse_sec"].mean(),
            "niveau_service": df_2025["niveau_service"].mean(),
            "niveau_service_pct": 100 * df_2025["niveau_service"].mean(),
        }
    ]
)

# Exports
journalier_2025.to_csv(
    PROCESSED_DIR / "appels_journaliers_2025.csv",
    index=False,
    sep=";",
    encoding="utf-8-sig",
    decimal=",",
)

mensuel_2025.to_csv(
    PROCESSED_DIR / "appels_mensuels_2025.csv",
    index=False,
    sep=";",
    encoding="utf-8-sig",
    decimal=",",
)

jour_semaine_2025.to_csv(
    PROCESSED_DIR / "appels_par_jour_semaine_2025.csv",
    index=False,
    sep=";",
    encoding="utf-8-sig",
    decimal=",",
)

synthese_2025.to_csv(
    PROCESSED_DIR / "synthese_appels_2025.csv",
    index=False,
    sep=";",
    encoding="utf-8-sig",
    decimal=",",
)

print("Fichiers préparés créés :")
print(PROCESSED_DIR / "appels_journaliers_2025.csv")
print(PROCESSED_DIR / "appels_mensuels_2025.csv")
print(PROCESSED_DIR / "appels_par_jour_semaine_2025.csv")
print(PROCESSED_DIR / "synthese_appels_2025.csv")
print()
print("Contrôle rapide 2025 :")
print(f"Appels présentés : {total_appels_presentes:,.0f}")
print(f"Appels traités : {total_appels_traites:,.0f}")
print(f"Appels abandonnés : {total_appels_abandonnes:,.0f}")
print(f"Taux d'abandon : {100 * total_appels_abandonnes / total_appels_presentes:.2f} %")