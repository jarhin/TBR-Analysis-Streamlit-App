import pandas as pd
import os
import streamlit as st
from streamlit_dynamic_filters import DynamicFilters

# read file

headers = pd.read_csv(
    os.path.join(
        os.path.dirname('__file__'), 
        "./Data/The Black Response Cambridge - Community Education Workshop Evaluation 2024 - Sheet1.csv"
        ),
        nrows=1       
)

df = pd.read_csv(
    os.path.join(
        os.path.dirname('__file__'), 
        "./Data/The Black Response Cambridge - Community Education Workshop Evaluation 2024 - Sheet1.csv"
        ),
    skiprows=1       
)


# reset index for person ID
df = df.reset_index()

print(headers.columns)
print("---")
print(df.columns)


# Age
columns_age = [
    '17 years or younger', '18 - 24 years', '25 - 34 years', '35 - 44 years', 
    '45 - 54 years', '55 - 64 years', '65 - 74 years', '75 years or older'
]

# melt ages
question_ages_df = pd.melt(
    df[
        ['17 years or younger', '18 - 24 years', '25 - 34 years', '35 - 44 years', 
        '45 - 54 years', '55 - 64 years', '65 - 74 years', '75 years or older', "index"
        ]
    ],
    id_vars=["index"], 
    value_vars=columns_age,
    var_name='question_ages', 
    value_name='question_ages_values',
    ignore_index=False
)

# filter na
question_ages_df = question_ages_df[
    question_ages_df["question_ages_values"].notnull()
].drop(columns = ["index", 'question_ages'])

# Gender
question_gender = ['Man', 'Non-binary', 'Woman', 'Self-describe:']


question_gender_df = pd.melt(
    df[
        ['Man', 'Non-binary', 'Woman', 'Self-describe:', 'index']
    ],
    value_vars=question_gender,
    var_name='question_gender', 
    value_name='question_gender_values',
    ignore_index=False
)

# filter na
question_gender_df = question_gender_df[
    question_gender_df["question_gender_values"].notnull()
].drop(columns = [ "question_gender"])


# Race

question_race = [
    'Asian or Asian American', 'Black or African American',
    'Hispanic or Latino/a/x', 'Middle Eastern or North African',
    'Native American or Alaska Native',
    'Native Hawaiian or other Pacific Islander', 'White',
    'Self-describe:.1'
]


# melt race
question_race_df = pd.melt(
    df[
        [
            'Asian or Asian American', 'Black or African American',
            'Hispanic or Latino/a/x', 'Middle Eastern or North African',
            'Native American or Alaska Native',
            'Native Hawaiian or other Pacific Islander', 'White',
            'Self-describe:.1',
            "index"
        ]
    ],
    id_vars=["index"], 
    value_vars=question_race,
    var_name='question_race', 
    value_name='question_race_values',
    ignore_index=False
)

# filter na
question_race_df = question_race_df[
    question_race_df["question_race_values"].notnull()
].drop(columns = ["index", "question_race"])



# full demographics in dataset
df_temp_merge = pd.merge(
    question_ages_df,
    question_gender_df,
    left_index=True, 
    right_index=True,
    how = "inner"
)

df_demographics_df = pd.merge(
    df_temp_merge,
    question_race_df,
    left_index=True, 
    right_index=True,
    how = "inner"
)

# using joins on indices to filter on the different demographic groups
df_demographics_df = df_demographics_df.rename(
    columns={
        "question_ages_values": "age-group",
        "question_gender_values": "gender",
        "question_race_values": "race"
    }
)



#TODO DYNAMIC FILTERS
# [GitHub - arsentievalexstreamlit-dynamic-filters Custom component with dynamic multiselect filters for Streamlit](https://github.com/arsentievalex/streamlit-dynamic-filters)







# Questions

questions_list = [
    'How likely is it that you would recommend The Black Response to a friend or family member?', 
    'What is The Black Response good at?',
    'What could The Black Response do better?',
    'Overall, how well has this workshop hosted by The Black Response met your needs?',
    'How often do members of The Black Response treat you with respect?',
    'How connected do you feel to other community participants at this workshop?',
    'How has your knowledge about abolition and advocacy changed since you got involved with The Black Response?',
    "How could we make it easier for you to attend The Black Response's Community Workshops?",
    'How can we make the workshops more engaging for you?',
    'If The Black Response Cambridge were to offer other workshops through our community partners, which topics would you be interested in? Check all that apply.',
    'How would you like to be involved in The Black Response’s future advocacy efforts? Check all that apply',
    "How can we encourage more community members to get involved with The Black Response?"
]



