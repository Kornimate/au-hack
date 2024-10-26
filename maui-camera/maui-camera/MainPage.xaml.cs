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
        }

        private void UpdateImage(object? sender, EventArgs e)
        {
            service.SendToWebSocket(CameraView.GetSnapShot(), Url.Text, Id.Text).Wait();
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
    }

}
