using maui_camera.Image;
using maui_camera.Models;
using System;
using System.Buffers.Text;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http.Json;
using System.Net.WebSockets;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;

namespace maui_camera.Services
{
    public class MainService
    {
        const int SecondPerFrames = 10;

        private Timer? photoTimer;
        private HttpClient client;

        public event EventHandler? TakePhoto;
        public event EventHandler? ConnectionFailed;

        public MainService()
        {
            client = new HttpClient();
        }

        private void CallForPhoto(object? state)
        {
            TakePhoto?.Invoke(this, EventArgs.Empty);
        }

        public void StartBroadcast()
        {
            photoTimer = new(CallForPhoto, null, TimeSpan.Zero, TimeSpan.FromSeconds(SecondPerFrames));
        }

        public async Task SendToWebSocket(ImageSource image, string url, string id)
        {
            if (string.IsNullOrWhiteSpace(url) || string.IsNullOrWhiteSpace(id))
            {
                ConnectionFailed?.Invoke(this, EventArgs.Empty);
                return;
            }

            try
            {
                var base64Image = ImageConverter.ConvertImageToB64S(await ImageConverter.ConvertImageSourceToByteArray(image), id);
                
                if (base64Image == null)
                    return;

                StringContent content = new StringContent(JsonSerializer.Serialize(new
                {
                    id=id,
                    data=base64Image
                }), Encoding.UTF8, "application/json");

                var response = await client.PostAsync($"{url}/stream-data",content);
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
                photoTimer?.Dispose();
                ConnectionFailed?.Invoke(this, EventArgs.Empty);

                return;
            }
        }
    }
}
