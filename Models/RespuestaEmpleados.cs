namespace Clinica.Models
{
    public class RespuestaEmpleados
    {
        public int estatus { get; set; }
        public string mensaje { get; set; }
        public List<EmpleadoModel> datos { get; set; }
    }
}
