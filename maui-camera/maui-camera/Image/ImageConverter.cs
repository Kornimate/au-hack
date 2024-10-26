using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace maui_camera.Image
{
    public static class ImageConverter
    {
        public static ImageSource? ConvertByteArrayToImageSource(byte[] bytes)
        {
            if (bytes == null || bytes.Length == 0)
                return null;

            using MemoryStream ms = new(bytes);

            return ImageSource.FromStream(() => ms);
        }

        public static async Task<byte[]?> ConvertImageSourceToByteArray(ImageSource imageSource)
        {
            if(imageSource is StreamImageSource streamImageSource)
            {
                using var stream = await streamImageSource.Stream(CancellationToken.None);

                using MemoryStream ms = new MemoryStream();

                await stream.CopyToAsync(ms);

                return ms.ToArray();
            }

            return null;
        }

        public static byte[]? ConvertImageAndAddId(byte[]? img, string id)
        {
            if (img == null)
                return img;

            string imgb64 = Convert.ToBase64String(img);

            imgb64 += ("&&" + id); //not in base64 encoding

            return Encoding.UTF8.GetBytes(imgb64);
        }
    }
}
