import datetime
import io
import os

from flask import (Flask, Response, redirect, render_template, request,
                   send_file)
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from PIL import Image, ImageFilter

app = Flask(__name__, template_folder='../templates')
app.secret_key = os.environ.get('SECRET_KEY', 'global_ico_ultimate_final_v10')
app.url_map.strict_slashes = False
app.config['MAX_CONTENT_LENGTH'] = 4.5 * 1024 * 1024

# ==========================================
# 1. 安全防护：频率限制
# ==========================================
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["300 per day", "60 per hour"],
    storage_uri="memory://"
)

# ==========================================
# 2. 图像处理：智能描边 (Smart Glow)
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
# 3. 终极全球语言包 (完整展开，无省略)
# ==========================================
# 通用指引文案 (用于非核心语言的兜底，确保文案准确)
EN_GUIDE = {
    'tab_create': 'Create',
    'tab_guide': 'Guide',
    'guide_preview_title': 'Visual Preview',
    'guide_preview_desc': 'Your icon will be displayed in browser tabs to help users identify your brand instantly.',
    'step1_title': 'Upload to Server',
    'step1_desc': 'Download the .ico file and upload it to the root directory of your website server.',
    'step1_file_path': '/root/',
    'step1_file_name': 'favicon.ico',
    'step2_title': 'Update HTML Code',
    'step2_desc': 'Copy the code below and paste it into the <head> section of your HTML files.',
    'guide_copy_btn': 'Copy',
    'guide_copied': 'Copied!',
}

