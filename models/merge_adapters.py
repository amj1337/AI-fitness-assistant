from llama_cpp import Llama
from peft import PeftModel

# Load base model
base_model = Llama(
    "./meta-llama-3.1-8b-instruct-q4_k_m.gguf",
    n_gpu_layers=20
)

# Merge with LoRA
merged_model = PeftModel.from_pretrained(
    base_model,
    "workout_lora",
    adapter_name="workout_plan_v1"
)

# Save merged model
merged_model.save_pretrained("merged_fitness_llama")