question_list_to_columns = {}

# add key values as lists
question_list_to_columns['How likely is it that you would recommend The Black Response to a friend or family member?'] = ['Response']
question_list_to_columns['What is The Black Response good at?'] = ['Open-Ended Response']
question_list_to_columns['What could The Black Response do better?'] = ['Open-Ended Response.1']
question_list_to_columns['Overall, how well has this workshop hosted by The Black Response met your needs?'] = [
    'Not well at all', 'A little bit', 'Fairly well', 'Very well', 'Extremely well'
]
question_list_to_columns['How often do members of The Black Response treat you with respect?'] = ['Never', 'Rarely', 'Sometimes', 'Usually', 'Always']
question_list_to_columns['How connected do you feel to other community participants at this workshop?'] = [
    'Not at all connected', 'A little bit connected', 'Fairly connected', 'Very connected', 
    'Extremely connected'
]
question_list_to_columns["How could we make it easier for you to attend The Black Response's Community Workshops?"] = [
    'Help with childcare', 'Help with transportation', 'Offer more virtual meetings',
    'Do more outreach before the workshops', 'Hold workshops at more convenient locations/venues', 'Hold workshops on other days and/or times', 
    'Provide food/drinks at workshops', 'Provide language interpretation', 'Other (please specify):'
]
question_list_to_columns['How can we make the workshops more engaging for you?'] = [
    'Open-Ended Response.3'
]
question_list_to_columns[
    'If The Black Response Cambridge were to offer other workshops through our community partners, which topics would you be interested in? Check all that apply.'
] = [
        'Affordable housing',
       'Anti-racism', 'Disaster preparation (eg. fires, floods, earthquakes, etc.)', 'Mental health services', 'Immigration/Support for immigrants',
       'Public schools', 'Preventing domestic/relationship abuse', 'Carceral systems', 'Alternatives to policing models', 'Abolition',
       'Community organizing', 'Campaign building', 'Physical/Digital security'
    ]
question_list_to_columns['How would you like to be involved in The Black Response’s future advocacy efforts? Check all that apply'] = [
    'I am not interested', 
    'I am willing to join an advocacy planning committee', 'I am willing to meet with local council members',
    'I am willing to meet with state officials', 'I am willing to volunteer at The Black Response (small admin tasks, grant writing, etc.)',
    'Other involvement (please specify):'
    ]
question_list_to_columns["How can we encourage more community members to get involved with The Black Response?"] = [
    'Open-Ended Response.4'
]

question_list_to_columns['How has your knowledge about abolition and advocacy changed since you got involved with The Black Response?'] = [
    'Open-Ended Response.2'
]

columns_option = st.sidebar.selectbox(
    "Please select the question to analyse",
    questions_list,
)



question_data = df[question_list_to_columns[columns_option]]


question_data_melt = pd.melt(
    df[question_list_to_columns[columns_option] + ["index"]],
    id_vars=["index"], 
    value_vars=question_list_to_columns[columns_option],
    var_name='question_columns', 
    value_name='question_columns_values',
    ignore_index=False
)

# filter na
question_data_melt = question_data_melt[
    question_data_melt["question_columns_values"].notnull()
].drop(columns = ["index", "question_columns"])


# add demographics
full_question_demographics = pd.merge(
    df_demographics_df,
    question_data_melt,
    left_index=True,
    right_index=True, 
    how = 'inner'
)

dynamic_filters = DynamicFilters(full_question_demographics, filters=['age-group', 'gender', 'race'])

with st.sidebar:
    st.write("Apply filters in any order 👇")
    st.button("Reset Filters", on_click=dynamic_filters.reset_filters)

val_counts_df = dynamic_filters.filter_df().reset_index().groupby(["question_columns_values"])['index'].nunique().reset_index().rename(columns={'index': 'people count'})
dynamic_filters.display_filters(location='sidebar')

tab1, tab2 = st.tabs(["Data", "Chart"])

with tab1:

    st.write("You selected:", columns_option)

    st.table(dynamic_filters.filter_df())

with tab2:

    st.write("You selected:", columns_option)
    
    st.bar_chart(
        val_counts_df, 
        x = 'question_columns_values', 
        y = 'people count'
    )






