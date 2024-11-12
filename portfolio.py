import faiss
import numpy as np
import pandas as pd
import uuid

class Portfolio:
    def __init__(self, file_path="app/resource/my_portfolio.csv"):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)

        # Create an FAISS index (Flat L2 distance search)
        self.index = faiss.IndexFlatL2(10)  # Adjust the dimension according to your embeddings

        # Dictionary to map IDs to metadata
        self.id_to_metadata = {}

    def load_portfolio(self):
        for _, row in self.data.iterrows():
            techstack_vector = self.vectorize(row["Techstack"])  # Assuming you have a vectorizer
            self.index.add(np.array([techstack_vector], dtype=np.float32))
            self.id_to_metadata[str(uuid.uuid4())] = {"links": row["Links"]}

    def vectorize(self, text):
        # Convert the tech stack text into a vector (this is a placeholder for actual vectorization logic)
        return np.random.rand(10)  # Assuming a 10-dimensional vector for now

    def query_links(self, skills):
        query_vector = self.vectorize(skills)
        D, I = self.index.search(np.array([query_vector]), 2)  # 2 is the number of nearest neighbors
        results = [self.id_to_metadata[str(i)] for i in I[0] if str(i) in self.id_to_metadata]
        return results


