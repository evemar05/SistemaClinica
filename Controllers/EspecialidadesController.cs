using Clinica.Ayudas;
using Clinica.Models;
using Microsoft.AspNetCore.Mvc;
using System.Text.Json;

namespace Clinica.Controllers
{
    public class EspecialidadesController : Controller
    {
        public IActionResult Index()
        {
            SocketPagina socket = new SocketPagina();
            string json = "{\"accion\":\"listar_especialidades\"}";

            string respuesta = socket.EnviarPeticion(json);
            RespuestaEspecialidades especialidades = JsonSerializer.Deserialize<RespuestaEspecialidades>(respuesta);

            return View(especialidades.datos);
        }

        [HttpGet]
        public IActionResult Crear()
        {
            return View();
        }

        [HttpPost]
        public IActionResult Crear(EspecialidadModel especialidad)
        {
            if (!ModelState.IsValid)
            {
                return View(especialidad);
            }

            SocketPagina socket = new SocketPagina();

            string json = $@"{{
                ""accion"":""registrar_especialidad"",
                ""nombre"":""{especialidad.nombre}"",
                ""descripcion"":""{especialidad.descripcion}""
            }}";

            string respuesta = socket.EnviarPeticion(json);
            RespuestaEspecialidad resultado = JsonSerializer.Deserialize<RespuestaEspecialidad>(respuesta);

            if (resultado.estatus == 0)
            {
                return RedirectToAction("Index");
            }

            ViewBag.Error = resultado.mensaje;
            return View(especialidad);
        }

        [HttpGet]
        public IActionResult Editar(string id)
        {
            SocketPagina socket = new SocketPagina();

            string json = $@"{{""accion"":""buscar_especialidad"",""nombre"":""{id}""}}";
            string respuesta = socket.EnviarPeticion(json);

            RespuestaEspecialidad resultado = JsonSerializer.Deserialize<RespuestaEspecialidad>(respuesta);

            if (resultado.estatus != 0)
            {
                return RedirectToAction("Index");
            }

            return View(resultado.datos);
        }

        [HttpPost]
        public IActionResult Editar(EspecialidadModel especialidad)
        {
            SocketPagina socket = new SocketPagina();

            string json = $@"{{
                ""accion"":""modificar_especialidad"",
                ""nombre"":""{especialidad.nombre}"",
                ""descripcion"":""{especialidad.descripcion}""
            }}";

            socket.EnviarPeticion(json);

            return RedirectToAction("Index");
        }

        [HttpGet]
        public IActionResult Eliminar(string id)
        {
            SocketPagina socket = new SocketPagina();

            string json = $@"{{""accion"":""buscar_especialidad"",""nombre"":""{id}""}}";
            string respuesta = socket.EnviarPeticion(json);

            RespuestaEspecialidad resultado = JsonSerializer.Deserialize<RespuestaEspecialidad>(respuesta);

            return View(resultado.datos);
        }

        [HttpPost]
        public IActionResult Eliminar(EspecialidadModel especialidad)
        {
            SocketPagina socket = new SocketPagina();

            string json = $@"{{""accion"":""eliminar_especialidad"",""nombre"":""{especialidad.nombre}""}}";

            socket.EnviarPeticion(json);

            return RedirectToAction("Index");
        }
    }
}
