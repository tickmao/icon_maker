import datetime
import io
import os

from flask import (Flask, Response, redirect, render_template, request,
                   send_file)
from PIL import Image

app = Flask(__name__, template_folder='../templates')
app.secret_key = os.environ.get('SECRET_KEY', 'global_ico_full_localized_v7')
app.url_map.strict_slashes = False
app.config['MAX_CONTENT_LENGTH'] = 4.5 * 1024 * 1024

# ==========================================
# 1. 终极全球语言包 (22种语言 - 全文翻译)
# ==========================================
TRANSLATIONS = {
    # --- English (英语) ---
    'en': {
        'name': 'English', 'dir': 'ltr', 'recommend': 'Recommended', 'badge': 'HOT',
        'seo_title': 'Free Online ICO Converter - Create Transparent Favicon',
        'seo_desc': 'Best free online ICO converter. Convert PNG, JPG to ICO format instantly.',
        'keywords': 'ico converter, favicon generator, png to ico, make favicon',
        'h1': 'ICO Converter', 'subtitle': 'Professional Favicon Generator',
        'upload_label': 'Click to upload or Drag image', 'size_label': 'Target Size', 'btn_submit': 'Generate ICO',
        'footer': 'Securely processed. Privacy protected.', 'error_large': 'File too large (Max 4MB)',
        # Guide
        'tab_create': 'Create', 'tab_guide': 'Guide',
        'guide_preview_title': 'Visual Preview', 'guide_preview_desc': 'Your icon will be displayed in browser tabs to help users identify your brand.',
        'step1_title': 'Upload to Server', 'step1_desc': 'Upload the favicon.ico file to your website root directory.', 'step1_file_path': '/root/', 'step1_file_name': 'favicon.ico',
        'step2_title': 'Update HTML', 'step2_desc': 'Paste this code into the <head> section of your HTML.',
        'guide_copy_btn': 'Copy', 'guide_copied': 'Copied!'
    },

    # --- 简体中文 ---
    'zh': {
        'name': '简体中文', 'dir': 'ltr', 'recommend': '推荐尺寸', 'badge': '常用',
        'seo_title': '在线 ICO 图标生成器 - 免费制作透明 Favicon',
        'seo_desc': '免费在线将图片转换为 ICO 图标。支持透明背景，一键生成。',
        'keywords': 'ICO生成器, favicon制作, 在线转ICO, png转ico',
        'h1': 'ICO 图标生成器', 'subtitle': '一键生成透明背景图标',
        'upload_label': '点击选择 或 拖拽图片', 'size_label': '目标尺寸', 'btn_submit': '生成并下载 .ICO',
        'footer': '数据安全保护，不保存任何图片。', 'error_large': '文件过大 (最大 4MB)',
        # Guide
        'tab_create': '制作图标', 'tab_guide': '使用指南',
        'guide_preview_title': '效果预览', 'guide_preview_desc': '图标将显示在浏览器标签页中，提升品牌识别度。',
        'step1_title': '上传至服务器', 'step1_desc': '将生成的 favicon.ico 上传到网站根目录。', 'step1_file_path': '/根目录/', 'step1_file_name': 'favicon.ico',
        'step2_title': '引入 HTML', 'step2_desc': '将下方代码粘贴到网页 <head> 标签之间。',
        'guide_copy_btn': '复制', 'guide_copied': '已复制!'
    },

    # --- 繁体中文 ---
    'tw': {
        'name': '繁體中文', 'dir': 'ltr', 'recommend': '推薦尺寸', 'badge': '常用',
        'seo_title': '線上 ICO 圖示產生器 - 製作透明 Favicon',
        'seo_desc': '免費線上圖片轉 ICO 工具。支援透明背景。',
        'keywords': 'ICO產生器, favicon製作, 線上轉ICO',
        'h1': 'ICO 圖示產生器', 'subtitle': '一鍵生成透明背景圖示',
        'upload_label': '點擊選擇 或 拖曳圖片', 'size_label': '目標尺寸', 'btn_submit': '產生並下載 .ICO',
        'footer': '資料安全保護，不保存任何圖片。', 'error_large': '檔案過大 (最大 4MB)',
        # Guide
        'tab_create': '製作圖示', 'tab_guide': '使用指南',
        'guide_preview_title': '效果預覽', 'guide_preview_desc': '圖示將顯示在瀏覽器分頁上，有助於識別品牌。',
        'step1_title': '上傳至伺服器', 'step1_desc': '將產生的 favicon.ico 上傳到網站根目錄。', 'step1_file_path': '/根目錄/', 'step1_file_name': 'favicon.ico',
        'step2_title': '引入 HTML', 'step2_desc': '將下方程式碼貼到網頁 <head> 標籤之間。',
        'guide_copy_btn': '複製', 'guide_copied': '已複製!'
    },

    # --- Español (西班牙语) ---
    'es': {
        'name': 'Español', 'dir': 'ltr', 'recommend': 'Recomendado', 'badge': 'HOT',
        'seo_title': 'Convertidor ICO Online', 'seo_desc': 'Convierte imágenes a ICO gratis.',
        'keywords': 'convertidor ico, favicon',
        'h1': 'Convertidor ICO', 'subtitle': 'Generador de Favicon', 'upload_label': 'Clic para subir',
        'size_label': 'Tamaño', 'btn_submit': 'Generar .ICO', 'footer': 'Privacidad protegida.', 'error_large': 'Archivo muy grande',
        # Guide
        'tab_create': 'Crear', 'tab_guide': 'Guía',
        'guide_preview_title': 'Vista Previa', 'guide_preview_desc': 'Su icono aparecerá en las pestañas del navegador.',
        'step1_title': 'Subir al Servidor', 'step1_desc': 'Sube el archivo favicon.ico al directorio raíz.', 'step1_file_path': '/raiz/', 'step1_file_name': 'favicon.ico',
        'step2_title': 'Actualizar HTML', 'step2_desc': 'Pega este código en la sección <head>.',
        'guide_copy_btn': 'Copiar', 'guide_copied': '¡Copiado!'
    },

    # --- Français (法语) ---
    'fr': {
        'name': 'Français', 'dir': 'ltr', 'recommend': 'Recommandé', 'badge': 'TOP',
        'seo_title': 'Convertisseur ICO en ligne', 'seo_desc': 'Créer Favicon gratuitement.',
        'keywords': 'convertisseur ico, favicon',
        'h1': 'Convertisseur ICO', 'subtitle': 'Générateur de Favicon', 'upload_label': 'Uploader une image',
        'size_label': 'Taille', 'btn_submit': 'Générer .ICO', 'footer': 'Confidentialité respectée.', 'error_large': 'Fichier trop volumineux',
        # Guide
        'tab_create': 'Créer', 'tab_guide': 'Guide',
        'guide_preview_title': 'Aperçu Visuel', 'guide_preview_desc': 'Votre icône apparaîtra dans les onglets du navigateur.',
        'step1_title': 'Mettre sur Serveur', 'step1_desc': 'Téléversez favicon.ico dans le répertoire racine.', 'step1_file_path': '/racine/', 'step1_file_name': 'favicon.ico',
        'step2_title': 'Code HTML', 'step2_desc': 'Collez ce code dans la section <head>.',
        'guide_copy_btn': 'Copier', 'guide_copied': 'Copié!'
    },

    # --- Deutsch (德语) ---
    'de': {
        'name': 'Deutsch', 'dir': 'ltr', 'recommend': 'Empfohlen', 'badge': 'TOP',
        'seo_title': 'ICO Konverter', 'seo_desc': 'Favicon erstellen.',
        'keywords': 'ico konverter, favicon',
        'h1': 'ICO Konverter', 'subtitle': 'Favicon-Generator', 'upload_label': 'Bild hochladen',
        'size_label': 'Größe', 'btn_submit': '.ICO Herunterladen', 'footer': 'Datenschutz.', 'error_large': 'Datei zu groß',
        # Guide
        'tab_create': 'Erstellen', 'tab_guide': 'Anleitung',
        'guide_preview_title': 'Vorschau', 'guide_preview_desc': 'Ihr Icon wird in den Browser-Tabs angezeigt.',
        'step1_title': 'Auf Server laden', 'step1_desc': 'Laden Sie favicon.ico in das Stammverzeichnis hoch.', 'step1_file_path': '/root/', 'step1_file_name': 'favicon.ico',
        'step2_title': 'HTML einfügen', 'step2_desc': 'Fügen Sie diesen Code in den <head> Bereich ein.',
        'guide_copy_btn': 'Kopieren', 'guide_copied': 'Kopiert!'
    },

    # --- Italiano (意大利语) ---
    'it': {
        'name': 'Italiano', 'dir': 'ltr', 'recommend': 'Consigliato', 'badge': 'TOP',
        'seo_title': 'Convertitore ICO', 'seo_desc': 'Crea Favicon online.',
        'keywords': 'convertitore ico, favicon',
        'h1': 'Convertitore ICO', 'subtitle': 'Generatore di Favicon', 'upload_label': 'Clicca per caricare',
        'size_label': 'Dimensione', 'btn_submit': 'Scarica .ICO', 'footer': 'Privacy protetta.', 'error_large': 'File troppo grande',
        # Guide
        'tab_create': 'Crea', 'tab_guide': 'Guida',
        'guide_preview_title': 'Anteprima', 'guide_preview_desc': 'La tua icona apparirà nelle schede del browser.',
        'step1_title': 'Carica su Server', 'step1_desc': 'Carica favicon.ico nella directory principale.', 'step1_file_path': '/root/', 'step1_file_name': 'favicon.ico',
        'step2_title': 'Codice HTML', 'step2_desc': 'Incolla questo codice nella sezione <head>.',
        'guide_copy_btn': 'Copia', 'guide_copied': 'Copiato!'
    },

    # --- Português (葡萄牙语) ---
    'pt': {
        'name': 'Português', 'dir': 'ltr', 'recommend': 'Recomendado', 'badge': 'HOT',
        'seo_title': 'Conversor ICO', 'seo_desc': 'Criar Favicon.',
        'keywords': 'conversor ico, favicon',
        'h1': 'Conversor de ICO', 'subtitle': 'Gerador de Favicon', 'upload_label': 'Clique para subir',
        'size_label': 'Tamanho', 'btn_submit': 'Baixar .ICO', 'footer': 'Privacidade protegida.', 'error_large': 'Arquivo muito grande',
        # Guide
        'tab_create': 'Criar', 'tab_guide': 'Guia',
        'guide_preview_title': 'Pré-visualização', 'guide_preview_desc': 'Seu ícone aparecerá nas abas do navegador.',
        'step1_title': 'Enviar ao Servidor', 'step1_desc': 'Envie favicon.ico para o diretório raiz.', 'step1_file_path': '/raiz/', 'step1_file_name': 'favicon.ico',
        'step2_title': 'Código HTML', 'step2_desc': 'Cole este código na seção <head>.',
        'guide_copy_btn': 'Copiar', 'guide_copied': 'Copiado!'
    },

    # --- Русский (俄语) ---
    'ru': {
        'name': 'Русский', 'dir': 'ltr', 'recommend': 'Стандарт', 'badge': 'ХИТ',
        'seo_title': 'Конвертер ICO', 'seo_desc': 'Создать Favicon.',
        'keywords': 'ico конвертер, favicon',
        'h1': 'Конвертер ICO', 'subtitle': 'Генератор иконок', 'upload_label': 'Загрузить файл',
        'size_label': 'Размер', 'btn_submit': 'Скачать .ICO', 'footer': 'Конфиденциальность.', 'error_large': 'Файл слишком большой',
        # Guide
        'tab_create': 'Создать', 'tab_guide': 'Гид',
        'guide_preview_title': 'Предпросмотр', 'guide_preview_desc': 'Ваша иконка будет отображаться во вкладках браузера.',
        'step1_title': 'Загрузка', 'step1_desc': 'Загрузите файл favicon.ico в корневой каталог сайта.', 'step1_file_path': '/root/', 'step1_file_name': 'favicon.ico',
        'step2_title': 'HTML код', 'step2_desc': 'Вставьте этот код в раздел <head>.',
        'guide_copy_btn': 'Копия', 'guide_copied': 'Скопировано!'
    },

    # --- Nederlands (荷兰语) ---
    'nl': {
        'name': 'Nederlands', 'dir': 'ltr', 'recommend': 'Aanbevolen', 'badge': 'TOP',
        'seo_title': 'ICO Converter', 'seo_desc': 'Favicon maken.',
        'keywords': 'ico converter, favicon',
        'h1': 'ICO Converter', 'subtitle': 'Favicon Generator', 'upload_label': 'Klik om te uploaden',
        'size_label': 'Grootte', 'btn_submit': 'Downloaden', 'footer': 'Privacy beschermd.', 'error_large': 'Bestand te groot',
        # Guide
        'tab_create': 'Maken', 'tab_guide': 'Gids',
        'guide_preview_title': 'Voorbeeld', 'guide_preview_desc': 'Uw pictogram verschijnt in browsertabbladen.',
        'step1_title': 'Uploaden', 'step1_desc': 'Upload favicon.ico naar de hoofdmap.', 'step1_file_path': '/root/', 'step1_file_name': 'favicon.ico',
        'step2_title': 'HTML Code', 'step2_desc': 'Plak deze code in de <head> sectie.',
        'guide_copy_btn': 'Kopiëren', 'guide_copied': 'Gekopieerd!'
    },

    # --- Polski (波兰语) ---
    'pl': {
        'name': 'Polski', 'dir': 'ltr', 'recommend': 'Zalecane', 'badge': 'HIT',
        'seo_title': 'Konwerter ICO', 'seo_desc': 'Generator Favicon.',
        'keywords': 'konwerter ico, favicon',
        'h1': 'Konwerter ICO', 'subtitle': 'Generator Favicon', 'upload_label': 'Prześlij plik',
        'size_label': 'Rozmiar', 'btn_submit': 'Pobierz .ICO', 'footer': 'Ochrona prywatności.', 'error_large': 'Plik zbyt duży',
        # Guide
        'tab_create': 'Stwórz', 'tab_guide': 'Instrukcja',
        'guide_preview_title': 'Podgląd', 'guide_preview_desc': 'Twoja ikona pojawi się na kartach przeglądarki.',
        'step1_title': 'Prześlij', 'step1_desc': 'Prześlij plik favicon.ico do katalogu głównego.', 'step1_file_path': '/root/', 'step1_file_name': 'favicon.ico',
        'step2_title': 'Kod HTML', 'step2_desc': 'Wklej ten kod w sekcji <head>.',
        'guide_copy_btn': 'Kopiuj', 'guide_copied': 'Skopiowano!'
    },

    # --- 日本語 (日语) ---
    'ja': {
        'name': '日本語', 'dir': 'ltr', 'recommend': '推奨', 'badge': '人気',
        'seo_title': 'ICO変換ツール', 'seo_desc': 'ファビコン作成。',
        'keywords': 'ico 変換, ファビコン',
        'h1': 'ICO 変換ツール', 'subtitle': 'プロフェッショナルなアイコン作成', 'upload_label': 'アップロード',
        'size_label': 'サイズ', 'btn_submit': 'ダウンロード', 'footer': 'プライバシー保護。', 'error_large': 'ファイルサイズ過大',
        # Guide
        'tab_create': '作成', 'tab_guide': 'ガイド',
        'guide_preview_title': 'プレビュー', 'guide_preview_desc': 'アイコンはブラウザのタブに表示されます。',
        'step1_title': 'アップロード', 'step1_desc': 'favicon.ico をルートディレクトリに配置します。', 'step1_file_path': '/ルート/', 'step1_file_name': 'favicon.ico',
        'step2_title': 'HTMLコード', 'step2_desc': '<head> セクションに貼り付けてください。',
        'guide_copy_btn': 'コピー', 'guide_copied': '完了!'
    },

    # --- 한국어 (韩语) ---
    'ko': {
        'name': '한국어', 'dir': 'ltr', 'recommend': '추천', 'badge': '인기',
        'seo_title': 'ICO 변환기', 'seo_desc': '파비콘 만들기.',
        'keywords': 'ico 변환, 파비콘',
        'h1': 'ICO 변환기', 'subtitle': '전문 파비콘 생성 도구', 'upload_label': '업로드',
        'size_label': '크기', 'btn_submit': '다운로드', 'footer': '개인정보 보호.', 'error_large': '파일이 너무 큽니다',
        # Guide
        'tab_create': '제작', 'tab_guide': '가이드',
        'guide_preview_title': '미리보기', 'guide_preview_desc': '아이콘이 브라우저 탭에 표시됩니다.',
        'step1_title': '업로드', 'step1_desc': 'favicon.ico 파일을 루트 디렉토리에 업로드하세요.', 'step1_file_path': '/루트/', 'step1_file_name': 'favicon.ico',
        'step2_title': 'HTML 코드', 'step2_desc': '<head> 섹션에 코드를 붙여넣으세요.',
        'guide_copy_btn': '복사', 'guide_copied': '완료!'
    },

    # --- Bahasa Indonesia (印尼语) ---
    'id': {
        'name': 'Bahasa Indonesia', 'dir': 'ltr', 'recommend': 'Disarankan', 'badge': 'HOT',
        'seo_title': 'Konverter ICO', 'seo_desc': 'Buat Favicon.',
        'keywords': 'konverter ico, favicon',
        'h1': 'Konverter ICO', 'subtitle': 'Pembuat Favicon', 'upload_label': 'Unggah gambar',
        'size_label': 'Ukuran', 'btn_submit': 'Unduh .ICO', 'footer': 'Privasi dilindungi.', 'error_large': 'File terlalu besar',
        # Guide
        'tab_create': 'Buat', 'tab_guide': 'Panduan',
        'guide_preview_title': 'Pratinjau', 'guide_preview_desc': 'Ikon Anda akan muncul di tab browser.',
        'step1_title': 'Unggah', 'step1_desc': 'Unggah favicon.ico ke direktori root.', 'step1_file_path': '/root/', 'step1_file_name': 'favicon.ico',
        'step2_title': 'Kode HTML', 'step2_desc': 'Tempel kode ini di bagian <head>.',
        'guide_copy_btn': 'Salin', 'guide_copied': 'Disalin!'
    },

    # --- Türkçe (土耳其语) ---
    'tr': {
        'name': 'Türkçe', 'dir': 'ltr', 'recommend': 'Önerilen', 'badge': 'POP',
        'seo_title': 'ICO Dönüştürücü', 'seo_desc': 'Favicon yapma.',
        'keywords': 'ico dönüştürücü, favicon',
        'h1': 'ICO Dönüştürücü', 'subtitle': 'Favicon Oluşturucu', 'upload_label': 'Dosya yükle',
        'size_label': 'Boyut', 'btn_submit': 'İndir', 'footer': 'Gizlilik korumalı.', 'error_large': 'Dosya çok büyük',
        # Guide
        'tab_create': 'Oluştur', 'tab_guide': 'Rehber',
        'guide_preview_title': 'Önizleme', 'guide_preview_desc': 'Simgeniz tarayıcı sekmelerinde görünecektir.',
        'step1_title': 'Yükle', 'step1_desc': 'favicon.ico dosyasını kök dizine yükleyin.', 'step1_file_path': '/kök/', 'step1_file_name': 'favicon.ico',
        'step2_title': 'HTML Kodu', 'step2_desc': 'Bu kodu <head> bölümüne yapıştırın.',
        'guide_copy_btn': 'Kopyala', 'guide_copied': 'Kopyalandı!'
    },

    # --- Tiếng Việt (越南语) ---
    'vi': {
        'name': 'Tiếng Việt', 'dir': 'ltr', 'recommend': 'Đề xuất', 'badge': 'HOT',
        'seo_title': 'Chuyển đổi ICO', 'seo_desc': 'Tạo Favicon.',
        'keywords': 'chuyển đổi ico, favicon',
        'h1': 'Chuyển đổi ICO', 'subtitle': 'Tạo Favicon', 'upload_label': 'Tải lên',
        'size_label': 'Kích thước', 'btn_submit': 'Tải xuống', 'footer': 'Bảo mật riêng tư.', 'error_large': 'Tệp quá lớn',
        # Guide
        'tab_create': 'Tạo', 'tab_guide': 'Hướng dẫn',
        'guide_preview_title': 'Xem trước', 'guide_preview_desc': 'Biểu tượng sẽ xuất hiện trên các tab trình duyệt.',
        'step1_title': 'Tải lên', 'step1_desc': 'Tải tệp favicon.ico lên thư mục gốc.', 'step1_file_path': '/gốc/', 'step1_file_name': 'favicon.ico',
        'step2_title': 'Mã HTML', 'step2_desc': 'Dán mã này vào phần <head>.',
        'guide_copy_btn': 'Sao chép', 'guide_copied': 'Đã sao chép!'
    },

    # --- ไทย (泰语) ---
    'th': {
        'name': 'ไทย', 'dir': 'ltr', 'recommend': 'แนะนำ', 'badge': 'ฮิต',
        'seo_title': 'ตัวแปลง ICO', 'seo_desc': 'สร้าง Favicon.',
        'keywords': 'แปลงไฟล์ ico, favicon',
        'h1': 'ตัวแปลง ICO', 'subtitle': 'สร้าง Favicon', 'upload_label': 'อัปโหลด',
        'size_label': 'ขนาด', 'btn_submit': 'ดาวน์โหลด', 'footer': 'ความเป็นส่วนตัว', 'error_large': 'ไฟล์ใหญ่เกินไป',
        # Guide
        'tab_create': 'สร้าง', 'tab_guide': 'คู่มือ',
        'guide_preview_title': 'ตัวอย่าง', 'guide_preview_desc': 'ไอคอนของคุณจะแสดงในแท็บเบราว์เซอร์',
        'step1_title': 'อัปโหลด', 'step1_desc': 'อัปโหลด favicon.ico ไปยังไดเรกทอรีราก', 'step1_file_path': '/ราก/', 'step1_file_name': 'favicon.ico',
        'step2_title': 'รหัส HTML', 'step2_desc': 'วางรหัสนี้ในส่วน <head>',
        'guide_copy_btn': 'คัดลอก', 'guide_copied': 'คัดลอกแล้ว!'
    },

    # --- हिन्दी (印地语) ---
    'hi': {
        'name': 'हिन्दी', 'dir': 'ltr', 'recommend': 'अनुशंसित', 'badge': 'आम',
        'seo_title': 'ICO कन्वर्टर', 'seo_desc': 'Favicon बनाएं.',
        'keywords': 'ico converter, favicon',
        'h1': 'ICO कन्वर्टर', 'subtitle': 'Favicon जनरेटर', 'upload_label': 'अपलोड करें',
        'size_label': 'आकार', 'btn_submit': 'डाउनलोड करें', 'footer': 'गोपनीयता', 'error_large': 'फ़ाइल बहुत बड़ी है',
        # Guide
        'tab_create': 'बनाएं', 'tab_guide': 'गाइड',
        'guide_preview_title': 'पूर्वावलोकन', 'guide_preview_desc': 'आपका आइकन ब्राउज़र टैब में दिखाई देगा।',
        'step1_title': 'अपलोड', 'step1_desc': 'favicon.ico को रूट डायरेक्टरी में अपलोड करें।', 'step1_file_path': '/रूट/', 'step1_file_name': 'favicon.ico',
        'step2_title': 'HTML कोड', 'step2_desc': 'इस कोड को <head> सेक्शन में पेस्ट करें।',
        'guide_copy_btn': 'कॉपी', 'guide_copied': 'कॉपी किया!'
    },

    # --- Svenska (瑞典语) ---
    'sv': {
        'name': 'Svenska', 'dir': 'ltr', 'recommend': 'Standard', 'badge': 'TOP',
        'seo_title': 'ICO Konverterare', 'seo_desc': 'Skapa Favicon.',
        'keywords': 'ico konverterare, favicon',
        'h1': 'ICO Konverterare', 'subtitle': 'Favicon Generator', 'upload_label': 'Ladda upp',
        'size_label': 'Storlek', 'btn_submit': 'Ladda ner', 'footer': 'Integritetsskyddad.', 'error_large': 'Filen är för stor',
        # Guide
        'tab_create': 'Skapa', 'tab_guide': 'Guide',
        'guide_preview_title': 'Förhandsvisning', 'guide_preview_desc': 'Din ikon kommer att visas i webbläsarflikarna.',
        'step1_title': 'Ladda upp', 'step1_desc': 'Ladda upp favicon.ico till rotkatalogen.', 'step1_file_path': '/rot/', 'step1_file_name': 'favicon.ico',
        'step2_title': 'HTML-kod', 'step2_desc': 'Klistra in denna kod i <head>-sektionen.',
        'guide_copy_btn': 'Kopiera', 'guide_copied': 'Kopierad!'
    },

    # --- Українська (乌克兰语) ---
    'uk': {
        'name': 'Українська', 'dir': 'ltr', 'recommend': 'Стандарт', 'badge': 'ХІТ',
        'seo_title': 'Конвертер ICO', 'seo_desc': 'Створити Favicon.',
        'keywords': 'ico конвертер, favicon',
        'h1': 'Конвертер ICO', 'subtitle': 'Генератор іконок', 'upload_label': 'Завантажити',
        'size_label': 'Розмір', 'btn_submit': 'Завантажити', 'footer': 'Конфіденційність.', 'error_large': 'Файл занадто великий',
        # Guide
        'tab_create': 'Створити', 'tab_guide': 'Інструкція',
        'guide_preview_title': 'Перегляд', 'guide_preview_desc': 'Ваша іконка з\'явиться на вкладках браузера.',
        'step1_title': 'Завантажити', 'step1_desc': 'Завантажте favicon.ico в кореневий каталог.', 'step1_file_path': '/root/', 'step1_file_name': 'favicon.ico',
        'step2_title': 'HTML код', 'step2_desc': 'Вставте цей код у розділ <head>.',
        'guide_copy_btn': 'Копія', 'guide_copied': 'Скопійовано!'
    },

    # --- العربية (阿拉伯语 - RTL) ---
    'ar': {
        'name': 'العربية', 'dir': 'rtl', 'recommend': 'موصى به', 'badge': 'شائع',
        'seo_title': 'محول ICO', 'seo_desc': 'إنشاء أيقونة.',
        'keywords': 'محول ico, favicon',
        'h1': 'محول ICO', 'subtitle': 'مولد أيقونات', 'upload_label': 'رفع صورة',
        'size_label': 'الحجم', 'btn_submit': 'تحميل .ICO', 'footer': 'حماية الخصوصية.', 'error_large': 'الملف كبير جداً',
        # Guide
        'tab_create': 'إنشاء', 'tab_guide': 'دليل',
        'guide_preview_title': 'معاينة', 'guide_preview_desc': 'سيظهر الرمز الخاص بك في علامات تبويب المتصفح.',
        'step1_title': 'رفع', 'step1_desc': 'ارفع favicon.ico إلى الدليل الجذر.', 'step1_file_path': '/جذر/', 'step1_file_name': 'favicon.ico',
        'step2_title': 'كود HTML', 'step2_desc': 'الصق هذا الكود في قسم <head>.',
        'guide_copy_btn': 'نسخ', 'guide_copied': 'تم النسخ!'
    },

    # --- עברית (希伯来语 - RTL) ---
    'he': {
        'name': 'עברית', 'dir': 'rtl', 'recommend': 'מומלץ', 'badge': 'נפוץ',
        'seo_title': 'ממיר ICO', 'seo_desc': 'צור Favicon.',
        'keywords': 'ממיר ico, favicon',
        'h1': 'ממיר ICO', 'subtitle': 'יוצר אייקונים', 'upload_label': 'העלאת תמונה',
        'size_label': 'גודל', 'btn_submit': 'הורד .ICO', 'footer': 'פרטיות מוגנת.', 'error_large': 'קובץ גדול מדי',
        # Guide
        'tab_create': 'צור', 'tab_guide': 'מדריך',
        'guide_preview_title': 'תצוגה מקדימה', 'guide_preview_desc': 'האייקון שלך יופיע בכרטיסיות הדפדפן.',
        'step1_title': 'העלאה', 'step1_desc': 'העלה את favicon.ico לתיקיית השורש.', 'step1_file_path': '/שורש/', 'step1_file_name': 'favicon.ico',
        'step2_title': 'קוד HTML', 'step2_desc': 'הדבק את הקוד הזה בתוך ה-<head>.',
        'guide_copy_btn': 'העתק', 'guide_copied': 'הועתק!'
    }
}

