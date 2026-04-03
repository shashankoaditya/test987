import streamlit as st
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key="YOUR_API_KEY")

st.title("SAP T-Code Explorer")

# Input field
tcode = st.text_input("Enter SAP T-Code (e.g., VA01, ME21N, FB60)")

def get_tcode_info(tcode):
    prompt = f"""
    Explain SAP T-Code: {tcode}

    Provide:
    1. What is this T-Code
    2. Its main use case
    3. Which SAP module it belongs to

    Keep the answer very concise and structured.
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content

# Button action
if st.button("Get Details"):
    if tcode:
        with st.spinner("Fetching details..."):
            result = get_tcode_info(tcode)
            st.subheader(f"Details for {tcode}")
            st.write(result)
    else:
        st.warning("Please enter a T-Code.")
