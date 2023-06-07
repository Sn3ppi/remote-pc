from app.config.const import SYSTEM_TYPE

if SYSTEM_TYPE == "Windows":
    from machine.randomizer.windows import *
elif SYSTEM_TYPE == "Linux":
    from machine.randomizer.linux import *
    
__all__ = [
    'random_mention'
]
    
reactions = {
    'mention': {
        'sticker': [
            "CAACAgIAAx0CWNWWlwAC_ZJkf4jWedHAU1WGjW4h0ml7isoB0gACGQADci8wB7Kljc4GAAHYcy8E",
            "CAACAgIAAx0CWNWWlwAC_ZRkf4k2ZwdRbNL4HbU1aVD0JaLJfwACJBkAAmCtMElao2m_ofkzpi8E",
            "CAACAgIAAx0CWNWWlwAC_ZZkf4lJ_jj-yTy7hEzaf_Oe1AABEMoAApEbAAKrnJFKymfll71CQy4vBA",
            "CAACAgIAAx0CWNWWlwAC_Zhkf4lWtUqnyTNgK3jgVNFEb1AisQAC0AADci8wB3Z_gZF9Em_uLwQ",
            "CAACAgIAAx0CWNWWlwAC_Zpkf4lgcoZ8FhgE3LqqlPVC5rUsewACXgADci8wB9iFUcZXF0ARLwQ",
            "CAACAgIAAx0CWNWWlwAC_Zxkf4ls1jzQnyFpEeoQPVjovTZt1AACUQADci8wBzrxMYbTCaKfLwQ",
            "CAACAgIAAx0CWNWWlwAC_Z5kf4l2J3OkZKCoi-nzy5YGYgTuWgACDQADci8wB7sGbYDBXVGnLwQ",
            "CAACAgIAAx0CWNWWlwAC_aBkf4mCNki_ZiKLByJlddHitmM8MAACCQADci8wB6PyDmoZHBAlLwQ",
            "CAACAgIAAx0CWNWWlwAC_aJkf4mjTYCpBga5VZ589eHAE8ngCQACRgwAApA0mEifDcUr-blOAS8E",
            "CAACAgIAAx0CWNWWlwAC_aRkf4m2gkNjFDHfbgbh6IZEYEgJmwAChQ4AAhdzUUumER2-UBYtxC8E",
            "CAACAgIAAx0CWNWWlwAC_aZkf4nE1jhznsS8fWllB0-JxUqBpQACThEAAqdqSUuLMwwcznbJaS8E",
            "CAACAgIAAx0CWNWWlwAC_ahkf4nR7lcgGDbmQ0NlFvS9uX2ncwACUQ0AAnJ0SEsw3y5YtLsQQy8E",
            "CAACAgIAAx0CWNWWlwAC_apkf4ngZM_n2Oj0BOy9T7v7gjgevwADDwACpD1JSw9yA9yKJ4a_LwQ",
        ],
        'emoji': [
            "🤔",
            "🧐",
            "😳",
            "😨",
            "🍿",
            "😶",
            "👀",
            "😉",
            "😧",
            "😈",
            "🌚",
            "☕️",
            "🌝"
        ]
    }
}

def random_mention() -> tuple:
    '''Возвращает рандомную реакцию'''
    categories = list(reactions['mention'].keys())
    random_category_number = random_number(0, len(categories))
    message_type = categories[random_category_number]
    values = reactions['mention'][message_type]
    random_value_number = random_number(0, len(values))
    message_text = reactions['mention'][message_type][random_value_number]
    return message_type, message_text