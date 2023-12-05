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

#user_api_key = st.sidebar.text_input("OpenAI API key", type="password")
#client = openai.OpenAI(api_key=user_api_key)

def generate_flower_recommendation(occasion, recipient_name, favorite_color, relationship):
    # Customize the prompt based on your requirements
    prompt = f"Recommend me a flower that are suitable for {occasion} and {favorite_color} for {recipient_name} who is my {relationship}. and write 5 notes for me to tell {recipient_name} why I chose this flower for this {occasion}."

    # Call OpenAI API for recommendation
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0.7,
        top_p=0.7,
        max_tokens=450,
        messages=[
            {"role": "system", "content": "You are a flowers recommendation bot. You will help users find the best flowers for their important person."},
            {"role": "user", "content": f"You will help users find the best flowers and make notes from the context:{prompt}."},
        ]
    )
    
    return response.choices[0].message.content

#st.title("🌼Flower For Your Important Person🌼")
st.markdown("<h2 style = 'font-size: 1.8rem'>🌼Flower For Your Important Person🌼</h2>",unsafe_allow_html=True)

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
    else:
        st.warning("Please fill in all fields.")'''

# Generate recommendation
if st.button("Generate Recommendation"):
    if occasion and recipient_name and favorite_color and relationship:
        recommendation = generate_flower_recommendation(
            occasion, recipient_name, favorite_color, relationship
        )

        # Extracting the flower and note from the recommendation
        flower_start = "Recommended Flower:"
        note_start = "Notes:"
        flower_end = recommendation.find(note_start)

        recommended_flower = recommendation[len(flower_start):flower_end].strip()
        note = recommendation[flower_end + len(note_start):].strip()

        # Create a DataFrame with the recommended flower and note
        data = {
            "Recommended Flower": [recommended_flower],
            "Note": [note],
        }

        df = pd.DataFrame(data)

        # Style the DataFrame for a beautiful output
        st.markdown("<h3 style='text-align: left; color: #336699;'>Recommended Flower and Note</h3>", unsafe_allow_html=True)
        st.dataframe(df.style.set_properties(**{'text-align': 'left'}).set_table_styles([{
            'selector': 'th',
            'props': [('text-align', 'left')]
        }]))

    else:
        st.warning("Please fill in all fields.")

  

    
#explanation_text = """
#<h3 style='text-align: center; color: green;'> FallacyBot </h3>
#<h6 style='text-align: center'> Checking for <span style='color:red'>fallacies</span> in your text since 2023!</h6>
#<p> For your convenience, a default example is provided. If you don't input any text, the bot will use the example text. </p>
#"""
#st.markdown(explanation_text, unsafe_allow_html=True)
