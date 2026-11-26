using System.ComponentModel.DataAnnotations;

namespace Clinica.Models
{
    public class CitaModel
    {
        public int idCita { get; set; }

        [Required(ErrorMessage = "El cliente es obligatorio")]
        public string idCliente { get; set; }

        [Required(ErrorMessage = "El médico es obligatorio")]
        public string idMedico { get; set; }

        [Required(ErrorMessage = "La fecha es obligatoria")]
        public string fecha { get; set; }

        [Required(ErrorMessage = "La hora de inicio es obligatoria")]
        public string horaInicio { get; set; }

        [Required(ErrorMessage = "La hora de fin es obligatoria")]
        public string horaFin { get; set; }

        public string estado { get; set; }
    }
}
