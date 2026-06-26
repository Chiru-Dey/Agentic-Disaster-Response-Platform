# Agentic Disaster Response Platform

A multi-agent system built with **Google's Agent Development Kit (ADK)** for coordinated disaster response. The platform is architected as three specialized, interconnected systems that enable end-to-end logistics management, public support, and human supervision.

## 🚀 Getting Started

1. Clone the repository
2. Install dependencies:
 ```bash
   pip install -r requirements.txt
   ```
4. Configure environment variables (Firebase credentials, API keys)
5. Run the three systems in separate terminals:
   - System 1:
     ```bash
      cd system1_manager && uvicorn main:app --reload
     ```
   - System 2:
     ```bash
     cd system2_support && python main.py
     ```
   - System 3:
      ```bash
      cd system3_supervisor && python main.py
      ```


---

Built as a demonstration of agentic AI systems for critical real-world applications.

Contributions are welcome!
