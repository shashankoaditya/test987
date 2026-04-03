import streamlit as st
from openai import OpenAI

# --- CONFIG ---
st.set_page_config(layout="wide", page_title="SAP T-Code Explorer")

# --- INIT ---
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# --- SESSION STATE INIT ---
if "response" not in st.session_state:
    st.session_state.response = ""

if "metrics" not in st.session_state:
    st.session_state.metrics = None

# --- COST CONFIG (approx) ---
INPUT_COST_PER_1K = 0.0005
OUTPUT_COST_PER_1K = 0.0015
USD_TO_INR = 83

# --- FUNCTIONS ---
def get_tcode_info(tcode):
    prompt = f"""
    Explain SAP T-Code: {tcode}

    Format:
    - Purpose:
    - Use Case:
    - Module:

    Keep it concise.
    """

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    output_text = response.output[0].content[0].text

    usage = response.usage
    input_tokens = usage.input_tokens
    output_tokens = usage.output_tokens
    total_tokens = usage.total_tokens

    cost_usd = (input_tokens / 1000) * INPUT_COST_PER_1K + \
               (output_tokens / 1000) * OUTPUT_COST_PER_1K
    cost_inr = cost_usd * USD_TO_INR

    return output_text, input_tokens, output_tokens, total_tokens, cost_usd, cost_inr


def clear_all():
    st.session_state.clear()
    st.rerun()


# --- UI STYLING ---
st.markdown("""
<style>
.main {
    background: linear-gradient(to right, #1e3c72, #2a5298);
    color: white;
}
.stTextInput input {
    border-radius: 10px;
}
.stButton button {
    border-radius: 10px;
    background-color: #ff7f50;
    color: white;
}
.card {
    background-color: #ffffff20;
    padding: 15px;
    border-radius: 15px;
}
</style>
""", unsafe_allow_html=True)

st.title("🚀 SAP T-Code Explorer")

# --- LAYOUT ---
left, right = st.columns([2, 1])

# --- LEFT SIDE ---
with left:
    st.subheader("🔍 Query")

    tcode = st.text_input("Enter SAP T-Code", key="tcode")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Get Details"):
            if tcode:
                with st.spinner("Processing..."):
                    try:
                        (result,
                         in_tok,
                         out_tok,
                         tot_tok,
                         cost_usd,
                         cost_inr) = get_tcode_info(tcode)

                        st.session_state.response = result
                        st.session_state.metrics = (in_tok, out_tok, tot_tok, cost_usd, cost_inr)

                    except Exception as e:
                        st.error("API Error. Check API key.")
            else:
                st.warning("Please enter a T-Code.")

    with col2:
        if st.button("🔄 Refresh"):
            clear_all()

    st.subheader("📄 Response")
    st.write(st.session_state.response)


# --- RIGHT SIDE ---
with right:
    st.subheader("📊 Usage Metrics")

    if st.session_state.metrics:
        in_tok, out_tok, tot_tok, cost_usd, cost_inr = st.session_state.metrics

        st.markdown(f"""
        <div class="card">
        <b>Input Tokens:</b> {in_tok} <br>
        <b>Output Tokens:</b> {out_tok} <br>
        <b>Total Tokens:</b> {tot_tok} <br><br>
        <b>Cost (USD):</b> ${cost_usd:.6f} <br>
        <b>Cost (INR):</b> ₹{cost_inr:.4f}
        </div>
        """, unsafe_allow_html=True)

    else:
        st.info("Run a query to see usage")

    st.subheader("🤖 Model Info")
    st.success("gpt-4.1-mini")
