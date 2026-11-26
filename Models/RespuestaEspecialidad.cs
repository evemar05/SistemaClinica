namespace Clinica.Models
{
    public class RespuestaEspecialidad
    {
        public int estatus { get; set; }
        public string mensaje { get; set; }
        public EspecialidadModel datos { get; set; }
    }
}
