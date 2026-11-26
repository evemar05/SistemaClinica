using System.ComponentModel.DataAnnotations;

namespace Clinica.Models
{
    public class LoginModelo
    {
        [Required]
        public string Usuario { get; set; }
        [Required]
        public string Password { get; set; }
    }
}
