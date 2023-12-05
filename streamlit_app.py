import streamlit as st
import openai
import pandas as pd

# Uncomment the following lines to enable the API key input form
# Initialize
st.cache_data.clear()

if "openai_api_key" not in st.session_state:
    st.session_state.openai_api_key = ""

openai.api_key = st.session_state.openai_api_key

if "text_error" not in st.session_state:
    st.session_state.text_error = None

if "text" not in st.session_state:
    st.session_state.text = None

if "n_requests" not in st.session_state:
    st.session_state.n_requests = 0

with st.sidebar:
    api_key_form = st.form(key="api_key_form")
    openai_api_key = api_key_form.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    api_key_form_submitted = api_key_form.form_submit_button("Submit")

    if api_key_form_submitted:
        st.session_state.openai_api_key = openai_api_key
        openai.api_key = st.session_state.openai_api_key
        st.success("Your OpenAI API key was saved successfully!")

def generate_flower_recommendation(occasion, recipient_name, favorite_color, relationship):
    # Customize the prompt based on your requirements
    prompt1 = f"Recommend me a flower that are suitable for {occasion} and {favorite_color} for {recipient_name} who is my {relationship}."
    prompt2 = f'write 5 notes for me to tell {recipient_name} who is my {relationship} why I chose this flower for this {occasion}.'
    # Call OpenAI API for recommendation
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0.9,
        top_p=0.1,
        max_tokens=450,
        messages=[
            {"role": "system", "content": f"You are a flowers recommendation bot. You will help users find the best flowers for their important person from the context{occasion} and {favorite_color}"},
            {"role": "user", "content": f"You will help users find the best flowers from the context:{prompt1}. and make notes from the context:{prompt2}"},
        ]
    )
    
    return response.choices[0].message.content

# Center the title
st.markdown("<div style='text-align: center;'><h2 style='font-size: 2rem;'>🌼Flower For Your Important Person🌼</h2></div>", unsafe_allow_html=True)

# Uncomment the following lines to enable the API key input form


# User input
occasion = st.text_input("Occasion:")
recipient_name = st.text_input("Recipient's Name:")
favorite_color = st.text_input("Recipient's Favorite Color:")
relationship = st.text_input("Recipient's Relationship to you:")

# Generate recommendation
'''if st.button("Generate Recommendation"):
    if occasion and recipient_name and favorite_color and relationship:
        recommendation = generate_flower_recommendation(
            occasion, recipient_name, favorite_color, relationship
        )
        st.success(f"Recommended Flower: {recommendation}")
        st.success(f"{recommendation}")
    else:
        st.warning("Please fill in all fields.")'''

# Generate recommendation
if st.button("Generate Recommendation"):
    if occasion and recipient_name and favorite_color and relationship:
        recommendation = generate_flower_recommendation(
            occasion, recipient_name, favorite_color, relationship
        )

        # Extracting the flower and notes from the recommendation
        flower_start = "Recommended Flower:"
        note_start = "Notes:"
        flower_end = recommendation.find(note_start)

        recommended_flower = recommendation[len(flower_start):flower_end].strip()
        notes = recommendation[flower_end + len(note_start):].strip().split("\n")

        # Create a DataFrame with the recommended flower
        flower_data = {
            "Recommended Flower": [recommended_flower],
        }

        flower_df = pd.DataFrame(flower_data)

        # Create a DataFrame with the notes
        notes_data = {
            "Notes": notes,
        }

        notes_df = pd.DataFrame(notes_data)

        # Display the recommended flower and notes in separate DataFrames
        st.subheader("Recommended Flower:")
        st.dataframe(flower_df.style.set_properties(**{'text-align': 'left'}).set_table_styles([{
            'selector': 'th',
            'props': [('text-align', 'left')]
        }]))

        st.subheader("Notes:")
        st.dataframe(notes_df.style.set_properties(**{'text-align': 'left'}).set_table_styles([{
            'selector': 'th',
            'props': [('text-align', 'left')]
        }]))

    else:
        st.warning("Please fill in all fields.")

# Center the title
st.markdown("<div style='text-align: center;'><h2 style='font-size: 1.5rem;'><i>“I must have flowers, always, and always.”</i></h2></div>", unsafe_allow_html=True)
# Center the title
st.markdown("<div style='text-align: center;'><h2 style='font-size: 1rem;'><i>— Claude Monet —</i></h2></div>", unsafe_allow_html=True)