SUPPORTED_LANGS = list(TRANSLATIONS.keys())
DEFAULT_LANG = 'en'

# ==========================================
# 3. 路由逻辑
# ==========================================

def render_index(lang_code):
    if lang_code not in SUPPORTED_LANGS: return redirect(f"/{DEFAULT_LANG}")
    base_url = request.url_root.rstrip('/')
    alternates = [{'lang': l, 'name': TRANSLATIONS[l]['name'], 'href': f"{base_url}/{l}"} for l in SUPPORTED_LANGS]
    return render_template('index.html', t=TRANSLATIONS[lang_code], current_lang=lang_code, alternates=alternates, base_url=base_url)

for lang in SUPPORTED_LANGS:
    app.add_url_rule(f'/{lang}', endpoint=f'view_{lang}', view_func=render_index, defaults={'lang_code': lang})

@app.errorhandler(404)
def page_not_found(e): return redirect(f"/{DEFAULT_LANG}")

@app.route('/')
def root():
    accept_lang = request.headers.get('Accept-Language', '')
    target = DEFAULT_LANG
    if 'zh-CN' in accept_lang: target = 'zh'
    elif 'zh-TW' in accept_lang: target = 'tw'
    else:
        for lang in SUPPORTED_LANGS:
            if lang in accept_lang:
                target = lang
                break
    return redirect(f"/{target}")

