import json
import cv2
import os

JSON_DIR = 'cccd_json'
JPG_DIR = 'cccd_jpg'
BOXES_JPG_DIR = 'cccd_jpg_with_boxes'
WORD_IMG_DIR = 'one_word_img_with_label'
ANNOTATION_FILENAME = 'annotation.txt'
IMG_EXT = '.jpg'

FIELD_COLOUR = {
    # "field_name" : (b, g, r)
    "ID": (0, 255, 0), # grün
    "name": (255, 0, 0), # blau
    "DOB": (0, 0, 255), # rot
    "doe": (0, 255, 255), # gelb
    "sex": (0, 0, 0), # schwarz
    "home": (255, 0, 255), # rosa
    "address": (255, 255, 0) # cyan
}

def get_label(json_dict, field_name):
    field_data = data[field_name]
    label_pairs = []
    for item in field_data:
        label_str = item['label']
        label_rect_box_x = item['box']['x']
        label_rect_box_y = item['box']['y']
        label_rect_box_w = item['box']['width']
        label_rect_box_h = item['box']['height']
        label_pairs.append((label_str,
            (label_rect_box_x, label_rect_box_y,
            label_rect_box_w, label_rect_box_h)))
    return label_pairs

def draw_boxes(json_dict, field_name, img):
    label_pairs = get_label(json_dict, field_name)
    for item in label_pairs:
        rect = item[1]
        x = rect[0]
        y = rect[1]
        w = rect[2]
        h = rect[3]
        cv2.rectangle(img, (x, y), (x + w, y + h), FIELD_COLOUR[field_name], 1)

def extract_word_img(json_dict, field_name, img, base_filename):
    if field_name in ['ID', 'name']:
        label_pairs = get_label(json_dict, field_name)
        f = open(os.path.join(WORD_IMG_DIR, field_name, ANNOTATION_FILENAME), 'a')
        for counter, item in enumerate(label_pairs, 1):
            str_label = item[0]
            rect = item[1]
            x = rect[0]
            y = rect[1]
            w = rect[2]
            h = rect[3]
            word_img = img[y: y + h, x: x + w]
            word_img_filename = base_filename + '_' + str(counter) + IMG_EXT
            cv2.imwrite(os.path.join(WORD_IMG_DIR, field_name, IMG_EXT[1:], word_img_filename), word_img)
            f.write(word_img_filename + '\t' + str_label + '\n')
        f.close()
    elif field_name == 'DOB':
        label_pairs = get_label(json_dict, field_name)
        f = open(os.path.join(WORD_IMG_DIR, field_name, ANNOTATION_FILENAME), 'a')
        counter = 1
        item = label_pairs[0]
        str_label = item[0]
        rect = item[1]
        x = rect[0]
        y = rect[1]
        w = rect[2]
        h = rect[3]
        word_img = img[y: y + h, x: x + w]
        word_img_filename = base_filename + '_' + str(counter) + IMG_EXT
        cv2.imwrite(os.path.join(WORD_IMG_DIR, field_name, IMG_EXT[1:], word_img_filename), word_img)
        f.write(word_img_filename + '\t' + str_label + '\n')
        f.close()
        label_pairs = get_label(json_dict, 'doe')
        if len(label_pairs) == 1:
            counter = 2
            f = open(os.path.join(WORD_IMG_DIR, field_name, ANNOTATION_FILENAME), 'a')
            item = label_pairs[0]
            str_label = item[0]
            rect = item[1]
            x = rect[0]
            y = rect[1]
            w = rect[2]
            h = rect[3]
            word_img = img[y: y + h, x: x + w]
            word_img_filename = base_filename + '_' + str(counter) + IMG_EXT
            cv2.imwrite(os.path.join(WORD_IMG_DIR, field_name, IMG_EXT[1:], word_img_filename), word_img)
            f.write(word_img_filename + '\t' + str_label + '\n')
            f.close()
    elif field_name == 'address':
        label_pairs = get_label(json_dict, field_name)
        f = open(os.path.join(WORD_IMG_DIR, field_name, ANNOTATION_FILENAME), 'a')
        for counter, item in enumerate(label_pairs, 1):
            str_label = item[0]
            rect = item[1]
            x = rect[0]
            y = rect[1]
            w = rect[2]
            h = rect[3]
            word_img = img[y: y + h, x: x + w]
            word_img_filename = base_filename + '_' + str(counter) + IMG_EXT
            cv2.imwrite(os.path.join(WORD_IMG_DIR, field_name, IMG_EXT[1:], word_img_filename), word_img)
            f.write(word_img_filename + '\t' + str_label + '\n')
        f.close()
        label_pairs = get_label(json_dict, 'home')
        f = open(os.path.join(WORD_IMG_DIR, field_name, ANNOTATION_FILENAME), 'a')
        for counter, item in enumerate(label_pairs, 1):
            str_label = item[0]
            rect = item[1]
            x = rect[0]
            y = rect[1]
            w = rect[2]
            h = rect[3]
            word_img = img[y: y + h, x: x + w]
            word_img_filename = base_filename + '_' + str(counter) + IMG_EXT
            cv2.imwrite(os.path.join(WORD_IMG_DIR, field_name, IMG_EXT[1:], word_img_filename), word_img)
            f.write(word_img_filename + '\t' + str_label + '\n')
        f.close()

for json_filename in os.listdir(JSON_DIR):
    with open(os.path.join(JSON_DIR, json_filename)) as f:
        data = json.load(f)
    jpg_filename = json_filename.replace('.json', IMG_EXT)
    img = cv2.imread(os.path.join(JPG_DIR, jpg_filename))

    """ for field in FIELD_COLOUR.keys():
        draw_boxes(data, field, img)
    cv2.imwrite(os.path.join(BOXES_JPG_DIR, jpg_filename), img) """
    base_filename = os.path.splitext(jpg_filename)[0]
    extract_word_img(data, 'ID', img, base_filename)
    extract_word_img(data, 'name', img, base_filename)
    extract_word_img(data, 'DOB', img, base_filename)
    extract_word_img(data, 'address', img, base_filename)

    print('>>', jpg_filename)
