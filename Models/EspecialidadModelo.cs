using System.ComponentModel.DataAnnotations;

namespace Clinica.Models
{
    public class EspecialidadModel
    {
        [Required(ErrorMessage = "El nombre es obligatorio")]
        public string nombre { get; set; }

        [Required(ErrorMessage = "La descripción es obligatoria")]
        public string descripcion { get; set; }
    }
}
