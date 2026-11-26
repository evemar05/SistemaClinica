using Clinica.Models;

namespace Clinica.Models
{
    public class RespuestaCliente
    {
        public int estatus { get; set; }

        public string mensaje { get; set; }

        public ClientesModel datos { get; set; }

    }
}