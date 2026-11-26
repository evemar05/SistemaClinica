using System.ComponentModel.DataAnnotations;

namespace Clinica.Models
{
    public class MedicoModel
    {
        [Required(ErrorMessage = "La identificación es obligatoria")]
        [RegularExpression(@"^[0-9]+$",
            ErrorMessage = "La identificación debe contener solo números")]
        public string identificacion { get; set; }

        [Required(ErrorMessage = "El nombre es obligatorio")]
        public string nombre { get; set; }

        [Required(ErrorMessage = "El teléfono es obligatorio")]
        [RegularExpression(@"^[0-9]+$",
            ErrorMessage = "El teléfono solo puede contener números")]
        public string telefono { get; set; }

        [Required(ErrorMessage = "El correo es obligatorio")]
        [EmailAddress(ErrorMessage = "Debe ingresar un correo válido")]
        public string email { get; set; }

        [Required(ErrorMessage = "La especialidad es obligatoria")]
        public string especialidad { get; set; }
    }
}