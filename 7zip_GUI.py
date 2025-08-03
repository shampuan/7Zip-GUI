#!/usr/bin/env python3

import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QLineEdit, QPushButton, QComboBox,
    QCheckBox, QSpinBox, QFileDialog, QGroupBox,
    QMessageBox, QListWidget, QListWidgetItem,
    QDialog, QProgressBar, QTextEdit, QSpacerItem, QSizePolicy
)
from PyQt5.QtGui import QPixmap, QIcon, QMovie
from PyQt5.QtCore import Qt, QUrl, pyqtSignal, QThread, QSize
import subprocess
import shlex

# --- Dil Betikleri ---
LANGUAGES = {
    "tr": {
        "window_title": "7Zip GUI",
        "about_title": "Hakkında",
        "about_text": "7-Zip Arşivleme Arayüzü\n\nVersiyon: 0.1\nGeliştirici: A. Serhat KILIÇOĞLU \ngithub.com/shampuan \n7zip geliştirici: Igor Pavlov \nLisans: MIT Lisansı",
        "source_group_title": "Kaynak Dosyalar/Klasörler",
        "add_files_button": "Dosya Ekle...",
        "add_folder_button": "Klasör Ekle...",
        "remove_selected_button": "Seçileni Kaldır",
        "target_group_title": "Hedef",
        "archive_label": "Arşiv:",
        "browse_button": "Gözat...",
        "archive_format_label": "Arşiv Biçimi:",
        "compression_group_title": "Sıkıştırma Ayarları",
        "compression_level_label": "Sıkıştırma Seviyesi:",
        "level_store": "Depola (Sıkıştırma yok)",
        "level_fastest": "En Hızlı",
        "level_fast": "Hızlı",
        "level_normal": "Normal",
        "level_maximum": "Maksimum",
        "level_ultra": "Ultra",
        "compression_method_label": "Sıkıştırma Yöntemi:",
        "dictionary_size_label": "Sözlük Boyutu:",
        "threads_label": "CPU İş Parçacıkları:",
        "options_group_title": "Arşivleme Seçenekleri",
        "update_mode_label": "Güncelleme Modu:",
        "update_add_replace": "Dosya Ekle ve Güncelle",
        "update_only_update": "Yalnızca Güncelle",
        "update_synchronize": "Senkronize Et",
        "update_add_no_replace": "Dosya Ekle (mevcut olanları değiştirme)",
        "password_label": "Şifre:",
        "password_repeat_label": "Şifre Tekrar:",
        "encrypt_filenames_checkbox": "Dosya Adlarını Şifrele",
        "show_password_checkbox": "Şifreyi Göster",
        "solid_block_checkbox": "Katı Blok Arşivleme",
        "split_volumes_checkbox": "Bölümlere Ayır",
        "split_placeholder": "Boyut Seçin veya Girin",
        "ok_button": "Arşivle",
        "cancel_button": "İptal",
        "about_button": "Hakkında",
        "language_button": "Dil (TR/EN)",
        "password_mismatch_title": "Şifre Hatası",
        "password_mismatch_message": "Girilen şifreler uyuşmuyor!",
        "options_summary_title": "Seçenekler Özeti",
        "summary_source_files": "--- Kaynak Dosyalar/Klasörler ---",
        "summary_selected_items": "Seçilen Ögeler:",
        "summary_archive_settings": "--- Arşiv Ayarları ---",
        "summary_archive_path": "Arşiv Yolu:",
        "summary_archive_format": "Arşiv Biçimi:",
        "summary_compression_settings": "--- Sıkıştırma Ayarları ---",
        "summary_compression_level": "Sıkıştırma Seviyesi:",
        "summary_compression_method": "Sıkıştırma Yöntemi:",
        "summary_dictionary_size": "Sözlük Boyutu:",
        "summary_cpu_threads": "CPU İş Parçacıkları:",
        "summary_archive_options": "--- Arşivleme Seçenekleri ---",
        "summary_update_mode": "Güncelleme Modu:",
        "summary_password_set": "Şifre Belirleme:",
        "summary_encrypt_filenames": "Dosya Adlarını Şifrele:",
        "summary_solid_block": "Katı Blok Arşivleme:",
        "summary_split_volumes": "Bölümlere Ayır:",
        "summary_split_size": "Bölme Boyutu:",
        "summary_none": "Yok",
        "summary_start_compression": "Bu ayarlarla sıkıştırma işlemi başlatılacak.",
        "no_source_selected": "Hiçbir dosya veya klasör seçilmedi.",
        "compression_command_success_title": "Arşivleme Başarılı",
        "compression_command_success_message": "Arşiv başarıyla oluşturuldu!",
        "compression_command_error_title": "Arşivleme Hatası",
        "compression_command_error_message": "Arşivleme işlemi sırasında hata oluştu:",
        "command_not_found_message": "7z komutu bulunamadı. Lütfen p7zip-full paketinin kurulu olduğundan ve 7z'nin PATH'inizde olduğundan emin olun.",
        "progress_dialog_title": "Arşivleme İlerlemesi",
        "progress_label_text_initial": "Arşivleme sürüyor...",
        "progress_status_label": "Durum:",
        "cancel_compression_button": "İptal Et",
        "default_archive_basename": "yeni_arsiv" 
    },
    "en": {
        "window_title": "7Zip GUI",
        "about_title": "About",
        "about_text": "7-Zip Like Archiving Interface\n\nVersion: 0.1\nDeveloper: A. Serhat KILIÇOĞLU \ngithub.com/shampuan \n7zip maintainer: Igor Pavlov \nLicense: MIT License",
        "source_group_title": "Source Files/Folders",
        "add_files_button": "Add Files...",
        "add_folder_button": "Add Folder...",
        "remove_selected_button": "Remove Selected",
        "target_group_title": "Target",
        "archive_label": "Archive:",
        "browse_button": "Browse...",
        "archive_format_label": "Archive Format:",
        "compression_group_title": "Compression Settings",
        "compression_level_label": "Compression Level:",
        "level_store": "Store (No compression)",
        "level_fastest": "Fastest",
        "level_fast": "Fast",
        "level_normal": "Normal",
        "level_maximum": "Maximum",
        "level_ultra": "Ultra",
        "compression_method_label": "Compression Method:",
        "dictionary_size_label": "Dictionary Size:",
        "threads_label": "CPU Threads:",
        "options_group_title": "Archiving Options",
        "update_mode_label": "Update Mode:",
        "update_add_replace": "Add and replace files",
        "update_only_update": "Update existing files",
        "update_synchronize": "Synchronize",
        "update_add_no_replace": "Add files (do not replace existing)",
        "password_label": "Password:",
        "password_repeat_label": "Repeat Password:",
        "encrypt_filenames_checkbox": "Encrypt File Names",
        "show_password_checkbox": "Show Password",
        "solid_block_checkbox": "Solid Block Archiving",
        "split_volumes_checkbox": "Split to Volumes",
        "split_placeholder": "Select or Enter Size",
        "ok_button": "Archive",
        "cancel_button": "Cancel",
        "about_button": "About",
        "language_button": "Language (EN/TR)",
        "password_mismatch_title": "Password Mismatch",
        "password_mismatch_message": "Passwords do not match!",
        "options_summary_title": "Options Summary",
        "summary_source_files": "--- Source Files/Folders ---",
        "summary_selected_items": "Selected Items:",
        "summary_archive_settings": "--- Archive Settings ---",
        "summary_archive_path": "Archive Path:",
        "summary_archive_format": "Archive Format:",
        "summary_compression_settings": "--- Compression Settings ---",
        "summary_compression_level": "Compression Level:",
        "summary_compression_method": "Compression Method:",
        "summary_dictionary_size": "Dictionary Size:",
        "summary_cpu_threads": "CPU Threads:",
        "summary_archive_options": "--- Archiving Options ---",
        "summary_update_mode": "Update Mode:",
        "summary_password_set": "Password Set:",
        "summary_encrypt_filenames": "Encrypt File Names:",
        "summary_solid_block": "Solid Block Archiving:",
        "summary_split_volumes": "Split to Volumes:",
        "summary_split_size": "Split Size:",
        "summary_none": "None",
        "summary_start_compression": "Compression will start with these settings.",
        "no_source_selected": "No files or folders selected.",
        "compression_command_success_title": "Archiving Successful",
        "compression_command_success_message": "Archive created successfully!",
        "compression_command_error_title": "Archiving Error",
        "compression_command_error_message": "An error occurred during archiving:",
        "command_not_found_message": "7z command not found. Please ensure p7zip-full is installed and 7z is in your PATH.",
        "progress_dialog_title": "Archiving Progress",
        "progress_label_text_initial": "Archiving in progress...",
        "progress_status_label": "Status:",
        "cancel_compression_button": "Cancel",
        "default_archive_basename": "new_archive" 
    }
}

