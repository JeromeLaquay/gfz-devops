# GFZ Online

Site web du **Groupe Français des Zéolithes** : frontend Nuxt 3 et API Spring Boot, avec pipeline CI/CD et déploiement sur Kubernetes (K3s).

---

## Structure du projet

| Dossier / Fichier | Description |
|-------------------|-------------|
| `frontend/` | Application Nuxt 3 (Vue 3, Tailwind CSS) |
| `backend/` | API Spring Boot (Java 17), JWT, PostgreSQL |
| `k8s/` | Manifests Kubernetes (dev, test, prod, infra) |
| `gitlab/` | Déploiement GitLab (Docker Compose) |
| `init/` | Scripts SQL d'initialisation BDD |
| `scripts/` | Outils (import actualités, conversion images, etc.) |
| `docs/` | Documentation (gestion des documents, etc.) |
| `.gitlab-ci.yml` | Pipeline CI/CD (build, test, déploiements) |
| `docker-compose.yml` | Lancement local frontend + backend + PostgreSQL |

---

## Prérequis

- **Frontend :** Node.js 18+, npm ou yarn
- **Backend :** Java 17+, Maven 3.6+
- **Optionnel (K8s) :** kubectl, cluster K3s, registry Docker

---

## Développement local

### Backend

```bash
cd backend
mvn clean install
mvn spring-boot:run
```

→ API sur `http://localhost:8080`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

→ Interface sur `http://localhost:3000`

### Avec Docker Compose (tout en un)

```bash
docker-compose up -d
```

---

## Compte par défaut (dev)

- **Username :** `admin`
- **Password :** `admin123`

---

## Pipeline CI/CD (GitLab)

| Stage | Déclencheur | Rôle |
|-------|-------------|------|
| **build** | `main`, `develop` | Build Docker frontend/backend, push vers le registry |
| **test** | `main`, `develop` | `mvn test` (backend) |
| **deploy-dev** | `develop` | Mise à jour des déploiements dans le namespace `dev` |
| **deploy-test** | `main` | Mise à jour des déploiements dans le namespace `test` |
| **deploy-prod** | `main` | **Manuel** — déploiement en `prod` |

Variables utilisées : `REGISTRY`, `FRONTEND_IMAGE`, `BACKEND_IMAGE`. Secrets (DB, JWT, mail) via variables GitLab et Secret K8s.

---

## Déploiement Kubernetes (K3s)

- **Namespaces :** `dev`, `test`, `prod`, `infra`
- **Registry :** déploiement dans `infra` (Service NodePort), config dans `/etc/rancher/k3s/registries.yaml` pour accès HTTP.
- **Environnements :**
  - Dev : `http://dev.gfz.local`
  - Test : `http://test.gfz.local`
  - Prod : `http://gfz.local`

Appliquer les manifests (après création des namespaces) :

```bash
kubectl apply -f k8s/namespaces/
kubectl apply -f k8s/infra/
kubectl apply -f k8s/dev/   # ou test/, prod/
```

---

## Fonctionnalités

- Authentification JWT
- Inscription newsletter, envoi d'emails (config SMTP)
- Gestion actualités, offres d'emploi, documents
- Interface responsive (Tailwind CSS)

---

## Documentation complémentaire

- `DEVIS_DEPLOIEMENT.md` — Devis / déploiement
- `docs/` — Gestion des documents
- `scripts/` — Guides d'utilisation des scripts d'import et de conversion
