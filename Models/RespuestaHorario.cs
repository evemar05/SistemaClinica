namespace Clinica.Models
{
    public class RespuestaHorario
    {
        public int estatus { get; set; }

        public string mensaje { get; set; }

        public HorarioModel datos { get; set; }
    }
}