namespace Clinica.Models
{
    public class RespuestaEmpleado
    {
        public int estatus { get; set; }
        public string mensaje { get; set; }
        public EmpleadoModel datos { get; set; }
    }
}
