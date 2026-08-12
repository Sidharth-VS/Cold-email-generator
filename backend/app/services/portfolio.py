import chromadb
import uuid

class Portfolio:
    def __init__(self):
        self.chroma_client = chromadb.PersistentClient('vectorstore')
        self.collection = self.chroma_client.get_or_create_collection('portfolio')

    def store(self, tech_stack, link):
            self.collection.add(documents=tech_stack,
                                metadatas={"links":link},
                                ids=[str(uuid.uuid4())])
            
    def query(self, skills):
         return self.collection.query(query_texts=skills, n_results=2).get('metadatas', [])            
            