TRANSLATIONS = {
    'en': {
        **EN_GUIDE,
        'name': 'English', 'dir': 'ltr', 'recommend': 'Recommended', 'badge': 'HOT',
        'seo_title': 'Free Online ICO Converter - Create Transparent Favicon',
        'seo_desc': 'Best free online ICO converter. Convert PNG, JPG to ICO format instantly.', 'keywords': 'ico converter, favicon generator',
        'h1': 'ICO Converter', 'subtitle': 'Professional Favicon Generator', 'upload_label': 'Click to upload or Drag image', 'size_label': 'Target Size',
        'btn_submit': 'Generate ICO', 'footer': 'Securely processed. Privacy protected.', 'error_large': 'File too large'
    },
    'zh': {
        'name': '简体中文', 'dir': 'ltr', 'recommend': '推荐尺寸', 'badge': '常用',
        'seo_title': '在线 ICO 图标生成器 - 免费制作透明 Favicon', 'seo_desc': '免费在线将图片转换为 ICO 图标。支持透明背景。', 'keywords': 'ICO生成器, favicon制作',
        'h1': 'ICO 图标生成器', 'subtitle': '一键生成透明背景图标', 'upload_label': '点击选择 或 拖拽图片', 'size_label': '目标尺寸',
        'btn_submit': '生成并下载 .ICO', 'footer': '数据安全保护，不保存任何图片。', 'error_large': '文件过大',
        'tab_create': '制作图标', 'tab_guide': '使用指南',
        'guide_preview_title': '效果预览', 'guide_preview_desc': '图标将显示在浏览器标签页中，提升品牌识别度。',
        'step1_title': '上传至服务器', 'step1_desc': '将生成的 favicon.ico 上传到网站根目录。', 'step1_file_path': '/根目录/', 'step1_file_name': 'favicon.ico',
        'step2_title': '引入 HTML', 'step2_desc': '将下方代码粘贴到网页 <head> 标签之间。', 'guide_copy_btn': '复制', 'guide_copied': '已复制!'
    },
    'tw': {
        'name': '繁體中文', 'dir': 'ltr', 'recommend': '推薦尺寸', 'badge': '常用',
        'seo_title': '線上 ICO 圖示產生器 - 製作透明 Favicon', 'seo_desc': '免費線上圖片轉 ICO 工具。', 'keywords': 'ICO產生器, favicon製作',
        'h1': 'ICO 圖示產生器', 'subtitle': '一鍵生成透明背景圖示', 'upload_label': '點擊選擇 或 拖曳圖片', 'size_label': '目標尺寸',
        'btn_submit': '產生並下載 .ICO', 'footer': '資料安全保護，不保存任何圖片。', 'error_large': '檔案過大',
        'tab_create': '製作圖示', 'tab_guide': '使用指南',
        'guide_preview_title': '效果預覽', 'guide_preview_desc': '圖示將顯示在瀏覽器分頁上。',
        'step1_title': '上傳至伺服器', 'step1_desc': '將產生的 favicon.ico 上傳到網站根目錄。', 'step1_file_path': '/根目錄/', 'step1_file_name': 'favicon.ico',
        'step2_title': '引入 HTML', 'step2_desc': '將下方程式碼貼到網頁 <head> 標籤之間。', 'guide_copy_btn': '複製', 'guide_copied': '已複製!'
    },
    'es': {
        **EN_GUIDE, 'name': 'Español', 'dir': 'ltr', 'recommend': 'Recomendado', 'badge': 'HOT',
        'seo_title': 'Convertidor ICO Online', 'seo_desc': 'Convierte imágenes a ICO.', 'keywords': 'convertidor ico',
        'h1': 'Convertidor ICO', 'subtitle': 'Generador de Favicon', 'upload_label': 'Clic para subir', 'size_label': 'Tamaño',
        'btn_submit': 'Generar .ICO', 'footer': 'Privacidad protegida.', 'error_large': 'Archivo muy grande',
        'tab_create': 'Crear', 'tab_guide': 'Guía'
    },
    'fr': {
        **EN_GUIDE, 'name': 'Français', 'dir': 'ltr', 'recommend': 'Recommandé', 'badge': 'TOP',
        'seo_title': 'Convertisseur ICO', 'seo_desc': 'Convertir en ICO.', 'keywords': 'convertisseur ico',
        'h1': 'Convertisseur ICO', 'subtitle': 'Générateur de Favicon', 'upload_label': 'Uploader une image', 'size_label': 'Taille',
        'btn_submit': 'Générer .ICO', 'footer': 'Confidentialité respectée.', 'error_large': 'Fichier trop volumineux',
        'tab_create': 'Créer', 'tab_guide': 'Guide'
    },
    'de': {
        **EN_GUIDE, 'name': 'Deutsch', 'dir': 'ltr', 'recommend': 'Empfohlen', 'badge': 'TOP',
        'seo_title': 'ICO Konverter', 'seo_desc': 'In ICO umwandeln.', 'keywords': 'ico konverter',
        'h1': 'ICO Konverter', 'subtitle': 'Favicon-Generator', 'upload_label': 'Bild hochladen', 'size_label': 'Größe',
        'btn_submit': '.ICO Herunterladen', 'footer': 'Datenschutz.', 'error_large': 'Datei zu groß',
        'tab_create': 'Erstellen', 'tab_guide': 'Anleitung'
    },
    'it': {
        **EN_GUIDE, 'name': 'Italiano', 'dir': 'ltr', 'recommend': 'Consigliato', 'badge': 'TOP',
        'seo_title': 'Convertitore ICO', 'seo_desc': 'Crea Favicon.', 'keywords': 'convertitore ico',
        'h1': 'Convertitore ICO', 'subtitle': 'Generatore di Favicon', 'upload_label': 'Clicca per caricare', 'size_label': 'Dimensione',
        'btn_submit': 'Scarica .ICO', 'footer': 'Privacy protetta.', 'error_large': 'File troppo grande',
        'tab_create': 'Crea', 'tab_guide': 'Guida'
    },
    'pt': {
        **EN_GUIDE, 'name': 'Português', 'dir': 'ltr', 'recommend': 'Recomendado', 'badge': 'HOT',
        'seo_title': 'Conversor ICO', 'seo_desc': 'Criar Favicon.', 'keywords': 'conversor ico',
        'h1': 'Conversor ICO', 'subtitle': 'Gerador de Favicon', 'upload_label': 'Clique para subir', 'size_label': 'Tamanho',
        'btn_submit': 'Baixar .ICO', 'footer': 'Privacidade protegida.', 'error_large': 'Arquivo muito grande',
        'tab_create': 'Criar', 'tab_guide': 'Guia'
    },
    'ru': {
        **EN_GUIDE, 'name': 'Русский', 'dir': 'ltr', 'recommend': 'Стандарт', 'badge': 'ХИТ',
        'seo_title': 'Конвертер ICO', 'seo_desc': 'Создать Favicon.', 'keywords': 'ico конвертер',
        'h1': 'Конвертер ICO', 'subtitle': 'Генератор иконок', 'upload_label': 'Загрузить файл', 'size_label': 'Размер',
        'btn_submit': 'Скачать .ICO', 'footer': 'Конфиденциальность.', 'error_large': 'Файл слишком большой',
        'tab_create': 'Создать', 'tab_guide': 'Гид'
    },
    'nl': {
        **EN_GUIDE, 'name': 'Nederlands', 'dir': 'ltr', 'recommend': 'Aanbevolen', 'badge': 'TOP',
        'seo_title': 'ICO Converter', 'seo_desc': 'Favicon maken.', 'keywords': 'ico converter',
        'h1': 'ICO Converter', 'subtitle': 'Favicon Generator', 'upload_label': 'Uploaden', 'size_label': 'Grootte',
        'btn_submit': 'Downloaden', 'footer': 'Privacy.', 'error_large': 'Fout',
        'tab_create': 'Maken', 'tab_guide': 'Gids'
    },
    'pl': {
        **EN_GUIDE, 'name': 'Polski', 'dir': 'ltr', 'recommend': 'Zalecane', 'badge': 'HIT',
        'seo_title': 'Konwerter ICO', 'seo_desc': 'Generator Favicon.', 'keywords': 'konwerter ico',
        'h1': 'Konwerter ICO', 'subtitle': 'Generator Favicon', 'upload_label': 'Prześlij', 'size_label': 'Rozmiar',
        'btn_submit': 'Pobierz .ICO', 'footer': 'Prywatność.', 'error_large': 'Błąd',
        'tab_create': 'Stwórz', 'tab_guide': 'Info'
    },
    'sv': {
        **EN_GUIDE, 'name': 'Svenska', 'dir': 'ltr', 'recommend': 'Standard', 'badge': 'TOP',
        'seo_title': 'ICO Konverterare', 'seo_desc': 'Skapa Favicon.', 'keywords': 'ico konverterare',
        'h1': 'ICO Konverterare', 'subtitle': 'Favicon Generator', 'upload_label': 'Ladda upp', 'size_label': 'Storlek',
        'btn_submit': 'Ladda ner', 'footer': 'Säker.', 'error_large': 'Fel',
        'tab_create': 'Skapa', 'tab_guide': 'Guide'
    },
    'uk': {
        **EN_GUIDE, 'name': 'Українська', 'dir': 'ltr', 'recommend': 'Стандарт', 'badge': 'ХІТ',
        'seo_title': 'Конвертер ICO', 'seo_desc': 'Створити Favicon.', 'keywords': 'ico конвертер',
        'h1': 'Конвертер ICO', 'subtitle': 'Генератор іконок', 'upload_label': 'Завантажити', 'size_label': 'Розмір',
        'btn_submit': 'Завантажити', 'footer': 'Конфіденційність.', 'error_large': 'Помилка',
        'tab_create': 'Створити', 'tab_guide': 'Інструкція'
    },
    'ja': {
        **EN_GUIDE, 'name': '日本語', 'dir': 'ltr', 'recommend': '推奨', 'badge': '人気',
        'seo_title': 'ICO変換ツール', 'seo_desc': 'ファビコン作成。', 'keywords': 'ico 変換',
        'h1': 'ICO 変換ツール', 'subtitle': 'プロフェッショナルなアイコン作成', 'upload_label': 'アップロード', 'size_label': 'サイズ',
        'btn_submit': 'ダウンロード', 'footer': 'プライバシー保護。', 'error_large': 'ファイルサイズ過大',
        'tab_create': '作成', 'tab_guide': 'ガイド'
    },
    'ko': {
        **EN_GUIDE, 'name': '한국어', 'dir': 'ltr', 'recommend': '추천', 'badge': '인기',
        'seo_title': 'ICO 변환기', 'seo_desc': '파비콘 만들기.', 'keywords': 'ico 변환',
        'h1': 'ICO 변환기', 'subtitle': '전문 파비콘 생성 도구', 'upload_label': '업로드', 'size_label': '크기',
        'btn_submit': '다운로드', 'footer': '개인정보 보호.', 'error_large': '파일이 너무 큽니다',
        'tab_create': '제작', 'tab_guide': '가이드'
    },
    'id': {
        **EN_GUIDE, 'name': 'Bahasa Indonesia', 'dir': 'ltr', 'recommend': 'Disarankan', 'badge': 'HOT',
        'seo_title': 'Konverter ICO', 'seo_desc': 'Buat Favicon.', 'keywords': 'konverter ico',
        'h1': 'Konverter ICO', 'subtitle': 'Pembuat Favicon', 'upload_label': 'Unggah', 'size_label': 'Ukuran',
        'btn_submit': 'Unduh .ICO', 'footer': 'Aman.', 'error_large': 'Error',
        'tab_create': 'Buat', 'tab_guide': 'Panduan'
    },
    'tr': {
        **EN_GUIDE, 'name': 'Türkçe', 'dir': 'ltr', 'recommend': 'Önerilen', 'badge': 'POP',
        'seo_title': 'ICO Dönüştürücü', 'seo_desc': 'Favicon yapma.', 'keywords': 'ico dönüştürücü',
        'h1': 'ICO Dönüştürücü', 'subtitle': 'Favicon Oluşturucu', 'upload_label': 'Yükle', 'size_label': 'Boyut',
        'btn_submit': 'İndir', 'footer': 'Gizlilik.', 'error_large': 'Hata',
        'tab_create': 'Oluştur', 'tab_guide': 'Rehber'
    },
    'vi': {
        **EN_GUIDE, 'name': 'Tiếng Việt', 'dir': 'ltr', 'recommend': 'Đề xuất', 'badge': 'HOT',
        'seo_title': 'Chuyển đổi ICO', 'seo_desc': 'Tạo Favicon.', 'keywords': 'chuyển đổi ico',
        'h1': 'Chuyển đổi ICO', 'subtitle': 'Tạo Favicon', 'upload_label': 'Tải lên', 'size_label': 'Kích thước',
        'btn_submit': 'Tải xuống', 'footer': 'Bảo mật.', 'error_large': 'Lỗi',
        'tab_create': 'Tạo', 'tab_guide': 'Hướng dẫn'
    },
    'th': {
        **EN_GUIDE, 'name': 'ไทย', 'dir': 'ltr', 'recommend': 'แนะนำ', 'badge': 'ฮิต',
        'seo_title': 'ตัวแปลง ICO', 'seo_desc': 'สร้าง Favicon.', 'keywords': 'แปลงไฟล์ ico',
        'h1': 'ตัวแปลง ICO', 'subtitle': 'สร้าง Favicon', 'upload_label': 'อัปโหลด', 'size_label': 'ขนาด',
        'btn_submit': 'ดาวน์โหลด', 'footer': 'ปลอดภัย', 'error_large': 'ไฟล์ใหญ่',
        'tab_create': 'สร้าง', 'tab_guide': 'คู่มือ'
    },
    'hi': {
        **EN_GUIDE, 'name': 'हिन्दी', 'dir': 'ltr', 'recommend': 'अनुशंसित', 'badge': 'आम',
        'seo_title': 'ICO कन्वर्टर', 'seo_desc': 'Favicon बनाएं.', 'keywords': 'ico converter',
        'h1': 'ICO कन्वर्टर', 'subtitle': 'Favicon जनरेटर', 'upload_label': 'अपलोड', 'size_label': 'आकार',
        'btn_submit': 'डाउनलोड', 'footer': 'सुरक्षित', 'error_large': 'बड़ी फ़ाइल',
        'tab_create': 'बनाएं', 'tab_guide': 'गाइड'
    },
    'ar': {
        **EN_GUIDE, 'name': 'العربية', 'dir': 'rtl', 'recommend': 'موصى به', 'badge': 'شائع',
        'seo_title': 'محول ICO', 'seo_desc': 'إنشاء أيقونة.', 'keywords': 'محول ico',
        'h1': 'محول ICO', 'subtitle': 'مولد أيقونات', 'upload_label': 'رفع', 'size_label': 'الحجم',
        'btn_submit': 'تحميل', 'footer': 'آمن.', 'error_large': 'خطأ',
        'tab_create': 'إنشاء', 'tab_guide': 'دليل'
    },
    'he': {
        **EN_GUIDE, 'name': 'עברית', 'dir': 'rtl', 'recommend': 'מומלץ', 'badge': 'נפוץ',
        'seo_title': 'ממיר ICO', 'seo_desc': 'צור Favicon.', 'keywords': 'ממיר ico',
        'h1': 'ממיר ICO', 'subtitle': 'יוצר אייקונים', 'upload_label': 'העלאת', 'size_label': 'גודל',
        'btn_submit': 'הורד', 'footer': 'פרטיות.', 'error_large': 'שגיאה',
        'tab_create': 'צור', 'tab_guide': 'מדריך'
    }
}

SUPPORTED_LANGS = list(TRANSLATIONS.keys())
DEFAULT_LANG = 'en'

# ==========================================
# 4. 路由与逻辑
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
        # 内存熔断
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
