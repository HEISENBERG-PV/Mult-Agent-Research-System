
import streamlit as st
import os
import json
from datetime import datetime
from pathlib import Path
from pipeline import research_pipeline

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="ResearchAI | Multi-Agent Research",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: #0B0D12;
    color: #F4F4F5;
}

[data-testid="stSidebar"] {
    background: #10131A;
    border-right: 1px solid #252936;
}

[data-testid="stHeader"] {
    background: transparent;
}

h1, h2, h3 {
    font-family: 'Space Grotesk', sans-serif !important;
    color: #F4F4F5;
}

.main-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 38px;
    font-weight: 700;
    letter-spacing: -1.5px;
}

.subtitle {
    color: #9298A5;
    font-size: 14px;
}

.section-label {
    color: #A78BFA;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}

.agent-card {
    background: #161A23;
    border: 1px solid #292E3B;
    border-radius: 12px;
    padding: 18px;
    min-height: 115px;
}

.agent-name {
    color: #F4F4F5;
    font-size: 15px;
    font-weight: 600;
}

.agent-description {
    color: #9298A5;
    font-size: 12px;
    margin-top: 7px;
}

.status-dot {
    color: #4ADE80;
    font-size: 12px;
}

.report-box {
    background: #161A23;
    border: 1px solid #292E3B;
    border-radius: 14px;
    padding: 24px;
}

div.stButton > button {
    background: #A78BFA;
    color: #0B0D12;
    border: none;
    border-radius: 8px;
    font-weight: 700;
    padding: 10px 22px;
    transition: 0.2s;
}

div.stButton > button:hover {
    background: #B9A2FF;
    color: #0B0D12;
    border: none;
}

.stTextInput input, .stTextArea textarea {
    background: #161A23 !important;
    color: #F4F4F5 !important;
    border: 1px solid #303646 !important;
    border-radius: 8px !important;
}

[data-testid="stExpander"] {
    background: #121620;
    border: 1px solid #292E3B;
    border-radius: 10px;
}

hr {
    border-color: #252936;
}

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "research_result" not in st.session_state:
    st.session_state.research_result = None

if "research_history" not in st.session_state:
    st.session_state.research_history = []

if "selected_history" not in st.session_state:
    st.session_state.selected_history = None


# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def to_text(value):
    """Convert different LangChain output types into readable text."""
    if isinstance(value, str):
        return value

    if isinstance(value, dict):
        return json.dumps(value, indent=2, ensure_ascii=False, default=str)

    if hasattr(value, "content"):
        return str(value.content)

    return str(value)


def save_markdown(topic, result):
    report = to_text(result.get("report", ""))
    feedback = to_text(result.get("feedback", ""))

    content = f"""# Research Report

**Topic:** {topic}

**Generated:** {datetime.now().strftime("%d %B %Y, %I:%M %p")}

---

## Final Research Report

{report}

---

## Critic Review

{feedback}
"""
    return content


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.markdown("""
    <div style="padding: 12px 0 28px 0;">
        <div style="font-size:27px; font-weight:700;
                    font-family:Space Grotesk; color:#A78BFA;">
            ✦ ResearchAI
        </div>
        <div style="font-size:11px; color:#9298A5;">
            MULTI-AGENT RESEARCH SYSTEM
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Workspace")

    page = st.radio(
        "Navigation",
        ["New Research", "Research History", "About"],
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown("### System Status")

    st.markdown("""
    <div style="background:#161A23; padding:14px;
                border-radius:10px; border:1px solid #292E3B;">
        <div style="color:#4ADE80; font-size:13px;">
            ● System Ready
        </div>
        <div style="color:#9298A5; font-size:11px; margin-top:8px;">
            Model: Groq · GPT-OSS 120B
        </div>
        <div style="color:#9298A5; font-size:11px;">
            Architecture: Multi-Agent
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown(
        "<div style='color:#656D7D;font-size:11px;'>"
        "BUILT WITH STREAMLIT · LANGCHAIN · GROQ"
        "</div>",
        unsafe_allow_html=True
    )


# --------------------------------------------------
# NEW RESEARCH PAGE
# --------------------------------------------------

if page == "New Research":

    st.markdown(
        '<div class="section-label">INTELLIGENT RESEARCH WORKSPACE</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="main-title">What do you want to research?</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Let your AI research team search, analyze, '
        'write and review information from across the web.</div>',
        unsafe_allow_html=True
    )

    st.write("")

    topic = st.text_area(
        "Research Topic",
        placeholder="e.g. Impact of artificial intelligence on the future of healthcare...",
        height=100,
        label_visibility="collapsed"
    )

    col1, col2 = st.columns([1, 5])

    with col1:
        start_research = st.button(
            "✦ Start Research",
            use_container_width=True
        )

    with col2:
        st.caption("Powered by autonomous AI agents")

    st.write("")
    st.markdown("---")

    # AGENT OVERVIEW

    st.markdown("### Your Research Team")

    agent_cols = st.columns(4)

    agents = [
        ("🔎", "Search Agent", "Finds relevant information and web sources."),
        ("📖", "Reader Agent", "Scrapes and extracts useful content."),
        ("✍️", "Writer Agent", "Creates a structured research report."),
        ("🛡️", "Critic Agent", "Reviews the report and provides feedback.")
    ]

    for col, agent in zip(agent_cols, agents):
        with col:
            st.markdown(f"""
            <div class="agent-card">
                <div style="font-size:25px;">{agent[0]}</div>
                <div class="agent-name">{agent[1]}</div>
                <div class="agent-description">{agent[2]}</div>
            </div>
            """, unsafe_allow_html=True)

    st.write("")

    # --------------------------------------------------
    # RUN PIPELINE
    # --------------------------------------------------

    if start_research:

        if not topic.strip():
            st.warning("Please enter a research topic first.")

        else:

            st.session_state.research_result = None

            st.markdown("### Research Execution")

            progress = st.progress(0)
            status = st.empty()

            try:

                status.info("🔎 Search Agent is searching the web...")
                progress.progress(10)

                # Existing pipeline is called without modifying it.
                result = research_pipeline(topic.strip())

                progress.progress(100)
                status.success("Research pipeline completed successfully!")

                st.session_state.research_result = {
                    "topic": topic.strip(),
                    "result": result,
                    "date": datetime.now().strftime("%d %b %Y, %I:%M %p")
                }

                st.session_state.research_history.insert(
                    0,
                    st.session_state.research_result
                )

                st.success("Your research report is ready!")

            except Exception as e:
                status.error("Research execution failed.")
                st.exception(e)

    # --------------------------------------------------
    # DISPLAY RESEARCH RESULTS
    # --------------------------------------------------

    if st.session_state.research_result:

        research = st.session_state.research_result
        result = research["result"]

        st.markdown("---")
        st.markdown("## Research Results")

        st.markdown(f"**Topic:** {research['topic']}")

        # FINAL REPORT

        st.markdown("### 📝 Final Research Report")

        report = to_text(result.get("report", ""))

        with st.container(border=True):
            st.markdown(report)

        # CRITIC FEEDBACK

        st.markdown("### 🛡️ Critic Review")

        feedback = to_text(result.get("feedback", ""))

        with st.expander("View Critic Feedback", expanded=True):
            st.markdown(feedback)

        # SOURCE EXPLORER

        st.markdown("### 🔍 Research Sources")

        with st.expander("View Search Agent Output"):
            st.markdown(
                to_text(result.get("search_agent_result", "No search data available."))
            )

        with st.expander("View Scraped Content"):
            st.markdown(
                to_text(result.get("scraped_content", "No scraped content available."))
            )

        # EXPORTS

        st.markdown("---")
        st.markdown("### Export Research")

        markdown_content = save_markdown(
            research["topic"],
            result
        )

        col1, col2 = st.columns(2)

        with col1:
            st.download_button(
                label="⬇ Download Markdown",
                data=markdown_content,
                file_name="research_report.md",
                mime="text/markdown",
                use_container_width=True
            )

        with col2:
            st.download_button(
                label="⬇ Download TXT",
                data=markdown_content,
                file_name="research_report.txt",
                mime="text/plain",
                use_container_width=True
            )


# --------------------------------------------------
# RESEARCH HISTORY PAGE
# --------------------------------------------------

elif page == "Research History":

    st.markdown(
        '<div class="section-label">YOUR PREVIOUS WORK</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="main-title">Research History</div>',
                unsafe_allow_html=True)

    st.markdown(
        '<div class="subtitle">Access your previous research sessions.</div>',
        unsafe_allow_html=True
    )

    st.write("")

    if not st.session_state.research_history:

        st.info("No research history available in this session yet.")

    else:

        for index, item in enumerate(st.session_state.research_history):

            with st.expander(
                f"📄 {item['topic']}  ·  {item['date']}"
            ):

                result = item["result"]

                st.markdown("### Final Report")
                st.markdown(to_text(result.get("report", "")))

                st.markdown("### Critic Feedback")
                st.markdown(to_text(result.get("feedback", "")))

                content = save_markdown(item["topic"], result)

                st.download_button(
                    "⬇ Download Report",
                    data=content,
                    file_name=f"research_{index + 1}.md",
                    mime="text/markdown",
                    key=f"history_download_{index}"
                )


# --------------------------------------------------
# ABOUT PAGE
# --------------------------------------------------

elif page == "About":

    st.markdown(
        '<div class="section-label">ABOUT THE PROJECT</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="main-title">Multi-Agent Research System</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    ### Overview

    The Multi-Agent Research System is an AI-powered research application
    designed to automate the process of gathering, analyzing and generating
    information on a given topic.

    Instead of relying on a single AI model, the system uses multiple
    specialized agents that collaborate to produce a structured research report.

    ### Workflow

    1. **Search Agent:** Searches the internet for relevant information.
    2. **Reader Agent:** Scrapes and extracts useful information from selected sources.
    3. **Writer Agent:** Generates a structured research report.
    4. **Critic Agent:** Reviews the generated report and provides feedback.

    ### Technology Stack

    - Python
    - Streamlit
    - LangChain
    - Groq API
    - GPT-OSS 120B
    - Tavily Search API
    - BeautifulSoup

    ### Objective

    To demonstrate how multiple specialized AI agents can collaborate
    to automate complex research tasks and improve the quality of
    information generation.
    """)
