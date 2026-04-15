# -*- coding: utf-8 -*-
"""
在 kneron/toolchain 容器內執行（需 conda env onnx1.13）：
ONNX -> 量化分析 -> batch compile，產出 KL520 用 NEF。
校準影像預設使用映像內 /workspace/examples/mobilenetv2/images（僅作校準統計用）。
"""
import os
import sys

import numpy as np
import onnx
from PIL import Image

sys.path.insert(0, "/workspace")

import ktc  # noqa: E402


def preprocess_yolo640(path: str) -> np.ndarray:
    image = Image.open(path).convert("RGB")
    image = image.resize((640, 640), Image.BILINEAR)
    img_data = np.asarray(image, dtype=np.float32) / 255.0
    img_data = np.transpose(img_data, (2, 0, 1))
    return np.expand_dims(img_data, 0)


def main() -> None:
    # 主機專案掛在 /project，勿掛載到 /workspace（會覆蓋映像內 toolchain）
    project = os.environ.get("KNERON_PROJECT", "/project")
    onnx_path = os.path.join(project, "kneron_workspace", "best.onnx")
    if os.environ.get("KNERON_ONNX"):
        onnx_path = os.environ["KNERON_ONNX"]
    if not os.path.isfile(onnx_path):
        raise SystemExit(f"[ERROR] 找不到 ONNX: {onnx_path}")

    local_calib = os.path.join(project, "kneron_workspace", "calib")
    calib_dir = (
        local_calib
        if os.path.isdir(local_calib)
        and any(
            f.lower().endswith((".jpg", ".jpeg", ".png"))
            for f in os.listdir(local_calib)
        )
        else "/workspace/examples/mobilenetv2/images"
    )
    names = sorted(
        f for f in os.listdir(calib_dir) if f.lower().endswith((".jpg", ".jpeg", ".png"))
    )
    if not names:
        raise SystemExit(f"[ERROR] 校準目錄沒有影像: {calib_dir}")

    input_images = [preprocess_yolo640(os.path.join(calib_dir, n)) for n in names]
    print(f"[KL520] 校準影像目錄: {calib_dir}（共 {len(names)} 張，建議改放 kneron_workspace/calib/ 真實場景圖）")

    out_dir = os.environ.get("KNERON_KL520_OUT", "/data1/kneron_flow")
    os.makedirs(out_dir, exist_ok=True)

    print("[KL520] ONNX preprocess (torch_exported -> kneron optimize)...")
    model_proto = onnx.load(onnx_path)
    model_proto = ktc.onnx_optimizer.torch_exported_onnx_flow(model_proto)
    onnx_kn = os.path.join(out_dir, "best_kl520_prep.onnx")
    onnx.save(model_proto, onnx_kn)
    print(f"[KL520] 使用輸入 ONNX: {onnx_path} -> {onnx_kn}")

    rng = np.random.RandomState(0)
    random_inputs = [
        np.clip(rng.randn(1, 3, 640, 640).astype(np.float32) * 0.25 + 0.5, 0.0, 1.0)
        for _ in range(8)
    ]
    input_mapping = {"images": random_inputs + input_images}

    # 與既有 KL530 流程相同 model id，可依部署需求修改
    km = ktc.ModelConfig(32770, "0001", "520", onnx_path=onnx_kn)

    print("[KL520] fix point analysis (knerex)...")
    km.analysis(
        input_mapping,
        output_dir=out_dir,
        threads=4,
        percentage=0.999,
        percentage_16b=0.999999,
    )

    print("[KL520] batch compile -> NEF...")
    nef_path = ktc.compile([km], output_dir=out_dir)
    print(f"[KL520] 完成: {nef_path}")


if __name__ == "__main__":
    main()
