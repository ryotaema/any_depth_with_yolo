# any_depth_yolo

YOLOで検出したオブジェクト領域、または画像全体に対して Depth Anything V2 による深度推定を行うスクリプト。

## ディレクトリ構成

```
any_depth_yolo/
├── yolo_depth.py
├── input/                       # 入力画像を置く
├── output/                      # 推定結果が保存される
└── model/
    ├── yolo_model/              # YOLOモデルを置く
    └── depth_anything_model/    # Depth Anything V2 モデルを置く
```

Depth-Anything-V2 リポジトリが同階層に必要です。

```
depth_anything/
├── any_depth_yolo/     ← このプロジェクト
└── Depth-Anything-V2/  ← 別途クローン
```

## セットアップ

```bash
# Depth Anything V2 リポジトリのクローン
cd /path/to/depth_anything
git clone https://github.com/DepthAnything/Depth-Anything-V2

# 依存関係のインストール
pip install -r Depth-Anything-V2/requirements.txt
pip install ultralytics
```

### モデルの配置

**YOLOモデル**を `model/yolo_model/` に置く。

**Depth Anything V2 モデル**を `model/depth_anything_model/` に置く。
公式モデルは [Hugging Face](https://huggingface.co/depth-anything) からダウンロードできる。

```bash
wget -P model/depth_anything_model \
  https://huggingface.co/depth-anything/Depth-Anything-V2-Small/resolve/main/depth_anything_v2_vits.pth
```

## 使い方

1. `input/` に画像（PNG / JPG）を置く
2. `yolo_depth.py` の `MODE` を設定する
3. スクリプトを実行する

```bash
cd /path/to/any_depth_yolo
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

Depth Anything V2 のエンコーダは以下から選択できる。使用するモデルに合わせて `CHECKPOINT` と `model_configs` のキーを変更する。

| エンコーダ | パラメータ数 | model_configs キー |
|-----------|-------------|-------------------|
| ViT-Small | 24.8M       | vits |
| ViT-Base  | 97.5M       | vitb |
| ViT-Large | 335.3M      | vitl |

## ライセンス

本プロジェクト（`yolo_depth.py`）は [GNU Affero General Public License v3.0 (AGPL-3.0)](LICENSE) の下で公開されています。
Copyright (C) 2026 Ryota Ema

本プロジェクトは以下のライブラリを使用しています。

### Ultralytics（AGPL-3.0）

本プロジェクトは [Ultralytics](https://github.com/ultralytics/ultralytics) を使用しています。

> Ultralytics is licensed under the [GNU Affero General Public License v3.0 (AGPL-3.0)](https://github.com/ultralytics/ultralytics/blob/main/LICENSE).
> Copyright (c) Ultralytics

**AGPL-3.0 の主な義務：**
- 本プロジェクトのソースコードを配布する場合、AGPL-3.0 の条件下で公開する必要があります（コピーレフト条項）。
- ネットワーク越しにサービスとして提供する場合も、ソースコードの開示義務が生じます。
- 著作権表示およびライセンス表記を保持する必要があります。

商用利用や AGPL 非適合の環境での使用には、Ultralytics の [Enterprise License](https://www.ultralytics.com/license) が必要です。

### Depth Anything V2（Apache-2.0）

本プロジェクトは [Depth Anything V2](https://github.com/DepthAnything/Depth-Anything-V2) を使用しています。

> Depth Anything V2 is licensed under the [Apache License 2.0](https://github.com/DepthAnything/Depth-Anything-V2/blob/main/LICENSE).
> Copyright (c) 2024 Depth Anything Team