class DroppableListWidget(QListWidget):
    """
    Sürükle-bırak olaylarını işleyebilen özel QListWidget.
    """
    new_paths_dropped = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setDragDropMode(QListWidget.InternalMove)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            dropped_paths = []
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                if os.path.isdir(file_path) or os.path.isfile(file_path):
                    dropped_paths.append(file_path)
            self.new_paths_dropped.emit(dropped_paths)
            event.acceptProposedAction()
        else:
            event.ignore()

class SevenZipWorker(QThread):
    """
    7-Zip sıkıştırma işlemini ayrı bir iş parçacığında yürütmek için QThread.
    """
    progress_update = pyqtSignal(str) # Durum mesajları için
    finished = pyqtSignal(str)        # Başarılı tamamlama için
    error = pyqtSignal(str)           # Hata için
    command_not_found = pyqtSignal(str) # Komut bulunamadı hatası için

    def __init__(self, command_parts, parent=None):
        super().__init__(parent)
        self.command_parts = command_parts
        self._is_canceled = False

    def run(self):
        try:
            # subprocess.Popen kullanarak çıktıyı satır satır okuyabiliriz
            process = subprocess.Popen(
                self.command_parts,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1, # Satır bazında tamponlama
                universal_newlines=True # Çıktıyı metin olarak al
            )

            # Standard çıktıyı oku
            for line in process.stdout:
                if self._is_canceled:
                    process.terminate()
                    self.error.emit("İşlem kullanıcı tarafından iptal edildi.")
                    return
                self.progress_update.emit(line.strip()) # Her satırı ana arayüze gönder

            # Sürecin tamamlanmasını bekle ve hata çıktısını al
            stderr_output = process.stderr.read()
            process.wait() # Sürecin tamamen bitmesini bekle

            if self._is_canceled:
                self.error.emit("İşlem kullanıcı tarafından iptal edildi.")
                return

            if process.returncode == 0:
                self.finished.emit("Arşivleme başarıyla tamamlandı.")
            else:
                self.error.emit(f"7z komutu hata ile sonlandı (Çıkış kodu: {process.returncode}).\nHata:\n{stderr_output}")

        except FileNotFoundError:
            self.command_not_found.emit("7z komutu bulunamadı. Lütfen 7-Zip'in kurulu olduğundan ve sistem PATH'inizde olduğundan emin olun.")
        except Exception as e:
            self.error.emit(f"Beklenmeyen bir hata oluştu: {e}")

    def cancel(self):
        self._is_canceled = True

