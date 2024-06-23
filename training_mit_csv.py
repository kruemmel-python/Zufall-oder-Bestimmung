import sqlite3
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report
import joblib

# Funktion zum Einfügen von 25 Datensätzen in die Datenbank
def insert_data_from_csv_to_db(csv_file, db_conn):
    df = pd.read_csv(csv_file)
    if df.empty:
        return False  # Keine Daten mehr in der CSV-Datei

    # Nimm die ersten 25 Datensätze
    new_data = df.iloc[:25]
    remaining_data = df.iloc[25:]

    # Einfügen in die Datenbank
    new_data.to_sql('survey_responses', db_conn, if_exists='append', index=False)

    # Verbleibende Daten zurück in die CSV-Datei schreiben
    remaining_data.to_csv(csv_file, index=False)

    return True

# Funktion zum Trainieren des Modells
def train_model():
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

    # Feature Engineering: Neue Features erstellen
    df['age_gender_interaction'] = df['age'] * df['gender']
    df['education_decision_interaction'] = df['education'] * df['decision_type']
    df['rating_interaction'] = df['decision_rating'] * df['consequence_rating']

    # Features und Zielvariable definieren
    X = df.drop('consequence_rating', axis=1)  # Unabhängige Variablen
    y = df['consequence_rating']  # Zielvariable

    # Daten in Trainings- und Testdaten aufteilen
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Feature Scaling
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Hyperparameter-Tuning mit GridSearchCV
    param_grid = {
        'n_estimators': [100, 200],
        'max_depth': [10, 20, 30],
        'min_samples_split': [2, 5],
        'min_samples_leaf': [1, 2]
    }

    # GridSearchCV verwenden, um die besten Hyperparameter zu finden
    clf = GridSearchCV(RandomForestClassifier(random_state=42), param_grid, cv=3, n_jobs=-1, verbose=2)
    clf.fit(X_train, y_train)

    # Beste Hyperparameter anzeigen
    print("Beste Hyperparameter: ", clf.best_params_)

    # Modell mit den besten Hyperparametern trainieren
    best_clf = clf.best_estimator_
    best_clf.fit(X_train, y_train)

    # Vorhersagen treffen und Leistung des Modells bewerten
    y_pred = best_clf.predict(X_test)
    print(classification_report(y_test, y_pred))

    # Modell und Scaler speichern
    joblib.dump(best_clf, 'trained_model.pkl')
    joblib.dump(scaler, 'scaler.pkl')

    # Verbindung schließen
    conn.close()

# Hauptprozess
csv_file = 'random_survey_data.csv'

while True:
    # Versuche, 25 Datensätze aus der CSV in die Datenbank zu inserieren
    conn = sqlite3.connect('survey.db')
    success = insert_data_from_csv_to_db(csv_file, conn)
    conn.close()

    if not success:
        print("Keine Daten mehr in der CSV-Datei.")
        break

    # Trainiere das Modell mit den neuen Daten
    train_model()
    print("Modell wurde neu trainiert.")
