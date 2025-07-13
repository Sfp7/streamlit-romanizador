import streamlit as st
import re
import pykakasi

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
            if lyrics_line.strip():
                romanized_lyrics = romanize_lyrics(lyrics_line)
                output_lines.append(f"{timestamp} {romanized_lyrics}")
            else:
                output_lines.append(timestamp)
        else:
            output_lines.append(line)
    return "\n".join(output_lines)

st.title("Romanizador de lyrics japoneses")

st.write("Puedes subir un archivo de lyrics (.txt) o ingresar los lyrics directamente:")

uploaded_file = st.file_uploader("Sube tu archivo de lyrics (.txt)", type=["txt"])

input_text = ""

if uploaded_file is not None:
    input_text = uploaded_file.read().decode("utf-8")
else:
    input_text = st.text_area("Pega los lyrics aquí", height=200)

if st.button("Romanizar lyrics") and input_text.strip():
    romanized = process_lyrics_text(input_text)
    st.subheader("Lyrics romanizados")
    st.text_area("", romanized, height=400)  # Más alto para menos scroll

    st.download_button(
        "Descargar archivo romanizado",
        romanized,
        file_name="lyrics_romanizados.txt",
        mime="text/plain",
    )
