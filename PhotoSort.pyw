import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil
import threading
import json
import webbrowser
import datetime
import re
import sys
import traceback
import io
import gc
import hashlib
import subprocess
import math
import platform
import multiprocessing
from pathlib import Path
from collections import Counter, OrderedDict
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from PIL import Image, ImageTk, ImageOps, ImageFilter, ImageStat

# ==========================================
# SETUP DRAG & DROP
# ==========================================
try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    DND_AVAILABLE = True
    class TkinterDnD_CTk(ctk.CTk, TkinterDnD.DnDWrapper):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.TkdndVersion = TkinterDnD._require(self)
except ImportError:
    DND_AVAILABLE = False
    class TkinterDnD_CTk(ctk.CTk):
        pass

# ==========================================
# SETUP LIBRARY PENDUKUNG (RAW & CV2)
# ==========================================
try:
    import rawpy
    import imageio
    RAWPY_AVAILABLE = True
except ImportError:
    RAWPY_AVAILABLE = False

try:
    import cv2
    import numpy as np
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False

# ==========================================
# KONFIGURASI TEMA & WARNA
# ==========================================
COLORS = { 
    "bg": "#343541",      
    "fg": "#ECECF1",         
    "accent": "#10A37F",     
    "accent_hover": "#1A7F64",
    "secondary": "#444654",  
    "danger": "#EF4444",     
    "warning": "#EAB308",
    "success": "#22C55E",
    "input_bg": "#40414F"
}

# ==========================================
# DATABASE BAHASA (6 BAHASA LENGKAP)
# ==========================================
LANGUAGES = {
    "English": {
        "title": "PhotoSort Pro v4.1 (Optimized)",
        "tab_auto": "Auto Sort",
        "tab_manual": "Manual Sort",
        "tab_smart": "Smart Select",
        "tab_log": "Activity Log",
        "lbl_source": "Source Folder:",
        "lbl_dest": "Destination Folder:",
        "btn_browse": "Browse...",
        "lbl_subfolder": "Subfolder Name:",
        "lbl_codes": "Client Codes (input list below):",
        "btn_check_codes": "Check Codes", 
        "lbl_action": "Action Type:",
        "radio_copy": "Copy Files",
        "radio_cut": "Cut (Move) Files",
        "chk_rename": "Rename Files (Code_OriginalName)",
        "lbl_filter": "File Filter:",
        "radio_raw_jpg": "RAW + JPG",
        "radio_raw_only": "RAW Only",
        "btn_start_auto": "START AUTO SORT",
        "status_ready": "Ready.",
        "status_done": "Sorting Complete!",
        "status_processing": "Processing... ",
        "btn_set_hotkey": "Set Hotkeys",
        "btn_start_manual": "EXECUTE SORT",
        "lbl_sort_type": "Sort Output Type:",
        "note_preview": "NOTE: Click image area to Zoom. Scroll to Resize.",
        "change_lang": "Change Language",
        "no_images": "No compatible images found.",
        "select_folders": "Please select both Source and Destination folders.",
        "enter_codes": "Please enter at least one code to sort.",
        "btn_refresh": "Refresh App",
        "btn_undo": "Undo (Ctrl+Z)",
        "report_missing": "Missing Codes Report",
        "report_msg": "Sorting Done!\nFiles Processed: {count}\n\n{missing}\n\n{duplicates}",
        "report_dup_msg": "⚠️ DUPLICATE CODES DETECTED:\n{duplicates}",
        "tip_tutorial": "Start Interactive Tutorial",
        "tip_lang": "Change Language",
        "tip_refresh": "Refresh Application State",
        "raw_install_hint": "RAW Preview requires: pip install rawpy imageio",
        "lbl_remaining": "Remaining: {count}",
        "preview_title": "Parsed Codes Preview",
        "preview_header": "System detected {count} valid codes:",
        "btn_open_folder": "Open Output Folder",
        "msg_checksum_fail": "Checksum verification failed for file: {file}",
        "lbl_drag_drop": "Drag & Drop Folder Here",
        "lbl_target_count": "Target Photo Count:",
        "lbl_smart_criteria": "AI Criteria: Sharpness, Exposure & Similarity grouping.",
        "btn_start_smart": "ANALYZE & PICK BEST",
        "smart_processing": "Analyzing Quality & Grouping Similar Photos...",
        "smart_done": "Smart Selection Complete! Top {count} unique photos moved.",
        "lbl_sensitivity": "AI Sensitivity:",
        "msg_confirm_stop": "Are you sure you want to stop the process?"
    },
    "Indonesia": {
        "title": "PhotoSort Pro v4.1 (Optimized)",
        "tab_auto": "Sortir Otomatis",
        "tab_manual": "Sortir Manual",
        "tab_smart": "Pilih Cerdas",
        "tab_log": "Log Aktivitas",
        "lbl_source": "Folder Sumber:",
        "lbl_dest": "Folder Tujuan:",
        "btn_browse": "Pilih...",
        "lbl_subfolder": "Nama Sub-Folder:",
        "lbl_codes": "Kode Klien (masukkan daftar di bawah):",
        "btn_check_codes": "Cek Kode",
        "lbl_action": "Tipe Aksi:",
        "radio_copy": "Salin (Copy)",
        "radio_cut": "Pindah (Cut)",
        "chk_rename": "Ganti Nama (Kode_NamaAsli)",
        "lbl_filter": "Filter File:",
        "radio_raw_jpg": "RAW & JPG",
        "radio_raw_only": "Hanya RAW",
        "btn_start_auto": "MULAI SORTIR",
        "status_ready": "Siap.",
        "status_done": "Penyortiran Selesai!",
        "status_processing": "Memproses... ",
        "btn_set_hotkey": "Atur Tombol",
        "btn_start_manual": "EKSEKUSI SORTIR",
        "lbl_sort_type": "Tipe Output:",
        "note_preview": "INFO: Klik gambar untuk Zoom. Scroll untuk Resize.",
        "change_lang": "Ganti Bahasa",
        "no_images": "Tidak ada file gambar yang kompatibel.",
        "select_folders": "Mohon pilih Folder Sumber dan Tujuan.",
        "enter_codes": "Mohon masukkan setidaknya satu kode.",
        "btn_refresh": "Refresh Aplikasi",
        "btn_undo": "Undo (Ctrl+Z)",
        "report_missing": "Laporan Kode Hilang",
        "report_msg": "Selesai!\nFile Diproses: {count}\n\n{missing}\n\n{duplicates}",
        "report_dup_msg": "⚠️ DUPLIKASI KODE DITEMUKAN:\n{duplicates}",
        "tip_tutorial": "Mulai Tutorial Interaktif",
        "tip_lang": "Ganti Bahasa",
        "tip_refresh": "Refresh Status Aplikasi",
        "raw_install_hint": "Preview RAW butuh: pip install rawpy imageio",
        "lbl_remaining": "Sisa: {count}",
        "preview_title": "Preview Kode",
        "preview_header": "Sistem mendeteksi {count} kode valid:",
        "btn_open_folder": "Buka Folder Hasil",
        "msg_checksum_fail": "Verifikasi Checksum Gagal pada file: {file}",
        "lbl_drag_drop": "Tarik & Lepas Folder Di Sini",
        "lbl_target_count": "Jumlah Foto Target:",
        "lbl_smart_criteria": "Kriteria AI: Ketajaman, Cahaya & Grup Foto Mirip.",
        "btn_start_smart": "ANALISA & PILIH TERBAIK",
        "smart_processing": "Menganalisa Kualitas & Mengelompokkan...",
        "smart_done": "Selesai! {count} foto unik terbaik telah dipilih.",
        "lbl_sensitivity": "Sensitivitas AI:",
        "msg_confirm_stop": "Yakin ingin menghentikan proses?"
    },
    "Deutsch": {
        "title": "PhotoSort Pro v4.1 (Optimized)",
        "tab_auto": "Auto-Sortierung",
        "tab_manual": "Manuelle Sortierung",
        "tab_smart": "Intelligente Auswahl",
        "tab_log": "Aktivitätsprotokoll",
        "lbl_source": "Quellordner:",
        "lbl_dest": "Zielordner:",
        "btn_browse": "Durchsuchen...",
        "lbl_subfolder": "Unterordner Name:",
        "lbl_codes": "Kundencodes (Liste unten eingeben):",
        "btn_check_codes": "Codes Prüfen", 
        "lbl_action": "Aktionstyp:",
        "radio_copy": "Kopieren",
        "radio_cut": "Ausschneiden (Verschieben)",
        "chk_rename": "Umbenennen (Code_OriginalName)",
        "lbl_filter": "Dateifilter:",
        "radio_raw_jpg": "RAW + JPG",
        "radio_raw_only": "Nur RAW",
        "btn_start_auto": "AUTO-SORTIERUNG STARTEN",
        "status_ready": "Bereit.",
        "status_done": "Sortierung Abgeschlossen!",
        "status_processing": "Verarbeitung... ",
        "btn_set_hotkey": "Tastenbelegung",
        "btn_start_manual": "SORTIERUNG AUSFÜHREN",
        "lbl_sort_type": "Ausgabetyp:",
        "note_preview": "HINWEIS: Klicken zum Zoomen. Scrollen zum Ändern der Größe.",
        "change_lang": "Sprache ändern",
        "no_images": "Keine kompatiblen Bilder gefunden.",
        "select_folders": "Bitte wählen Sie Quell- und Zielordner aus.",
        "enter_codes": "Bitte geben Sie mindestens einen Code ein.",
        "btn_refresh": "App Aktualisieren",
        "btn_undo": "Rückgängig (Ctrl+Z)",
        "report_missing": "Fehlende Codes Bericht",
        "report_msg": "Fertig!\nVerarbeitete Dateien: {count}\n\n{missing}\n\n{duplicates}",
        "report_dup_msg": "⚠️ DOPPELTE CODES ERKANNT:\n{duplicates}",
        "tip_tutorial": "Interaktives Tutorial starten",
        "tip_lang": "Sprache ändern",
        "tip_refresh": "Anwendungsstatus aktualisieren",
        "raw_install_hint": "RAW-Vorschau benötigt: pip install rawpy imageio",
        "lbl_remaining": "Verbleibend: {count}",
        "preview_title": "Code-Vorschau",
        "preview_header": "System erkannte {count} gültige Codes:",
        "btn_open_folder": "Ausgabeordner öffnen",
        "msg_checksum_fail": "Prüfsummenfehler bei Datei: {file}",
        "lbl_drag_drop": "Ordner hier ablegen",
        "lbl_target_count": "Zielanzahl Fotos:",
        "lbl_smart_criteria": "KI-Kriterien: Schärfe, Belichtung & Ähnlichkeit.",
        "btn_start_smart": "ANALYSIEREN & BESTE WÄHLEN",
        "smart_processing": "Analysiere Qualität & gruppiere ähnliche Fotos...",
        "smart_done": "Auswahl abgeschlossen! Top {count} Fotos verschoben.",
        "lbl_sensitivity": "KI-Empfindlichkeit:",
        "msg_confirm_stop": "Möchten Sie den Vorgang wirklich stoppen?"
    },
    "日本語": {
        "title": "PhotoSort Pro v4.1 (Optimized)",
        "tab_auto": "自動仕分け",
        "tab_manual": "手動仕分け",
        "tab_smart": "スマート選択",
        "tab_log": "ログ",
        "lbl_source": "ソースフォルダ:",
        "lbl_dest": "保存先フォルダ:",
        "btn_browse": "参照...",
        "lbl_subfolder": "サブフォルダ名:",
        "lbl_codes": "顧客コード (リストを入力):",
        "btn_check_codes": "コード確認", 
        "lbl_action": "アクション:",
        "radio_copy": "コピー",
        "radio_cut": "移動 (切り取り)",
        "chk_rename": "名前変更 (コード_元の名前)",
        "lbl_filter": "ファイル形式:",
        "radio_raw_jpg": "RAW + JPG",
        "radio_raw_only": "RAWのみ",
        "btn_start_auto": "自動仕分け開始",
        "status_ready": "準備完了。",
        "status_done": "仕分け完了！",
        "status_processing": "処理中... ",
        "btn_set_hotkey": "キー設定",
        "btn_start_manual": "仕分け実行",
        "lbl_sort_type": "出力タイプ:",
        "note_preview": "注: クリックでズーム。スクロールでサイズ変更。",
        "change_lang": "言語変更",
        "no_images": "対応画像が見つかりません。",
        "select_folders": "ソースと保存先のフォルダを選択してください。",
        "enter_codes": "コードを少なくとも1つ入力してください。",
        "btn_refresh": "更新",
        "btn_undo": "元に戻す (Ctrl+Z)",
        "report_missing": "未検出コード レポート",
        "report_msg": "完了！\n処理ファイル数: {count}\n\n{missing}\n\n{duplicates}",
        "report_dup_msg": "⚠️ 重複コード検出:\n{duplicates}",
        "tip_tutorial": "チュートリアルを開始",
        "tip_lang": "言語を変更",
        "tip_refresh": "アプリの状態をリセット",
        "raw_install_hint": "RAWプレビューには pip install rawpy imageio が必要です",
        "lbl_remaining": "残り: {count}",
        "preview_title": "コード プレビュー",
        "preview_header": "{count} 個の有効なコードを検出:",
        "btn_open_folder": "フォルダを開く",
        "msg_checksum_fail": "チェックサム検証失敗: {file}",
        "lbl_drag_drop": "ここにフォルダをドロップ",
        "lbl_target_count": "目標枚数:",
        "lbl_smart_criteria": "AI基準: シャープネス、露出、類似性。",
        "btn_start_smart": "分析してベストを選択",
        "smart_processing": "品質分析と類似写真のグループ化中...",
        "smart_done": "完了！ ベスト {count} 枚が移動されました。",
        "lbl_sensitivity": "AI感度:",
        "msg_confirm_stop": "停止しますか？"
    },
    "Español": {
        "title": "PhotoSort Pro v4.1 (Optimized)",
        "tab_auto": "Clasif. Automática",
        "tab_manual": "Clasif. Manual",
        "tab_smart": "Selección Inteligente",
        "tab_log": "Registro",
        "lbl_source": "Carpeta Origen:",
        "lbl_dest": "Carpeta Destino:",
        "btn_browse": "Explorar...",
        "lbl_subfolder": "Nombre Subcarpeta:",
        "lbl_codes": "Códigos de Cliente:",
        "btn_check_codes": "Verificar Códigos", 
        "lbl_action": "Acción:",
        "radio_copy": "Copiar",
        "radio_cut": "Cortar (Mover)",
        "chk_rename": "Renombrar (Cód_Original)",
        "lbl_filter": "Filtro:",
        "radio_raw_jpg": "RAW + JPG",
        "radio_raw_only": "Solo RAW",
        "btn_start_auto": "INICIAR CLASIFICACIÓN",
        "status_ready": "Listo.",
        "status_done": "¡Clasificación Completa!",
        "status_processing": "Procesando... ",
        "btn_set_hotkey": "Atajos",
        "btn_start_manual": "EJECUTAR CLASIFICACIÓN",
        "lbl_sort_type": "Tipo de Salida:",
        "note_preview": "NOTA: Clic para Zoom. Scroll para redimensionar.",
        "change_lang": "Cambiar Idioma",
        "no_images": "No se encontraron imágenes compatibles.",
        "select_folders": "Seleccione carpetas de origen y destino.",
        "enter_codes": "Ingrese al menos un código.",
        "btn_refresh": "Refrescar App",
        "btn_undo": "Deshacer (Ctrl+Z)",
        "report_missing": "Reporte de Códigos Faltantes",
        "report_msg": "¡Hecho!\nArchivos Procesados: {count}\n\n{missing}\n\n{duplicates}",
        "report_dup_msg": "⚠️ CÓDIGOS DUPLICADOS:\n{duplicates}",
        "tip_tutorial": "Iniciar Tutorial Interactivo",
        "tip_lang": "Cambiar Idioma",
        "tip_refresh": "Refrescar Estado",
        "raw_install_hint": "Vista RAW requiere: pip install rawpy imageio",
        "lbl_remaining": "Restantes: {count}",
        "preview_title": "Vista Previa Códigos",
        "preview_header": "Sistema detectó {count} códigos válidos:",
        "btn_open_folder": "Abrir Carpeta",
        "msg_checksum_fail": "Fallo de checksum en archivo: {file}",
        "lbl_drag_drop": "Arrastrar y Soltar Carpeta Aquí",
        "lbl_target_count": "Cantidad Objetivo:",
        "lbl_smart_criteria": "Criterio AI: Nitidez, Exposición y Similitud.",
        "btn_start_smart": "ANALIZAR Y ELEGIR MEJORES",
        "smart_processing": "Analizando Calidad y Agrupando...",
        "smart_done": "¡Selección Inteligente Completa! {count} fotos movidas.",
        "lbl_sensitivity": "Sensibilidad IA:",
        "msg_confirm_stop": "¿Detener proceso?"
    },
    "Français": {
        "title": "PhotoSort Pro v4.1 (Optimized)",
        "tab_auto": "Tri Automatique",
        "tab_manual": "Tri Manuel",
        "tab_smart": "Sélection Intelligente",
        "tab_log": "Journal",
        "lbl_source": "Dossier Source:",
        "lbl_dest": "Dossier Destination:",
        "btn_browse": "Parcourir...",
        "lbl_subfolder": "Nom du Sous-dossier:",
        "lbl_codes": "Codes Client:",
        "btn_check_codes": "Vérifier Codes", 
        "lbl_action": "Action:",
        "radio_copy": "Copier",
        "radio_cut": "Couper (Déplacer)",
        "chk_rename": "Renommer (Code_NomOrig)",
        "lbl_filter": "Filtre:",
        "radio_raw_jpg": "RAW + JPG",
        "radio_raw_only": "RAW Uniquement",
        "btn_start_auto": "DÉMARRER LE TRI",
        "status_ready": "Prêt.",
        "status_done": "Tri Terminé !",
        "status_processing": "Traitement... ",
        "btn_set_hotkey": "Raccourcis",
        "btn_start_manual": "EXÉCUTER LE TRI",
        "lbl_sort_type": "Type de Sortie:",
        "note_preview": "NOTE: Clic pour Zoomer. Scroll pour Redimensionner.",
        "change_lang": "Changer Langue",
        "no_images": "Aucune image compatible trouvée.",
        "select_folders": "Veuillez sélectionner les dossiers Source et Destination.",
        "enter_codes": "Veuillez entrer au moins un code.",
        "btn_refresh": "Rafraîchir App",
        "btn_undo": "Annuler (Ctrl+Z)",
        "report_missing": "Rapport Codes Manquants",
        "report_msg": "Terminé !\nFichiers Traités: {count}\n\n{missing}\n\n{duplicates}",
        "report_dup_msg": "⚠️ CODES DUPLIQUÉS:\n{duplicates}",
        "tip_tutorial": "Démarrer le Tutoriel",
        "tip_lang": "Changer Langue",
        "tip_refresh": "Rafraîchir État",
        "raw_install_hint": "Aperçu RAW nécessite: pip install rawpy imageio",
        "lbl_remaining": "Restant: {count}",
        "preview_title": "Aperçu des Codes",
        "preview_header": "Le système a détecté {count} codes valides:",
        "btn_open_folder": "Ouvrir Dossier",
        "msg_checksum_fail": "Échec Checksum pour: {file}",
        "lbl_drag_drop": "Glisser-Déposer Dossier Ici",
        "lbl_target_count": "Nombre Cible:",
        "lbl_smart_criteria": "Critère IA: Netteté, Exposition & Similitude.",
        "btn_start_smart": "ANALYSER & CHOISIR",
        "smart_processing": "Analyse de la qualité et regroupement...",
        "smart_done": "Sélection terminée ! Top {count} photos déplacées.",
        "lbl_sensitivity": "Sensibilité IA:",
        "msg_confirm_stop": "Arrêter le processus ?"
    }
}

