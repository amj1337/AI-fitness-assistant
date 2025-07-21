from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferWindowMemory
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA

class FitnessAssistant:
    def __init__(self):
        # Initialize the Ollama LLM
        self.llm = Ollama(
            base_url="http://localhost:11434",
            model="fitgpt", #model name
            temperature=0.7,
            num_gpu=1,  # Match your Modelfile setting
            num_thread=6
        )
        
        # Conversation memory
        self.memory = ConversationBufferWindowMemory(
            k=5,
            memory_key="chat_history",
            return_messages=True
        )
        
        # Load fitness knowledge base
        self.vector_db = self._create_knowledge_base()
        
    def _create_knowledge_base(self):
        # Your fitness-specific documents
        fitness_docs = [
            "Progressive overload is key for muscle growth",
            "Aim for 1.6-2.2g protein per kg bodyweight daily",
            "Cardio should be 150 mins/week for general health",
            "Allow 48h recovery for worked muscle groups"
        ]
        
        embeddings = OllamaEmbeddings(
            model="fitgpt",
            base_url="http://localhost:11434"
        )
        
        return FAISS.from_texts(fitness_docs, embeddings)
    
    def generate_response(self, user_input: str, user_context: dict):
        # Create personalized prompt
        prompt = self._build_prompt(user_input, user_context)
        
        # Use retrieval for factual queries
        if self._needs_factual_response(user_input):
            return self._retrieval_response(user_input)
            
        # Standard conversational response
        response = self.llm.invoke(prompt)
        self.memory.save_context({"input": user_input}, {"output": response})
        return response
    
    def _build_prompt(self, user_input: str, user_context: dict):
        # Retrieve conversation history
        history = self.memory.load_memory_variables({})["chat_history"]
        
        return f"""
        [User Context]
        Goals: {user_context.get('goals', 'N/A')}
        Preferences: {user_context.get('preferences', 'N/A')}
        Last Progress: {user_context.get('last_progress', 'N/A')}
        
        [Conversation History]
        {history}
        
        [Current Query]
        {user_input}
        
        [Instructions]
        Provide personalized fitness advice considering the context and history.
        """
    
    def _needs_factual_response(self, query: str):
        factual_keywords = ["define", "what is", "explain", "how does"]
        return any(kw in query.lower() for kw in factual_keywords)
    
    def _retrieval_response(self, query: str):
        qa_chain = RetrievalQA.from_chain_type(
            self.llm,
            retriever=self.vector_db.as_retriever(),
            chain_type="stuff"
        )
        return qa_chain.invoke(query)["result"]