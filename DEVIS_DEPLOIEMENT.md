# DEVIS - DÉPLOIEMENT SITE WEB GFZ ONLINE

## INFORMATIONS GÉNÉRALES

**Client :** Groupe Français des Zéolithes (GFZ)  
**Projet :** Déploiement et mise en production du site web GFZ Online  
**Date :** [DATE]  
**Validité :** 30 jours

---

## 1. PRÉSENTATION DU PROJET

Site web institutionnel du Groupe Français des Zéolithes comprenant :
- **Frontend :** Application Nuxt 3 (Vue.js 3) avec Tailwind CSS
- **Backend :** API REST Spring Boot avec authentification JWT
- **Base de données :** PostgreSQL
- **Architecture :** Application containerisée avec Docker

### Fonctionnalités principales :
- Gestion de contenu (articles, actualités)
- Gestion des offres d'emploi et stages
- Système de newsletter avec envoi d'emails
- Formulaire de contact avec réponse par email
- Espace d'administration sécurisé
- Authentification JWT pour les administrateurs

---

## 2. PRÉREQUIS TECHNIQUES (À FOURNIR PAR LE CLIENT)

### 2.1 Serveur
- **Type :** Serveur VPS ou dédié (OVH, AWS, DigitalOcean, etc.)
- **Spécifications minimales recommandées :**
  - CPU : 2 cœurs minimum
  - RAM : 4 Go minimum (8 Go recommandé)
  - Stockage : 20 Go minimum (SSD recommandé)
  - Bande passante : Illimitée ou 100 Go/mois minimum

### 2.2 Système d'exploitation
- Linux (Ubuntu 22.04 LTS ou Debian 11+ recommandé)
- Accès root ou sudo

### 2.3 Logiciels à installer (par le client ou inclus dans le devis)
- Docker (version 20.10+)
- Docker Compose (version 2.0+)
- Git

### 2.4 Services externes
- **Nom de domaine :** À configurer par le client
- **Certificat SSL :** Let's Encrypt (gratuit) ou certificat commercial
- **Service email SMTP :** Pour l'envoi d'emails (Gmail, SendGrid, Mailgun, etc.)
  - Configuration requise : serveur SMTP, port, identifiants

### 2.5 Accès nécessaires
- Accès SSH au serveur
- Accès au panneau de contrôle du nom de domaine (pour DNS)
- Identifiants du service email SMTP

---

## 3. PRESTATIONS INCLUSES

### 3.1 Préparation de l'environnement de production
- [ ] Configuration des variables d'environnement de production
- [ ] Sécurisation des secrets (JWT, mots de passe, clés API)
- [ ] Configuration des fichiers Docker Compose pour la production
- [ ] Optimisation des configurations (cache, performances)