# ==========================================
# TUTORIAL DATA
# ==========================================
TUTORIAL_STEPS_BASE = [
    (None, None, "tut_intro", 'center'),
    (None, 'btn_lang', "tut_lang", 'right'),
    (None, 'btn_refresh', "tut_refresh", 'right'),
    # AUTO
    ('tab_auto', 'frame_folders_auto', "tut_auto_src", 'right'),
    ('tab_auto', 'frame_codes', "tut_auto_codes", 'right'),
    ('tab_auto', 'btn_check_codes', "tut_auto_check", 'left'),
    ('tab_auto', 'frame_opts_auto', "tut_auto_opts", 'right'),
    ('tab_auto', 'btn_auto_start', "tut_auto_start", 'top'),
    # MANUAL
    ('tab_manual', 'btn_load_manual', "tut_man_load", 'bottom'),
    ('tab_manual', 'canvas_preview', "tut_man_view", 'left'),
    ('tab_manual', 'frame_cats_dynamic', "tut_man_cats", 'left'),
    ('tab_manual', 'btn_undo', "tut_man_undo", 'left'),
    ('tab_manual', 'btn_execute_man', "tut_man_exec", 'top'),
    # SMART
    ('tab_smart', 'frame_folders_smart', "tut_smart_src", 'right'),
    ('tab_smart', 'entry_smart_count', "tut_smart_count", 'left'),
    ('tab_smart', 'sl_sensitivity', "tut_smart_sens", 'left'),
    ('tab_smart', 'btn_smart_start', "tut_smart_start", 'top'),
    # LOG
    ('tab_log', 'txt_log', "tut_log", 'center'),
    (None, None, "tut_end", 'center')
]

TUTORIAL_LOCALIZED = {
    "English": {
        "tut_intro": "Welcome to PhotoSort Pro!\nLet's take a tour.",
        "tut_lang": "Change Application Language here.",
        "tut_refresh": "Reset app state if needed.",
        "tut_auto_src": "Select Source and Destination folders here.",
        "tut_auto_codes": "Paste Client Codes here.",
        "tut_auto_check": "Verify how codes are read.",
        "tut_auto_opts": "Set Copy/Cut, Rename, and Filter options.",
        "tut_auto_start": "Start the Auto Sorting process.",
        "tut_man_load": "Load a folder to start manual sorting.",
        "tut_man_view": "Preview image. Scroll to Zoom, Drag to Pan.",
        "tut_man_cats": "Click or use Keys (1, 2, 3) to categorize.",
        "tut_man_undo": "Undo last action (Ctrl+Z).",
        "tut_man_exec": "Apply changes and move files.",
        "tut_smart_src": "Select folders for AI selection.",
        "tut_smart_count": "How many best photos do you want?",
        "tut_smart_sens": "Adjust AI similarity grouping sensitivity.",
        "tut_smart_start": "Start AI Analysis.",
        "tut_log": "Check logs for errors or activity.",
        "tut_end": "Tutorial Complete!"
    },
    "Indonesia": {
        "tut_intro": "Selamat Datang di PhotoSort Pro!\nMari kita mulai tur.",
        "tut_lang": "Ganti Bahasa aplikasi di sini.",
        "tut_refresh": "Reset aplikasi jika ada masalah.",
        "tut_auto_src": "Pilih folder Sumber dan Tujuan di sini.",
        "tut_auto_codes": "Tempel Kode Klien di sini.",
        "tut_auto_check": "Cek cara kode dibaca.",
        "tut_auto_opts": "Atur opsi Salin/Pindah, Rename, dan Filter.",
        "tut_auto_start": "Mulai proses Sortir Otomatis.",
        "tut_man_load": "Muat folder untuk sortir manual.",
        "tut_man_view": "Preview. Scroll untuk Zoom, Drag untuk geser.",
        "tut_man_cats": "Klik atau tekan (1, 2, 3) untuk kategori.",
        "tut_man_undo": "Batalkan aksi terakhir (Ctrl+Z).",
        "tut_man_exec": "Terapkan perubahan dan pindahkan file.",
        "tut_smart_src": "Pilih folder untuk seleksi AI.",
        "tut_smart_count": "Berapa foto terbaik yang diinginkan?",
        "tut_smart_sens": "Atur sensitivitas pengelompokan AI.",
        "tut_smart_start": "Mulai Analisis AI.",
        "tut_log": "Cek log untuk error atau aktivitas.",
        "tut_end": "Tutorial Selesai!"
    },
    "Deutsch": {"tut_intro": "Willkommen!", "tut_lang": "Sprache ändern.", "tut_refresh": "App neu laden.", "tut_auto_src": "Ordner wählen.", "tut_auto_codes": "Codes eingeben.", "tut_auto_check": "Codes prüfen.", "tut_auto_opts": "Optionen einstellen.", "tut_auto_start": "Starten.", "tut_man_load": "Ordner laden.", "tut_man_view": "Vorschau.", "tut_man_cats": "Kategorisieren (1,2,3).", "tut_man_undo": "Rückgängig.", "tut_man_exec": "Ausführen.", "tut_smart_src": "Ordner wählen.", "tut_smart_count": "Anzahl Fotos.", "tut_smart_sens": "Sensitivität.", "tut_smart_start": "Starten.", "tut_log": "Logbuch.", "tut_end": "Ende."},
    "日本語": {"tut_intro": "ようこそ！", "tut_lang": "言語変更。", "tut_refresh": "リセット。", "tut_auto_src": "フォルダ選択。", "tut_auto_codes": "コード入力。", "tut_auto_check": "確認。", "tut_auto_opts": "オプション。", "tut_auto_start": "開始。", "tut_man_load": "読込。", "tut_man_view": "プレビュー。", "tut_man_cats": "分類 (1,2,3)。", "tut_man_undo": "元に戻す。", "tut_man_exec": "実行。", "tut_smart_src": "フォルダ選択。", "tut_smart_count": "枚数。", "tut_smart_sens": "感度。", "tut_smart_start": "開始。", "tut_log": "ログ。", "tut_end": "終了。"},
    "Español": {"tut_intro": "¡Bienvenido!", "tut_lang": "Idioma.", "tut_refresh": "Recargar.", "tut_auto_src": "Carpetas.", "tut_auto_codes": "Códigos.", "tut_auto_check": "Verificar.", "tut_auto_opts": "Opciones.", "tut_auto_start": "Iniciar.", "tut_man_load": "Cargar.", "tut_man_view": "Vista.", "tut_man_cats": "Categorías (1,2,3).", "tut_man_undo": "Deshacer.", "tut_man_exec": "Ejecutar.", "tut_smart_src": "Carpetas.", "tut_smart_count": "Cantidad.", "tut_smart_sens": "Sensibilidad.", "tut_smart_start": "Iniciar.", "tut_log": "Registro.", "tut_end": "Fin."},
    "Français": {"tut_intro": "Bienvenue !", "tut_lang": "Langue.", "tut_refresh": "Rafraîchir.", "tut_auto_src": "Dossiers.", "tut_auto_codes": "Codes.", "tut_auto_check": "Vérifier.", "tut_auto_opts": "Options.", "tut_auto_start": "Démarrer.", "tut_man_load": "Charger.", "tut_man_view": "Aperçu.", "tut_man_cats": "Catégories (1,2,3).", "tut_man_undo": "Annuler.", "tut_man_exec": "Exécuter.", "tut_smart_src": "Dossiers.", "tut_smart_count": "Nombre.", "tut_smart_sens": "Sensibilité.", "tut_smart_start": "Démarrer.", "tut_log": "Journal.", "tut_end": "Fin."}
}

# ==========================================
# EXTENSIONS
# ==========================================
EXT_JPG = {'.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG'} 
EXT_RAW = {'.cr2', '.nef', '.arw', '.orf', '.dng', '.raf', '.sr2', '.cr3', '.heic', '.hif', 
           '.CR2', '.NEF', '.ARW', '.ORF', '.DNG', '.RAF', '.SR2', '.CR3', '.HEIC', '.HIF'} 
EXT_ALL = EXT_JPG.union(EXT_RAW)

# ==========================================
# STANDALONE WORKER FUNCTION (MULTIPROCESSING)
# ==========================================
_FACE_CASCADE = None
_EYE_CASCADE = None

def analyze_image_worker(filepath):
    try:
        # Inisialisasi awal (PENTING: agar tidak ada variabel yang 'missing')
        score = 0; dhash = 0; hist_data = []; img = None
        penalty = 0; blink_penalty = 0 
        
        # 1. Load Strategy
        try:
            if RAWPY_AVAILABLE:
                ext = os.path.splitext(filepath)[1].lower()
                if ext in EXT_RAW:
                    with rawpy.imread(filepath) as raw:
                        thumb = raw.extract_thumb()
                        img = Image.open(io.BytesIO(thumb.data)) if thumb.format == rawpy.ThumbFormat.JPEG else Image.fromarray(raw.postprocess())
        except: pass
        
        if img is None: img = Image.open(filepath)
        img = ImageOps.exif_transpose(img)
        
        # 2. Histogram
        img_small = img.resize((32, 32), Image.Resampling.NEAREST).convert("RGB")
        hist_data = [x / (32*32) for x in img_small.histogram()]

        # 3. Kualitas & dHash
        img_p = img.copy()
        img_p.thumbnail((100, 100))
        gray_pil = img_p.convert("L")
        w, h = gray_pil.size
        
        # Hitung dHash asli untuk kemiripan
        tiny = gray_pil.resize((9, 8), Image.Resampling.LANCZOS)
        pixels = list(tiny.getdata())
        diff = []
        for row in range(8):
            for col in range(8): diff.append(pixels[row*9+col] > pixels[row*9+col+1])
        dhash = int("".join("1" if x else "0" for x in diff), 2)
        
        # Sharpness
        sharpness_score = ImageStat.Stat(gray_pil.filter(ImageFilter.FIND_EDGES)).var[0]

        # 4. Exposure Penalty
        center = gray_pil.crop((w*0.25, h*0.25, w*0.75, h*0.75))
        hist = center.histogram(); tot = center.width * center.height
        if tot > 0:
            if (sum(hist[:15])/tot) > 0.3: penalty += 500
            if (sum(hist[240:])/tot) > 0.3: penalty += 800

        # 5. Face/Blink Detection
        if CV2_AVAILABLE:
            global _FACE_CASCADE, _EYE_CASCADE
            if _FACE_CASCADE is None: 
                _FACE_CASCADE = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
                _EYE_CASCADE = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
            
            if not _FACE_CASCADE.empty():
                img_cv = np.array(img_p)
                gray_cv = cv2.cvtColor(img_cv, cv2.COLOR_RGB2GRAY)
                faces = _FACE_CASCADE.detectMultiScale(gray_cv, 1.3, 5)
                for (x,y,fw,fh) in faces:
                    roi = gray_cv[y:y+fh, x:x+fw]
                    if len(_EYE_CASCADE.detectMultiScale(roi, 1.1, 3)) < 1: blink_penalty += 800

        score = max(0, sharpness_score - penalty - blink_penalty)
        return (filepath, score, dhash, hist_data)
    except Exception as e:
        print(f"Error worker: {e}")
        return (filepath, 0, 0, [])

