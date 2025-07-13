import streamlit as st
import re
import pykakasi
import streamlit.components.v1 as components

# Inicializar kakasi
kks = pykakasi.kakasi()
kks.setMode("H", "a")
kks.setMode("K", "a")
kks.setMode("J", "a")
kks.setMode("r", "Hepburn")
kks.setMode("s", True)
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

# Título
st.title("Japanese Lyrics Romanizer")

st.write("You can upload a `.txt` lyrics file or paste the lyrics manually below:")

# Uploader
uploaded_file = st.file_uploader("Upload a lyrics file (.txt)", type=["txt"])

# Input title and paste aligned horizontally
col1, col2 = st.columns([6, 1])
with col1:
    st.markdown("### Paste lyrics manually")
with col2:
    if st.button("📋 Paste from clipboard"):
        components.html("""
            <script>
            navigator.clipboard.readText().then(text => {
                const ta = window.parent.document.querySelectorAll('textarea')[0];
                ta.value = text;
                ta.dispatchEvent(new Event('input', { bubbles: true }));
            });
            </script>
        """, height=0)

# Text input
input_text = ""
if uploaded_file is not None:
    input_text = uploaded_file.read().decode("utf-8")
else:
    input_text = st.text_area("", value="", key="lyrics_input", height=200)

# Process
if st.button("Romanize Lyrics") and input_text.strip():
    romanized = process_lyrics_text(input_text)

    # Output title + copy aligned
    col1, col2 = st.columns([6, 1])
    with col1:
        st.markdown("### Romanized Lyrics")
    with col2:
        if st.button("📄 Copy to clipboard"):
            components.html(f"""
                <script>
                navigator.clipboard.writeText(`{romanized}`);
                </script>
            """, height=0)
            st.success("Copied to clipboard!")

    # Result textarea
    st.text_area("Result", romanized, height=500, key="output_text")

    # Download button
    st.download_button(
        "Download romanized lyrics",
        romanized,
        file_name="romanized_lyrics.txt",
        mime="text/plain",
    )
