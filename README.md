# GFZ Online

Site web du Groupe Français des Zéolithes avec frontend Nuxt 3 et backend Spring Boot.

## Structure du projet

- `frontend/` - Application Nuxt 3 (Vue 3)
- `backend/` - API Spring Boot avec authentification JWT

## Prérequis

### Frontend
- Node.js 18+
- npm ou yarn

### Backend
- Java 17+
- Maven 3.6+

## Installation et démarrage

### Backend

```bash
cd backend
mvn clean install
mvn spring-boot:run
```

Le backend sera accessible sur `http://localhost:8080`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Le frontend sera accessible sur `http://localhost:3000`

## Utilisateur par défaut

- **Username:** `admin`
- **Password:** `admin123`

## Fonctionnalités

- Authentification JWT
- Inscription à la newsletter
- Recherche
- Interface responsive avec Tailwind CSS
