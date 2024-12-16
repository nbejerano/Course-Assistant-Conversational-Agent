# A Pedagogical Conversational Agent for Stanford CS 106B Online Lectures

## Project Description
I developed a chatbot for Stanford’s Data Structures and Algorithms (CS 106B) course designed to support both instructors and students. The chatbot functions as a virtual assistant by providing relevant information and personalized assistance for course lectures.

### Key Features
- **Answer Specific Questions:** References specific lectures and timestamps.
- **Summarize Lectures:** Provides concise summaries of parts or entire lectures.
- **Provide Examples:** Delivers examples of concepts discussed in lectures.
- **Retrieve Code:** Retrieves relevant code snippets from lectures.
- **Recommend Resources:** Suggests additional helpful materials.

## Table of Contents
- **Course Transcript JSON File:** Contains all course transcript information organized into a JSON format (not included due to confidentiality constraints).
- **Poster Presentation.pdf:** An overview of the project, including technical implementation, testing, and results.

## How to Run the Chatbot
1. **Set Up API Key:**
   ```bash
   export TOGETHER_API_KEY="<your_api_key>"
   ```

2. **Install Dependencies:**
   ```bash
   pip install streamlit
   ```

3. **Run the Chatbot:**
   ```bash
   streamlit run 3.0.py
   ```

   - This will open the Streamlit interface in your web browser.
   - Enter your queries into the chatbot interface.
   - Note: The Streamlit interface may take a moment to load responses.

### Example Questions to Ask:
- What is a linked list?
- When should I use recursion?
- What is an example of recursive backtracking from the lecture?
- Summarize the first 5 minutes of lecture 4.
- What is the professor talking about between minutes 30-35 of lecture 7?
