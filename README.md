# Zufall-oder-Bestimmung
# Survey Response Prediction

Dieses Projekt zielt darauf ab, ein Machine-Learning-Modell zu trainieren, das basierend auf Umfragedaten zukünftige Konsequenzen von Entscheidungen vorhersagt. Die Implementierung umfasst mehrere Python-Skripte zur Verwaltung der Daten, dem Training des Modells und zur Durchführung von Vorhersagen.

## Inhaltsverzeichnis
- [Überblick](#überblick)
- [Voraussetzungen](#voraussetzungen)
- [Installation](#installation)
- [Datenbank und Initialtraining](#datenbank-und-initialtraining)
- [Hinzufügen von Datensätzen](#hinzufügen-von-datensätzen)
- [Training in Schritten](#training-in-schritten)
- [Vorhersage von zukünftigen Ereignissen](#vorhersage-von-zukünftigen-ereignissen)
- [Erstellen der Datenbank und CSV-Daten](#erstellen-der-datenbank-und-csv-daten)
- [Ausführen](#ausführen)
- [Lizenz](#lizenz)

## Überblick
Das Projekt besteht aus mehreren Skripten, die zusammenarbeiten, um eine SQLite-Datenbank mit Umfragedaten zu erstellen, diese Daten zu nutzen, um ein Random Forest-Modell zu trainieren und schließlich Vorhersagen über zukünftige Ereignisse basierend auf neuen Eingabedaten zu treffen.

## Voraussetzungen
- Python 3.12
- Bibliotheken: pandas, scikit-learn, joblib, tkinter, sqlite3

## Installation
1. Klone das Repository:
    ```bash
    git clone <repository-url>
    ```
2. Wechsle in das Projektverzeichnis:
    ```bash
    cd <project-directory>
    ```
3. Installiere die benötigten Bibliotheken:
    ```bash
    pip install -r requirements.txt
    ```

## Datenbank und Initialtraining
Das Skript `main.py` erstellt die SQLite-Datenbank `survey.db` und führt das initiale Training des Modells durch.

- **Erstellen der Datenbank und Tabelle**:
    ```python
    conn = sqlite3.connect('survey.db')
    c = conn.cursor()
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
    ```

- **Initialtraining des Modells**:
    Das Modell wird mit den vorhandenen Daten in der Datenbank trainiert. Die besten Hyperparameter werden mittels GridSearchCV ermittelt.

## Hinzufügen von Datensätzen
Das Skript `database_insertes.py` fügt neue Datensätze in die SQLite-Datenbank `survey.db` ein.

- **Einfügen von Daten**:
    ```python
    def insert_data_from_csv_to_db(csv_file, db_conn):
        df = pd.read_csv(csv_file)
        if df.empty:
            return False

        new_data = df.iloc[:25]
        remaining_data = df.iloc[25:]
        new_data.to_sql('survey_responses', db_conn, if_exists='append', index=False)
        remaining_data.to_csv(csv_file, index=False)
        return True
    ```

## Training in Schritten
Das Skript `training_mit_csv.py` führt das Training in festlegbaren Schritten durch. Es werden jeweils 25 Datensätze aus der CSV-Datei in die Datenbank eingetragen und danach ein Training durchgeführt.

- **Iteratives Training**:
    ```python
    while True:
        conn = sqlite3.connect('survey.db')
        success = insert_data_from_csv_to_db(csv_file, conn)
        conn.close()

        if not success:
            print("Keine Daten mehr in der CSV-Datei.")
            break

        train_model()
        print("Modell wurde neu trainiert.")
    ```

## Vorhersage von zukünftigen Ereignissen
Das Skript `Vorhersage.py` erstellt Vorhersagen basierend auf zukünftigen Entscheidungen, die in der GUI eingegeben werden.

- **GUI-Anwendung**:
    Eine tkinter-basierte GUI ermöglicht die Eingabe von zukünftigen Entscheidungen und zeigt die Vorhersagen der Konsequenzen an.
    ```python
    class SurveyApp:
        def __init__(self, root):
            self.root = root
            self.root.title("Survey Form")
            self.root.geometry("450x450")
            ...
        def future_analyze(self):
            ...
            future_person_df = pd.DataFrame([future_person_encoded], columns=self.columns)
            prediction = self.model.predict(future_person_df)
            predicted_consequence = self.label_encoders['consequence_rating'].inverse_transform(prediction)
            result = f'Vorhergesagte Konsequenz: {predicted_consequence[0]}'
            messagebox.showinfo("Zukunftsanalyse", result)
    ```

## Erstellen der Datenbank und CSV-Daten
Das Skript `Datensätze_zu_csv.py` generiert zufällige Datensätze und speichert sie in einer CSV-Datei.

- **Generierung von Zufallsdaten**:
    ```python
    def generate_random_record():
        return [
            random.choice(age_values),
            random.choice(gender_values),
            random.choice(education_values),
            ...
        ]

    records = [generate_random_record() for _ in range(10000)]
    ```

- **Speichern in CSV**:
    ```python
    with open('random_survey_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(columns)
        writer.writerows(records)
    ```

## Ausführen
1. Führen Sie `main.py` aus, um die Datenbank zu erstellen und das initiale Training durchzuführen:
    ```bash
    python main.py
    ```

2. Verwenden Sie `Vorhersage.py`, um Vorhersagen über zukünftige Ereignisse zu treffen:
    ```bash
    python Vorhersage.py
    ```

3. Fügen Sie neue Daten mit `database_insertes.py` zur Datenbank hinzu und führen Sie das Training erneut durch:
    ```bash
    python database_insertes.py
    ```

4. Erstellen Sie eine CSV-Datei mit `Datensätze_zu_csv.py` und führen Sie `training_mit_csv.py` aus, um das Training in festlegbaren Schritten durchzuführen:
    ```bash
    python Datensätze_zu_csv.py
    python training_mit_csv.py
    ```

## Lizenz
Dieses Projekt ist lizenziert unter der MIT-Lizenz.


Stellen Sie sicher, dass die Verzeichnisstruktur wie folgt ist:

```python
- main.py
- Vorhersage.py
- database_insertes.py
- Datensätze_zu_csv.py
- training_mit_csv.py
- abfrageDatenbank_consequence_rating.py
- survey.db (falls bereits erstellt)
- random_survey_data.csv (falls bereits erstellt)
- README.md (dieses Dokument)
```


