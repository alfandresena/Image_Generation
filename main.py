def main():
    # Exemple d'utilisation
    generateur = GenerateurImage()
    
    while True:
        # Demander le prompt à l'utilisateur
        prompt = input("Image d'une chat")
        
        if prompt.lower() == 'q':
            break
            
        # Demander le nombre d'images
        try:
            nombre = int(input("Combien d'images voulez-vous générer ? (1-5) : "))
            nombre = max(1, min(5, nombre))  # Limiter entre 1 et 5
        except ValueError:
            nombre = 1
            print("Nombre invalide, génération d'une seule image.")
        
        try:
            # Générer les images
            chemins = generateur.generer_image(prompt, nombre)
            print(f"\n{len(chemins)} image(s) générée(s) avec succès!")
            
        except Exception as e:
            print(f"Une erreur est survenue : {str(e)}")

if __name__ == "__main__":
    main()