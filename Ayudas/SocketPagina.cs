using System.Net.Sockets;
using System.Text;


namespace Clinica.Ayudas
{
    public class SocketPagina
    {
        private string host = "localhost";
        private int puerto = 8000;

        public string EnviarPeticion(string json)
        {
            try
            {
                using (TcpClient cliente = new TcpClient())
                {
                    cliente.Connect(host,puerto);
                    NetworkStream stream = cliente.GetStream();
                    byte[] datosEnviar = Encoding.UTF8.GetBytes(json);
                    stream.Write(datosEnviar,0,datosEnviar.Length);
                    byte[] buffer = new byte[4096];
                    int bytesRecibidos = stream.Read(buffer, 0, buffer.Length);
                    string respuesta = Encoding.UTF8.GetString(buffer, 0, bytesRecibidos);
                    return respuesta;

                }
            }
            catch (Exception ex)
            {
                return "{\"estatus\":-1,\"mensaje\":\"" + ex.Message + "\"}";
            }
        }
    }
}

