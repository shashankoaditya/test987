import streamlit as st
from openai import OpenAI

# Initialize client using Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="SAP T-Code Helper")

st.title("SAP T-Code Explorer")

# Input field
tcode = st.text_input("Enter SAP T-Code (e.g., VA01, ME21N, FB60)")

def get_tcode_info(tcode):
    prompt = f"""
    Explain SAP T-Code: {tcode}

    Give output in this format:
    - Purpose:
    - Use Case:
    - Module:

    Keep it very concise (max 4-5 lines).
    """

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return response.output[0].content[0].text

# Button
if st.button("Get Details"):
    if tcode:
        with st.spinner("Fetching details..."):
            try:
                result = get_tcode_info(tcode)
                st.success("Result:")
                st.write(result)
            except Exception as e:
                st.error("Error: Check API key or connection.")
    else:
        st.warning("Please enter a T-Code.")
