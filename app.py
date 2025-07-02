import streamlit as st
import pandas as pd
import re
from datetime import datetime
import io
from typing import List, Dict

def parse_experience(experience_text: str, row_id: int, nom: str, prenom: str) -> List[Dict]:
    """
    Extraire les expériences professionnelles à partir du texte brut.
    Retourne une liste de dictionnaires contenant les informations structurées.
    """
    experiences = []

    # Diviser le texte en blocs d'expérience (chaque expérience contient typiquement 3 lignes)
    lines = experience_text.strip().split('\n')

    i = 0
    while i < len(lines):
        # Ignorer les lignes vides
        if not lines[i].strip():
            i += 1
            continue

        # Première ligne contient généralement le titre et l'entreprise
        position_company = lines[i].strip()
        position = ''
        company = ''

        # Extraction de la position et de l'entreprise (séparées par un tiret)
        if ' - ' in position_company:
            parts = position_company.split(' - ', 1)
            position = parts[0].strip()
            company = parts[1].strip()
        else:
            position = position_company

        i += 1
        if i >= len(lines):
            break

        # Deuxième ligne contient généralement les dates
        dates = lines[i].strip()
        length = ''

        # Extraction des dates
        date_pattern = r'(\d{2}/\d{2}/\d{4})\s*-\s*(\d{2}/\d{2}/\d{4})'
        date_match = re.search(date_pattern, dates)

        if date_match:
            start_date = date_match.group(1)
            end_date = date_match.group(2)

            # Calcul de la durée
            try:
                start = datetime.strptime(start_date, "%d/%m/%Y")
                end = datetime.strptime(end_date, "%d/%m/%Y")

                # Calcul de la durée en années et mois
                diff_months = (end.year - start.year) * 12 + (end.month - start.month)
                years = diff_months // 12
                months = diff_months % 12

                if years > 0 and months > 0:
                    length = f"{years} an{'s' if years > 1 else ''} {months} mois"
                elif years > 0:
                    length = f"{years} an{'s' if years > 1 else ''}"
                else:
                    length = f"{months} mois"
            except:
                length = "Durée non déterminée"

        i += 1
        if i >= len(lines):
            break

        # Troisième ligne contient généralement la localisation
        location = lines[i].strip()

        i += 1

        # Ajouter cette expérience à la liste
        experiences.append({
            'ID': f"{row_id}_{len(experiences)+1}",
            'Nom': nom,
            'Prénom': prenom,
            'Rôle': position,
            'Entreprise': company,
            'Localisation': location,
            'Durée': length
        })

    return experiences

def process_uploaded_file(uploaded_file) -> pd.DataFrame:
    """
    Traiter un fichier Excel uploadé et retourner un DataFrame avec les données structurées.
    """
    try:
        # Lire le fichier Excel avec skiprows=2
        df = pd.read_excel(uploaded_file, skiprows=2)
        
        # Vérifier que les colonnes nécessaires existent
        required_columns = ['EXPÉRIENCES', 'NOM', 'PRÉNOM(S)']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            st.error(f"Colonnes manquantes dans le fichier: {', '.join(missing_columns)}")
            st.info(f"Colonnes disponibles: {', '.join(df.columns.tolist())}")
            return None

        # Initialiser une liste pour stocker les données extraites
        parsed_data = []

        # Traiter chaque ligne
        for index, row in df.iterrows():
            if pd.notna(row['EXPÉRIENCES']):
                # Extraire le nom et prénom
                nom = str(row['NOM']) if pd.notna(row['NOM']) else ''
                prenom = str(row['PRÉNOM(S)']) if pd.notna(row['PRÉNOM(S)']) else ''
                
                experiences = parse_experience(str(row['EXPÉRIENCES']), index, nom, prenom)
                parsed_data.extend(experiences)

        # Créer un DataFrame avec les données extraites
        result_df = pd.DataFrame(parsed_data)
        return result_df
        
    except Exception as e:
        st.error(f"Erreur lors du traitement du fichier: {str(e)}")
        return None

def main():
    st.set_page_config(
        page_title="Extracteur d'Expériences Alumni",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("📊 Extracteur d'Expériences Alumni")
    st.markdown("---")
    
    # Sidebar avec instructions
    with st.sidebar:
        st.header("📋 Instructions")
        st.markdown("""
        1. **Format requis du fichier Excel:**
           - Le fichier doit avoir 2 lignes d'en-tête à ignorer
           - Colonnes nécessaires:
             - `NOM`: Nom de famille
             - `PRÉNOM(S)`: Prénom(s)
             - `EXPÉRIENCES`: Données d'expérience au format texte
        
        2. **Format des expériences:**
           - Chaque expérience sur 3 lignes:
             - Ligne 1: Poste - Entreprise
             - Ligne 2: Dates (DD/MM/YYYY - DD/MM/YYYY)
             - Ligne 3: Localisation
        
        3. **Résultat:**
           - Téléchargez le fichier Excel structuré
           - Colonnes de sortie: ID, Nom, Prénom, Rôle, Entreprise, Localisation, Durée
        """)
    
    # Interface principale
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📤 Upload du fichier")
        uploaded_file = st.file_uploader(
            "Choisissez votre fichier Excel (.xlsx)",
            type=['xlsx'],
            help="Assurez-vous que votre fichier respecte le format requis"
        )
        
        if uploaded_file is not None:
            st.success(f"Fichier uploadé: {uploaded_file.name}")
            
            # Afficher les informations du fichier
            file_details = {
                "Nom du fichier": uploaded_file.name,
                "Taille": f"{uploaded_file.size} bytes",
                "Type": uploaded_file.type
            }
            st.json(file_details)
    
    with col2:
        st.header("ℹ️ Aperçu")
        if uploaded_file is not None:
            try:
                # Lire les premières lignes pour l'aperçu
                preview_df = pd.read_excel(uploaded_file, skiprows=2, nrows=3)
                st.dataframe(preview_df)
            except Exception as e:
                st.error(f"Impossible de prévisualiser: {str(e)}")
    
    # Traitement du fichier
    if uploaded_file is not None:
        st.markdown("---")
        st.header("🔄 Traitement")
        
        if st.button("🚀 Traiter le fichier", type="primary"):
            with st.spinner("Traitement en cours..."):
                result_df = process_uploaded_file(uploaded_file)
                
                if result_df is not None and not result_df.empty:
                    st.success(f"✅ Traitement terminé! {len(result_df)} expériences extraites.")
                    
                    # Afficher un aperçu des résultats
                    st.subheader("📋 Aperçu des résultats")
                    st.dataframe(result_df.head(10))
                    
                    # Statistiques
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total expériences", len(result_df))
                    with col2:
                        st.metric("Personnes uniques", result_df['Nom'].nunique())
                    with col3:
                        st.metric("Entreprises uniques", result_df['Entreprise'].nunique())
                    with col4:
                        st.metric("Localisations uniques", result_df['Localisation'].nunique())
                    
                    # Téléchargement
                    st.markdown("---")
                    st.header("📥 Téléchargement")
                    
                    # Convertir en Excel pour le téléchargement
                    output = io.BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        result_df.to_excel(writer, index=False, sheet_name='Expériences')
                    excel_data = output.getvalue()
                    
                    st.download_button(
                        label="📄 Télécharger le fichier Excel traité",
                        data=excel_data,
                        file_name="experiences_extraites.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                    
                else:
                    st.error("❌ Aucune donnée n'a pu être extraite du fichier.")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666;'>"
        "🎓 Extracteur d'Expériences Alumni - Développé Par la JECC avec Streamlit"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
