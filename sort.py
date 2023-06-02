import sys
import pathlib
import shutil
import os


# Аргумент = шлях
path = sys.argv[1]

# Перевіряємо чи шлях веде до папки
folder_path = pathlib.Path(path)
if not folder_path.is_dir():
    print("Помилка! Такої теки не існує!")
    sys.exit(1)

print("Тека:", folder_path)

# Створюємо функцію нормалізації імен
TRANS = {1072: 'a', 1040: 'A', 1073: 'b', 1041: 'B', 1074: 'v', 1042: 'V', 1075: 'g', 1043: 'G', 1076: 'd', 1044: 'D', 1077: 'e', 1045: 'E', 1105: 'e', 1025: 'E', 1078: 'j', 1046: 'J', 1079: 'z', 1047: 'Z', 1080: 'i', 1048: 'I', 1081: 'j', 1049: 'J', 1082: 'k', 1050: 'K', 1083: 'l', 1051: 'L', 1084: 'm', 1052: 'M', 1085: 'n', 1053: 'N', 1086: 'o', 1054: 'O', 1087: 'p', 1055: 'P', 1088: 'r', 1056: 'R', 1089: 's', 1057: 'S', 1090: 't', 1058: 'T', 1091: 'u', 1059: 'U', 1092: 'f', 1060: 'F', 1093: 'h', 1061: 'H', 1094: 'ts', 1062: 'TS', 1095: 'ch', 1063: 'CH', 1096: 'sh', 1064: 'SH', 1097: 'sch', 1065: 'SCH', 1098: '', 1066: '', 1099: 'y', 1067: 'Y', 1100: '', 1068: '', 1101: 'e', 1069: 'E', 1102: 'yu', 1070: 'YU', 1103: 'ya', 1071: 'YA', 1108: 'je', 1028: 'JE', 1110: 'i', 1030: 'I', 1111: 'ji', 1031: 'JI', 1169: 'g', 1168: 'G'}

def normalize(name):
    translated = name.translate(TRANS)
    normalize_name = ''
    for i in translated:
        if ord(i) in range(65, 91) or ord(i) in range(97, 123) or ord(i) in range(48, 58) or i == '.':
            normalize_name += i
        else:
            normalize_name += '_'
    return normalize_name

# Створюємо паки для відсортованих фалів
extensions = {
    'images': ['JPEG', 'PNG', 'JPG', 'SVG'],
    'videos': ['AVI', 'MP4', 'MOV', 'MKV'],
    'documents': ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'],
    'music': ['MP3', 'OGG', 'WAV', 'AMR'],
    'archives': ['ZIP', 'GZ', 'TAR'],
    'other': []
}

for folder_name in extensions.keys():
    item_folder_path = folder_path / folder_name
    item_folder_path.mkdir(exist_ok=True)

# Для повторююмих імен файлів
def get_new_path(folder, item):
    new_name = normalize(item.stem)
    extension = item.suffix
    new_path = folder / (new_name + extension)

    if new_path.exists():
        i = 1
        while True:
            new_path = folder / f"{new_name}{i}{extension}"
            if not new_path.exists():
                break
            i += 1

    return new_path

# Сортувальник файлів з рекурсією 
def sorting_all(folder):
    for item in folder.iterdir():
        if item.is_file():
            extension = item.suffix.upper()[1:]
            for folder_name, folder_extensions in extensions.items():
                if extension in folder_extensions:
                    destination_folder = folder_path / folder_name
                    new_path = get_new_path(destination_folder, item)
                    item.rename(new_path)
                    break
            else:
                destination_folder = folder_path / 'other'
                new_path = get_new_path(destination_folder, item)
                item.rename(new_path)
        elif item.is_dir():
            sorting_all(item)


sorting_all(folder_path)

def unpack_archive(archive):
    archive_folder = archive / 'archives'
    for arch in archive_folder.iterdir():
        if arch.is_dir():
            continue
        else:
            archive_name = normalize(arch.stem)
            unpack_archive_folder = archive_folder / archive_name
            unpack_archive_folder.mkdir(exist_ok=True)
            shutil.unpack_archive(str(arch), unpack_archive_folder)
            os.remove(arch)

unpack_archive(folder_path)
                
def clean(sort_path):
    for item in sort_path.iterdir():
        if item.is_dir():
            clean(item)
            if not list(item.iterdir()):
                item.rmdir()
        elif item.is_file():
            continue
clean(folder_path)