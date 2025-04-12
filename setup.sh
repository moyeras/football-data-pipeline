#!/bin/bash

echo "🚀 Setting up the project..."

# Install dependencies
pip install -r requirements.txt

# Run the full pipeline
python run_pipeline.py

echo "✅ Setup complete!"
