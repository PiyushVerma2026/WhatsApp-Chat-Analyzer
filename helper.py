
# Third-party libraries used by the analysis functions.
from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
import matplotlib.pyplot as plt 
from collections import Counter
import emoji 
import seaborn as sns



# Reusable URL extractor for link statistics.
extract = URLExtract()

# Return message, word, media, and link totals for the selected participant.
def fetch_stats(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    # fetch the number of messages
    num_messages = df.shape[0]

    # fetch the total number of words
    words = []
    for message in df['messages']:
        words.extend(message.split())

    # fetch number of media messages
    num_media_messages = df[df['messages'] == '<Media omitted>\n'].shape[0]

    # fetch number of links shared
    links = []
    for message in df['messages']:
        links.extend(extract.find_urls(message))

    return num_messages,len(words),num_media_messages,len(links)


# Build daily message counts for the timeline chart.
def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['messages'].reset_index()
    daily_timeline['messages'] = daily_timeline['messages'].astype(int)
    return daily_timeline




# Build monthly message counts and readable month labels.
def monthly_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    timeline = (
        df.groupby(['year', 'month_num', 'month'])
        .count()['messages']
        .reset_index()
    )

    timeline['year'] = timeline['year'].astype(int)
    timeline['messages'] = timeline['messages'].astype(int)

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline





# Count messages by day of the week.
def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    return df['day_name'].value_counts()







# Count messages by calendar month.
def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    return df['month'].value_counts()

# Create a day-by-hour table with all 24 time slots included.
def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    period_order = [
        f'{hour:02d}-{(hour + 1) % 24:02d}'
        for hour in range(24)
    ]

    day_order = [
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
        'Saturday',
        'Sunday'
    ]

    user_heatmap = (
        df.pivot_table(
            index='day_name',
            columns='period',
            values='messages',
            aggfunc='count',
            fill_value=0
        )
        .reindex(index=day_order, columns=period_order, fill_value=0)
        .astype(int)
    )

    return user_heatmap








# Return the busiest participants and their percentage share.
def most_busy_users(df):
    x = df['users'].value_counts().head()
    df = round((df['users'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return x,df


# Generate a wordcloud after removing the configured stop words.
def create_wordcloud(selected_user,df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    


    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp = df[df['messages'] != '<Media omitted>\n']


    words = []

    for message in temp['messages']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)


    df_wc = wc.generate(" ".join(words))
    
    return df_wc


# Return the twenty most frequently used non-stop words.
def most_common_words(selected_user,df):

    f = open('stop_hinglish.txt','r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    temp = df[df['messages'] != '<Media omitted>\n']
  

    words = []

    for message in temp['messages']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df


# Count emoji characters used by the selected participant or whole chat.
def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    emojis = []
    for message in df['messages']:
       
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df





