import tkinter as tk
from tkinter import messagebox
import sqlite3
import joblib
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import os

# Verbindung zur SQLite-Datenbank herstellen
conn = sqlite3.connect('survey.db')
query = "SELECT * FROM survey_responses"
df = pd.read_sql_query(query, conn)

# 'id' Spalte entfernen
df = df.drop(columns=['id'], errors='ignore')

# Label Encoding für alle Spalten
label_encoders = {}
for column in df.columns:
    le = LabelEncoder()
    df[column] = le.fit_transform(df[column].astype(str))
    label_encoders[column] = le

# Features und Zielvariable definieren
X = df.drop('consequence_rating', axis=1)  # Unabhängige Variablen
y = df['consequence_rating']  # Zielvariable

# Modell und Scaler laden
clf = joblib.load('trained_model.pkl')
scaler = joblib.load('scaler.pkl')

# GUI-Anwendung
class SurveyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Zukunftsprognose Formular")
        self.root.geometry("450x600")

        # Canvas und Scrollbar erstellen
        self.canvas = tk.Canvas(root, borderwidth=0, background="#ffffff")
        self.frame = tk.Frame(self.canvas, background="#ffffff")
        self.vsb = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4, 4), window=self.frame, anchor="nw", tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)

        self.create_widgets()

    def create_widgets(self):
        self.future_fields = {
            "age": ("Alter:", ["Unter 18", "18-24", "25-34", "35-44", "45-54", "55-64", "65 oder älter"]),
            "gender": ("Geschlecht:", ["Männlich", "Weiblich", "Divers"]),
            "education": ("Bildungsniveau:", ["Kein Abschluss", "Hauptschulabschluss", "Realschulabschluss", "Abitur", "Berufsausbildung", "Bachelor-Abschluss", "Master-Abschluss", "Promotion", "Andere"]),
            "decision_description": ("Beschreiben Sie eine zukünftige Entscheidung:", ["Arbeitsplatzwechsel", "Umzug in eine andere Stadt", "Beginn oder Ende einer Beziehung", "Größere finanzielle Investition", "Gesundheitsbezogene Entscheidung", "Andere"]),
            "decision_type": ("Art der zukünftigen Entscheidung:", ["Beruflich", "Persönlich", "Finanziell", "Gesundheitlich", "Zwischenmenschlich", "Andere"]),
            "decision_rating": ("Bewertung der zukünftigen Entscheidung:", ["Sehr gut", "Gut", "Neutral", "Schlecht", "Sehr schlecht"]),
            "influencing_factors": ("Einflussfaktoren für die zukünftige Entscheidung:", ["Ratschläge von Freunden/Familie", "Eigene Erfahrungen", "Expertenmeinungen", "Online-Recherche", "Bauchgefühl", "Andere"]),
            "consequences": ("Erwartete direkte Folgen der Entscheidung:", ["Positive berufliche Entwicklung", "Negative berufliche Entwicklung", "Verbesserte finanzielle Situation", "Verschlechterte finanzielle Situation", "Verbesserte zwischenmenschliche Beziehungen", "Verschlechterte zwischenmenschliche Beziehungen", "Verbesserte Gesundheit", "Verschlechterte Gesundheit", "Andere"]),
            "time_to_consequences": ("Zeit bis zu den Folgen:", ["Sofort", "Innerhalb eines Tages", "Innerhalb einer Woche", "Innerhalb eines Monats", "Innerhalb eines Jahres", "Mehr als ein Jahr später"]),
            "long_term_impact": ("Langfristige Auswirkungen:", ["Ja", "Nein", "Unsicher"]),
            "similar_decisions": ("Ähnliche Entscheidungen in der Vergangenheit:", ["Ja", "Nein"]),
            "similar_outcomes": ("Ähnliche Folgen:", ["Ja", "Nein", "Teilweise"]),
            "noticed_patterns": ("Bemerkte Muster:", ["Bestimmte Entscheidungen führen immer zu positiven Folgen", "Bestimmte Entscheidungen führen immer zu negativen Folgen", "Die Folgen sind unvorhersehbar", "Andere"]),
            "suggestions": ("Vorschläge oder Anmerkungen:", ["Keine"])
        }

        self.entries = {}
        for key, (label_text, options) in self.future_fields.items():
            self.add_label(self.frame, label_text)
            if options:
                var = tk.StringVar(value=options[0])
                self.entries[key] = var
                self.add_options(self.frame, var, options)
            else:
                var = tk.StringVar()
                self.entries[key] = var
                self.add_entry(self.frame, var)

        # Buttons
        future_analyze_button = tk.Button(self.frame, text="Zukunftsanalyse", command=self.future_analyze)
        future_analyze_button.pack(pady=10)

    def add_label(self, parent, text):
        label = tk.Label(parent, text=text)
        label.pack(pady=5)

    def add_entry(self, parent, var):
        entry = tk.Entry(parent, textvariable=var, width=50)
        entry.pack(pady=5)

    def add_options(self, parent, var, options):
        dropdown = tk.OptionMenu(parent, var, *options)
        dropdown.pack(pady=5)

    def future_analyze(self):
        future_data = {key: self.entries[key].get() for key in self.entries}
        future_person_encoded = []
        for column in X.columns:
            if column in future_data:
                future_person_encoded.append(label_encoders[column].transform([future_data[column]])[0])
            else:
                future_person_encoded.append(0)

        # Feature Engineering
        future_person_df = pd.DataFrame([future_person_encoded], columns=X.columns)
        future_person_df['age_gender_interaction'] = future_person_df['age'] * future_person_df['gender']
        future_person_df['education_decision_interaction'] = future_person_df['education'] * future_person_df['decision_type']
        # Entfernen der Interaktion mit consequence_rating
        future_person_df['rating_interaction'] = future_person_df['decision_rating'] * future_person_df['education']  # Beispiel für eine andere Interaktion

        # Feature Scaling
        future_person_df_scaled = scaler.transform(future_person_df)

        # Vorhersage treffen
        prediction = clf.predict(future_person_df_scaled)
        predicted_consequence = label_encoders['consequence_rating'].inverse_transform(prediction)
        result = f'Vorhergesagte Konsequenz: {predicted_consequence[0]}'

        # Begründung
        reason = f'Die Entscheidung basiert auf den eingegebenen Daten: {future_data} und dem trainierten Modell.'
        messagebox.showinfo("Zukunftsanalyse", f"{result}\n\nBegründung:\n{reason}")

    def onFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

if __name__ == "__main__":
    root = tk.Tk()
    app = SurveyApp(root)
    root.mainloop()

    # Verbindung zur Datenbank schließen
    conn.close()
