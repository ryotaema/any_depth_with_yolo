import sys
import os
import cv2
import torch
import numpy as np
from ultralytics import YOLO

sys.path.append('/home/ryota/harvesting_ws/depth_anything/Depth-Anything-V2')
from depth_anything_v2.dpt import DepthAnythingV2

DEVICE = 'cuda' if torch.cuda.is_available() else 'mps' if torch.backends.mps.is_available() else 'cpu'
CHECKPOINT = 'model/depth_anything_model/depth_anything_v2_vits.pth'
INPUT_DIR = 'input'
OUTPUT_DIR = 'output'

# 'yolo'  : YOLOで検出した領域のみに深度推定
# 'full'  : 画像全体に深度推定
# 'both'  : 両方を並べて出力
MODE = 'full'
# MODE = 'yolo'

yolo = YOLO('model/yolo_model/260410_pepper_yolo11.pt')

model_configs = {
    'vits': {'encoder': 'vits', 'features': 64, 'out_channels': [48, 96, 192, 384]},
}
depth_model = DepthAnythingV2(**model_configs['vits'])
depth_model.load_state_dict(torch.load(CHECKPOINT, map_location='cpu'))
depth_model = depth_model.to(DEVICE).eval()


def depth_to_color(depth):
    depth_norm = cv2.normalize(depth, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    return cv2.applyColorMap(depth_norm, cv2.COLORMAP_INFERNO)


def draw_boxes(img, results):
    for box in results[0].boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        label = results[0].names[int(box.cls[0])]
        conf = float(box.conf[0])
        mean_depth_text = ''

        crop = img[y1:y2, x1:x2]
        if crop.size > 0:
            depth = depth_model.infer_image(crop)
            mean_depth_text = f' depth={depth.mean():.2f}'

            depth_color = depth_to_color(depth)
            depth_resized = cv2.resize(depth_color, (x2 - x1, y2 - y1))
            img[y1:y2, x1:x2] = depth_resized

        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(img, f'{label} {conf:.2f}{mean_depth_text}',
                    (x1, y1 - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    return img


image_paths = sorted([
    os.path.join(INPUT_DIR, f) for f in os.listdir(INPUT_DIR)
    if f.lower().endswith(('.png', '.jpg', '.jpeg'))
])

for image_path in image_paths:
    img = cv2.imread(image_path)
    if img is None:
        print(f'スキップ: {image_path}')
        continue

    results = yolo(img)
    filename = os.path.basename(image_path)

    if MODE == 'full':
        depth = depth_model.infer_image(img)
        output = depth_to_color(depth)

    elif MODE == 'yolo':
        output = draw_boxes(img.copy(), results)

    elif MODE == 'both':
        depth = depth_model.infer_image(img)
        full_depth = depth_to_color(depth)
        yolo_depth = draw_boxes(img.copy(), results)
        output = np.hstack([yolo_depth, full_depth])

    output_path = os.path.join(OUTPUT_DIR, filename)
    cv2.imwrite(output_path, output)
    print(f'保存完了: {output_path}')
