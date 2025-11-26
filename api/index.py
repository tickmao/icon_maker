import datetime
import io
import os

from flask import (Flask, Response, redirect, render_template, request,
                   send_file)
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from PIL import Image, ImageFilter

app = Flask(__name__, template_folder='../templates')
app.secret_key = os.environ.get('SECRET_KEY', 'global_ico_ultimate_final_v_full_lang')
app.url_map.strict_slashes = False
app.config['MAX_CONTENT_LENGTH'] = 4.5 * 1024 * 1024

# ==========================================
# 1. 安全防护
# ==========================================
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["300 per day", "60 per hour"],
    storage_uri="memory://"
)

# ==========================================
# 2. 图像处理：智能描边
# ==========================================
def add_smart_glow(img):
    if img.mode != 'RGBA': return img.convert('RGBA')
    r, g, b, a = img.split()
    if a.getextrema()[0] > 250: return img
    glow = Image.new('RGBA', img.size, (255, 255, 255, 0))
    for offset in [(1,0), (-1,0), (0,1), (0,-1)]:
        temp = Image.new('RGBA', img.size, (0,0,0,0))
        temp.paste((255, 255, 255, 80), offset, mask=a)
        glow = Image.alpha_composite(glow, temp)
    return Image.alpha_composite(glow, img)

