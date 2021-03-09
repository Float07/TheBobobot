_strings_ = {"pt-br":{
    "help":{
        "help": "PLACEHOLDER",
        "default": "Não existe ajuda para esse comando."
    }
}}


def get_string(key_array):
    string = _strings_
    for key in key_array:
        if type(string) == str:
            return string
        if key in string:
            string = string[key]
        elif "default" in string:
            return string["default"]
        else:
            return "<ERROR: String not found>"