### 3.2 Installation et configuration serveur
- [ ] Installation de Docker et Docker Compose
- [ ] Configuration du pare-feu (ports 80, 443, 22)
- [ ] Configuration du reverse proxy (Nginx ou Traefik)
- [ ] Configuration du certificat SSL (Let's Encrypt)
- [ ] Configuration du domaine et DNS

### 3.3 Déploiement de l'application
- [ ] Clonage/transfert du code source sur le serveur
- [ ] Configuration de la base de données PostgreSQL
- [ ] Exécution des migrations de base de données
- [ ] Build et démarrage des conteneurs Docker
- [ ] Configuration des services (backend, frontend, base de données)
- [ ] Vérification du fonctionnement de tous les services

### 3.4 Configuration email
- [ ] Configuration du service SMTP dans l'application
- [ ] Test d'envoi d'emails (newsletter, contact, création de compte)
- [ ] Configuration des templates d'emails

### 3.5 Sécurisation
- [ ] Configuration des règles de sécurité (CORS, headers HTTP)
- [ ] Sécurisation des endpoints API
- [ ] Configuration des backups automatiques de la base de données
- [ ] Mise en place de la rotation des logs

### 3.6 Tests et validation
- [ ] Tests de toutes les fonctionnalités en production
- [ ] Tests de performance et charge
- [ ] Vérification de la responsivité mobile
- [ ] Tests de sécurité de base

### 3.7 Documentation et formation
- [ ] Documentation de déploiement
- [ ] Documentation d'administration
- [ ] Guide de maintenance
- [ ] Formation de l'administrateur (1 session de 2h)

---

## 4. PRESTATIONS OPTIONNELLES (HORS DEVIS)

### 4.1 Monitoring et supervision
- Installation d'outils de monitoring (Grafana, Prometheus)
- Configuration d'alertes
- Tableaux de bord de supervision

### 4.2 Sauvegardes automatisées
- Configuration de sauvegardes quotidiennes
- Stockage externe des sauvegardes
- Plan de restauration

### 4.3 Optimisation avancée
- Configuration d'un CDN
- Optimisation des images
- Mise en cache avancée

### 4.4 Support et maintenance
- Support technique mensuel
- Mises à jour de sécurité
- Maintenance préventive

---

## 5. LIVRABLES

1. **Application déployée et fonctionnelle** en production
2. **Documentation technique** de déploiement
3. **Documentation d'administration** pour la gestion quotidienne
4. **Accès et identifiants** sécurisés remis au client
5. **Scripts de maintenance** (backup, restart, etc.)

---

## 6. DÉLAIS

- **Délai de réalisation :** 3 à 5 jours ouvrés après réception de :
  - Accès au serveur
  - Configuration du nom de domaine
  - Identifiants du service email SMTP

---

## 7. CONDITIONS DE GARANTIE

- **Période de garantie :** 30 jours après la mise en production
- **Interventions couvertes :** Corrections de bugs liés au déploiement
- **Non couvert :** Modifications fonctionnelles, évolutions, problèmes liés au matériel/serveur

---

## 8. TARIFICATION

### 8.1 Forfait déploiement initial
**Montant :** **1 500 € HT** (1 800 € TTC)

**Inclut :**
- Toutes les prestations listées en section 3
- 1 session de formation (2h)
- Support pendant la période de garantie (30 jours)

**Justification du tarif :**
- Temps estimé : 3-5 jours (24-40 heures)
- Complexité technique : Docker, SSL, reverse proxy, configuration email
- Documentation complète et formation incluse
- Support et garantie 30 jours

### 8.2 Prestations optionnelles (sur devis séparé)
- Monitoring et supervision : **400 € HT**
- Configuration sauvegardes automatisées : **300 € HT**
- Support et maintenance mensuel : **150 € HT/mois**

---

## 9. CONDITIONS DE PAIEMENT

- **Acompte :** 50% à la commande
- **Solde :** 50% à la livraison et mise en production

**Modalités :** Virement bancaire, chèque

---

## 10. EXCLUSIONS

Ce devis n'inclut **PAS** :
- L'achat et la configuration du serveur (à la charge du client)
- L'achat du nom de domaine (à la charge du client)
- Les modifications fonctionnelles ou évolutions
- La maintenance au-delà de la période de garantie
- Les interventions liées à des problèmes matériels ou réseau
- La création de contenu (articles, pages, etc.)

---

## 11. INFORMATIONS COMPLÉMENTAIRES

### Architecture technique déployée :
- **Frontend :** Nuxt 3 (port 3000, accessible via reverse proxy)
- **Backend :** Spring Boot (port 8080, interne)
- **Base de données :** PostgreSQL 16 (port 5432, interne)
- **Reverse proxy :** Nginx ou Traefik (ports 80/443)
- **SSL :** Let's Encrypt (gratuit) ou certificat commercial

### Variables d'environnement à configurer :
- URL du frontend
- URL de l'API backend
- Configuration base de données
- JWT secret et expiration
- Configuration SMTP (email)
- CORS origins

---

## ACCEPTATION DU DEVIS

Fait à [LIEU], le [DATE]

**Prestataire :**  
[NOM]  
[ADRESSE]  
[EMAIL]  
[TÉLÉPHONE]

**Client :**  
[NOM]  
[ADRESSE]  
[EMAIL]  
[TÉLÉPHONE]

Signature client : _________________  Date : _________

---

## NOTES IMPORTANTES

1. Le client doit s'assurer que le serveur respecte les spécifications minimales
2. Le client doit fournir tous les accès nécessaires dans les délais convenus
3. Les modifications du code source après le déploiement peuvent nécessiter un redéploiement
4. Il est recommandé de prévoir un budget pour la maintenance et les mises à jour de sécurité