class ProgressDialog(QDialog):
    """
    Arşivleme ilerlemesini gösteren açılır pencere.
    """
    def __init__(self, parent=None, language_data=None):
        super().__init__(parent)
        self.language_data = language_data if language_data else LANGUAGES["tr"]
        self.setWindowTitle(self.language_data["progress_dialog_title"])
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint) # Yardım butonunu kaldır
        self.setModal(True) # Ana pencereyi bloke et

        layout = QVBoxLayout()

        # Başlangıç metni buradan güncellendi
        self.status_label = QLabel(self.language_data["progress_label_text_initial"])
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 0) # Belirsiz (indeterminate) mod
        layout.addWidget(self.progress_bar)
        
        # İlerleme detaylarını gösteren metin alanı
        self.log_text_edit = QTextEdit(self)
        self.log_text_edit.setReadOnly(True)
        self.log_text_edit.setMinimumHeight(150)
        layout.addWidget(self.log_text_edit)

        self.cancel_button = QPushButton(self.language_data["cancel_compression_button"])
        layout.addWidget(self.cancel_button)

        self.setLayout(layout)
        self.setFixedSize(400, 300) # Sabit boyut

    def update_progress_status(self, message):
        self.log_text_edit.append(message) # Her yeni satırı log'a ekle
        self.log_text_edit.verticalScrollBar().setValue(self.log_text_edit.verticalScrollBar().maximum()) # En aşağı kaydır

    def set_progress_finished(self):
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(100)
        self.status_label.setText(self.language_data["compression_command_success_message"])
        self.cancel_button.setEnabled(False) # Tamamlanınca iptal etme düğmesini devre dışı bırak

    def set_progress_error(self, error_message):
        self.progress_bar.setRange(0, 1)
        self.progress_bar.setValue(1) # Hata durumunda da progress barı tamamlanmış gibi göster
        self.status_label.setText(self.language_data["compression_command_error_message"])
        self.log_text_edit.append(error_message)
        self.log_text_edit.verticalScrollBar().setValue(self.log_text_edit.verticalScrollBar().maximum())
        self.cancel_button.setEnabled(False)


class SevenZipAddArchiveGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.supported_languages = list(LANGUAGES.keys())
        self.current_language_index = 0
        self.current_language = self.supported_languages[self.current_language_index]
        self.selected_source_paths = []
        self.worker = None # Worker nesnesini tutmak için
        self.progress_dialog = None # İlerleme penceresini tutmak için
        self.initUI()
        self.apply_language() # initUI sonrası dili uygula ve başlangıç arşiv yolunu ayarla

    def _find_image_path(self, filename):
        # Deb paketi kurulduğunda resim dosyalarının bulunması beklenen standart yol.
        # Kullanıcının isteği üzerine, /usr/share/7zip_GUI/ dizini içinde arar.
        installed_path = os.path.join("/usr", "share", "7zip_GUI", filename)
        if os.path.exists(installed_path):
            return installed_path
        
        # Geliştirme/test ortamı için yedek (eğer resimler betik ile aynı dizinde ise)
        current_script_dir = os.path.dirname(os.path.abspath(__file__))
        dev_path = os.path.join(current_script_dir, filename)
        if os.path.exists(dev_path):
            return dev_path
            
        return None

    def initUI(self):
        self.setGeometry(100, 100, 600, 600) 

        main_layout = QVBoxLayout()

        # Uygulama simgesi
        logo_path = self._find_image_path("7zlogo.png")
        if logo_path:
            app_icon = QIcon(logo_path)
            QApplication.setWindowIcon(app_icon)
            self.setWindowIcon(app_icon)

        # Amblem ve butonlar için üst yatay düzen
        top_bar_layout = QHBoxLayout()

        # Amblem etiketi
        self.emblem_label = QLabel(self)
        # Amblem etiketine sabit boyut verin, böylece hem PNG hem GIF aynı alanı kaplar
        self.emblem_label.setFixedSize(QSize(128, 128)) 
        
        # Statik amblemi yükle
        emblem_path = self._find_image_path("7zemblem.png")
        if emblem_path:
            self.static_emblem_pixmap = QPixmap(emblem_path)
            if not self.static_emblem_pixmap.isNull():
                # PNG boyutunu 128x128 olarak ayarla (oranı koruyarak)
                scaled_pixmap = self.static_emblem_pixmap.scaled(128, 128, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.emblem_label.setPixmap(scaled_pixmap)
            else:
                self.emblem_label.setText("Amblem Yüklenemedi (Statik)")
        else:
            self.static_emblem_pixmap = QPixmap() # Boş QPixmap
            self.emblem_label.setText("Amblem Yüklenemedi (Statik)")

        # Animasyonlu GIF'i yükle
        gif_path = self._find_image_path("emblemgif.gif")
        if gif_path:
            self.animated_emblem_movie = QMovie(gif_path)
            # GIF boyutunu burada doğrudan ayarlamayız, _apply_gif_scaling metodunda yapacağız
            # Ancak yine de QMovie nesnesini geçerli bir şekilde başlatmak iyi bir fikir olabilir
            if not self.animated_emblem_movie.isValid():
                self.animated_emblem_movie = None # Geçersizse None olarak işaretle
        else:
            self.animated_emblem_movie = None # GIF bulunamazsa None olarak ayarla
            
        self.emblem_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter) # Sola yasla
        top_bar_layout.addWidget(self.emblem_label)
        top_bar_layout.addItem(QSpacerItem(20, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)) # Genişletilebilir boşluk

        self.about_button = QPushButton()
        self.about_button.clicked.connect(self.show_about_dialog)
        self.language_button = QPushButton()
        self.language_button.clicked.connect(self.toggle_language)

        top_bar_layout.addWidget(self.about_button)
        top_bar_layout.addWidget(self.language_button)
        main_layout.addLayout(top_bar_layout)


        # --- Kaynak Dosyalar/Klasörler ---
        self.source_group = QGroupBox()
        source_layout = QGridLayout()

        self.source_list_widget = DroppableListWidget()
        self.source_list_widget.setMinimumHeight(60)
        self.source_list_widget.new_paths_dropped.connect(self.add_paths_to_source_list)

        source_layout.addWidget(self.source_list_widget, 0, 0, 1, 3)

        source_buttons_layout = QHBoxLayout()
        self.add_files_button = QPushButton()
        self.add_files_button.clicked.connect(lambda: self.add_files())
        self.add_folder_button = QPushButton()
        self.add_folder_button.clicked.connect(lambda: self.add_folder())
        self.remove_selected_button = QPushButton()
        self.remove_selected_button.clicked.connect(self.remove_selected_sources)

        source_buttons_layout.addWidget(self.add_files_button)
        source_buttons_layout.addWidget(self.add_folder_button)
        source_buttons_layout.addWidget(self.remove_selected_button)
        source_buttons_layout.addStretch(1)

        source_layout.addLayout(source_buttons_layout, 1, 0, 1, 3)

        self.source_group.setLayout(source_layout)
        main_layout.addWidget(self.source_group)


        # --- Hedef Arşiv Ayarları ---
        self.archive_group = QGroupBox()
        archive_layout = QGridLayout()

        self.archive_label = QLabel()
        self.archive_path_input = QLineEdit() # Başlangıç değeri burada verilmeyecek
        self.browse_archive_button = QPushButton()
        self.browse_archive_button.clicked.connect(self.browse_archive_path)

        archive_path_input_browse_layout = QHBoxLayout()
        archive_path_input_browse_layout.addWidget(self.archive_path_input)
        archive_path_input_browse_layout.addWidget(self.browse_archive_button)
        archive_path_input_browse_layout.setStretch(0, 1)

        archive_layout.addWidget(self.archive_label, 0, 0)
        archive_layout.addLayout(archive_path_input_browse_layout, 0, 1)

        self.format_label = QLabel()
        self.format_combo = QComboBox()
        self.format_combo.addItems(["7z", "zip", "tar", "wim", "xz", "gzip", "bzip2"])
        self.format_combo.currentIndexChanged.connect(self.update_archive_extension)
        archive_layout.addWidget(self.format_label, 1, 0)
        archive_layout.addWidget(self.format_combo, 1, 1)
        
        archive_layout.setColumnStretch(0, 0)
        archive_layout.setColumnStretch(1, 1)

        self.archive_group.setLayout(archive_layout)
        main_layout.addWidget(self.archive_group)

        # --- Sıkıştırma Ayarları ---
        self.compression_group = QGroupBox()
        compression_layout = QGridLayout()

        self.level_label = QLabel()
        self.level_combo = QComboBox()
        compression_layout.addWidget(self.level_label, 0, 0)
        compression_layout.addWidget(self.level_combo, 0, 1)

        self.method_label = QLabel()
        self.method_combo = QComboBox()
        self.method_combo.addItems(["LZMA2", "LZMA", "PPMD", "BZip2", "Deflate"])
        self.method_combo.setCurrentText("LZMA2")
        compression_layout.addWidget(self.method_label, 1, 0)
        compression_layout.addWidget(self.method_combo, 1, 1)

        self.dict_size_label = QLabel()
        self.dict_size_combo = QComboBox()
        self.dict_size_combo.addItems(["Otomatik", "1 MB", "2 MB", "4 MB", "8 MB", "16 MB", "32 MB", "64 MB", "128 MB", "256 MB"])
        self.dict_size_combo.setCurrentText("32 MB")
        compression_layout.addWidget(self.dict_size_label, 2, 0)
        compression_layout.addWidget(self.dict_size_combo, 2, 1)

        self.threads_label = QLabel()
        self.threads_spinbox = QSpinBox()
        self.threads_spinbox.setMinimum(1)
        self.threads_spinbox.setMaximum(8)
        self.threads_spinbox.setValue(4)
        compression_layout.addWidget(self.threads_label, 3, 0)
        compression_layout.addWidget(self.threads_spinbox, 3, 1)
        
        compression_layout.setColumnStretch(0, 0)
        compression_layout.setColumnStretch(1, 1)

        self.compression_group.setLayout(compression_layout)
        main_layout.addWidget(self.compression_group)

        # --- Arşivleme Seçenekleri ---
        self.options_group = QGroupBox()
        options_layout = QGridLayout()

        self.update_mode_label = QLabel()
        self.update_mode_combo = QComboBox()
        options_layout.addWidget(self.update_mode_label, 0, 0)
        options_layout.addWidget(self.update_mode_combo, 0, 1)

        self.password_label = QLabel()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        
        self.password_repeat_label = QLabel()
        self.password_repeat_input = QLineEdit()
        self.password_repeat_input.setEchoMode(QLineEdit.Password)

        password_fields_layout = QHBoxLayout()
        password_fields_layout.addWidget(self.password_input)
        password_fields_layout.addWidget(self.password_repeat_label)
        password_fields_layout.addWidget(self.password_repeat_input)
        password_fields_layout.addStretch(1)

        options_layout.addWidget(self.password_label, 1, 0)
        options_layout.addLayout(password_fields_layout, 1, 1)

        self.encrypt_filenames_checkbox = QCheckBox()
        self.show_password_checkbox = QCheckBox()
        self.show_password_checkbox.stateChanged.connect(self.toggle_password_visibility)

        options_layout.addWidget(self.encrypt_filenames_checkbox, 2, 0, 1, 2)
        options_layout.addWidget(self.show_password_checkbox, 3, 0, 1, 2)

        self.solid_block_checkbox = QCheckBox()
        self.split_volumes_checkbox = QCheckBox()
        self.split_size_combo = QComboBox()
        self.split_size_combo.setEditable(True)
        self.split_size_combo.setEnabled(False)
        self.split_volumes_checkbox.stateChanged.connect(lambda state: self.split_size_combo.setEnabled(state == Qt.Checked))

        options_layout.addWidget(self.solid_block_checkbox, 4, 0, 1, 2)
        options_layout.addWidget(self.split_volumes_checkbox, 5, 0)
        options_layout.addWidget(self.split_size_combo, 5, 1)
        
        options_layout.setColumnStretch(0, 0)
        options_layout.setColumnStretch(1, 1)

        self.options_group.setLayout(options_layout)
        main_layout.addWidget(self.options_group)

        # --- Aksiyon Butonları ---
        button_layout = QHBoxLayout()
        self.ok_button = QPushButton()
        self.ok_button.clicked.connect(self.on_ok_clicked)
        self.cancel_button = QPushButton()
        self.cancel_button.clicked.connect(self.close)

        button_layout.addStretch(1)
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def _set_initial_archive_path(self):
        """Program başlangıcında veya dil değiştiğinde varsayılan arşiv yolunu ayarlar."""
        lang_data = LANGUAGES[self.current_language]
        default_basename = lang_data["default_archive_basename"]
        current_format = self.format_combo.currentText()
        
        if self.selected_source_paths:
            # Eğer kaynak dosyalar/klasörler seçiliyse, ilk öğenin dizinini ve adını kullan
            first_source_path = self.selected_source_paths[0]
            initial_dir = os.path.dirname(first_source_path)
            # Eğer tek bir dosya seçildiyse, o dosyanın adını kullan, aksi takdirde klasör adını veya varsayılanı kullan
            if os.path.isfile(first_source_path):
                initial_name = os.path.splitext(os.path.basename(first_source_path))[0]
            else: # Klasör ise
                initial_name = os.path.basename(first_source_path)
            
            self.archive_path_input.setText(os.path.join(initial_dir, f"{initial_name}.{current_format}"))
        else:
            # Hiçbir kaynak seçili değilse, kullanıcının ana dizinini ve varsayılan adı kullan
            initial_dir = os.path.expanduser('~')
            self.archive_path_input.setText(os.path.join(initial_dir, f"{default_basename}.{current_format}"))


    def add_files(self):
        lang_data = LANGUAGES[self.current_language]
        files, _ = QFileDialog.getOpenFileNames(self, lang_data["add_files_button"], "", "All Files (*);;Text Files (*.txt)")
        if files:
            self.add_paths_to_source_list(files)

    def add_folder(self):
        lang_data = LANGUAGES[self.current_language]
        folder = QFileDialog.getExistingDirectory(self, lang_data["add_folder_button"])
        if folder:
            self.add_paths_to_source_list([folder])

    def add_paths_to_source_list(self, paths):
        
        is_first_addition = not self.selected_source_paths # İlk ekleme mi kontrol et
        
        for p in paths:
            if p not in self.selected_source_paths:
                self.selected_source_paths.append(p)
                self.source_list_widget.addItem(p)
        
        # Eğer ilk ekleme ise veya arşiv yolu hala varsayılan isimdeyse güncelle
        # Bu, kullanıcının manuel olarak değiştirdiği bir arşiv yolunu korumamızı sağlar.
        current_archive_path_text = self.archive_path_input.text()
        default_basename = LANGUAGES[self.current_language]["default_archive_basename"]
        
        # Eğer current_archive_path_text varsayılan isme sahipse veya boşsa güncelle
        # (Örnek: "yeni_arsiv.7z" içeriyorsa veya hiç ayarlanmamışsa)
        if is_first_addition or default_basename in os.path.basename(current_archive_path_text):
            self._set_initial_archive_path()

    def remove_selected_sources(self):
        selected_items = self.source_list_widget.selectedItems()
        if not selected_items:
            return

        for item in reversed(selected_items):
            row = self.source_list_widget.row(item)
            path_to_remove = self.source_list_widget.item(row).text()
            if path_to_remove in self.selected_source_paths:
                self.selected_source_paths.remove(path_to_remove)
            self.source_list_widget.takeItem(row)
        
        # Eğer tüm kaynaklar kaldırıldıysa, arşiv yolunu ana dizine geri çevir
        # veya kalan ilk öğeye göre yeniden ayarla.
        self._set_initial_archive_path()

    def apply_language(self):
        lang_data = LANGUAGES[self.current_language]

        self.setWindowTitle(lang_data["window_title"])
        self.about_button.setText(lang_data["about_button"])
        self.language_button.setText(lang_data["language_button"])

        self.source_group.setTitle(lang_data["source_group_title"])
        self.add_files_button.setText(lang_data["add_files_button"])
        self.add_folder_button.setText(lang_data["add_folder_button"])
        self.remove_selected_button.setText(lang_data["remove_selected_button"])

        self.archive_group.setTitle(lang_data["target_group_title"])
        self.archive_label.setText(lang_data["archive_label"])
        self.browse_archive_button.setText(lang_data["browse_button"])
        self.format_label.setText(lang_data["archive_format_label"])

        self.compression_group.setTitle(lang_data["compression_group_title"])
        self.level_label.setText(lang_data["compression_level_label"])
        current_level_text = self.level_combo.currentText()
        self.level_combo.clear()
        self.level_combo.addItems([
            lang_data["level_store"],
            lang_data["level_fastest"],
            lang_data["level_fast"],
            lang_data["level_normal"],
            lang_data["level_maximum"],
            lang_data["level_ultra"]
        ])
        if self.level_combo.findText(current_level_text) != -1:
            self.level_combo.setCurrentText(current_level_text)
        else:
            self.level_combo.setCurrentText(lang_data["level_normal"])


        self.method_label.setText(lang_data["compression_method_label"])
        self.dict_size_label.setText(lang_data["dictionary_size_label"])
        self.threads_label.setText(lang_data["threads_label"])

        self.options_group.setTitle(lang_data["options_group_title"])
        self.update_mode_label.setText(lang_data["update_mode_label"])
        current_update_mode_text = self.update_mode_combo.currentText()
        self.update_mode_combo.clear()
        self.update_mode_combo.addItems([
            lang_data["update_add_replace"],
            lang_data["update_only_update"],
            lang_data["update_synchronize"],
            lang_data["update_add_no_replace"]
        ])
        if self.update_mode_combo.findText(current_update_mode_text) != -1:
            self.update_mode_combo.setCurrentText(current_update_mode_text)
        else:
            self.update_mode_combo.setCurrentText(lang_data["update_add_replace"])


        self.password_label.setText(lang_data["password_label"])
        self.password_repeat_label.setText(lang_data["password_repeat_label"])
        self.encrypt_filenames_checkbox.setText(lang_data["encrypt_filenames_checkbox"])
        self.show_password_checkbox.setText(lang_data["show_password_checkbox"])
        self.solid_block_checkbox.setText(lang_data["solid_block_checkbox"])
        self.split_volumes_checkbox.setText(lang_data["split_volumes_checkbox"])

        current_split_text = self.split_size_combo.currentText()
        self.split_size_combo.setPlaceholderText(lang_data["split_placeholder"])
        self.split_size_combo.clear()
        self.split_size_combo.addItems(["", "1.44 MB (Floppy)", "650 MB (CD)", "700 MB (CD)", "4480 MB (DVD)"])
        if current_split_text and current_split_text not in self.split_size_combo.currentText():
            self.split_size_combo.setEditText(current_split_text)

        self.ok_button.setText(lang_data["ok_button"])
        self.cancel_button.setText(lang_data["cancel_button"])

        # Dil değiştiğinde veya başlangıçta arşiv yolu adını güncelle
        self._set_initial_archive_path()

    def browse_archive_path(self):
        lang_data = LANGUAGES[self.current_language]
        current_format = self.format_combo.currentText()
        
        # Mevcut arşiv yolu inputundaki metni al
        current_path_text = self.archive_path_input.text()
        
        initial_dir = os.path.dirname(current_path_text) if current_path_text else os.path.expanduser('~')
        initial_filename = os.path.basename(current_path_text) if current_path_text else f"{LANGUAGES[self.current_language]['default_archive_basename']}.{current_format}"

        # Eğer uzantı format_combo'daki ile eşleşmiyorsa, doğru uzantıyı ekle
        if not initial_filename.endswith(f".{current_format}"):
            # Önceki uzantıyı kaldırıp yenisini eklemeye çalış
            name_without_ext = os.path.splitext(initial_filename)[0]
            initial_filename = f"{name_without_ext}.{current_format}"


        file_name, _ = QFileDialog.getSaveFileName(self, lang_data["archive_label"], 
                                                   os.path.join(initial_dir, initial_filename),
                                                   f"7z Archives (*.7z);Zip Archives (*.zip);All Files (*)")
        if file_name:
            self.archive_path_input.setText(file_name)
            # Seçilen dosya adına göre formatı otomatik ayarla
            ext = file_name.split('.')[-1]
            if ext in ["7z", "zip", "tar", "wim", "xz", "gzip", "bzip2"]:
                self.format_combo.setCurrentText(ext)
            else:
                # Bilinmeyen bir uzantı ise varsayılan 7z'ye dön
                self.format_combo.setCurrentText("7z")


    def update_archive_extension(self):
        current_path = self.archive_path_input.text()
        current_format = self.format_combo.currentText()
        
        if current_path:
            # Dosya adını ve uzantısını ayır
            base_name, old_ext = os.path.splitext(current_path)
            
            # Eğer eski uzantı mevcut ve geçerli formatlardan biri değilse,
            # veya eski uzantı yeni formatla aynı değilse, uzantıyı güncelle.
            # Aksi takdirde, kullanıcının girdiği tam adı koru.
            valid_extensions = ["7z", "zip", "tar", "wim", "xz", "gzip", "bzip2"]
            
            if old_ext and old_ext[1:] in valid_extensions and old_ext[1:] != current_format:
                self.archive_path_input.setText(f"{base_name}.{current_format}")
            elif not old_ext: # Uzantı yoksa ekle
                 self.archive_path_input.setText(f"{base_name}.{current_format}")
            # Eğer eski uzantı zaten doğru formatı gösteriyorsa veya
            # kullanıcı manuel olarak başka bir uzantı girdiyse (ve bu geçerli bir 7z uzantısı değilse),
            # otomatik değiştirmeyi yapma.
            # Örneğin, kullanıcı "my_archive.rar" yazdıysa, format "zip" olsa bile ".rar" kalsın.
            # Ancak biz burada sadece 7z ile ilgili uzantıları kontrol ediyoruz.
            elif old_ext[1:] == current_format:
                pass # Zaten doğru uzantıda, değişiklik yapma
        else:
            # Eğer arşiv yolu boşsa, varsayılan adı ve uzantıyı ayarla
            self._set_initial_archive_path()

    def toggle_password_visibility(self, state):
        if state == Qt.Checked:
            self.password_input.setEchoMode(QLineEdit.Normal)
            self.password_repeat_input.setEchoMode(QLineEdit.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.Password)
            self.password_repeat_input.setEchoMode(QLineEdit.Password)

    def _apply_gif_scaling(self):
        """Calculates and applies aspect-ratio preserving scaling for the GIF movie."""
        if self.animated_emblem_movie and self.animated_emblem_movie.isValid():
            # movie'nin çerçeve bilgilerini alabilmek için başlat ve durdur
            # Bu, QMovie'nin ilk çerçevesini yüklemesini sağlar.
            self.animated_emblem_movie.setPaused(True) # Oynatmayı duraklat
            self.animated_emblem_movie.jumpToFrame(0) # İlk kareye git

            original_size = self.animated_emblem_movie.currentImage().size()
            
            if not original_size.isEmpty() and original_size.width() > 0 and original_size.height() > 0:
                target_width = 128
                target_height = 128

                w_ratio = float(target_width) / original_size.width()
                h_ratio = float(target_height) / original_size.height()
                
                scale_factor = min(w_ratio, h_ratio)
                
                scaled_width = int(original_size.width() * scale_factor)
                scaled_height = int(original_size.height() * scale_factor)
                
                self.animated_emblem_movie.setScaledSize(QSize(scaled_width, scaled_height))
            # else: print("Warning: Original GIF frame size invalid or zero.")
        # else: print("Warning: Animated emblem movie is not valid.")

    def on_ok_clicked(self):
        lang_data = LANGUAGES[self.current_language]

        if not self.selected_source_paths:
            QMessageBox.warning(self, lang_data["options_summary_title"], lang_data["no_source_selected"])
            return

        # GIF'i göstermeden önce doğru ölçeklemeyi uygula
        self._apply_gif_scaling()

        # Animasyonlu GIF'i göster
        if self.animated_emblem_movie and self.animated_emblem_movie.isValid():
            self.emblem_label.setMovie(self.animated_emblem_movie)
            self.animated_emblem_movie.start()
        elif not self.static_emblem_pixmap.isNull():
            # Eğer GIF yoksa ama statik amblem varsa onu göster (yedek)
            # PNG zaten initUI'da uygun şekilde ölçeklenmişti.
            # Burada tekrar atama yapıldığından emin olun.
            scaled_pixmap = self.static_emblem_pixmap.scaled(128, 128, Qt.KeepAspectRatio, Qt.SmoothTransformation) 
            self.emblem_label.setPixmap(scaled_pixmap) 
        else:
            self.emblem_label.setText("Amblem Yüklenemedi")

        archive_path = self.archive_path_input.text()
        archive_format = self.format_combo.currentText()
        compression_level_text = self.level_combo.currentText()
        compression_method = self.method_combo.currentText()
        dictionary_size_text = self.dict_size_combo.currentText()
        cpu_threads = self.threads_spinbox.value()
        update_mode_text = self.update_mode_combo.currentText()
        password = self.password_input.text()
        password_repeat = self.password_repeat_input.text()
        encrypt_filenames = self.encrypt_filenames_checkbox.isChecked()
        solid_block = self.solid_block_checkbox.isChecked()
        split_volumes = self.split_volumes_checkbox.isChecked()
        split_size = self.split_size_combo.currentText() if split_volumes else ""

        if password and password != password_repeat:
            QMessageBox.warning(self, lang_data["password_mismatch_title"], lang_data["password_mismatch_message"])
            self.reset_emblem() # Şifre hatasında amblemi geri çevir
            return

        # 7-Zip komutunu oluştur (Linux'a uygun)
        command_parts = ["7z", "a"] # 'a' arşivleme (add) komutu

        # Arşiv yolu - shlex.quote() KALDIRILDI
        command_parts.append(archive_path) 

        # Kaynak yollar - shlex.quote() KALDIRILDI
        for path in self.selected_source_paths:
            command_parts.append(path)

        # Sıkıştırma Seviyesi
        compression_level_map = {
            lang_data["level_store"]: "0",
            lang_data["level_fastest"]: "1",
            lang_data["level_fast"]: "3",
            lang_data["level_normal"]: "5",
            lang_data["level_maximum"]: "7",
            lang_data["level_ultra"]: "9"
        }
        level_param = compression_level_map.get(compression_level_text, "5")
        command_parts.append(f"-mx{level_param}")

        # Arşiv Biçimi
        command_parts.append(f"-t{archive_format}")

        # Sıkıştırma Yöntemi (7z formatı için)
        if archive_format == "7z":
            if compression_method:
                command_parts.append(f"-m0={compression_method}")
            # Sözlük Boyutu (7z ve LZMA/LZMA2 için)
            if dictionary_size_text != "Otomatik" and compression_method in ["LZMA2", "LZMA"]:
                dict_size_value = dictionary_size_text.replace(" MB", "m").replace(" ", "")
                command_parts.append(f"-md={dict_size_value}")

        # CPU İş Parçacıkları
        command_parts.append(f"-mmt={cpu_threads}")

        # Şifre
        if password:
            command_parts.append(f'-p{shlex.quote(password)}') # Şifreyi tırnak içine al - KORUNDU
            if encrypt_filenames:
                command_parts.append("-mhe") # Dosya adlarını şifrele

        # Katı Blok Arşivleme (Solid Block Archiving)
        if solid_block and archive_format == "7z":
            command_parts.append("-ms=on")

        # Bölümlere Ayır (Split Volumes)
        if split_volumes and split_size:
            size_val = ""
            if " " in split_size: # "1.44 MB (Floppy)" gibi
                size_val_parts = split_size.split(" ")
                size_num = size_val_parts[0]
                unit = size_val_parts[1] if len(size_val_parts) > 1 else ""

                try:
                    numeric_value = float(size_num)
                    if "MB" in unit:
                        if size_num == "1.44":
                            size_val = "1440k"
                        else:
                            size_val = f"{int(numeric_value * 1024 * 1024)}" # MB'ı byte'a çevir
                    elif "GB" in unit:
                        size_val = f"{int(numeric_value * 1024 * 1024 * 1024)}" # GB'ı byte'a çevir
                    elif "KB" in unit:
                        size_val = f"{int(numeric_value * 1024)}" # KB'ı byte'a çevir
                    else:
                        size_val = split_size # Bilinmeyen birim, olduğu gibi bırak
                except ValueError:
                    size_val = split_size # Sayısal olmayan giriş, olduğu gibi bırak
            else: # Kullanıcı sadece "100m", "5g" gibi bir değer girmiş olabilir
                size_val = split_size

            if size_val:
                command_parts.append(f"-v{size_val}")

        # Güncelleme Modu (Update Mode)
        update_mode_map = {
            lang_data["update_add_replace"]: [], # Varsayılan 'a' ile
            lang_data["update_only_update"]: ["-u!a-"], # Sadece güncelle
            lang_data["update_synchronize"]: ["-u-", "-up0", "-u!a-"], # Senkronize et
            lang_data["update_add_no_replace"]: ["-uo-"] # Ekle, var olanları değiştirme
        }
        update_params = update_mode_map.get(update_mode_text, [])
        command_parts.extend(update_params)

        # İlerleme penceresini göster
        self.progress_dialog = ProgressDialog(self, language_data=lang_data)
        self.progress_dialog.cancel_button.clicked.connect(self.cancel_compression)
        self.progress_dialog.show()

        # Worker thread'i başlat
        self.worker = SevenZipWorker(command_parts)
        self.worker.progress_update.connect(self.progress_dialog.update_progress_status)
        self.worker.finished.connect(self.on_compression_finished)
        self.worker.error.connect(self.on_compression_error)
        self.worker.command_not_found.connect(self.on_command_not_found)
        self.worker.start() # İş parçacığını başlat

    def reset_emblem(self):
        """Amblemi statik PNG resmine döndürür ve GIF animasyonunu durdurur."""
        if self.animated_emblem_movie and self.animated_emblem_movie.state() == QMovie.Running:
            self.animated_emblem_movie.stop()
        if not self.static_emblem_pixmap.isNull():
            # Yeniden ölçekleme, çünkü reset_emblem doğrudan çağrılabilir ve initUI'deki ilk ayar silinmiş olabilir.
            scaled_pixmap = self.static_emblem_pixmap.scaled(128, 128, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.emblem_label.setPixmap(scaled_pixmap)
        else:
            self.emblem_label.setText("Amblem Yüklenemedi (Statik)")


    def cancel_compression(self):
        """Sıkıştırma işlemini iptal eder."""
        if self.worker and self.worker.isRunning():
            self.worker.cancel() # Worker'a iptal sinyali gönder
            self.progress_dialog.status_label.setText(LANGUAGES[self.current_language]["progress_status_label"] + " İptal ediliyor...")
            self.progress_dialog.cancel_button.setEnabled(False)
            self.reset_emblem() # Amblemi sıfırla


    def on_compression_finished(self, message):
        """Sıkıştırma tamamlandığında çağrılır."""
        self.progress_dialog.set_progress_finished()
        QMessageBox.information(
            self,
            LANGUAGES[self.current_language]["compression_command_success_title"],
            f"{LANGUAGES[self.current_language]['compression_command_success_message']}\n{message}"
        )
        self.progress_dialog.accept() # Pencereyi kapat
        self.reset_emblem() # Amblemi sıfırla

    def on_compression_error(self, message):
        """Sıkıştırma hatası oluştuğunda çağrılır."""
        self.progress_dialog.set_progress_error(message)
        QMessageBox.critical(
            self,
            LANGUAGES[self.current_language]["compression_command_error_title"],
            f"{LANGUAGES[self.current_language]['compression_command_error_message']}\n{message}"
        )
        self.progress_dialog.accept() # Pencereyi kapat
        self.reset_emblem() # Amblemi sıfırla

    def on_command_not_found(self, message):
        """7z komutu bulunamadığında çağrılır."""
        self.progress_dialog.set_progress_error(message)
        QMessageBox.critical(
            self,
            LANGUAGES[self.current_language]["compression_command_error_title"],
            message
        )
        self.progress_dialog.accept() # Pencereyi kapat
        self.reset_emblem() # Amblemi sıfırla


    def show_about_dialog(self):
        lang_data = LANGUAGES[self.current_language]
        QMessageBox.about(self, lang_data["about_title"], lang_data["about_text"])

    def toggle_language(self):
        self.current_language_index = (self.current_language_index + 1) % len(self.supported_languages)
        self.current_language = self.supported_languages[self.current_language_index]
        self.apply_language()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SevenZipAddArchiveGUI()
    ex.show()
    sys.exit(app.exec_())
