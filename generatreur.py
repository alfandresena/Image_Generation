from diffusers import StableDiffusionPipeline
import torch
from transformers import pipeline
from pathlib import Path
import datetime

class GenerateurImage:
    def __init__(self, model_id="stabilityai/stable-diffusion-2-1"):
        """
        Initialise le générateur d'images avec Stable Diffusion.
        
        Args:
            model_id (str): L'identifiant du modèle à utiliser
        """
        self.pipe = StableDiffusionPipeline.from_pretrained(
            model_id,
            torch_dtype=torch.float16
        )
        
        # Déplacer le modèle sur GPU si disponible
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.pipe = self.pipe.to(self.device)
        
        # Initialiser le traducteur français -> anglais
        self.traducteur = pipeline("translation_fr_to_en", model="Helsinki-NLP/opus-mt-fr-en")
    
    def traduire_prompt(self, prompt_fr):
        """
        Traduit le prompt français en anglais.
        
        Args:
            prompt_fr (str): Le prompt en français
            
        Returns:
            str: Le prompt traduit en anglais
        """
        resultat = self.traducteur(prompt_fr)
        return resultat[0]['translation_text']
    
    def generer_image(self, prompt_fr, nombre_images=1, dossier_sortie="images_generees"):
        """
        Génère des images à partir d'un prompt en français.
        
        Args:
            prompt_fr (str): Le prompt en français
            nombre_images (int): Nombre d'images à générer
            dossier_sortie (str): Dossier où sauvegarder les images
            
        Returns:
            list: Liste des chemins des images générées
        """
        # Créer le dossier de sortie s'il n'existe pas
        Path(dossier_sortie).mkdir(parents=True, exist_ok=True)
        
        # Traduire le prompt en anglais
        prompt_en = self.traduire_prompt(prompt_fr)
        print(f"Prompt traduit : {prompt_en}")
        
        # Générer les images
        chemins_images = []
        for i in range(nombre_images):
            # Générer l'image
            image = self.pipe(prompt_en).images[0]
            
            # Créer un nom de fichier unique avec timestamp
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            nom_fichier = f"{dossier_sortie}/image_{timestamp}_{i}.png"
            
            # Sauvegarder l'image
            image.save(nom_fichier)
            chemins_images.append(nom_fichier)
            print(f"Image générée et sauvegardée : {nom_fichier}")
        
        return chemins_images
