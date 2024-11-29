import streamlit as st
from pymongo import MongoClient
from components.note_processor import NoteProcessor
import asyncio
import pyperclip
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    # Custom CSS for the delete button
    st.markdown("""
        <style>
        div[data-testid="stButton"] button[kind="secondary"]:hover {
            background-color: #ff4b4b;
            color: white;
        }
        /* Yellow color for AI Note button */
        div[data-testid="stButton"] button[kind="primary"] {
            background-color: #ffd700;
            color: black;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("AI Notes System")
    
    # Initialize MongoDB client
    client = MongoClient(os.getenv("MONGODB_URL", "mongodb://localhost:27017/"))
    db = client.notes_db
    
    # Initialize note processor
    note_processor = NoteProcessor()
    note_processor.set_db(db)
    
    # Initialize session state
    if "should_clear" not in st.session_state:
        st.session_state.should_clear = False
    
    # Note input section with clearing logic
    if st.session_state.should_clear:
        title = st.text_input("Title", value="", key=f"title_{st.session_state.should_clear}")
        content = st.text_area("Content", value="", height=200, key=f"content_{st.session_state.should_clear}")
        st.session_state.should_clear = False
    else:
        title = st.text_input("Title", key="title")
        content = st.text_area("Content", height=200, key="content")
    
    # Button layout with columns for AI Note and Save Note
    col1, col2, col3 = st.columns([2, 2, 4])
    
    with col1:
        if st.button("🤖 AI Note", type="primary", use_container_width=True):
            if not title or not content:
                st.error("Please enter both title and content")
            else:
                try:
                    with st.spinner('Processing with AI...'):
                        asyncio.run(note_processor.create_ai_note(title, content))
                    st.success("AI Note created!")
                    st.session_state.should_clear = True
                    st.rerun()
                except Exception as e:
                    st.error(f"Error creating AI note: {str(e)}")
                
    with col2:
        if st.button("💾 Save Note", use_container_width=True):
            if not title or not content:
                st.error("Please enter both title and content")
            else:
                try:
                    note_processor.create_note(title, content)
                    st.success("Note saved!")
                    st.session_state.should_clear = True
                    st.rerun()
                except Exception as e:
                    st.error(f"Error saving note: {str(e)}")
    
    with col3:
        st.empty()

    # Display saved notes
    st.markdown("---")
    st.subheader("Saved Notes")
    
    # Get all notes
    notes = list(db.notes.find().sort("created_at", -1))
    
    # Display each note
    for note in notes:
        with st.expander(f"{note['title']} - {note['created_at'].strftime('%Y-%m-%d %H:%M')}"):
            st.markdown(note['content'])
            
            # Buttons for copy and delete with reduced spacing
            col1, col2, col3 = st.columns([2, 2, 6])
            with col1:
                if st.button("📋 Copy", key=f"copy_{note['_id']}", use_container_width=True):
                    pyperclip.copy(note['content'])
                    st.success("Copied to clipboard!")
            with col2:
                if st.button("🗑️ Delete", key=f"delete_{note['_id']}", type="secondary", use_container_width=True):
                    db.notes.delete_one({"_id": note["_id"]})
                    st.rerun()
            with col3:
                st.empty()

if __name__ == "__main__":
    main()