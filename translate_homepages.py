#!/usr/bin/env python3
"""
translate_homepages.py
Translates hub card content on all language homepages.
"""

import re, glob

TRANSLATIONS = {
    'es': {
        'Everything You Need to Know': 'Todo Lo Que Necesita Saber',
        'Car insurance answers for immigrants — the questions others won\'t answer, in your language.': 'Respuestas de seguro de auto para inmigrantes — en su idioma.',
        'Getting Insured': 'Obtener Seguro',
        'Everything you need to know about getting car insurance as an immigrant in the US — regardless of your documentation status.': 'Todo sobre como obtener seguro de auto como inmigrante en EEUU.',
        'Insurance by Immigration Status': 'Seguro por Estatus Migratorio',
        'Car insurance requirements and options differ by immigration status. Find your exact situation.': 'Los requisitos de seguro difieren segun su estatus migratorio.',
        'Common Questions': 'Preguntas Frecuentes',
        'The questions every immigrant asks about car insurance in the US — answered directly, honestly, in your language.': 'Las preguntas que todo inmigrante hace — respondidas directamente en su idioma.',
        'Foreign License Insurance': 'Seguro con Licencia Extranjera',
        "Using your home country driver's license for car insurance in the US — by country and by state.": 'Usando su licencia extranjera para seguro en EEUU.',
        'After an Accident': 'Despues de un Accidente',
        'What to do after a car accident as an immigrant — with or without insurance, with or without a license.': 'Que hacer despues de un accidente como inmigrante.',
        'Coverage Explained': 'Cobertura Explicada',
        'US car insurance coverage types explained simply for immigrants — what you must have, what is optional, and what actually protects you.': 'Tipos de cobertura explicados simplemente para inmigrantes.',
        'Insurance Companies': 'Companias de Seguros',
        'Which car insurance companies work best for immigrants — who accepts ITIN, who accepts foreign licenses, and who has the best rates.': 'Que companias funcionan mejor para inmigrantes — quien acepta ITIN y licencias extranjeras.',
        "Driver's License Guide": 'Guia de Licencia de Conducir',
        "Getting a driver's license as an immigrant — which states allow it, how to convert your foreign license, and how it affects your insurance.": 'Obtener licencia de conducir como inmigrante — que estados lo permiten.',
        'By State': 'Por Estado',
        'Save Money on Insurance': 'Ahorrar en el Seguro',
        'About Us': 'Sobre Nosotros',
        'How We Research': 'Como Investigamos',
        'Disclaimer': 'Aviso Legal',
        'Privacy Policy': 'Politica de Privacidad',
        'Terms of Use': 'Terminos de Uso',
        'Contact': 'Contacto',
        'Get Insured': 'Obtener Seguro',
        'Questions': 'Preguntas',
        'By Status': 'Por Estatus',
        'Accidents': 'Accidentes',
        'License': 'Licencia',
    },
    'zh': {
        'Everything You Need to Know': '您需要了解的一切',
        'Car insurance answers for immigrants — the questions others won\'t answer, in your language.': '为移民解答汽车保险问题——用您的语言。',
        'Getting Insured': '获得保险',
        'Everything you need to know about getting car insurance as an immigrant in the US — regardless of your documentation status.': '作为美国移民获得汽车保险的一切知识。',
        'Insurance by Immigration Status': '按移民身份投保',
        'Car insurance requirements and options differ by immigration status. Find your exact situation.': '保险要求因移民身份而异。找到您的具体情况。',
        'Common Questions': '常见问题',
        'The questions every immigrant asks about car insurance in the US — answered directly, honestly, in your language.': '每个移民对美国汽车保险的疑问——用您的语言直接回答。',
        'Foreign License Insurance': '外国驾照保险',
        "Using your home country driver's license for car insurance in the US — by country and by state.": '使用您本国驾照在美国购买汽车保险。',
        'After an Accident': '事故后处理',
        'What to do after a car accident as an immigrant — with or without insurance, with or without a license.': '作为移民发生车祸后该怎么做。',
        'Coverage Explained': '保险类型说明',
        'US car insurance coverage types explained simply for immigrants — what you must have, what is optional, and what actually protects you.': '为移民简单解释美国汽车保险类型。',
        'Insurance Companies': '保险公司',
        'Which car insurance companies work best for immigrants — who accepts ITIN, who accepts foreign licenses, and who has the best rates.': '哪些保险公司最适合移民——谁接受ITIN和外国驾照。',
        "Driver's License Guide": '驾照指南',
        "Getting a driver's license as an immigrant — which states allow it, how to convert your foreign license, and how it affects your insurance.": '作为移民获得驾照——哪些州允许，如何转换驾照。',
        'By State': '按州查询',
        'Save Money on Insurance': '节省保险费用',
        'About Us': '关于我们',
        'Disclaimer': '免责声明',
        'Privacy Policy': '隐私政策',
        'Terms of Use': '使用条款',
        'Contact': '联系我们',
        'Get Insured': '获得保险',
        'Questions': '常见问题',
        'By Status': '按身份',
        'Accidents': '事故处理',
        'License': '驾照',
    },
    'ar': {
        'Everything You Need to Know': 'كل ما تحتاج معرفته',
        'Car insurance answers for immigrants — the questions others won\'t answer, in your language.': 'اجابات تامين السيارات للمهاجرين — بلغتك.',
        'Getting Insured': 'الحصول على التامين',
        'Everything you need to know about getting car insurance as an immigrant in the US — regardless of your documentation status.': 'كل ما تحتاج معرفته للحصول على تامين سيارة كمهاجر في امريكا.',
        'Insurance by Immigration Status': 'التامين حسب الوضع المهاجر',
        'Car insurance requirements and options differ by immigration status. Find your exact situation.': 'متطلبات التامين تختلف حسب وضعك المهاجر. ابحث عن حالتك.',
        'Common Questions': 'الاسئلة الشائعة',
        'The questions every immigrant asks about car insurance in the US — answered directly, honestly, in your language.': 'اسئلة كل مهاجر عن تامين السيارة في امريكا — مجاب عليها بلغتك.',
        'Foreign License Insurance': 'تامين برخصة اجنبية',
        "Using your home country driver's license for car insurance in the US — by country and by state.": 'استخدام رخصة بلدك للتامين في امريكا.',
        'After an Accident': 'بعد الحادث',
        'What to do after a car accident as an immigrant — with or without insurance, with or without a license.': 'ماذا تفعل بعد حادث سيارة كمهاجر.',
        'Coverage Explained': 'انواع التغطية',
        'US car insurance coverage types explained simply for immigrants — what you must have, what is optional, and what actually protects you.': 'انواع تامين السيارة في امريكا موضحة ببساطة للمهاجرين.',
        'Insurance Companies': 'شركات التامين',
        'Which car insurance companies work best for immigrants — who accepts ITIN, who accepts foreign licenses, and who has the best rates.': 'ايي شركات التامين الافضل للمهاجرين — من يقبل ITIN والرخص الاجنبية.',
        "Driver's License Guide": 'دليل رخصة القيادة',
        "Getting a driver's license as an immigrant — which states allow it, how to convert your foreign license, and how it affects your insurance.": 'الحصول على رخصة قيادة كمهاجر — اي الولايات تسمح بذلك.',
        'By State': 'حسب الولاية',
        'Save Money on Insurance': 'توفير في التامين',
        'About Us': 'من نحن',
        'Disclaimer': 'اخلاء المسؤولية',
        'Privacy Policy': 'سياسة الخصوصية',
        'Terms of Use': 'شروط الاستخدام',
        'Contact': 'اتصل بنا',
        'Get Insured': 'احصل على التامين',
        'Questions': 'الاسئلة',
        'By Status': 'حسب الوضع',
        'Accidents': 'الحوادث',
        'License': 'الرخصة',
    },
    'pt': {
        'Everything You Need to Know': 'Tudo Que Voce Precisa Saber',
        'Car insurance answers for immigrants — the questions others won\'t answer, in your language.': 'Respostas sobre seguro de carro para imigrantes — no seu idioma.',
        'Getting Insured': 'Obter Seguro',
        'Everything you need to know about getting car insurance as an immigrant in the US — regardless of your documentation status.': 'Tudo sobre como obter seguro de carro como imigrante nos EUA.',
        'Insurance by Immigration Status': 'Seguro por Status de Imigracao',
        'Car insurance requirements and options differ by immigration status. Find your exact situation.': 'Os requisitos de seguro diferem conforme seu status. Encontre sua situacao.',
        'Common Questions': 'Perguntas Frequentes',
        'The questions every immigrant asks about car insurance in the US — answered directly, honestly, in your language.': 'As perguntas que todo imigrante faz — respondidas diretamente no seu idioma.',
        'Foreign License Insurance': 'Seguro com Carteira Estrangeira',
        "Using your home country driver's license for car insurance in the US — by country and by state.": 'Usando sua carteira estrangeira para seguro nos EUA.',
        'After an Accident': 'Apos um Acidente',
        'What to do after a car accident as an immigrant — with or without insurance, with or without a license.': 'O que fazer apos um acidente de carro como imigrante.',
        'Coverage Explained': 'Coberturas Explicadas',
        'US car insurance coverage types explained simply for immigrants — what you must have, what is optional, and what actually protects you.': 'Tipos de cobertura de seguro nos EUA explicados para imigrantes.',
        'Insurance Companies': 'Seguradoras',
        'Which car insurance companies work best for immigrants — who accepts ITIN, who accepts foreign licenses, and who has the best rates.': 'Quais seguradoras funcionam melhor para imigrantes — quem aceita ITIN e carteira estrangeira.',
        "Driver's License Guide": 'Guia de Carteira de Motorista',
        "Getting a driver's license as an immigrant — which states allow it, how to convert your foreign license, and how it affects your insurance.": 'Obter carteira de motorista como imigrante — quais estados permitem.',
        'By State': 'Por Estado',
        'Save Money on Insurance': 'Economizar no Seguro',
        'About Us': 'Sobre Nos',
        'Disclaimer': 'Aviso Legal',
        'Privacy Policy': 'Politica de Privacidade',
        'Terms of Use': 'Termos de Uso',
        'Contact': 'Contato',
        'Get Insured': 'Obter Seguro',
        'Questions': 'Perguntas',
        'By Status': 'Por Status',
        'Accidents': 'Acidentes',
        'License': 'Carteira',
    },
    'ru': {
        'Everything You Need to Know': 'Все что вам нужно знать',
        'Car insurance answers for immigrants — the questions others won\'t answer, in your language.': 'Ответы на вопросы об автостраховании для иммигрантов — на вашем языке.',
        'Getting Insured': 'Получить страховку',
        'Everything you need to know about getting car insurance as an immigrant in the US — regardless of your documentation status.': 'Всё о получении автострахования как иммигранта в США.',
        'Insurance by Immigration Status': 'Страховка по иммиграционному статусу',
        'Car insurance requirements and options differ by immigration status. Find your exact situation.': 'Требования к страховке различаются в зависимости от статуса.',
        'Common Questions': 'Частые вопросы',
        'The questions every immigrant asks about car insurance in the US — answered directly, honestly, in your language.': 'Вопросы каждого иммигранта — отвечаем прямо на вашем языке.',
        'Foreign License Insurance': 'Страховка с иностранными правами',
        "Using your home country driver's license for car insurance in the US — by country and by state.": 'Использование иностранных прав для страховки в США.',
        'After an Accident': 'После аварии',
        'What to do after a car accident as an immigrant — with or without insurance, with or without a license.': 'Что делать после аварии как иммигрант.',
        'Coverage Explained': 'Виды покрытия',
        'US car insurance coverage types explained simply for immigrants — what you must have, what is optional, and what actually protects you.': 'Виды автострахования в США простым языком для иммигрантов.',
        'Insurance Companies': 'Страховые компании',
        'Which car insurance companies work best for immigrants — who accepts ITIN, who accepts foreign licenses, and who has the best rates.': 'Какие компании лучше для иммигрантов — кто принимает ITIN и иностранные права.',
        "Driver's License Guide": 'Руководство по водительским правам',
        "Getting a driver's license as an immigrant — which states allow it, how to convert your foreign license, and how it affects your insurance.": 'Получение водительских прав как иммигрант — какие штаты разрешают.',
        'By State': 'По штатам',
        'Save Money on Insurance': 'Сэкономить на страховке',
        'About Us': 'О нас',
        'Disclaimer': 'Отказ от ответственности',
        'Privacy Policy': 'Политика конфиденциальности',
        'Terms of Use': 'Условия использования',
        'Contact': 'Контакты',
        'Get Insured': 'Получить страховку',
        'Questions': 'Вопросы',
        'By Status': 'По статусу',
        'Accidents': 'Аварии',
        'License': 'Права',
    },
    'pl': {
        'Everything You Need to Know': 'Wszystko Co Musisz Wiedziec',
        'Car insurance answers for immigrants — the questions others won\'t answer, in your language.': 'Odpowiedzi na pytania o ubezpieczenie auta dla imigrantow — po polsku.',
        'Getting Insured': 'Uzyskaj Ubezpieczenie',
        'Everything you need to know about getting car insurance as an immigrant in the US — regardless of your documentation status.': 'Wszystko o ubezpieczeniu auta jako imigrant w USA.',
        'Insurance by Immigration Status': 'Ubezpieczenie wg statusu imigracyjnego',
        'Car insurance requirements and options differ by immigration status. Find your exact situation.': 'Wymagania ubezpieczeniowe roznia sie w zaleznosci od statusu.',
        'Common Questions': 'Czeste Pytania',
        'The questions every immigrant asks about car insurance in the US — answered directly, honestly, in your language.': 'Pytania kazdego imigranta — odpowiedzi po polsku.',
        'Foreign License Insurance': 'Ubezpieczenie z Zagranicznym Prawem Jazdy',
        "Using your home country driver's license for car insurance in the US — by country and by state.": 'Korzystanie z zagranicznego prawa jazdy do ubezpieczenia w USA.',
        'After an Accident': 'Po Wypadku',
        'What to do after a car accident as an immigrant — with or without insurance, with or without a license.': 'Co zrobic po wypadku samochodowym jako imigrant.',
        'Coverage Explained': 'Rodzaje Ubezpieczen',
        'US car insurance coverage types explained simply for immigrants — what you must have, what is optional, and what actually protects you.': 'Rodzaje ubezpieczen samochodowych w USA wyjasnionych prosto dla imigrantow.',
        'Insurance Companies': 'Firmy Ubezpieczeniowe',
        'Which car insurance companies work best for immigrants — who accepts ITIN, who accepts foreign licenses, and who has the best rates.': 'Ktore firmy ubezpieczeniowe sa najlepsze dla imigrantow.',
        "Driver's License Guide": 'Prawo Jazdy - Przewodnik',
        "Getting a driver's license as an immigrant — which states allow it, how to convert your foreign license, and how it affects your insurance.": 'Uzyskanie prawa jazdy jako imigrant — ktore stany to umozliwiaja.',
        'By State': 'Wg Stanu',
        'Save Money on Insurance': 'Oszczedzaj na Ubezpieczeniu',
        'About Us': 'O Nas',
        'Disclaimer': 'Zastrzezenie',
        'Privacy Policy': 'Polityka Prywatnosci',
        'Terms of Use': 'Warunki Uzytkowania',
        'Contact': 'Kontakt',
        'Get Insured': 'Ubezpiecz sie',
        'Questions': 'Pytania',
        'By Status': 'Wg Statusu',
        'Accidents': 'Wypadki',
        'License': 'Prawo Jazdy',
    },
    'vi': {
        'Everything You Need to Know': 'Tất Cả Những Gì Bạn Cần Biết',
        'Car insurance answers for immigrants — the questions others won\'t answer, in your language.': 'Giải đáp bảo hiểm xe hơi cho người nhập cư — bằng ngôn ngữ của bạn.',
        'Getting Insured': 'Mua Bảo Hiểm',
        'Everything you need to know about getting car insurance as an immigrant in the US — regardless of your documentation status.': 'Tất cả về mua bảo hiểm xe hơi với tư cách người nhập cư tại Mỹ.',
        'Insurance by Immigration Status': 'Bảo Hiểm Theo Tình Trạng Di Trú',
        'Common Questions': 'Câu Hỏi Thường Gặp',
        'Foreign License Insurance': 'Bảo Hiểm Với Bằng Lái Nước Ngoài',
        'After an Accident': 'Sau Tai Nạn',
        'Coverage Explained': 'Giải Thích Loại Bảo Hiểm',
        'Insurance Companies': 'Công Ty Bảo Hiểm',
        "Driver's License Guide": 'Hướng Dẫn Bằng Lái Xe',
        'By State': 'Theo Tiểu Bang',
        'Save Money on Insurance': 'Tiết Kiệm Phí Bảo Hiểm',
        'About Us': 'Về Chúng Tôi',
        'Contact': 'Liên Hệ',
        'Get Insured': 'Mua Bảo Hiểm',
        'Questions': 'Câu Hỏi',
        'By Status': 'Theo Tình Trạng',
        'Accidents': 'Tai Nạn',
        'License': 'Bằng Lái',
    },
    'tl': {
        'Everything You Need to Know': 'Lahat ng Kailangan Mong Malaman',
        'Car insurance answers for immigrants — the questions others won\'t answer, in your language.': 'Mga sagot sa car insurance para sa mga imigrante — sa iyong wika.',
        'Getting Insured': 'Kumuha ng Insurance',
        'Insurance by Immigration Status': 'Insurance ayon sa Immigration Status',
        'Common Questions': 'Mga Karaniwang Tanong',
        'Foreign License Insurance': 'Insurance gamit ang Foreign License',
        'After an Accident': 'Pagkatapos ng Aksidente',
        'Coverage Explained': 'Paliwanag ng Coverage',
        'Insurance Companies': 'Mga Kumpanya ng Insurance',
        "Driver's License Guide": "Gabay sa Driver's License",
        'By State': 'Ayon sa Estado',
        'Save Money on Insurance': 'Makatipid sa Insurance',
        'About Us': 'Tungkol sa Amin',
        'Contact': 'Makipag-ugnayan',
        'Get Insured': 'Kumuha ng Insurance',
        'Questions': 'Mga Tanong',
        'By Status': 'Ayon sa Status',
        'Accidents': 'Mga Aksidente',
        'License': 'Lisensya',
    },
    'ko': {
        'Everything You Need to Know': '알아야 할 모든 것',
        'Car insurance answers for immigrants — the questions others won\'t answer, in your language.': '이민자를 위한 자동차 보험 답변 — 귀하의 언어로.',
        'Getting Insured': '보험 가입',
        'Insurance by Immigration Status': '이민 신분별 보험',
        'Common Questions': '자주 묻는 질문',
        'Foreign License Insurance': '외국 면허증 보험',
        'After an Accident': '사고 후 처리',
        'Coverage Explained': '보험 유형 설명',
        'Insurance Companies': '보험 회사',
        "Driver's License Guide": '운전 면허증 가이드',
        'By State': '주별 안내',
        'Save Money on Insurance': '보험료 절약',
        'About Us': '소개',
        'Contact': '연락처',
        'Get Insured': '보험 가입',
        'Questions': '질문',
        'By Status': '신분별',
        'Accidents': '사고',
        'License': '면허증',
    },
}

def translate_file(filepath, lang_code):
    if lang_code not in TRANSLATIONS:
        return False
    
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    original = content
    translations = TRANSLATIONS[lang_code]
    
    for en, translated in translations.items():
        content = content.replace(en, translated)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


# Map language folders to language codes
lang_map = {
    'es': 'es', 'zh': 'zh', 'ar': 'ar', 'pt': 'pt',
    'ru': 'ru', 'pl': 'pl', 'vi': 'vi', 'tl': 'tl', 'ko': 'ko'
}

total_fixed = 0
for lang_folder, lang_code in lang_map.items():
    files = glob.glob(f'{lang_folder}/**/*.html', recursive=True) + [f'{lang_folder}/index.html']
    files = list(set(files))
    fixed = 0
    for filepath in files:
        try:
            if translate_file(filepath, lang_code):
                fixed += 1
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"  Error {filepath}: {e}")
    print(f"  [{lang_code}] translated {fixed} files")
    total_fixed += fixed

print(f"\nTotal: {total_fixed} files translated across 9 languages.")
