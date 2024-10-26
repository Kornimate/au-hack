using maui_camera.Image;
using System;
using System.Buffers.Text;
using System.Collections.Generic;
using System.Linq;
using System.Net.WebSockets;
using System.Text;
using System.Threading.Tasks;

namespace maui_camera.Services
{
    public class MainService
    {
        private Timer photoTimer;
        private ClientWebSocket ws;

        public event EventHandler? TakePhoto;

        public MainService()
        {
            photoTimer = new(CallForPhoto, null, TimeSpan.Zero, TimeSpan.FromSeconds(1));
            ws = new ClientWebSocket();
        }

        private void CallForPhoto(object? state)
        {
            TakePhoto?.Invoke(this, EventArgs.Empty);
        }

        public async Task SendToWebSocket(ImageSource image, string url, string id)
        {
            if (string.IsNullOrWhiteSpace(url))
                return;

            if (ws.State != WebSocketState.Open)
            {
                await ws.ConnectAsync(new Uri(url), CancellationToken.None);
            }

            var byteArrayImage = ImageConverter.ConvertImageAndAddId(await ImageConverter.ConvertImageSourceToByteArray(image), id);

            if (byteArrayImage == null)
                return;

            try
            {
                await ws.SendAsync(new ArraySegment<byte>(byteArrayImage),
                                    WebSocketMessageType.Binary,
                                    endOfMessage: true,
                                    cancellationToken: CancellationToken.None);
            }
            catch (Exception) { }
        }
    }
}
