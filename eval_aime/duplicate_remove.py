## checkするだけ
import os
import re

def check_for_duplicate_ids_by_model_keyword(filepath):
    """
    JSONファイルを読み込み、"model"キーワードの直前にあるIDを正規表現で抽出し、
    重複がないかを確認します。
    """
    all_ids = []

    print(f"Reading and extracting IDs from: {filepath}")

    try:
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File not found at '{filepath}'")
        return False, []

    # "ID": { "model": ... } のパターンを抽出する正規表現
    # `"([a-fA-F0-9]+)"` -> ID（16進数文字列）をキャプチャ
    # `\s*:\s*\{` -> コロンと中括弧の間の空白にマッチ
    # `.*?` -> "model"キーワードまでの非貪欲マッチ
    # `"model":` -> "model"キーワードにマッチ
    pattern = re.compile(r'"([a-fA-F0-9]+)"\s*:\s*\{.*?\"model\":', re.DOTALL)
    
    matches = pattern.finditer(content)
    
    for match in matches:
        all_ids.append(match.group(1))

    total_ids = len(all_ids)
    unique_ids_set = set(all_ids)
    unique_ids = len(unique_ids_set)
    has_duplicates = total_ids != unique_ids

    print("\n--- Summary ---")
    print(f"Total number of IDs found: {total_ids}")
    print(f"Number of unique IDs: {unique_ids}")

    if has_duplicates:
        duplicate_count = total_ids - unique_ids
        print(f"Result: DUPLICATES FOUND! ({duplicate_count} duplicate(s))")
        
        # 重複IDのリストを生成
        duplicate_list = [id for id in all_ids if all_ids.count(id) > 1]
        
        return True, duplicate_list
    else:
        print("Result: No duplicates found.")
        return False, []

# --- 使用例 ---
if __name__ == "__main__":
    filepath_to_check = "./predictions/hle_Qwen3-32B.json" 
    
    has_dupes, dupes_list = check_for_duplicate_ids_by_model_keyword(filepath_to_check)
    if has_dupes:
        print(f"\n対応が必要です。重複IDが含まれています: {set(dupes_list)}")