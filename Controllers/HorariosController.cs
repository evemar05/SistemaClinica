using Microsoft.AspNetCore.Mvc;
using System.Text.Json;
using Clinica.Ayudas;
using Clinica.Models;

namespace Clinica.Controllers
{
    public class HorariosController : Controller
    {
        public IActionResult Index()
        {
            SocketPagina socket = new SocketPagina();

            string json = @"{""accion"":""listar_horarios""}";

            string respuesta = socket.EnviarPeticion(json);

            RespuestaHorarios horarios = JsonSerializer.Deserialize<RespuestaHorarios>(respuesta);

            return View(horarios.datos);
        }

        [HttpGet]
        public IActionResult Crear()
        {
            return View();
        }


        [HttpPost]
        public IActionResult Crear(HorarioModel horario)
        {
            if (!ModelState.IsValid)
            {
                return View(horario);
            }

            SocketPagina socket = new SocketPagina();

            string json = $@"{{
                ""accion"":""registrar_horario"",
                ""identificacionMedico"":""{horario.identificacionMedico}"",
                ""diaSemana"":""{horario.diaSemana}"",
                ""horaInicio"":""{horario.horaInicio}"",
                ""horaFin"":""{horario.horaFin}""
                }}";

            string respuesta = socket.EnviarPeticion(json);

            return RedirectToAction("Index");
        }

        [HttpGet]
        public IActionResult Editar(string id)
        {
            SocketPagina socket = new SocketPagina();

            string json = $@"{{
                ""accion"":""buscar_horario"",
                ""identificacionMedico"":""{id}""
                }}";

            string respuesta = socket.EnviarPeticion(json);

            RespuestaHorarios resultado = JsonSerializer.Deserialize<RespuestaHorarios>(respuesta);

            if (resultado == null || resultado.datos.Count == 0)
            {
                return RedirectToAction("Index");
            }

            return View(resultado.datos.First());
        }

        [HttpPost]
        public IActionResult Editar(HorarioModel horario)
        {
            SocketPagina socket = new SocketPagina();

            string json = $@"{{
                ""accion"":""modificar_horario"",
                ""identificacionMedico"":""{horario.identificacionMedico}"",
                ""diaSemana"":""{horario.diaSemana}"",
                ""horaInicio"":""{horario.horaInicio}"",
                ""horaFin"":""{horario.horaFin}""
                }}";

            socket.EnviarPeticion(json);

            return RedirectToAction("Index");
        }


        [HttpGet]
        public IActionResult Eliminar(string id)
        {
            SocketPagina socket = new SocketPagina();

            string json = $@"{{
                ""accion"":""buscar_horario"",
                ""identificacionMedico"":""{id}""
                }}";

            string respuesta = socket.EnviarPeticion(json);

            RespuestaHorarios resultado = JsonSerializer.Deserialize<RespuestaHorarios>(respuesta);

            if ( resultado == null ||resultado.datos.Count == 0)
            {
                return RedirectToAction("Index");
            }

            return View(resultado.datos.First());
        }

        [HttpPost]
        public IActionResult Eliminar(HorarioModel horario)
        {
            SocketPagina socket = new SocketPagina();

            string json = $@"{{
                ""accion"":""eliminar_horario"",
                ""identificacionMedico"":""{horario.identificacionMedico}""
                }}";

            socket.EnviarPeticion(json);

            return RedirectToAction("Index");
        }
    }
}