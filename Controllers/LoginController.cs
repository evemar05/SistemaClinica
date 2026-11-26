using Microsoft.AspNetCore.Mvc;
using System.Text.Json;
using Clinica.Models;
using Clinica.Ayudas;


namespace Clinica.Controllers
{
    public class LoginController : Controller
    {
        [HttpGet]
        public IActionResult Index()
        {
            return View();
        }
        [HttpPost]
        public IActionResult Index(LoginModelo modelo) { 
            SocketPagina socket = new SocketPagina();

            string json = JsonSerializer.Serialize(new { accion = "login", usuario = modelo.Usuario, password = modelo.Password });
            string respuesta = socket.EnviarPeticion(json);

            RespuestaLogin resultado = JsonSerializer.Deserialize<RespuestaLogin>(respuesta);

            if (resultado != null && resultado.estatus == 0)
            {
                HttpContext.Session.SetString("usuario", resultado.datos.usuario);
                HttpContext.Session.SetString("rol", resultado.datos.rol);
                HttpContext.Session.SetString("identificacion", resultado.datos.identificacion);

                return RedirectToAction("Index","Menu");
            }

            ViewBag.Error = resultado != null ? resultado.mensaje : "Usuario o contraseña incorrectos";

            return View(modelo);
        }

        [HttpGet]
        public IActionResult Registro()
        {
            return View();
        }

        [HttpPost]
        public IActionResult Registro(ClientesModel cliente)
        {
            if (!ModelState.IsValid)
            {
                return View(cliente);
            }

            SocketPagina socket = new SocketPagina();

            string json = $@"{{
            ""accion"":""registrar_cliente"",
            ""identificacion"":""{cliente.identificacion}"",
            ""nacionalidad"":""{cliente.nacionalidad}"",
            ""nombre"":""{cliente.nombre}"",
            ""primerApellido"":""{cliente.primerApellido}"",
            ""segundoApellido"":""{cliente.segundoApellido}"",
            ""telefono"":""{cliente.telefono}"",
            ""email"":""{cliente.email}"",
            ""usuario"":""{cliente.usuario}"",
            ""password"":""{cliente.password}"",
            ""padecimientos"":[]}}";

            string respuesta = socket.EnviarPeticion(json);
            var resultado = JsonSerializer.Deserialize<RespuestaClientes>(respuesta);

            if (resultado != null && resultado.estatus == 0)
            {
                return RedirectToAction("Index");
            }

            ViewBag.Error = resultado != null ? resultado.mensaje : "No fue posible completar el registro";

            return View(cliente);
        }

        public IActionResult Salir()
        {
            HttpContext.Session.Clear();
            return RedirectToAction("Index");
        }
    }
}
