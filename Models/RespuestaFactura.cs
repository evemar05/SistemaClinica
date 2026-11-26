namespace Clinica.Models
{
    public class RespuestaFactura
    {
        public int estatus { get; set; }
        public string mensaje { get; set; }
        public FacturaModel datos { get; set; }
    }
}