# ==========================================
# HELPER CLASSES
# ==========================================

class ToolTip(object):
    def __init__(self, widget, text='widget info'):
        self.waittime = 500
        self.wraplength = 180
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        try:
            x, y, cx, cy = self.widget.bbox("insert")
        except:
            x = y = 0
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        self.tw = tk.Toplevel(self.widget)
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        self.tw.attributes("-topmost", True)
        label = tk.Label(self.tw, text=self.text, justify='left',
                       background="#ffffe0", relief='solid', borderwidth=1,
                       font=("tahoma", "8", "normal"),
                       wraplength = self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()

class ConfigManager:
    def __init__(self):
        if sys.platform.startswith("win"):
            appdata_dir = Path(os.environ.get('APPDATA', Path.home() / 'AppData/Roaming')) / "PhotoSortPro"
        else: 
            appdata_dir = Path.home() / ".config" / "photosortpro"
            
        appdata_dir.mkdir(parents=True, exist_ok=True)
        self.config_file = appdata_dir / "photosort_config_v4.json"
        
        self.defaults = {
            "language": None,
            "first_run": True,
            "categories": [
                {"slug": "good", "name": "Good", "color": "#22C55E", "hotkey": "1"},
                {"slug": "mid", "name": "Mid", "color": "#EAB308", "hotkey": "2"},
                {"slug": "bad", "name": "Bad", "color": "#EF4444", "hotkey": "3"}
            ],
            "verify_checksum": True
        }
        self.data = self.load_config()

    def load_config(self):
        if self.config_file.exists(): 
            try:
                with open(self.config_file, 'r') as f:
                    loaded = json.load(f)
                    for k, v in self.defaults.items():
                        if k not in loaded: loaded[k] = v
                    return loaded
            except:
                return self.defaults
        return self.defaults

    def save_config(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.data, f)

class LanguageSelector(ctk.CTkToplevel):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.callback = callback
        self.title("Select Language")
        self.geometry("400x500")
        self.resizable(False, False)
        self.grab_set() 
        self.center_window_toplevel()
        
        ctk.CTkLabel(self, text="Welcome / Selamat Datang", font=("Arial", 20, "bold")).pack(pady=20)
        ctk.CTkLabel(self, text="Please select your language:", font=("Arial", 14)).pack(pady=10)
        
        for lang in LANGUAGES.keys():
            ctk.CTkButton(self, text=lang, command=lambda l=lang: self.select_lang(l),
                          fg_color=COLORS["secondary"], hover_color=COLORS["accent"]).pack(pady=5, fill="x", padx=50)

    def center_window_toplevel(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def select_lang(self, lang):
        self.destroy()
        self.callback(lang)

class HotkeyDialog(ctk.CTkToplevel):
    def __init__(self, parent, categories, callback):
        super().__init__(parent)
        self.callback = callback
        self.categories = categories
        self.new_cats = [c.copy() for c in categories]
        self.title("Set Hotkeys")
        self.geometry("350x450")
        self.attributes("-topmost", True)
        self.update_idletasks()
        
        x = parent.winfo_x() + (parent.winfo_width() // 2) - 175
        y = parent.winfo_y() + (parent.winfo_height() // 2) - 225
        self.geometry(f"350x450+{x}+{y}")
        
        self.listening_idx = None
        self.layout_ui()

    def layout_ui(self):
        scroll = ctk.CTkScrollableFrame(self)
        scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        for idx, cat in enumerate(self.new_cats):
            f = ctk.CTkFrame(scroll, fg_color="transparent")
            f.pack(pady=5, padx=5, fill="x")
            
            lbl_col = ctk.CTkLabel(f, text="█", text_color=cat["color"], font=("Arial", 16))
            lbl_col.pack(side="left", padx=5)
            
            ctk.CTkLabel(f, text=cat["name"]).pack(side="left")
            
            btn = ctk.CTkButton(f, text=cat["hotkey"].upper(), width=80, 
                             command=lambda i=idx: self.listen_key(i))
            btn.pack(side="right")
            setattr(self, f"btn_{idx}", btn)
            
        ctk.CTkButton(self, text="Save", fg_color=COLORS["accent"], command=self.save).pack(pady=10)

    def listen_key(self, idx):
        self.listening_idx = idx
        getattr(self, f"btn_{idx}").configure(text="Press Key...")
        self.unbind("<Key>") 
        self.bind("<Key>", self.on_key)

    def on_key(self, event):
        if self.listening_idx is not None:
            key = event.keysym
            if len(key) == 1: key = key.lower()
            self.new_cats[self.listening_idx]["hotkey"] = key
            getattr(self, f"btn_{self.listening_idx}").configure(text=key)
            self.listening_idx = None
            self.unbind("<Key>") 

    def save(self):
        self.callback(self.new_cats)
        self.destroy()

# --- IMAGE VIEWER (ZOOM/PAN) ---
class ImageViewerWindow(ctk.CTkToplevel):
    def __init__(self, parent, image_path):
        super().__init__(parent)
        
        # PERBAIKAN: Viewer harus lebih depan daripada Review Window
        self.attributes("-topmost", True)
        self.focus_force()
        
        self.title(f"Viewer - {os.path.basename(image_path)}")
        self.geometry("1000x800")
        
        self.image_path = image_path
        
        # ... (Sisa kode init sama seperti sebelumnya)
        if hasattr(parent, '_load_image_data'):
             self.pil_image = parent._load_image_data(image_path, os.path.basename(image_path), thumb_only=False)
        else:
             # Fallback
             try: self.pil_image = Image.open(image_path)
             except: self.pil_image = None
        
        # ... (Lanjutkan sampai self.redraw())
        
        # PASTIKAN DI SINI KODE LAINNYA TIDAK DIHAPUS (Zoom/Pan logic)
        if not self.pil_image:
             messagebox.showerror("Error", "Failed", parent=self)
             self.destroy()
             return
             
        self.zoom_scale = 1.0
        self.pan_x = 0
        self.pan_y = 0
        self._drag_data = {"x": 0, "y": 0}

        self.canvas = tk.Canvas(self, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)
        self.canvas.bind("<ButtonPress-1>", self.on_pan_start)
        self.canvas.bind("<B1-Motion>", self.on_pan_move)
        
        self.redraw()

    def redraw(self):
        cw = self.winfo_width()
        ch = self.winfo_height()
        if cw < 50: cw = 1000 
        if ch < 50: ch = 800
        
        iw, ih = self.pil_image.size
        fit_scale = min(cw/iw, ch/ih)
        final_scale = fit_scale * self.zoom_scale
        
        new_w, new_h = int(iw * final_scale), int(ih * final_scale)
        if new_w < 1: new_w = 1
        if new_h < 1: new_h = 1
        
        if final_scale < 1.0:
            resample = Image.Resampling.NEAREST if self.zoom_scale < 1.0 else Image.Resampling.LANCZOS
        else:
            resample = Image.Resampling.NEAREST
            
        img_res = self.pil_image.resize((new_w, new_h), resample)
        self.tk_img = ImageTk.PhotoImage(img_res)
        
        self.canvas.delete("all")
        self.canvas.create_image((cw//2)+self.pan_x, (ch//2)+self.pan_y, image=self.tk_img, anchor="center")

    def on_mouse_wheel(self, event):
        if event.delta > 0: self.zoom_scale *= 1.1
        else: self.zoom_scale /= 1.1
        self.redraw()

    def on_pan_start(self, event):
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def on_pan_move(self, event):
        dx = event.x - self._drag_data["x"]
        dy = event.y - self._drag_data["y"]
        self.pan_x += dx
        self.pan_y += dy
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y
        self.redraw()

class SmartReviewWindow(ctk.CTkToplevel):
    def __init__(self, parent, grouped_data, callback_confirm):
        super().__init__(parent)
        self.parent = parent
        self.grouped_data = grouped_data 
        self.callback_confirm = callback_confirm
        self.executor = ThreadPoolExecutor(max_workers=4)
        
        # --- CONFIG WINDOW ---
        self.title(f"Smart Select Review - {len(grouped_data)} Groups")
        self.geometry("1100x750")
        self.attributes("-topmost", True)
        self.grab_set()

        # --- STATE MANAGEMENT ---
        self.page_size = 8
        self.current_page = 0
        self.total_pages = max(1, math.ceil(len(grouped_data) / self.page_size))
        
        # --- CONTAINER UTAMA ---
        # Kita gunakan satu container untuk menampung View List atau View Preview
        self.main_container = ctk.CTkFrame(self)
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)

        # Init View Variables
        self.view_canvas = None
        self.hr_image = None
        self.hr_zoom = 1.0
        self.hr_pan_x = 0
        self.hr_pan_y = 0

        # Mulai dengan Tampilan List
        self.show_list_view()

    # =========================================================
    # LOGIC: TAMPILAN LIST (GRID)
    # =========================================================
    def show_list_view(self):
        """Menampilkan daftar foto (Grid Mode)"""
        self._clear_container()

        # 1. HEADER LIST
        header = ctk.CTkFrame(self.main_container, height=50, fg_color="transparent")
        header.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(header, text="Review Mode (JPG Priority)", font=("Arial", 18, "bold")).pack(side="left")
        
        btn_box = ctk.CTkFrame(header, fg_color="transparent")
        btn_box.pack(side="right")
        ctk.CTkButton(btn_box, text="CONFIRM & MOVE", fg_color="#22C55E", command=self.confirm_selection).pack(side="left", padx=5)
        ctk.CTkButton(btn_box, text="CANCEL", fg_color="#EF4444", command=self.destroy).pack(side="left", padx=5)

        # 2. SCROLL AREA
        self.scroll_frame = ctk.CTkScrollableFrame(self.main_container, fg_color="#2B2C38")
        self.scroll_frame.pack(fill="both", expand=True)

        # 3. PAGINATION FOOTER
        footer = ctk.CTkFrame(self.main_container, height=40, fg_color="transparent")
        footer.pack(fill="x", pady=10)
        
        self.btn_prev = ctk.CTkButton(footer, text="< Prev", width=100, command=self.prev_page)
        self.btn_prev.pack(side="left")
        self.lbl_page = ctk.CTkLabel(footer, text=f"Page {self.current_page+1}/{self.total_pages}", font=("Arial", 12, "bold"))
        self.lbl_page.pack(side="left", expand=True)
        self.btn_next = ctk.CTkButton(footer, text="Next >", width=100, command=self.next_page)
        self.btn_next.pack(side="right")

        # ISI DATA
        self.populate_rows()

    def populate_rows(self):
        # Bersihkan isian lama
        for w in self.scroll_frame.winfo_children(): w.destroy()
        
        start = self.current_page * self.page_size
        end = start + self.page_size
        page_data = self.grouped_data[start:end]
        
        self.lbl_page.configure(text=f"Page {self.current_page + 1} / {self.total_pages}")
        self.btn_prev.configure(state="normal" if self.current_page > 0 else "disabled")
        self.btn_next.configure(state="normal" if self.current_page < self.total_pages - 1 else "disabled")

        for i, group in enumerate(page_data):
            self._create_row_ui(start + i, group)

    def _create_row_ui(self, idx, group):
        row = ctk.CTkFrame(self.scroll_frame, fg_color="#343541", corner_radius=8)
        row.pack(fill="x", pady=5, padx=5)
        
        # --- WINNER SECTION ---
        w_data = group['winner']
        w_path = w_data[0]
        w_score = w_data[1] if len(w_data) > 1 else 0
        
        left = ctk.CTkFrame(row, fg_color="transparent", width=180)
        left.pack(side="left", padx=10, pady=5)
        
        ctk.CTkLabel(left, text="WINNER", text_color="#22C55E", font=("Arial", 10, "bold")).pack()
        
        # KLIK INI -> Masuk ke Mode Preview di Window yang SAMA
        btn_w = ctk.CTkButton(left, text="Loading...", width=150, height=110, fg_color="#111",
                              command=lambda p=w_path: self.show_preview_view(p))
        btn_w.pack(pady=3)
        ctk.CTkLabel(left, text=f"Score: {int(w_score)}").pack()
        self.executor.submit(self._load_thumb_task, w_path, btn_w, 150)
        
        # --- CANDIDATES SECTION ---
        right = ctk.CTkScrollableFrame(row, orientation="horizontal", height=150, fg_color="transparent")
        right.pack(side="left", fill="both", expand=True, padx=5)
        
        for cand in group['candidates']:
            c_path = cand[0]
            c_score = cand[1] if len(cand) > 1 else 0
            
            card = ctk.CTkFrame(right, fg_color="#444654")
            card.pack(side="left", padx=5)
            
            # KLIK INI -> Masuk ke Mode Preview
            btn_c = ctk.CTkButton(card, text="...", width=80, height=80, fg_color="#111",
                                  command=lambda p=c_path: self.show_preview_view(p))
            btn_c.pack(pady=2, padx=2)
            
            ctk.CTkLabel(card, text=f"{int(c_score)}").pack()
            ctk.CTkButton(card, text="Pick", width=60, height=20, fg_color="#3B82F6",
                          command=lambda i=idx, c=cand: self.swap_winner(i, c)).pack(pady=2)
            
            self.executor.submit(self._load_thumb_task, c_path, btn_c, 80)

    # =========================================================
    # LOGIC: TAMPILAN PREVIEW (SINGLE WINDOW / SPA MODE)
    # =========================================================
    def show_preview_view(self, image_path):
        """Menghapus Grid, Menampilkan Canvas Preview (Zoom/Pan)"""
        self._clear_container()

        # 1. TOOLBAR
        toolbar = ctk.CTkFrame(self.main_container, height=50, fg_color="#1E1E2E")
        toolbar.pack(fill="x", pady=(0, 5))
        
        # Tombol BACK (PENTING: Kembali ke List)
        ctk.CTkButton(toolbar, text="⬅ BACK TO LIST", width=120, fg_color="#4B5563",
                      command=self.show_list_view).pack(side="left", padx=10, pady=10)
        
        ctk.CTkLabel(toolbar, text=f"Viewing: {os.path.basename(image_path)}").pack(side="left", padx=10)
        ctk.CTkButton(toolbar, text="Reset Zoom", width=100, command=self._reset_zoom).pack(side="right", padx=10)

        # 2. CANVAS AREA
        self.view_canvas = tk.Canvas(self.main_container, bg="black", highlightthickness=0)
        self.view_canvas.pack(fill="both", expand=True)
        
        self.lbl_loading = ctk.CTkLabel(self.view_canvas, text="Loading High-Res...", text_color="white", bg_color="black")
        self.lbl_loading.place(relx=0.5, rely=0.5, anchor="center")

        # Reset Zoom Vars
        self.hr_zoom = 1.0
        self.hr_pan_x = 0
        self.hr_pan_y = 0
        self.hr_drag_data = {"x": 0, "y": 0}

        # Bind Events
        self.view_canvas.bind("<MouseWheel>", self._on_zoom)
        self.view_canvas.bind("<ButtonPress-1>", self._start_pan)
        self.view_canvas.bind("<B1-Motion>", self._do_pan)

        # Load Image
        threading.Thread(target=self._worker_load_hr, args=(image_path,), daemon=True).start()

    def _worker_load_hr(self, path):
        try:
            d_path = self._get_display_path(path)
            pil_img = Image.open(d_path)
            pil_img = ImageOps.exif_transpose(pil_img)
            self.hr_image = pil_img
            self.after(0, lambda: self.lbl_loading.destroy())
            self.after(0, self._redraw_hr)
        except Exception as e:
            self.after(0, lambda: self.lbl_loading.configure(text=f"Err: {e}"))

    def _redraw_hr(self):
        if not self.hr_image: return
        cw = self.view_canvas.winfo_width() or 800
        ch = self.view_canvas.winfo_height() or 600
        
        iw, ih = self.hr_image.size
        scale = min(cw/iw, ch/ih) * self.hr_zoom
        new_w, new_h = int(iw*scale), int(ih*scale)
        
        # Resize & Draw
        res = self.hr_image.resize((max(1, new_w), max(1, new_h)), Image.Resampling.NEAREST if self.hr_zoom<1 else Image.Resampling.LANCZOS)
        self.hr_tk_image = ImageTk.PhotoImage(res)
        
        self.view_canvas.delete("all")
        self.view_canvas.create_image((cw//2)+self.hr_pan_x, (ch//2)+self.hr_pan_y, image=self.hr_tk_image)

    # =========================================================
    # UTILITIES & HELPERS
    # =========================================================
    def _clear_container(self):
        for w in self.main_container.winfo_children(): w.destroy()

    def _get_display_path(self, path):
        """Cari JPG untuk RAW agar cepat"""
        base, ext = os.path.splitext(path)
        if ext.lower() in ['.arw', '.cr2', '.nef', '.dng', '.orf', '.raf']:
            for j in ['.jpg', '.JPG', '.jpeg', '.JPEG']:
                if os.path.exists(base + j): return base + j
        return path

    def _load_thumb_task(self, path, btn, base_height):
        try:
            # Ambil gambar dari loader utama
            pil_img = self.parent._load_image_data(path, os.path.basename(path), thumb_only=True)
            
            if pil_img:
                # Gunakan .copy() untuk memisahkan data antar thread
                temp_img = pil_img.copy()
                
                # Hitung Aspect Ratio agar gambar tidak gepeng
                aspect = temp_img.width / temp_img.height if temp_img.height != 0 else 1
                new_w = int(base_height * aspect)
                new_w = max(1, new_w)
                
                # Resize untuk tampilan tombol
                display_img = temp_img.resize((new_w, base_height), Image.Resampling.LANCZOS)
                
                def update_ui(ready_img, target_w, target_h):
                    if btn.winfo_exists():
                        # Buat CTkImage di thread utama UI
                        ctk_img = ctk.CTkImage(
                            light_image=ready_img, 
                            dark_image=ready_img, 
                            size=(target_w, target_h)
                        )
                        # Terapkan ke tombol
                        btn.configure(image=ctk_img, text="", width=target_w, height=target_h)
                        
                        # --- DOUBLE ANCHORING: MENCEGAH KOTAK HITAM ---
                        btn._img_ref = ctk_img
                        btn.image = ctk_img 
                
                # Kirim ke main thread
                btn.after(0, lambda: update_ui(display_img, new_w, base_height))
            else:
                btn.after(0, lambda: btn.configure(text="N/A"))
        except Exception as e:
            print(f"Review Thumb Error: {e}")
            btn.after(0, lambda: btn.configure(text="ERR"))

    # Zoom/Pan Handlers
    def _on_zoom(self, e):
        self.hr_zoom *= 1.1 if e.delta > 0 else 0.9
        self._redraw_hr()
    def _start_pan(self, e): self.hr_drag_data = {"x": e.x, "y": e.y}
    def _do_pan(self, e):
        self.hr_pan_x += e.x - self.hr_drag_data["x"]
        self.hr_pan_y += e.y - self.hr_drag_data["y"]
        self.hr_drag_data = {"x": e.x, "y": e.y}
        self._redraw_hr()
    def _reset_zoom(self):
        self.hr_zoom = 1.0; self.hr_pan_x = 0; self.hr_pan_y = 0
        self._redraw_hr()

    # Navigasi & Aksi
    def swap_winner(self, idx, new_win):
        grp = self.grouped_data[idx]
        old = grp['winner']
        grp['candidates'].append(old)
        grp['candidates'] = [c for c in grp['candidates'] if c[0] != new_win[0]]
        grp['winner'] = new_win
        self.show_list_view() # Refresh list
        
    def prev_page(self): 
        if self.current_page > 0: self.current_page -= 1; self.show_list_view()
    def next_page(self): 
        if self.current_page < self.total_pages - 1: self.current_page += 1; self.show_list_view()
    def confirm_selection(self):
        self.callback_confirm(self.grouped_data)
        self.destroy()

# ==========================================
# TUTORIAL OVERLAY
# ==========================================
class TutorialOverlay(tk.Toplevel):
    def __init__(self, parent, text, next_callback, prev_callback, skip_callback, target_widget=None, is_first=False):
        super().__init__(parent)
        self.parent = parent
        self.next_callback = next_callback
        self.prev_callback = prev_callback
        self.skip_callback = skip_callback
        self.text = text
        self.target_widget = target_widget
        self.is_first = is_first
        
        self._resize_job = None
        self._drag_data = {"x": 0, "y": 0} # Data untuk fitur drag
        
        self.overrideredirect(True)
        self.wm_attributes("-topmost", True)
        self.transparent_color = "#add123" 
        self.configure(bg=self.transparent_color)
        self.wm_attributes("-transparentcolor", self.transparent_color)
        
        self.canvas = tk.Canvas(self, bg=self.transparent_color, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        self.parent.bind("<Configure>", self.on_parent_configure, add="+")
        self.after(100, self.force_refresh_layout)
    
    def on_parent_configure(self, event):
        if event.widget == self.parent:
            if self._resize_job: self.after_cancel(self._resize_job)
            self._resize_job = self.after(50, self.force_refresh_layout)

    def force_refresh_layout(self):
        if not self.winfo_exists() or not self.parent.winfo_exists(): return
        try:
            self.parent.update_idletasks()
            x = self.parent.winfo_rootx()
            y = self.parent.winfo_rooty()
            w = self.parent.winfo_width()
            h = self.parent.winfo_height()
            if w < 50 or h < 50: return
            self.geometry(f"{w}x{h}+{x}+{y}")
            self.after(10, lambda: self._draw_content(w, h))
        except: pass

    def _draw_content(self, app_w, app_h):
        self.canvas.delete("all")
        dim_opts = {'fill': 'black', 'outline': '', 'stipple': 'gray50'}
        
        if not self.target_widget:
            self.canvas.create_rectangle(0, 0, app_w, app_h, **dim_opts)
            self._create_explanation_box(app_w, app_h, 0, 0, 0, 0, has_target=False)
            return

        try:
            self.target_widget.update_idletasks()
            t_x = self.target_widget.winfo_rootx()
            t_y = self.target_widget.winfo_rooty()
            t_w = self.target_widget.winfo_width()
            t_h = self.target_widget.winfo_height()
            
            my_x = self.winfo_rootx()
            my_y = self.winfo_rooty()
            
            draw_x = t_x - my_x
            draw_y = t_y - my_y
            
            pad = 5
            x = draw_x - pad; y = draw_y - pad
            w = t_w + (pad * 2); h = t_h + (pad * 2)
            
            self.canvas.create_rectangle(0, 0, app_w, y, **dim_opts) 
            self.canvas.create_rectangle(0, y + h, app_w, app_h, **dim_opts)
            self.canvas.create_rectangle(0, y, x, y + h, **dim_opts) 
            self.canvas.create_rectangle(x + w, y, app_w, y + h, **dim_opts) 
            self.canvas.create_rectangle(x, y, x+w, y+h, outline="#FFD700", width=3)
            self._create_explanation_box(app_w, app_h, x, y, w, h, has_target=True)
        except:
            self.canvas.create_rectangle(0, 0, app_w, app_h, **dim_opts)
            self._create_explanation_box(app_w, app_h, 0, 0, 0, 0, has_target=False)

    def _create_explanation_box(self, app_w, app_h, tx, ty, tw, th, has_target):
        # Frame Utama Kotak Penjelasan
        self.container = ctk.CTkFrame(self.canvas, fg_color=COLORS["bg"], border_width=2, border_color=COLORS["accent"], corner_radius=10)
        
        # FITUR DRAG: Klik dan tarik kotak untuk memindahkannya
        self.container.bind("<Button-1>", self._on_drag_start)
        self.container.bind("<B1-Motion>", self._on_drag_move)
        
        lbl_text = ctk.CTkLabel(self.container, text=self.text, wraplength=350, justify="left", font=("Arial", 14), text_color=COLORS["fg"])
        lbl_text.pack(padx=20, pady=(20, 10))
        # Bind juga ke label agar bisa di-drag lewat teks
        lbl_text.bind("<Button-1>", self._on_drag_start)
        lbl_text.bind("<B1-Motion>", self._on_drag_move)

        frame_btns = ctk.CTkFrame(self.container, fg_color="transparent")
        frame_btns.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkButton(frame_btns, text="Exit", command=self.skip, width=50, fg_color=COLORS["danger"]).pack(side="left")
        ctk.CTkButton(frame_btns, text="Next >", command=self.next_step, width=70, fg_color=COLORS["accent"]).pack(side="right")
        
        if not self.is_first:
            ctk.CTkButton(frame_btns, text="< Prev", command=self.prev_step, width=70, fg_color=COLORS["secondary"]).pack(side="right", padx=5)

        # LOGIKA POSISI: Tengah jika target terlalu besar (seperti Log Aktivitas)
        box_w, box_h = 400, 250
        
        # Jika target widget memakan lebih dari 70% layar, paksa ke tengah
        if not has_target or tw > (app_w * 0.7) or th > (app_h * 0.7):
            final_x = (app_w - box_w) // 2
            final_y = (app_h - box_h) // 2
        else:
            # Kalkulasi posisi aman di sekitar target
            if (tx + tw + 20 + box_w) < app_w: final_x, final_y = tx + tw + 20, ty
            elif (tx - box_w - 20) > 0: final_x, final_y = tx - box_w - 20, ty
            else: final_x, final_y = (app_w - box_w) // 2, (app_h - box_h) // 2
            
        self.explanation_window_id = self.canvas.create_window(final_x, final_y, window=self.container, anchor="nw")

    def _on_drag_start(self, event):
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def _on_drag_move(self, event):
        dx = event.x - self._drag_data["x"]
        dy = event.y - self._drag_data["y"]
        # Update posisi window di dalam canvas
        cur_x, cur_y = self.canvas.coords(self.explanation_window_id)
        self.canvas.coords(self.explanation_window_id, cur_x + dx, cur_y + dy)

    def next_step(self): self._cleanup(); self.next_callback()
    def prev_step(self): self._cleanup(); self.prev_callback()
    def skip(self): self._cleanup(); self.skip_callback()
    def _cleanup(self):
        if self._resize_job: self.after_cancel(self._resize_job)
        try: self.parent.unbind("<Configure>")
        except: pass
        self.destroy()

# ==========================================
# MAIN APPLICATION
# ==========================================
class PhotoSortApp(TkinterDnD_CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")
        
        self.config_mgr = ConfigManager()
        self.config = self.config_mgr.data
        self.lang_code = self.config["language"]
        self.categories = self.config["categories"]
        
        self.title("PhotoSort Pro v4.1")
        self.center_window(1200, 850)
        
        self.executor = ThreadPoolExecutor(max_workers=min(4, os.cpu_count() or 1))
        self.processing = False
        self.stop_event = threading.Event()
        
        # --- PERBAIKAN: VARIABEL KONTROL ---
        self.smart_window = None         # "Satpam" Window: Agar tidak muncul dobel
        self.thumbnail_cache = {}        # Cache Foto Kecil (Agar foto tidak blank/error)
        self.cache_lock = threading.Lock()
        self.cached_smart_groups = None  # Simpan hasil scan (Agar tidak scan ulang saat Batal)
        self.cached_smart_params = None
        # -----------------------------------

        # State Variables
        
        # State Variables
        self.smart_window = None     # Untuk mencegah window muncul dobel
        self.thumbnail_cache = {}
        self.manual_files = [] 
        self.manual_index = 0
        self.manual_decisions = {} 
        self.rotation_angle = 0
        self.current_pil_image = None 
        self.tutorial_step = 0 
        self.current_overlay = None 
        self.preview_mode = "JPG" 
        self.undo_stack = []
        self.image_cache = OrderedDict()
        self.cache_size = 5
        self.thumbnail_cache = {} # OPTIMIZATION: Reduced from 15 to 10 for better RAM usage
        self.filmstrip_cache = {} 
        self.cached_smart_groups = None  # Cache hasil analisis Smart Select
        self.cached_smart_params = None
        self.zoom_scale = 1.0
        self.pan_x = 0; self.pan_y = 0
        self._drag_data = {"x": 0, "y": 0}

        if not self.lang_code:
            self.withdraw() 
            LanguageSelector(self, self.set_language_and_start)
        else:
            self.init_ui()
            if self.config["first_run"]:
                self.after(1000, self.start_guided_tour)
                self.config["first_run"] = False
                self.config_mgr.save_config()
                
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        if self.processing:
            if not messagebox.askyesno("Exit", self.get_text("msg_confirm_stop")): return
            self.stop_event.set()
        self.destroy()
        sys.exit()

    def check_dependencies(self):
        missing = []
        if not RAWPY_AVAILABLE:
            missing.append("rawpy")
        if not CV2_AVAILABLE:
            missing.append("opencv-python")
        
        # Baris 'if' ini sejajar dengan 'missing = []'
        if missing:
            # Baris di bawah ini HARUS lebih menjorok ke kanan daripada 'if'
            self.log_message(f"⚠️ FITUR TERBATAS: Pustaka {', '.join(missing)} tidak ditemukan.", tag="danger") [cite: 157]
            self.log_message("Saran: Jalankan 'pip install rawpy opencv-python' agar fitur maksimal.") [cite: 157]

    def center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def set_language_and_start(self, lang):
        self.config["language"] = lang
        self.config_mgr.save_config()
        self.lang_code = lang
        self.deiconify()
        self.update()
        self.lift()
        self.focus_force()
        self.center_window(1200, 850)
        self.init_ui()
        if self.config["first_run"]:
            self.after(1000, self.start_guided_tour)
            self.config["first_run"] = False
            self.config_mgr.save_config()

    def get_text(self, key):
        lang_dict = LANGUAGES.get(self.lang_code, LANGUAGES["English"])
        return lang_dict.get(key, key)
    
    def _get_unique_path(self, destination, filename):
        base, ext = os.path.splitext(filename)
        counter = 1
        new_name = filename
        while os.path.exists(os.path.join(destination, new_name)):
            new_name = f"{base}_{counter}{ext}"
            counter += 1
        return os.path.join(destination, new_name)

    def _is_protected_path(self, path):
        try:
            norm = os.path.abspath(path)
            if platform.system() == "Windows":
                protected = [os.environ.get("SystemRoot", r"C:\Windows"), r"C:\Program Files", r"C:\Program Files (x86)"]
                return any(norm.lower().startswith(p.lower()) for p in protected)
            else:
                return norm in ["/", "/root", "/etc", "/usr", "/bin", "/sbin", "/var"]
        except:
            return False

    def safe_copy_move(self, src, dst, action="copy", use_checksum=True):
        """OPTIMIZED COPY MOVE FOR MACOS (Fixes Permission & SSD Issues)"""
        try:
            # 1. Cek File Sumber
            if not os.path.isfile(src):
                print(f"[ERROR] Source missing: {src}")
                return False, "Source not found"
            
            # 2. Buat Folder Tujuan
            dst_dir = os.path.dirname(dst)
            os.makedirs(dst_dir, exist_ok=True)

            # 3. EKSEKUSI COPY (Dengan penanganan error spesifik)
            try:
                shutil.copy2(src, dst)
            except PermissionError:
                err_msg = "Permission Denied. Check Full Disk Access."
                print(f"[CRITICAL] {err_msg} -> {dst}")
                return False, err_msg
            except OSError as e:
                # Menangani error filesystem (misal: SSD NTFS yang Read-Only)
                print(f"[OS ERROR] {e} -> {dst}")
                return False, f"OS Error: {e}"

            # 4. VERIFIKASI (Di macOS SSD External, checksum sering bikin macet/timeout)
            # Kita matikan checksum yang berat jika di macOS, kecuali user memaksa.
            if use_checksum and platform.system() != "Darwin":
                s_size = os.path.getsize(src)
                d_size = os.path.getsize(dst)
                if s_size != d_size:
                    try: os.remove(dst)
                    except: pass
                    return False, "Size Mismatch"

            return True, None
            
        except Exception as e:
            print(f"[GENERAL ERROR] {e}")
            return False, str(e)

    def log_message(self, message, tag=None):
        ts = datetime.datetime.now().strftime("[%H:%M:%S]")
        full_msg = f"{ts} {message}"
        
        # 1. Tulis ke GUI (seperti biasa)
        try:
            self.txt_log.configure(state="normal")
            self.txt_log.insert("end", full_msg + "\n", tag)
            self.txt_log.see("end")
            self.txt_log.configure(state="disabled")
        except:
            pass 

        # 2. IMPROVEMENT: Tulis ke File (Append Mode)
        try:
            log_file = "PhotoSort_Debug.log"
            # Gunakan encoding utf-8 agar simbol panah/emoji tidak bikin error
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(full_msg + "\n")
        except Exception as e:
            print(f"Gagal menulis log: {e}")

    def init_ui(self):
        for widget in self.winfo_children(): widget.destroy() 
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar [cite: 160, 161]
        self.sidebar = ctk.CTkFrame(self, width=80, corner_radius=0, fg_color=COLORS["secondary"])
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.btn_help = ctk.CTkButton(self.sidebar, text="❓", width=50, height=50, command=self.start_guided_tour)
        self.btn_help.pack(pady=(20, 10), padx=10)

        self.btn_lang = ctk.CTkButton(self.sidebar, text="🌐", width=50, height=50, fg_color=COLORS["input_bg"], command=self.change_language_ui)
        self.btn_lang.pack(pady=10, padx=10)
        
        self.btn_refresh = ctk.CTkButton(self.sidebar, text="🔄", width=50, height=50, fg_color=COLORS["input_bg"], hover_color=COLORS["warning"], command=self.refresh_app_state)
        self.btn_refresh.pack(pady=10, padx=10)
        ToolTip(self.btn_refresh, self.get_text("tip_refresh"))

        # Link Instagram [cite: 1, 161]
        spacer = ctk.CTkLabel(self.sidebar, text="") 
        spacer.pack(expand=True, fill="both")
        
        ctk.CTkLabel(self.sidebar, text="complain\nhere:", font=("Arial", 10), text_color="gray").pack(pady=(10,0))
        self.btn_instagram = ctk.CTkButton(self.sidebar, text="📸", width=40, height=40, fg_color="transparent", 
                                           command=lambda: webbrowser.open("https://www.instagram.com/hiro.fx/"))
        self.btn_instagram.pack(pady=(0, 20))

        # Content [cite: 162]
        self.tabview = ctk.CTkTabview(self, command=self.on_tab_change)
        self.tabview.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.tab_auto = self.tabview.add(self.get_text("tab_auto"))
        self.tab_manual = self.tabview.add(self.get_text("tab_manual"))
        self.tab_smart = self.tabview.add(self.get_text("tab_smart"))
        self.tab_log = self.tabview.add(self.get_text("tab_log"))

        self.setup_auto_sort_ui()
        self.setup_manual_sort_ui()
        self.setup_smart_select_ui() 
        self.setup_log_ui()

    def refresh_app_state(self):
        self.stop_event.clear()
        self.processing = False
        self.manual_files = []; self.manual_index = 0; self.manual_decisions = {} 
        self.undo_stack = []; self.image_cache.clear(); self.filmstrip_cache.clear()
        self.rotation_angle = 0; self.current_pil_image = None
        self.zoom_scale = 1.0; self.pan_x = 0; self.pan_y = 0
        self.init_ui()

    def setup_log_ui(self):
        t = self.tab_log
        t.grid_columnconfigure(0, weight=1); t.grid_rowconfigure(0, weight=1)
        self.txt_log = ctk.CTkTextbox(t, fg_color=COLORS["bg"], font=("Consolas", 12))
        self.txt_log.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.txt_log.tag_config("danger", foreground=COLORS["danger"])
        self.txt_log.insert("0.0", f"--- {self.get_text('title')} Log Started ---\n")
        self.txt_log.configure(state="disabled")

    def on_tab_change(self): self.focus()
    def change_language_ui(self): LanguageSelector(self, self.reload_language)
    def reload_language(self, lang):
        self.config["language"] = lang
        self.config_mgr.save_config()
        self.lang_code = lang
        self.init_ui()

    def select_folder(self, entry_widget):
        folder = filedialog.askdirectory()
        if folder:
            if self._is_protected_path(folder):
                messagebox.showwarning("Warning", "Selected folder is protected by the system. Please choose another folder.")
                return
            entry_widget.configure(state="normal")
            entry_widget.delete(0, "end")
            entry_widget.insert(0, folder)
            entry_widget.configure(state="disabled")

    def drop_handler(self, event, entry_widget):
        data = event.data
        if data.startswith('{') and data.endswith('}'): data = data[1:-1]
        if os.path.isdir(data):
            if self._is_protected_path(data):
                messagebox.showwarning("Warning", "Selected folder is protected by the system. Please choose another folder.")
                return
            entry_widget.configure(state="normal")
            entry_widget.delete(0, "end")
            entry_widget.insert(0, data)
            entry_widget.configure(state="disabled")

    def open_file_explorer(self, path):
        if platform.system() == "Windows": os.startfile(path)
        elif platform.system() == "Darwin": subprocess.Popen(["open", path])
        else: subprocess.Popen(["xdg-open", path])

    # ==========================================
    # AUTO SORT UI
    # ==========================================
    def setup_auto_sort_ui(self):
        t = self.tab_auto
        t.grid_columnconfigure(0, weight=1)
        
        self.frame_folders_auto = ctk.CTkFrame(t) 
        self.frame_folders_auto.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkLabel(self.frame_folders_auto, text=self.get_text("lbl_source")).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_src_auto = ctk.CTkEntry(self.frame_folders_auto, width=400)
        self.entry_src_auto.grid(row=0, column=1, padx=10)
        if DND_AVAILABLE:
            self.entry_src_auto.drop_target_register(DND_FILES)
            self.entry_src_auto.dnd_bind('<<Drop>>', lambda e: self.drop_handler(e, self.entry_src_auto))
        ctk.CTkButton(self.frame_folders_auto, text=self.get_text("btn_browse"), width=100, command=lambda: self.select_folder(self.entry_src_auto)).grid(row=0, column=2, padx=10)

        ctk.CTkLabel(self.frame_folders_auto, text=self.get_text("lbl_dest")).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.entry_dst_auto = ctk.CTkEntry(self.frame_folders_auto, width=400)
        self.entry_dst_auto.grid(row=1, column=1, padx=10)
        if DND_AVAILABLE:
            self.entry_dst_auto.drop_target_register(DND_FILES)
            self.entry_dst_auto.dnd_bind('<<Drop>>', lambda e: self.drop_handler(e, self.entry_dst_auto))
        ctk.CTkButton(self.frame_folders_auto, text=self.get_text("btn_browse"), width=100, command=lambda: self.select_folder(self.entry_dst_auto)).grid(row=1, column=2, padx=10)

        self.lbl_subfolder_auto = ctk.CTkLabel(self.frame_folders_auto, text=self.get_text("lbl_subfolder"))
        self.lbl_subfolder_auto.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.entry_subfolder = ctk.CTkEntry(self.frame_folders_auto, width=400, placeholder_text="Sorted_Result")
        self.entry_subfolder.grid(row=2, column=1, padx=10)

        self.frame_codes = ctk.CTkFrame(t)
        self.frame_codes.pack(pady=10, padx=20, fill="x")
        
        header_frame = ctk.CTkFrame(self.frame_codes, fg_color="transparent")
        header_frame.pack(fill="x", padx=10, pady=(10,0))
        ctk.CTkLabel(header_frame, text=self.get_text("lbl_codes")).pack(side="left")
        
        self.btn_check_codes = ctk.CTkButton(header_frame, text=self.get_text("btn_check_codes"), width=100, height=24, fg_color=COLORS["secondary"], command=self.check_codes_window)
        self.btn_check_codes.pack(side="right")
        
        self.txt_codes = ctk.CTkTextbox(self.frame_codes, height=80, fg_color=COLORS["input_bg"])
        self.txt_codes.pack(fill="x", padx=10, pady=10)

        self.frame_opts_auto = ctk.CTkFrame(t)
        self.frame_opts_auto.pack(pady=10, padx=20, fill="x")
        self.var_auto_action = tk.StringVar(value="copy")
        self.var_auto_filter = tk.StringVar(value="all")
        self.var_auto_rename = tk.BooleanVar(value=False)
        self.var_checksum = tk.BooleanVar(value=self.config.get("verify_checksum", True))

        ctk.CTkLabel(self.frame_opts_auto, text=self.get_text("lbl_action")).pack(side="left", padx=15)
        ctk.CTkRadioButton(self.frame_opts_auto, text=self.get_text("radio_copy"), variable=self.var_auto_action, value="copy").pack(side="left", padx=5)
        ctk.CTkRadioButton(self.frame_opts_auto, text=self.get_text("radio_cut"), variable=self.var_auto_action, value="cut").pack(side="left", padx=5)
        ctk.CTkLabel(self.frame_opts_auto, text="| " + self.get_text("lbl_filter")).pack(side="left", padx=15)
        ctk.CTkRadioButton(self.frame_opts_auto, text=self.get_text("radio_raw_jpg"), variable=self.var_auto_filter, value="all").pack(side="left", padx=5)
        ctk.CTkRadioButton(self.frame_opts_auto, text=self.get_text("radio_raw_only"), variable=self.var_auto_filter, value="raw").pack(side="left", padx=5)
        ctk.CTkCheckBox(self.frame_opts_auto, text=self.get_text("chk_rename"), variable=self.var_auto_rename).pack(side="right", padx=15)
        ctk.CTkCheckBox(self.frame_opts_auto, text="Fast Checksum", variable=self.var_checksum).pack(side="right", padx=5)

        self.btn_auto_start = ctk.CTkButton(t, text=self.get_text("btn_start_auto"), fg_color=COLORS["accent"], hover_color=COLORS["accent_hover"], height=50, font=("Arial", 16, "bold"), command=self.run_auto_sort)
        self.btn_auto_start.pack(pady=20, padx=20, fill="x")
        self.progress_bar = ctk.CTkProgressBar(t); self.progress_bar.set(0)
        self.progress_bar.pack(pady=5, padx=20, fill="x")
        self.lbl_status_auto = ctk.CTkLabel(t, text=self.get_text("status_ready"))
        self.lbl_status_auto.pack(pady=5)

    def parse_codes_ultimate(self, raw_text):
        raw_text = re.sub(r'(No\s*file\s*:|list\s*:)', '', raw_text, flags=re.IGNORECASE)
        raw_text = re.sub(r'\s+(\d+[.)])', r'\n\1', raw_text)
        raw_text = raw_text.replace(',', '\n')
        codes = []
        for line in raw_text.splitlines():
            clean = re.sub(r'^\d+\s*[.)]\s*', '', line.strip()).rstrip(" .")
            if 3 <= len(clean) <= 12: codes.append(clean)
        return codes

    def check_codes_window(self):
        codes = self.parse_codes_ultimate(self.txt_codes.get("0.0", "end"))
        top = ctk.CTkToplevel(self)
        top.title(self.get_text("preview_title")); top.geometry("300x400"); top.attributes("-topmost", True)
        ctk.CTkLabel(top, text=self.get_text("preview_header").format(count=len(codes)), font=("Arial", 14, "bold")).pack(pady=10)
        txt = ctk.CTkTextbox(top); txt.pack(fill="both", expand=True, padx=10, pady=10)
        txt.insert("0.0", "\n".join(codes)); txt.configure(state="disabled")

    def run_auto_sort(self):
        src = self.entry_src_auto.get()
        dst = self.entry_dst_auto.get()
        sub = self.entry_subfolder.get().strip() or "Sorted_Result"
        codes = self.parse_codes_ultimate(self.txt_codes.get("0.0", "end"))
        
        if not src or not dst: 
            messagebox.showerror("Error", self.get_text("select_folders"))
            return
        if self._is_protected_path(dst): 
            messagebox.showerror("Error", "Destination folder is protected by system.")
            return
        if not codes: 
            messagebox.showerror("Error", self.get_text("enter_codes"))
            return

        # --- PERBAIKAN MASALAH 2: CEK KAPASITAS ASLI ---
        try:
            total_needed = 0
            for root, dirs, files in os.walk(src):
                for f in files:
                    total_needed += os.path.getsize(os.path.join(root, f))
            
            _, _, free_space = shutil.disk_usage(dst)
            if free_space < total_needed:
                messagebox.showerror("Error", f"Penyimpanan tidak cukup!\nButuh: {total_needed/1e9:.2f} GB\nTersedia: {free_space/1e9:.2f} GB")
                return
        except:
            pass 

        counts = Counter(codes)
        duplicates = [c for c, n in counts.items() if n > 1]
        self.btn_auto_start.configure(state="disabled")
        self.processing = True
        self.stop_event.clear()
        self.lbl_status_auto.configure(text=self.get_text("status_processing"))
        self.progress_bar.set(0)

        threading.Thread(target=self.auto_sort_logic, args=(src, dst, sub, codes, duplicates, self.var_auto_rename.get(), self.var_checksum.get()), daemon=True).start()

    def auto_sort_logic(self, src, dst, sub_name, codes, duplicates, do_rename, do_checksum):
        all_files = []
        files_to_delete = [] # List untuk delayed deletion
        try:
            for r, d, f in os.walk(src):
                for file in f: 
                    if self.stop_event.is_set(): break
                    all_files.append(os.path.join(r, file))
        except Exception as e:
            self.after(0, lambda: self.finish_auto_sort(f"Error scanning: {e}", True, None))
            return

        total = len(all_files)
        if total == 0: 
            self.after(0, lambda: self.finish_auto_sort(self.get_text("no_images"), False, None))
            return

        target_dir = os.path.join(dst, sub_name)
        if not os.path.exists(target_dir): 
            try: os.makedirs(target_dir)
            except Exception as e:
                self.after(0, lambda: self.finish_auto_sort(f"Cannot create output: {e}", True, None))
                return

        processed = 0; moved_count = 0; codes_found = set()
        compiled = {c: re.compile(re.escape(c.lower()), re.IGNORECASE) for c in codes if c}

        for filepath in all_files:
            if self.stop_event.is_set(): break
            filename = os.path.basename(filepath)
            ext = os.path.splitext(filename)[1].upper()
            filter_mode = self.var_auto_filter.get()
            valid = False
            
            if filter_mode == "all" and ext in EXT_ALL: valid = True
            elif filter_mode == "raw" and ext in EXT_RAW: valid = True
            
            if not valid:
                processed += 1
                continue

            match_found = False; found_code = ""
            for code, pattern in compiled.items():
                if pattern.search(filename): 
                    match_found = True
                    codes_found.add(code)
                    found_code = code
                    break
            
            if match_found:
                final = f"{found_code}_{filename}" if do_rename else filename
                dest_path = self._get_unique_path(target_dir, final)
                
                # Gunakan mode 'copy' dulu agar file sumber tidak langsung hilang
                ok, err = self.safe_copy_move(filepath, dest_path, "copy", do_checksum)
                if ok: 
                    moved_count += 1
                    # Jika aksi user adalah 'cut', masukkan ke antrean hapus
                    if self.var_auto_action.get() == "cut":
                        files_to_delete.append(filepath)
                else: 
                    self.after(0, lambda m=f"Error {filename}: {err}": self.log_message(m))
            
            processed += 1
            if processed % 50 == 0: 
                self.after(0, lambda p=processed/total: self.progress_bar.set(p))

        # --- PERBAIKAN MASALAH 4: EKSEKUSI PENGHAPUSAN DI AKHIR ---
        if not self.stop_event.is_set() and files_to_delete:
            self.after(0, lambda: self.log_message("Memulai pembersihan file sumber..."))
            for f in files_to_delete:
                try: os.remove(f)
                except: pass

        missing = list(set(codes) - codes_found)
        miss_txt = "\n".join([f"- {c}" for c in missing]) if missing else ""
        dup_txt = "\n".join([f"• {c}" for c in duplicates]) if duplicates else ""
        msg = self.get_text("report_msg").format(count=moved_count, missing=miss_txt, duplicates=self.get_text("report_dup_msg").format(duplicates=dup_txt) if duplicates else "")
        self.after(0, lambda: self.finish_auto_sort(msg, bool(missing) or bool(duplicates), target_dir))

    def finish_auto_sort(self, msg, issues, folder):
        self.btn_auto_start.configure(state="normal")
        self.processing = False
        self.lbl_status_auto.configure(text=self.get_text("status_done"))
        if issues: messagebox.showwarning(self.get_text("report_missing"), msg)
        else: messagebox.showinfo("Info", msg)
        if folder and os.path.exists(folder):
            if messagebox.askyesno("Open", "Open Output Folder?"): self.open_file_explorer(folder)

    # ==========================================
    # SMART SELECT UI (OPTIMIZED MULTIPROCESSING)
    # ==========================================
    def setup_smart_select_ui(self):
        t = self.tab_smart
        t.grid_columnconfigure(0, weight=1)

        self.frame_folders_smart = ctk.CTkFrame(t)
        self.frame_folders_smart.pack(pady=10, padx=20, fill="x")

        # Source
        ctk.CTkLabel(self.frame_folders_smart, text=self.get_text("lbl_source")).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_src_smart = ctk.CTkEntry(self.frame_folders_smart, width=400)
        self.entry_src_smart.grid(row=0, column=1, padx=10)
        if DND_AVAILABLE:
            self.entry_src_smart.drop_target_register(DND_FILES)
            self.entry_src_smart.dnd_bind('<<Drop>>', lambda e: self.drop_handler(e, self.entry_src_smart))
        ctk.CTkButton(self.frame_folders_smart, text=self.get_text("btn_browse"), width=100, 
            command=lambda: self.select_folder(self.entry_src_smart)).grid(row=0, column=2, padx=10)

        # Dest
        ctk.CTkLabel(self.frame_folders_smart, text=self.get_text("lbl_dest")).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.entry_dst_smart = ctk.CTkEntry(self.frame_folders_smart, width=400)
        self.entry_dst_smart.grid(row=1, column=1, padx=10)
        if DND_AVAILABLE:
            self.entry_dst_smart.drop_target_register(DND_FILES)
            self.entry_dst_smart.dnd_bind('<<Drop>>', lambda e: self.drop_handler(e, self.entry_dst_smart))
        ctk.CTkButton(self.frame_folders_smart, text=self.get_text("btn_browse"), width=100,
                      command=lambda: self.select_folder(self.entry_dst_smart)).grid(row=1, column=2, padx=10)

        # Config Panel
        self.frame_config_smart = ctk.CTkFrame(t)
        self.frame_config_smart.pack(pady=10, padx=20, fill="x")
        self.frame_config_smart.grid_columnconfigure(1, weight=1)

        # 1. Input Jumlah Foto (Target Count)
        ctk.CTkLabel(self.frame_config_smart, text=self.get_text("lbl_target_count")).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_smart_count = ctk.CTkEntry(self.frame_config_smart, width=100, placeholder_text="e.g 50")
        self.entry_smart_count.grid(row=0, column=1, padx=10, sticky="w")
        self.entry_smart_count.insert(0, "50")

        # 2. Input Nama Sub-folder Output
        ctk.CTkLabel(self.frame_config_smart, text=self.get_text("lbl_subfolder")).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.entry_subfolder_smart = ctk.CTkEntry(self.frame_config_smart, width=250)
        self.entry_subfolder_smart.grid(row=1, column=1, padx=10, sticky="w")
        self.entry_subfolder_smart.insert(0, "Smart_Best_Select") 
        
        # 3. Sensitivity Slider
        ctk.CTkLabel(self.frame_config_smart, text=self.get_text("lbl_sensitivity")).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.sl_sensitivity = ctk.CTkSlider(self.frame_config_smart, from_=5, to=30, number_of_steps=25)
        self.sl_sensitivity.grid(row=2, column=1, padx=10, sticky="ew")
        self.sl_sensitivity.set(12)

        # 4. Options
        opts_frame = ctk.CTkFrame(self.frame_config_smart, fg_color="transparent")
        opts_frame.grid(row=3, column=0, columnspan=2, pady=10, sticky="w")
        
        self.var_smart_action = tk.StringVar(value="copy")
        self.var_smart_filter = tk.StringVar(value="all")
        
        ctk.CTkRadioButton(opts_frame, text=self.get_text("radio_copy"), variable=self.var_smart_action, value="copy").pack(side="left", padx=10)
        ctk.CTkRadioButton(opts_frame, text=self.get_text("radio_cut"), variable=self.var_smart_action, value="cut").pack(side="left", padx=10)
        ctk.CTkLabel(opts_frame, text="|").pack(side="left", padx=10)
        ctk.CTkRadioButton(opts_frame, text=self.get_text("radio_raw_jpg"), variable=self.var_smart_filter, value="all").pack(side="left", padx=10)
        ctk.CTkRadioButton(opts_frame, text=self.get_text("radio_raw_only"), variable=self.var_smart_filter, value="raw").pack(side="left", padx=10)

        # Info
        blink_txt = "(Blink Detect ON)" if CV2_AVAILABLE else "(Install opencv-python for blink detect)"
        ctk.CTkLabel(t, text=f"{self.get_text('lbl_smart_criteria')} {blink_txt}", text_color="gray").pack()

        # Button
        self.btn_smart_start = ctk.CTkButton(t, text=self.get_text("btn_start_smart"), 
                                             fg_color=COLORS["success"], hover_color="#15803d",
                                             height=50, font=("Arial", 16, "bold"),
                                             command=self.run_smart_analysis)
        self.btn_smart_start.pack(pady=20, padx=20, fill="x")
        
        self.smart_progress = ctk.CTkProgressBar(t); self.smart_progress.set(0)
        self.smart_progress.pack(pady=5, padx=20, fill="x")
        self.lbl_status_smart = ctk.CTkLabel(t, text=self.get_text("status_ready"))
        self.lbl_status_smart.pack(pady=5)

    def run_smart_analysis(self):
        src = self.entry_src_smart.get()
        dst = self.entry_dst_smart.get()
        try: target_count = int(self.entry_smart_count.get())
        except: messagebox.showerror("Error", "Target count must be a number!"); return
        sub_name = self.entry_subfolder_smart.get().strip() or "Smart_Best_Select"

        if not src or not dst: messagebox.showerror("Error", "Please select folders."); return
        if self._is_protected_path(dst): messagebox.showerror("Error", "Destination folder is protected by system."); return

        # --- FITUR BARU: CEK CACHE AGAR TIDAK SCAN ULANG ---
        current_params = (src, target_count, int(self.sl_sensitivity.get()))
        if self.cached_smart_groups and self.cached_smart_params == current_params:
            # Jika parameter sama dengan sebelumnya, langsung buka window review tanpa loading
            if messagebox.askyesno("Smart Select", "Previous analysis result found. Open immediately without re-scanning?"):
                self.open_smart_review_window(self.cached_smart_groups, dst, sub_name)
                return
        # ---------------------------------------------------

        self.btn_smart_start.configure(state="disabled")
        self.processing = True
        self.stop_event.clear()
        self.lbl_status_smart.configure(text=self.get_text("smart_processing"))
        self.smart_progress.set(0)
        
        threading.Thread(target=self.smart_sort_logic, args=(src, dst, target_count, sub_name), daemon=True).start()
        
        # Main logic runs in a separate thread to keep UI alive, 
        # but image analysis will spawn subprocesses
        threading.Thread(target=self.smart_sort_logic, args=(src, dst, target_count, sub_name), daemon=True).start()

    def smart_sort_logic(self, src, dst, target_count, sub_name):
        # 1. LOGIKA JPG PRIORITY: Kelompokkan file agar AI hanya scan 1 perwakilan per foto
        file_map = {} 
        for root, dirs, filenames in os.walk(src):
            for f in filenames:
                if self.stop_event.is_set(): break
                ext = os.path.splitext(f)[1].lower()
                
                if ext in EXT_ALL:
                    full_path = os.path.join(root, f)
                    base = os.path.splitext(f)[0].lower()
                    key = (root, base) 
                    
                    if key not in file_map:
                        file_map[key] = {'jpg': None, 'raw': None}
                    
                    if ext in EXT_JPG:
                        file_map[key]['jpg'] = full_path
                    elif ext in EXT_RAW:
                        file_map[key]['raw'] = full_path

        # Pilih hanya 1 file perwakilan untuk di-scan oleh AI
        files_to_scan = []
        for formats in file_map.values():
            if formats['jpg']:
                # Jika ada JPG, gunakan JPG sebagai perwakilan (prioritas)
                files_to_scan.append(formats['jpg'])
            elif formats['raw']:
                # Jika tidak ada JPG, baru gunakan RAW
                files_to_scan.append(formats['raw'])
        
        total = len(files_to_scan)
        if total == 0: 
            self.after(0, lambda: self.finish_smart_sort(self.get_text("no_images"), None))
            return

        # --- BAGIAN PENTING: PROSES ANALISIS AI ---
        results = [] 
        processed = 0
        # Batasi penggunaan CPU agar aplikasi tetap responsif
        max_cpu = min(4, os.cpu_count() or 1)

        # --- PERBAIKAN KHUSUS MACOS (START) ---
        try:
            # Deteksi OS: Jika Mac (Darwin), pakai ThreadPool. Jika Windows, pakai ProcessPool.
            if platform.system() == "Darwin":
                print("Running on macOS: Using ThreadPoolExecutor (Safe Mode)")
                MyExecutor = ThreadPoolExecutor
                # ThreadPool aman berbagi memori & izin akses dengan aplikasi utama
                workers = 4 
            else:
                MyExecutor = ProcessPoolExecutor
                workers = max_cpu

            # Jalankan Executor yang sudah dipilih
            with MyExecutor(max_workers=workers) as executor:
                futures = [executor.submit(analyze_image_worker, fp) for fp in files_to_scan]
                
                for f in futures:
                    if self.stop_event.is_set(): 
                        executor.shutdown(wait=False, cancel_futures=True)
                        break
                    
                    try:
                        data = f.result()
                        if data and len(data) == 4:
                            filepath, score, dh, hist = data
                            if score > 0: 
                                results.append((filepath, score, dh, hist))
                    except Exception as err:
                        print(f"Worker Error: {err}")

        except Exception as e:
            print(f"Critical Error pada analisis AI: {e}")
        # --- PERBAIKAN KHUSUS MACOS (END) ---

        if not results:
             self.after(0, lambda: self.finish_smart_sort("Tidak ada foto yang berhasil dianalisis.", None))
             return

        # 2. PENGURUTAN BERDASARKAN SKOR KUALITAS
        results.sort(key=lambda x: x[1], reverse=True)
        
        groups = []
        assigned_paths = set()
        base_threshold = int(self.sl_sensitivity.get())

        self.after(0, lambda: self.lbl_status_smart.configure(text="Mengelompokkan foto yang mirip..."))

        # 3. LOGIKA CLUSTERING (PENGELOMPOKAN)
        for item in results:
            path, score, dhash, hist = item
            if path in assigned_paths: 
                continue
            
            current_group = {'winner': item, 'candidates': []}
            assigned_paths.add(path)
            
            for other in results:
                other_path, _, other_dhash, other_hist = other
                if other_path in assigned_paths: 
                    continue
                
                # Bandingkan kemiripan visual
                dist_shape = bin(dhash ^ other_dhash).count('1')
                dist_color = sum(abs(a - b) for a, b in zip(hist, other_hist)) if hist and other_hist else 1.0
                
                # Jika sangat mirip, masukkan ke grup yang sama
                is_similar = dist_shape < base_threshold or (dist_color < 0.4 and dist_shape < (base_threshold + 10))

                if is_similar:
                    current_group['candidates'].append(other)
                    assigned_paths.add(other_path)
                    
            groups.append(current_group)
        
        # Urutkan grup berdasarkan skor pemenang terbaik
        groups.sort(key=lambda g: g['winner'][1], reverse=True)
        final_groups = groups[:target_count]
        
        # Simpan ke cache
        self.cached_smart_groups = final_groups
        self.cached_smart_params = (src, target_count, int(self.sl_sensitivity.get()))
        
        # Buka Jendela Review
        self.after(0, lambda: self.open_smart_review_window(final_groups, dst, sub_name))
    def open_smart_review_window(self, groups, dst, sub_name):
        # 1. CEK KEAMANAN (GATEKEEPER)
        if self.smart_window is not None:
            # Jika sedang loading atau sudah ada window, angkat window itu ke depan
            if self.smart_window != "LOADING":
                try:
                    if self.smart_window.winfo_exists():
                        self.smart_window.lift()
                        self.smart_window.attributes("-topmost", True)
                        return
                except:
                    pass
            else:
                # Jika status masih "LOADING", berarti window sedang dibuat. Abaikan perintah ini.
                return

        # 2. BOOKING DULU (PENTING!)
        # Kita isi variabel dengan string sementara agar perintah berikutnya langsung ditolak
        self.smart_window = "LOADING"

        try:
            # 3. BARU BUAT JENDELA ASLINYA
            # Kita kirim 'self' sebagai parent
            real_window = SmartReviewWindow(self, groups, 
                lambda final: threading.Thread(target=self.execute_smart_move, args=(final, dst, sub_name), daemon=True).start())
            
            # 4. SETELAH JADI, SIMPAN KE VARIABEL
            self.smart_window = real_window
            
        except Exception as e:
            print(f"Gagal membuka window: {e}")
            self.smart_window = None # Reset jika gagal agar bisa dicoba lagi

    def execute_smart_move(self, unique_picks, dst, sub_name):
        output_folder = os.path.join(dst, sub_name)
        if not os.path.exists(output_folder): os.makedirs(output_folder)
        action = self.var_smart_action.get()
        filter_mode = self.var_smart_filter.get()
        moved_count = 0
        processed_basenames = set()
        
        self.after(0, lambda: self.lbl_status_smart.configure(text="Moving Selected Photos..."))

        # --- FIX: Iterasi melalui list of dictionaries ---
        for group in unique_picks:
            # Mengambil data pemenang (winner) dari setiap grup
            file_info = group.get('winner')
            if not file_info: continue
            
            src_path = file_info[0] # Path file
            filename = os.path.basename(src_path)
            base = os.path.splitext(filename)[0].lower()
            if base in processed_basenames: continue

            src_dir = os.path.dirname(src_path)
            files_to_move = []
            found_raw = None
            found_jpg = None
            
            # Deteksi pasangan RAW/JPG
            ext = os.path.splitext(filename)[1].lower()
            if ext in EXT_JPG:
                found_jpg = src_path
                for rext in EXT_RAW:
                    for p in [os.path.join(src_dir, os.path.splitext(filename)[0] + rext),
                              os.path.join(src_dir, os.path.splitext(filename)[0] + rext.upper()),
                              os.path.join(src_dir, os.path.splitext(filename)[0] + rext.lower())]:
                        if os.path.exists(p): 
                            found_raw = p
                            break
                    if found_raw: break
            elif ext in EXT_RAW:
                found_raw = src_path
                for jext in EXT_JPG:
                    for p in [os.path.join(src_dir, os.path.splitext(filename)[0] + jext),
                              os.path.join(src_dir, os.path.splitext(filename)[0] + jext.upper()),
                              os.path.join(src_dir, os.path.splitext(filename)[0] + jext.lower())]:
                        if os.path.exists(p): 
                            found_jpg = p
                            break
                    if found_jpg: break

            # Filter mode
            if filter_mode == "all":
                if found_raw: files_to_move.append(found_raw)
                if found_jpg: files_to_move.append(found_jpg)
            elif filter_mode == "raw":
                if found_raw: files_to_move.append(found_raw)

            # Eksekusi pindah/copy
            for f_path in files_to_move:
                dest = self._get_unique_path(output_folder, os.path.basename(f_path))
                self.safe_copy_move(f_path, dest, action, use_checksum=False)
            
            if files_to_move: moved_count += 1
            processed_basenames.add(base)
            
        msg = self.get_text("smart_done").format(count=moved_count)
        self.after(0, lambda: self.finish_smart_sort(msg, output_folder))

    def finish_smart_sort(self, msg, output_folder=None):
        self.btn_smart_start.configure(state="normal")
        self.processing = False
        self.lbl_status_smart.configure(text=self.get_text("status_done"))
        messagebox.showinfo(self.get_text("title"), msg)
        if output_folder and os.path.exists(output_folder): self.open_file_explorer(output_folder)

    # ==========================================
    # MANUAL SORT UI
    # ==========================================
    def setup_manual_sort_ui(self):
        t = self.tab_manual
        t.grid_rowconfigure(1, weight=1); t.grid_columnconfigure(0, weight=3); t.grid_columnconfigure(1, weight=1) 

        # Top
        self.frame_top_manual = ctk.CTkFrame(t, fg_color="transparent")
        self.frame_top_manual.grid(row=0, column=0, columnspan=2, sticky="ew", pady=5)
        ctk.CTkLabel(self.frame_top_manual, text=self.get_text("lbl_source")).pack(side="left", padx=5)
        self.entry_src_man = ctk.CTkEntry(self.frame_top_manual, width=200); self.entry_src_man.pack(side="left", padx=5)
        if DND_AVAILABLE: self.entry_src_man.drop_target_register(DND_FILES); self.entry_src_man.dnd_bind('<<Drop>>', lambda e: self.drop_handler(e, self.entry_src_man))
        ctk.CTkButton(self.frame_top_manual, text="...", width=40, command=lambda: self.select_folder(self.entry_src_man)).pack(side="left", padx=5)
        self.btn_load_manual = ctk.CTkButton(self.frame_top_manual, text="Load", width=60, fg_color=COLORS["accent"], command=self.load_manual_folder); self.btn_load_manual.pack(side="left", padx=5)
        
        ctk.CTkLabel(self.frame_top_manual, text="| " + self.get_text("lbl_dest")).pack(side="left", padx=5)
        self.entry_dst_man = ctk.CTkEntry(self.frame_top_manual, width=200); self.entry_dst_man.pack(side="left", padx=5)
        if DND_AVAILABLE: self.entry_dst_man.drop_target_register(DND_FILES); self.entry_dst_man.dnd_bind('<<Drop>>', lambda e: self.drop_handler(e, self.entry_dst_man))
        ctk.CTkButton(self.frame_top_manual, text="...", width=40, command=lambda: self.select_folder(self.entry_dst_man)).pack(side="left", padx=5)

        # Preview
        self.frame_preview = ctk.CTkFrame(t, fg_color="black"); self.frame_preview.grid(row=1, column=0, sticky="nsew", padx=10, pady=10); self.frame_preview.grid_propagate(False) 
        self.canvas_preview = tk.Canvas(self.frame_preview, bg="black", highlightthickness=0); self.canvas_preview.pack(fill="both", expand=True)
        self.lbl_zoom_instruct = ctk.CTkLabel(self.frame_preview, text=self.get_text("note_preview"), font=("Arial", 11), text_color="gray"); self.lbl_zoom_instruct.pack(side="bottom", fill="x", pady=2)
        
        self.frame_filmstrip = ctk.CTkScrollableFrame(self.frame_preview, height=100, orientation="horizontal", fg_color=COLORS["bg"]); self.frame_filmstrip.pack(side="bottom", fill="x", pady=5)
        self.filmstrip_widgets = []
        
        self.canvas_preview.bind("<MouseWheel>", self.on_mouse_wheel); self.canvas_preview.bind("<ButtonPress-1>", self.on_pan_start_or_click); self.canvas_preview.bind("<B1-Motion>", self.on_pan_move)
        
        status_frame = ctk.CTkFrame(t, fg_color="transparent"); status_frame.grid(row=2, column=0, sticky="ew", pady=5)
        self.lbl_manual_status = ctk.CTkLabel(status_frame, text="", font=("Arial", 14, "bold")); self.lbl_manual_status.pack(side="left", padx=10)
        self.lbl_remaining_count = ctk.CTkLabel(status_frame, text="", font=("Arial", 12, "bold"), text_color=COLORS["warning"]); self.lbl_remaining_count.pack(side="right", padx=10)

        # Controls
        frame_ctrl = ctk.CTkFrame(t); frame_ctrl.grid(row=1, column=1, rowspan=2, sticky="nsew", padx=10, pady=10); frame_ctrl.grid_columnconfigure(0, weight=1)
        
        frame_config = ctk.CTkFrame(frame_ctrl, fg_color="transparent"); frame_config.pack(fill="x", pady=10)
        ctk.CTkLabel(frame_config, text=self.get_text("lbl_sort_type")).pack(anchor="w", padx=10)
        self.var_sort_type = ctk.StringVar(value="RAW + JPG")
        ctk.CTkOptionMenu(frame_config, variable=self.var_sort_type, values=["RAW Only", "RAW + JPG"]).pack(fill="x", padx=10, pady=(0, 10))

        self.frame_man_action = ctk.CTkFrame(frame_ctrl, fg_color="transparent"); self.frame_man_action.pack(fill="x", pady=10)
        ctk.CTkLabel(self.frame_man_action, text="Action, Rotate & Zoom").pack(anchor="w", padx=10)
        sub_act = ctk.CTkFrame(self.frame_man_action, fg_color="transparent"); sub_act.pack(fill="x", padx=10)
        self.var_man_action = tk.StringVar(value="copy")
        ctk.CTkRadioButton(sub_act, text="Copy", variable=self.var_man_action, value="copy").pack(side="left", padx=5)
        ctk.CTkRadioButton(sub_act, text="Cut", variable=self.var_man_action, value="cut").pack(side="left", padx=5)
        ctk.CTkButton(sub_act, text="⟳", width=30, command=lambda: self.rotate_image(-90)).pack(side="right", padx=2)
        ctk.CTkButton(sub_act, text="⟲", width=30, command=lambda: self.rotate_image(90)).pack(side="right", padx=2)
        ctk.CTkButton(sub_act, text="🔍 1:1", width=40, command=self.reset_zoom, fg_color=COLORS["secondary"]).pack(side="right", padx=5)

        self.btn_set_hotkey_man = ctk.CTkButton(frame_ctrl, text=self.get_text("btn_set_hotkey"), command=self.open_hotkey_dialog, height=25); self.btn_set_hotkey_man.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(frame_ctrl, text="Categorize (Press Key)").pack(pady=(20, 5))
        self.frame_cats_dynamic = ctk.CTkFrame(frame_ctrl, fg_color="transparent"); self.frame_cats_dynamic.pack(fill="x", padx=5)
        self.render_category_buttons()

        self.btn_undo = ctk.CTkButton(frame_ctrl, text=self.get_text("btn_undo"), fg_color=COLORS["secondary"], hover_color="#555", command=self.undo_decision, height=30); self.btn_undo.pack(fill="x", padx=10, pady=10)
        
        frame_nav = ctk.CTkFrame(frame_ctrl, fg_color="transparent"); frame_nav.pack(pady=10, fill="x")
        self.btn_nav_prev = ctk.CTkButton(frame_nav, text="< Prev", command=lambda: self.nav_image(-1)); self.btn_nav_prev.pack(side="left", expand=True, fill="x", padx=5)
        self.btn_nav_next = ctk.CTkButton(frame_nav, text="Next >", command=lambda: self.nav_image(1)); self.btn_nav_next.pack(side="right", expand=True, fill="x", padx=5)
        
        ctk.CTkLabel(frame_ctrl, text="Progress").pack(anchor="w", padx=10)
        self.manual_progress = ctk.CTkProgressBar(frame_ctrl); self.manual_progress.set(0); self.manual_progress.pack(fill="x", padx=10, pady=(0, 20))
        self.btn_execute_man = ctk.CTkButton(frame_ctrl, text=self.get_text("btn_start_manual"), fg_color=COLORS["accent"], height=40, command=self.execute_manual_sort); self.btn_execute_man.pack(side="bottom", fill="x", padx=10, pady=20)
        self.bind_hotkeys(); self.frame_preview.bind("<Configure>", self.on_frame_configure)

    def render_category_buttons(self):
        for widget in self.frame_cats_dynamic.winfo_children(): widget.destroy()
        for cat in self.categories:
            btn = ctk.CTkButton(self.frame_cats_dynamic, text=f"{cat['name']}\n({cat['hotkey'].upper()})", fg_color=cat["color"], hover_color=cat["color"], width=60, command=lambda c=cat["slug"]: self.mark_file(c))
            btn.pack(side="left", expand=True, fill="x", padx=2)

    def on_frame_configure(self, event):
        if self.current_pil_image:
            if hasattr(self, '_resize_timer') and self._resize_timer: self.after_cancel(self._resize_timer)
            self._resize_timer = self.after(100, self.redraw_canvas)

    def open_hotkey_dialog(self): HotkeyDialog(self, self.categories, self.update_hotkeys)
    def update_hotkeys(self, new_categories):
        self.categories = new_categories; self.config["categories"] = new_categories; self.config_mgr.save_config(); self.render_category_buttons(); self.bind_hotkeys()
    
    def bind_hotkeys(self):
        self.unbind_all("<Key>")
        self.bind("<Right>", lambda e: self.nav_image(1))
        self.bind("<Left>", lambda e: self.nav_image(-1))
        for cat in self.categories: 
            self.bind(cat["hotkey"], lambda e, c=cat["slug"]: self.mark_file(c))
        self.bind("r", lambda e: self.rotate_image(90))
        self.bind("R", lambda e: self.rotate_image(-90))
        self.bind("<Control-z>", lambda e: self.undo_decision())
        self.bind("z", lambda e: self.undo_decision())

    def load_manual_folder(self):
        folder = self.entry_src_man.get()
        if not os.path.exists(folder): messagebox.showerror("Error", "Invalid Source Folder"); return
        all_files = sorted(os.listdir(folder)); jpg_files = []; raw_files = []
        for f in all_files:
            ext = os.path.splitext(f)[1].lower() 
            if ext in EXT_JPG: jpg_files.append(f)
            elif ext in EXT_RAW: raw_files.append(f)
        if jpg_files: self.manual_files = jpg_files; self.preview_mode = "JPG"
        elif raw_files: self.manual_files = raw_files; self.preview_mode = "RAW"
        else: self.manual_files = []
        if not self.manual_files: messagebox.showinfo(self.get_text("title"), self.get_text("no_images")); return
        self.manual_index = 0; self.manual_decisions = {}; self.undo_stack = []; self.rotation_angle = 0; self.image_cache.clear(); self.manual_progress.set(0); self.show_image()
        # Ensure focus is set to capture keys
        self.focus_set()

    def _load_image_data(self, filepath, filename, thumb_only=False):
        # 1. Cek Cache dengan Lock
        with self.cache_lock:
            if thumb_only and filepath in self.thumbnail_cache:
                # Berikan salinan (copy) agar thread-safe
                return self.thumbnail_cache[filepath].copy()

        try:
            img = None
            ext = os.path.splitext(filepath)[1].lower()
            
            # --- JPG PRIORITY LOGIC ---
            actual_load_path = filepath
            if ext in EXT_RAW:
                base_path = os.path.splitext(filepath)[0]
                for j_ext in ['.jpg', '.JPG', '.jpeg', '.JPEG']:
                    potential_jpg = base_path + j_ext
                    if os.path.exists(potential_jpg):
                        actual_load_path = potential_jpg
                        ext = j_ext.lower()
                        break

            # 2. Pemuatan Gambar
            if ext in EXT_RAW and RAWPY_AVAILABLE:
                with rawpy.imread(actual_load_path) as raw:
                    try:
                        thumb = raw.extract_thumb()
                        if thumb.format == rawpy.ThumbFormat.JPEG: 
                            img = Image.open(io.BytesIO(thumb.data))
                        else: 
                            img = Image.fromarray(raw.postprocess(use_camera_wb=False, half_size=True, no_auto_bright=True))
                    except: 
                        img = Image.fromarray(raw.postprocess(use_camera_wb=False, half_size=True, no_auto_bright=True))
            else:
                img = Image.open(actual_load_path)
            
            if img:
                img = ImageOps.exif_transpose(img)
                
                # --- PERBAIKAN KRUSIAL: PAKSA MASUK RAM ---
                img.load() 
                
                if thumb_only:
                    img.thumbnail((150, 150), Image.Resampling.LANCZOS)
                    with self.cache_lock:
                        self.thumbnail_cache[filepath] = img.copy() # Simpan salinan di cache
                
            return img
        except Exception as e:
            print(f"Gagal load display {filename}: {e}")
            return None

    def preload_images(self, center_idx, src_dir):
        indices_to_load = range(max(0, center_idx - 2), min(len(self.manual_files), center_idx + 6))
        for idx in indices_to_load:
            if idx not in self.image_cache:
                self.executor.submit(self._cache_worker, idx, os.path.join(src_dir, self.manual_files[idx]), self.manual_files[idx])
        if len(self.image_cache) > self.cache_size: 
            try:
                self.image_cache.popitem(last=False)
            except:
                pass
    
    def _cache_worker(self, idx, filepath, filename):
        img = self._load_image_data(filepath, filename)
        if img: self.image_cache[idx] = img

    def show_image(self):
        self.zoom_scale = 1.0; self.pan_x = 0; self.pan_y = 0
        if not self.manual_files: return
        filename = self.manual_files[self.manual_index]; src_dir = self.entry_src_man.get()
        if self.manual_index in self.image_cache: self.current_pil_image = self.image_cache[self.manual_index]
        else: self.current_pil_image = self._load_image_data(os.path.join(src_dir, filename), filename); self.image_cache[self.manual_index] = self.current_pil_image
        self.preload_images(self.manual_index, src_dir); self.update_filmstrip(); self.redraw_canvas()
        status = self.manual_decisions.get(filename, "Unsorted")
        col = {c["slug"]: c["color"] for c in self.categories}.get(status, "white")
        self.lbl_manual_status.configure(text=f"{filename} [{self.manual_index+1}/{len(self.manual_files)}] : {status.upper()}", text_color=col)
        self.update_manual_progress()

    def update_filmstrip(self):
        for w in self.filmstrip_widgets: w.destroy()
        self.filmstrip_widgets.clear()
        start = max(0, self.manual_index - 3); end = min(len(self.manual_files), self.manual_index + 4)
        for idx in range(start, end):
            f_name = self.manual_files[idx]
            f_frame = ctk.CTkFrame(self.frame_filmstrip, width=80, height=80, fg_color=COLORS["accent"] if idx == self.manual_index else "transparent", border_width=1 if idx == self.manual_index else 0)
            f_frame.pack(side="left", padx=2)
            ctk.CTkLabel(f_frame, text=f"{idx+1}", font=("Arial", 10)).place(relx=0.5, rely=0.5, anchor="center")
            status = self.manual_decisions.get(f_name, None)
            if status:
                col = {c["slug"]: c["color"] for c in self.categories}.get(status, "gray")
                ctk.CTkLabel(f_frame, text="●", text_color=col, font=("Arial", 20)).place(relx=0.8, rely=0.8, anchor="center")
            self.filmstrip_widgets.append(f_frame)

    def redraw_canvas(self):
        if not self.current_pil_image: return
        img = self.current_pil_image
        if img is None: return
        if self.rotation_angle != 0: img = img.rotate(self.rotation_angle, expand=True)
        cw = self.canvas_preview.winfo_width(); ch = self.canvas_preview.winfo_height()
        if cw < 50 or ch < 50: return
        iw, ih = img.size; self.fit_scale = min(cw/iw, ch/ih)
        final_scale = self.fit_scale * self.zoom_scale
        new_w, new_h = int(iw * final_scale), int(ih * final_scale)
        if new_w < 1 or new_h < 1: return
        resized_img = img.resize((new_w, new_h), Image.Resampling.NEAREST)
        self.tk_image = ImageTk.PhotoImage(resized_img)
        self.canvas_preview.delete("all")
        self.canvas_preview.create_image((cw//2)+self.pan_x, (ch//2)+self.pan_y, image=self.tk_image, anchor="center")

    def on_mouse_wheel(self, event):
        if not self.current_pil_image: return
        if event.delta > 0: self.zoom_scale *= 1.1
        else: self.zoom_scale /= 1.1; self.zoom_scale = max(0.1, self.zoom_scale)
        self.redraw_canvas()

    def on_pan_start_or_click(self, event):
        self.canvas_preview.scan_mark(event.x, event.y); self._drag_data["x"] = event.x; self._drag_data["y"] = event.y
        if hasattr(self, 'fit_scale'):
            if abs(self.zoom_scale - 1.0) < 0.1:
                target_scale = 1.0 / self.fit_scale
                cw = self.canvas_preview.winfo_width(); ch = self.canvas_preview.winfo_height()
                self.pan_x = -(event.x - cw//2) * (target_scale - 1); self.pan_y = -(event.y - ch//2) * (target_scale - 1)
                self.zoom_scale = target_scale
            else: self.zoom_scale = 1.0; self.pan_x = 0; self.pan_y = 0
            self.redraw_canvas()

    def on_pan_move(self, event):
        dx = event.x - self._drag_data["x"]; dy = event.y - self._drag_data["y"]
        if abs(dx) > 2 or abs(dy) > 2:
            self.pan_x += dx; self.pan_y += dy; self._drag_data["x"] = event.x; self._drag_data["y"] = event.y
            self.redraw_canvas()

    def reset_zoom(self): self.zoom_scale = 1.0; self.pan_x = 0; self.pan_y = 0; self.redraw_canvas()
    def rotate_image(self, angle): self.rotation_angle = (self.rotation_angle + angle) % 360; self.redraw_canvas()
    def nav_image(self, direction):
        new_idx = self.manual_index + direction
        if 0 <= new_idx < len(self.manual_files): self.manual_index = new_idx; self.rotation_angle = 0; self.show_image()

    def mark_file(self, category_slug):
        if not self.manual_files: return
        fname = self.manual_files[self.manual_index]
        self.undo_stack.append({"index": self.manual_index, "filename": fname, "prev": self.manual_decisions.get(fname, None)})
        self.manual_decisions[fname] = category_slug; self.nav_image(1)

    def undo_decision(self):
        if not self.undo_stack: 
            if self.manual_index > 0: self.nav_image(-1)
            return
        last = self.undo_stack.pop(); self.manual_index = last["index"]
        if last["prev"] is None: 
            if last["filename"] in self.manual_decisions: del self.manual_decisions[last["filename"]]
        else: self.manual_decisions[last["filename"]] = last["prev"]
        self.show_image()

    def update_manual_progress(self):
        if not self.manual_files: self.manual_progress.set(0); return
        count = len(self.manual_decisions); total = len(self.manual_files)
        self.manual_progress.set(count / total)
        self.lbl_remaining_count.configure(text=self.get_text("lbl_remaining").format(count=total - count))

    def execute_manual_sort(self):
        src = self.entry_src_man.get(); dst = self.entry_dst_man.get()
        if not dst or not os.path.exists(dst): messagebox.showerror("Error", "Invalid Dest"); return
        if self._is_protected_path(dst): messagebox.showerror("Error", "Destination folder is protected by system."); return
        if not self.manual_decisions: messagebox.showinfo("Info", "Nothing sorted"); return
        self.btn_execute_man.configure(state="disabled", text="PROCESSING...")
        self.processing = True
        self.manual_progress.set(0)
        threading.Thread(target=self.manual_sort_logic, args=(src, dst), daemon=True).start()

    def manual_sort_logic(self, src_dir, dest_root):
        files_to_delete_man = []
        sort_mode = self.var_sort_type.get() 
        action = self.var_man_action.get()
        moved = 0
        
        slugs = {c["slug"]: c["name"] for c in self.categories}
        # Hanya ambil file yang sudah dikategorikan [cite: 312]
        keys = [k for k, v in self.manual_decisions.items() if v in slugs]
        total = len(keys)
        
        for i, fname in enumerate(keys):
            if self.stop_event.is_set(): break
            slug = self.manual_decisions[fname]
            folder = os.path.join(dest_root, slugs.get(slug, "Unsorted"))
            if not os.path.exists(folder): os.makedirs(folder, exist_ok=True)

            # PERBAIKAN: Gunakan set agar tidak ada path ganda
            to_process = set()
            base = os.path.splitext(fname)[0]
            
            if sort_mode == "RAW + JPG":
                # Tambahkan JPG jika ada
                jpg_path = os.path.join(src_dir, fname)
                if os.path.exists(jpg_path): to_process.add(jpg_path)
                
                # Tambahkan RAW jika ada
                for ext in EXT_RAW:
                    p = os.path.join(src_dir, base + ext)
                    if os.path.exists(p): 
                        to_process.add(p)
                        break
            else: # RAW Only
                for ext in EXT_RAW:
                    p = os.path.join(src_dir, base + ext)
                    if os.path.exists(p):
                        to_process.add(p)
                        break

            # Eksekusi pemindahan tunggal
            for f_path in to_process:
                dest = self._get_unique_path(folder, os.path.basename(f_path))
                ok, err = self.safe_copy_move(f_path, dest, "copy", use_checksum=True)
                if ok:
                    moved += 1
                    if action == "cut": files_to_delete_man.append(f_path)
            
            self.after(0, lambda p=(i+1)/total: self.manual_progress.set(p))
            
        if action == "cut" and not self.stop_event.is_set():
            for f_del in files_to_delete_man:
                try: os.remove(f_del)
                except: pass

        self.after(0, lambda: self.finish_manual_sort(moved, None, dest_root))

    def finish_manual_sort(self, count, err, folder):
        self.processing = False
        self.manual_files = []; self.manual_decisions = {}; self.manual_progress.set(0)
        self.canvas_preview.delete("all"); self.btn_execute_man.configure(state="normal", text=self.get_text("btn_start_manual"))
        if err: messagebox.showerror("Error", str(err))
        else: 
            messagebox.showinfo("Done", f"Sorted {count} files.")
            if folder: self.open_file_explorer(folder)

    def start_guided_tour(self):
        if self.current_overlay: return
        self.tutorial_step = 0
        self._show_tutorial_step()
    
    def _finish_tutorial(self):
        self.tutorial_step = 0
        if self.current_overlay: self.current_overlay._cleanup(); self.current_overlay = None
    
    def _show_tutorial_step(self):
        if self.tutorial_step >= len(TUTORIAL_STEPS_BASE): 
            self._finish_tutorial()
            return
            
        tab_name, widget_name, text_key, position = TUTORIAL_STEPS_BASE[self.tutorial_step]
        
        # Ganti Tab jika perlu
        if tab_name:
            localized_tab_name = self.get_text(tab_name)
            if self.tabview.get() != localized_tab_name:
                self.tabview.set(localized_tab_name)
                # Tunggu sebentar agar UI render tab baru sebelum highlight widget
                self.after(300, lambda: self._create_overlay_safe(widget_name, text_key))
            else:
                self._create_overlay_safe(widget_name, text_key)
        else:
            self._create_overlay_safe(widget_name, text_key)

    def _create_overlay_safe(self, widget_name, text_key):
        text = TUTORIAL_LOCALIZED.get(self.lang_code, TUTORIAL_LOCALIZED["English"]).get(text_key, text_key)
        widget = None
        if widget_name:
            try: widget = getattr(self, widget_name)
            except: pass
            
        if self.current_overlay: self.current_overlay._cleanup()
        if widget: widget.update_idletasks()
        
        self.current_overlay = TutorialOverlay(self, text, self._next_tutorial_step, self._prev_tutorial_step, self._finish_tutorial, widget, self.tutorial_step == 0)

    def _next_tutorial_step(self): self.tutorial_step += 1; self._show_tutorial_step()
    def _prev_tutorial_step(self): 
        if self.tutorial_step > 0: self.tutorial_step -= 1; self._show_tutorial_step()

if __name__ == "__main__":
    multiprocessing.freeze_support() # Required for Windows EXE to support Multiprocessing
    app = PhotoSortApp()
    app.mainloop()