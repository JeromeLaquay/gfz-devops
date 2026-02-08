# Déploiement Kubernetes (K3s) — GFZ Online

Ce dossier contient les manifests pour déployer l'application sur un cluster **K3s** (namespaces `dev`, `test`, `prod`, `infra`).

---

## 1. Installation de K3s

### 1.1 Prérequis

- Machine Linux (Ubuntu 22.04 recommandé)
- Droits root ou sudo
- Connexion réseau

### 1.2 Installation du serveur K3s (nœud unique)

```bash
# Téléchargement et installation en une commande
curl -sfL https://get.k3s.io | sh -

# Activer et démarrer le service
sudo systemctl enable k3s
sudo systemctl start k3s
sudo systemctl status k3s
```

### 1.3 Accès à kubectl

Le kubeconfig est écrit dans `/etc/rancher/k3s/k3s.yaml`. Pour l'utiliser :

```bash
# Option 1 : utiliser sudo pour kubectl
sudo kubectl get nodes

# Option 2 : copier le kubeconfig pour votre utilisateur
mkdir -p ~/.kube
sudo cp /etc/rancher/k3s/k3s.yaml ~/.kube/config
sudo chown $(id -u):$(id -g) ~/.kube/config
chmod 600 ~/.kube/config
kubectl get nodes
```

### 1.4 (Optionnel) Configuration du registry HTTP

Si vous utilisez un registry Docker en HTTP (ex. `registry.gfz.local:31076`), configurez K3s :

```bash
sudo mkdir -p /etc/rancher/k3s
sudo nano /etc/rancher/k3s/registries.yaml
```

Contenu type (adapter host/port) :

```yaml
mirrors:
  "registry.gfz.local:31076":
    endpoint:
      - "http://registry.gfz.local:31076"
configs:
  "registry.gfz.local:31076":
    tls:
      insecure_skip_verify: true
```

Puis redémarrer K3s :

```bash
sudo systemctl restart k3s
```

---

## 2. Application des manifests

Ordre recommandé :

```bash
# 1. Créer les namespaces (dev, test, prod)
kubectl apply -f namespaces/

# 2. Déployer l'infra (registry Docker)
kubectl apply -f infra/

# 3. Déployer un environnement (ex. dev)
kubectl apply -f dev/
# ou test/, prod/
```

Vérifications :

```bash
kubectl get namespaces
kubectl get pods -n dev
kubectl get svc -n infra
```

---

## 3. Patcher les secrets (DB_PASSWORD, JWT_SECRET, MAIL_USERNAME, MAIL_PASSWORD)

Le Secret `backend-secret` dans chaque namespace contient les données sensibles du backend. Il peut être créé par les manifests avec des valeurs par défaut, puis **patché** avec les vraies valeurs (sans les mettre en clair dans les fichiers versionnés).

### 3.1 Namespace concerné

Remplacer `<NAMESPACE>` par `dev`, `test` ou `prod` selon l'environnement.

### 3.2 Patch complet (les 4 clés en une commande)

Remplacez les valeurs entre guillemets par vos secrets réels (pas d'espaces dans le mot de passe mail si vous le collez en ligne de commande).

```bash
kubectl patch secret backend-secret -n <NAMESPACE> -p '{
  "stringData": {
    "DB_PASSWORD": "VOTRE_MOT_DE_PASSE_BDD",
    "JWT_SECRET": "VOTRE_CLE_JWT_BASE64_OU_ALEATOIRE",
    "MAIL_USERNAME": "votre@email.com",
    "MAIL_PASSWORD": "MOT_DE_PASSE_APPLICATION_MAIL_SANS_ESPACES"
  }
}'
```

**Exemple pour l'environnement dev :**

```bash
kubectl patch secret backend-secret -n dev -p '{
  "stringData": {
    "DB_PASSWORD": "devpass123",
    "JWT_SECRET": "mCnYSHIL0evDMgXO5U1cm4VfWnBPPnMWUmZNasnF9ng=",
    "MAIL_USERNAME": "dev@gfz.local",
    "MAIL_PASSWORD": "votre_mot_de_passe_application"
  }
}'
```

### 3.3 Patch d'une seule clé

Pour mettre à jour uniquement une variable (sans écraser les autres) :

```bash
# DB_PASSWORD uniquement
kubectl patch secret backend-secret -n <NAMESPACE> -p '{"stringData":{"DB_PASSWORD":"nouveau_mdp_bdd"}}'

# JWT_SECRET uniquement
kubectl patch secret backend-secret -n <NAMESPACE> -p '{"stringData":{"JWT_SECRET":"nouvelle_cle_jwt"}}'

# MAIL_USERNAME uniquement
kubectl patch secret backend-secret -n <NAMESPACE> -p '{"stringData":{"MAIL_USERNAME":"email@exemple.com"}}'

# MAIL_PASSWORD uniquement
kubectl patch secret backend-secret -n <NAMESPACE> -p '{"stringData":{"MAIL_PASSWORD":"mot_de_passe_sans_espaces"}}'
```

### 3.4 Redémarrer le backend après un patch

Les pods existants ne voient pas les nouvelles valeurs tant qu'ils ne sont pas recréés :

```bash
kubectl rollout restart deployment/backend -n <NAMESPACE>
kubectl rollout status deployment/backend -n <NAMESPACE>
```

### 3.5 Vérifier la présence des clés (sans afficher les valeurs)

```bash
kubectl get secret backend-secret -n <NAMESPACE> -o jsonpath='{.data}' | jq 'keys'
```

Pour vérifier qu'une valeur est bien renseignée (longueur non nulle) :

```bash
kubectl get secret backend-secret -n <NAMESPACE> -o jsonpath='{.data.MAIL_PASSWORD}' | base64 -d | wc -c
```

---

## 4. Récapitulatif des environnements

| Namespace | Usage        | URL type (Ingress)   |
|-----------|---------------|----------------------|
| `dev`     | Développement | http://dev.gfz.local |
| `test`    | Recette       | http://test.gfz.local |
| `prod`    | Production    | http://gfz.local    |
| `infra`   | Registry, etc.| —                    |

---

## 5. Structure des dossiers

- `namespaces/` — Création des namespaces dev, test, prod
- `infra/` — Registry Docker (optionnel)
- `dev/` — Backend, frontend, Postgres, ConfigMaps, Secrets, Ingress (dev)
- `test/` — Idem pour l’environnement test
- `prod/` — Idem pour l’environnement production
