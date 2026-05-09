import streamlit as st  # UI Framework
import ollama           # Local LLM interaction
import io               # For capturing output
import sys              # For stdout redirection

st.title("Ollama Coding Assist! 🐍")

# Input area for the user's request
prompt_input = st.text_area(label="Write your coding prompt.", placeholder="e.g., Write a function to calculate Fibonacci numbers")
button = st.button("Generate & Fix Code")

# Use session state to store the working code so Part 2 can access it
if "working_code" not in st.session_state:
    st.session_state["working_code"] = ""

if button:
    if prompt_input:
        current_prompt = prompt_input + "\nNote: Output must have only Python code. Do not add any explanation or text outside of the code block."
        attempts = 0
        max_attempts = 5  # Safety limit to prevent infinite loops

        while attempts < max_attempts:
            attempts += 1
            st.write(f"⚙️ Attempt {attempts}...")

            # 1. Generate Code
            response = ollama.generate(model='llama3.1:8b', prompt=current_prompt)
            raw_response = response["response"]

            # 2. Clean the Code (Remove markdown backticks)
            code = raw_response.replace("```python", "").replace("```", "").strip()

            # 3. Setup Output Capture
            old_stdout = sys.stdout
            sys.stdout = buffer = io.StringIO()

            # 4. Execute the Code
            exec_error = None
            try:
                # We use a dictionary for globals to keep the namespace clean
                exec(code, {})
            except Exception as e:
                exec_error = str(e)

            # 5. Restore Output
            sys.stdout = old_stdout
            output = buffer.getvalue()

            # 6. Decision Logic
            if exec_error:
                # FAILURE: Feed the error back to the LLM
                st.warning(f"Attempt {attempts} failed with error. Retrying...")
                current_prompt = f"The following code produced an error: {exec_error}\n\nCode:\n{code}\n\nPlease fix the code and provide ONLY the corrected Python code."
                
                if attempts == max_attempts:
                    st.error("Could not fix the code after 5 attempts. Please try a different prompt.")
            else:
                # SUCCESS: Break the loop
                st.success("Code is working perfectly!")
                st.code(code, language='python')
                
                if output:
                    st.subheader("Output:")
                    st.text(output)
                
                st.session_state["working_code"] = code
                break

# --- Part 2: Q&A about the Code ---
st.divider()
st.subheader("Ask a Question about the Code")
question = st.text_input(label="What part of the code should I explain?")
ask_button = st.button("Explain")

if ask_button:
    if st.session_state["working_code"]:
        with st.spinner("Thinking..."):
            explanation_prompt = f"""
            Context Code:
            {st.session_state["working_code"]}

            Question:
            {question}

            Please explain the logic behind this specific part of the code in detail.
            """
            
            answer = ollama.generate(model='llama3.1:8b', prompt=explanation_prompt)
            
            st.info("Explanation:")
            st.markdown(answer["response"])
    else:
        st.warning("Please generate a working piece of code first!")