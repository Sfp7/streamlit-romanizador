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

# Convert line to romaji
def romanize_lyrics(lyrics):
    return converter.do(lyrics)

# Romanize all lines with or without timestamp
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

# PAGE UI
st.title("Japanese Lyrics Romanizer")

st.write("You can upload a `.txt` lyrics file or paste the lyrics manually below:")

# File uploader comes first
uploaded_file = st.file_uploader("Upload a lyrics file (.txt)", type=["txt"])

# Paste from clipboard
st.markdown("### Paste lyrics manually")
paste = st.button("📋 Paste from clipboard")

input_text_key = "lyrics_input"
if paste:
    components.html("""
        <script>
        navigator.clipboard.readText().then(text => {
            const streamlitInput = window.parent.document.querySelectorAll('textarea')[0];
            streamlitInput.value = text;
            streamlitInput.dispatchEvent(new Event('input', { bubbles: true }));
        });
        </script>
    """, height=0)

# Show text input
input_text = ""
if uploaded_file is not None:
    input_text = uploaded_file.read().decode("utf-8")
else:
    input_text = st.text_area("", value="", key=input_text_key, height=200)

# Romanize button
if st.button("Romanize Lyrics") and input_text.strip():
    romanized = process_lyrics_text(input_text)

    # Output section with title and copy button inline
    col1, col2 = st.columns([6, 1])
    with col1:
        st.subheader("Romanized Lyrics")
    with col2:
        if st.button("📄 Copy to clipboard"):
            components.html(f"""
                <script>
                navigator.clipboard.writeText(`{romanized}`);
                </script>
            """, height=0)
            st.success("Copied to clipboard!")

    st.text_area("Result", romanized, height=400, key="output_text")

    # Download button
    st.download_button(
        "Download romanized lyrics",
        romanized,
        file_name="romanized_lyrics.txt",
        mime="text/plain",
    )

