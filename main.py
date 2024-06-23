import tkinter as tk
from tkinter import messagebox
import sqlite3
import joblib
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import os

# Verbindung zur SQLite-Datenbank herstellen
conn = sqlite3.connect('survey.db')
c = conn.cursor()

# Tabelle erstellen, falls sie noch nicht existiert
c.execute('''CREATE TABLE IF NOT EXISTS survey_responses (
             id INTEGER PRIMARY KEY,
             age TEXT,
             gender TEXT,
             education TEXT,
             decision_description TEXT,
             decision_type TEXT,
             decision_rating TEXT,
             influencing_factors TEXT,
             consequences TEXT,
             time_to_consequences TEXT,
             consequence_rating TEXT,
             long_term_impact TEXT,
             similar_decisions TEXT,
             similar_outcomes TEXT,
             noticed_patterns TEXT,
             suggestions TEXT)''')

conn.commit()

# GUI-Anwendung
class SurveyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Survey Form")
        self.root.geometry("450x450")

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
        self.load_or_initialize_model()

    def create_widgets(self):
        self.fields = {
            "age": ("Alter:", ["Unter 18", "18-24", "25-34", "35-44", "45-54", "55-64", "65 oder älter"]),
            "gender": ("Geschlecht:", ["Männlich", "Weiblich", "Divers"]),
            "education": ("Bildungsniveau:", ["Kein Abschluss", "Hauptschulabschluss", "Realschulabschluss", "Abitur", "Berufsausbildung", "Bachelor-Abschluss", "Master-Abschluss", "Promotion", "Andere"]),
            "decision_description": ("Beschreiben Sie eine wichtige Entscheidung:", ["Arbeitsplatzwechsel", "Umzug in eine andere Stadt", "Beginn oder Ende einer Beziehung", "Größere finanzielle Investition", "Gesundheitsbezogene Entscheidung", "Andere"]),
            "decision_type": ("Art der Entscheidung:", ["Beruflich", "Persönlich", "Finanzielle Natur", "Gesundheitlich", "Zwischenmenschlich", "Andere"]),
            "decision_rating": ("Bewertung der Entscheidung:", ["Sehr gut", "Gut", "Neutral", "Schlecht", "Sehr schlecht"]),
            "influencing_factors": ("Einflussfaktoren:", ["Ratschläge von Freunden/Familie", "Eigene Erfahrungen", "Expertenmeinungen", "Online-Recherche", "Bauchgefühl", "Andere"]),
            "consequences": ("Direkte Folgen der Entscheidung:", ["Positive berufliche Entwicklung", "Negative berufliche Entwicklung", "Verbesserte finanzielle Situation", "Verschlechterte finanzielle Situation", "Verbesserte zwischenmenschliche Beziehungen", "Verschlechterte zwischenmenschliche Beziehungen", "Verbesserte Gesundheit", "Verschlechterte Gesundheit", "Andere"]),
            "time_to_consequences": ("Zeit bis zu den Folgen:", ["Sofort", "Innerhalb eines Tages", "Innerhalb einer Woche", "Innerhalb eines Monats", "Innerhalb eines Jahres", "Mehr als ein Jahr später"]),
            "consequence_rating": ("Bewertung der Folgen:", ["Sehr positiv", "Positiv", "Neutral", "Negativ", "Sehr negativ"]),
            "long_term_impact": ("Langfristige Auswirkungen:", ["Ja", "Nein", "Unsicher"]),
            "similar_decisions": ("Ähnliche Entscheidungen in der Vergangenheit:", ["Ja", "Nein"]),
            "similar_outcomes": ("Ähnliche Folgen:", ["Ja", "Nein", "Teilweise"]),
            "noticed_patterns": ("Bemerkte Muster:", ["Bestimmte Entscheidungen führen immer zu positiven Folgen", "Bestimmte Entscheidungen führen immer zu negativen Folgen", "Die Folgen sind unvorhersehbar", "Andere"]),
            "suggestions": ("Vorschläge oder Anmerkungen:", [])
        }

        self.entries = {}
        for key, (label_text, options) in self.fields.items():
            self.add_label(label_text)
            if options:
                var = tk.StringVar(value=options[0])
                self.entries[key] = var
                self.add_options(var, options)
            else:
                var = tk.StringVar()
                self.entries[key] = var
                self.add_entry(var)

        # Buttons
        submit_button = tk.Button(self.frame, text="Absenden", command=self.submit)
        submit_button.pack(pady=10)

        train_button = tk.Button(self.frame, text="Modell trainieren", command=self.train_model_button)
        train_button.pack(pady=10)

        analyze_button = tk.Button(self.frame, text="Analyse und Ergebnisse", command=self.analyze)
        analyze_button.pack(pady=10)

        self.console = tk.Text(self.frame, height=10, state='disabled')
        self.console.pack(pady=10)

    def add_label(self, text):
        label = tk.Label(self.frame, text=text, background="#ffffff")
        label.pack(pady=5)

    def add_entry(self, var):
        entry = tk.Entry(self.frame, textvariable=var, width=50)
        entry.pack(pady=5)

    def add_options(self, var, options):
        dropdown = tk.OptionMenu(self.frame, var, *options)
        dropdown.pack(pady=5)

    def load_data(self):
        query = "SELECT age, gender, education, decision_description, decision_type, decision_rating, influencing_factors, consequences, time_to_consequences, consequence_rating, long_term_impact, similar_decisions, similar_outcomes, noticed_patterns, suggestions FROM survey_responses"
        df = pd.read_sql_query(query, conn)
        return df

    def encode_data(self):
        self.df = self.load_data()
        self.label_encoders = {}
        for column in self.df.columns:
            if column != 'suggestions':  # 'suggestions' nicht kodieren
                le = LabelEncoder()
                self.df[column] = le.fit_transform(self.df[column].astype(str))
                self.label_encoders[column] = le

    def train_model(self):
        self.encode_data()
        X = self.df.drop(['consequence_rating', 'suggestions'], axis=1)  # 'suggestions' nicht als Feature verwenden
        y = self.df['consequence_rating']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        self.clf = RandomForestClassifier(n_estimators=100, random_state=42)
        self.clf.fit(X_train, y_train)

        y_pred = self.clf.predict(X_test)
        report = classification_report(y_test, y_pred)
        self.update_console(report)

        # Modell speichern
        joblib.dump(self.clf, 'trained_model.pkl')

    def load_or_initialize_model(self):
        if os.path.exists('trained_model.pkl'):
            self.clf = joblib.load('trained_model.pkl')
        else:
            self.train_model()

    def update_console(self, text):
        self.console.config(state='normal')
        self.console.insert(tk.END, text + "\n")
        self.console.config(state='disabled')

    def train_model_button(self):
        self.train_model()
        messagebox.showinfo("Erfolg", "Das Modell wurde erfolgreich trainiert und gespeichert!")

    def submit(self):
        data = {key: self.entries[key].get() for key in self.entries}
        new_person_encoded = []
        for column in self.df.columns:
            if column not in ['consequence_rating', 'suggestions']:  # 'consequence_rating' und 'suggestions' nicht kodieren
                if column in self.label_encoders and data[column] in self.label_encoders[column].classes_:
                    new_person_encoded.append(self.label_encoders[column].transform([data[column]])[0])
                else:
                    new_person_encoded.append(0)

        prediction = self.clf.predict([new_person_encoded])
        predicted_consequence = self.label_encoders['consequence_rating'].inverse_transform(prediction)
        result = f'Vorhergesagte Konsequenz: {predicted_consequence[0]}'
        self.update_console(result)

        # Neuen Datensatz in die Datenbank einfügen
        c.execute('''INSERT INTO survey_responses (age, gender, education, decision_description, decision_type,
                            decision_rating, influencing_factors, consequences, time_to_consequences, consequence_rating,
                            long_term_impact, similar_decisions, similar_outcomes, noticed_patterns, suggestions)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                       tuple(new_person_encoded + [predicted_consequence[0]]))
        conn.commit()
        messagebox.showinfo("Erfolg", "Ihre Antworten wurden erfolgreich gespeichert!")

    def analyze(self):
        c.execute('''SELECT decision_rating, consequence_rating FROM survey_responses''')
        results = c.fetchall()

        good_decisions = len([r for r in results if r[0] in ['Sehr gut', 'Gut']])
        bad_decisions = len([r for r in results if r[0] in ['Schlecht', 'Sehr schlecht']])
        positive_outcomes = len([r for r in results if r[1] in ['Sehr positiv', 'Positiv']])
        negative_outcomes = len([r for r in results if r[1] in ['Negativ', 'Sehr negativ']])

        analysis_result = f'''
        Anzahl der guten Entscheidungen: {good_decisions}
        Anzahl der schlechten Entscheidungen: {bad_decisions}
        Anzahl der positiven Folgen: {positive_outcomes}
        Anzahl der negativen Folgen: {negative_outcomes}
        '''

        messagebox.showinfo("Analyseergebnis", analysis_result)

    def onFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

if __name__ == "__main__":
    root = tk.Tk()
    app = SurveyApp(root)
    root.mainloop()

    # Verbindung zur Datenbank schließen
    conn.close()
