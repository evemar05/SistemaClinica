using Clinica.Ayudas;
using Clinica.Models;
using Microsoft.AspNetCore.Mvc;
using System.Text.Json;
using Microsoft.AspNetCore.Http;

namespace Clinica.Controllers
{
    public class CitasController : Controller
    {
        public IActionResult Index()
        {
            SocketPagina socket = new SocketPagina();
            string json = "{\"accion\":\"listar_citas\"}";

            string respuesta = socket.EnviarPeticion(json);
            RespuestaCitas citas = JsonSerializer.Deserialize<RespuestaCitas>(respuesta);

            return View(citas.datos);
        }

        [HttpGet]
        public IActionResult Crear()
        {
            return View();
        }

        [HttpPost]
        public IActionResult Crear(CitaModel cita)
        {
            if (!ModelState.IsValid)
            {
                return View(cita);
            }

            SocketPagina socket = new SocketPagina();

            string json = $@"{{
                ""accion"":""crear_cita"",
                ""idCliente"":""{cita.idCliente}"",
                ""idMedico"":""{cita.idMedico}"",
                ""fecha"":""{cita.fecha}"",
                ""horaInicio"":""{cita.horaInicio}"",
                ""horaFin"":""{cita.horaFin}""
            }}";

            string respuesta = socket.EnviarPeticion(json);
            RespuestaCita resultado = JsonSerializer.Deserialize<RespuestaCita>(respuesta);

            if (resultado.estatus == 0)
            {
                return RedirectToAction("Index");
            }

