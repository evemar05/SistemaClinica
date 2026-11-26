using System.ComponentModel.DataAnnotations;

namespace Clinica.Models
{
    public class HorarioModel
    {
        [Required]
        public string identificacionMedico { get; set; }

        [Required]
        public string diaSemana { get; set; }

        [Required]
        public string horaInicio { get; set; }

        [Required]
        public string horaFin { get; set; }
    }
} 