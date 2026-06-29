# Agentic Disaster Response Platform

A multi-agent system built with **Google's Agent Development Kit (ADK)** for coordinated disaster response. The platform is architected as three specialized, interconnected systems that enable end-to-end logistics management, public support, and human supervision.

## 🚀 Getting Started

1. Clone the repository
2. Install dependencies:
 ```bash
   uv sync
   ```
4. Configure environment variables (Firebase credentials, API keys)
  ```env
    GOOGLE_API_KEY=your-gemini-api-key-here
    GROQ_API_KEY=your-groq-api-key-here
  ```
5. Run the three systems in separate terminals:
   - System 1:
     ```bash
      uvicorn system1_manager.main:app --host 127.0.0.1 --port 8000 
     ```
   - System 2:
     ```bash
      uvicorn system2_support.main:app --host 0.0.0.0 --port 8001
     ```
   - System 3:
      ```bash
      uvicorn system3_supervisor.main:app --host 0.0.0.0 --port 8002
      ```


---

Built as a demonstration of agentic AI systems for critical real-world applications.

Contributions are welcome!
