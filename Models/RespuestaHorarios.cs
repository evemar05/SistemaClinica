namespace Clinica.Models
{
    public class RespuestaHorarios
    {
        public int estatus { get; set; }

        public string mensaje { get; set; }

        public List<HorarioModel> datos { get; set; }
    }
}