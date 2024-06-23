import csv
import random

# Beispielwerte für die verschiedenen Bereiche
age_values = ["Unter 18", "18-24", "25-34", "35-44", "45-54", "55-64", "65 oder älter"]
gender_values = ["Männlich", "Weiblich", "Divers"]
education_values = ["Kein Abschluss", "Hauptschulabschluss", "Realschulabschluss", "Abitur", "Berufsausbildung", "Bachelor-Abschluss", "Master-Abschluss", "Promotion", "Andere"]
decision_description_values = ["Arbeitsplatzwechsel", "Umzug in eine andere Stadt", "Beginn oder Ende einer Beziehung", "Größere finanzielle Investition", "Gesundheitsbezogene Entscheidung"]
decision_type_values = ["Beruflich", "Persönlich", "Finanziell", "Gesundheitlich", "Zwischenmenschlich", "Andere"]
decision_rating_values = ["Sehr gut", "Gut", "Neutral", "Schlecht", "Sehr schlecht"]
influencing_factors_values = ["Ratschläge von Freunden/Familie", "Eigene Erfahrungen", "Expertenmeinungen", "Online-Recherche", "Bauchgefühl", "Andere"]
consequences_values = ["Positive berufliche Entwicklung", "Negative berufliche Entwicklung", "Verbesserte finanzielle Situation", "Verschlechterte finanzielle Situation", "Verbesserte zwischenmenschliche Beziehungen", "Verschlechterte zwischenmenschliche Beziehungen", "Verbesserte Gesundheit", "Verschlechterte Gesundheit", "Andere"]
time_to_consequences_values = ["Sofort", "Innerhalb eines Tages", "Innerhalb einer Woche", "Innerhalb eines Monats", "Innerhalb eines Jahres", "Mehr als ein Jahr später"]
consequence_rating_values = ["Sehr positiv", "Positiv", "Neutral", "Negativ", "Sehr negativ"]
long_term_impact_values = ["Ja", "Nein", "Unsicher"]
similar_decisions_values = ["Ja", "Nein"]
similar_outcomes_values = ["Ja", "Nein", "Teilweise"]
noticed_patterns_values = ["Bestimmte Entscheidungen führen immer zu positiven Folgen", "Bestimmte Entscheidungen führen immer zu negativen Folgen", "Die Folgen sind unvorhersehbar", "Andere"]
suggestions_values = ["Keine"]

# Funktion zum Zufallsgenerieren eines Datensatzes
def generate_random_record():
    return [
        random.choice(age_values),
        random.choice(gender_values),
        random.choice(education_values),
        random.choice(decision_description_values),
        random.choice(decision_type_values),
        random.choice(decision_rating_values),
        random.choice(influencing_factors_values),
        random.choice(consequences_values),
        random.choice(time_to_consequences_values),
        random.choice(consequence_rating_values),
        random.choice(long_term_impact_values),
        random.choice(similar_decisions_values),
        random.choice(similar_outcomes_values),
        random.choice(noticed_patterns_values),
        random.choice(suggestions_values)
    ]

# Datensätze generieren
records = [generate_random_record() for _ in range(1000)]

# Spaltennamen auf Englisch umbenennen, um mit der Datenbank übereinzustimmen
columns = [
    "age", "gender", "education", "decision_description",
    "decision_type", "decision_rating", "influencing_factors",
    "consequences", "time_to_consequences", "consequence_rating",
    "long_term_impact", "similar_decisions", "similar_outcomes",
    "noticed_patterns", "suggestions"
]

# Datensätze in eine CSV-Datei speichern
with open('random_survey_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(columns)  # Spaltennamen schreiben
    writer.writerows(records)  # Datensätze schreiben

print("10.000 Datensätze wurden erfolgreich in 'random_survey_data.csv' gespeichert.")
