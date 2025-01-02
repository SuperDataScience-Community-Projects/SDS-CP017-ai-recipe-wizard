# Function to send a prompt to generate image as per the recipe
def generate_image(client, image_prompt, size="1024x1024"):
  response = client.images.generate(
      model="dall-e-3",
      prompt=image_prompt,
      n=1,  # Number of images to generate
      size=size  # Image size
  )
   # Extract the generated image URL
  return response.data[0].url
