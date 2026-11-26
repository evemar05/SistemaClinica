using Clinica.Ayudas;
using Clinica.Models;
using Microsoft.AspNetCore.Mvc;
using System.Text.Json;

namespace Clinica.Controllers
{
    public class EmpleadosController : Controller
    {
        public IActionResult Index()
        {
            SocketPagina socket = new SocketPagina();
            string json = "{\"accion\":\"listar_empleados\"}";

            string respuesta = socket.EnviarPeticion(json);
            RespuestaEmpleados empleados = JsonSerializer.Deserialize<RespuestaEmpleados>(respuesta);

            return View(empleados.datos);
        }

        [HttpGet]
        public IActionResult Crear()
        {
            return View();
        }

        [HttpPost]
        public IActionResult Crear(EmpleadoModel empleado)
        {
            if (!ModelState.IsValid)
            {
                return View(empleado);
            }

            SocketPagina socket = new SocketPagina();

            string identificacionRegistrador = HttpContext.Session.GetString("identificacion") ?? "";   // Usuario Activo

            string json = $@"{{
                ""accion"":""registrar_empleado"",
                ""identificacionRegistrador"":""{identificacionRegistrador}"",
                ""identificacion"":""{empleado.identificacion}"",
                ""nombre"":""{empleado.nombre}"",
                ""telefono"":""{empleado.telefono}"",
                ""email"":""{empleado.email}"",
                ""puesto"":""{empleado.puesto}"",
                ""usuario"":""{empleado.usuario}"",
                ""password"":""{empleado.password}""
                }}";

            string respuesta = socket.EnviarPeticion(json);
            RespuestaEmpleado resultado = JsonSerializer.Deserialize<RespuestaEmpleado>(respuesta);

            if (resultado.estatus == 0)
            {
                return RedirectToAction("Index");
            }

            ViewBag.Error = resultado.mensaje;
            return View(empleado);
        }

        [HttpGet]
        public IActionResult Editar(string id)
        {
            SocketPagina socket = new SocketPagina();

            string json = $@"{{""accion"":""buscar_empleado"",""identificacion"":""{id}""}}";
            string respuesta = socket.EnviarPeticion(json);

            RespuestaEmpleado resultado = JsonSerializer.Deserialize<RespuestaEmpleado>(respuesta);

            if (resultado.estatus != 0)
            {
                return RedirectToAction("Index");
            }

            return View(resultado.datos);
        }

        [HttpPost]
        public IActionResult Editar(EmpleadoModel empleado)
        {
            SocketPagina socket = new SocketPagina();

            string json = $@"{{
                ""accion"":""modificar_empleado"",
                ""identificacion"":""{empleado.identificacion}"",
                ""telefono"":""{empleado.telefono}"",
                ""email"":""{empleado.email}"",
                ""puesto"":""{empleado.puesto}""
            }}";

            socket.EnviarPeticion(json);

            return RedirectToAction("Index");
        }

        [HttpGet]
        public IActionResult Eliminar(string id)
        {
            SocketPagina socket = new SocketPagina();

            string json = $@"{{""accion"":""buscar_empleado"",""identificacion"":""{id}""}}";
            string respuesta = socket.EnviarPeticion(json);

            RespuestaEmpleado resultado = JsonSerializer.Deserialize<RespuestaEmpleado>(respuesta);

            return View(resultado.datos);
        }

        [HttpPost]
        public IActionResult Eliminar(EmpleadoModel empleado)
        {
            SocketPagina socket = new SocketPagina();

            string json = $@"{{""accion"":""eliminar_empleado"",""identificacion"":""{empleado.identificacion}""}}";

            socket.EnviarPeticion(json);

            return RedirectToAction("Index");
        }

        [HttpPost]
        public IActionResult CambiarEstado(string identificacion, bool estadoActual)
        {
            SocketPagina socket = new SocketPagina();

            string json = $@"{{
            ""accion"":""cambiar_estado_empleado"",
            ""identificacion"":""{identificacion}"",
            ""estado"":{(!estadoActual ? "true" : "false")}}}";

            socket.EnviarPeticion(json);

            return RedirectToAction("Index");
        }
    }
}
