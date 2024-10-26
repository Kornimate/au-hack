using maui_camera.Services;

namespace maui_camera
{
    public partial class MainPage : ContentPage
    {
        private MainService service;

        public MainPage()
        {
            InitializeComponent();

            service = new MainService();

            service.TakePhoto += UpdateImage;
            service.ConnectionFailed += ResetState;
        }

        private void ResetState(object? sender, EventArgs e)
        {
            Url.IsEnabled = true;
            ClientId.IsEnabled = true;
            StartService.IsEnabled = true;
        }

        private void UpdateImage(object? sender, EventArgs e)
        {
            service.SendToWebSocket(CameraView.GetSnapShot(), Url.Text, ClientId.Text).Wait();
        }

        private void CameraView_CamerasLoaded(object sender, EventArgs e)
        {
            CameraView.Camera = CameraView.Cameras.First();

            MainThread.BeginInvokeOnMainThread(async () =>
            {
                await CameraView.StopCameraAsync();
                await CameraView.StartCameraAsync();
            });
        }

        private void Start_Broadcast(object sender, EventArgs e)
        {
            service.StartBroadcast();

            Url.IsEnabled = false;
            ClientId.IsEnabled = false;
            StartService.IsEnabled = false;
        }
    }

}
