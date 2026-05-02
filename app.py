import streamlit as st
from PIL import Image
import google.generativeai as genai
import sys

# --- 1. CONFIGURATION SÉCURISÉE ---
st.set_page_config(page_title="PALM-INTELLIGENCE", layout="wide", page_icon="🌿")

try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error("⚠️ Erreur : La clé API n'est pas configurée dans les Secrets Streamlit.")
    st.stop()

# --- 2. BARRE DE DIAGNOSTIC ---
with st.sidebar:
    st.header("🛠️ Diagnostic Système")
    try:
        import google.generativeai as pkg
        st.write(f"**Version SDK GenAI :** {pkg.__version__}")
        
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        st.write("**Modèles détectés par la clé :**")
        st.dataframe(models) 
        
        # --- LA MODIFICATION EST ICI : ON CIBLE LA GÉNÉRATION 2.5 ---
        best_model = "gemini-2.5-flash" # Fallback par défaut
        if "models/gemini-2.5-flash" in models:
            best_model = "gemini-2.5-flash"
        elif "models/gemini-2.0-flash" in models:
            best_model = "gemini-2.0-flash"
        elif "models/gemini-1.5-flash" in models:
            best_model = "gemini-1.5-flash"
            
        st.success(f"**Modèle sélectionné :** {best_model}")
            
    except Exception as e:
        st.error(f"Erreur de diagnostic: {e}")
        best_model = "gemini-2.5-flash" 

# --- 3. INTERFACE PRINCIPALE ---
st.title("🌿 PALM-INTELLIGENCE")
st.markdown("### Moteur d'Analyse Agronomique Connecté")
st.divider()

uploaded_file = st.file_uploader("Insérez une photographie de la parcelle...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    col_img, col_res = st.columns([1, 1.5])
    
    with col_img:
        img = Image.open(uploaded_file)
        st.image(img, caption='Image acquise par drone', use_column_width=True)
        
    with col_res:
        st.subheader("Diagnostic IA en Direct")
        
        if st.button("Lancer l'Analyse Cloud", type="primary"):
            with st.spinner(f"Analyse avec le moteur {best_model}..."):
                
                prompt = """
                Tu es le moteur IA du projet "PALM-INTELLIGENCE" en Côte d'Ivoire. 
                Tu es un expert agronome de classe mondiale spécialisé dans le palmier à huile.
                Analyse attentivement cette image.
                Utilise le formatage suivant avec ces 5 titres exacts en gras :
                
                1. STATUT DE LA PLANTE : [Indique si c'est Sain, Carence, Maladie, ou Stress]
                2. OBSERVATIONS VISUELLES : [Décris les anomalies colorimétriques ou structurelles]
                3. DIAGNOSTIC CLINIQUE : [Donne la pathologie ou la carence exacte]
                4. PRESCRIPTION D'INTRANTS : [Propose le traitement chimique précis si inévitable]
                5. MODULE PALM-CIRCULAR : [Explique comment réutiliser les rafles de palmiers ou la biomasse pour corriger ce problème de façon organique]
                """
                
                try:
                    model = genai.GenerativeModel(best_model)
                    response = model.generate_content([prompt, img])
                    
                    st.success("Rapport généré avec succès.")
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"Erreur IA détaillée : {e}")
       # Code à ajouter tout à la fin de app.py
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_view_content=True)
