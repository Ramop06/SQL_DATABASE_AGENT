import requests
import streamlit as st

# PAGE CONFIG

st.set_page_config(
    page_title="SQL Database Agent",
    page_icon="🗄️",
    layout="centered"
)

# CUSTOM CSS

st.markdown("""
<style>

.main-title {
    font-size: 38px;
    font-weight: 700;
    margin-bottom: 5px;
}

.subtitle {
    color: #777;
    font-size: 17px;
    margin-bottom: 25px;
}

.stButton > button {
    width: 100%;
    height: 45px;
    font-size: 16px;
    font-weight: 600;
    border-radius: 8px;
}

.result-box {
    padding: 15px;
    border-radius: 10px;
    background-color: #f5f7fa;
    margin-top: 10px;
}

</style>
""", unsafe_allow_html=True)


# TITLE

st.markdown(
    '<div class="main-title">🗄️ SQL Database Agent</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Ask questions about your database in natural language.</div>',
    unsafe_allow_html=True
)


# SESSION HISTORY

if "history" not in st.session_state:
    st.session_state.history = []


# QUESTION INPUT

question = st.text_input(
    "Ask your database question",
    placeholder="e.g. Show the top 5 CSE students by marks"
)


# RUN AGENT

if st.button("🚀 Run Agent", type="primary") and question:

    try:

        with st.spinner("Thinking..."):

            response = requests.post(
                "http://127.0.0.1:8000/query",
                json={"question": question},
                timeout=90
            )

        data = response.json()

        # SUCCESS

        if response.status_code == 200:

            # ANSWER
            st.subheader("💡 Answer")

            answer = data.get(
                "answer",
                "I could not generate an answer."
            )

            st.write(answer)


            # TABLE RESULT

            result = data.get("result")

            if result and isinstance(result, dict):

                rows = result.get("rows", [])

                if rows:

                    st.subheader("📊 Results")

                    st.dataframe(
                        rows,
                        use_container_width=True,
                        hide_index=True
                    )


            # GENERATED SQL

            sql = data.get("sql")

            if sql:

                with st.expander("🔍 View Generated SQL"):

                    st.code(
                        sql,
                        language="sql"
                    )


            # SAVE HISTORY

            st.session_state.history.append(
                {
                    "question": question,
                    "answer": answer
                }
            )

        else:

            st.error(
                data.get(
                    "detail",
                    "The agent returned an error."
                )
            )


    except requests.exceptions.ConnectionError:

        st.error(
            "❌ Could not connect to the API. "
            "Make sure FastAPI is running on port 8000."
        )

    except requests.exceptions.Timeout:

        st.error(
            "⏳ The request took too long. Please try again."
        )

    except Exception as e:

        st.error(
            f"❌ Something went wrong: {e}"
        )


# QUERY HISTORY

if st.session_state.history:

    st.divider()

    with st.expander("🕘 Query History"):

        for item in reversed(st.session_state.history[-10:]):

            st.markdown(
                f"**Q:** {item['question']}"
            )

            st.markdown(
                f"**A:** {item['answer']}"
            )

            st.divider()