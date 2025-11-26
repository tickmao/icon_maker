import datetime
import io
import os

from flask import (Flask, Response, redirect, render_template, request,
                   send_file)
from PIL import Image

app = Flask(__name__, template_folder='../templates')
app.secret_key = os.environ.get('SECRET_KEY', 'global_ico_full_v5')
app.url_map.strict_slashes = False
app.config['MAX_CONTENT_LENGTH'] = 4.5 * 1024 * 1024

# ==========================================
# 1. 通用指引文案 (英语兜底)
# ==========================================
EN_GUIDE = {
    'tab_create': 'Create',
    'tab_guide': 'Guide',
    'guide_preview_title': 'Visual Preview',
    'guide_preview_desc': 'Your icon will be displayed in browser tabs, bookmarks, and history to help users identify your brand instantly.',
    'step1_title': 'Upload to Server',
    'step1_desc': 'Download the generated .ico file and upload it to the root directory of your website server (e.g. /public_html).',
    'step1_file_path': '/root/',
    'step1_file_name': 'favicon.ico',
    'step2_title': 'Update HTML Code',
    'step2_desc': 'Copy the code below and paste it into the <head> section of your HTML files, before the closing tag.',
    'guide_copy_btn': 'Copy',
    'guide_copied': 'Copied!',
}

