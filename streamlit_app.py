import os
import streamlit as st
import openai
from hh_parser import get_candidate_info, get_job_description


# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    st.error("OPENAI_API_KEY is not set. Please configure it in the environment variables.")
    st.stop()

# System prompt for GPT
SYSTEM_PROMPT = """
Проскорь кандидата, насколько он подходит для данной вакансии.

Сначала напиши короткий анализ, который будет пояснять оценку.
Отдельно оцени качество заполнения резюме (понятно ли, с какими задачами сталкивался кандидат и каким образом их решал?). Эта оценка должна учитываться при выставлении финальной оценки - нам важно нанимать таких кандидатов, которые могут рассказать про свою работу.
Потом представь результат в виде оценки от 1 до 10.
""".strip()

# Function to request GPT completion
def request_gpt(system_prompt, user_prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Ensure your API key has access to this model
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=1000,
            temperature=0,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

# Streamlit interface
st.title("CV Scoring App")

job_description_url = st.text_area("Enter the job description URL", placeholder="Paste the job description URL here")
cv_url = st.text_area("Enter the CV URL", placeholder="Paste the CV URL here")

if st.button("Score CV"):
    if not job_description_url.strip() or not cv_url.strip():
        st.warning("Please enter both the job description URL and CV URL.")
    else:
        with st.spinner("Scoring CV..."):
            try:
                # Fetch job description
                job_description = get_job_description(job_description_url)
                if not job_description:
                    raise ValueError("Failed to extract job description. The page structure may have changed.")

                # Fetch candidate information
                cv = get_candidate_info(cv_url)
                if not cv:
                    raise ValueError("Failed to extract CV. The page structure may have changed.")

                st.write("### Job Description:")
                st.write(job_description)
                st.write("### CV:")
                st.write(cv)

                # Prepare prompt for GPT
                user_prompt = f"# ВАКАНСИЯ\n{job_description}\n\n# РЕЗЮМЕ\n{cv}"
                response = request_gpt(SYSTEM_PROMPT, user_prompt)

                st.write("### Scoring Result:")
                st.write(response)

            except Exception as e:
                st.error(f"An error occurred: {e}")



