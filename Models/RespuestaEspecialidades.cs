namespace Clinica.Models
{
    public class RespuestaEspecialidades
    {
        public int estatus { get; set; }
        public string mensaje { get; set; }
        public List<EspecialidadModel> datos { get; set; }
    }
}
