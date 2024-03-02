import streamlit as st
import pandas as pd

st.set_page_config(page_title="Policy Search", page_icon="🔍")

@st.cache_data
def load_data():
    data = pd.read_csv('fullpolicylist.csv')  
    return data

def run():
    st.write("# Policy Search App")

    data = load_data()

    st.sidebar.header("Filter options")

    state = st.sidebar.selectbox('Select State', options=data['State'].unique())

    year = st.sidebar.slider('Select Year', min_value=int(data['Year'].min()), max_value=int(data['Year'].max()), value=int(data['Year'].min()), step=1, format='%d')

    filtered_data = data[(data['State'] == state) & (data['Year'] == year)]

    if not filtered_data.empty:
      st.dataframe(filtered_data.style.format({"Year": "{:}"}))

    else:
        st.write("No policies found for the selected criteria.")

if __name__ == "__main__":
    run()
