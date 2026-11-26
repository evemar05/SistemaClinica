using Microsoft.AspNetCore.Mvc;
using System.Text.Json;
using Clinica.Ayudas;
using Clinica.Models;

namespace Clinica.Controllers
{
    public class MedicosController : Controller
    {
        public IActionResult Index()
        {
            SocketPagina socket = new SocketPagina();

            string json = @"{""accion"":""listar_medicos""}";

            string respuesta = socket.EnviarPeticion(json);

            RespuestaMedicos medicos = JsonSerializer.Deserialize<RespuestaMedicos>(respuesta);

            return View(
                medicos.datos
            );
        }

        [HttpGet]
        public IActionResult Crear()
        {
            return View();
        }


        [HttpPost]
        public IActionResult Crear(MedicoModel medico)
        {
            if (!ModelState.IsValid)
            {
                return View(medico);
            }

            SocketPagina socket =
                new SocketPagina();

            string json = $@"{{
                ""accion"":""registrar_medico"",
                ""identificacion"":""{medico.identificacion}"",
                ""nombre"":""{medico.nombre}"",
                ""telefono"":""{medico.telefono}"",
                ""email"":""{medico.email}"",
                ""especialidad"":""{medico.especialidad}""
            }}";

            string respuesta =
                socket.EnviarPeticion(json);

            RespuestaMedico resultado =JsonSerializer.Deserialize<RespuestaMedico>(respuesta);

            if (resultado.estatus == 0)
            {
                return RedirectToAction(
                    "Index"
                );
            }

            ViewBag.Error = resultado.mensaje;

            return View(medico);
        }


        [HttpGet]
        public IActionResult Editar(string id)
        {
            SocketPagina socket = new SocketPagina();

            string json = $@"{{
                ""accion"":""buscar_medico"",
                ""identificacion"":""{id}""}}";

            string respuesta = socket.EnviarPeticion(json);

            RespuestaMedico resultado = JsonSerializer.Deserialize<RespuestaMedico>(respuesta);

            if (resultado.estatus != 0)
            {
                return RedirectToAction("Index");
            }

            return View(
                resultado.datos
            );
        }


        [HttpPost]
        public IActionResult Editar(MedicoModel medico)
        {
            SocketPagina socket = new SocketPagina();

            string json = $@"{{
                ""accion"":""modificar_medico"",
                ""identificacion"":""{medico.identificacion}"",
                ""nombre"":""{medico.nombre}"",
                ""telefono"":""{medico.telefono}"",
                ""email"":""{medico.email}"",
                ""especialidad"":""{medico.especialidad}""
            }}";

            socket.EnviarPeticion(json);

            return RedirectToAction(
                "Index"
            );
        }


        [HttpGet]
        public IActionResult Eliminar(string id)
        {
            SocketPagina socket = new SocketPagina();

            string json = $@"{{
                ""accion"":""buscar_medico"",
                ""identificacion"":""{id}""
                }}";

            string respuesta = socket.EnviarPeticion(json);

            RespuestaMedico resultado = JsonSerializer.Deserialize<RespuestaMedico>(respuesta);

            return View(resultado.datos);
        }


        [HttpPost]
        public IActionResult Eliminar(MedicoModel medico)
        {
            SocketPagina socket = new SocketPagina();

            string json = $@"{{
                ""accion"":""eliminar_medico"",
                ""identificacion"":""{medico.identificacion}""
                }}";

            socket.EnviarPeticion(json);

            return RedirectToAction("Index");
        }
    }
}