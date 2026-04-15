"""
檢查 ONNX 模型的資訊
用於確認模型是否符合 Kneron 的要求
"""

import onnx
import os
import sys

def check_onnx_model(onnx_path):
    """檢查 ONNX 模型的詳細資訊"""
    
    if not os.path.exists(onnx_path):
        print(f"錯誤：找不到 ONNX 檔案 {onnx_path}")
        return False
    
    try:
        # 載入 ONNX 模型
        model = onnx.load(onnx_path)
        
        print("=" * 60)
        print("ONNX 模型資訊")
        print("=" * 60)
        
        # 檢查模型版本
        print(f"\n模型版本:")
        print(f"  - IR Version: {model.ir_version}")
        print(f"  - Producer Name: {model.producer_name}")
        print(f"  - Producer Version: {model.producer_version}")
        print(f"  - Domain: {model.domain}")
        print(f"  - Model Version: {model.model_version}")
        
        # 檢查輸入
        print(f"\n輸入資訊:")
        for i, input_tensor in enumerate(model.graph.input):
            print(f"  輸入 {i+1}:")
            print(f"    - 名稱: {input_tensor.name}")
            shape = [dim.dim_value if dim.dim_value > 0 else '?' 
                    for dim in input_tensor.type.tensor_type.shape.dim]
            print(f"    - 形狀: {shape}")
            print(f"    - 資料類型: {onnx.TensorProto.DataType.Name(input_tensor.type.tensor_type.elem_type)}")
        
        # 檢查輸出
        print(f"\n輸出資訊:")
        for i, output_tensor in enumerate(model.graph.output):
            print(f"  輸出 {i+1}:")
            print(f"    - 名稱: {output_tensor.name}")
            shape = [dim.dim_value if dim.dim_value > 0 else '?' 
                    for dim in output_tensor.type.tensor_type.shape.dim]
            print(f"    - 形狀: {shape}")
            print(f"    - 資料類型: {onnx.TensorProto.DataType.Name(output_tensor.type.tensor_type.elem_type)}")
        
        # 檢查 Opset 版本
        print(f"\nOpset 版本:")
        for opset in model.opset_import:
            print(f"  - {opset.domain}: {opset.version}")
        
        # 驗證模型
        print(f"\n模型驗證:")
        try:
            onnx.checker.check_model(model)
            print("  [OK] 模型驗證通過")
        except onnx.checker.ValidationError as e:
            print(f"  [ERROR] 模型驗證失敗: {e}")
            return False
        
        # Kneron 相容性檢查
        print(f"\nKneron 相容性檢查:")
        issues = []
        
        # 檢查輸入數量
        if len(model.graph.input) != 1:
            issues.append(f"警告：模型有 {len(model.graph.input)} 個輸入，Kneron 通常期望 1 個輸入")
        
        # 檢查輸入尺寸是否固定
        input_shape = model.graph.input[0].type.tensor_type.shape.dim
        has_dynamic_dim = any(dim.dim_value == 0 for dim in input_shape)
        if has_dynamic_dim:
            issues.append("警告：模型有動態維度，Kneron 可能需要固定尺寸")
        
        # 檢查輸入尺寸是否為 640x640
        if len(input_shape) >= 3:
            h = input_shape[2].dim_value if input_shape[2].dim_value > 0 else None
            w = input_shape[3].dim_value if input_shape[3].dim_value > 0 else None
            if h != 640 or w != 640:
                issues.append(f"警告：輸入尺寸為 {h}x{w}，YOLOv8 通常使用 640x640")
        
        if issues:
            for issue in issues:
                print(f"  [WARNING] {issue}")
        else:
            print("  [OK] 模型看起來符合 Kneron 的要求")
        
        print("\n" + "=" * 60)
        return True
        
    except Exception as e:
        print(f"錯誤：無法讀取 ONNX 檔案: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    # 預設 ONNX 檔案路徑
    default_onnx = "kneron_workspace/best.onnx"
    
    if len(sys.argv) > 1:
        onnx_path = sys.argv[1]
    else:
        onnx_path = default_onnx
    
    print(f"檢查 ONNX 檔案: {onnx_path}\n")
    check_onnx_model(onnx_path)

if __name__ == "__main__":
    main()

