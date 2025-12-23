import numpy as np


def country_year_list(df):
    years = sorted(df['Year'].unique().tolist())
    years.insert(0, 'Overall')

    countries = sorted(df['region'].dropna().unique().tolist())
    countries.insert(0, 'Overall')

    return years, countries


def fetch_medal_tally(df, years, country):
    medal_df = df.drop_duplicates(
        subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal']
    )

    if years == 'Overall' and country == 'Overall':
        temp_df = medal_df
    elif years == 'Overall':
        temp_df = medal_df[medal_df['region'] == country]
    elif country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(years)]
    else:
        temp_df = medal_df[
            (medal_df['Year'] == int(years)) &
            (medal_df['region'] == country)
        ]

    if country != 'Overall' and years == 'Overall':
        x = (
            temp_df.groupby('Year')[['Gold', 'Silver', 'Bronze']]
            .sum()
            .reset_index()
            .sort_values('Year')
        )
    else:
        x = (
            temp_df.groupby('region')[['Gold', 'Silver', 'Bronze']]
            .sum()
            .reset_index()
            .sort_values('Gold', ascending=False)
        )

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']
    x[['Gold', 'Silver', 'Bronze', 'total']] = x[
        ['Gold', 'Silver', 'Bronze', 'total']
    ].astype(int)

    return x


def data_over_time(df, col):
    temp = df.drop_duplicates(['Year', col])

    temp = (
        temp.groupby('Year')[col]
        .nunique()
        .reset_index()
        .rename(columns={'Year': 'Edition'})
    )

    return temp


def most_successful(df, sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    medal_count = (
        temp_df.groupby(['Name', 'Sport', 'region'])
        .size()
        .reset_index(name='Medal Count')
        .sort_values('Medal Count', ascending=False)
        .head(10)
    )

    return medal_count


def yearwise_medal_tally(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(
        subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True
    )

    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df

def country_event_heatmap(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(
        subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True
    )

    new_df = temp_df[temp_df['region'] == country]
    heatmap_df = new_df.pivot_table(
        index='Sport',
        columns='Year',
        values='Medal',
        aggfunc='count'
    ).fillna(0).astype(int)

    return heatmap_df


def most_successful(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]

    x = (
        temp_df['Name']
        .value_counts()
        .reset_index(name='Medal Count')   # 👈 count column named
        .rename(columns={'index': 'Name'}) # 👈 explicit rename
        .head(10)
        .merge(df, on='Name', how='left')[['Name', 'Medal Count', 'Sport']]
        .drop_duplicates('Name')
    )

    return x


def weght_v_height(df, sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df
    

def men_women_participation(df):    
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final