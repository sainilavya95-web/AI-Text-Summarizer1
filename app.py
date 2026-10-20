import streamlit as st
from transformers import pipeline
import torch

st.set_page_config(
    page_title="AI Text Summarizer",
    page_icon="📝",
    layout="centered",
)

MODEL_NAME = "sshleifer/distilbart-cnn-12-6"


@st.cache_resource(show_spinner=False)
def load_summarizer():
    """Load the pretrained summarization pipeline once per app session."""
    device = 0 if torch.cuda.is_available() else -1
    return pipeline(
        "summarization",
        model=MODEL_NAME,
        device=device,
    )


def summarize_text(summarizer, text, length):
    """Generate a summary, splitting long text into manageable chunks."""
    settings = {
        "Short": {"max_length": 60, "min_length": 20},
        "Medium": {"max_length": 110, "min_length": 40},
        "Long": {"max_length": 170, "min_length": 70},
    }
    options = settings[length]

    # Keep chunks below the model's input token limit.
    chunks = summarizer.tokenizer(
        text,
        max_length=900,
        truncation=True,
        return_tensors=None,
    )
    input_ids = chunks["input_ids"]
    chunk_size = 700
    token_chunks = [
        input_ids[i:i + chunk_size]
        for i in range(0, len(input_ids), chunk_size)
    ]

    summaries = []
    for token_chunk in token_chunks:
        chunk_text = summarizer.tokenizer.decode(
            token_chunk,
            skip_special_tokens=True,
        ).strip()
        if not chunk_text:
            continue
        result = summarizer(
            chunk_text,
            max_length=options["max_length"],
            min_length=min(options["min_length"], max(5, len(token_chunk) // 3)),
            do_sample=False,
            truncation=True,
        )
        summaries.append(result[0]["summary_text"])

    return " ".join(summaries).strip()


st.title("📝 AI Text Summarizer")
st.write(
    "Turn a long article into a clear, shorter summary with an AI model."
)

with st.sidebar:
    st.header("About this project")
    st.write("**Built with:** Python, Streamlit, Hugging Face Transformers")
    st.write(f"**Model:** `{MODEL_NAME}`")
    st.caption(
        "The model is downloaded the first time you generate a summary. "
        "An internet connection is required for the first run."
    )

article = st.text_area(
    "Paste your English article or text",
    height=260,
    placeholder="Paste an article, blog post, or notes here...",
    help="For best results, use clear English text with at least 40 words.",
)

col1, col2 = st.columns([2, 1])
with col1:
    length = st.selectbox("Summary length", ["Short", "Medium", "Long"])
with col2:
    st.metric("Input words", len(article.split()))

if st.button("✨ Generate Summary", type="primary", use_container_width=True):
    if len(article.strip()) < 100 or len(article.split()) < 40:
        st.warning("Please enter at least 40 words (and 100 characters) to summarize.")
    else:
        try:
            with st.spinner("Loading AI model and generating your summary..."):
                summarizer = load_summarizer()
                summary = summarize_text(summarizer, article.strip(), length)

            if summary:
                st.subheader("📌 Your Summary")
                st.write(summary)
                summary_words = len(summary.split())
                original_words = len(article.split())
                reduction = max(0, (1 - summary_words / original_words) * 100)

                m1, m2 = st.columns(2)
                m1.metric("Summary words", summary_words)
                m2.metric("Approx. word reduction", f"{reduction:.1f}%")

                st.download_button(
                    "⬇️ Download summary (.txt)",
                    data=summary,
                    file_name="summary.txt",
                    mime="text/plain",
                    use_container_width=True,
                )
            else:
                st.error("The model returned an empty summary. Please try different text.")
        except Exception as exc:
            st.error("Sorry, the summary could not be generated.")
            st.info(
                "Check your internet connection and try again. "
                "The first model download may take a few minutes."
            )
            with st.expander("Technical error details"):
                st.code(str(exc))

st.divider()
st.caption(
    "Note: This demo is optimized for English news-style text. "
    "AI summaries can omit details, so verify important information."
)
