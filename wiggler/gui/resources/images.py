import wx

from wiggler.core.resources.images import Image as CoreImage


class Image(CoreImage):

    def __init__(self, asset_id, scaleTo=None):
        super(Image, self).__init__(asset_id)

        self.bitmap = wx.Bitmap(self._data_filepath)

    def get_bitmap(self, scale=None):
        if scale is None:
            bitmap = self.bitmap
        else:
            width, height = scale
            image = wx.ImageFromBitmap(self.bitmap)
            image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
            bitmap = wx.BitmapFromImage(image)

        return bitmap
