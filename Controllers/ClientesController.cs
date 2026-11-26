using Clinica.Ayudas;
using Clinica.Models;
using Microsoft.AspNetCore.Mvc;
using System.Text.Json;

namespace Clinica.Controllers
{
    public class ClientesController : Controller
    {
        public IActionResult Index()
        {
            SocketPagina socket = new SocketPagina();
            string json = "{\"accion\":\"listarClientes\"}";

            string respuesta = socket.EnviarPeticion(json);
            Models.RespuestaClientes clientes = JsonSerializer.Deserialize<Models.RespuestaClientes>(respuesta);

            return View(clientes.datos);        

        }

        [HttpGet]
        public IActionResult Crear(){
            return View();
        }


        [HttpPost]
        public IActionResult Crear(ClientesModel cliente)
        {
            if (!ModelState.IsValid) { 
                return View();
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

            if (resultado.estatus == 0)
            {
                return RedirectToAction("Index");
            }

            ViewBag.Error = resultado.mensaje;

            return View(cliente);

        }


        [HttpGet]
        public IActionResult Editar(string id)
        {
            SocketPagina socket = new SocketPagina();

            string json =$@"{{""accion"":""buscar_cliente"",""identificacion"":""{id}""}}";
            string respuesta = socket.EnviarPeticion(json);
            var resultado = JsonSerializer.Deserialize<RespuestaCliente>(respuesta);

            if (resultado.estatus != 0)
            {
                return RedirectToAction("Index");
            }

            return View(resultado.datos);
        }


        [HttpPost]
        public IActionResult Editar(ClientesModel cliente)
        {
            SocketPagina socket = new SocketPagina();

            string json = $@"{{
            ""accion"":""modificar_cliente"",
            ""identificacion"":""{cliente.identificacion}"",
            ""nacionalidad"":""{cliente.nacionalidad}"",
            ""nombre"":""{cliente.nombre}"",
            ""primerApellido"":""{cliente.primerApellido}"",
            ""segundoApellido"":""{cliente.segundoApellido}"",
            ""telefono"":""{cliente.telefono}"",
            ""email"":""{cliente.email}""}}";

            string respuesta = socket.EnviarPeticion(json);

            if (HttpContext.Session.GetString("rol") == "cliente")
            {
                return RedirectToAction("Index", "Menu");
            }

            return RedirectToAction("Index");
        }


        [HttpGet]
        public IActionResult Eliminar(string id)
        {
            SocketPagina socket = new SocketPagina();

            string json =$@"{{
            ""accion"":""buscar_cliente"",
            ""identificacion"":""{id}""}}";

            string respuesta = socket.EnviarPeticion(json);

            var resultado = JsonSerializer.Deserialize<RespuestaCliente>(respuesta);

            return View(resultado.datos);
        }


        [HttpPost]
        public IActionResult Eliminar(ClientesModel cliente)
        {
            SocketPagina socket =new SocketPagina();

            string json = $@"{{
            ""accion"":""eliminar_cliente"",
            ""identificacion"":""{cliente.identificacion}""}}";

            socket.EnviarPeticion(json);

            return RedirectToAction("Index");
        }

        [HttpPost]
        public IActionResult CambiarEstado(string identificacion, bool estadoActual)
        {
            SocketPagina socket = new SocketPagina();

            string json = $@"{{
            ""accion"":""cambiar_estado_cliente"",
            ""identificacion"":""{identificacion}"",
            ""estado"":{(!estadoActual ? "true" : "false")}}}";

            socket.EnviarPeticion(json);

            return RedirectToAction("Index");
        }
    }
}
