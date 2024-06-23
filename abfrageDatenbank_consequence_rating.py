import sqlite3
import pandas as pd

# Verbindung zur SQLite-Datenbank herstellen
conn = sqlite3.connect('survey.db')
query = "SELECT consequence_rating FROM survey_responses"
df = pd.read_sql_query(query, conn)

# Verteilung der Konsequenzbewertungen anzeigen
print(df['consequence_rating'].value_counts())

# Verbindung schließen
conn.close()
