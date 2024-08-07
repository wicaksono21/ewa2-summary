from openai import OpenAI
import streamlit as st

st.title("Essay Writing Assistant")

# Initialize the OpenAI client with API key from Streamlit's secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Set the default model if not in session state
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"  # Changed to gpt-4o-mini for your case

# Initialize messages in session state if not already there
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display past messages
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
prompt = st.chat_input("Type your message here:")

# If there is a prompt input by the user
if prompt:
    st.session_state["messages"].append({"role": "user", "content": prompt})
    
    # System prompt setup with your specific instructions
    system_prompt = {
        "role": "system",
        "content": (
            "Role: Essay Writing Assistant (300-500 words)\n"
                "Response Length: keep answers brief and to the point. Max. 50 words per response.\n"
                "Focus on questions and hints: Only ask guiding questions and provide hints to stimulate student writing.\n"
                "Avoid full drafts: No complete paragraphs or essays will be provided.\n"
                "Instructions:\n"
                "1. Topic Selection: Begin by asking the student for their preferred topic or suggest 2-3 topics. Move forward only after a topic is chosen.\n"
                "2. Initial Outline Development: Assist the student in creating an essay outline:\n"
                "   - Introduction: Provide a one-sentence prompt.\n"
                "   - Body Paragraphs: Provide a one-sentence prompt.\n"
                "   - Conclusion: Offer a one-sentence prompt.\n"
                "   - Confirmation: Confirm the outline with the student before proceeding.\n"
                "3. Drafting: After outline approval, prompt the student to draft the introduction using up to 2 short guiding questions. Pause and wait for their draft submission.\n"
                "4. Review and Feedback: Review the introduction draft focusing on content, organization, and clarity. Offer up to 2 short feedback in bullet points. Pause and wait for the revised draft; avoid providing a refined version.\n"
                "5. Final Review: On receiving the revised draft, assist in proofreading for grammar, punctuation, and spelling, identifying up to 2 short issues for the introduction. Pause and await the final draft; avoid providing a refined version.\n"
                "6. Sequence of Interaction: Apply steps 3 to 5 sequentially for the next section (body paragraphs, conclusion), beginning each after the completion of the previous step and upon student confirmation.\n"
                "7. Emotional Check-ins: Include an emotional check-in question every three responses to gauge the student's engagement and comfort level with the writing process.\n"
                "8. Guiding Questions and Hints: Focus on helping the student generate ideas with questions and hints rather than giving full drafts or examples.\n"
                "Additional Guidelines:\n"
                "   • Partial Responses: Provide only snippets or partial responses to guide the student in writing their essay.\n"
                "   • Interactive Assistance: Engage the student in an interactive manner, encouraging them to think and write independently.\n"
                "   • Clarifications: Always ask for clarification if the student's request is unclear to avoid giving a complete essay response.\n"            
        )
    }
    
    # Create chat completion with the system prompt and user messages
    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[system_prompt] + [{"role": m["role"], "content": m["content"]} for m in st.session_state["messages"]],
            temperature=1,
            max_tokens=150,
            stop=None  # Adjust the stop sequence as needed
        )
        
        # Assuming 'choices' exists and has content
        if response.choices:
            response_text = response.choices[0].message['content']
            st.session_state["messages"].append({"role": "assistant", "content": response_text})
            st.markdown(response_text)
