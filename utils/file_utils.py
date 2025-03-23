# utils/file_utils.py
import pandas as pd
import io
import chardet  # install via pip install chardet
import fitz    # PyMuPDF; install via pip install PyMuPDF
import docx    # python-docx; install via pip install python-docx
from PIL import Image, ExifTags

def detect_encoding(file_obj, num_bytes=10000):
    rawdata = file_obj.read(num_bytes)
    file_obj.seek(0)
    import chardet
    result = chardet.detect(rawdata)
    return result["encoding"]

def parse_csv(file_obj, delimiter=",", chunksize=None) -> pd.DataFrame:
    try:
        encoding = detect_encoding(file_obj)
        if chunksize:
            return pd.read_csv(file_obj, delimiter=delimiter, chunksize=chunksize, encoding=encoding)
        else:
            return pd.read_csv(file_obj, delimiter=delimiter, encoding=encoding)
    except Exception as e:
        return None

def parse_excel(file_obj, sheet_name=0) -> pd.DataFrame:
    try:
        return pd.read_excel(file_obj, sheet_name=sheet_name)
    except Exception as e:
        return None

def parse_text(file_obj, encoding="utf-8") -> str:
    try:
        content = file_obj.read()
        if isinstance(content, bytes):
            return content.decode(encoding)
        return content
    except Exception as e:
        return ""

def parse_pdf(file_obj) -> str:
    try:
        file_bytes = file_obj.read()
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        return ""

def parse_docx(file_obj) -> str:
    try:
        document = docx.Document(file_obj)
        full_text = [para.text for para in document.paragraphs]
        return "\n".join(full_text)
    except Exception as e:
        return ""

def parse_html(file_obj, encoding="utf-8") -> str:
    try:
        content = file_obj.read()
        if isinstance(content, bytes):
            content = content.decode(encoding)
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(content, "html.parser")
        return soup.get_text(separator="\n")
    except Exception as e:
        return ""

def parse_css(file_obj, encoding="utf-8") -> str:
    try:
        content = file_obj.read()
        if isinstance(content, bytes):
            content = content.decode(encoding)
        return content
    except Exception as e:
        return ""

def parse_image(file_obj) -> dict:
    try:
        img = Image.open(file_obj)
        info = {
            "format": img.format,
            "size": img.size,
            "mode": img.mode
        }
        try:
            exif_data = img._getexif()
            if exif_data:
                exif = {}
                for tag, value in exif_data.items():
                    decoded = ExifTags.TAGS.get(tag, tag)
                    exif[decoded] = value
                info["exif"] = exif
            else:
                info["exif"] = {}
        except Exception as e:
            info["exif"] = {}
        return info
    except Exception as e:
        return {}

def parse_uploaded_file(file_obj, file_extension: str) -> dict:
    result = {"content": None, "metadata": None}
    if file_extension.lower() in ["csv"]:
        df = parse_csv(file_obj)
        if df is not None:
            result["content"] = df.to_dict(orient="records")
    elif file_extension.lower() in ["xlsx"]:
        df = parse_excel(file_obj)
        if df is not None:
            result["content"] = df.to_dict(orient="records")
    elif file_extension.lower() in ["txt"]:
        result["content"] = parse_text(file_obj)
    elif file_extension.lower() in ["pdf"]:
        result["content"] = parse_pdf(file_obj)
    elif file_extension.lower() in ["docx"]:
        result["content"] = parse_docx(file_obj)
    elif file_extension.lower() in ["html"]:
        result["content"] = parse_html(file_obj)
    elif file_extension.lower() in ["css"]:
        result["content"] = parse_css(file_obj)
    elif file_extension.lower() in ["jpg", "jpeg", "png"]:
        result["metadata"] = parse_image(file_obj)
    else:
        result["content"] = None
    return result
