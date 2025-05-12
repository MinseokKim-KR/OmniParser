import base64
from PIL import Image
import io
import os
import sys
sys.path.append('C:\\Users\\kimis\\Project\\OmniParser-master\\util')
from omniparser import Omniparser

# OmniParser 설정
config = {
    'som_model_path': 'weights/icon_detect/model.pt',
    'caption_model_name': 'florence2',
    'caption_model_path': 'weights/icon_caption_florence',
    'BOX_TRESHOLD': 0.05
}

# OmniParser 초기화
parser = Omniparser(config)

# 이미지 디렉토리 및 출력 디렉토리 설정
image_dir = 'intai_data/image'
output_dir = 'intai_data/output_results/'  # 드로잉된 이미지를 저장할 디렉토리
output_text_dir = 'intai_data/output_results/'  # 파싱 결과를 저장할 디렉토리
image_extensions = ('.png', '.jpg', '.jpeg')  # 처리할 이미지 확장자

# 출력 디렉토리가 없으면 생성
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
if not os.path.exists(output_text_dir):
    os.makedirs(output_text_dir)

# 이미지 파일 목록 생성 (하위 폴더 포함)
image_paths = []
for root, dirs, files in os.walk(image_dir):
    for file in files:
        if file.lower().endswith(image_extensions):
            image_paths.append(os.path.join(root, file))

# 각 이미지를 처리
for image_path in image_paths:
    print(f"\nProcessing image: {image_path}")
    
    # 이미지 로드 및 base64로 인코딩
    try:
        image = Image.open(image_path).convert('RGB')
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        image_base64 = base64.b64encode(buffered.getvalue()).decode('ascii')

        # OmniParser로 이미지 파싱
        labeled_img, parsed_content = parser.parse(image_base64)

        # 하위 폴더 구조를 유지하며 출력 경로 설정
        relative_path = os.path.relpath(image_path, image_dir)  # imgs/ 기준 상대 경로
        output_subdir = os.path.dirname(relative_path)
        
        # 드로잉된 이미지 저장 경로
        output_image_subdir = os.path.join(output_dir, output_subdir)
        if not os.path.exists(output_image_subdir):
            os.makedirs(output_image_subdir)
        output_image_path = os.path.join(output_image_subdir, f"labeled_{os.path.basename(image_path)}")
        
        # 드로잉된 이미지 저장
        labeled_img_bytes = base64.b64decode(labeled_img)
        labeled_img_pil = Image.open(io.BytesIO(labeled_img_bytes))
        labeled_img_pil.save(output_image_path, format="PNG")
        print(f"Labeled image saved to: {output_image_path}")

        # 결과 출력 (요청된 형식으로)
        print(f"Parsed UI Elements for {image_path}:")
        for idx, item in enumerate(parsed_content):
            print(f"{idx}: {item}")

        # 텍스트 파일로 저장 경로
        output_text_subdir = os.path.join(output_text_dir, output_subdir)
        if not os.path.exists(output_text_subdir):
            os.makedirs(output_text_subdir)
        output_text_path = os.path.join(output_text_subdir, f"parsed_{os.path.splitext(os.path.basename(image_path))[0]}.txt")
        
        # 텍스트 파일로 저장
        with open(output_text_path, 'w', encoding='utf-8') as f:
            for idx, item in enumerate(parsed_content):
                f.write(f"{idx}: {item}\n")
        print(f"Parsed results saved to: {output_text_path}")

    except Exception as e:
        print(f"Error processing {image_path}: {e}")