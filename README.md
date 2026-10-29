# 💬 WhatsApp Chat Analyzer

> A privacy-conscious WhatsApp export analyzer with a polished Streamlit dashboard and a standalone Jupyter Notebook workflow.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?style=for-the-badge&logo=jupyter&logoColor=white)

## ✨ Overview

WhatsApp Chat Analyzer turns a WhatsApp text export into useful conversation insights. Upload a `.txt` export or a `.zip` file containing one, then explore message activity, participants, words, links, media, and emojis.

The project also includes [`standalone_whatsapp_analysis.ipynb`](standalone_whatsapp_analysis.ipynb), which contains the same analysis workflow without a UI framework.

## 🚀 Features

- Upload WhatsApp `.txt` exports directly.
- Upload `.zip` exports and automatically read the included text file.
- Filter analysis by participant or view the complete chat.
- View total messages, words, media messages, and shared links.
- Explore monthly and daily timelines.
- Compare activity by weekday and month.
- Inspect a complete 24-hour activity heatmap.
- Identify the busiest participants.
- Generate a Hindi/English-aware wordcloud using `stop_hinglish.txt`.
- Find the most frequently used words.
- Analyse emoji usage with counts and a chart.
- Run the same analysis cell by cell in Jupyter.

## 🖼️ Dashboard Preview

Add a screenshot here when you are ready:

```text
screenshots/dashboard.png
```

## 📁 Project Structure

```text
WCA/
├── main.py                              # Streamlit dashboard
├── preprocessor.py                      # WhatsApp export parsing
├── helper.py                            # Analysis and chart data functions
├── standalone_whatsapp_analysis.ipynb   # UI-free notebook workflow
├── stop_hinglish.txt                    # Stop words for text analysis
├── chat.txt                             # Example chat export
└── README.md                            # Project documentation
```

## ⚙️ Installation

Create and activate a virtual environment if desired, then install the dependencies:

```bash
pip install streamlit pandas matplotlib seaborn wordcloud urlextract emoji jupyter
```

## ▶️ Run the Streamlit App Locally

From the project directory:

```bash
streamlit run main.py
```

Upload a WhatsApp `.txt` file or a `.zip` file containing a `.txt` export, select a participant, and click **Show Analysis**.

## ☁️ Deploy on Streamlit Community Cloud

Vercel does not start Streamlit servers. Deploy this project through [Streamlit Community Cloud](https://share.streamlit.io/):

1. Push this project to a GitHub repository.
2. Confirm that `main.py`, `helper.py`, `preprocessor.py`, `stop_hinglish.txt`, and `requirements.txt` are committed.
3. Open Streamlit Community Cloud and choose **Create app**.
4. Select your GitHub repository and branch.
5. Set the app entrypoint to `main.py`.
6. Deploy the app.

Streamlit Community Cloud installs the packages listed in `requirements.txt` and runs `main.py` as the app entrypoint.

## 📓 Run the Standalone Notebook

Start Jupyter:

```bash
jupyter notebook
```

Then open:

```text
standalone_whatsapp_analysis.ipynb
```

Run the cells from top to bottom. To analyse another export, update the `chat_path` value in the notebook.

## 📱 Export a WhatsApp Chat

### Android

1. Open the WhatsApp chat.
2. Tap **⋮ → More → Export chat**.
3. Choose **Without media**.
4. Save the `.txt` file or upload the original `.zip` file.

### iPhone

1. Open the WhatsApp chat.
2. Tap the contact or group name.
3. Tap **Export Chat**.
4. Choose **Without Media**.
5. Save the `.txt` file or upload the original `.zip` file.

## 🔒 Privacy

The application is designed to process the uploaded chat locally during the app session. The project does not include a database or cloud-storage layer for saving chat exports.

Avoid sharing exports that contain sensitive personal information.

## 🛠️ Technologies

- Python
- Streamlit
- Pandas
- Matplotlib
- Seaborn
- WordCloud
- URLExtract
- Emoji
- Jupyter Notebook

## 👤 Author

[Piyush Verma Portfolio ↗](https://portfoliopiyushverma.vercel.app/)

View source code: `https://github.com/PiyushVerma2026/WhatsApp-Chat-Analyzer `



