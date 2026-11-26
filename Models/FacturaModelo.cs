using System.ComponentModel.DataAnnotations;

namespace Clinica.Models
{
    public class FacturaModel
    {
        public int idFactura { get; set; }

        [Required(ErrorMessage = "La cita es obligatoria")]
        public int idCita { get; set; }

        [Required(ErrorMessage = "El servicio es obligatorio")]
        public string servicio { get; set; }

        [Required(ErrorMessage = "El precio es obligatorio")]
        public decimal precio { get; set; }

        public decimal iva { get; set; }

        public decimal total { get; set; }

        public string estadoPago { get; set; }
    }
}
