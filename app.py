import streamlit as st
from PIL import Image
import google.generativeai as genai

# Configuration de la clé API cachée
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Initialisation du modèle IA
model = genai.GenerativeModel('gemini-1.5-flash')

# Interface utilisateur
st.set_page_config(page_title="PALM-INTELLIGENCE", layout="wide", page_icon="🌿")
st.title("🌿 PALM-INTELLIGENCE : Analyse IA Connectée")
st.divider()

uploaded_file = st.file_uploader("Chargez une image de la plantation...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    col1, col2 = st.columns([1, 1.5])
    with col1:
        img = Image.open(uploaded_file)
        st.image(img, caption='Image prête', use_column_width=True)
        
    with col2:
        st.subheader("Diagnostic en Temps Réel")
        if st.button("Lancer l'Analyse IA", type="primary"):
            with st.spinner("L'IA analyse les pixels et génère les solutions..."):
                prompt = """
                Tu es l'IA "PALM-INTELLIGENCE", expert agronome. Analyse cette image.
                Rédige un rapport technique :
                1. STATUT GLOBAL : [Sain, Carence, ou Maladie]
                2. OBSERVATIONS : [Ce que tu vois]
                3. DIAGNOSTIC : [La cause]
                4. PLAN D'ACTION CHIMIQUE : [Engrais ou traitement]
                5. VALORISATION ORGANIQUE : [Comment utiliser des rafles/résidus pour ce problème]
                """
                try:
                    response = model.generate_content([prompt, img])
                    st.success("Analyse terminée.")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Erreur IA : {e}")
