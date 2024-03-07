import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

def load_data():
 
    df1 = pd.read_csv('app_pages/data_up_to_2000.csv')
    df2 = pd.read_csv('app_pages/did_results.csv')
    predictions_data = pd.read_csv('app_pages/predictions_output.csv')
    data_from_2001 = pd.read_csv('app_pages/data_from_2001.csv')

    predictions_data.rename(columns={'predicted_DiD_rate_for_women': 'DiD_rate_for_women'}, inplace=True)

    merged_df1_df2 = pd.merge(df1, df2, on='policy_id', how='left')
    merged_df1_df2.drop(columns=['Unnamed: 0_x', 'Unnamed: 0_y'], inplace=True)
    merged_predictions = pd.merge(data_from_2001, predictions_data, on='policy_id', how='left')
    # Merging with specified suffixes to identify duplicate columns
    merged_predictions = pd.merge(data_from_2001, predictions_data, on='policy_id', how='left', suffixes=('', '_drop'))

    merged_predictions = merged_predictions.loc[:, ~merged_predictions.columns.str.endswith('_drop')]

    merged_predictions.drop(columns=['Unnamed: 0'], inplace=True)
    full_data = pd.concat([merged_df1_df2, merged_predictions], ignore_index=True)


    return full_data

full_data = load_data()



def display_filtered_data(df):
    displayed = set()  # keep track of displayed policies to avoid duplicates
    for _, row in df.iterrows():
        # check if the policy has been displayed already
        if row['policy_id'] in displayed:
            continue
        else:
            displayed.add(row['policy_id'])

        print("Policy ID:", row['policy_id'])  # debug statement
        print("Impact Score:", row['DiD_rate_for_women'])  # debug statement

        full_policy = row['full_policy'] if pd.notnull(row['full_policy']) else 'Unavailable'
        impact_score = row['DiD_rate_for_women'] if pd.notnull(row['DiD_rate_for_women']) else 'Unavailable'

        print("Impact Score After Condition Check:", impact_score)  # debug statement

        impact_description = "increase" if row['DiD_rate_for_women'] > 0 else "decrease"
        DiD_rate_for_women_abs = abs(row['DiD_rate_for_women'])
        
        dynamic_impact_sentence = f"This policy, enacted in {row['year']}, is associated with a {impact_description} in the abortion rate by {DiD_rate_for_women_abs:.2f} percentage points."
        template = f"""
        <div><strong>Policy Information:</strong></div>
        <ul>
            <li>Year: {row['year']}</li>
            <li>Location: {row['location']}</li>
            <li>Impact Score: {impact_score}</li>
        </ul>
        <div><strong>Full Text:</strong><br>
        {full_policy}</div>
        <br>
        <div><strong>Impact Analysis:</strong><br>
        {dynamic_impact_sentence}</div>
        <hr style='margin: 1em 0;'>
        """
        st.markdown(template, unsafe_allow_html=True)




def visualize_data(full_data, location):
    state_data = full_data[full_data['location'] == location]
    state_data.sort_values('year', inplace=True)
    
    state_data['DiD_rate_for_women'].fillna(0, inplace=True)


    last_known_rate = state_data.loc[state_data['year'] <= 2000, 'rate_for_women'].iloc[-1]
    adjusted_rates = [last_known_rate]
    for i in range(1, len(state_data)):
        year = state_data.iloc[i]['year']
        if year > 2000:
            adjusted_rate = adjusted_rates[-1] + state_data.iloc[i]['DiD_rate_for_women']
            adjusted_rates.append(adjusted_rate)
        else:
            adjusted_rates.append(state_data.iloc[i]['rate_for_women'])
    state_data['rate_for_women_adjusted'] = adjusted_rates

    historical_state_data = state_data[state_data['year'] <= 2000]
    predicted_state_data = state_data[state_data['year'] > 2000]
    non_zero_did = state_data['DiD_rate_for_women'] != 0

    fig, ax = plt.subplots()
    ax.plot(historical_state_data['year'], historical_state_data['rate_for_women_adjusted'], label='Confirmed Abortion Rates', marker='o', linestyle='-', color='blue')
    ax.plot(predicted_state_data['year'], predicted_state_data['rate_for_women_adjusted'], label='Predicted Abortion Rates', marker='o', linestyle='--', color='blue', alpha=0.5)
    ax.bar(state_data[non_zero_did]['year'], state_data[non_zero_did]['DiD_rate_for_women'], width=0.4, label='Annual DiD Impact', color='orange', alpha=0.7)
    ax.set_xlabel('Year')
    ax.set_ylabel('Abortion Rate for Women')
    ax.set_title(f'Impact of Policies on Abortion Rate for Women in {location}')
    ax.legend()
    ax.grid(True)
    plt.tight_layout()

    

def show():
    st.title('Policy Search 🔍')
    df = load_data()
    
    location_to_filter = st.sidebar.selectbox('Select Location:', sorted(df['location'].unique()))
    
    available_years = df[df['location'] == location_to_filter]['year'].unique()
    available_years.sort()  # Sort the years if needed

    year_to_filter = st.sidebar.selectbox('Select Year:', available_years)

    if year_to_filter > 2000:
        st.info("The impact score is based on predictions derived from historical data and modeling. It represents the projected change in abortion rates due to specific policies, expressed as a percentage point difference.")
    
    filtered_df = df[(df['year'] == year_to_filter) & (df['location'] == location_to_filter)]
    
    if not filtered_df.empty:
        display_filtered_data(filtered_df)
    else:
        st.write("No data available for the selected year and location.")
    
    #if location_to_filter == "Federal":
        #visualize_data(df, location_to_filter)
