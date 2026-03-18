from sentence_transformers import SentenceTransformer
import chromadb
from utils.parser import chunk_text
import uuid


class Embedder:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.client = chromadb.Client()
        self.collection = self.client.create_collection(
            name=f"resumes_{uuid.uuid4().hex[:8]}",
            metadata={"hnsw:space": "cosine"}
        )
        self.resume_map = {}  # chunk_id -> filename

    def add_resume(self, filename: str, text: str):
        """Chunk, embed, and store a resume in the vector DB."""
        chunks = chunk_text(text, chunk_size=400, overlap=50)
        if not chunks:
            return

        embeddings = self.model.encode(chunks).tolist()
        ids = [f"{filename}__chunk_{i}" for i in range(len(chunks))]
        metadatas = [{"filename": filename, "chunk_index": i} for i in range(len(chunks))]

        self.collection.add(
            documents=chunks,
            embeddings=embeddings,
            ids=ids,
            metadatas=metadatas
        )

        for id_ in ids:
            self.resume_map[id_] = filename

    def find_matches(self, jd_text: str, top_k: int = 3) -> list[tuple[str, float]]:
        """Find top-k resumes most similar to the job description."""
        jd_embedding = self.model.encode([jd_text]).tolist()

        # Query more results to aggregate by filename
        n_results = min(self.collection.count(), max(top_k * 10, 30))
        if n_results == 0:
            return []

        results = self.collection.query(
            query_embeddings=jd_embedding,
            n_results=n_results,
            include=["metadatas", "distances"]
        )

        # Aggregate scores per filename (take best chunk score per resume)
        filename_scores: dict[str, float] = {}
        for meta, distance in zip(results["metadatas"][0], results["distances"][0]):
            filename = meta["filename"]
            similarity = 1 - distance  # cosine distance -> similarity
            if filename not in filename_scores or similarity > filename_scores[filename]:
                filename_scores[filename] = similarity

        # Sort by score descending
        sorted_matches = sorted(filename_scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_matches[:top_k]
