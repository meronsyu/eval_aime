import json
import os
import re

def remove_duplicate_entries(input_filepath, output_filepath):
    """
    JSONファイルから重複するIDのエントリを削除し、最初に出現したもののみを保持します。
    ファイルは { "id1": {...}, "id2": {...} } の形式を想定しています。
    """
    try:
        # JSONファイルを読み込む
        with open(input_filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 辞書のキーは重複を許さないため、
        # json.load()の時点でキーが重複していた場合、最後に出現した値が保持されます。
        # ユーザーの意図（「最初に出現したもののみを保持」）とは異なる動作になります。
        # そこで、一旦読み込んだデータを順番を保持できるOrderedDict（Python 3.7以降はdict）
        # に変換し、重複をチェックしながら再構築します。

        # 読み込んだファイルの内容を一旦文字列として取得
        with open(input_filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # 正規表現を使用して、個々のキーと値のペアを抽出
        # ここではよりシンプルな正規表現を使用します
        pattern = r'"([a-fA-F0-9]+)"\s*:\s*(\{.*?\})'
        matches = re.finditer(pattern, content, re.DOTALL)

        unique_data = {}
        for match in matches:
            key = match.group(1)
            value_str = match.group(2)
            
            if key not in unique_data:
                # 重複していないキーの場合のみ追加
                try:
                    # 値をJSONとして読み込む
                    unique_data[key] = json.loads(value_str)
                except json.JSONDecodeError as e:
                    print(f"エラー: ID '{key}' の値のJSONデコードに失敗しました。詳細: {e}")
                    # デコードできないエントリはスキップするか、そのまま文字列として保持するなどの対応が必要
                    pass

        # 処理結果を新しいファイルに書き出す
        os.makedirs(os.path.dirname(output_filepath), exist_ok=True)
        with open(output_filepath, 'w', encoding='utf-8') as f:
            json.dump(unique_data, f, indent=4, ensure_ascii=False)

        print(f"重複削除が完了しました。元のファイルには {len(data)} 件のエントリがありました。")
        print(f"重複を削除し、ユニークな {len(unique_data)} 件のエントリを '{output_filepath}' に保存しました。")

    except FileNotFoundError:
        print(f"エラー: ファイル '{input_filepath}' が見つかりません。")
    except json.JSONDecodeError as e:
        print(f"エラー: JSONファイルのデコードに失敗しました。詳細: {e}")

# --- 使用例 ---
if __name__ == "__main__":
    input_file = "./predictions/hle_Qwen3-32B.json"
    output_file = "./predictions/hle_Qwen3-32B-deduplicated.json"
    
    remove_duplicate_entries(input_file, output_file)