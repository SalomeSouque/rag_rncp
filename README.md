# RAG RNCP — Assistant pédagogique Dev IA

## Description
Outil conversationnel permettant d'analyser un projet étudiant et d'identifier 
les compétences du référentiel RNCP Dev IA qu'il couvre. L'utilisateur décrit 
son projet en langage naturel et reçoit une analyse structurée des compétences 
validées, partiellement couvertes et manquantes.

## Architecture
Le projet repose sur une architecture RAG (Retrieval Augmented Generation) :
PDF Référentiel RNCP
↓ Chargement + Découpage (chunks)
↓ Embeddings (qwen3-embedding:0.6b)
↓ Stockage FAISS
↓
Question utilisateur → Vectorisation → Similarité FAISS
↓
Prompt enrichi (chunks + question) → qwen3:4b → Réponse structurée

## Stack technique
- **LangChain** — orchestration du pipeline RAG
- **Ollama** — serveur LLM local (qwen3:4b + qwen3-embedding:0.6b)
- **FAISS** — base vectorielle locale
- **Chainlit** — interface conversationnelle
- **uv** — gestionnaire de projet Python
- **Docker** — conteneurisation

## Installation

### Prérequis
- Docker et Docker Compose installés
- Git

### Lancement
```bash
# Cloner le repo
git clone https://github.com/TON_USERNAME/rag-rncp.git
cd rag-rncp

# Lancer les services
docker compose up -d

# Télécharger les modèles (première fois uniquement)
docker exec -it ollama ollama pull qwen3:4b
docker exec -it ollama ollama pull qwen3-embedding:0.6b

# Lancer l'ingestion du référentiel
docker exec -it rag-rncp uv run python -c "import sys; sys.path.insert(0, 'src'); from ingestion import ingest; ingest()"
```

### Accès
Ouvre `http://localhost:8000` dans ton navigateur.

## Usage

Décris ton projet dans la zone de texte. Exemples de questions :

- "Mon projet déploie une API FastAPI avec Docker et un pipeline GitHub Actions. Quelles compétences RNCP couvre-t-il ?"
- "La compétence C13 est-elle validée si j'ai seulement un Dockerfile sans CI/CD ?"
- "Quelles compétences me manquent pour valider le bloc MLOps ?"

## Variables d'environnement

Crée un fichier `.env` à la racine :

```bash
OLLAMA_MODEL=qwen3:4b
EMBEDDING_MODEL=qwen3-embedding:0.6b
OLLAMA_HOST=http://ollama:11434
```