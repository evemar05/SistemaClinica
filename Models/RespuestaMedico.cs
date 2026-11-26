namespace Clinica.Models
{
    public class RespuestaMedico
    {
        public int estatus { get; set; }

        public string mensaje { get; set; }

        public MedicoModel datos { get; set; }
    }
}