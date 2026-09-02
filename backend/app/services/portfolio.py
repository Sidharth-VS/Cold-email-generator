import chromadb
import uuid

class Portfolio:
    def __init__(self):
        self.chroma_client = chromadb.PersistentClient('vectorstore')
        self.collection = self.chroma_client.get_or_create_collection('portfolio')

    def store(self, tech_stack, link, user_id):
        doc_ids = [str(uuid.uuid4()) for _ in tech_stack.split(",")]
        self.collection.add(
            documents=tech_stack.split(","),
            metadatas=[{"links": link.strip(), "user_id": str(user_id)} for _ in tech_stack.split(",")],
            ids=doc_ids,
        )
        return doc_ids

    def query(self, skills, user_id):
        if not skills:
            return []
        results = self.collection.query(query_texts=skills, n_results=2)
        metadatas = results.get('metadatas', [])
        filtered = []
        for group in metadatas:
            for meta in (group or []):
                if meta.get("user_id") == str(user_id):
                    filtered.append(meta)
        return [filtered] if filtered else []

    def delete(self, chromadb_ids):
        if chromadb_ids:
            self.collection.delete(ids=chromadb_ids)            
            