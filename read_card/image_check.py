def num_channels_check(img):
    return img.ndim


def get_image_size(image):
    image_shape = image.shape
    return image_shape[0], image_shape[1]
