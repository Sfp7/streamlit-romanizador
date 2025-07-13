import streamlit as st
import re
import pykakasi
import streamlit.components.v1 as components

# Initialize kakasi
kks = pykakasi.kakasi()
kks.setMode("H", "a")  # Hiragana to ascii
kks.setMode("K", "a")  # Katakana to ascii
kks.setMode("J", "a")  # Kanji to ascii
kks.setMode("r", "Hepburn")  # Use Hepburn romanization
kks.setMode("s", True)  # Add spaces
converter = kks.getConverter()

def romanize_lyrics(lyrics):
    return converter.do(lyrics)

def process_lyrics_text(text):
    output_lines = []
    for line in text.splitlines():
        match = re.match(r'(\[.*?\])\s*(.*)', line)
        if match:
            timestamp = match.group(1)
            lyrics_line = match.group(2)
            romanized_lyrics = romanize_lyrics(lyrics_line)
            output_lines.append(f"{timestamp} {romanized_lyrics}")
        else:
            if line.strip():
                romanized_lyrics = romanize_lyrics(line)
                output_lines.append(romanized_lyrics)
            else:
                output_lines.append("")
    return "\n".join(output_lines)

# PAGE START
st.title("Japanese Lyrics Romanizer")

st.write("You can upload a `.txt` lyrics file or paste the lyrics manually below:")

# Upload first
uploaded_file = st.file_uploader("Upload a lyrics file (.txt)", type=["txt"])

# Title and paste button inline
st.markdown("""
<div style="display: flex; justify-content: space-between; align-items: center;">
  <h3 style="margin-bottom: 0;">Paste lyrics manually</h3>
  <button onclick="navigator.clipboard.readText().then(text => {
    const ta = window.parent.document.querySelector('textarea');
    ta.value = text;
    ta.dispatchEvent(new Event('input', { bubbles: true }));
  })">📋 Paste from clipboard</button>
</div>
""", unsafe_allow_html=True)

input_text_key = "lyrics_input"
input_text = ""

if uploaded_file is not None:
    input_text = uploaded_file.read().decode("utf-8")
else:
    input_text = st.text_area("", value="", key=input_text_key, height=200)

# Process text
if st.button("Romanize Lyrics") and input_text.strip():
    romanized = process_lyrics_text(input_text)

    # Header with copy button inline
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center;">
      <h3 style="margin-bottom: 0;">Romanized Lyrics</h3>
      <button onclick="navigator.clipboard.writeText(document.querySelector('textarea[aria-label=Result]').value)">📄 Copy to clipboard</button>
    </div>
    """, unsafe_allow_html=True)

    st.text_area("Result", romanized, height=500, key="output_text")  # Increased height

    # Download button
    st.download_button(
        "Download romanized lyrics",
        romanized,
        file_name="romanized_lyrics.txt",
        mime="text/plain",
    )
