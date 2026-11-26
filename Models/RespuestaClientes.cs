using static System.Runtime.InteropServices.JavaScript.JSType;

namespace Clinica.Models
{
    public class RespuestaClientes
    {
        public int estatus { get; set; }
        public string mensaje { get; set; }
        public List<ClientesModel> datos { get; set; }
    }
}
