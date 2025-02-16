from __init__ import client  # Import the OpenAI client from __init__.py
#from __init__ import init_client_openaikey


def generate_image(image_prompt, num_images=1, image_size="1024x1024"):
    """
    Generate an image using the DALL·E API.

    Args:
        image_prompt (str): The prompt describing the image to generate.
        num_images (int): The number of images to generate (default is 1).
        image_size (str): The resolution of the generated image (default is "1024x1024").

    Returns:
        list: A list of URLs for the generated images.
    """
    try:
        # Call the OpenAI API to generate images
        # init_client_openaikey()
        response = client.images.generate(
            prompt=image_prompt,
            n=num_images,  # Number of images to generate
            size=image_size  # Image resolution
        )

        # Extract and return all image URLs
        image_urls = [data.url for data in response.data]
        return image_urls

    except Exception as e:
        # Handle errors gracefully
        print(f"Error generating image: {e}")
        raise RuntimeError(f"Failed to generate image: {e}")