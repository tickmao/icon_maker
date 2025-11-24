import io
import os

from flask import (Flask, Response, redirect, render_template, request,
                   send_file)
from PIL import Image

app = Flask(__name__, template_folder='../templates')
app.secret_key = os.environ.get('SECRET_KEY', 'global_ico_ultimate_v1')
# 允许 URL 末尾带不带斜杠都能访问
app.url_map.strict_slashes = False
app.config['MAX_CONTENT_LENGTH'] = 4.5 * 1024 * 1024

# ==========================================
# 1. 终极全球语言包 (22种语言 / Top 95% Coverage)
# ==========================================
TRANSLATIONS = {
    # --- 英语 (基准) ---
    'en': {
        'name': 'English', 'dir': 'ltr',
        'seo_title': 'Free Online ICO Converter - Create Transparent Favicon',
        'seo_desc': 'Convert PNG, JPG to ICO format online. Support transparent background. Professional Favicon generator tool.',
        'h1': 'ICO Converter', 'subtitle': 'Professional Favicon Generator',
        'upload_label': 'Click to upload or Drag image', 'size_label': 'Target Size',
        'btn_submit': 'Generate ICO', 'footer': 'Securely processed. Privacy protected.',
        'error_large': 'File too large (Max 4MB)'
    },
    # --- 中文圈 ---
    'zh': {
        'name': '简体中文', 'dir': 'ltr',
        'seo_title': '在线 ICO 图标生成器 - 免费制作透明 Favicon',
        'seo_desc': '免费在线将图片转换为 ICO 图标。支持透明背景，一键生成。网站图标制作专业工具。',
        'h1': 'ICO 图标生成器', 'subtitle': '一键生成透明背景图标',
        'upload_label': '点击选择 或 拖拽图片', 'size_label': '目标尺寸',
        'btn_submit': '生成并下载 .ICO', 'footer': '数据安全保护，不保存任何图片。',
        'error_large': '文件过大 (最大 4MB)'
    },
    'tw': {
        'name': '繁體中文', 'dir': 'ltr',
        'seo_title': '線上 ICO 圖示產生器 - 製作透明 Favicon',
        'seo_desc': '免費線上圖片轉 ICO 工具。支援透明背景。專業網頁圖示製作工具。',
        'h1': 'ICO 圖示產生器', 'subtitle': '一鍵生成透明背景圖示',
        'upload_label': '點擊選擇 或 拖曳圖片', 'size_label': '目標尺寸',
        'btn_submit': '產生並下載 .ICO', 'footer': '資料安全保護，不保存任何圖片。',
        'error_large': '檔案過大 (最大 4MB)'
    },
    # --- 欧洲核心 ---
    'es': { # 西班牙语 (全球第二大母语)
        'name': 'Español', 'dir': 'ltr',
        'seo_title': 'Convertidor ICO Online - Crear Favicon Transparente',
        'seo_desc': 'Convierte imágenes a formato ICO en línea. Generador de Favicon profesional.',
        'h1': 'Convertidor ICO', 'subtitle': 'Generador de Favicon Profesional',
        'upload_label': 'Clic para subir o arrastrar', 'size_label': 'Tamaño',
        'btn_submit': 'Generar .ICO', 'footer': 'Privacidad protegida.', 'error_large': 'Archivo muy grande'
    },
    'fr': { # 法语
        'name': 'Français', 'dir': 'ltr',
        'seo_title': 'Convertisseur ICO en ligne - Créer Favicon',
        'seo_desc': 'Convertir image en ICO gratuitement. Outil professionnel.',
        'h1': 'Convertisseur ICO', 'subtitle': 'Générateur de Favicon',
        'upload_label': 'Cliquez ou glissez l\'image', 'size_label': 'Taille',
        'btn_submit': 'Générer .ICO', 'footer': 'Confidentialité respectée.', 'error_large': 'Fichier trop volumineux'
    },
    'de': { # 德语
        'name': 'Deutsch', 'dir': 'ltr',
        'seo_title': 'Online ICO Konverter - Favicon erstellen',
        'seo_desc': 'Bilder online in ICO umwandeln. Professionelles Werkzeug.',
        'h1': 'ICO Konverter', 'subtitle': 'Favicon-Generator',
        'upload_label': 'Klicken oder Bild ziehen', 'size_label': 'Größe',
        'btn_submit': '.ICO Herunterladen', 'footer': 'Datenschutz.', 'error_large': 'Datei zu groß'
    },
    'it': { # 意大利语
        'name': 'Italiano', 'dir': 'ltr',
        'seo_title': 'Convertitore ICO Online - Crea Favicon',
        'seo_desc': 'Converti immagini in ICO online. Strumento professionale.',
        'h1': 'Convertitore ICO', 'subtitle': 'Generatore di Favicon',
        'upload_label': 'Clicca per caricare', 'size_label': 'Dimensione',
        'btn_submit': 'Scarica .ICO', 'footer': 'Privacy protetta.', 'error_large': 'File troppo grande'
    },
    'pt': { # 葡萄牙语 (巴西)
        'name': 'Português', 'dir': 'ltr',
        'seo_title': 'Conversor ICO Online - Criar Favicon',
        'seo_desc': 'Converta imagens para ICO. Melhor gerador de Favicon grátis.',
        'h1': 'Conversor de ICO', 'subtitle': 'Gerador de Favicon',
        'upload_label': 'Clique ou arraste a imagem', 'size_label': 'Tamanho',
        'btn_submit': 'Baixar .ICO', 'footer': 'Privacidade protegida.', 'error_large': 'Arquivo muito grande'
    },
    'ru': { # 俄语
        'name': 'Русский', 'dir': 'ltr',
        'seo_title': 'Онлайн конвертер ICO - Создать Favicon',
        'seo_desc': 'Конвертировать PNG, JPG в ICO онлайн. Профессиональный инструмент.',
        'h1': 'Конвертер ICO', 'subtitle': 'Генератор иконок',
        'upload_label': 'Нажмите или перетащите файл', 'size_label': 'Размер',
        'btn_submit': 'Скачать .ICO', 'footer': 'Конфиденциальность.', 'error_large': 'Файл слишком большой'
    },
    'nl': { # 荷兰语
        'name': 'Nederlands', 'dir': 'ltr',
        'seo_title': 'Online ICO Converter - Favicon Maken',
        'seo_desc': 'Afbeeldingen converteren naar ICO. Professionele tool.',
        'h1': 'ICO Converter', 'subtitle': 'Favicon Generator',
        'upload_label': 'Klik om te uploaden', 'size_label': 'Grootte',
        'btn_submit': '.ICO Downloaden', 'footer': 'Privacy beschermd.', 'error_large': 'Bestand te groot'
    },
    'pl': { # 波兰语
        'name': 'Polski', 'dir': 'ltr',
        'seo_title': 'Konwerter ICO Online - Stwórz Favicon',
        'seo_desc': 'Konwertuj obrazy na format ICO. Profesjonalne narzędzie.',
        'h1': 'Konwerter ICO', 'subtitle': 'Generator Favicon',
        'upload_label': 'Kliknij, aby przesłać', 'size_label': 'Rozmiar',
        'btn_submit': 'Pobierz .ICO', 'footer': 'Ochrona prywatności.', 'error_large': 'Plik zbyt duży'
    },
    # --- 亚洲/其他重要市场 ---
    'ja': { # 日语
        'name': '日本語', 'dir': 'ltr',
        'seo_title': 'ICO変換ツール - 無料でFavicon作成',
        'seo_desc': '画像をICO形式に変換。プロフェッショナルな作成ツール。',
        'h1': 'ICO 変換ツール', 'subtitle': 'プロフェッショナルなアイコン作成',
        'upload_label': 'クリック または ドラッグ', 'size_label': 'サイズ',
        'btn_submit': 'ダウンロード', 'footer': 'プライバシー保護。', 'error_large': 'ファイルサイズ過大'
    },
    'ko': { # 韩语
        'name': '한국어', 'dir': 'ltr',
        'seo_title': 'ICO 변환기 - 파비콘 만들기',
        'seo_desc': 'ICO 변환 도구. 전문 파비콘 생성기.',
        'h1': 'ICO 변환기', 'subtitle': '전문 파비콘 생성 도구',
        'upload_label': '클릭하여 업로드', 'size_label': '크기',
        'btn_submit': '다운로드', 'footer': '개인정보 보호.', 'error_large': '파일이 너무 큽니다'
    },
    'id': { # 印尼语 (巨大市场)
        'name': 'Bahasa Indonesia', 'dir': 'ltr',
        'seo_title': 'Konverter ICO Online - Buat Favicon',
        'seo_desc': 'Ubah gambar menjadi ICO online. Alat Favicon profesional.',
        'h1': 'Konverter ICO', 'subtitle': 'Pembuat Favicon',
        'upload_label': 'Klik untuk mengunggah', 'size_label': 'Ukuran',
        'btn_submit': 'Unduh .ICO', 'footer': 'Privasi dilindungi.', 'error_large': 'File terlalu besar'
    },
    'tr': { # 土耳其语
        'name': 'Türkçe', 'dir': 'ltr',
        'seo_title': 'Online ICO Dönüştürücü - Favicon Yapma',
        'seo_desc': 'Resimleri ICO formatına çevirin. Profesyonel araç.',
        'h1': 'ICO Dönüştürücü', 'subtitle': 'Favicon Oluşturucu',
        'upload_label': 'Yüklemek için tıklayın', 'size_label': 'Boyut',
        'btn_submit': '.ICO İndir', 'footer': 'Gizlilik korumalı.', 'error_large': 'Dosya çok büyük'
    },
    'vi': { # 越南语
        'name': 'Tiếng Việt', 'dir': 'ltr',
        'seo_title': 'Chuyển đổi ICO Trực tuyến - Tạo Favicon',
        'seo_desc': 'Chuyển đổi ảnh sang ICO miễn phí. Công cụ chuyên nghiệp.',
        'h1': 'Chuyển đổi ICO', 'subtitle': 'Tạo Favicon nhanh chóng',
        'upload_label': 'Nhấp để tải lên', 'size_label': 'Kích thước',
        'btn_submit': 'Tải xuống .ICO', 'footer': 'Bảo mật riêng tư.', 'error_large': 'Tệp quá lớn'
    },
    'th': { # 泰语
        'name': 'ไทย', 'dir': 'ltr',
        'seo_title': 'แปลงไฟล์ ICO ออนไลน์ - สร้าง Favicon',
        'seo_desc': 'แปลงรูปภาพเป็น ICO ฟรี เครื่องมือระดับมืออาชีพ',
        'h1': 'ตัวแปลง ICO', 'subtitle': 'สร้าง Favicon ทันที',
        'upload_label': 'คลิกเพื่ออัปโหลด', 'size_label': 'ขนาด',
        'btn_submit': 'ดาวน์โหลด .ICO', 'footer': 'คุ้มครองความเป็นส่วนตัว', 'error_large': 'ไฟล์ใหญ่เกินไป'
    },
    'hi': { # 印地语
        'name': 'हिन्दी', 'dir': 'ltr',
        'seo_title': 'ICO कन्वर्टर - Favicon बनाएं',
        'seo_desc': 'छवियों को ICO में बदलें। पेशेवर उपकरण।',
        'h1': 'ICO कन्वर्टर', 'subtitle': 'Favicon जनरेटर',
        'upload_label': 'अपलोड करने के लिए क्लिक करें', 'size_label': 'आकार',
        'btn_submit': '.ICO डाउनलोड करें', 'footer': 'गोपनीयता सुरक्षित।', 'error_large': 'फ़ाइल बहुत बड़ी है'
    },
    'sv': { # 瑞典语
        'name': 'Svenska', 'dir': 'ltr',
        'seo_title': 'Online ICO Konverterare - Skapa Favicon',
        'seo_desc': 'Konvertera bilder till ICO. Professionellt verktyg.',
        'h1': 'ICO Konverterare', 'subtitle': 'Favicon Generator',
        'upload_label': 'Klicka för att ladda upp', 'size_label': 'Storlek',
        'btn_submit': 'Ladda ner .ICO', 'footer': 'Integritetsskyddad.', 'error_large': 'Filen är för stor'
    },
    'uk': { # 乌克兰语
        'name': 'Українська', 'dir': 'ltr',
        'seo_title': 'Онлайн конвертер ICO - Створити Favicon',
        'seo_desc': 'Конвертувати зображення в ICO. Професійний інструмент.',
        'h1': 'Конвертер ICO', 'subtitle': 'Генератор іконок',
        'upload_label': 'Натисніть для завантаження', 'size_label': 'Розмір',
        'btn_submit': 'Завантажити .ICO', 'footer': 'Конфіденційність.', 'error_large': 'Файл занадто великий'
    },
    # --- RTL 语言 (从右向左) ---
    'ar': { # 阿拉伯语
        'name': 'العربية', 'dir': 'rtl',
        'seo_title': 'محول ICO عبر الإنترنت - إنشاء أيقونة Favicon',
        'seo_desc': 'تحويل الصور إلى صيغة ICO مجاناً. أداة احترافية.',
        'h1': 'محول ICO', 'subtitle': 'مولد أيقونات احترافي',
        'upload_label': 'انقر للتحميل أو اسحب الصورة', 'size_label': 'الحجم المطلوب',
        'btn_submit': 'تحميل ملف .ICO', 'footer': 'حماية الخصوصية.', 'error_large': 'الملف كبير جداً'
    },
    'he': { # 希伯来语
        'name': 'עברית', 'dir': 'rtl',
        'seo_title': 'ממיר ICO מקוון - צור Favicon',
        'seo_desc': 'המרת תמונות ל-ICO בחינם. כלי מקצועי.',
        'h1': 'ממיר ICO', 'subtitle': 'יוצר אייקונים מקצועי',
        'upload_label': 'לחץ להעלאה או גרור תמונה', 'size_label': 'גודל יעד',
        'btn_submit': 'הורד .ICO', 'footer': 'פרטיות מוגנת.', 'error_large': 'קובץ גדול מדי'
    }
}

