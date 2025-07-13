import streamlit as st
import re
import pykakasi
import streamlit.components.v1 as components

# Inicializar pykakasi
kks = pykakasi.kakasi()
kks.setMode("H", "a")  # Hiragana a romaji
kks.setMode("K", "a")  # Katakana a romaji
kks.setMode("J", "a")  # Kanji a romaji
kks.setMode("r", "Hepburn")  # Romanización estilo Hepburn
kks.setMode("s", True)  # Separar palabras
converter = kks.getConverter()

# Función que romaniza una línea completa
def romanize_lyrics(lyrics):
    return converter.do(lyrics)

# Procesa el texto: con o sin timestamp
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
st.title("Romanizador de lyrics japoneses")

st.write("Puedes subir un archivo de lyrics (.txt) o ingresar los lyrics directamente:")

# Botón para pegar desde el portapapeles
st.markdown("### Pega los lyrics aquí")
paste = st.button("📋 Pegar desde portapapeles")

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

# Área de entrada
uploaded_file = st.file_uploader("Sube tu archivo de lyrics (.txt)", type=["txt"])
input_text = ""

if uploaded_file is not None:
    input_text = uploaded_file.read().decode("utf-8")
else:
    input_text = st.text_area("", value="", key=input_text_key, height=200)

# Procesamiento al presionar botón
if st.button("Romanizar lyrics") and input_text.strip():
    romanized = process_lyrics_text(input_text)

    st.subheader("Lyrics romanizados")

    # Área de resultado con botón de copiar
    st.text_area("Lyrics romanizados", romanized, height=400, key="output_text")

    if st.button("📄 Copiar romanizados al portapapeles"):
        components.html(f"""
            <script>
            navigator.clipboard.writeText(`{romanized}`);
            </script>
        """, height=0)
        st.success("¡Copiado al portapapeles!")

    # Botón para descargar
    st.download_button(
        "Descargar archivo romanizado",
        romanized,
        file_name="lyrics_romanizados.txt",
        mime="text/plain",
    )

