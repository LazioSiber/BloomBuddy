import streamlit as st
import openai
# Uncomment the following lines to enable the API key input form
with st.sidebar:
    api_key_form = st.form(key="api_key_form")
    openai_api_key = api_key_form.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    api_key_form_submitted = api_key_form.form_submit_button("Submit")

    if api_key_form_submitted:
        if True:                              
            openai.api_key = openai_api_key
            st.success("Your OpenAI API key was saved successfully!")
        else:
            st.info("Your OpenAI API key is invalid, please check to see if it is correctly inputted or contact OpenAI")


def generate_flower_recommendation(occasion, recipient_name, favorite_color, relationship):
    # Customize the prompt based on your requirements
    prompt = f"Recommend a flower that are suitable for {occasion} and {favorite_color} for {recipient_name} who is my {relationship}. and make 5 notes telling {recipient_name} why I chose this flower for this {occasion}."

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
relationship = st.text_input("Your Relationship to the Recipient:")

# Generate recommendation
if st.button("Generate Recommendation"):
    if occasion and recipient_name and favorite_color and relationship:
        recommendation = generate_flower_recommendation(
            occasion, recipient_name, favorite_color, relationship
        )
        st.success(f"Recommended Flower: {recommendation}")
    else:
        st.warning("Please fill in all fields.")
