import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.append(parent_dir)

from src.eval.eval_harness import EvalHarness

def main():

    config_path = os.path.join(parent_dir, "data", "config.yaml")
  
    ground_truth_path = os.path.join(current_dir, "ground_truth.json")

    if not os.path.exists(config_path):
        print(f"HATA: Config bulunamadı: {config_path}")
        return

    if not os.path.exists(ground_truth_path):
        print(f"HATA: Cevap anahtarı bulunamadı: {ground_truth_path}")
        return

    try:
        harness = EvalHarness(
            config_path=config_path,
            ground_truth_path=ground_truth_path
        )
        harness.run()
    except TypeError as e:
        print(f"Kod hatası: {e}")
        print("Lütfen src/eval/eval_harness.py dosyasını güncellediğinizden emin olun.")
    except Exception as e:
        print(f"Beklenmeyen bir hata: {e}")

if __name__ == "__main__":
    main()