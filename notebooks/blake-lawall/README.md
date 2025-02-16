# AI-Powered Recipe Generator

A Python application that generates recipes and accompanying food photography based on user-provided ingredients, dietary constraints, and items to avoid. The application supports both AWS Bedrock and OpenAI as backend providers.

## Features

- Generate recipes based on:
  - Available ingredients
  - Dietary constraints
  - Food allergies or items to avoid
- Create professional food photography for each recipe
- Web interface built with Gradio
- Flexible provider selection (AWS Bedrock or OpenAI)
- JSON-formatted recipe output
- Responsive HTML recipe display

## Prerequisites

- Python 3.x
- AWS account with Bedrock access (for AWS provider)
- OpenAI API key (for OpenAI provider)
- Required Python packages (see Installation section)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/numberwrangler/SDS-CP017-ai-recipe-wizard.git recipe-generator
cd recipe-generator
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install required packages using requirements.txt:
```bash
pip install -r requirements.txt
```

The requirements.txt file includes:
```
boto3
botocore
openai
gradio
jupyter
ipython
requests

```

3. Set up environment variables:
- For OpenAI provider:
```bash
export OPENAI_API_KEY='your-api-key'
```
- For AWS provider, ensure your AWS credentials are configured:
```bash
aws configure
```

## Usage

You can run the application in two ways:

### Option 1: Web Application
1. Start the application:
```bash
python app.py
```

2. Access the web interface through your browser (http://localhost:7860)

3. In the interface:
   - Select your preferred provider (AWS or OpenAI)
   - Enter ingredients as a comma-separated list
   - Specify any items to avoid
   - Add dietary constraints
   - Click submit to generate your recipe and image


### Option 2: Jupyter Notebook
1. Start Jupyter:
```bash
jupyter lab
```

2. Navigate to and open `RecipeGenerator.ipynb`

3. Run the notebook cells sequentially to:
   - Set up your environment variables
   - Initialize the recipe generator
   - Generate recipes interactively
   - View results with inline image display

## Architecture

The application follows an object-oriented design with the following key components:

- `RecipeGeneratorInterface`: Abstract base class defining the interface for recipe generators
- `AWSRecipeGenerator`: Implementation using AWS Bedrock services
- `OpenAIRecipeGenerator`: Implementation using OpenAI's GPT and DALL-E
- `RecipeGeneratorApp`: Main application class handling the recipe generation workflow
- User Interfaces:
   - Option 1. Gradio Web App
   - Option 2. Jupyter Notebook

## API Providers

### AWS Bedrock
- Uses Claude 3.5 Sonnet for recipe generation
- Uses Stable Diffusion XL for image generation
- Requires AWS credentials and Bedrock access

### OpenAI
- Uses GPT-4 for recipe generation
- Uses DALL-E 3 for image generation
- Requires OpenAI API key

## Example Output

The generator produces:
- Recipe name and description
- List of ingredients with measurements
- Step-by-step instructions
- Cooking time and difficulty level
- Professional food photography
- Dietary constraints summary

## Error Handling

The application includes comprehensive error handling for:
- API authentication failures
- Service availability issues
- Invalid input formats
- Image generation failures

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT Opensource License

## Acknowledgments

- AWS Bedrock team for providing AI services
- OpenAI for their API services
- Gradio team for the web interface framework
- Jupyter Project