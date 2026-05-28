from pathlib import Path
import pickle

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

DATA_PATH = Path(__file__).with_name("mtsamples.csv")
MODEL_PATH = Path(__file__).with_name("model.pkl")
VECTORIZER_PATH = Path(__file__).with_name("vectorizer.pkl")
ENCODER_PATH = Path(__file__).with_name("encoder.pkl")

SELECTED = [
    " Cardiovascular / Pulmonary",
    " Orthopedic",
    " Gastroenterology",
    " Neurology",
    " Urology",
    " Obstetrics / Gynecology",
    " ENT - Otolaryngology",
    " Neurosurgery",
    " Hematology - Oncology",
    " Ophthalmology",
    " Nephrology",
]


def load_data():
    df = pd.read_csv(DATA_PATH)
    df = df[["transcription", "medical_specialty"]].dropna()
    df = df[df["medical_specialty"].isin(SELECTED)]

    balanced_df = []
    for specialty in SELECTED:
        subset = df[df["medical_specialty"] == specialty]
        if subset.empty:
            continue
        sample_size = min(80, len(subset))
        balanced_df.append(subset.sample(sample_size, random_state=42))

    if not balanced_df:
        raise ValueError("No data available after filtering specialties.")

    return pd.concat(balanced_df, ignore_index=True)


def train_and_save():
    balanced_df = load_data()

    encoder = LabelEncoder()
    y = encoder.fit_transform(balanced_df["medical_specialty"])
    X = balanced_df["transcription"]

    vectorizer = TfidfVectorizer(stop_words="english", max_features=10000)
    X_vec = vectorizer.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X_vec,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    model = LogisticRegression(max_iter=2000)
    model.fit(X_train, y_train)
    _ = model.score(X_test, y_test)

    with open(MODEL_PATH, "wb") as file:
        pickle.dump(model, file)

    with open(VECTORIZER_PATH, "wb") as file:
        pickle.dump(vectorizer, file)

    with open(ENCODER_PATH, "wb") as file:
        pickle.dump(encoder, file)


if __name__ == "__main__":
    train_and_save()
    print("Saved model.pkl, vectorizer.pkl, encoder.pkl")
