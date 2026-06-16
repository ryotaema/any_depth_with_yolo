# any_depth_yolo

YOLOで検出したオブジェクト領域、または画像全体に対して Depth Anything V2 による深度推定を行うスクリプト。

## ディレクトリ構成

```
any_depth_yolo/
├── yolo_depth.py
├── input/                  # 入力画像を置く
├── output/                 # 推定結果が保存される
└── model/
    ├── yolo_model/
    │   └── 260410_pepper_yolo11.pt
    └── depth_anything_model/
        └── depth_anything_v2_vits.pth
```

Depth-Anything-V2 リポジトリが同階層に必要です。

```
depth_anything/
├── any_depth_yolo/     ← このプロジェクト
└── Depth-Anything-V2/  ← 別途クローン
```

## セットアップ

```bash
# Depth Anything V2 リポジトリのクローン（未実施の場合）
cd /home/ryota/harvesting_ws/depth_anything
git clone https://github.com/DepthAnything/Depth-Anything-V2

# 依存関係のインストール
pip install -r Depth-Anything-V2/requirements.txt
pip install ultralytics
```

## 使い方

1. `input/` に画像（PNG / JPG）を置く
2. `yolo_depth.py` の `MODE` を設定する
3. スクリプトを実行する

```bash
cd /home/ryota/harvesting_ws/depth_anything/any_depth_yolo
python yolo_depth.py
```

結果は `output/` に入力と同じファイル名で保存される。

## MODE の設定

`yolo_depth.py` 上部の `MODE` 変数で動作を切り替える。

| MODE | 動作 |
|------|------|
| `'yolo'` | YOLOで検出した領域のみに深度推定。BBoxと深度カラーマップを重ねて表示する |
| `'full'` | 画像全体に深度推定。カラーマップ画像を出力する |
| `'both'` | `yolo` と `full` の結果を横並びで出力する |

```python
MODE = 'yolo'  # ← ここを変更
```

## モデル

| モデル | 用途 | 備考 |
|--------|------|------|
| `260410_pepper_yolo11.pt` | ピーマン検出（YOLO11） | カスタム学習済みモデル |
| `depth_anything_v2_vits.pth` | 深度推定（ViT-Small） | Depth Anything V2 公式モデル |

Depth Anything V2 の他のモデルを使う場合は、`CHECKPOINT` とモデル設定を変更する。

| エンコーダ | パラメータ数 | `model_configs` キー |
|-----------|-------------|----------------------|
| ViT-Small | 24.8M       | `vits` |
| ViT-Base  | 97.5M       | `vitb` |
| ViT-Large | 335.3M      | `vitl` |
# any_depth_with_yolo