SUPPORTED_LANGS = list(TRANSLATIONS.keys())
DEFAULT_LANG = 'en'

# ===========================
# 2. 核心路由与逻辑
# ===========================

def render_index(lang_code):
    """通用渲染函数"""
    if lang_code not in SUPPORTED_LANGS:
        return redirect(f"/{DEFAULT_LANG}")

    base_url = request.url_root.rstrip('/')
    # 生成所有语言的 Hreflang 链接
    alternates = [{'lang': l, 'href': f"{base_url}/{l}"} for l in SUPPORTED_LANGS]

    return render_template(
        'index.html',
        t=TRANSLATIONS[lang_code],
        current_lang=lang_code,
        alternates=alternates
    )

# 【核心功能】：循环注册所有 22 个语言的路由
# 这样 Flask 就能精准识别 /fr, /it, /vi 等路径
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
    """根目录智能跳转"""
    accept_lang = request.headers.get('Accept-Language', '')
    target = DEFAULT_LANG

    # 优先匹配全名 (e.g., zh-CN)
    if 'zh-CN' in accept_lang: target = 'zh'
    elif 'zh-TW' in accept_lang: target = 'tw'
    else:
        # 模糊匹配 (e.g., fr-CA -> fr)
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
        img = Image.open(file.stream).convert("RGBA")
        img = img.resize((size, size), Image.Resampling.LANCZOS)
        img_io = io.BytesIO()
        img.save(img_io, format='ICO', sizes=[(size, size)])
        img_io.seek(0)
        return send_file(img_io, mimetype='image/x-icon', as_attachment=True, download_name='favicon.ico')
    except Exception as e:
        return str(e), 500

@app.route('/sitemap.xml')
def sitemap():
    base_url = request.url_root.rstrip('/')
    urls = []
    # 自动生成 22 个语言的 Sitemap 链接
    for lang in SUPPORTED_LANGS:
        urls.append(f"<url><loc>{base_url}/{lang}</loc><changefreq>weekly</changefreq><priority>0.8</priority></url>")
    xml = f"""<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{''.join(urls)}</urlset>"""
    return Response(xml, mimetype="application/xml")
