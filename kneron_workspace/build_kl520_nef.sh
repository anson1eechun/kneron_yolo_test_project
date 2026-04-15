#!/bin/bash
# 在 kneron/toolchain 容器內執行：以 ktc Python API 產出 KL520 NEF
set -eu
source /workspace/miniconda/etc/profile.d/conda.sh
conda activate onnx1.13
export PYTHONPATH="/workspace:${PYTHONPATH:-}"
mkdir -p /data1/kneron_flow
cd /project/kneron_workspace
echo "[build_kl520_nef] PYTHON=$(which python3)"
exec python3 build_kl520_ktc.py
