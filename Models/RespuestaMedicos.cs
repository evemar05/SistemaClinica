namespace Clinica.Models
{
    public class RespuestaMedicos
    {
        public int estatus { get; set; }

        public string mensaje { get; set; }

        public List<MedicoModel> datos { get; set; }
    }
}