            ViewBag.Error = resultado.mensaje;
            return View(cita);
        }

        [HttpGet]
        public IActionResult Editar(int id)
        {
            SocketPagina socket = new SocketPagina();

            string json = $@"{{""accion"":""buscar_cita"",""idCita"":{id}}}";
            string respuesta = socket.EnviarPeticion(json);

            RespuestaCita resultado = JsonSerializer.Deserialize<RespuestaCita>(respuesta);

            if (resultado.estatus != 0)
            {
                return RedirectToAction("Index");
            }

            return View(resultado.datos);
        }

        [HttpPost]
        public IActionResult Editar(CitaModel cita)
        {
            SocketPagina socket = new SocketPagina();

            string json = $@"{{
                ""accion"":""modificar_cita"",
                ""idCita"":{cita.idCita},
                ""fecha"":""{cita.fecha}"",
                ""horaInicio"":""{cita.horaInicio}"",
                ""horaFin"":""{cita.horaFin}""
                }}";

            string respuesta = socket.EnviarPeticion(json);
            RespuestaCita resultado = JsonSerializer.Deserialize<RespuestaCita>(respuesta);

            if (resultado.estatus != 0)
            {
                ViewBag.Error = resultado.mensaje;
                return View(cita);
            }

            return RedirectToAction("Index");
        }

        [HttpGet]
        public IActionResult Cancelar(int id)
        {
            SocketPagina socket = new SocketPagina();

            string json = $@"{{""accion"":""buscar_cita"",""idCita"":{id}}}";
            string respuesta = socket.EnviarPeticion(json);

            RespuestaCita resultado = JsonSerializer.Deserialize<RespuestaCita>(respuesta);

            string idClienteSesion = HttpContext.Session.GetString("identificacion");
            if (HttpContext.Session.GetString("rol") == "cliente" && resultado.datos.idCliente != idClienteSesion)
            {
                return RedirectToAction("MisCitas");
            }

            return View(resultado.datos);
        }

        [HttpPost]
        public IActionResult Cancelar(CitaModel cita)
        {
            string idClienteSesion = HttpContext.Session.GetString("identificacion");
            if (HttpContext.Session.GetString("rol") == "cliente" && cita.idCliente != idClienteSesion)
            {
                return RedirectToAction("MisCitas");
            }

            SocketPagina socket = new SocketPagina();

            string json = $@"{{""accion"":""cancelar_cita"",""idCita"":{cita.idCita}}}";
            string respuesta = socket.EnviarPeticion(json);
            RespuestaCita resultado = JsonSerializer.Deserialize<RespuestaCita>(respuesta);

            if (resultado.estatus != 0)
            {
                ViewBag.Error = resultado.mensaje;
                return View(cita);
            }

            bool esCliente = HttpContext.Session.GetString("rol") == "cliente";
            return RedirectToAction(esCliente ? "MisCitas" : "Index");
        }

        [HttpGet]
        public IActionResult SemanaBuscar(string criterio)
        {
            if (string.IsNullOrWhiteSpace(criterio))
            {
                return View(new List<MedicoModel>());
            }

            SocketPagina socket = new SocketPagina();
            string json = "{\"accion\":\"listar_medicos\"}";
            string respuesta = socket.EnviarPeticion(json);
            RespuestaMedicos medicos = JsonSerializer.Deserialize<RespuestaMedicos>(respuesta);

            var resultado = medicos.datos.Where(m =>
                m.identificacion.Contains(criterio, StringComparison.OrdinalIgnoreCase) ||
                m.nombre.Contains(criterio, StringComparison.OrdinalIgnoreCase) ||
                m.especialidad.Contains(criterio, StringComparison.OrdinalIgnoreCase)).ToList();

            return View(resultado);
        }

        [HttpGet]
        public IActionResult Semana(string idMedico, string fecha)
        {
            if (string.IsNullOrEmpty(fecha))
            {
                fecha = DateTime.Now.ToString("yyyy-MM-dd");
            }

            SocketPagina socket = new SocketPagina();
            string json = $@"{{""accion"":""listar_citas_medico_semana"",""idMedico"":""{idMedico}"",""fecha"":""{fecha}""}}";
            string respuesta = socket.EnviarPeticion(json);

            RespuestaHorarioSemana resultado = JsonSerializer.Deserialize<RespuestaHorarioSemana>(respuesta);

            ViewBag.IdMedico = idMedico;
            ViewBag.Fecha = fecha;

            if (resultado.estatus != 0)
            {
                ViewBag.Error = resultado.mensaje;
                return View(new HorarioSemanaModel());
            }

            return View(resultado.datos);
        }

        [HttpGet]
        public IActionResult Especialidades()
        {
            SocketPagina socket = new SocketPagina();
            string json = "{\"accion\":\"listar_especialidades\"}";
            string respuesta = socket.EnviarPeticion(json);

            RespuestaEspecialidades resultado = JsonSerializer.Deserialize<RespuestaEspecialidades>(respuesta);
            return View(resultado.datos);
        }

        [HttpGet]
        public IActionResult MedicosPorEspecialidad(string especialidad)
        {
            SocketPagina socket = new SocketPagina();
            string json = $@"{{""accion"":""listar_medicos_especialidad"",""especialidad"":""{especialidad}""}}";
            string respuesta = socket.EnviarPeticion(json);

            RespuestaMedicos resultado = JsonSerializer.Deserialize<RespuestaMedicos>(respuesta);
            return View(resultado.datos);
        }

        [HttpGet]
        public IActionResult Disponibilidad(string idMedico, string fecha)
        {
            if (string.IsNullOrEmpty(fecha))
            {
                fecha = DateTime.Now.ToString("yyyy-MM-dd");
            }

            SocketPagina socket = new SocketPagina();
            string json = $@"{{""accion"":""disponibilidad_semana"",""idMedico"":""{idMedico}"",""fecha"":""{fecha}""}}";
            string respuesta = socket.EnviarPeticion(json);

            RespuestaDisponibilidad resultado = JsonSerializer.Deserialize<RespuestaDisponibilidad>(respuesta);

            ViewBag.IdMedico = idMedico;
            ViewBag.Fecha = fecha;

            if (resultado.estatus != 0)
            {
                ViewBag.Error = resultado.mensaje;
                return View(new DisponibilidadSemanaModel());
            }

            return View(resultado.datos);
        }

        [HttpGet]
        public IActionResult Agendar(string idMedico, string fecha)
        {
            var cita = new CitaModel { idMedico = idMedico, fecha = fecha };
            return View(cita);
        }

        [HttpPost]
        public IActionResult Agendar(CitaModel cita)
        {
            string identificacionCliente = HttpContext.Session.GetString("identificacion");

            if (string.IsNullOrEmpty(identificacionCliente))
            {
                return RedirectToAction("Index", "Login");
            }

            SocketPagina socket = new SocketPagina();

            string json = $@"{{
                ""accion"":""crear_cita"",
                ""idCliente"":""{identificacionCliente}"",
                ""idMedico"":""{cita.idMedico}"",
                ""fecha"":""{cita.fecha}"",
                ""horaInicio"":""{cita.horaInicio}"",
                ""horaFin"":""{cita.horaFin}""
            }}";

            string respuesta = socket.EnviarPeticion(json);
            RespuestaCita resultado = JsonSerializer.Deserialize<RespuestaCita>(respuesta);

            if (resultado.estatus != 0)
            {
                ViewBag.Error = resultado.mensaje;
                return View(cita);
            }

            return RedirectToAction("MisCitas");
        }

        [HttpGet]
        public IActionResult MisCitas()
        {
            string identificacionCliente = HttpContext.Session.GetString("identificacion");

            if (string.IsNullOrEmpty(identificacionCliente))
            {
                return RedirectToAction("Index", "Login");
            }

            SocketPagina socket = new SocketPagina();
            string json = $@"{{""accion"":""listar_citas_cliente"",""idCliente"":""{identificacionCliente}""}}";
            string respuesta = socket.EnviarPeticion(json);

            RespuestaCitas resultado = JsonSerializer.Deserialize<RespuestaCitas>(respuesta);
            return View(resultado.datos);
        }

        [HttpGet]
        public IActionResult CancelarPropia(int id)
        {
            return RedirectToAction("Cancelar", new { id });
        }
    }
}
