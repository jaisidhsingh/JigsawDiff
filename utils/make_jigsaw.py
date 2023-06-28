from tqdm import tqdm
import numpy as np
from PIL import Image
import random
import os
import sys

cwd = os.getcwd()
module2add = '/'.join(cwd.split("/")[:-1])
sys.path.append(module2add)

from configs import configs 


def create_jigsaw_puzzle(input_image_path, save_path, image_size=256, patch_size=64):
	input_image = Image.open(input_image_path)

	resized_image = input_image.resize((image_size, image_size))
	image_array = np.array(resized_image)
	patches_per_side = image_size // patch_size

	patches = np.split(image_array, patches_per_side, axis=0)
	patches = [np.split(patch, patches_per_side, axis=1) for patch in patches]

	patch_list = [patch for row in patches for patch in row]
	random.shuffle(patch_list)

	puzzle_size = patch_size * patches_per_side
	puzzle_image = Image.new('RGB', (puzzle_size, puzzle_size))

	for i in range(patches_per_side):
		for j in range(patches_per_side):
			patch = patch_list[i * patches_per_side + j]
			patch_image = Image.fromarray(patch)
			puzzle_image.paste(patch_image, (j * patch_size, i * patch_size))

	puzzle_image.save(save_path)

def resize_images(image_dir, new_size=256):
	image_names = os.listdir(image_dir)
	image_names.sort()
	image_paths = [os.path.join(image_dir, p) for p in image_names]

	for path in tqdm(image_paths):
		img = Image.open(path).convert("RGB")
		img = img.resize((new_size, new_size))
		img.save(path)
	
	print("Done!")

def make_jigsaw_dataset(base_image_dir, output_dir):
	image_names = os.listdir(base_image_dir)
	image_names.sort()
	image_paths = [os.path.join(base_image_dir, p) for p in image_names]

	for i, input_path in tqdm(enumerate(image_paths)):
		save_name = image_names[i]
		save_path = os.path.join(output_dir, save_name)

		create_jigsaw_puzzle(input_path, save_path)
	
	print("Done!")


if __name__ == "__main__":
	random.seed(configs.random_seed)

	base_dir = os.path.join(configs.dataset_dir, configs.dataset_name, "base_images")
	output_dir = os.path.join(configs.dataset_dir, configs.dataset_name, "shuffled_images")

	resize_images(base_dir)	
	# make_jigsaw_dataset(base_dir, output_dir)
