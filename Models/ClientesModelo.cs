using System.ComponentModel.DataAnnotations;
using System.Runtime.CompilerServices;

namespace Clinica.Models
{
    public class ClientesModel
    {
        [Required (ErrorMessage = "La identificacion es obligatoria.")]
        [RegularExpression(@"^[0-9]+$",ErrorMessage = "La identificación debe contener solo números")]
        public string identificacion { get; set; }

        [Required(ErrorMessage = "La nacionalidad es obligatoria.")]
        public string nacionalidad { get; set; }

        [Required(ErrorMessage ="El nombre es obligatorio.")]
        public string nombre    { get; set; }

        [Required(ErrorMessage ="El primer apellido es obligatorio.")]
        public string primerApellido { get; set; }

        [Required(ErrorMessage = "El segundo apellido es obligatorio.")]  
        public string segundoApellido { get; set; }

        [Required(ErrorMessage ="El telefono es obligatorio.")]
        [RegularExpression(@"^[0-9]+$",ErrorMessage = "El telefono debe contener solo números")]
        public string telefono { get; set; }

        [Required]
        [EmailAddress(ErrorMessage = "Debe ingresar un correo válido")]
        public string email { get; set; }

        public bool estado { get; set; }

        public string usuario { get; set; }
        public string password { get; set; }
    }
}
