# Hugging Face Spaces Deployment

This app is ready for deployment on Hugging Face Spaces.

## Steps to Deploy:

1. Go to [Hugging Face Spaces](https://huggingface.co/spaces)
2. Click 'Create new Space'
3. Choose 'Gradio' as the SDK
4. Connect to your GitHub repository: https://github.com/karan5719/ML--BASED-SANSKRIT-SANDHI-ANALYZER-
5. Set the main file to 'app.py'
6. Click 'Create Space'

The Space will automatically build and deploy your Gradio app.

## Notes:
- The app uses local model files in the 'models/' directory
- All dependencies are listed in requirements.txt
- The app is configured to run with Gradio's launch() method
