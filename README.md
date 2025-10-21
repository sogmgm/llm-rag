# LLM LangChain & LangGraph Practice and Some RAG

## Project Overview
This project focuses on practicing various LLM (Large Language Model)-related tasks using LangChain and LangGraph, while also learning the Retrieval-Augmented Generation (RAG) technique.

## Directory Structure
### langchain_langraph/
- `prac/`: Directory containing practice code and notebook files for LangChain and LangGraph basics.
- `faiss_index/` and `faiss_index_jupyter/`: Directories where FAISS index files are stored.
- `requirements_mac.txt` and `lang_requirements.txt`: Files defining the Python package requirements for running the project.

### RAG/
- `RAG_general/`: Advanced RAG implementations including Multi-Turn RAG, Adaptive RAG, Human-in-the-Loop, and Agentic RAG.
- `RAG_multimodal/`: Multimodal RAG implementations for audio, image, and GraphRAG.
- `RAG_judge/`: RAG evaluation using RAGAS framework.

## Key Practice Topics
### Basic LangChain & LangGraph (langchain_langraph/prac/)
1. **Using Hugging Face**: Basic usage of LLMs with the Hugging Face library.
2. **Getting Started with LangChain**: Overview and basic usage of LangChain.
3. **Model**: Understanding and working with LLM models.
4. **Output Parser**: Methods for parsing model outputs.
5. **Prompt Memory**: Utilizing prompt memory effectively.
6. **Introduction to RAG**: Basic concepts of Retrieval-Augmented Generation.
7. **LCEL and Runnable**: LangChain Expression Language and Runnable interfaces.
8. **Introduction to LangGraph**: Graph-based workflows using LangGraph.
9. **Agents**: Automating tasks with LangChain agents.
10. **Spam Filter**: Building spam filter applications.

### Advanced RAG (RAG/RAG_general/)
1. **Multi-Turn RAG and Memory Management**: Implementing conversational RAG with memory.
2. **Adaptive & Iterative RAG**: Advanced RAG techniques for improved accuracy.
3. **Human-in-the-Loop**: Interactive RAG systems with human feedback.
4. **Advanced Agentic RAG**: Combining agents with RAG for complex tasks.
5. **DB Conversational Search Agent**: Building database query agents with natural language.
6. **Generation Model Evaluation Metrics**: BLEU, ROUGE, and BERT-based metrics.

### Multimodal RAG (RAG/RAG_multimodal/)
1. **Multimodal Audio RAG**: Processing and retrieving audio data.
2. **Multimodal Image RAG**: Image-based retrieval and generation.
3. **GraphRAG**: Knowledge graph-based RAG implementation.

### RAG Evaluation (RAG/RAG_judge/)
1. **RAGAS Evaluation**: Evaluating RAG systems using RAGAS framework.

## Environment Setup(recommend)
It is recommended to set up the virtual environment locally using `uv` and the `lang_requirements.txt` file.