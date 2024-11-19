## 🔐 Keylogger Éthique – Outil de Surveillance Sécurisé (utilisateur linux)
**⚠️ Avertissement Légal
Ce logiciel est strictement destiné à des fins éthiques, éducatives et de recherche en cybersécurité autorisée.**

L'utilisation non autorisée, y compris la surveillance des frappes clavier, des données du presse-papiers ou du contenu de l'écran sans le consentement éclairé et vérifiable de tous les utilisateurs, constitue une violation des lois locales, nationales et internationales sur la confidentialité et la cybersécurité.

L'utilisateur assume l'entière responsabilité de toutes les conséquences juridiques ou éthiques résultant de l'utilisation de ce logiciel.

## 🧩 Aperçu du Projet
Cet outil est un keylogger basé sur le consentement, chiffré AES, avec rapport par email conçu pour :

**Démonstrations de hacking éthique**

**Éducation et ateliers en cybersécurité**

**Recherche en criminalistique numérique**

Il prend en charge l'enregistrement des frappes en temps réel, la capture d'écran, la surveillance du presse-papiers et le rapport par email chiffré — avec vérification du consentement avant l'activation.

## ✅ Fonctionnalités Principales
**Fonctionnalité	                Description**
Enregistrement des Frappes	     Enregistre toutes les entrées clavier avec les titres de fenêtres actives et horodatages
Surveillance du Presse-papiers   Surveille les activités de copier, couper et coller du presse-papiers système
Capture d'Écran	                 Prend des captures d'écran périodiques ; transmises de manière sécurisée par email
Chiffrement AES	                 Utilise cryptography.Fernet pour chiffrer les données de logs
Rapport par Email	             Envoie des logs chiffrés et captures d'écran par email avec paramètres configurables
Demande de Consentement	         Nécessite l'approbation de l'utilisateur avant tout démarrage de la surveillance
Informations Système	         Collecte les métadonnées système (nom d'utilisateur, adresses IP, horodatage)
Vérification d'Intégrité	     Applique un hachage SHA256 pour vérifier l'authenticité des logs
Journalisation d'Audit	         Maintient des logs locaux pour la traçabilité et la conformité

## 🐧 Installation (Linux – Ubuntu / Debian / Kali)
~~~
sudo apt update && sudo apt install git python3 python3-pip python3-venv -y

git clone https://github.com/mateo/ethical-keylogger-lab.git
cd ethical-keylogger-lab

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

# Optionnel (pour le support des captures d'écran)
sudo apt install scrot python3-tk python3-dev -y
~~~

## 📦 Paquets Requis (Assurez-vous qu'ils sont Installés)
Pour installer manuellement les dépendances Python essentielles dans votre environnement virtuel :
~~~
pip install pynput cryptography clipboard mss requests

Pour supporter le suivi des fenêtres actives (si pas déjà installé) :

sudo apt install xdotool
~~~
## 🔐 Configuration des Variables d'Environnement
Avant d'exécuter le script, configurez les variables email nécessaires dans votre session de terminal :

~~~
export SENDER_EMAIL='votre_email@gmail.com'
export EMAIL_PASSWORD='votre_mot_de_passe_app'   # Utilisez un Mot de Passe d'Application sécurisé
export RECEIVER_EMAIL='email_recepteur@gmail.com'
~~~
**Important : Ne codez jamais en dur les identifiants sensibles directement dans le script. Utilisez toujours des variables d'environnement**.

## 🚀 Exécution du Keylogger
Pour démarrer le keylogger :
~~~
python keyloggers_2025.py
~~~
Le script demandera le consentement explicite de l'utilisateur.

Après approbation, il commencera à capturer les logs (frappes clavier, données du presse-papiers, captures d'écran).

Les logs et images capturées sont chiffrés et soit sauvegardés localement, soit envoyés par email.

## ⚙️ Configuration & Personnalisation
Vous pouvez personnaliser le script en modifiant :

Intervalles et formats des captures d'écran

Fréquence de journalisation et taille des lots

Chemin de stockage des logs locaux

Logique de réessai et déclencheurs d'email

Référez-vous au fichier keyloggers_2025.py pour les paramètres de configuration.

## 📄 Licence
**Ce projet est sous licence MIT.**

Vous êtes libre d'utiliser, modifier et distribuer ce logiciel, à condition d'inclure les informations
de copyright et de licence originales. Le logiciel est fourni "tel quel", sans aucune garantie.

## ⚖️ Politique d'Utilisation Légale & Éthique
Exigence de Consentement
Le consentement doit être explicite, éclairé et vérifiable.

Maintenez une documentation appropriée et stockez les enregistrements de consentement de manière sécurisée.

Utilisation Interdite
La surveillance non autorisée d'individus ou de systèmes sans consentement est strictement interdite.

Les violations peuvent entraîner des poursuites judiciaires en vertu des lois applicables sur la cybercriminalité et la confidentialité.

Cas d'Utilisation Prévus
Éducation au hacking éthique

Tests de pénétration (avec autorisation)

Recherche et cours académiques

Cet outil n'est pas destiné à la surveillance personnelle, à l'espionnage d'entreprise ou à tout déploiement commercial sans autorisation explicite.

Conformité Légale
Les utilisateurs doivent se conformer aux lois et cadres pertinents, y compris mais sans s'y limiter :

France – Loi Informatique et Libertés, RGPD

Union Européenne – Règlement Général sur la Protection des Données (RGPD)

États-Unis – CFAA, ECPA

Autres – Statuts nationaux et régionaux sur la confidentialité et la protection des données

## 🛡️ Meilleures Pratiques Recommandées
Environnements Virtuels : Isolez les dépendances pour la reproductibilité et la sécurité

Chiffrement des Données : Chiffrez toujours les logs et informations sensibles

Manipulation Sécurisée : Assurez une transmission et un stockage sûrs de toutes les données surveillées

Pistes d'Audit : Maintenez des logs complets pour la responsabilité

Documentation du Consentement : Conservez les enregistrements de toutes les approbations de consentement

Restez Informé : Révisez régulièrement les normes légales et éthiques pertinentes

## ⚠️ Avertissement Final
Ce logiciel est fourni "tel quel", sans aucune garantie — expresse ou implicite.
Les auteurs et contributeurs ne sauraient être tenus responsables de toute utilisation abusive, dommages ou conséquences juridiques découlant de son utilisation.

En téléchargeant ou en utilisant cet outil, vous acceptez de :

Accepter l'entière responsabilité juridique de son déploiement

L'utiliser uniquement dans des contextes éthiques et autorisés

**Respecter toutes les lois locales et internationales concernant la confidentialité numérique et la surveillance**
