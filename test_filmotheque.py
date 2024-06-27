import filmotheque
from unittest.mock import Mock

def test_ajouter_film():
    filmotheque = filmotheque.Filmotheque()
    filmotheque.ajouter_film("123", "Inception")
    assert filmotheque.films["123"] == {'realisateur': None, 'titre': "Inception"}

def test_inscrire_utilisateur():
    filmotheque = filmotheque.Filmotheque()
    filmotheque.inscrire_utilisateur("user1")
    assert "user1" in filmotheque.utilisateurs

def test_emprunter_film():
    filmotheque = filmotheque.Filmotheque()
    filmotheque.ajouter_film("123", "Inception")
    filmotheque.inscrire_utilisateur("user1")
    filmotheque.emprunter_film("user1", "123")
    assert filmotheque.emprunts["123"] == "user1"

def test_emprunter_film_deja_emprunte():
    filmotheque = filmotheque.Filmotheque()
    filmotheque.ajouter_film("123", "Inception")
    filmotheque.inscrire_utilisateur("user1")
    filmotheque.inscrire_utilisateur("user2")
    filmotheque.emprunter_film("user1", "123")
    try:
        filmotheque.emprunter_film("user2", "123")
    except ValueError as e:
        assert str(e) == "Film déjà emprunté"

def test_retourner_film():
    filmotheque = filmotheque.Filmotheque()
    filmotheque.ajouter_film("123", "Inception")
    filmotheque.inscrire_utilisateur("user1")
    filmotheque.emprunter_film("user1", "123")
    filmotheque.retourner_film("user1", "123")
    assert "123" not in filmotheque.emprunts

def test_retourner_film_non_emprunte():
    filmotheque = filmotheque.Filmotheque()
    filmotheque.ajouter_film("123", "Inception")
    filmotheque.inscrire_utilisateur("user1")
    try:
        filmotheque.retourner_film("user1", "123")
    except ValueError as e:
        assert str(e) == "Film non emprunté"

def test_emprunter_film_utilisateur_non_inscrit():
    filmotheque = filmotheque.Filmotheque()
    filmotheque.ajouter_film("123", "Inception")
    try:
        filmotheque.emprunter_film("user1", "123")
    except ValueError as e:
        assert str(e) == "Utilisateur non inscrit"

def test_emprunter_film_non_disponible():
    filmotheque = filmotheque.Filmotheque()
    filmotheque.inscrire_utilisateur("user1")
    try:
        filmotheque.emprunter_film("user1", "123")
    except ValueError as e:
        assert str(e) == "Film non trouvé"

def test_notification_emprunt():
    notification_service = Mock()
    filmotheque = filmotheque.Filmotheque(notification_service)
    filmotheque.ajouter_film("123", "Inception")
    filmotheque.inscrire_utilisateur("user1")
    filmotheque.emprunter_film("user1", "123")
    notification_service.notifier.assert_called_with("user1", "Vous avez emprunté Inception")

def test_notification_retour():
    notification_service = Mock()
    filmotheque = filmotheque.Filmotheque(notification_service)
    filmotheque.ajouter_film("123", "Inception")
    filmotheque.inscrire_utilisateur("user1")
    filmotheque.emprunter_film("user1", "123")
    filmotheque.retourner_film("user1", "123")
    notification_service.notifier.assert_called_with("user1", "Vous avez retourné Inception")

def test_recherche_par_titre():
    filmotheque = filmotheque.Filmotheque()
    filmotheque.ajouter_film("123", "Inception")
    filmotheque.ajouter_film("124", "Inception 2")
    resultats = filmotheque.recherche(titre="Inception")
    assert len(resultats) == 2
    assert resultats[0]["id_film"] == "123"
    assert resultats[1]["id_film"] == "124"

def test_recherche_par_realisateur():
    filmotheque = filmotheque.Filmotheque()
    filmotheque.ajouter_film("123", "Inception", "Christopher Nolan")
    filmotheque.ajouter_film("124", "The Dark Knight", "Christopher Nolan")
    resultats = filmotheque.recherche(realisateur="Christopher Nolan")
    assert len(resultats) == 2
    assert resultats[0]["id_film"] == "123"
    assert resultats[1]["id_film"] == "124"

def test_recherche_disponible():
    filmotheque = filmotheque.Filmotheque()
    filmotheque.ajouter_film("123", "Inception")
    filmotheque.ajouter_film("124", "The Dark Knight")
    filmotheque.inscrire_utilisateur("user1")
    filmotheque.emprunter_film("user1", "123")
    resultats = filmotheque.recherche(disponible=True)
    assert len(resultats) == 1
    assert resultats[0]["id_film"] == "124"

def test_tri_par_titre():
    filmotheque = filmotheque.Filmotheque()
    filmotheque.ajouter_film("123", "Inception")
    filmotheque.ajouter_film("124", "The Dark Knight")
    filmotheque.ajouter_film("125", "A Beautiful Mind")
    resultats = filmotheque.recherche(tri="titre")
    assert len(resultats) == 3
    assert resultats[0]["id_film"] == "125"
    assert resultats[1]["id_film"] == "123"
    assert resultats[2]["id_film"] == "124"

def test_tri_par_realisateur():
    filmotheque = filmotheque.Filmotheque()
    filmotheque.ajouter_film("123", "Inception", "Christopher Nolan")
    filmotheque.ajouter_film("124", "The Dark Knight", "Christopher Nolan")
    filmotheque.ajouter_film("125", "A Beautiful Mind", "Ron Howard")
    resultats = filmotheque.recherche(tri="realisateur")
    assert len(resultats) == 3
    assert resultats[0]["id_film"] == "123"
    assert resultats[1]["id_film"] == "125"
    assert resultats[2]["id_film"] == "124"

def test_filtrage_et_tri():
    filmotheque = filmotheque.Filmotheque()
    filmotheque.ajouter_film("123", "Inception", "Christopher Nolan")
    filmotheque.ajouter_film("124", "The Dark Knight", "Christopher Nolan")
    filmotheque.ajouter_film("125", "A Beautiful Mind", "Ron Howard")
    filmotheque.inscrire_utilisateur("user1")
    filmotheque.emprunter_film("user1", "124")
    resultats = filmotheque.recherche(realisateur="Christopher", disponible=True, tri="titre")
    assert len(resultats) == 1
    assert resultats[0]["id_film"] == "123"
