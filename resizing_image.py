from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# Função para salvar uma imagem no formato PPM
def save_as_ppm(image, output_file):
    image = Image.open(lenna_png).convert("RGB")  # Certifica-se de que está em RGB
    width, height = image.size
    pixels = list(image.getdata())
    with open(output_file, 'w') as f:
        f.write("P3\n")  # Formato RGB no PPM
        f.write(f"{width} {height}\n")
        f.write("255\n")  # Máximo valor de cor
        for pixel in pixels:
            f.write(f"{pixel[0]} {pixel[1]} {pixel[2]} ")
            if (pixels.index(pixel) + 1) % width == 0:
                f.write("\n")
    print(f"Imagem salva no formato PPM: {output_file}")

def save_as_ppm_optimized(input_path, output_path): # Usa o numpy para obter o array de pixels, melhorando a performance.
    # Carregar a imagem
    lenna = Image.open(input_path).convert("RGB")
    pixels = np.array(lenna)

    # Obter dimensões
    height, width, _ = pixels.shape

    # Escrever o arquivo PPM
    with open(output_path, "w") as f:
        f.write("P3\n")
        f.write(f"{width} {height}\n")
        f.write("255\n")

        # Converter pixels para strings e escrever em blocos
        for row in pixels:
            f.write(" ".join(f"{r} {g} {b}" for r, g, b in row) + "\n")


# Função para converter PPM para tons de cinza
def ppm_to_grayscale(ppm_file, output_file):
    with open(ppm_file, 'r') as f:
        # Leia o cabeçalho
        header = f.readline().strip()
        dimensions = f.readline().strip()
        max_val = f.readline().strip()

        if header != "P3":
            raise ValueError("O arquivo PPM deve estar no formato P3.")

        width, height = map(int, dimensions.split())
        pixels = []
        for line in f:
            pixels.extend(map(int, line.split()))

        # Processar os valores RGB e converter para tons de cinza
        gray_pixels = []
        for i in range(0, len(pixels), 3):
            r, g, b = pixels[i], pixels[i+1], pixels[i+2]
            gray = int(0.299 * r + 0.587 * g + 0.114 * b)  # Fórmula Y'601
            gray_pixels.append(gray)

    # Escrever a saída no formato PPM
    with open(output_file, 'w') as f:
        f.write("P2\n")  # Formato de tons de cinza
        f.write(f"{width} {height}\n")
        f.write("255\n")
        for i, gray in enumerate(gray_pixels):
            f.write(f"{gray} ")
            if (i + 1) % width == 0:
                f.write("\n")

    print(f"Imagem convertida para tons de cinza salva em {output_file}")


# Função para converter tons de cinza para binário
def ppm_to_binary(ppm_file, output_file, threshold=128):
    with open(ppm_file, 'r') as f:
        # Leia o cabeçalho
        header = f.readline().strip()
        dimensions = f.readline().strip()
        max_val = f.readline().strip()

        if header != "P2":
            raise ValueError("O arquivo PPM deve estar no formato P2 (tons de cinza).")

        width, height = map(int, dimensions.split())
        pixels = []
        for line in f:
            pixels.extend(map(int, line.split()))

        # Converta para preto e branco
        binary_pixels = [0 if pixel >= threshold else 1 for pixel in pixels]

    # Escrever a saída no formato PPM
    with open(output_file, 'w') as f:
        f.write("P1\n")  # Formato binário
        f.write(f"{width} {height}\n")
        for i, binary in enumerate(binary_pixels):
            f.write(f"{binary} ")
            if (i + 1) % width == 0:
                f.write("\n")

    print(f"Imagem convertida para preto e branco salva em {output_file}")


# Função para converter uma imagem usando Pillow
def convert_image(input_file, output_file, mode=None):
    img = Image.open(input_file)
    if mode:
        img = img.convert(mode)
    img.save(output_file)
    print(f"Imagem convertida e salva como {output_file}")


# Caminhos dos arquivos
lenna_png = "images/lenna.png"
lenna_ppm = "images/lenna.ppm"
lenna_gray_ppm = "images/lenna_gray.ppm"
lenna_binary_ppm = "images/lenna_binary.ppm"
lenna_gray_png = "images/lenna_gray.png"
lenna_binary_png = "images/lenna_binary.png"

# Passo 1: Converter PNG para PPM
save_as_ppm_optimized(lenna_png, lenna_ppm)

# Passo 2: Converter PPM para tons de cinza
ppm_to_grayscale(lenna_ppm, lenna_gray_ppm)

# Passo 3: Converter tons de cinza para binário
ppm_to_binary(lenna_gray_ppm, lenna_binary_ppm, threshold=128)

# Passo 4: Converter PPMs modificados de volta para PNG
convert_image(lenna_gray_ppm, lenna_gray_png)
convert_image(lenna_binary_ppm, lenna_binary_png)


# Exibe os resultados
original_image = np.array(Image.open(lenna_png))
gray_image = np.array(Image.open(lenna_gray_png))
binary_image = np.array(Image.open(lenna_binary_png))

plt.figure(figsize=(12, 4))
plt.subplot(1, 3, 1)
plt.title("Original")
plt.imshow(original_image)
plt.subplot(1, 3, 2)
plt.title("Tons de Cinza")
plt.imshow(gray_image, cmap='gray')
plt.subplot(1, 3, 3)
plt.title("Binário")
plt.imshow(binary_image, cmap='gray')
plt.show()
