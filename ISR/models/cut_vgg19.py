from tensorflow.keras.models import Model
from tensorflow.keras.applications.vgg19 import VGG19
from ISR.utils.logger import get_logger


class Cut_VGG19:
    """
    Class object that fetches keras' VGG19 model trained on the imagenet dataset
    and declares <layers_to_extract> as output layers. Used as feature extractor
    for the perceptual loss function.

    Args:
        layers_to_extract: list of layers to be declared as output layers.
        patch_size: integer, defines the size of the input (patch_size x patch_size).

    Attributes:
        loss_model: multi-output vgg architecture with <layers_to_extract> as output layers.
    """

    def __init__(self, patch_size, layers_to_extract):
        self.patch_size = patch_size
        self.input_shape = (patch_size,) * 2 + (3,)
        self.layers_to_extract = layers_to_extract
        self.logger = get_logger(__name__)

        if len(self.layers_to_extract) > 0:
            self._cut_vgg()
        else:
            self.logger.error('Invalid VGG instantiation: extracted layer must be > 0')
            raise ValueError('Invalid VGG instantiation: extracted layer must be > 0')

    def _cut_vgg(self):
        """
        Loads pre-trained VGG, declares as output the intermediate
        layers selected by self.layers_to_extract.
        """

        vgg = VGG19(weights='imagenet', include_top=False, input_shape=self.input_shape)
        vgg.trainable = False
        outputs = [vgg.layers[i].output for i in self.layers_to_extract]
        self.model = Model([vgg.input], outputs)
        self.model._name = 'feature_extractor'
        self.name = 'vgg19'  # used in weights naming
