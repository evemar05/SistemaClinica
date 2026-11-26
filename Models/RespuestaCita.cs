namespace Clinica.Models
{
    public class RespuestaCita
    {
        public int estatus { get; set; }
        public string mensaje { get; set; }
        public CitaModel datos { get; set; }
    }
}
