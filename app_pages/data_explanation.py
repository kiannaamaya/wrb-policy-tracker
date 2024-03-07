import streamlit as st
import pandas as pd
import plotly.express as px

data = pd.read_csv('app_pages/data_up_to_2000.csv')

def show():
    st.title('Data')
    
    st.header('Data Sources')
    st.markdown("""
    The primary historical data on abortion rates for women in the United States from 1970 to 2000 is sourced from the **Guttmacher Institute**. This dataset provides comprehensive statistical insights into abortion trends over three decades, serving as a crucial baseline for our analysis.
    
    In addition to historical abortion rate data, policy data from various sources (to be detailed later) have been utilized. These datasets encompass a range of abortion-related policies across different states, enabling a multifaceted examination of policy impacts over time.
    """)

    locations = data['location'].unique()

    selected_location = st.selectbox('Select a location:', locations)
    
    filtered_data = data[data['location'] == selected_location]
    
    fig = px.line(filtered_data, x='year', y='rate_for_women', title=f'Rate for Women Over Time in {selected_location}',
                  markers=True, line_shape='linear')
    
    fig.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)',  # transparent background in the plot area
        'paper_bgcolor': 'rgba(255,255,255,1)',  # background color for the entire figure
        'title': {'x': 0.5, 'xanchor': 'center'},  # center the title horizontally
        'xaxis': {
            'title': 'Year',
            'showline': True,  # show the x-axis line
            'linecolor': 'black',  # color of the x-axis line
        },
        'yaxis': {
            'title': 'Rate for Women',
            'showline': True,  # show the y-axis line
            'linecolor': 'black',  # color of the y-axis line
        }
    })
    
    fig.update_traces(line={'color': 'black'}, marker={'color': 'black'})
    
    fig.update_xaxes(title_font=dict(size=18, color='black'), tickfont=dict(color='black'))
    fig.update_yaxes(title_font=dict(size=18, color='black'), tickfont=dict(color='black'))
    
    st.plotly_chart(fig)
    
    st.header('Historical vs. New Data')
    st.markdown("""
    The analysis distinguishes between **historical** and **new** data segments:
    
    - **Historical Data (1970-2000):** This segment, derived from the Guttmacher Institute, forms the foundation of our analysis. It provides a retrospective look at abortion rates, facilitating an understanding of trends prior to the 21st century.
    
    - **New Data (2001-2022):** Considered the "new" dataset, this portion includes estimated abortion rates and policy impacts from 2001 onwards. The new data segment is crucial for making predictions about potential impacts of existing and future abortion-related policies.
    """)
    
    st.header('Additional Sources')
    st.markdown("""
    Further data sources and contributions to this analysis will be acknowledged as they are confirmed. Collaboration with various datasets and partners ensures a robust and comprehensive examination of the subject matter.
    """)
    
    st.header('Learn More')
    st.markdown("""
    For more detailed information about the Guttmacher Institute's research and methodologies, visit their [official website](https://www.guttmacher.org).
    
    Stay tuned for updates on additional data sources and insights as our analysis progresses.
    """)

if __name__ == "__main__":
    show()
