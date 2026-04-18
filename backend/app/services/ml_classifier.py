import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import make_pipeline

class SymptomClassifier:
    def __init__(self):
        self.model = None
        self._load_data()

    def _load_data(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.normpath(os.path.join(current_dir, "../../Symptom2Disease.csv"))
        try:
            df = pd.read_csv(csv_path)
            # Remove any leading white spaces in columns
            df.columns = [col.strip() for col in df.columns]
            
            if "label" in df.columns and "text" in df.columns:
                X = df["text"]
                y = df["label"]
                # Create a simple, fast, and highly effective text classifier
                self.model = make_pipeline(TfidfVectorizer(stop_words='english'), LinearSVC(random_state=42, dual='auto'))
                self.model.fit(X, y)
                print("TriageX ML Model loaded and trained from Symptom2Disease.csv")
        except Exception as e:
            print("ML Model Error:", e)

    def predict(self, text: str) -> str:
        if not self.model:
            return None
        return self.model.predict([text])[0]

ml_classifier = SymptomClassifier()
