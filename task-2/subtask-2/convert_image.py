from PIL import Image

def main():
    image = Image.open("image.jpg")
    bw_image = image.convert("L")
    bw_image.show()

if __name__ == "__main__":
    main()