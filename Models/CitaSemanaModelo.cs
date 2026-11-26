namespace Clinica.Models
{
    public class CitaSemanaModel
    {
        public int idCita { get; set; }
        public string fecha { get; set; }
        public string horaInicio { get; set; }
        public string horaFin { get; set; }
        public string estado { get; set; }
        public string identificacionCliente { get; set; }
        public string nombreCliente { get; set; }
        public string telefonoCliente { get; set; }
        public string emailCliente { get; set; }
    }

    public class HorarioSemanaModel
    {
        public string inicioSemana { get; set; }
        public string finSemana { get; set; }
        public List<CitaSemanaModel> citas { get; set; }
    }

    public class RespuestaHorarioSemana
    {
        public int estatus { get; set; }
        public string mensaje { get; set; }
        public HorarioSemanaModel datos { get; set; }
    }

    public class OcupadaModel
    {
        public string fecha { get; set; }
        public string horaInicio { get; set; }
    }

    public class DisponibilidadSemanaModel
    {
        public string inicioSemana { get; set; }
        public string finSemana { get; set; }
        public List<HorarioModel> horario { get; set; }
        public List<OcupadaModel> ocupadas { get; set; }
    }

    public class RespuestaDisponibilidad
    {
        public int estatus { get; set; }
        public string mensaje { get; set; }
        public DisponibilidadSemanaModel datos { get; set; }
    }
}