@app.route('/generate', methods=['POST'])
def generate_ico():
    if 'file' not in request.files: return "Error", 400
    file = request.files['file']
    if file.filename == '': return "Error", 400
    try:
        size = int(request.form.get('size', '32'))
        file_bytes = file.read()
        if len(file_bytes) == 0: return "Error: Empty file", 400
        input_stream = io.BytesIO(file_bytes)
        img = Image.open(input_stream)
        if img.mode != "RGBA": img = img.convert("RGBA")
        img = img.resize((size, size), Image.Resampling.LANCZOS)
        output_stream = io.BytesIO()
        img.save(output_stream, format='ICO', sizes=[(size, size)])
        output_stream.seek(0)
        return send_file(output_stream, mimetype='image/x-icon', as_attachment=True, download_name='favicon.ico')
    except Exception as e:
        print(f"Error: {str(e)}")
        return "Invalid image file", 500

@app.route('/sitemap.xml')
def sitemap():
    base_url = request.url_root.rstrip('/')
    urls = []
    today = datetime.date.today().isoformat()
    for lang in SUPPORTED_LANGS:
        urls.append(f"""<url><loc>{base_url}/{lang}</loc><lastmod>{today}</lastmod><changefreq>weekly</changefreq><priority>{'1.0' if lang == 'en' else '0.8'}</priority></url>""")
    xml = f"""<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{''.join(urls)}</urlset>"""
    return Response(xml, mimetype="application/xml")

@app.route('/robots.txt')
def robots():
    base_url = request.url_root.rstrip('/')
    lines = ["User-agent: *", "Allow: /", "Disallow: /generate", f"Sitemap: {base_url}/sitemap.xml"]
    return Response("\n".join(lines), mimetype="text/plain")

@app.route('/favicon.ico')
def favicon():
    return send_file('../favicon.ico', mimetype='image/vnd.microsoft.icon')
