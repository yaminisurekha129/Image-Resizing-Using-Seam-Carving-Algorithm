import numpy as np
from PIL import Image
from PIL import ImageFilter
import numpy as np
from PIL import Image, ImageFilter


# Rest of the code remains unchanged

def energy_map(image):
    """
    Calculate the energy map of the given image using the gradient magnitude.
    """
    grayscale_image = image.convert('L')
    gradient_x = np.array(grayscale_image.filter(ImageFilter.FIND_EDGES)).astype(np.float32)
    gradient_y = np.array(grayscale_image.transpose(Image.TRANSPOSE).filter(ImageFilter.FIND_EDGES)).astype(np.float32)

    gradient_y = np.resize(gradient_y, (image.size[1], image.size[0]))  # Resize gradient_y to match the width of the image

    energy_map = np.sqrt(np.square(gradient_x) + np.square(gradient_y))
    return energy_map


def seam_carving(image, new_width, new_height):
    """
    Seam carving algorithm to resize the image.
    """
    width, height = image.size

    # Calculate energy map of the original image
    energy = energy_map(image)

    # Dynamic programming to find the minimum energy seam
    dp = energy.copy()
    for row in range(1, height):
        dp[row, 0] += min(dp[row - 1, 0], dp[row - 1, 1])
        dp[row, width - 1] += min(dp[row - 1, width - 2], dp[row - 1, width - 1])
        for col in range(1, width - 1):
            dp[row, col] += min(dp[row - 1, col - 1], dp[row - 1, col], dp[row - 1, col + 1])

    # Find the minimum energy seam by backtracking
    seam = []
    j = np.argmin(dp[-1])
    seam.append((height - 1, j))
    for i in reversed(range(height - 1)):
        if j == 0:
            j = np.argmin(dp[i, j:j + 2])
        elif j == width - 1:
            j = np.argmin(dp[i, j - 1:j + 1]) + j - 1
        else:
            j = np.argmin(dp[i, j - 1:j + 2]) + j - 1
        seam.append((i, j))

    # Remove the minimum energy seam from the image
    new_image = image.copy()
    for row, col in seam:
        new_image.putpixel((col, row), (255, 255, 255))  # Set seam pixels to white
    new_image = new_image.crop((0, 0, width - 1, height))  # Remove seam

    # Resize the image to the desired dimensions
    resized_image = new_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    resized_image = new_image.resize((new_width, new_height), Image.LANCZOS)


    return resized_image


# Main program
if __name__ == '__main__':
    # Input the image file dynamically
    image_path = input("Enter the path to the image file: ")
    image = Image.open(image_path)

    # Input the desired width and height dynamically
    new_width = int(input("Enter the desired width: "))
    new_height = int(input("Enter the desired height: "))

    # Perform seam carving
    resized_image = seam_carving(image, new_width, new_height)

    # Display the resized image
    resized_image.show()
