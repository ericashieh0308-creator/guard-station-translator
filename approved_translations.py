
# Guard Station Translator
# Week 7 - Standard Translation Library
#
# IMPORTANT:
# All translations are draft candidates.
# They must be verified by qualified human reviewers
# before being marked as approved.

TRANSLATION_LIBRARY = {
    "Please check in at the front desk.": {
        "zh": "请在前台登记。",
        "es": "Por favor, regístrese en la recepción.",
        "fr": "Veuillez vous enregistrer à l'accueil.",
        "ru": "Пожалуйста, зарегистрируйтесь на стойке регистрации.",
        "ar": "يرجى تسجيل الوصول في مكتب الاستقبال.",
    },

    "Please use the elevator to go to the fifth floor.": {
        "zh": "请乘电梯到五楼。",
        "es": "Por favor, tome el ascensor hasta el quinto piso.",
        "fr": "Veuillez prendre l'ascenseur jusqu'au cinquième étage.",
        "ru": "Пожалуйста, поднимитесь на лифте на пятый этаж.",
        "ar": "يرجى استخدام المصعد للوصول إلى الطابق الخامس.",
    },

    "Please present your access badge before entering this area.": {
        "zh": "进入此区域前，请出示您的门禁卡。",
        "es": "Por favor, muestre su tarjeta de acceso antes de entrar en esta zona.",
        "fr": "Veuillez présenter votre badge d'accès avant d'entrer dans cette zone.",
        "ru": "Пожалуйста, предъявите свой пропуск перед входом в эту зону.",
        "ar": "يرجى إبراز بطاقة الدخول الخاصة بك قبل دخول هذه المنطقة.",
    },

    "Please wait here for assistance.": {
        "zh": "请在这里等候工作人员协助。",
        "es": "Por favor, espere aquí para recibir ayuda.",
        "fr": "Veuillez attendre ici qu'un membre du personnel vous aide.",
        "ru": "Пожалуйста, подождите здесь, пока вам не окажут помощь.",
        "ar": "يرجى الانتظار هنا للحصول على المساعدة.",
    },

    "Please show your identification.": {
        "zh": "请出示您的身份证件。",
        "es": "Por favor, muestre su documento de identidad.",
        "fr": "Veuillez présenter votre pièce d'identité.",
        "ru": "Пожалуйста, предъявите документ, удостоверяющий личность.",
        "ar": "يرجى إبراز وثيقة إثبات الهوية.",
    },
}


# Approval status for each translation.
# False means NOT YET HUMAN-APPROVED.
TRANSLATION_APPROVAL = {
    english: {
        language: False
        for language in translations
    }
    for english, translations in TRANSLATION_LIBRARY.items()
}


def get_approved_translation(english_text, target_language):
    """
    Return a translation only if it has been
    explicitly approved by a human reviewer.

    Otherwise return None so the system can
    use its existing translation workflow.
    """

    translations = TRANSLATION_LIBRARY.get(english_text)

    if translations is None:
        return None

    if not TRANSLATION_APPROVAL.get(
        english_text, {}
    ).get(target_language, False):
        return None

    return translations.get(target_language)


if __name__ == "__main__":
    print("Guard Station Translation Library")
    print("---------------------------------")

    print("Standard instructions:",
          len(TRANSLATION_LIBRARY))

    print("Supported languages: zh, es, fr, ru, ar")

    total = sum(
        len(translations)
        for translations in TRANSLATION_LIBRARY.values()
    )

    approved = sum(
        sum(status.values())
        for status in TRANSLATION_APPROVAL.values()
    )

    print("Translation candidates:", total)
    print("Human-approved translations:", approved)
    print("Pending human review:", total - approved)
