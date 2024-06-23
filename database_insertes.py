import sqlite3
import random

# Verbindung zur SQLite-Datenbank herstellen
conn = sqlite3.connect('survey.db')
c = conn.cursor()

# Hilfsfunktionen zur Erstellung der Daten
def random_choice(choices):
    return random.choice(choices)

def create_example_data():
    ages = ["Unter 18", "18-24", "25-34", "35-44", "45-54", "55-64", "65 oder älter"]
    genders = ["Männlich", "Weiblich", "Divers"]
    educations = ["Kein Abschluss", "Hauptschulabschluss", "Realschulabschluss", "Abitur", "Berufsausbildung", "Bachelor-Abschluss", "Master-Abschluss", "Promotion", "Andere"]
    decision_descriptions = ["Arbeitsplatzwechsel", "Umzug in eine andere Stadt", "Beginn oder Ende einer Beziehung", "Größere finanzielle Investition", "Gesundheitsbezogene Entscheidung", "Andere"]
    decision_types = ["Beruflich", "Persönlich", "Finanzielle Natur", "Gesundheitlich", "Zwischenmenschlich", "Andere"]
    decision_ratings = ["Sehr gut", "Gut", "Neutral", "Schlecht", "Sehr schlecht"]
    influencing_factors = ["Ratschläge von Freunden/Familie", "Eigene Erfahrungen", "Expertenmeinungen", "Online-Recherche", "Bauchgefühl", "Andere"]
    consequences = ["Positive berufliche Entwicklung", "Negative berufliche Entwicklung", "Verbesserte finanzielle Situation", "Verschlechterte finanzielle Situation", "Verbesserte zwischenmenschliche Beziehungen", "Verschlechterte zwischenmenschliche Beziehungen", "Verbesserte Gesundheit", "Verschlechterte Gesundheit", "Andere"]
    time_to_consequences = ["Sofort", "Innerhalb eines Tages", "Innerhalb einer Woche", "Innerhalb eines Monats", "Innerhalb eines Jahres", "Mehr als ein Jahr später"]
    consequence_ratings = ["Sehr positiv", "Positiv", "Neutral", "Negativ", "Sehr negativ"]
    long_term_impacts = ["Ja", "Nein", "Unsicher"]
    similar_decisions = ["Ja", "Nein"]
    similar_outcomes = ["Ja", "Nein", "Teilweise"]
    noticed_patterns = ["Bestimmte Entscheidungen führen immer zu positiven Folgen", "Bestimmte Entscheidungen führen immer zu negativen Folgen", "Die Folgen sind unvorhersehbar", "Andere"]

    data = []
    for _ in range(100):
        data.append(( 
            random_choice(ages),
            random_choice(genders),
            random_choice(educations),
            random_choice(decision_descriptions),
            random_choice(decision_types),
            random_choice(decision_ratings),
            random_choice(influencing_factors),
            random_choice(consequences),
            random_choice(time_to_consequences),
            random_choice(consequence_ratings),
            random_choice(long_term_impacts),
            random_choice(similar_decisions),
            random_choice(similar_outcomes),
            random_choice(noticed_patterns),
            ""
        ))
    return data

# Datensätze für vier Gruppen erstellen
data_group_1 = create_example_data()
data_group_2 = create_example_data()
data_group_3 = create_example_data()
data_group_4 = create_example_data()

# Datensätze in die Datenbank einfügen
c.executemany('''INSERT INTO survey_responses (age, gender, education, decision_description, decision_type,
                decision_rating, influencing_factors, consequences, time_to_consequences, consequence_rating,
                long_term_impact, similar_decisions, similar_outcomes, noticed_patterns, suggestions)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', data_group_1)

c.executemany('''INSERT INTO survey_responses (age, gender, education, decision_description, decision_type,
                decision_rating, influencing_factors, consequences, time_to_consequences, consequence_rating,
                long_term_impact, similar_decisions, similar_outcomes, noticed_patterns, suggestions)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', data_group_2)

c.executemany('''INSERT INTO survey_responses (age, gender, education, decision_description, decision_type,
                decision_rating, influencing_factors, consequences, time_to_consequences, consequence_rating,
                long_term_impact, similar_decisions, similar_outcomes, noticed_patterns, suggestions)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', data_group_3)

c.executemany('''INSERT INTO survey_responses (age, gender, education, decision_description, decision_type,
                decision_rating, influencing_factors, consequences, time_to_consequences, consequence_rating,
                long_term_impact, similar_decisions, similar_outcomes, noticed_patterns, suggestions)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', data_group_4)

conn.commit()
conn.close()

print("400 Beispieldatensätze wurden erfolgreich eingefügt.")
