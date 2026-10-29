# Standard library and visualization imports.
from pathlib import Path
import zipfile
import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns


# Configure the browser page before rendering any Streamlit elements.
st.set_page_config(
    page_title="WhatsApp Chat Analyzer",
    page_icon="💬",
    layout="wide"
)

# Global styles for the dashboard, cards, banners, and footer.
st.markdown("""
<style>
    .stApp {
        background: #f5f7fb;
    }
    .hero {
        padding: 2rem 2.25rem;
        border-radius: 1.25rem;
        background: linear-gradient(135deg, #102a43 0%, #1f6f8b 100%);
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 25px rgba(16, 42, 67, 0.15);
    }
    .hero h1 {
        margin: 0;
        font-size: 2.4rem;
    }
    .hero p {
        margin: 0.5rem 0 0;
        color: #d9f0f7;
    }
    .section-title {
        color: #102a43;
        font-size: 1.45rem;
        font-weight: 700;
        margin: 1.25rem 0 1rem;
    }
    .metric-card {
        padding: 1rem 1.15rem;
        border-radius: 1rem;
        background: white;
        border: 1px solid #d9e2ec;
        box-shadow: 0 5px 16px rgba(16, 42, 67, 0.07);
    }
    .metric-label {
        color: #627d98;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .metric-value {
        color: #102a43;
        font-size: 1.85rem;
        font-weight: 800;
        margin-top: 0.2rem;
    }
    .footer-card {
        margin-top: 2.5rem;
        padding: 1.25rem 1.5rem;
        border-radius: 1rem;
        background: linear-gradient(135deg, #102a43 0%, #1f6f8b 100%);
        color: white;
        box-shadow: 0 10px 25px rgba(16, 42, 67, 0.15);
    }
    .footer-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
    }
    .footer-title {
        font-size: 1.05rem;
        font-weight: 700;
    }
    .footer-link {
        display: inline-block;
        padding: 0.55rem 1rem;
        border-radius: 0.6rem;
        background: white;
        color: #102a43 !important;
        text-decoration: none !important;
        font-weight: 700;
    }
    .footer-source {
        display: inline-block;
        margin-top: 0.9rem;
        color: #d9f0f7 !important;
        text-decoration: none !important;
        font-size: 0.9rem;
    }
    .privacy-banner {
        padding: 1rem 1.25rem;
        border-radius: 0.9rem;
        background: #e8f5e9;
        border: 1px solid #a5d6a7;
        color: #1b5e20;
        margin-bottom: 1rem;
    }
    .start-analysis-title {
        color: #102a43;
        font-size: 1.25rem;
        font-weight: 700;
        margin-bottom: 0.75rem;
    }
    [data-testid="stExpander"] summary,
    [data-testid="stExpander"] p,
    [data-testid="stExpander"] li,
    [data-testid="stExpander"] strong {
        color: #000000 !important;
    }
    [data-testid="stAlert"] p {
        color: #000000 !important;
    }
    [data-testid="stMarkdownContainer"] h3,
    [data-testid="stMarkdownContainer"] h4 {
        color: #102a43 !important;
    }
</style>
""", unsafe_allow_html=True)

