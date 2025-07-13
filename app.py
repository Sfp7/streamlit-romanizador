import streamlit as st
import re
import pykakasi
import streamlit.components.v1 as components

# Configurar pykakasi
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

# Inicializar estado
if "pasted" not in st.session_state:
    st.session_state.pasted = False
if "copied" not in st.session_state:
    st.session_state.copied = False

# Título
st.title("Japanese Lyrics Romanizer")
st.write("You can upload a `.txt` file or paste lyrics manually below:")

# Uploader
uploaded_file = st.file_uploader("Upload a lyrics file (.txt)", type=["txt"])

# Título + botón de pegar alineado
col1, col2 = st.columns([6, 1])
with col1:
    st.markdown("### Paste lyrics manually")
with col2:
    if st.button("📋 Paste"):
        st.session_state.pasted = True
        components.html("""
            <script>
            navigator.clipboard.readText().then(text => {
                const textarea = window.parent.document.querySelectorAll('textarea')[0];
                textarea.value = text;
                textarea.dispatchEvent(new Event('input', { bubbles: true }));
            });
            </script>
        """, height=0)

# Mostrar mensaje de feedback
if st.session_state.pasted:
    st.success("✅ Pasted from clipboard!")

# Input
input_text = ""
if uploaded_file is not None:
    input_text = uploaded_file.read().decode("utf-8")
else:
    input_text = st.text_area("", value="", key="lyrics_input", height=200)

# Procesar al hacer click
if st.button("Romanize Lyrics") and input_text.strip():
    romanized = process_lyrics_text(input_text)

    # Título + botón copiar alineados
    col1, col2 = st.columns([6, 1])
    with col1:
        st.markdown("### Romanized Lyrics")
    with col2:
        if st.button("📄 Copy"):
            st.session_state.copied = True
            components.html(f"""
                <script>
                navigator.clipboard.writeText(`{romanized}`);
                </script>
            """, height=0)

    if st.session_state.copied:
        st.success("✅ Copied to clipboard!")

    # Mostrar resultado
    st.text_area("Result", romanized, height=500, key="output_text")

    # Descargar
    st.download_button(
        "Download romanized lyrics",
        romanized,
        file_name="romanized_lyrics.txt",
        mime="text/plain",
    )
