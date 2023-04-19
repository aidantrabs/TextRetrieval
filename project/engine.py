from InquirerPy.utils import color_print, patched_print

def collect():
    patched_print("collect")

def inverted_index():
    patched_print("inverted_index")

def search(query: str):
    patched_print("search")

def train():
    patched_print("train")

def predict_link(link: str):
    patched_print("predicted_link")