# Main dashboard hero section.
st.markdown(
    """
    <div class="hero">
        <h1>WhatsApp Chat Analyzer</h1>
        <p>Discover patterns, activity, and highlights from your conversations.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Privacy notice shown before the upload control.
st.markdown(
    """
    <div class="privacy-banner">
        <strong>🔒 Your privacy matters</strong><br>
        Your chat is processed locally in this app session and is not saved by this app.
    </div>
    """,
    unsafe_allow_html=True
)

# File upload area. Both direct text exports and ZIP exports are supported.
with st.container(border=True):
    st.markdown('<div class="start-analysis-title">Start Your Analysis</div>', unsafe_allow_html=True)
    demo_path = Path(__file__).with_name('demo_chat.txt')
    use_demo = st.session_state.get('demo_chat_active', False)
    if demo_path.exists():
        st.markdown(
            '<p style="color: #000000; margin-bottom: 0.35rem;">Want to try the analyzer first?</p>',
            unsafe_allow_html=True
        )
        if st.button('Use demo chat'):
            st.session_state['demo_chat_active'] = True
            use_demo = True

    uploaded_file = st.file_uploader(
        "Upload a WhatsApp chat export",
        type=['txt', 'zip']
    )

    if uploaded_file is not None:
        st.session_state['demo_chat_active'] = False
        use_demo = False

# Explain how to export a chat when no file has been selected yet.
if uploaded_file is None and not use_demo:
    st.info("Upload a WhatsApp chat ZIP or TXT file.")

    with st.expander("How to export a WhatsApp chat"):
        st.markdown(
            """
            **Android**

            1. Open the WhatsApp chat.
            2. Tap **⋮ → More → Export chat**.
            3. Choose **Without media**.
            4. Save or upload the `.txt` file or original `.zip` file.

            **iPhone**

            1. Open the WhatsApp chat.
            2. Tap the contact or group name.
            3. Tap **Export Chat**.
            4. Choose **Without Media**.
            5. Save or upload the `.txt` file or original `.zip` file.
            """
        )
elif uploaded_file is not None or use_demo:
    # Read the uploaded text directly or locate the first text file in a ZIP.
    if use_demo:
        data = demo_path.read_text(encoding='utf-8', errors='replace')
    elif uploaded_file.name.lower().endswith('.zip'):
        with zipfile.ZipFile(uploaded_file) as archive:
            text_files = [
                name for name in archive.namelist()
                if name.lower().endswith('.txt')
            ]

            if not text_files:
                st.error('No text file found inside the ZIP file.')
                st.stop()

            data = archive.read(text_files[0]).decode(
                'utf-8',
                errors='replace'
            )
    else:
        data = uploaded_file.getvalue().decode(
            'utf-8',
            errors='replace'
        )

    # Parse the uploaded export into an analysis DataFrame.
    df = preprocessor.preprocess(data)
    df = preprocessor.preprocess(data)

    user_list = df['users'].unique().tolist()
    user_list.sort()
    user_list.insert(0, "Overall")

    # Keep participant selection and the analysis action together.
    control_col, button_col = st.columns([3, 1])
    with control_col:
        selected_user = st.selectbox("Analyze messages from", user_list)
    with button_col:
        st.write("")
        st.write("")
        show_analysis = st.button("✨ Show Analysis", use_container_width=True)
        if use_demo and selected_user == 'Overall':
            show_analysis = True

    if show_analysis:
        # Render the complete analysis as one continuous notebook-style page.
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)

        st.markdown(
            f"<div class='section-title'>Overview <span style='color:#627d98;font-size:0.9rem;font-weight:500;'>· {selected_user}</span></div>",
            unsafe_allow_html=True
        )

        metric_columns = st.columns(4)
        metric_data = [
            ("Total Messages", f"{num_messages:,}", "💬"),
            ("Total Words", f"{words:,}", "📝"),
            ("Media Shared", f"{num_media_messages:,}", "🖼️"),
            ("Links Shared", f"{num_links:,}", "🔗")
        ]
        for column, (label, value, icon) in zip(metric_columns, metric_data):
            with column:
                st.markdown(
                    f"""
                    <div class="metric-card">
                        <div class="metric-label">{icon} {label}</div>
                        <div class="metric-value">{value}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        st.markdown('<div class="section-title">Conversation Timeline</div>', unsafe_allow_html=True)
        timeline_col, daily_col = st.columns(2)

        with timeline_col:
            with st.container(border=True):
                st.subheader("Messages Over Months")
                timeline = helper.monthly_timeline(selected_user, df)
                fig, ax = plt.subplots()
                ax.plot(timeline['time'], timeline['messages'], color='green')
                ax.set_xlabel('Month')
                ax.set_ylabel('Number of Messages')
                ax.set_axisbelow(True)
                ax.grid(zorder=0)
                plt.xticks(rotation='vertical')
                st.pyplot(fig, use_container_width=True)

        with daily_col:
            with st.container(border=True):
                st.subheader("Messages by Date")
                daily_timeline = helper.daily_timeline(selected_user, df)
                fig, ax = plt.subplots()
                ax.plot(daily_timeline['only_date'], daily_timeline['messages'], color='black')
                ax.xaxis.set_major_locator(mdates.AutoDateLocator())
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
                fig.autofmt_xdate()
                plt.setp(
                    ax.get_xticklabels(),
                    rotation=90,
                    ha='center'
                )
                ax.set_xlabel('Date')
                ax.set_ylabel('Number of Messages')
                ax.set_axisbelow(True)
                ax.grid(zorder=0)
                st.pyplot(fig, use_container_width=True)

        st.markdown('<div class="section-title">Activity Map</div>', unsafe_allow_html=True)
        activity_col, month_col = st.columns(2)

        with activity_col:
            with st.container(border=True):
                st.subheader("Messages by Day of Week")
                busy_day = helper.week_activity_map(selected_user, df)
                fig, ax = plt.subplots()
                ax.bar(busy_day.index, busy_day.values, color='purple')
                ax.set_xlabel('Day')
                ax.set_ylabel('Number of Messages')
                ax.set_axisbelow(True)
                ax.grid(zorder=0)
                plt.xticks(rotation='vertical')
                st.pyplot(fig, use_container_width=True)

        with month_col:
            with st.container(border=True):
                st.subheader("Messages by Month")
                busy_month = helper.month_activity_map(selected_user, df)
                fig, ax = plt.subplots()
                ax.bar(busy_month.index, busy_month.values, color='orange')
                ax.set_xlabel('Month')
                ax.set_ylabel('Number of Messages')
                ax.set_axisbelow(True)
                ax.grid(zorder=0)
                plt.xticks(rotation='vertical')
                st.pyplot(fig, use_container_width=True)

        with st.container(border=True):
            st.subheader("Messages by Day and Time")
            user_heatmap = helper.activity_heatmap(selected_user, df)
            fig, ax = plt.subplots(figsize=(12, 6))
            sns.heatmap(
                user_heatmap,
                ax=ax,
                cmap="YlGnBu",
                annot=True,
                fmt=".0f",
                linewidths=0.5,
                linecolor="white"
            )
            ax.set_xlabel('Time Period')
            ax.set_ylabel('Day')
            st.pyplot(fig, use_container_width=True)

        st.markdown('<div class="section-title">Participant Insights</div>', unsafe_allow_html=True)
        if selected_user == 'Overall':
            chart_col, table_col = st.columns([1.4, 1])
            x, new_df = helper.most_busy_users(df)

            with chart_col:
                with st.container(border=True):
                    st.subheader("Top Participants by Message Count")
                    fig, ax = plt.subplots(figsize=(12, 6))
                    ax.bar(x.index, x.values, color='red')
                    ax.set_xlabel('Users')
                    ax.set_ylabel('Number of Messages')
                    ax.set_axisbelow(True)
                    ax.grid(zorder=0)
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig, use_container_width=True)

            with table_col:
                with st.container(border=True):
                    st.subheader("Participant Share")
                    new_df.columns = ['User', 'Percentage']
                    new_df.index = range(1, len(new_df) + 1)
                    st.dataframe(
                        new_df.style.format({'Percentage': '{:,.2f}%'}),
                        use_container_width=True
                    )
        else:
            st.info("Select Overall to view the participant comparison.")

        st.markdown('<div class="section-title">Content Insights</div>', unsafe_allow_html=True)
        with st.container(border=True):
            st.subheader("Most Used Words Wordcloud")
            df_wc = helper.create_wordcloud(selected_user, df)
            fig, ax = plt.subplots()
            ax.imshow(df_wc)
            ax.axis('off')
            st.pyplot(fig, use_container_width=True)

        with st.container(border=True):
            st.subheader("Most Frequently Used Words")
            most_common_df = helper.most_common_words(selected_user, df)
            fig, ax = plt.subplots()
            ax.set_axisbelow(True)
            ax.grid(zorder=0)
            ax.barh(most_common_df[0], most_common_df[1], zorder=2)
            ax.set_xlabel('Number of Occurrences')
            ax.set_ylabel('Words')
            st.pyplot(fig, use_container_width=True)

        st.markdown('<div class="section-title">Emoji Insights</div>', unsafe_allow_html=True)
        emoji_df = helper.emoji_helper(selected_user, df)
        table_col, chart_col = st.columns([1, 1.2])

        with table_col:
            with st.container(border=True):
                st.subheader("Emoji Counts")
                emoji_df.columns = ['Emoji', 'Count']
                emoji_df.index = range(1, len(emoji_df) + 1)
                st.dataframe(
                    emoji_df.style.format({'Count': '{:,}'}),
                    use_container_width=True
                )

        with chart_col:
            with st.container(border=True):
                st.subheader("Emoji Usage Distribution")
                emoji_data = emoji_df.head(5)
                fig, ax = plt.subplots(figsize=(8, 8))
                ax.pie(
                    emoji_data['Count'],
                    labels=emoji_data['Emoji'],
                    autopct="%1.2f%%",
                    textprops={
                        "fontname": "Segoe UI Emoji",
                        "fontsize": 16
                    }
                )
                st.pyplot(fig, use_container_width=True)

st.markdown(
    """
    <div class="footer-card">
        <div class="footer-row">
            <div class="footer-title">Want to see more work?</div>
            <a class="footer-link" href="https://portfoliopiyushverma.vercel.app/" target="_blank">
                Piyush Verma Portfolio ↗
            </a>
        </div>
        <a class="footer-source" href="https://github.com/PiyushVerma2026/WhatsApp-Chat-Analyzer">View source code</a>
    </div>
    """,
    unsafe_allow_html=True
)
