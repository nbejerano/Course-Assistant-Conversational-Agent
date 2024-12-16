Project title:
 A Pedagogical Conversational Agent for Stanford CS 106B Online Lectures

 
Project desrciption:
  I built a chatbot for Stanford’s Data Structures
  and Algorithms (CS 106B) course that seeks to at-
  tain the performance, style, and usefulness needed
  by both instructors and students. The chatbot serves
  as a virtual assistant in providing information and
  advice relevant to any of the course lectures. Specif-
  ically, it serves the following key capabilities:
  • Answer specific questions, referencing the correct lectures (and timestamps);
  • Succinctly summarize or restate parts of or entire lectures;
  • Provide examples of concepts mentioned in lecture;
  • Retrieve the correct code;
  • Recommend other useful resources.

Table of Contents:
   JSON file of course trasncript with metadata - this file contains all of the CS106B course transcript information organized into a JSON file to
     - Not included due to confidentiality constraints
  Poster Presentation.pdf - this file contains an overview of the project as a whole along with technical implementation, testing, and results

How to run chatbot: 
    1. In the terminal run the line: export TOGETHER_API_KEY = "" 
      - fill in with your API key 
    2. The chatbot is hosted on streamlit which needs to be installed run in the terminal: pip install stremalit 
    3. Once all dependencies have been installed run: streamlit run 3.0.py 
      - this will open the streamlit interface in the browser 
      - from the browser type in your queries to the chatbot to see responses 
      - the streamlit interface does tend to be slow and can take a minute to load a response 
      - example questions to ask: 
        - what is a linked list? - when should I use recursion? 
        - what is an example of recursvie bracktracking from the lecture? 
        - summarize the first 5 minutes of lecture 4? 
        - what is the professor talking about in minute 30-35 of lecture 7?
