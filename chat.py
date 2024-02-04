import os
import sys
from typing import Any, Dict, Generator, List, Union
import openai
import streamlit as st
from llama_index import StorageContext, load_index_from_storage
ResponseType = Union[Generator[Any, None, None], Any, List, Dict]

openai.api_key = st.secrets["chatgpt"]

@st.cache_resource(show_spinner=False)  # type: ignore[misc]
def load_index() -> Any:
    """Load the index from the storage directory."""
    print("Loading index...")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dir_path = os.path.join(base_dir, ".kb")
    # rebuild storage context
    storage_context = StorageContext.from_defaults(persist_dir=dir_path)
    # load index
    index = load_index_from_storage(storage_context)
    query_engine = index.as_query_engine()
    print("Done.")
    return query_engine


def main() -> None:
    """Run the chatbot."""
    if "query_engine" not in st.session_state:
        st.session_state.query_engine = load_index()
    st.title("Snak med Dinero")
    st.write("Er du i tvivl om dinero er programmet for dig? så spørg løs og få svar på din tvivl.")
    st.write("Skriv dit eget spørgsmål eller prøv et af disse")
    e2 = st.button("På mit arbejde er jeg meget på farten, og ikke mulighed for en computer, understøtter Dinero dette?",type="primary")
    e1 = st.button("Hvordan håndtere Dinero momsindberetning?",type="secondary")
    e3 = st.button("Kan Dinero hjælpe mig med at holde styr på mine udgifter og kvitteringer?",type="secondary")


    if "messages" not in st.session_state:
        system_prompt = (
                         "Du er en dansk Dinero ekspert som skal hjælpe brugeren med at forstå dinero ud fra et sæt dokumenter"
                         "Du kan forklare Dinero's funktioner på en let forstålig måde så alle kan være med, også dem som ikke forstår økonomi."
                         "Du forklare Dineros brugervenlighed, og skal sælge dinero til brugeren der spørger"
                         "Du skal kun bruge dokumenterne som din viden"
        )
        st.session_state.messages = [{"role": "system", "content": system_prompt}]

    for message in st.session_state.messages:
        if message["role"] not in ["user", "assistant"]:
            continue
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input() or e1==True or e2 ==True or e3==True:
        st.session_state.messages.append({"role": "user", "content": prompt})
        if e1:
            e1prompt = "Hvordan håndterer Dinero momsindberetning?"
            with st.chat_message("user"):
                st.markdown(e1prompt)
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                with st.status("Finder svar"):
                    print("Querying query engine API...")
                    response = st.session_state.query_engine.query(e1prompt)
                    full_response = f"{response}"
                    print(full_response)
                    message_placeholder.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
        elif e2:
            e2prompt = "På mit arbejde er jeg meget på farten, og ikke mulighed for en computer, understøtter Dinero dette?"
            with st.chat_message("user"):
                st.markdown(e2prompt)
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                with st.status("Finder svar"):
                    print("Querying query engine API...")
                    response = st.session_state.query_engine.query(e2prompt)
                    full_response = f"{response}"
                    print(full_response)
                    message_placeholder.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
        elif e3:
            e3prompt = "Kan Dinero hjælpe mig med at holde styr på mine udgifter og kvitteringer?"
            with st.chat_message("user"):
                st.markdown(e3prompt)
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                with st.status("Finder svar"):
                    print("Querying query engine API...")
                    response = st.session_state.query_engine.query(e3prompt)
                    full_response = f"{response}"
                    print(full_response)
                    message_placeholder.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})
        else:
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                with st.status("Finder svar"):
                    print("Querying query engine API...")
                    response = st.session_state.query_engine.query(prompt)
                    full_response = f"{response}"
                    print(full_response)
                    message_placeholder.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})

if __name__ == "__main__":
    main()