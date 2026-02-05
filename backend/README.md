# GFZ Online - Backend

Backend Spring Boot avec authentification JWT pour le site du Groupe Français des Zéolithes.

## Prérequis

- Java 17+
- Maven 3.6+

## Installation

```bash
mvn clean install
```

## Exécution

```bash
mvn spring-boot:run
```

L'API sera accessible sur `http://localhost:8080/api`

## Utilisateur par défaut

- Username: `admin`
- Password: `admin123`

## Endpoints

### Authentification
- `POST /api/auth/login` - Connexion

### Newsletter
- `POST /api/newsletter/subscribe` - S'inscrire à la newsletter
- `POST /api/newsletter/unsubscribe?email=...` - Se désinscrire
