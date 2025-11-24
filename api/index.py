import io
import os

from flask import (Flask, Response, redirect, render_template, request,
                   send_file)
from PIL import Image

app = Flask(__name__, template_folder='../templates')
app.secret_key = os.environ.get('SECRET_KEY', 'global_ico_ultimate_prod')
app.url_map.strict_slashes = False
app.config['MAX_CONTENT_LENGTH'] = 4.5 * 1024 * 1024

# ==========================================
# 1. 终极全球语言包 (22种语言 / Top 95% Coverage)
# ==========================================
TRANSLATIONS = {
    'en': { 'name': 'English', 'dir': 'ltr', 'seo_title': 'Free Online ICO Converter - Create Transparent Favicon', 'seo_desc': 'Convert PNG, JPG to ICO format online. Support transparent background. Professional Favicon generator tool.', 'h1': 'ICO Converter', 'subtitle': 'Professional Favicon Generator', 'upload_label': 'Click to upload or Drag image', 'size_label': 'Target Size', 'btn_submit': 'Generate ICO', 'footer': 'Securely processed. Privacy protected.', 'error_large': 'File too large (Max 4MB)' },
    'zh': { 'name': '简体中文', 'dir': 'ltr', 'seo_title': '在线 ICO 图标生成器 - 免费制作透明 Favicon', 'seo_desc': '免费在线将图片转换为 ICO 图标。支持透明背景，一键生成。网站图标制作专业工具。', 'h1': 'ICO 图标生成器', 'subtitle': '一键生成透明背景图标', 'upload_label': '点击选择 或 拖拽图片', 'size_label': '目标尺寸', 'btn_submit': '生成并下载 .ICO', 'footer': '数据安全保护，不保存任何图片。', 'error_large': '文件过大 (最大 4MB)' },
    'tw': { 'name': '繁體中文', 'dir': 'ltr', 'seo_title': '線上 ICO 圖示產生器 - 製作透明 Favicon', 'seo_desc': '免費線上圖片轉 ICO 工具。支援透明背景。專業網頁圖示製作工具。', 'h1': 'ICO 圖示產生器', 'subtitle': '一鍵生成透明背景圖示', 'upload_label': '點擊選擇 或 拖曳圖片', 'size_label': '目標尺寸', 'btn_submit': '產生並下載 .ICO', 'footer': '資料安全保護，不保存任何圖片。', 'error_large': '檔案過大 (最大 4MB)' },
    'es': { 'name': 'Español', 'dir': 'ltr', 'seo_title': 'Convertidor ICO Online', 'seo_desc': 'Convierte imágenes a formato ICO.', 'h1': 'Convertidor ICO', 'subtitle': 'Generador de Favicon Profesional', 'upload_label': 'Clic para subir', 'size_label': 'Tamaño', 'btn_submit': 'Generar .ICO', 'footer': 'Privacidad protegida.', 'error_large': 'Archivo muy grande' },
    'fr': { 'name': 'Français', 'dir': 'ltr', 'seo_title': 'Convertisseur ICO', 'seo_desc': 'Convertir en ICO.', 'h1': 'Convertisseur ICO', 'subtitle': 'Générateur de Favicon', 'upload_label': 'Uploader une image', 'size_label': 'Taille', 'btn_submit': 'Générer .ICO', 'footer': 'Confidentialité respectée.', 'error_large': 'Fichier trop volumineux' },
    'de': { 'name': 'Deutsch', 'dir': 'ltr', 'seo_title': 'ICO Konverter', 'seo_desc': 'In ICO umwandeln.', 'h1': 'ICO Konverter', 'subtitle': 'Favicon-Generator', 'upload_label': 'Bild hochladen', 'size_label': 'Größe', 'btn_submit': '.ICO Herunterladen', 'footer': 'Datenschutz.', 'error_large': 'Datei zu groß' },
    'it': { 'name': 'Italiano', 'dir': 'ltr', 'seo_title': 'Convertitore ICO', 'seo_desc': 'Converti in ICO.', 'h1': 'Convertitore ICO', 'subtitle': 'Generatore di Favicon', 'upload_label': 'Clicca per caricare', 'size_label': 'Dimensione', 'btn_submit': 'Scarica .ICO', 'footer': 'Privacy protetta.', 'error_large': 'File troppo grande' },
    'pt': { 'name': 'Português', 'dir': 'ltr', 'seo_title': 'Conversor ICO', 'seo_desc': 'Converta para ICO.', 'h1': 'Conversor de ICO', 'subtitle': 'Gerador de Favicon', 'upload_label': 'Clique para subir', 'size_label': 'Tamanho', 'btn_submit': 'Baixar .ICO', 'footer': 'Privacidade protegida.', 'error_large': 'Arquivo muito grande' },
    'ru': { 'name': 'Русский', 'dir': 'ltr', 'seo_title': 'Конвертер ICO', 'seo_desc': 'Конвертировать в ICO.', 'h1': 'Конвертер ICO', 'subtitle': 'Генератор иконок', 'upload_label': 'Загрузить файл', 'size_label': 'Размер', 'btn_submit': 'Скачать .ICO', 'footer': 'Конфиденциальность.', 'error_large': 'Файл слишком большой' },
    'nl': { 'name': 'Nederlands', 'dir': 'ltr', 'seo_title': 'ICO Converter', 'seo_desc': 'Naar ICO converteren.', 'h1': 'ICO Converter', 'subtitle': 'Favicon Generator', 'upload_label': 'Klik om te uploaden', 'size_label': 'Grootte', 'btn_submit': 'Downloaden', 'footer': 'Privacy beschermd.', 'error_large': 'Bestand te groot' },
    'pl': { 'name': 'Polski', 'dir': 'ltr', 'seo_title': 'Konwerter ICO', 'seo_desc': 'Konwertuj na ICO.', 'h1': 'Konwerter ICO', 'subtitle': 'Generator Favicon', 'upload_label': 'Prześlij plik', 'size_label': 'Rozmiar', 'btn_submit': 'Pobierz .ICO', 'footer': 'Ochrona prywatności.', 'error_large': 'Plik zbyt duży' },
    'ja': { 'name': '日本語', 'dir': 'ltr', 'seo_title': 'ICO変換ツール', 'seo_desc': 'ICO形式に変換。', 'h1': 'ICO 変換ツール', 'subtitle': 'プロフェッショナルなアイコン作成', 'upload_label': 'アップロード', 'size_label': 'サイズ', 'btn_submit': 'ダウンロード', 'footer': 'プライバシー保護。', 'error_large': 'ファイルサイズ過大' },
    'ko': { 'name': '한국어', 'dir': 'ltr', 'seo_title': 'ICO 변환기', 'seo_desc': 'ICO 변환 도구.', 'h1': 'ICO 변환기', 'subtitle': '전문 파비콘 생성 도구', 'upload_label': '업로드', 'size_label': '크기', 'btn_submit': '다운로드', 'footer': '개인정보 보호.', 'error_large': '파일이 너무 큽니다' },
    'id': { 'name': 'Bahasa Indonesia', 'dir': 'ltr', 'seo_title': 'Konverter ICO', 'seo_desc': 'Ubah ke ICO.', 'h1': 'Konverter ICO', 'subtitle': 'Pembuat Favicon', 'upload_label': 'Unggah gambar', 'size_label': 'Ukuran', 'btn_submit': 'Unduh .ICO', 'footer': 'Privasi dilindungi.', 'error_large': 'File terlalu besar' },
    'tr': { 'name': 'Türkçe', 'dir': 'ltr', 'seo_title': 'ICO Dönüştürücü', 'seo_desc': 'ICO\'ya çevir.', 'h1': 'ICO Dönüştürücü', 'subtitle': 'Favicon Oluşturucu', 'upload_label': 'Dosya yükle', 'size_label': 'Boyut', 'btn_submit': 'İndir', 'footer': 'Gizlilik korumalı.', 'error_large': 'Dosya çok büyük' },
    'vi': { 'name': 'Tiếng Việt', 'dir': 'ltr', 'seo_title': 'Chuyển đổi ICO', 'seo_desc': 'Sang định dạng ICO.', 'h1': 'Chuyển đổi ICO', 'subtitle': 'Tạo Favicon', 'upload_label': 'Tải lên', 'size_label': 'Kích thước', 'btn_submit': 'Tải xuống', 'footer': 'Bảo mật riêng tư.', 'error_large': 'Tệp quá lớn' },
    'th': { 'name': 'ไทย', 'dir': 'ltr', 'seo_title': 'ตัวแปลง ICO', 'seo_desc': 'แปลงเป็น ICO', 'h1': 'ตัวแปลง ICO', 'subtitle': 'สร้าง Favicon', 'upload_label': 'อัปโหลด', 'size_label': 'ขนาด', 'btn_submit': 'ดาวน์โหลด', 'footer': 'ความเป็นส่วนตัว', 'error_large': 'ไฟล์ใหญ่เกินไป' },
    'hi': { 'name': 'हिन्दी', 'dir': 'ltr', 'seo_title': 'ICO कन्वर्टर', 'seo_desc': 'ICO में बदलें', 'h1': 'ICO कन्वर्टर', 'subtitle': 'Favicon जनरेटर', 'upload_label': 'अपलोड करें', 'size_label': 'आकार', 'btn_submit': 'डाउनलोड करें', 'footer': 'गोपनीयता', 'error_large': 'फ़ाइल बहुत बड़ी है' },
    'sv': { 'name': 'Svenska', 'dir': 'ltr', 'seo_title': 'ICO Konverterare', 'seo_desc': 'Till ICO.', 'h1': 'ICO Konverterare', 'subtitle': 'Favicon Generator', 'upload_label': 'Ladda upp', 'size_label': 'Storlek', 'btn_submit': 'Ladda ner', 'footer': 'Integritetsskyddad.', 'error_large': 'Filen är för stor' },
    'uk': { 'name': 'Українська', 'dir': 'ltr', 'seo_title': 'Конвертер ICO', 'seo_desc': 'В ICO.', 'h1': 'Конвертер ICO', 'subtitle': 'Генератор іконок', 'upload_label': 'Завантажити', 'size_label': 'Розмір', 'btn_submit': 'Завантажити', 'footer': 'Конфіденційність.', 'error_large': 'Файл занадто великий' },
    'ar': { 'name': 'العربية', 'dir': 'rtl', 'seo_title': 'محول ICO', 'seo_desc': 'تحويل إلى ICO.', 'h1': 'محول ICO', 'subtitle': 'مولد أيقونات', 'upload_label': 'رفع صورة', 'size_label': 'الحجم', 'btn_submit': 'تحميل .ICO', 'footer': 'حماية الخصوصية.', 'error_large': 'الملف كبير جداً' },
    'he': { 'name': 'עברית', 'dir': 'rtl', 'seo_title': 'ממיר ICO', 'seo_desc': 'להמיר ל-ICO.', 'h1': 'ממיר ICO', 'subtitle': 'יוצר אייקונים', 'upload_label': 'העלאת תמונה', 'size_label': 'גודל', 'btn_submit': 'הורד .ICO', 'footer': 'פרטיות מוגנת.', 'error_large': 'קובץ גדול מדי' }
}

