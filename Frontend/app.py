import streamlit as st
import requests

st.set_page_config(page_title="Realtime Calculator", layout="centered")
st.title("Realtime Calculator App")

API_URL = "http://127.0.0.1:8000"

#initialize history in session state
if "history" not in st.session_state:
    st.session_state.history = []

def add_to_history(entry:str):
    st.session_state.history.append(entry)
    #only last 10 entries
    if len(st.session_state.history) > 10:
        st.session_state.history = st.session_state.history[-10:]

st.sidebar.header("Choose Operation\n Sum, Mean, Variance, Matrix multiplication")
operation = st.sidebar.selectbox("Operation", ("Sum", "Mean", "Variance","Median", "Matrix Multiply"))



if operation.lower() in ["sum", "mean", "variance","median"]:
    numbers = st.text_input("Enter Numbers comma separated ex. 1,2,3,4,..")
    if st.button("Calculate"):
        if not numbers.strip():
            st.error("Please enter some numbers")
        else:
            try:
                nums = [float(x.strip()) for x in numbers.split(",") if x.strip()]
                if not nums:
                    st.error("Please enter valid numbers")
                else:
                    if operation.lower() == "sum":
                        endpoint = "/sum"
                    elif operation.lower() == "mean":
                        endpoint = "/mean"
                    elif operation.lower() == "variance":
                        endpoint = "/variance"
                    else:
                        endpoint = "/median"
                    #endpoint = "/sum" if operation.lower() == "sum" else "/mean"
                    response = requests.post(API_URL + endpoint, json={"numbers": nums})
                    if response.status_code == 200:
                        result = response.json()["result"]
                        #Record history entry
                        entry = f"{operation}: input={nums} => result={result}"
                        add_to_history(entry)
                        st.success(f"✅Result: {response.json()['result']}")
                    else:
                        st.error("❌Error Processing Request")
            except ValueError:
                st.error("Please enter valid numbers only")

elif operation == "Matrix Multiply":
    st.write("Enter two 2x2 matrices (as rows, separated by commas)")
    a = st.text_area("Matrix A:", "1,2\n3,4")
    b = st.text_area("Matrix B:", "5,6\n7,8")
    if st.button("Multiply"):
        try:
            A = [list(map(float, row.split(","))) for row in a.strip().split("\n")]
            B = [list(map(float, row.split(","))) for row in b.strip().split("\n")]
            response = requests.post(API_URL + "/multiply", json={"a": A, "b": B})
            if response.status_code == 200:
                result_mat = response.json()["result"]
                entry = f"Matrix Multiply: A={A} x B={B} => {result_mat}"
                add_to_history(entry)
                st.write("✅ Result Matrix:")
                st.table(result_mat)
            else:
                st.error("❌ Error processing request")
        except ValueError:
            st.error("Please enter valid numeric matrix values")

# Sidebar history display
st.sidebar.header("History")
if st.sidebar.button("Clear History"):
    st.session_state.history = []

if st.session_state.history:
    # show newest first, numbered
    for idx, item in enumerate(reversed(st.session_state.history), start=1):
        st.sidebar.write(f"{idx}. {item}")
else:
    st.sidebar.info("No history yet")

