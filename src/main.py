import streamlit as st
from database.mongodb import init_db
from components.note_processor import NoteProcessor
import pyperclip

def main():
    st.title("AI Notes System")
    
    # Initialize components
    db = init_db()
    note_processor = NoteProcessor()
    note_processor.set_db(db)
    
    # Initialize session state for form clearing
    if "form_submitted" not in st.session_state:
        st.session_state.form_submitted = False

    # Reset form if it was previously submitted
    if st.session_state.form_submitted:
        st.session_state.title = ""
        st.session_state.content = ""
        st.session_state.form_submitted = False

    # Basic UI elements
    with st.form("note_form"):
        st.text_input("Title", key="title")
        st.text_area("Content", key="content")
        submitted = st.form_submit_button("Save Note")
        
        if submitted:
            title = st.session_state.title
            content = st.session_state.content
            note_processor.create_note(title, content)
            st.session_state.form_submitted = True
            st.success("Note saved successfully!")
            st.rerun()

    display_notes(note_processor)


def copy_to_clipboard(title, content, created_at):
    markdown_text = f"# {title}\n\n{content}\n\n*Created at: {created_at}*"
    pyperclip.copy(markdown_text)
    st.toast("Note copied to clipboard! ")


def display_notes(processor):
    st.subheader("Saved Notes")
    notes = processor.db.notes.find().sort("created_at", -1)
    
    for note in notes:
        with st.expander(f"{note['title']} - {note['created_at'].strftime('%Y-%m-%d %H:%M')}"):
            st.write(note['content'])
            
            # Create a container for buttons
            col1, col2, col3 = st.columns([1, 1, 4])
            
            # Copy button
            with col1:
                if st.button("Copy", key=f"copy_{note['_id']}"):
                    copy_to_clipboard(
                        note['title'],
                        note['content'],
                        note['created_at'].strftime('%Y-%m-%d %H:%M')
                    )
            
            # Delete button
            with col2:
                if st.button("Delete", key=str(note['_id'])):
                    processor.db.notes.delete_one({"_id": note['_id']})
                    st.rerun()

if __name__ == "__main__":
    main()