SUPPORTED_LANGS = list(TRANSLATIONS.keys())
DEFAULT_LANG = 'en'

# ===========================
# 2. 路由逻辑
# ===========================

def render_index(lang_code):
    if lang_code not in SUPPORTED_LANGS:
        return redirect(f"/{DEFAULT_LANG}")

    base_url = request.url_root.rstrip('/')
    alternates = [{'lang': l, 'href': f"{base_url}/{l}"} for l in SUPPORTED_LANGS]

    return render_template(
        'index.html',
        t=TRANSLATIONS[lang_code],
        current_lang=lang_code,
        alternates=alternates
    )

# 显式注册所有路由，解决 Vercel 404 问题
for lang in SUPPORTED_LANGS:
    app.add_url_rule(
        f'/{lang}',
        endpoint=f'view_{lang}',
        view_func=render_index,
        defaults={'lang_code': lang}
    )

@app.errorhandler(404)
def page_not_found(e):
    return redirect(f"/{DEFAULT_LANG}")

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
    # 修复 Vercel 图像读取问题
    if 'file' not in request.files: return "Error", 400
    file = request.files['file']
    if file.filename == '': return "Error", 400

    try:
        size = int(request.form.get('size', '32'))

        # 必须先读入内存
        file_bytes = file.read()
        if len(file_bytes) == 0: return "Error: Empty file", 400
        input_stream = io.BytesIO(file_bytes)

        img = Image.open(input_stream)
        if img.mode != "RGBA":
            img = img.convert("RGBA")

        img = img.resize((size, size), Image.Resampling.LANCZOS)

        output_stream = io.BytesIO()
        img.save(output_stream, format='ICO', sizes=[(size, size)])
        output_stream.seek(0)

        return send_file(
            output_stream,
            mimetype='image/x-icon',
            as_attachment=True,
            download_name='favicon.ico'
        )
    except Exception as e:
        print(f"Error: {str(e)}")
        return "Invalid image file", 500

@app.route('/sitemap.xml')
def sitemap():
    base_url = request.url_root.rstrip('/')
    urls = []
    for lang in SUPPORTED_LANGS:
        urls.append(f"<url><loc>{base_url}/{lang}</loc><changefreq>weekly</changefreq></url>")
    xml = f"""<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{''.join(urls)}</urlset>"""
    return Response(xml, mimetype="application/xml")
