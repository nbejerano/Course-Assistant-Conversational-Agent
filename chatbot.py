import streamlit as st
import os
import requests
from together import Together
import json

# Naama's API
# TOGETHER_API_KEY="75c411b240adddc12fedd8e3c4d6f4416e861e3dcc81ad19b466d7023341c38a"

# Liv's API
# TOGETHER_API_KEY="b4096c4e32bcda5955f05d961f44580fac7853a85dae56efbefe19856bccb2ab"


def parse_timestamp_question(question):
    """
    Uses a LLaMA call to determine if a question references a lecture and timestamp.
    Returns a list with lecture number and a tuple of start and end times in seconds.

    Args:
        question (str): The input question.

    Returns:
        list: [lecture_number, (start_time_in_seconds, end_time_in_seconds)] if valid timestamp is found.
        None: If no timestamp reference is detected.
    """
    client = Together()

    instructions = f"""
    Given the following question: "{question}"

    Identify if it references a lecture, a lecture and a specific timestamp, or neither.
    
    If it references both lecture and timestamp, return the following format:
    [lecture_number, (start_time_in_seconds, end_time_in_seconds)]

    Example:
    Input: "Summarize the first 5 minutes of lecture 4"
    Output: [4, (0, 300)]

    If it references only a specific lecture, return the following format:
    [lecture_number, (-1, -1)]

    Input: "Summarize lecture 6"
    Output: [6, (-1, -1)] --> get everything in process_query

    If it references neither, return None.
    Input: "What is recursion?"
    Output: None

    Return only the specified format, without any extra text or explanation.
    """

    try:
        response = client.chat.completions.create(
            model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
            messages=[
                {"role": "system", "content": "You are a parsing assistant."},
                {"role": "user", "content": instructions}
            ],
            stream=False,
        )

        response_text = response.choices[0].message.content.strip()

        if response_text.lower() == "none":
            return None
        
        try:
            result = eval(response_text)
            if (
                isinstance(result, list)
                and len(result) == 2
                and isinstance(result[0], int)
                and isinstance(result[1], tuple)
                and len(result[1]) == 2
                and all(isinstance(x, (int, float)) for x in result[1])
            ):
                return [result[0], (int(result[1][0]), int(result[1][1]))]
            else:
                return None
        except Exception as e:
            return None
    except Exception as e:
        return None

def process_query(compiled_input, current_question, json_file_path="Bejerano_Sun_224V_Updated.jsonl"):
    """
    Processes the current question to retrieve relevant information from a JSON file.
    If the question contains time-based information, it filters entries based on lecture number (and time range).

    Args:
        compiled_input (list): The list of all past user questions.
        current_question (str): The current user question.
        json_file_path (str): Path to the JSON file containing lecture data.

    Returns:
        list: Filtered lecture entries based on timestamp and lecture number.
    """
    timestamp_info = parse_timestamp_question(current_question)

    if timestamp_info:
        lecture_number, (start_time, end_time) = timestamp_info
        filtered_entries = []

        try:
            with open(json_file_path, "r") as file:
                data = [json.loads(line) for line in file]

            for entry in data:
                if entry.get("document_title") == f"Lecture {lecture_number}":
                    block_metadata = entry.get("block_metadata", {})
                    block_start = block_metadata.get("start_time", 0)
                    block_end = block_metadata.get("end_time", 0)

                    # If start_time and end_time are -1, use the entire lecture duration
                    if start_time == -1 and end_time == -1:
                        filtered_entries.append(entry)
                    elif block_start <= end_time and block_end >= start_time:
                        filtered_entries.append(entry)

            return filtered_entries

        except FileNotFoundError:
            print(f"Error: JSON file '{json_file_path}' not found.")
            return None
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None

    # default retrieval
    url = "https://search.genie.stanford.edu/stanford_computer_science_106B"
    headers = {"Content-Type": "application/json"}
    payload = {
        "query": compiled_input, 
        "rerank": True,
        "num_blocks_to_rerank": 10,
        "num_blocks": 3
    }
    
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return None

def is_homework_related(question):
    homework_keywords = ["homework", "assignment", "problem set", "pset", "task", "exercise", "solve", "implement"]
    return any(keyword.lower() in question.lower() for keyword in homework_keywords)

def get_response_from_model(history, data, current_question, compiled_input):
    client = Together()
    messages = [
        {
            "role": "system", 
            "content": ("You are a teaching chatbot for a college computer science class on data structures and algorithms taught by Christopher Gregg and Cynthia Lee."
                        "Reply succinctly. Avoid unnecesary commentary and extraneous details."
                        "Maintain a respectful and constructive tone and refrain from any negative sentiment."
                        "Highlight how the lecture ties into the broader course themes, when relevant.")
        }
    ]
     
    for entry in history:
        messages.append({"role": "system", "content": entry["response"]})
    
    messages.append({
        "role": "user",
        "content": f"Respond to this question: {current_question}. Use {data} as the primary source and {compiled_input} for context about previously asked questions."
    })

    stream = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        messages=messages,
        stream=True,
    )

    response_text = ""
    for chunk in stream:
        text = chunk.choices[0].delta.content or ""
        response_text += text
    return response_text

def handle_user_input():
    user_input = st.session_state.user_input
    if user_input:
        if is_homework_related(user_input):
            st.error(
                "It seems your question may relate to homework. "
                "Please refer to the official honor code, which does not allow the use of AI to solve or assist in completing the homework."
            )

            st.warning("Please ask a different question.")
            st.session_state.user_input = ""
            return

        else:
            # provides context for the current question
            compiled_input = [entry["question"] for entry in st.session_state.history] + [user_input]

            json_file_path = "Bejerano_Sun_224V_Updated.jsonl"
            data = process_query(compiled_input, user_input, json_file_path=json_file_path)

            if data:
                response = get_response_from_model(st.session_state.history, data, user_input, compiled_input)
                st.session_state.history.append({"question": user_input, "response": response})

            else:
                st.error("Failed to process your question. Please try again.")

            st.session_state.user_input = ""


# Streamlit App
st.set_page_config(layout="wide")

st.title("CS106B Lecture Chatbot")
st.write("Interact with the chatbot below to ask questions about your virtual CS106B lectures.")

if "history" not in st.session_state:
    st.session_state.history = []

st.write("### Chat History")
chat_history = st.container()

user_style = """
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 10px;
"""
bot_style = """
    background-color: #848884;
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 10px;
"""

with chat_history:
    for entry in st.session_state.history:
        user_message = f"""
        <div style="{user_style}">
            <b>You:</b> {entry['question']}
        </div>
        """
        bot_message = f"""
        <div style="{bot_style}">
            <b>Bot:</b> {entry['response']}
        </div>
        """
        st.markdown(user_message, unsafe_allow_html=True)
        st.markdown(bot_message, unsafe_allow_html=True)

st.write("---")
st.text_input(
    "Your question:", 
    placeholder="Type your question here...", 
    key="user_input", 
    on_change=handle_user_input
)