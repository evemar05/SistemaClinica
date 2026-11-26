namespace Clinica.Models
{
    public class RespuestaCitas
    {
        public int estatus { get; set; }
        public string mensaje { get; set; }
        public List<CitaModel> datos { get; set; }
    }
}
