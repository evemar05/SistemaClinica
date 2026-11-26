namespace Clinica.Models
{
    public class LoginDatosModel
    {
        public string usuario { get; set; }
        public string rol { get; set; }
        public string identificacion { get; set; }
    }

    public class RespuestaLogin
    {
        public int estatus { get; set; }
        public string mensaje { get; set; }
        public LoginDatosModel datos { get; set; }
    }
}
