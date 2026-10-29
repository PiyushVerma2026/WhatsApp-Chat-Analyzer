import pandas as pd
import re

# Convert a WhatsApp text export into the columns used by the dashboard.
def preprocess(data):
    # Match both 24-hour timestamps and timestamps containing AM/PM.
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}(?:\s?[APap][Mm])?\s-\s'
    messages=re.split(pattern,data)[1:]
    dates=re.findall(pattern,data)

    df=pd.DataFrame({'user_message':messages,'message_date':dates})
    df['message_date'] = pd.to_datetime(
        df['message_date'].str.replace(' - ', '', regex=False),
        format='mixed'
    )
    df['message_date'] = df['message_date'].dt.strftime('%d/%m/%Y %H:%M')

    # Separate each record into participant name and message text.
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message )
        if entry[1:]:  # user nam
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['users']=users
    df['messages']=messages
    df.drop(columns=['user_message'],inplace=True)
    # Derive date, calendar, weekday, and time-period fields for analysis.
    df['message_date'] = pd.to_datetime(df['message_date'], errors='coerce')
    df['only_date'] = df['message_date'].dt.date
    df['year'] = df['message_date'].dt.year
    df['month_num'] = df['message_date'].dt.month
    df['month'] = df['message_date'].dt.month_name()
    df['day'] = df['message_date'].dt.day
    df['day_name'] = df['message_date'].dt.day_name()
    df['hour'] = df['message_date'].dt.hour
    df['period'] = df['hour'].apply(
        lambda hour: (
            f'{int(hour):02d}-{(int(hour) + 1) % 24:02d}'
            if pd.notna(hour)
            else 'Unknown'
        )
    )
    df['minute'] = df['message_date'].dt.minute
    # The original timestamp is no longer needed after derived fields exist.
    df=df.drop(columns='message_date')

    # Remove system notifications and rows without message text.
    df = df[df['users'] != 'group_notification']
    df = df[df['messages'].notna()]

    return df

