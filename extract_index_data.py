import os
import re

# 입력 및 출력 디렉토리 설정
input_list_file = 'extract_list_scene_num_icon.txt'  # scene, num, icon_num 리스트 파일
input_text_dir = 'output_results/'  # 파싱된 텍스트 파일이 있는 디렉토리
output_extracted_dir = 'output_extracted_results/'  # 추출된 결과를 저장할 디렉토리

# 출력 디렉토리가 없으면 생성
if not os.path.exists(output_extracted_dir):
    os.makedirs(output_extracted_dir)

# 특정 인덱스의 데이터를 추출하여 텍스트 파일로 저장하는 함수
def extract_and_save_index_data(scene, num, icon_num):
    # 대상 텍스트 파일 경로
    parsed_file_path = os.path.join(input_text_dir, scene, f"parsed_{scene}_{num}.txt")
    
    # 텍스트 파일 읽기
    try:
        with open(parsed_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading {parsed_file_path}: {e}")
        return

    # 특정 인덱스(icon_num)에 해당하는 데이터 찾기
    target_line = None
    for line in lines:
        match = re.match(r'(\d+):', line)
        if match and int(match.group(1)) == icon_num:
            target_line = line.strip()
            break

    if target_line is None:
        print(f"Index {icon_num} not found in {parsed_file_path}")
        return

    # 데이터 파싱
    try:
        # 인덱스와 데이터를 분리
        data_str = re.sub(r'^\d+:\s*', '', target_line)
        data = eval(data_str)  # 문자열을 딕셔너리로 변환 (eval 사용 주의, 안전한 환경에서만 사용)
        bbox = data['bbox']
        content = data['content']

        # 하위 폴더 구조를 유지하며 출력 경로 설정
        output_extracted_subdir = os.path.join(output_extracted_dir, scene)
        if not os.path.exists(output_extracted_subdir):
            os.makedirs(output_extracted_subdir)

        # 추출된 데이터를 텍스트 파일로 저장
        extracted_file_path = os.path.join(output_extracted_subdir, f"extracted_{icon_num}_parsed_{scene}_{num}.txt")
        with open(extracted_file_path, 'w', encoding='utf-8') as f:
            #f.write(f"Index: {icon_num}\n")
            f.write(f"BBox: {bbox}\n")
            f.write(f"Content: {content}")
        print(f"Extracted data saved to: {extracted_file_path}")
    except Exception as e:
        print(f"Error parsing data for index {icon_num} in {parsed_file_path}: {e}")

# 메인 실행 로직
def main():
    # 입력 리스트 파일 읽기
    try:
        with open(input_list_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading {input_list_file}: {e}")
        return

    # 각 줄을 처리
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            scene, num, icon_num = line.split(',')
            icon_num = int(icon_num)
            print(f"\nProcessing: scene={scene}, num={num}, icon_num={icon_num}")
            extract_and_save_index_data(scene, num, icon_num)
        except ValueError as e:
            print(f"Error parsing line '{line}': {e}")
        except Exception as e:
            print(f"Error processing line '{line}': {e}")

if __name__ == "__main__":
    main()