# ==========================================
# 2. 终极全球语言包 (22种语言完整配置)
# ==========================================
TRANSLATIONS = {
    # --- 英语 ---
    'en': {
        **EN_GUIDE,
        'name': 'English', 'dir': 'ltr', 'recommend': 'Recommended', 'badge': 'HOT',
        'seo_title': 'Free Online ICO Converter - Create Transparent Favicon (Fast & Secure)',
        'seo_desc': 'Best free online ICO converter. Convert PNG, JPG, WEBP to ICO format instantly. Support transparent backgrounds.',
        'keywords': 'ico converter, favicon generator, png to ico, jpg to ico, make favicon, transparent ico, online icon maker',
        'h1': 'ICO Converter', 'subtitle': 'Professional Favicon Generator', 'upload_label': 'Click to upload or Drag image',
        'size_label': 'Target Size', 'btn_submit': 'Generate ICO', 'footer': 'Securely processed. Privacy protected.', 'error_large': 'File too large (Max 4MB)'
    },

    # --- 简体中文 ---
    'zh': {
        'name': '简体中文', 'dir': 'ltr', 'recommend': '推荐尺寸', 'badge': '常用',
        'seo_title': '在线 ICO 图标生成器 - 免费制作透明 Favicon (极速版)',
        'seo_desc': '免费在线将图片转换为 ICO 图标。支持透明背景，一键生成多种尺寸。网站 Favicon 制作最佳工具。',
        'keywords': 'ICO生成器, favicon制作, 在线转ICO, png转ico, jpg转ico, 网站图标制作, 透明ico',
        'h1': 'ICO 图标生成器', 'subtitle': '一键生成透明背景图标', 'upload_label': '点击选择 或 拖拽图片',
        'size_label': '目标尺寸', 'btn_submit': '生成并下载 .ICO', 'footer': '数据安全保护，不保存任何图片。', 'error_large': '文件过大 (最大 4MB)',
        'tab_create': '制作图标', 'tab_guide': '使用指南',
        'guide_preview_title': '效果预览', 'guide_preview_desc': '您的图标将显示在浏览器标签页、书签栏及历史记录中。',
        'step1_title': '上传至服务器', 'step1_desc': '下载生成的 .ico 文件，并将其上传到您网站服务器的根目录下。', 'step1_file_path': '/根目录/', 'step1_file_name': 'favicon.ico',
        'step2_title': '引入 HTML 代码', 'step2_desc': '复制下方的代码片段，粘贴到您网页源文件 <head> 标签之间。',
        'guide_copy_btn': '复制', 'guide_copied': '已复制!'
    },

    # --- 繁体中文 ---
    'tw': {
        'name': '繁體中文', 'dir': 'ltr', 'recommend': '推薦尺寸', 'badge': '常用',
        'seo_title': '線上 ICO 圖示產生器 - 製作透明 Favicon (免費工具)',
        'seo_desc': '免費線上圖片轉 ICO 工具。支援透明背景，快速產生。網頁 Favicon 製作神器。',
        'keywords': 'ICO產生器, favicon製作, 線上轉ICO, png轉ico, 網站圖示, 透明ico',
        'h1': 'ICO 圖示產生器', 'subtitle': '一鍵生成透明背景圖示', 'upload_label': '點擊選擇 或 拖曳圖片',
        'size_label': '目標尺寸', 'btn_submit': '產生並下載 .ICO', 'footer': '資料安全保護，不保存任何圖片。', 'error_large': '檔案過大 (最大 4MB)',
        'tab_create': '製作圖示', 'tab_guide': '使用指南',
        'guide_preview_title': '效果預覽', 'guide_preview_desc': '您的圖示將顯示在瀏覽器分頁上，有助於快速識別品牌。',
        'step1_title': '上傳至伺服器', 'step1_desc': '下載產生的 .ico 檔案，並將其上傳到您網站伺服器的根目錄下。', 'step1_file_path': '/根目錄/', 'step1_file_name': 'favicon.ico',
        'step2_title': '引入 HTML 程式碼', 'step2_desc': '複製下方的程式碼片段，貼上到您網頁原始檔 <head> 標籤之間。',
        'guide_copy_btn': '複製', 'guide_copied': '已複製!'
    },

    # --- 西班牙语 ---
    'es': {
        **EN_GUIDE,
        'name': 'Español', 'dir': 'ltr', 'recommend': 'Recomendado', 'badge': 'HOT',
        'seo_title': 'Convertidor ICO Online - Crear Favicon Transparente',
        'seo_desc': 'Convierte imágenes PNG/JPG a formato ICO en línea gratis.',
        'keywords': 'convertidor ico, generador favicon, png a ico, crear favicon',
        'h1': 'Convertidor ICO', 'subtitle': 'Generador de Favicon', 'upload_label': 'Clic para subir',
        'size_label': 'Tamaño', 'btn_submit': 'Generar .ICO', 'footer': 'Privacidad protegida.', 'error_large': 'Archivo muy grande'
    },

    # --- 法语 ---
    'fr': {
        **EN_GUIDE,
        'name': 'Français', 'dir': 'ltr', 'recommend': 'Recommandé', 'badge': 'TOP',
        'seo_title': 'Convertisseur ICO en ligne - Créer Favicon Gratuit',
        'seo_desc': 'Convertir image en ICO gratuitement. Fond transparent supporté.',
        'keywords': 'convertisseur ico, générateur favicon, png en ico, créer favicon',
        'h1': 'Convertisseur ICO', 'subtitle': 'Générateur de Favicon', 'upload_label': 'Uploader une image',
        'size_label': 'Taille', 'btn_submit': 'Générer .ICO', 'footer': 'Confidentialité respectée.', 'error_large': 'Fichier trop volumineux'
    },

    # --- 德语 ---
    'de': {
        **EN_GUIDE,
        'name': 'Deutsch', 'dir': 'ltr', 'recommend': 'Empfohlen', 'badge': 'TOP',
        'seo_title': 'Online ICO Konverter - Favicon erstellen',
        'seo_desc': 'Bilder online in ICO umwandeln. Professionelles Werkzeug.',
        'keywords': 'ico konverter, favicon erstellen, png in ico, bild in ico',
        'h1': 'ICO Konverter', 'subtitle': 'Favicon-Generator', 'upload_label': 'Bild hochladen',
        'size_label': 'Größe', 'btn_submit': '.ICO Herunterladen', 'footer': 'Datenschutz.', 'error_large': 'Datei zu groß'
    },

    # --- 意大利语 ---
    'it': {
        **EN_GUIDE,
        'name': 'Italiano', 'dir': 'ltr', 'recommend': 'Consigliato', 'badge': 'TOP',
        'seo_title': 'Convertitore ICO Online - Crea Favicon',
        'seo_desc': 'Converti immagini in ICO online. Strumento professionale.',
        'keywords': 'convertitore ico, creare favicon, png in ico, generatore icone',
        'h1': 'Convertitore ICO', 'subtitle': 'Generatore di Favicon', 'upload_label': 'Clicca per caricare',
        'size_label': 'Dimensione', 'btn_submit': 'Scarica .ICO', 'footer': 'Privacy protetta.', 'error_large': 'File troppo grande'
    },

    # --- 葡萄牙语 ---
    'pt': {
        **EN_GUIDE,
        'name': 'Português', 'dir': 'ltr', 'recommend': 'Recomendado', 'badge': 'HOT',
        'seo_title': 'Conversor ICO Online - Criar Favicon',
        'seo_desc': 'Converta imagens para ICO. Melhor gerador de Favicon grátis.',
        'keywords': 'conversor ico, criar favicon, png para ico, gerador de icones',
        'h1': 'Conversor de ICO', 'subtitle': 'Gerador de Favicon', 'upload_label': 'Clique para subir',
        'size_label': 'Tamanho', 'btn_submit': 'Baixar .ICO', 'footer': 'Privacidade protegida.', 'error_large': 'Arquivo muito grande'
    },

    # --- 俄语 ---
    'ru': {
        **EN_GUIDE,
        'name': 'Русский', 'dir': 'ltr', 'recommend': 'Стандарт', 'badge': 'ХИТ',
        'seo_title': 'Онлайн конвертер ICO - Создать Favicon',
        'seo_desc': 'Конвертировать PNG, JPG в ICO онлайн. Профессиональный инструмент.',
        'keywords': 'конвертер ico, создать favicon, png в ico, иконка для сайта',
        'h1': 'Конвертер ICO', 'subtitle': 'Генератор иконок', 'upload_label': 'Загрузить файл',
        'size_label': 'Размер', 'btn_submit': 'Скачать .ICO', 'footer': 'Конфиденциальность.', 'error_large': 'Файл слишком большой'
    },

    # --- 荷兰语 ---
    'nl': {
        **EN_GUIDE,
        'name': 'Nederlands', 'dir': 'ltr', 'recommend': 'Aanbevolen', 'badge': 'TOP',
        'seo_title': 'Online ICO Converter - Favicon Maken',
        'seo_desc': 'Afbeeldingen converteren naar ICO. Professionele tool.',
        'keywords': 'ico converter, favicon maken, png naar ico',
        'h1': 'ICO Converter', 'subtitle': 'Favicon Generator', 'upload_label': 'Klik om te uploaden',
        'size_label': 'Grootte', 'btn_submit': 'Downloaden', 'footer': 'Privacy beschermd.', 'error_large': 'Bestand te groot'
    },

    # --- 波兰语 ---
    'pl': {
        **EN_GUIDE,
        'name': 'Polski', 'dir': 'ltr', 'recommend': 'Zalecane', 'badge': 'HIT',
        'seo_title': 'Konwerter ICO Online - Stwórz Favicon',
        'seo_desc': 'Konwertuj obrazy na format ICO. Profesjonalne narzędzie.',
        'keywords': 'konwerter ico, generator favicon, png na ico',
        'h1': 'Konwerter ICO', 'subtitle': 'Generator Favicon', 'upload_label': 'Prześlij plik',
        'size_label': 'Rozmiar', 'btn_submit': 'Pobierz .ICO', 'footer': 'Ochrona prywatności.', 'error_large': 'Plik zbyt duży'
    },

    # --- 日语 ---
    'ja': {
        **EN_GUIDE,
        'name': '日本語', 'dir': 'ltr', 'recommend': '推奨', 'badge': '人気',
        'seo_title': 'ICO変換ツール - 無料でFavicon作成',
        'seo_desc': '画像をICO形式に変換。プロフェッショナルな作成ツール。',
        'keywords': 'ico 変換, ファビコン 作成, png ico 変換, フリーソフト',
        'h1': 'ICO 変換ツール', 'subtitle': 'プロフェッショナルなアイコン作成', 'upload_label': 'アップロード',
        'size_label': 'サイズ', 'btn_submit': 'ダウンロード', 'footer': 'プライバシー保護。', 'error_large': 'ファイルサイズ過大'
    },

    # --- 韩语 ---
    'ko': {
        **EN_GUIDE,
        'name': '한국어', 'dir': 'ltr', 'recommend': '추천', 'badge': '인기',
        'seo_title': 'ICO 변환기 - 파비콘 만들기',
        'seo_desc': 'ICO 변환 도구. 전문 파비콘 생성기.',
        'keywords': 'ico 변환, 파비콘 만들기, png ico 변환',
        'h1': 'ICO 변환기', 'subtitle': '전문 파비콘 생성 도구', 'upload_label': '업로드',
        'size_label': '크기', 'btn_submit': '다운로드', 'footer': '개인정보 보호.', 'error_large': '파일이 너무 큽니다'
    },

    # --- 印尼语 ---
    'id': {
        **EN_GUIDE,
        'name': 'Bahasa Indonesia', 'dir': 'ltr', 'recommend': 'Disarankan', 'badge': 'HOT',
        'seo_title': 'Konverter ICO Online - Buat Favicon',
        'seo_desc': 'Ubah gambar menjadi ICO online. Alat Favicon profesional.',
        'keywords': 'konverter ico, buat favicon, ubah png ke ico',
        'h1': 'Konverter ICO', 'subtitle': 'Pembuat Favicon', 'upload_label': 'Unggah gambar',
        'size_label': 'Ukuran', 'btn_submit': 'Unduh .ICO', 'footer': 'Privasi dilindungi.', 'error_large': 'File terlalu besar'
    },

    # --- 土耳其语 ---
    'tr': {
        **EN_GUIDE,
        'name': 'Türkçe', 'dir': 'ltr', 'recommend': 'Önerilen', 'badge': 'POP',
        'seo_title': 'Online ICO Dönüştürücü - Favicon Yapma',
        'seo_desc': 'Resimleri ICO formatına çevirin. Profesyonel araç.',
        'keywords': 'ico dönüştürücü, favicon yapma, png to ico',
        'h1': 'ICO Dönüştürücü', 'subtitle': 'Favicon Oluşturucu', 'upload_label': 'Dosya yükle',
        'size_label': 'Boyut', 'btn_submit': 'İndir', 'footer': 'Gizlilik korumalı.', 'error_large': 'Dosya çok büyük'
    },

    # --- 越南语 ---
    'vi': {
        **EN_GUIDE,
        'name': 'Tiếng Việt', 'dir': 'ltr', 'recommend': 'Đề xuất', 'badge': 'HOT',
        'seo_title': 'Chuyển đổi ICO Trực tuyến - Tạo Favicon',
        'seo_desc': 'Chuyển đổi ảnh sang ICO miễn phí. Công cụ chuyên nghiệp.',
        'keywords': 'chuyển đổi ico, tạo favicon, png sang ico',
        'h1': 'Chuyển đổi ICO', 'subtitle': 'Tạo Favicon', 'upload_label': 'Tải lên',
        'size_label': 'Kích thước', 'btn_submit': 'Tải xuống', 'footer': 'Bảo mật riêng tư.', 'error_large': 'Tệp quá lớn'
    },

    # --- 泰语 ---
    'th': {
        **EN_GUIDE,
        'name': 'ไทย', 'dir': 'ltr', 'recommend': 'แนะนำ', 'badge': 'ฮิต',
        'seo_title': 'แปลงไฟล์ ICO ออนไลน์ - สร้าง Favicon',
        'seo_desc': 'แปลงรูปภาพเป็น ICO ฟรี เครื่องมือระดับมืออาชีพ',
        'keywords': 'แปลงไฟล์ ico, สร้าง favicon, png เป็น ico',
        'h1': 'ตัวแปลง ICO', 'subtitle': 'สร้าง Favicon', 'upload_label': 'อัปโหลด',
        'size_label': 'ขนาด', 'btn_submit': 'ดาวน์โหลด', 'footer': 'ความเป็นส่วนตัว', 'error_large': 'ไฟล์ใหญ่เกินไป'
    },

    # --- 印地语 ---
    'hi': {
        **EN_GUIDE,
        'name': 'हिन्दी', 'dir': 'ltr', 'recommend': 'अनुशंसित', 'badge': 'आम',
        'seo_title': 'ICO कन्वर्टर - Favicon बनाएं',
        'seo_desc': 'छवियों को ICO में बदलें। पेशेवर उपकरण।',
        'keywords': 'ico converter, favicon generator, hindi',
        'h1': 'ICO कन्वर्टर', 'subtitle': 'Favicon जनरेटर', 'upload_label': 'अपलोड करें',
        'size_label': 'आकार', 'btn_submit': 'डाउनलोड करें', 'footer': 'गोपनीयता', 'error_large': 'फ़ाइल बहुत बड़ी है'
    },

    # --- 瑞典语 ---
    'sv': {
        **EN_GUIDE,
        'name': 'Svenska', 'dir': 'ltr', 'recommend': 'Rekommenderas', 'badge': 'TOP',
        'seo_title': 'Online ICO Konverterare - Skapa Favicon',
        'seo_desc': 'Konvertera bilder till ICO. Professionellt verktyg.',
        'keywords': 'ico konverterare, skapa favicon, png till ico',
        'h1': 'ICO Konverterare', 'subtitle': 'Favicon Generator', 'upload_label': 'Ladda upp',
        'size_label': 'Storlek', 'btn_submit': 'Ladda ner', 'footer': 'Integritetsskyddad.', 'error_large': 'Filen är för stor'
    },

    # --- 乌克兰语 ---
    'uk': {
        **EN_GUIDE,
        'name': 'Українська', 'dir': 'ltr', 'recommend': 'Стандарт', 'badge': 'ХІТ',
        'seo_title': 'Онлайн конвертер ICO - Створити Favicon',
        'seo_desc': 'Конвертувати зображення в ICO. Професійний інструмент.',
        'keywords': 'конвертер ico, створити favicon, png в ico',
        'h1': 'Конвертер ICO', 'subtitle': 'Генератор іконок', 'upload_label': 'Завантажити',
        'size_label': 'Розмір', 'btn_submit': 'Завантажити', 'footer': 'Конфіденційність.', 'error_large': 'Файл занадто великий'
    },

    # --- 阿拉伯语 ---
    'ar': {
        **EN_GUIDE,
        'name': 'العربية', 'dir': 'rtl', 'recommend': 'موصى به', 'badge': 'شائع',
        'seo_title': 'محول ICO عبر الإنترنت - إنشاء أيقونة Favicon',
        'seo_desc': 'تحويل الصور إلى صيغة ICO مجاناً. أداة احترافية.',
        'keywords': 'محول ico, انشاء favicon, تحويل الصور الى ايقونات',
        'h1': 'محول ICO', 'subtitle': 'مولد أيقونات', 'upload_label': 'رفع صورة',
        'size_label': 'الحجم', 'btn_submit': 'تحميل .ICO', 'footer': 'حماية الخصوصية.', 'error_large': 'الملف كبير جداً'
    },

    # --- 希伯来语 ---
    'he': {
        **EN_GUIDE,
        'name': 'עברית', 'dir': 'rtl', 'recommend': 'מומלץ', 'badge': 'נפוץ',
        'seo_title': 'ממיר ICO מקוון - צור Favicon',
        'seo_desc': 'המרת תמונות ל-ICO בחינם. כלי מקצועי.',
        'keywords': 'ממיר ico, יצירת favicon, המרת תמונה לאייקון',
        'h1': 'ממיר ICO', 'subtitle': 'יוצר אייקונים', 'upload_label': 'העלאת תמונה',
        'size_label': 'גודל', 'btn_submit': 'הורד .ICO', 'footer': 'פרטיות מוגנת.', 'error_large': 'קובץ גדול מדי'
    }
}

SUPPORTED_LANGS = list(TRANSLATIONS.keys())
DEFAULT_LANG = 'en'

# ==========================================
# 3. 路由与核心逻辑
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

# SEO: Robots.txt
@app.route('/robots.txt')
def robots():
    base_url = request.url_root.rstrip('/')
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /generate",
        f"Sitemap: {base_url}/sitemap.xml"
    ]
    return Response("\n".join(lines), mimetype="text/plain")

# SEO: Sitemap.xml
@app.route('/sitemap.xml')
def sitemap():
    base_url = request.url_root.rstrip('/')
    urls = []
    today = datetime.date.today().isoformat()
    for lang in SUPPORTED_LANGS:
        urls.append(f"""
        <url>
            <loc>{base_url}/{lang}</loc>
            <lastmod>{today}</lastmod>
            <changefreq>weekly</changefreq>
            <priority>{'1.0' if lang == 'en' else '0.8'}</priority>
        </url>""")

    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
        {''.join(urls)}
    </urlset>"""
    return Response(xml, mimetype="application/xml")

# Favicon: 读取本地文件
@app.route('/favicon.ico')
def favicon():
    return send_file('../favicon.ico', mimetype='image/vnd.microsoft.icon')