# ==========================================
# 3. 终极全球语言包 (22语言全量翻译 - 无省略)
# ==========================================
TRANSLATIONS = {
    # 1. English
    'en': {
        'name': 'English', 'dir': 'ltr', 'recommend': 'Recommended', 'badge': 'HOT',
        'seo_title': 'Free Online ICO Converter - Create Transparent Favicon',
        'seo_desc': 'Best free online ICO converter. Convert PNG, JPG to ICO format instantly.',
        'keywords': 'ico converter, favicon generator',
        'h1': 'ICO Converter', 'subtitle': 'Professional Favicon Generator',
        'upload_label': 'Click to upload or Drag image', 'size_label': 'Target Size', 'btn_submit': 'Generate ICO',
        'footer': 'Securely processed. Privacy protected.', 'error_large': 'File too large',
        'tab_create': 'Create', 'tab_guide': 'Guide',
        'guide_preview_title': 'Visual Preview', 'guide_preview_desc': 'Your icon will be displayed in browser tabs.',
        'step1_title': 'Upload to Server', 'step1_desc': 'Upload favicon.ico to your website root directory.', 'step1_file_path': '/root/', 'step1_file_name': 'favicon.ico',
        'step2_title': 'Update HTML', 'step2_desc': 'Paste this code into the <head> section.',
        'guide_copy_btn': 'Copy', 'guide_copied': 'Copied!',
        'faq_title': 'FAQ', 'share_title': 'Share', 'share_modal_title': 'Share with Friends', 'share_copy_label': 'Copy Link', 'share_msg': 'Check out this ICO converter:',
        'faq_list': [
            {'q': 'What is a Favicon?', 'a': 'A small icon displayed in browser tabs.'},
            {'q': 'Transparent backgrounds?', 'a': 'Yes, we preserve transparency.'},
            {'q': 'Best size?', 'a': '32x32 is standard for desktop.'},
            {'q': 'Is it safe?', 'a': 'Yes, images are not saved.'}
        ]
    },
    # 2. Simplified Chinese
    'zh': {
        'name': '简体中文', 'dir': 'ltr', 'recommend': '推荐', 'badge': '常用',
        'seo_title': '在线 ICO 图标生成器 - 免费制作透明 Favicon',
        'seo_desc': '免费在线图片转 ICO 工具。支持透明背景。',
        'keywords': 'ICO生成器, favicon制作',
        'h1': 'ICO 图标生成器', 'subtitle': '一键生成透明背景图标',
        'upload_label': '点击选择 或 拖拽图片', 'size_label': '目标尺寸', 'btn_submit': '生成并下载 .ICO',
        'footer': '数据安全保护，不保存任何图片。', 'error_large': '文件过大',
        'tab_create': '制作图标', 'tab_guide': '使用指南',
        'guide_preview_title': '效果预览', 'guide_preview_desc': '图标将显示在浏览器标签页中。',
        'step1_title': '上传至服务器', 'step1_desc': '将 favicon.ico 上传到网站根目录。', 'step1_file_path': '/根目录/', 'step1_file_name': 'favicon.ico',
        'step2_title': '引入 HTML', 'step2_desc': '将代码粘贴到 <head> 标签之间。',
        'guide_copy_btn': '复制', 'guide_copied': '已复制!',
        'faq_title': '常见问题', 'share_title': '分享工具', 'share_modal_title': '分享给朋友', 'share_copy_label': '复制链接', 'share_msg': '推荐这个好用的 ICO 工具：',
        'faq_list': [
            {'q': '什么是 Favicon？', 'a': '浏览器标签页上的小图标。'},
            {'q': '支持透明吗？', 'a': '支持，完美保留透明背景。'},
            {'q': '最佳尺寸？', 'a': 'PC 端推荐 32x32。'},
            {'q': '安全吗？', 'a': '绝对安全，不保存文件。'}
        ]
    },
    # 3. Traditional Chinese
    'tw': {
        'name': '繁體中文', 'dir': 'ltr', 'recommend': '推薦', 'badge': '常用',
        'seo_title': '線上 ICO 圖示產生器 - 製作透明 Favicon',
        'seo_desc': '免費線上圖片轉 ICO 工具。支援透明背景。',
        'keywords': 'ICO產生器, favicon製作',
        'h1': 'ICO 圖示產生器', 'subtitle': '一鍵生成透明背景圖示',
        'upload_label': '點擊選擇 或 拖曳圖片', 'size_label': '目標尺寸', 'btn_submit': '產生並下載 .ICO',
        'footer': '資料安全保護，不保存任何圖片。', 'error_large': '檔案過大',
        'tab_create': '製作圖示', 'tab_guide': '使用指南',
        'guide_preview_title': '效果預覽', 'guide_preview_desc': '圖示將顯示在瀏覽器分頁上。',
        'step1_title': '上傳至伺服器', 'step1_desc': '將 favicon.ico 上傳到網站根目錄。', 'step1_file_path': '/根目錄/', 'step1_file_name': 'favicon.ico',
        'step2_title': '引入 HTML', 'step2_desc': '將程式碼貼到 <head> 標籤之間。',
        'guide_copy_btn': '複製', 'guide_copied': '已複製!',
        'faq_title': '常見問題', 'share_title': '分享工具', 'share_modal_title': '分享給朋友', 'share_copy_label': '複製連結', 'share_msg': '推薦這個好用的 ICO 工具：',
        'faq_list': [
            {'q': '什麼是 Favicon？', 'a': '瀏覽器分頁上的小圖示。'},
            {'q': '支援透明嗎？', 'a': '支援，完美保留透明背景。'},
            {'q': '最佳尺寸？', 'a': 'PC 端推薦 32x32。'},
            {'q': '安全嗎？', 'a': '絕對安全，不儲存檔案。'}
        ]
    },
    # 4. Spanish
    'es': {
        'name': 'Español', 'dir': 'ltr', 'recommend': 'Recomendado', 'badge': 'HOT',
        'seo_title': 'Convertidor ICO Online', 'seo_desc': 'Imágenes a ICO gratis.', 'keywords': 'convertidor ico',
        'h1': 'Convertidor ICO', 'subtitle': 'Generador de Favicon',
        'upload_label': 'Clic para subir', 'size_label': 'Tamaño', 'btn_submit': 'Generar .ICO',
        'footer': 'Privacidad protegida.', 'error_large': 'Archivo grande',
        'tab_create': 'Crear', 'tab_guide': 'Guía',
        'guide_preview_title': 'Vista Previa', 'guide_preview_desc': 'Su icono aparecerá en las pestañas.',
        'step1_title': 'Subir al Servidor', 'step1_desc': 'Sube favicon.ico al directorio raíz.', 'step1_file_path': '/raíz/', 'step1_file_name': 'favicon.ico',
        'step2_title': 'HTML', 'step2_desc': 'Pega en la sección <head>.',
        'guide_copy_btn': 'Copiar', 'guide_copied': '¡Copiado!',
        'faq_title': 'Preguntas', 'share_title': 'Compartir', 'share_modal_title': 'Compartir', 'share_copy_label': 'Copiar', 'share_msg': 'Mira este convertidor ICO:',
        'faq_list': [
            {'q': '¿Qué es Favicon?', 'a': 'Icono en la pestaña del navegador.'},
            {'q': '¿Transparencia?', 'a': 'Sí, la mantenemos.'},
            {'q': '¿Tamaño?', 'a': '32x32 es estándar.'},
            {'q': '¿Seguro?', 'a': 'Sí, no guardamos imágenes.'}
        ]
    },
    # 5. French
    'fr': {
        'name': 'Français', 'dir': 'ltr', 'recommend': 'Recommandé', 'badge': 'TOP',
        'seo_title': 'Convertisseur ICO', 'seo_desc': 'Image en ICO gratuit.', 'keywords': 'convertisseur ico',
        'h1': 'Convertisseur ICO', 'subtitle': 'Générateur de Favicon',
        'upload_label': 'Uploader image', 'size_label': 'Taille', 'btn_submit': 'Générer .ICO',
        'footer': 'Confidentialité.', 'error_large': 'Fichier volumineux',
        'tab_create': 'Créer', 'tab_guide': 'Guide',
        'guide_preview_title': 'Aperçu', 'guide_preview_desc': 'Icône dans les onglets.',
        'step1_title': 'Mettre sur Serveur', 'step1_desc': 'Mettez favicon.ico à la racine.', 'step1_file_path': '/racine/', 'step1_file_name': 'favicon.ico',
        'step2_title': 'HTML', 'step2_desc': 'Collez dans <head>.',
        'guide_copy_btn': 'Copier', 'guide_copied': 'Copié!',
        'faq_title': 'FAQ', 'share_title': 'Partager', 'share_modal_title': 'Partager', 'share_copy_label': 'Copier', 'share_msg': 'Convertisseur ICO génial :',
        'faq_list': [
            {'q': 'C\'est quoi Favicon ?', 'a': 'Icône d\'onglet.'},
            {'q': 'Transparence ?', 'a': 'Oui, supportée.'},
            {'q': 'Taille ?', 'a': '32x32 standard.'},
            {'q': 'Sécurisé ?', 'a': 'Oui, pas de stockage.'}
        ]
    },
    # 6. German
    'de': {
        'name': 'Deutsch', 'dir': 'ltr', 'recommend': 'Empfohlen', 'badge': 'TOP',
        'seo_title': 'ICO Konverter', 'seo_desc': 'Bild zu ICO.', 'keywords': 'ico konverter',
        'h1': 'ICO Konverter', 'subtitle': 'Favicon-Generator',
        'upload_label': 'Bild hochladen', 'size_label': 'Größe', 'btn_submit': 'Herunterladen',
        'footer': 'Datenschutz.', 'error_large': 'Zu groß',
        'tab_create': 'Erstellen', 'tab_guide': 'Anleitung',
        'guide_preview_title': 'Vorschau', 'guide_preview_desc': 'Icon im Browser-Tab.',
        'step1_title': 'Hochladen', 'step1_desc': 'Laden Sie favicon.ico ins Stammverzeichnis.', 'step1_file_path': '/root/', 'step1_file_name': 'favicon.ico',
        'step2_title': 'HTML', 'step2_desc': 'In <head> einfügen.',
        'guide_copy_btn': 'Kopieren', 'guide_copied': 'Kopiert!',
        'faq_title': 'FAQ', 'share_title': 'Teilen', 'share_modal_title': 'Teilen', 'share_copy_label': 'Kopieren', 'share_msg': 'Toller ICO Konverter:',
        'faq_list': [
            {'q': 'Was ist Favicon?', 'a': 'Symbol im Tab.'},
            {'q': 'Transparenz?', 'a': 'Ja.'},
            {'q': 'Größe?', 'a': '32x32 Standard.'},
            {'q': 'Sicher?', 'a': 'Ja, keine Speicherung.'}
        ]
    },
    # 7. Japanese
    'ja': {
        'name': '日本語', 'dir': 'ltr', 'recommend': '推奨', 'badge': '人気',
        'seo_title': 'ICO変換ツール', 'seo_desc': 'ファビコン作成。', 'keywords': 'ico 変換',
        'h1': 'ICO 変換ツール', 'subtitle': 'プロフェッショナル作成',
        'upload_label': 'アップロード', 'size_label': 'サイズ', 'btn_submit': 'ダウンロード',
        'footer': 'プライバシー保護。', 'error_large': 'ファイル過大',
        'tab_create': '作成', 'tab_guide': 'ガイド',
        'guide_preview_title': 'プレビュー', 'guide_preview_desc': 'ブラウザのタブに表示されます。',
        'step1_title': 'アップロード', 'step1_desc': 'ルートディレクトリに配置。', 'step1_file_path': '/ルート/', 'step1_file_name': 'favicon.ico',
        'step2_title': 'HTML', 'step2_desc': '<head> 内に貼り付け。',
        'guide_copy_btn': 'コピー', 'guide_copied': '完了!',
        'faq_title': 'FAQ', 'share_title': 'シェア', 'share_modal_title': 'シェアする', 'share_copy_label': 'コピー', 'share_msg': '便利なICO変換ツール:',
        'faq_list': [
            {'q': 'Faviconとは？', 'a': 'タブのアイコンです。'},
            {'q': '透過？', 'a': 'はい、対応しています。'},
            {'q': 'サイズ？', 'a': '32x32が標準です。'},
            {'q': '安全？', 'a': 'はい、保存されません。'}
        ]
    },
    # 8. Korean
    'ko': {
        'name': '한국어', 'dir': 'ltr', 'recommend': '추천', 'badge': '인기',
        'seo_title': 'ICO 변환기', 'seo_desc': '파비콘 만들기.', 'keywords': 'ico 변환',
        'h1': 'ICO 변환기', 'subtitle': '전문 파비콘 도구',
        'upload_label': '업로드', 'size_label': '크기', 'btn_submit': '다운로드',
        'footer': '개인정보 보호.', 'error_large': '파일 큼',
        'tab_create': '제작', 'tab_guide': '가이드',
        'guide_preview_title': '미리보기', 'guide_preview_desc': '브라우저 탭에 표시됩니다.',
        'step1_title': '업로드', 'step1_desc': '루트 디렉토리에 업로드.', 'step1_file_path': '/루트/', 'step1_file_name': 'favicon.ico',
        'step2_title': 'HTML', 'step2_desc': '<head> 섹션에 붙여넣기.',
        'guide_copy_btn': '복사', 'guide_copied': '완료!',
        'faq_title': 'FAQ', 'share_title': '공유', 'share_modal_title': '공유하기', 'share_copy_label': '링크 복사', 'share_msg': 'ICO 변환기 추천:',
        'faq_list': [
            {'q': '파비콘이란?', 'a': '탭 아이콘입니다.'},
            {'q': '투명?', 'a': '네, 지원합니다.'},
            {'q': '사이즈?', 'a': '32x32 표준.'},
            {'q': '안전?', 'a': '네, 저장 안 함.'}
        ]
    },
    # 9. Russian
    'ru': {
        'name': 'Русский', 'dir': 'ltr', 'recommend': 'Стандарт', 'badge': 'ХИТ',
        'seo_title': 'Конвертер ICO', 'seo_desc': 'Создать Favicon.', 'keywords': 'ico конвертер',
        'h1': 'Конвертер ICO', 'subtitle': 'Генератор иконок',
        'upload_label': 'Загрузить', 'size_label': 'Размер', 'btn_submit': 'Скачать',
        'footer': 'Конфиденциальность.', 'error_large': 'Файл большой',
        'tab_create': 'Создать', 'tab_guide': 'Гид',
        'guide_preview_title': 'Предпросмотр', 'guide_preview_desc': 'Иконка во вкладках.',
        'step1_title': 'Загрузка', 'step1_desc': 'В корень сайта.', 'step1_file_path': '/root/', 'step1_file_name': 'favicon.ico',
        'step2_title': 'HTML', 'step2_desc': 'Вставьте в <head>.',
        'guide_copy_btn': 'Копия', 'guide_copied': 'Готово!',
        'faq_title': 'Вопросы', 'share_title': 'Поделиться', 'share_modal_title': 'Поделиться', 'share_copy_label': 'Копировать', 'share_msg': 'ICO конвертер:',
        'faq_list': [
            {'q': 'Что это?', 'a': 'Иконка сайта.'},
            {'q': 'Прозрачность?', 'a': 'Да.'},
            {'q': 'Размер?', 'a': '32x32.'},
            {'q': 'Безопасно?', 'a': 'Да.'}
        ]
    },
    # 10. Italian
    'it': {
        'name': 'Italiano', 'dir': 'ltr', 'recommend': 'Consigliato', 'badge': 'TOP',
        'seo_title': 'Convertitore ICO', 'seo_desc': 'Crea Favicon.', 'keywords': 'convertitore ico',
        'h1': 'Convertitore ICO', 'subtitle': 'Generatore Favicon',
        'upload_label': 'Carica', 'size_label': 'Dimensione', 'btn_submit': 'Scarica',
        'footer': 'Privacy protetta.', 'error_large': 'Errore file',
        'tab_create': 'Crea', 'tab_guide': 'Guida',
        'guide_preview_title': 'Anteprima', 'guide_preview_desc': 'Icona nei tab.',
        'step1_title': 'Carica', 'step1_desc': 'Nella root.', 'step1_file_path': '/root/', 'step1_file_name': 'favicon.ico',
        'step2_title': 'HTML', 'step2_desc': 'Incolla in <head>.',
        'guide_copy_btn': 'Copia', 'guide_copied': 'Fatto!',
        'faq_title': 'FAQ', 'share_title': 'Condividi', 'share_modal_title': 'Condividi', 'share_copy_label': 'Copia', 'share_msg': 'Convertitore ICO:',
        'faq_list': [{'q': 'Cos\'è?', 'a': 'Icona del browser.'}, {'q': 'Trasparenza?', 'a': 'Sì.'}, {'q': 'Misura?', 'a': '32x32.'}, {'q': 'Sicuro?', 'a': 'Sì.'}]
    },
    # 11. Portuguese
    'pt': {
        'name': 'Português', 'dir': 'ltr', 'recommend': 'Recomendado', 'badge': 'HOT',
        'seo_title': 'Conversor ICO', 'seo_desc': 'Criar Favicon.', 'keywords': 'conversor ico',
        'h1': 'Conversor ICO', 'subtitle': 'Gerador Favicon',
        'upload_label': 'Subir', 'size_label': 'Tamanho', 'btn_submit': 'Baixar',
        'footer': 'Seguro.', 'error_large': 'Erro',
        'tab_create': 'Criar', 'tab_guide': 'Guia',
        'guide_preview_title': 'Prévia', 'guide_preview_desc': 'Ícone nas abas.',
        'step1_title': 'Upload', 'step1_desc': 'Para a raiz.', 'step1_file_path': '/raiz/', 'step1_file_name': 'favicon.ico',
        'step2_title': 'HTML', 'step2_desc': 'No <head>.',
        'guide_copy_btn': 'Copiar', 'guide_copied': 'Copiado!',
        'faq_title': 'FAQ', 'share_title': 'Compartilhar', 'share_modal_title': 'Compartilhar', 'share_copy_label': 'Copiar', 'share_msg': 'Conversor ICO:',
        'faq_list': [{'q': 'O que é?', 'a': 'Ícone de aba.'}, {'q': 'Transparência?', 'a': 'Sim.'}, {'q': 'Tamanho?', 'a': '32x32.'}, {'q': 'Seguro?', 'a': 'Sim.'}]
    },
    # 12. Dutch
    'nl': {
        'name': 'Nederlands', 'dir': 'ltr', 'recommend': 'Aanbevolen', 'badge': 'TOP',
        'seo_title': 'ICO Converter', 'seo_desc': 'Favicon maken.', 'keywords': 'ico converter',
        'h1': 'ICO Converter', 'subtitle': 'Favicon Generator',
        'upload_label': 'Uploaden', 'size_label': 'Grootte', 'btn_submit': 'Downloaden',
        'footer': 'Privacy.', 'error_large': 'Fout',
        'tab_create': 'Maken', 'tab_guide': 'Gids',
        'guide_preview_title': 'Voorbeeld', 'guide_preview_desc': 'Icoon in tabs.',
        'step1_title': 'Uploaden', 'step1_desc': 'Naar root.', 'step1_file_path': '/root/', 'step1_file_name': 'favicon.ico',
        'step2_title': 'HTML', 'step2_desc': 'In <head>.',
        'guide_copy_btn': 'Kopie', 'guide_copied': 'Klaar!',
        'faq_title': 'FAQ', 'share_title': 'Delen', 'share_modal_title': 'Delen', 'share_copy_label': 'Kopiëren', 'share_msg': 'Check ICO Converter:',
        'faq_list': [{'q': 'Wat is het?', 'a': 'Tab icoon.'}, {'q': 'Transparant?', 'a': 'Ja.'}, {'q': 'Grootte?', 'a': '32x32.'}, {'q': 'Veilig?', 'a': 'Ja.'}]
    },
    # 13. Polish
    'pl': {
        'name': 'Polski', 'dir': 'ltr', 'recommend': 'Zalecane', 'badge': 'HIT',
        'seo_title': 'Konwerter ICO', 'seo_desc': 'Generator Favicon.', 'keywords': 'konwerter ico',
        'h1': 'Konwerter ICO', 'subtitle': 'Generator Favicon',
        'upload_label': 'Prześlij', 'size_label': 'Rozmiar', 'btn_submit': 'Pobierz',
        'footer': 'Prywatność.', 'error_large': 'Błąd',
        'tab_create': 'Stwórz', 'tab_guide': 'Info',
        'guide_preview_title': 'Podgląd', 'guide_preview_desc': 'Ikona w kartach.',
        'step1_title': 'Prześlij', 'step1_desc': 'Do katalogu głównego.', 'step1_file_path': '/root/', 'step1_file_name': 'favicon.ico',
        'step2_title': 'HTML', 'step2_desc': 'W <head>.',
        'guide_copy_btn': 'Kopiuj', 'guide_copied': 'Gotowe!',
        'faq_title': 'FAQ', 'share_title': 'Udostępnij', 'share_modal_title': 'Udostępnij', 'share_copy_label': 'Kopiuj', 'share_msg': 'Konwerter ICO:',
        'faq_list': [{'q': 'Co to?', 'a': 'Ikona strony.'}, {'q': 'Przezroczyste?', 'a': 'Tak.'}, {'q': 'Rozmiar?', 'a': '32x32.'}, {'q': 'Bezpieczne?', 'a': 'Tak.'}]
    },
    # 14. Swedish
    'sv': {
        'name': 'Svenska', 'dir': 'ltr', 'recommend': 'Standard', 'badge': 'TOP',
        'seo_title': 'ICO Konverterare', 'seo_desc': 'Skapa Favicon.', 'keywords': 'ico konverterare',
        'h1': 'ICO Konverterare', 'subtitle': 'Favicon Generator',
        'upload_label': 'Ladda upp', 'size_label': 'Storlek', 'btn_submit': 'Ladda ner',
        'footer': 'Säker.', 'error_large': 'Fel',
        'tab_create': 'Skapa', 'tab_guide': 'Guide',
        'guide_preview_title': 'Förhandsvisning', 'guide_preview_desc': 'Ikon i flikar.',
        'step1_title': 'Ladda upp', 'step1_desc': 'Till rot.', 'step1_file_path': '/rot/', 'step1_file_name': 'favicon.ico',
        'step2_title': 'HTML', 'step2_desc': 'I <head>.',
        'guide_copy_btn': 'Kopiera', 'guide_copied': 'Klart!',
        'faq_title': 'FAQ', 'share_title': 'Dela', 'share_modal_title': 'Dela', 'share_copy_label': 'Kopiera', 'share_msg': 'ICO Konverterare:',
        'faq_list': [{'q': 'Vad är det?', 'a': 'Webbplatsikon.'}, {'q': 'Genomskinlig?', 'a': 'Ja.'}, {'q': 'Storlek?', 'a': '32x32.'}, {'q': 'Säkert?', 'a': 'Ja.'}]
    },
    # 15. Ukrainian
    'uk': {
        'name': 'Українська', 'dir': 'ltr', 'recommend': 'Стандарт', 'badge': 'ХІТ',
        'seo_title': 'Конвертер ICO', 'seo_desc': 'Створити Favicon.', 'keywords': 'ico конвертер',
        'h1': 'Конвертер ICO', 'subtitle': 'Генератор іконок',
        'upload_label': 'Завантажити', 'size_label': 'Розмір', 'btn_submit': 'Завантажити',
        'footer': 'Конфіденційність.', 'error_large': 'Помилка',
        'tab_create': 'Створити', 'tab_guide': 'Інструкція',
        'guide_preview_title': 'Перегляд', 'guide_preview_desc': 'Іконка у вкладках.',
        'step1_title': 'Завантаження', 'step1_desc': 'У корінь.', 'step1_file_path': '/root/', 'step1_file_name': 'favicon.ico',
        'step2_title': 'HTML', 'step2_desc': 'У <head>.',
        'guide_copy_btn': 'Копія', 'guide_copied': 'Готово!',
        'faq_title': 'FAQ', 'share_title': 'Поділитися', 'share_modal_title': 'Поділитися', 'share_copy_label': 'Копія', 'share_msg': 'ICO конвертер:',
        'faq_list': [{'q': 'Що це?', 'a': 'Іконка сайту.'}, {'q': 'Прозорість?', 'a': 'Так.'}, {'q': 'Розмір?', 'a': '32x32.'}, {'q': 'Безпечно?', 'a': 'Так.'}]
    },
    # 16. Indonesian
    'id': {
        'name': 'Bahasa Indonesia', 'dir': 'ltr', 'recommend': 'Disarankan', 'badge': 'HOT',
        'seo_title': 'Konverter ICO', 'seo_desc': 'Buat Favicon.', 'keywords': 'konverter ico',
        'h1': 'Konverter ICO', 'subtitle': 'Pembuat Favicon',
        'upload_label': 'Unggah', 'size_label': 'Ukuran', 'btn_submit': 'Unduh',
        'footer': 'Aman.', 'error_large': 'Error',
        'tab_create': 'Buat', 'tab_guide': 'Panduan',
        'guide_preview_title': 'Pratinjau', 'guide_preview_desc': 'Ikon di tab.',
        'step1_title': 'Unggah', 'step1_desc': 'Ke root.', 'step1_file_path': '/root/', 'step1_file_name': 'favicon.ico',
        'step2_title': 'HTML', 'step2_desc': 'Di <head>.',
        'guide_copy_btn': 'Salin', 'guide_copied': 'Disalin!',
        'faq_title': 'FAQ', 'share_title': 'Bagikan', 'share_modal_title': 'Bagikan', 'share_copy_label': 'Salin', 'share_msg': 'Konverter ICO:',
        'faq_list': [{'q': 'Apa itu?', 'a': 'Ikon web.'}, {'q': 'Transparan?', 'a': 'Ya.'}, {'q': 'Ukuran?', 'a': '32x32.'}, {'q': 'Aman?', 'a': 'Ya.'}]
    },
    # 17. Turkish
    'tr': {
        'name': 'Türkçe', 'dir': 'ltr', 'recommend': 'Önerilen', 'badge': 'POP',
        'seo_title': 'ICO Dönüştürücü', 'seo_desc': 'Favicon yapma.', 'keywords': 'ico dönüştürücü',
        'h1': 'ICO Dönüştürücü', 'subtitle': 'Favicon Oluşturucu',
        'upload_label': 'Yükle', 'size_label': 'Boyut', 'btn_submit': 'İndir',
        'footer': 'Gizlilik.', 'error_large': 'Hata',
        'tab_create': 'Oluştur', 'tab_guide': 'Rehber',
        'guide_preview_title': 'Önizleme', 'guide_preview_desc': 'Sekmelerde simge.',
        'step1_title': 'Yükle', 'step1_desc': 'Kök dizine.', 'step1_file_path': '/kök/', 'step1_file_name': 'favicon.ico',
        'step2_title': 'HTML', 'step2_desc': '<head>\'e.',
        'guide_copy_btn': 'Kopyala', 'guide_copied': 'Tamam!',
        'faq_title': 'SSS', 'share_title': 'Paylaş', 'share_modal_title': 'Paylaş', 'share_copy_label': 'Kopyala', 'share_msg': 'ICO Dönüştürücü:',
        'faq_list': [{'q': 'Nedir?', 'a': 'Site simgesi.'}, {'q': 'Şeffaflık?', 'a': 'Evet.'}, {'q': 'Boyut?', 'a': '32x32.'}, {'q': 'Güvenli mi?', 'a': 'Evet.'}]
    },
    # 18. Vietnamese
    'vi': {
        'name': 'Tiếng Việt', 'dir': 'ltr', 'recommend': 'Đề xuất', 'badge': 'HOT',
        'seo_title': 'Chuyển đổi ICO', 'seo_desc': 'Tạo Favicon.', 'keywords': 'chuyển đổi ico',
        'h1': 'Chuyển đổi ICO', 'subtitle': 'Tạo Favicon',
        'upload_label': 'Tải lên', 'size_label': 'Kích thước', 'btn_submit': 'Tải xuống',
        'footer': 'Bảo mật.', 'error_large': 'Lỗi',
        'tab_create': 'Tạo', 'tab_guide': 'H.dẫn',
        'guide_preview_title': 'Xem trước', 'guide_preview_desc': 'Biểu tượng trên tab.',
        'step1_title': 'Tải lên', 'step1_desc': 'Vào thư mục gốc.', 'step1_file_path': '/gốc/', 'step1_file_name': 'favicon.ico',
        'step2_title': 'HTML', 'step2_desc': 'Vào <head>.',
        'guide_copy_btn': 'Sao chép', 'guide_copied': 'Xong!',
        'faq_title': 'Hỏi đáp', 'share_title': 'Chia sẻ', 'share_modal_title': 'Chia sẻ', 'share_copy_label': 'Sao chép', 'share_msg': 'Chuyển đổi ICO:',
        'faq_list': [{'q': 'Là gì?', 'a': 'Biểu tượng web.'}, {'q': 'Trong suốt?', 'a': 'Có.'}, {'q': 'Kích thước?', 'a': '32x32.'}, {'q': 'An toàn?', 'a': 'Có.'}]
    },
    # 19. Thai
    'th': {
        'name': 'ไทย', 'dir': 'ltr', 'recommend': 'แนะนำ', 'badge': 'ฮิต',
        'seo_title': 'ตัวแปลง ICO', 'seo_desc': 'สร้าง Favicon.', 'keywords': 'แปลงไฟล์ ico',
        'h1': 'ตัวแปลง ICO', 'subtitle': 'สร้าง Favicon',
        'upload_label': 'อัปโหลด', 'size_label': 'ขนาด', 'btn_submit': 'ดาวน์โหลด',
        'footer': 'ปลอดภัย', 'error_large': 'ไฟล์ใหญ่',
        'tab_create': 'สร้าง', 'tab_guide': 'คู่มือ',
        'guide_preview_title': 'ตัวอย่าง', 'guide_preview_desc': 'ไอคอนบนแท็บ',
        'step1_title': 'อัปโหลด', 'step1_desc': 'ไปที่ราก', 'step1_file_path': '/ราก/', 'step1_file_name': 'favicon.ico',
        'step2_title': 'HTML', 'step2_desc': 'ใน <head>',
        'guide_copy_btn': 'คัดลอก', 'guide_copied': 'สำเร็จ!',
        'faq_title': 'FAQ', 'share_title': 'แชร์', 'share_modal_title': 'แชร์', 'share_copy_label': 'คัดลอก', 'share_msg': 'ตัวแปลง ICO:',
        'faq_list': [{'q': 'คืออะไร?', 'a': 'ไอคอนเว็บ'}, {'q': 'โปร่งใส?', 'a': 'ใช่'}, {'q': 'ขนาด?', 'a': '32x32'}, {'q': 'ปลอดภัย?', 'a': 'ใช่'}]
    },
    # 20. Hindi
    'hi': {
        'name': 'हिन्दी', 'dir': 'ltr', 'recommend': 'अनुशंसित', 'badge': 'आम',
        'seo_title': 'ICO कन्वर्टर', 'seo_desc': 'Favicon बनाएं.', 'keywords': 'ico converter',
        'h1': 'ICO कन्वर्टर', 'subtitle': 'Favicon जनरेटर',
        'upload_label': 'अपलोड', 'size_label': 'आकार', 'btn_submit': 'डाउनलोड',
        'footer': 'सुरक्षित', 'error_large': 'बड़ी फ़ाइल',
        'tab_create': 'बनाएं', 'tab_guide': 'गाइड',
        'guide_preview_title': 'पूर्वावलोकन', 'guide_preview_desc': 'टैब में आइकन।',
        'step1_title': 'अपलोड', 'step1_desc': 'रूट में।', 'step1_file_path': '/रूट/', 'step1_file_name': 'favicon.ico',
        'step2_title': 'HTML', 'step2_desc': '<head> में।',
        'guide_copy_btn': 'कॉपी', 'guide_copied': 'हो गया!',
        'faq_title': 'FAQ', 'share_title': 'साझा', 'share_modal_title': 'साझा करें', 'share_copy_label': 'कॉपी', 'share_msg': 'ICO कन्वर्टर:',
        'faq_list': [{'q': 'क्या है?', 'a': 'वेब आइकन।'}, {'q': 'पारदर्शी?', 'a': 'हाँ।'}, {'q': 'आकार?', 'a': '32x32'}, {'q': 'सुरक्षित?', 'a': 'हाँ।'}]
    },
    # 21. Arabic
    'ar': {
        'name': 'العربية', 'dir': 'rtl', 'recommend': 'موصى به', 'badge': 'شائع',
        'seo_title': 'محول ICO', 'seo_desc': 'إنشاء أيقونة.', 'keywords': 'محول ico',
        'h1': 'محول ICO', 'subtitle': 'مولد أيقونات',
        'upload_label': 'رفع', 'size_label': 'الحجم', 'btn_submit': 'تحميل',
        'footer': 'آمن.', 'error_large': 'خطأ',
        'tab_create': 'إنشاء', 'tab_guide': 'دليل',
        'guide_preview_title': 'معاينة', 'guide_preview_desc': 'أيقونة في التبويب.',
        'step1_title': 'رفع', 'step1_desc': 'للجذر.', 'step1_file_path': '/جذر/', 'step1_file_name': 'favicon.ico',
        'step2_title': 'HTML', 'step2_desc': 'في <head>.',
        'guide_copy_btn': 'نسخ', 'guide_copied': 'تم!',
        'faq_title': 'أسئلة', 'share_title': 'مشاركة', 'share_modal_title': 'مشاركة', 'share_copy_label': 'نسخ', 'share_msg': 'محول ICO:',
        'faq_list': [{'q': 'ما هو؟', 'a': 'أيقونة الموقع.'}, {'q': 'شفاف؟', 'a': 'نعم.'}, {'q': 'الحجم؟', 'a': '32x32'}, {'q': 'آمن؟', 'a': 'نعم.'}]
    },
    # 22. Hebrew
    'he': {
        'name': 'עברית', 'dir': 'rtl', 'recommend': 'מומלץ', 'badge': 'נפוץ',
        'seo_title': 'ממיר ICO', 'seo_desc': 'צור Favicon.', 'keywords': 'ממיר ico',
        'h1': 'ממיר ICO', 'subtitle': 'יוצר אייקונים',
        'upload_label': 'העלאה', 'size_label': 'גודל', 'btn_submit': 'הורד',
        'footer': 'פרטיות.', 'error_large': 'שגיאה',
        'tab_create': 'צור', 'tab_guide': 'מדריך',
        'guide_preview_title': 'תצוגה', 'guide_preview_desc': 'אייקון בכרטיסייה.',
        'step1_title': 'העלאה', 'step1_desc': 'לשורש.', 'step1_file_path': '/שורש/', 'step1_file_name': 'favicon.ico',
        'step2_title': 'HTML', 'step2_desc': 'ב-<head>.',
        'guide_copy_btn': 'העתק', 'guide_copied': 'בוצע!',
        'faq_title': 'שאלות', 'share_title': 'שתף', 'share_modal_title': 'שתף', 'share_copy_label': 'העתק', 'share_msg': 'ממיר ICO:',
        'faq_list': [{'q': 'מה זה?', 'a': 'אייקון אתר.'}, {'q': 'שקוף?', 'a': 'כן.'}, {'q': 'גודל?', 'a': '32x32'}, {'q': 'בטוח?', 'a': 'כן.'}]
    }
}

SUPPORTED_LANGS = list(TRANSLATIONS.keys())
DEFAULT_LANG = 'en'

# ==========================================
# 4. 路由逻辑
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
@limiter.limit("15 per minute")
def generate_ico():
    if 'file' not in request.files: return "Error", 400
    file = request.files['file']
    if file.filename == '': return "Error", 400
    try:
        size = int(request.form.get('size', '32'))
        file_bytes = file.read()
        if len(file_bytes) == 0: return "Error", 400
        input_stream = io.BytesIO(file_bytes)
        img = Image.open(input_stream)
        if img.width > 2500 or img.height > 2500: img.thumbnail((512, 512), Image.Resampling.LANCZOS)
        if img.mode != "RGBA": img = img.convert("RGBA")
        img = add_smart_glow(img)
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
