class Filmotheque:class Filmotheque:
    def __init__(self, notification_service=None):
        self.films = {}
        
        self.films = {}
        self.utilisateurs = set()
        self.emprunts = {}
        self.notification_service = notification_service

    def ajouter_film(self, id_film, titre, realisateur=None):
        self.films[id_film] = {"titre": titre, "realisateur": realisateur}

    def inscrire_utilisateur(self, utilisateur_id):
        self.utilisateurs.add(utilisateur_id)

    def emprunter_film(self, utilisateur_id, id_film):
        if id_film not in self.films:
            raise ValueError("Film non trouvé")
        if id_film in self.emprunts:
            raise ValueError("Film déjà emprunté")
        if utilisateur_id not in self.utilisateurs:
            raise ValueError("Utilisateur non inscrit")
        self.emprunts[id_film] = utilisateur_id
        if self.notification_service:
            self.notification_service.notifier(utilisateur_id, f"Vous avez emprunté {self.films[id_film]['titre']}")

    def retourner_film(self, utilisateur_id, id_film):
        if id_film not in self.emprunts:
            raise ValueError("Film non emprunté")
        if self.emprunts[id_film] != utilisateur_id:
            raise ValueError("Ce film n'a pas été emprunté par cet utilisateur")
        del self.emprunts[id_film]
        if self.notification_service:
            self.notification_service.notifier(utilisateur_id, f"Vous avez retourné {self.films[id_film]['titre']}")

    def recherche(self, titre=None, realisateur=None, disponible=None, tri=None):
        resultats = []
        for id_film, details in self.films.items():
            if titre and titre.lower() not in details["titre"].lower():
                continue
            if realisateur and realisateur.lower() not in details.get("realisateur", "").lower():
                continue
            if disponible is not None:
                if disponible and id_film in self.emprunts:
                    continue
                if not disponible and id_film not in self.emprunts:
                    continue
            resultats.append({"id_film": id_film, "titre": details["titre"], "realisateur": details.get("realisateur")})

        if tri:
            resultats = sorted(resultats, key=lambda x: x[tri])

        return resultats
