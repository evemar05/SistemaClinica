namespace Clinica.Models
{
    public class RespuestaFacturas
    {
        public int estatus { get; set; }
        public string mensaje { get; set; }
        public List<FacturaModel> datos { get; set; }
    }
}
