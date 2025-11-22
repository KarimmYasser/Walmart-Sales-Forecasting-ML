"""
Script to train the production model for deployment.
This script properly handles paths and trains the model from stage3.
"""

import sys
from pathlib import Path

# Add stage3/ML_models to path
stage3_path = Path(__file__).parent.parent / 'stage3' / 'ML_models'
sys.path.insert(0, str(stage3_path))

# Check if training data exists
data_path = Path(__file__).parent.parent / 'stage1' / 'processed_data' / 'Stage1.3.4_Final' / 'train_final.csv'

if not data_path.exists():
    print("❌ Training data not found!")
    print(f"   Expected location: {data_path}")
    print("\n📋 To create the training data, run:")
    print("   cd stage1")
    print("   python Stage1_pipline_runner.py")
    print("\nThis will process the raw data and create train_final.csv")
    sys.exit(1)

print("="*70)
print("TRAINING PRODUCTION MODEL")
print("="*70)

# Import and run training
from Best_model import Best_model_results

# Train and save the model
model_save_path = Path(__file__).parent / 'models' / 'best_model.pkl'
model_save_path.parent.mkdir(parents=True, exist_ok=True)

print(f"\n📁 Saving model to: {model_save_path}")

model, metrics = Best_model_results(save_model=True, save_path=str(model_save_path))

print("\n" + "="*70)
print("✅ MODEL TRAINING COMPLETE!")
print("="*70)
print(f"📊 Performance Metrics:")
print(f"   MAE:  ${metrics['MAE']:,.2f}")
print(f"   RMSE: ${metrics['RMSE']:,.2f}")
print(f"   R²:   {metrics['R2']:.4f} ({metrics['R2']*100:.2f}%)")
print(f"\n💾 Model saved to: {model_save_path}")
print("\n🚀 You can now use this model in:")
print("   • FastAPI (run_api.py)")
print("   • Streamlit Dashboard (run_dashboard.py)")
print("="*70)
