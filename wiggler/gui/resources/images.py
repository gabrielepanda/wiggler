import wx


class Image(object):

    def __init__(self, core_image, scaleTo=None):
        self._core_image = core_image
        self.bitmap = wx.Bitmap(self._core_image._data_filepath)

    def get_bitmap(self, scale=None):
        if scale is None:
            bitmap = self.bitmap
        else:
            width, height = scale
            image = wx.ImageFromBitmap(self.bitmap)
            image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
            bitmap = wx.BitmapFromImage(image)

        return bitmap
