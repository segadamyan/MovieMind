import faiss
import numpy as np


class FAISSIndex:
    def __init__(self, dimension, index_file="faiss_index.bin"):
        self.dimension = dimension
        self.index_file = index_file
        index = faiss.IndexFlatL2(self.dimension)
        self.index = faiss.IndexIDMap(index) 

    def _initialize_index(self):
        """
        Initializes a FAISS index, either by loading an existing one or creating a new one.
        """
        try:
            print("Attempting to load existing index...")
            return faiss.read_index(self.index_file)
        except Exception as e:
            print(f"Failed to load index: {e}. Creating a new one.")
            return faiss.IndexFlatL2(self.dimension)

    def add_vectors(self, vectors, custom_ids=None):
        """
        Adds vectors and stores corresponding movie data.
        :param vectors: List or numpy array of vectors to add.
        :param movies: List of movie data (e.g., dicts) corresponding to vectors.
        :param custom_ids: List or numpy array of custom IDs.
        """
        if isinstance(vectors, list):
            vectors = np.array(vectors).astype('float32')
        
        if custom_ids is None:
            custom_ids = np.arange(self.index.ntotal, self.index.ntotal + len(vectors))

        if isinstance(custom_ids, list):
            custom_ids = np.array(custom_ids, dtype=np.int64)

        if custom_ids.shape[0] != vectors.shape[0]:
            raise ValueError("The number of custom IDs must match the number of vectors.")

        self.index.add_with_ids(vectors, custom_ids)

    def search_vectors(self, query_vector, k=5):
        """
        Searches for the k nearest neighbors to the query vector.
        :param query_vector: A single vector to search.
        :param k: Number of nearest neighbors to return.
        :return: Distances and indices of nearest neighbors.
        """
        if isinstance(query_vector, list):
            query_vector = np.array([query_vector]).astype('float32')
        distances, indices = self.index.search(query_vector, k)
        return distances, indices

    def save_index(self):
        """
        Saves the index to disk.
        """
        faiss.write_index(self.index, self.index_file)
        print(f"Index saved to {self.index_file}.")

    def get_total_vectors(self):
        """
        Returns the total number of vectors in the index.
        """
        return self.index.ntotal

    def load_index(self):
        """
        Reloads the index from disk.
        """
        self.index = faiss.read_index(self.index_file)
        print(f"Index loaded from {self.index_file}.")
