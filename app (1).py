import math
import streamlit as st

# ---------------- PAGE CONFIGURATION ----------------
st.set_page_config(
    page_title="Smart Calculator",
    page_icon="🧮",
    layout="centered"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #101827, #172554);
        color: white;
    }

    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        color: #60A5FA;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #CBD5E1;
        font-size: 16px;
        margin-bottom: 30px;
    }

    .result-box {
        background: linear-gradient(135deg, #1D4ED8, #2563EB);
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        margin-top: 20px;
        color: white;
    }

    .result-box h1 {
        font-size: 35px;
        font-weight: bold;
    }

    div.stButton > button {
        width: 100%;
        border-radius: 10px;
        height: 48px;
        background-color: #2563EB;
        color: white;
        font-weight: bold;
        border: none;
    }

    div.stButton > button:hover {
        background-color: #3B82F6;
        color: white;
        border: none;
    }

    [data-testid="stSidebar"] {
        background-color: #111827;
    }
</style>
""", unsafe_allow_html=True)


# ---------------- SESSION STATE ----------------
if "history" not in st.session_state:
    st.session_state.history = []

if "result_text" not in st.session_state:
    st.session_state.result_text = ""

if "expression" not in st.session_state:
    st.session_state.expression = ""


# ---------------- HEADER ----------------
st.markdown(
    '<div class="main-title">🧮 Smart Calculator</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">A simple and powerful calculator built with Python & Streamlit</div>',
    unsafe_allow_html=True
)

st.divider()


# ---------------- OPERATION SELECTION ----------------
st.subheader("⚙️ Select Operation")

operation = st.selectbox(
    "Choose your mathematical operation",
    [
        "Addition (+)",
        "Subtraction (-)",
        "Multiplication (×)",
        "Division (÷)"
    ]
)


# ---------------- INPUT SECTION ----------------
st.subheader("📝 Enter Your Values")

# Initialize values so they are always defined.
values: str = ""
val1: float = 0.0
val2: float = 0.0

if operation in ["Addition (+)", "Multiplication (×)"]:
    values = st.text_input(
        "Enter multiple numbers separated by commas",
        placeholder="Example: 10, 20, 30, 40"
    ) or ""

else:
    col1, col2 = st.columns(2)

    with col1:
        input1 = st.number_input(
            "First Number",
            value=0.0,
            format="%g"
        )
        val1 = 0.0 if input1 is None else float(input1)

    with col2:
        input2 = st.number_input(
            "Second Number",
            value=0.0,
            format="%g"
        )
        val2 = 0.0 if input2 is None else float(input2)


# ---------------- CALCULATION FUNCTION ----------------
def calculate() -> None:
    try:
        calculated_result: float = 0.0
        calculated_expression: str = ""

        # ADDITION AND MULTIPLICATION
        if operation in ["Addition (+)", "Multiplication (×)"]:
            if not values.strip():
                st.error("Please enter your numbers!")
                return

            parsed_numbers: list[float] = [
                float(item.strip())
                for item in values.split(",")
            ]

            if not parsed_numbers:
                st.error("Please enter valid numbers!")
                return

            if not all(math.isfinite(number) for number in parsed_numbers):
                st.error("Please enter finite numbers only!")
                return

            if operation == "Addition (+)":
                calculated_result = sum(parsed_numbers)
                calculated_expression = " + ".join(
                    map(str, parsed_numbers)
                )
            else:
                calculated_result = 1.0
                for number in parsed_numbers:
                    calculated_result *= number

                calculated_expression = " × ".join(
                    map(str, parsed_numbers)
                )

        # SUBTRACTION
        elif operation == "Subtraction (-)":
            calculated_result = val1 - val2
            calculated_expression = f"{val1} - {val2}"

        # DIVISION
        elif operation == "Division (÷)":
            if val2 == 0:
                st.error("Division by zero is not possible!")
                return

            calculated_result = val1 / val2
            calculated_expression = f"{val1} ÷ {val2}"

        # VALIDATE RESULT
        if not math.isfinite(calculated_result):
            st.error("The result is too large!")
            return

        # SAVE RESULT AND HISTORY
        st.session_state.result_text = f"{calculated_result:,.10g}"
        st.session_state.expression = calculated_expression
        st.session_state.history.insert(
            0,
            f"{calculated_expression} = {calculated_result}"
        )

    except ValueError:
        st.error("Invalid input! Please enter numbers only.")

    except OverflowError:
        st.error("The result is too large to calculate.")


# ---------------- CALCULATE BUTTON ----------------
st.write("")

if st.button("Calculate Result 🚀"):
    calculate()


# ---------------- RESULT DISPLAY ----------------
if st.session_state.result_text:
    st.markdown(
        f"""
        <div class="result-box">
            <h2>Calculation Result</h2>
            <h1>{st.session_state.result_text}</h1>
            <p>{st.session_state.expression}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


# ---------------- CALCULATION HISTORY ----------------
st.divider()
st.subheader("📜 Calculation History")

if st.session_state.history:
    for index, item in enumerate(st.session_state.history, start=1):
        st.write(f"**{index}.** {item}")

    if st.button("🗑️ Clear History"):
        st.session_state.history = []
        st.session_state.result_text = ""
        st.session_state.expression = ""
        st.rerun()
else:
    st.info("No calculations yet. Start calculating!")


# ---------------- FOOTER ----------------
st.divider()

st.markdown(
    """
    <center style='color:#94A3B8;'>
        Developed using Python & Streamlit | Smart Calculator
    </center>
    """,
    unsafe_allow_html=True
)
