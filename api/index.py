import datetime
import io
import os

from flask import (Flask, Response, redirect, render_template, request,
                   send_file)
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from PIL import Image, ImageFilter

app = Flask(__name__, template_folder='../templates')
app.secret_key = os.environ.get('SECRET_KEY', 'global_ico_full_localized_final_v99')
app.url_map.strict_slashes = False
app.config['MAX_CONTENT_LENGTH'] = 4.5 * 1024 * 1024

# 安全防护
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["300 per day", "60 per hour"],
    storage_uri="memory://"
)

# 图像处理：智能描边
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
# 全球语言包：22种语言，全字段翻译 (UI + Guide + FAQ)
# ==========================================
TRANSLATIONS = {
    # --- English ---
    'en': {
        'name': 'English', 'dir': 'ltr', 'recommend': 'Recommended', 'badge': 'HOT',
        'seo_title': 'Free Online ICO Converter - Create Transparent Favicon',
        'seo_desc': 'Best free online ICO converter. Convert PNG, JPG to ICO format instantly.',
        'keywords': 'ico converter, favicon generator',
        'h1': 'ICO Converter', 'subtitle': 'Professional Favicon Generator',
        'upload_label': 'Click to upload or Drag image', 'size_label': 'Target Size', 'btn_submit': 'Generate ICO',
        'footer': 'Securely processed. Privacy protected.', 'error_large': 'File too large (Max 4MB)',
        'tab_create': 'Create', 'tab_guide': 'Guide',
        'guide_preview_title': 'Visual Preview', 'guide_preview_desc': 'Your icon will be displayed in browser tabs.',
        'step1_title': 'Upload to Server', 'step1_desc': 'Upload favicon.ico to your website root.', 'step1_file_path': '/root/', 'step1_file_name': 'favicon.ico',
        'step2_title': 'Update HTML', 'step2_desc': 'Paste this code into the <head> section.',
        'guide_copy_btn': 'Copy', 'guide_copied': 'Copied!',
        'faq_title': 'FAQ', 'share_title': 'Share',
        'faq_list': [
            {'q': 'What is a Favicon?', 'a': 'A small icon displayed in browser tabs to identify your website.'},
            {'q': 'Transparent backgrounds?', 'a': 'Yes, we preserve transparency and optimize for dark mode.'},
            {'q': 'Best size?', 'a': '32x32 is standard. 16x16 for tabs, 48x48 for shortcuts.'},
            {'q': 'Is it safe?', 'a': 'Yes. Images are processed in memory and never saved.'}
        ]
    },
    # --- 简体中文 ---
    'zh': {
        'name': '简体中文', 'dir': 'ltr', 'recommend': '推荐尺寸', 'badge': '常用',
        'seo_title': '在线 ICO 图标生成器 - 免费制作透明 Favicon',
        'seo_desc': '免费在线图片转 ICO 工具。支持透明背景。',
        'keywords': 'ICO生成器, favicon制作',
        'h1': 'ICO 图标生成器', 'subtitle': '一键生成透明背景图标',
        'upload_label': '点击选择 或 拖拽图片', 'size_label': '目标尺寸', 'btn_submit': '生成并下载 .ICO',
        'footer': '数据安全保护，不保存任何图片。', 'error_large': '文件过大',
        'tab_create': '制作图标', 'tab_guide': '使用指南',
        'guide_preview_title': '效果预览', 'guide_preview_desc': '图标将显示在浏览器标签页中。',
        'step1_title': '上传至服务器', 'step1_desc': '将 favicon.ico 上传到网站根目录。', 'step1_file_path': '/根目录/', 'step1_file_name': 'favicon.ico',
        'step2_title': '引入 HTML', 'step2_desc': '将代码粘贴到网页 <head> 标签之间。',
        'guide_copy_btn': '复制', 'guide_copied': '已复制!',
        'faq_title': '常见问题', 'share_title': '分享工具',
        'faq_list': [
            {'q': '什么是 Favicon？', 'a': '显示在浏览器标签页上的小图标，用于识别网站品牌。'},
            {'q': '支持透明背景吗？', 'a': '支持。我们会保留 PNG 透明度并适配深色模式。'},
            {'q': '最佳尺寸是多少？', 'a': '32x32 是标准尺寸。16x16 用于标签，48x48 用于桌面。'},
            {'q': '数据安全吗？', 'a': '绝对安全。所有处理在内存中进行，不保存文件。'}
        ]
    },
    # --- 繁体中文 ---
    'tw': {
        'name': '繁體中文', 'dir': 'ltr', 'recommend': '推薦尺寸', 'badge': '常用',
        'seo_title': '線上 ICO 圖示產生器 - 製作透明 Favicon',
        'seo_desc': '免費線上圖片轉 ICO 工具。',
        'keywords': 'ICO產生器, favicon製作',
        'h1': 'ICO 圖示產生器', 'subtitle': '一鍵生成透明背景圖示',
        'upload_label': '點擊選擇 或 拖曳圖片', 'size_label': '目標尺寸', 'btn_submit': '產生並下載 .ICO',
        'footer': '資料安全保護，不保存任何圖片。', 'error_large': '檔案過大',
        'tab_create': '製作圖示', 'tab_guide': '使用指南',
        'guide_preview_title': '效果預覽', 'guide_preview_desc': '圖示將顯示在瀏覽器分頁上。',
        'step1_title': '上傳至伺服器', 'step1_desc': '將 favicon.ico 上傳到網站根目錄。', 'step1_file_path': '/根目錄/', 'step1_file_name': 'favicon.ico',
        'step2_title': '引入 HTML', 'step2_desc': '將程式碼貼到網頁 <head> 標籤之間。',
        'guide_copy_btn': '複製', 'guide_copied': '已複製!',
        'faq_title': '常見問題', 'share_title': '分享工具',
        'faq_list': [
            {'q': '什麼是 Favicon？', 'a': '顯示在瀏覽器分頁上的小圖示，用於識別網站品牌。'},
            {'q': '支援透明背景嗎？', 'a': '支援。我們會保留 PNG 透明度並適配深色模式。'},
            {'q': '最佳尺寸是多少？', 'a': '32x32 是標準尺寸。16x16 用於分頁，48x48 用於桌面。'},
            {'q': '資料安全嗎？', 'a': '絕對安全。所有處理在記憶體中進行，不儲存檔案。'}
        ]
    },
    # --- Spanish ---
    'es': {
        'name': 'Español', 'dir': 'ltr', 'recommend': 'Recomendado', 'badge': 'HOT',
        'seo_title': 'Convertidor ICO Online', 'seo_desc': 'Imágenes a ICO gratis.',
        'keywords': 'convertidor ico, favicon',
        'h1': 'Convertidor ICO', 'subtitle': 'Generador de Favicon',
        'upload_label': 'Clic para subir', 'size_label': 'Tamaño', 'btn_submit': 'Generar .ICO',
        'footer': 'Privacidad protegida.', 'error_large': 'Archivo grande',
        'tab_create': 'Crear', 'tab_guide': 'Guía',
        'guide_preview_title': 'Vista Previa', 'guide_preview_desc': 'Su icono aparecerá en las pestañas.',
        'step1_title': 'Subir al Servidor', 'step1_desc': 'Sube favicon.ico al directorio raíz.', 'step1_file_path': '/raíz/', 'step1_file_name': 'favicon.ico',
        'step2_title': 'Código HTML', 'step2_desc': 'Pega esto en la sección <head>.',
        'guide_copy_btn': 'Copiar', 'guide_copied': '¡Copiado!',
        'faq_title': 'Preguntas Frecuentes', 'share_title': 'Compartir',
        'faq_list': [
            {'q': '¿Qué es un Favicon?', 'a': 'Un pequeño icono en la pestaña del navegador.'},
            {'q': '¿Fondo transparente?', 'a': 'Sí, mantenemos la transparencia del PNG.'},
            {'q': '¿Mejor tamaño?', 'a': '32x32 es el estándar para escritorio.'},
            {'q': '¿Es seguro?', 'a': 'Sí, no guardamos sus imágenes.'}
        ]
    },
    # --- French ---
    'fr': {
        'name': 'Français', 'dir': 'ltr', 'recommend': 'Recommandé', 'badge': 'TOP',
        'seo_title': 'Convertisseur ICO', 'seo_desc': 'Image en ICO gratuit.',
        'keywords': 'convertisseur ico',
        'h1': 'Convertisseur ICO', 'subtitle': 'Générateur de Favicon',
        'upload_label': 'Uploader image', 'size_label': 'Taille', 'btn_submit': 'Générer .ICO',
        'footer': 'Confidentialité respectée.', 'error_large': 'Fichier volumineux',
        'tab_create': 'Créer', 'tab_guide': 'Guide',
        'guide_preview_title': 'Aperçu', 'guide_preview_desc': 'Icône visible dans les onglets.',
        'step1_title': 'Mettre sur Serveur', 'step1_desc': 'Téléversez favicon.ico à la racine.', 'step1_file_path': '/racine/', 'step1_file_name': 'favicon.ico',
        'step2_title': 'Code HTML', 'step2_desc': 'Collez dans la section <head>.',
        'guide_copy_btn': 'Copier', 'guide_copied': 'Copié!',
        'faq_title': 'FAQ', 'share_title': 'Partager',
        'faq_list': [
            {'q': 'Qu\'est-ce qu\'un Favicon ?', 'a': 'Une petite icône dans l\'onglet du navigateur.'},
            {'q': 'Fond transparent ?', 'a': 'Oui, nous conservons la transparence.'},
            {'q': 'Meilleure taille ?', 'a': '32x32 est le standard.'},
            {'q': 'Est-ce sécurisé ?', 'a': 'Oui, aucune image n\'est stockée.'}
        ]
    },
    # --- German ---
    'de': {
        'name': 'Deutsch', 'dir': 'ltr', 'recommend': 'Empfohlen', 'badge': 'TOP',
        'seo_title': 'ICO Konverter', 'seo_desc': 'Bild zu ICO.',
        'keywords': 'ico konverter',
        'h1': 'ICO Konverter', 'subtitle': 'Favicon-Generator',
        'upload_label': 'Bild hochladen', 'size_label': 'Größe', 'btn_submit': '.ICO Herunterladen',
        'footer': 'Datenschutz.', 'error_large': 'Datei zu groß',
        'tab_create': 'Erstellen', 'tab_guide': 'Anleitung',
        'guide_preview_title': 'Vorschau', 'guide_preview_desc': 'Icon im Browser-Tab.',
        'step1_title': 'Hochladen', 'step1_desc': 'Laden Sie favicon.ico ins Stammverzeichnis.', 'step1_file_path': '/root/', 'step1_file_name': 'favicon.ico',
        'step2_title': 'HTML', 'step2_desc': 'In den <head> Bereich einfügen.',
        'guide_copy_btn': 'Kopieren', 'guide_copied': 'Kopiert!',
        'faq_title': 'FAQ', 'share_title': 'Teilen',
        'faq_list': [
            {'q': 'Was ist ein Favicon?', 'a': 'Ein kleines Symbol im Browser-Tab.'},
            {'q': 'Transparenz?', 'a': 'Ja, wir unterstützen transparente Hintergründe.'},
            {'q': 'Beste Größe?', 'a': '32x32 ist Standard.'},
            {'q': 'Ist es sicher?', 'a': 'Ja, wir speichern keine Bilder.'}
        ]
    },
    # --- Japanese ---
    'ja': {
        'name': '日本語', 'dir': 'ltr', 'recommend': '推奨', 'badge': '人気',
        'seo_title': 'ICO変換ツール', 'seo_desc': 'ファビコン作成。',
        'keywords': 'ico 変換',
        'h1': 'ICO 変換ツール', 'subtitle': 'プロフェッショナル作成',
        'upload_label': 'アップロード', 'size_label': 'サイズ', 'btn_submit': 'ダウンロード',
        'footer': 'プライバシー保護。', 'error_large': 'ファイル過大',
        'tab_create': '作成', 'tab_guide': 'ガイド',
        'guide_preview_title': 'プレビュー', 'guide_preview_desc': 'ブラウザのタブに表示されます。',
        'step1_title': 'アップロード', 'step1_desc': 'ルートディレクトリに配置してください。', 'step1_file_path': '/ルート/', 'step1_file_name': 'favicon.ico',
        'step2_title': 'HTML', 'step2_desc': '<head> 内に貼り付けてください。',
        'guide_copy_btn': 'コピー', 'guide_copied': '完了!',
        'faq_title': 'よくある質問', 'share_title': 'シェア',
        'faq_list': [
            {'q': 'Faviconとは？', 'a': 'ブラウザのタブに表示される小さなアイコンです。'},
            {'q': '透過背景は？', 'a': 'はい、透過PNGに対応しています。'},
            {'q': '最適なサイズは？', 'a': 'PCでは32x32が標準です。'},
            {'q': '安全ですか？', 'a': 'はい、画像は保存されません。'}
        ]
    },
    # --- Korean ---
    'ko': {
        'name': '한국어', 'dir': 'ltr', 'recommend': '추천', 'badge': '인기',
        'seo_title': 'ICO 변환기', 'seo_desc': '파비콘 만들기.',
        'keywords': 'ico 변환',
        'h1': 'ICO 변환기', 'subtitle': '전문 파비콘 도구',
        'upload_label': '업로드', 'size_label': '크기', 'btn_submit': '다운로드',
        'footer': '개인정보 보호.', 'error_large': '파일 큼',
        'tab_create': '제작', 'tab_guide': '가이드',
        'guide_preview_title': '미리보기', 'guide_preview_desc': '브라우저 탭에 표시됩니다.',
        'step1_title': '업로드', 'step1_desc': '루트 디렉토리에 업로드하세요.', 'step1_file_path': '/루트/', 'step1_file_name': 'favicon.ico',
        'step2_title': 'HTML', 'step2_desc': '<head> 섹션에 붙여넣으세요.',
        'guide_copy_btn': '복사', 'guide_copied': '완료!',
        'faq_title': 'FAQ', 'share_title': '공유',
        'faq_list': [
            {'q': '파비콘이란?', 'a': '브라우저 탭에 표시되는 아이콘입니다.'},
            {'q': '투명 배경?', 'a': '네, 투명도를 유지합니다.'},
            {'q': '최적 사이즈?', 'a': '32x32가 표준입니다.'},
            {'q': '안전한가요?', 'a': '네, 이미지는 저장되지 않습니다.'}
        ]
    },
    # --- Russian ---
    'ru': {
        'name': 'Русский', 'dir': 'ltr', 'recommend': 'Стандарт', 'badge': 'ХИТ',
        'seo_title': 'Конвертер ICO', 'seo_desc': 'Создать Favicon.',
        'keywords': 'ico конвертер',
        'h1': 'Конвертер ICO', 'subtitle': 'Генератор иконок',
        'upload_label': 'Загрузить', 'size_label': 'Размер', 'btn_submit': 'Скачать',
        'footer': 'Конфиденциальность.', 'error_large': 'Файл большой',
        'tab_create': 'Создать', 'tab_guide': 'Гид',
        'guide_preview_title': 'Предпросмотр', 'guide_preview_desc': 'Иконка в браузере.',
        'step1_title': 'Загрузка', 'step1_desc': 'Загрузите в корень сайта.', 'step1_file_path': '/root/', 'step1_file_name': 'favicon.ico',
        'step2_title': 'HTML', 'step2_desc': 'Вставьте в <head>.',
        'guide_copy_btn': 'Копия', 'guide_copied': 'Готово!',
        'faq_title': 'Вопросы', 'share_title': 'Поделиться',
        'faq_list': [
            {'q': 'Что такое Favicon?', 'a': 'Иконка во вкладке браузера.'},
            {'q': 'Прозрачность?', 'a': 'Да, поддерживается.'},
            {'q': 'Лучший размер?', 'a': '32x32 - стандарт.'},
            {'q': 'Это безопасно?', 'a': 'Да, файлы не сохраняются.'}
        ]
    },
    # --- Italian ---
    'it': {
        'name': 'Italiano', 'dir': 'ltr', 'recommend': 'Consigliato', 'badge': 'TOP',
        'seo_title': 'Convertitore ICO', 'seo_desc': 'Crea Favicon.',
        'keywords': 'convertitore ico',
        'h1': 'Convertitore ICO', 'subtitle': 'Generatore Favicon',
        'upload_label': 'Carica', 'size_label': 'Dimensione', 'btn_submit': 'Scarica',
        'footer': 'Privacy protetta.', 'error_large': 'File grande',
        'tab_create': 'Crea', 'tab_guide': 'Guida',
        'guide_preview_title': 'Anteprima', 'guide_preview_desc': 'Icona nei tab.',
        'step1_title': 'Carica', 'step1_desc': 'Carica nella root.', 'step1_file_path': '/root/', 'step1_file_name': 'favicon.ico',
        'step2_title': 'HTML', 'step2_desc': 'Incolla in <head>.',
        'guide_copy_btn': 'Copia', 'guide_copied': 'Fatto!',
        'faq_title': 'FAQ', 'share_title': 'Condividi',
        'faq_list': [{'q': 'Cos\'è un Favicon?', 'a': 'Icona nel tab del browser.'}, {'q': 'Trasparenza?', 'a': 'Sì, supportata.'}, {'q': 'Dimensione?', 'a': '32x32 è standard.'}, {'q': 'Sicuro?', 'a': 'Sì, nessun salvataggio.'}]
    },
    # --- Portuguese ---
    'pt': {
        'name': 'Português', 'dir': 'ltr', 'recommend': 'Recomendado', 'badge': 'HOT',
        'seo_title': 'Conversor ICO', 'seo_desc': 'Criar Favicon.',
        'keywords': 'conversor ico',
        'h1': 'Conversor ICO', 'subtitle': 'Gerador Favicon',
        'upload_label': 'Subir', 'size_label': 'Tamanho', 'btn_submit': 'Baixar',
        'footer': 'Seguro.', 'error_large': 'Erro',
        'tab_create': 'Criar', 'tab_guide': 'Guia',
        'guide_preview_title': 'Prévia', 'guide_preview_desc': 'Ícone nas abas.',
        'step1_title': 'Upload', 'step1_desc': 'Envie para a raiz.', 'step1_file_path': '/raiz/', 'step1_file_name': 'favicon.ico',
        'step2_title': 'HTML', 'step2_desc': 'Cole no <head>.',
        'guide_copy_btn': 'Copiar', 'guide_copied': 'Copiado!',
        'faq_title': 'FAQ', 'share_title': 'Compartilhar',
        'faq_list': [{'q': 'O que é Favicon?', 'a': 'Ícone na aba.'}, {'q': 'Transparência?', 'a': 'Sim, suportada.'}, {'q': 'Tamanho?', 'a': '32x32 padrão.'}, {'q': 'Seguro?', 'a': 'Sim, sem armazenamento.'}]
    },
    # --- Dutch ---
    'nl': {
        'name': 'Nederlands', 'dir': 'ltr', 'recommend': 'Aanbevolen', 'badge': 'TOP',
        'seo_title': 'ICO Converter', 'seo_desc': 'Favicon maken.',
        'keywords': 'ico converter',
        'h1': 'ICO Converter', 'subtitle': 'Favicon Generator',
        'upload_label': 'Uploaden', 'size_label': 'Grootte', 'btn_submit': 'Downloaden',
        'footer': 'Privacy.', 'error_large': 'Fout',
        'tab_create': 'Maken', 'tab_guide': 'Gids',
        'guide_preview_title': 'Voorbeeld', 'guide_preview_desc': 'Icoon in tabs.',
        'step1_title': 'Uploaden', 'step1_desc': 'Upload naar root.', 'step1_file_path': '/root/', 'step1_file_name': 'favicon.ico',
        'step2_title': 'HTML', 'step2_desc': 'Plak in <head>.',
        'guide_copy_btn': 'Kopie', 'guide_copied': 'Klaar!',
        'faq_title': 'FAQ', 'share_title': 'Delen',
        'faq_list': [{'q': 'Wat is een Favicon?', 'a': 'Icoon in browsertab.'}, {'q': 'Transparant?', 'a': 'Ja, ondersteund.'}, {'q': 'Grootte?', 'a': '32x32 is standaard.'}, {'q': 'Veilig?', 'a': 'Ja, geen opslag.'}]
    },
    # --- Polish ---
    'pl': {
        'name': 'Polski', 'dir': 'ltr', 'recommend': 'Zalecane', 'badge': 'HIT',
        'seo_title': 'Konwerter ICO', 'seo_desc': 'Generator Favicon.',
        'keywords': 'konwerter ico',
        'h1': 'Konwerter ICO', 'subtitle': 'Generator Favicon',
        'upload_label': 'Prześlij', 'size_label': 'Rozmiar', 'btn_submit': 'Pobierz',
        'footer': 'Prywatność.', 'error_large': 'Błąd',
        'tab_create': 'Stwórz', 'tab_guide': 'Info',
        'guide_preview_title': 'Podgląd', 'guide_preview_desc': 'Ikona w kartach.',
        'step1_title': 'Prześlij', 'step1_desc': 'Wgraj do katalogu głównego.', 'step1_file_path': '/root/', 'step1_file_name': 'favicon.ico',
        'step2_title': 'HTML', 'step2_desc': 'Wklej w <head>.',
        'guide_copy_btn': 'Kopiuj', 'guide_copied': 'Gotowe!',
        'faq_title': 'FAQ', 'share_title': 'Udostępnij',
        'faq_list': [{'q': 'Co to Favicon?', 'a': 'Ikona w karcie.'}, {'q': 'Przezroczystość?', 'a': 'Tak.'}, {'q': 'Rozmiar?', 'a': 'Standard to 32x32.'}, {'q': 'Bezpieczne?', 'a': 'Tak.'}]
    },
    # --- Swedish ---
    'sv': {
        'name': 'Svenska', 'dir': 'ltr', 'recommend': 'Standard', 'badge': 'TOP',
        'seo_title': 'ICO Konverterare', 'seo_desc': 'Skapa Favicon.',
        'keywords': 'ico konverterare',
        'h1': 'ICO Konverterare', 'subtitle': 'Favicon Generator',
        'upload_label': 'Ladda upp', 'size_label': 'Storlek', 'btn_submit': 'Ladda ner',
        'footer': 'Säker.', 'error_large': 'Fel',
        'tab_create': 'Skapa', 'tab_guide': 'Guide',
        'guide_preview_title': 'Förhandsvisning', 'guide_preview_desc': 'Ikon i flikar.',
        'step1_title': 'Ladda upp', 'step1_desc': 'Ladda till rot.', 'step1_file_path': '/rot/', 'step1_file_name': 'favicon.ico',
        'step2_title': 'HTML', 'step2_desc': 'Klistra in i <head>.',
        'guide_copy_btn': 'Kopiera', 'guide_copied': 'Klart!',
        'faq_title': 'FAQ', 'share_title': 'Dela',
        'faq_list': [{'q': 'Vad är Favicon?', 'a': 'Ikon i webbläsaren.'}, {'q': 'Genomskinlig?', 'a': 'Ja.'}, {'q': 'Storlek?', 'a': '32x32 är standard.'}, {'q': 'Säkert?', 'a': 'Ja.'}]
    },
    # --- Ukrainian ---
    'uk': {
        'name': 'Українська', 'dir': 'ltr', 'recommend': 'Стандарт', 'badge': 'ХІТ',
        'seo_title': 'Конвертер ICO', 'seo_desc': 'Створити Favicon.',
        'keywords': 'ico конвертер',
        'h1': 'Конвертер ICO', 'subtitle': 'Генератор іконок',
        'upload_label': 'Завантажити', 'size_label': 'Розмір', 'btn_submit': 'Завантажити',
        'footer': 'Конфіденційність.', 'error_large': 'Помилка',
        'tab_create': 'Створити', 'tab_guide': 'Інструкція',
        'guide_preview_title': 'Перегляд', 'guide_preview_desc': 'Іконка у вкладках.',
        'step1_title': 'Завантаження', 'step1_desc': 'Завантажте в корінь.', 'step1_file_path': '/root/', 'step1_file_name': 'favicon.ico',
        'step2_title': 'HTML', 'step2_desc': 'Вставте в <head>.',
        'guide_copy_btn': 'Копія', 'guide_copied': 'Готово!',
        'faq_title': 'FAQ', 'share_title': 'Поділитися',
        'faq_list': [{'q': 'Що таке Favicon?', 'a': 'Іконка сайту.'}, {'q': 'Прозорість?', 'a': 'Так.'}, {'q': 'Розмір?', 'a': '32x32 стандарт.'}, {'q': 'Безпечно?', 'a': 'Так.'}]
    },
    # --- Indonesian ---
    'id': {
        'name': 'Bahasa Indonesia', 'dir': 'ltr', 'recommend': 'Disarankan', 'badge': 'HOT',
        'seo_title': 'Konverter ICO', 'seo_desc': 'Buat Favicon.',
        'keywords': 'konverter ico',
        'h1': 'Konverter ICO', 'subtitle': 'Pembuat Favicon',
        'upload_label': 'Unggah', 'size_label': 'Ukuran', 'btn_submit': 'Unduh',
        'footer': 'Aman.', 'error_large': 'Error',
        'tab_create': 'Buat', 'tab_guide': 'Panduan',
        'guide_preview_title': 'Pratinjau', 'guide_preview_desc': 'Ikon di tab.',
        'step1_title': 'Unggah', 'step1_desc': 'Unggah ke root.', 'step1_file_path': '/root/', 'step1_file_name': 'favicon.ico',
        'step2_title': 'HTML', 'step2_desc': 'Tempel di <head>.',
        'guide_copy_btn': 'Salin', 'guide_copied': 'Disalin!',
        'faq_title': 'FAQ', 'share_title': 'Bagikan',
        'faq_list': [{'q': 'Apa itu Favicon?', 'a': 'Ikon tab.'}, {'q': 'Transparan?', 'a': 'Ya.'}, {'q': 'Ukuran?', 'a': '32x32 standar.'}, {'q': 'Aman?', 'a': 'Ya.'}]
    },
    # --- Turkish ---
    'tr': {
        'name': 'Türkçe', 'dir': 'ltr', 'recommend': 'Önerilen', 'badge': 'POP',
        'seo_title': 'ICO Dönüştürücü', 'seo_desc': 'Favicon yapma.',
        'keywords': 'ico dönüştürücü',
        'h1': 'ICO Dönüştürücü', 'subtitle': 'Favicon Oluşturucu',
        'upload_label': 'Yükle', 'size_label': 'Boyut', 'btn_submit': 'İndir',
        'footer': 'Gizlilik.', 'error_large': 'Hata',
        'tab_create': 'Oluştur', 'tab_guide': 'Rehber',
        'guide_preview_title': 'Önizleme', 'guide_preview_desc': 'Sekmelerde simge.',
        'step1_title': 'Yükle', 'step1_desc': 'Kök dizine yükle.', 'step1_file_path': '/kök/', 'step1_file_name': 'favicon.ico',
        'step2_title': 'HTML', 'step2_desc': '<head>\'e yapıştır.',
        'guide_copy_btn': 'Kopyala', 'guide_copied': 'Tamam!',
        'faq_title': 'SSS', 'share_title': 'Paylaş',
        'faq_list': [{'q': 'Favicon nedir?', 'a': 'Sekme simgesi.'}, {'q': 'Şeffaflık?', 'a': 'Evet.'}, {'q': 'Boyut?', 'a': '32x32 standart.'}, {'q': 'Güvenli mi?', 'a': 'Evet.'}]
    },
    # --- Vietnamese ---
    'vi': {
        'name': 'Tiếng Việt', 'dir': 'ltr', 'recommend': 'Đề xuất', 'badge': 'HOT',
        'seo_title': 'Chuyển đổi ICO', 'seo_desc': 'Tạo Favicon.',
        'keywords': 'chuyển đổi ico',
        'h1': 'Chuyển đổi ICO', 'subtitle': 'Tạo Favicon',
        'upload_label': 'Tải lên', 'size_label': 'Kích thước', 'btn_submit': 'Tải xuống',
        'footer': 'Bảo mật.', 'error_large': 'Lỗi',
        'tab_create': 'Tạo', 'tab_guide': 'H.dẫn',
        'guide_preview_title': 'Xem trước', 'guide_preview_desc': 'Biểu tượng trên tab.',
        'step1_title': 'Tải lên', 'step1_desc': 'Tải lên thư mục gốc.', 'step1_file_path': '/gốc/', 'step1_file_name': 'favicon.ico',
        'step2_title': 'HTML', 'step2_desc': 'Dán vào <head>.',
        'guide_copy_btn': 'Sao chép', 'guide_copied': 'Xong!',
        'faq_title': 'Hỏi đáp', 'share_title': 'Chia sẻ',
        'faq_list': [{'q': 'Favicon là gì?', 'a': 'Biểu tượng tab.'}, {'q': 'Trong suốt?', 'a': 'Có.'}, {'q': 'Kích thước?', 'a': '32x32 chuẩn.'}, {'q': 'An toàn?', 'a': 'Có.'}]
    },
    # --- Thai ---
    'th': {
        'name': 'ไทย', 'dir': 'ltr', 'recommend': 'แนะนำ', 'badge': 'ฮิต',
        'seo_title': 'ตัวแปลง ICO', 'seo_desc': 'สร้าง Favicon.',
        'keywords': 'แปลงไฟล์ ico',
        'h1': 'ตัวแปลง ICO', 'subtitle': 'สร้าง Favicon',
        'upload_label': 'อัปโหลด', 'size_label': 'ขนาด', 'btn_submit': 'ดาวน์โหลด',
        'footer': 'ปลอดภัย', 'error_large': 'ไฟล์ใหญ่',
        'tab_create': 'สร้าง', 'tab_guide': 'คู่มือ',
        'guide_preview_title': 'ตัวอย่าง', 'guide_preview_desc': 'ไอคอนบนแท็บ',
        'step1_title': 'อัปโหลด', 'step1_desc': 'อัปโหลดไปที่ราก', 'step1_file_path': '/ราก/', 'step1_file_name': 'favicon.ico',
        'step2_title': 'HTML', 'step2_desc': 'วางใน <head>',
        'guide_copy_btn': 'คัดลอก', 'guide_copied': 'สำเร็จ!',
        'faq_title': 'คำถามที่พบบ่อย', 'share_title': 'แชร์',
        'faq_list': [{'q': 'Favicon คือ?', 'a': 'ไอคอนแท็บ'}, {'q': 'โปร่งใส?', 'a': 'ใช่'}, {'q': 'ขนาด?', 'a': '32x32'}, {'q': 'ปลอดภัย?', 'a': 'ใช่'}]
    },
    # --- Hindi ---
    'hi': {
        'name': 'हिन्दी', 'dir': 'ltr', 'recommend': 'अनुशंसित', 'badge': 'आम',
        'seo_title': 'ICO कन्वर्टर', 'seo_desc': 'Favicon बनाएं.',
        'keywords': 'ico converter',
        'h1': 'ICO कन्वर्टर', 'subtitle': 'Favicon जनरेटर',
        'upload_label': 'अपलोड', 'size_label': 'आकार', 'btn_submit': 'डाउनलोड',
        'footer': 'सुरक्षित', 'error_large': 'बड़ी फ़ाइल',
        'tab_create': 'बनाएं', 'tab_guide': 'गाइड',
        'guide_preview_title': 'पूर्वावलोकन', 'guide_preview_desc': 'टैब में आइकन।',
        'step1_title': 'अपलोड', 'step1_desc': 'रूट में अपलोड करें।', 'step1_file_path': '/रूट/', 'step1_file_name': 'favicon.ico',
        'step2_title': 'HTML', 'step2_desc': '<head> में पेस्ट करें।',
        'guide_copy_btn': 'कॉपी', 'guide_copied': 'हो गया!',
        'faq_title': 'सामान्य प्रश्न', 'share_title': 'साझा करें',
        'faq_list': [{'q': 'Favicon क्या है?', 'a': 'टैब आइकन।'}, {'q': 'पारदर्शी?', 'a': 'हाँ।'}, {'q': 'आकार?', 'a': '32x32'}, {'q': 'सुरक्षित?', 'a': 'हाँ।'}]
    },
    # --- Arabic ---
    'ar': {
        'name': 'العربية', 'dir': 'rtl', 'recommend': 'موصى به', 'badge': 'شائع',
        'seo_title': 'محول ICO', 'seo_desc': 'إنشاء أيقونة.',
        'keywords': 'محول ico',
        'h1': 'محول ICO', 'subtitle': 'مولد أيقونات',
        'upload_label': 'رفع', 'size_label': 'الحجم', 'btn_submit': 'تحميل',
        'footer': 'آمن.', 'error_large': 'خطأ',
        'tab_create': 'إنشاء', 'tab_guide': 'دليل',
        'guide_preview_title': 'معاينة', 'guide_preview_desc': 'أيقونة في التبويب.',
        'step1_title': 'رفع', 'step1_desc': 'ارفع للجذر.', 'step1_file_path': '/جذر/', 'step1_file_name': 'favicon.ico',
        'step2_title': 'HTML', 'step2_desc': 'لصق في <head>.',
        'guide_copy_btn': 'نسخ', 'guide_copied': 'تم!',
        'faq_title': 'أسئلة شائعة', 'share_title': 'مشاركة',
        'faq_list': [{'q': 'ما هو Favicon؟', 'a': 'أيقونة تبويب.'}, {'q': 'شفافية؟', 'a': 'نعم.'}, {'q': 'الحجم؟', 'a': '32x32'}, {'q': 'آمن؟', 'a': 'نعم.'}]
    },
    # --- Hebrew ---
    'he': {
        'name': 'עברית', 'dir': 'rtl', 'recommend': 'מומלץ', 'badge': 'נפוץ',
        'seo_title': 'ממיר ICO', 'seo_desc': 'צור Favicon.',
        'keywords': 'ממיר ico',
        'h1': 'ממיר ICO', 'subtitle': 'יוצר אייקונים',
        'upload_label': 'העלאה', 'size_label': 'גודל', 'btn_submit': 'הורד',
        'footer': 'פרטיות.', 'error_large': 'שגיאה',
        'tab_create': 'צור', 'tab_guide': 'מדריך',
        'guide_preview_title': 'תצוגה', 'guide_preview_desc': 'אייקון בכרטיסייה.',
        'step1_title': 'העלאה', 'step1_desc': 'העלה לשורש.', 'step1_file_path': '/שורש/', 'step1_file_name': 'favicon.ico',
        'step2_title': 'HTML', 'step2_desc': 'הדבק ב-<head>.',
        'guide_copy_btn': 'העתק', 'guide_copied': 'בוצע!',
        'faq_title': 'שאלות נפוצות', 'share_title': 'שתף',
        'faq_list': [{'q': 'מה זה Favicon?', 'a': 'אייקון.'}, {'q': 'שקיפות?', 'a': 'כן.'}, {'q': 'גודל?', 'a': '32x32'}, {'q': 'בטוח?', 'a': 'כן.'}]
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
